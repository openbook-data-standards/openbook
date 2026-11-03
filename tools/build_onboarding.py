"""Build and statically check informational onboarding assets; never run project tests."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/ecosystem.json"
SKILLS = ROOT / ".devin/skills"
DOCS = ("docs/onboarding.md", "docs/agent-skills.md", "docs/extending-ecosystem.md")


def load_catalog() -> dict:
    data = json.loads(CATALOG.read_text())
    schema = json.loads((ROOT / "docs/ecosystem.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    if date.fromisoformat(data["reviewed_on"]) > datetime.now(UTC).date():
        raise ValueError("Catalog review date is in the future")
    projects = {p["id"] for p in data["projects"]}
    blockers = {b["id"] for b in data["blockers"]}
    if len(projects) != len(data["projects"]) or len(blockers) != len(data["blockers"]):
        raise ValueError("Duplicate project or blocker id")
    for project in data["projects"]:
        if project["skill"] not in data["skills"]:
            raise ValueError(f"Unknown skill: {project['id']}")
        if not set(project["related_projects"]) <= projects - {project["id"]}:
            raise ValueError(f"Unknown/self-related project: {project['id']}")
        if not set(project["blockers"]) <= blockers:
            raise ValueError(f"Unknown blocker: {project['id']}")
        for source in project["sources"]:
            parts = urlsplit(source).path.strip("/").split("/")
            if len(parts) < 5 or parts[:4] != ["openbook-data-standards", project["id"], "blob", "main"]:
                raise ValueError(f"Source must belong to the catalogued public project on main: {source}")
    referenced = {b for p in data["projects"] for b in p["blockers"]}
    if referenced != blockers:
        raise ValueError("Every readiness blocker must be attached to a project")
    return data


def render(data: dict) -> str:
    lines = [
        "# OpenBook ecosystem catalog",
        "",
        "Informational, not a wire specification. Generated from [ecosystem.json](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json); edit the catalog, not this page.",
        "",
        f"Bundle **{data['bundle_version']}** · reviewed **{data['reviewed_on']}**. Versions and distribution are observations, not promises of current registry availability.",
        "",
        "Start with the [onboarding guide](https://github.com/openbook-data-standards/openbook/blob/main/docs/onboarding.md), [agent setup](https://github.com/openbook-data-standards/openbook/blob/main/docs/agent-skills.md), or [extension workflow](https://github.com/openbook-data-standards/openbook/blob/main/docs/extending-ecosystem.md).",
        "",
        "Related projects below are conceptual relationships, not an install dependency graph. Standalone projects do not claim conformance to sibling standards.",
    ]
    for p in data["projects"]:
        repo = f"https://github.com/openbook-data-standards/{p['id']}"
        lines.extend([
            "", f"## {p['id']}", "", p["summary"], "",
            f"- Repository: [{p['id']}]({repo}).",
            f"- Type: {p['kind']}; maturity: {p['maturity']}.",
            f"- Version: {p['version']}.", f"- License: {p['license']}.",
            f"- Prerequisites: {'; '.join(p['prerequisites'])}.",
            f"- Distribution: {p['distribution']}",
            f"- Related projects: {', '.join(p['related_projects']) or 'standalone / none required'}.",
            f"- Agent skill: `{p['skill']}`.",
            f"- First success: {p['first_success']}",
            f"- Readiness blockers: {', '.join(p['blockers']) or 'none recorded; not a runtime certification'}.",
            "- Sources: " + " · ".join(f"[source {i}]({s})" for i, s in enumerate(p["sources"], 1)) + ".",
        ])
    lines.extend(["", "## Readiness register", "", "A skill install does not resolve these owner decisions. Do not remove a blocker until its source and distribution/compatibility evidence have been rechecked."])
    for blocker in data["blockers"]:
        lines.extend(["", f"### {blocker['id']}", "", blocker["detail"], "", f"Owner: {blocker['owner']}. Required: {blocker['requires']}."])
    return "\n".join(lines) + "\n"


def check_links(paths: list[Path]) -> None:
    for path in paths:
        text = re.sub(r"```.*?```", "", path.read_text(), flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", text):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                if url.scheme not in {"https", "mailto"}:
                    raise ValueError(f"Unsupported link scheme in {path.relative_to(ROOT)}: {target}")
                continue
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not dest.is_relative_to(ROOT) or not dest.exists():
                raise ValueError(f"Missing/outside local link in {path.relative_to(ROOT)}: {target}")
            if path.is_relative_to(SKILLS) and not dest.is_relative_to(SKILLS / path.relative_to(SKILLS).parts[0]):
                raise ValueError(f"Skill link escapes its installable bundle: {path.relative_to(ROOT)}: {target}")
            if url.fragment and dest.suffix == ".md":
                headings = re.findall(r"^#{1,6} (.+)$", dest.read_text(), re.MULTILINE)
                anchors = {re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-") for h in headings}
                if url.fragment not in anchors:
                    raise ValueError(f"Missing heading in {path.relative_to(ROOT)}: {target}")


def check_skills(data: dict) -> None:
    actual = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    if actual != set(data["skills"]):
        raise ValueError(f"Skill/catalog mismatch: {actual ^ set(data['skills'])}")
    paths = [ROOT / p for p in DOCS]
    for name in data["skills"]:
        path = SKILLS / name / "SKILL.md"
        text = path.read_text()
        header = re.match(r"\A---\nname: ([a-z-]+)\ndescription: ([^\n]+)\n---\n", text)
        if not header or header[1] != name or len(header[2]) < 30:
            raise ValueError(f"Invalid portable skill metadata: {name}")
        for section in ("## Sources", "## Workflow", "## Evidence", "## Boundaries"):
            if section not in text:
                raise ValueError(f"Missing {section}: {name}")
        if "Do not run tests locally" not in text:
            raise ValueError(f"Missing local-test boundary: {name}")
        paths.append(path)
    check_links(paths)


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if attrs.get("href"):
            self.links.append(attrs["href"])
        if attrs.get("src"):
            self.links.append(attrs["src"])


def check_site() -> None:
    for name in ("onboarding", "ecosystem", "agent-skills", "extending-ecosystem"):
        path = ROOT / f"{name}.html"
        page = PageLinks()
        page.feed(path.read_text())
        if "./onboarding.html" not in page.links:
            raise ValueError(f"Missing onboarding navigation: {path.name}")
        for target in page.links:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path
            if dest.is_dir():
                dest /= "index.html"
            if not dest.is_relative_to(ROOT) or not dest.is_file():
                raise ValueError(f"Broken rendered link in {path.name}: {target}")
            if url.fragment and dest.suffix == ".html":
                linked = PageLinks()
                linked.feed(dest.read_text())
                if url.fragment not in linked.ids:
                    raise ValueError(f"Broken rendered anchor in {path.name}: {target}")
    print("Rendered onboarding links and anchors: OK")


def check_upstream(data: dict) -> None:
    result = subprocess.run(
        ["gh", "api", "orgs/openbook-data-standards/repos?per_page=100", "--paginate", "--jq", ".[] | select(.private == false and .archived == false) | .name"],
        capture_output=True, text=True, check=True,
    )
    actual = set(result.stdout.splitlines())
    expected = {p["id"] for p in data["projects"]}
    if actual != expected:
        raise ValueError(f"Public inventory drift; uncatalogued={sorted(actual - expected)}, missing/archived={sorted(expected - actual)}")
    for project in data["projects"]:
        for source in project["sources"]:
            parts = urlsplit(source).path.strip("/").split("/")
            if len(parts) < 5 or parts[2] != "blob" or parts[3] != "main":
                raise ValueError(f"Unsupported source URL: {source}")
            endpoint = f"repos/{parts[0]}/{parts[1]}/contents/{'/'.join(parts[4:])}?ref=main"
            response = subprocess.run(["gh", "api", endpoint, "--silent"], capture_output=True, check=False)
            if response.returncode:
                raise ValueError(f"Source unavailable (check access/rate limit or moved file): {source}")
    print("Upstream inventory and source links: OK")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Read-only schema, skill, local-link and generated-content checks")
    parser.add_argument("--upstream", action="store_true", help="Also check public inventory and source links using authenticated gh; no remote writes")
    parser.add_argument("--site", action="store_true", help="Check local links and anchors in rendered onboarding pages after building the site")
    args = parser.parse_args()
    data = load_catalog()
    content = render(data)
    outputs = [ROOT / "docs/ecosystem.md", SKILLS / "openbook/references/ecosystem.md"]
    for output in outputs:
        if args.check:
            if not output.is_file() or output.read_text() != content:
                raise ValueError(f"Stale generated catalog: {output.relative_to(ROOT)}; run python3 tools/build_onboarding.py")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content)
    check_skills(data)
    check_links(outputs)
    if args.upstream:
        check_upstream(data)
    if args.site:
        check_site()
    mode = "checked" if args.check else "built"
    print(f"Onboarding {mode}: {len(data['projects'])} public projects, {len(data['skills'])} skills, {len(data['blockers'])} named owner blockers")


if __name__ == "__main__":
    main()
