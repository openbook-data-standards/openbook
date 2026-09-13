#!/usr/bin/env python3
"""Render OpenBook markdown into GitHub Pages HTML. Canonical source stays the .md files."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV = [
    ("spec.html", "Spec"),
    ("vocabularies/", "Vocabularies"),
    ("schemas.html", "Schemas"),
    ("examples.html", "Examples"),
    ("decisions.html", "Decisions"),
    ("https://github.com/openbook-data-standards/openbook", "GitHub"),
]

PAGE_MAP = {
    "spec/openbook.md": "spec.html",
    "../spec/openbook.md": "spec.html",
    "docs/decisions.md": "decisions.html",
    "../docs/decisions.md": "decisions.html",
    "docs/building-blocks.md": "building-blocks.html",
    "../docs/building-blocks.md": "building-blocks.html",
    "docs/industry-patterns.md": "industry-patterns.html",
    "../docs/industry-patterns.md": "industry-patterns.html",
    "GOVERNANCE.md": "governance.html",
    "../GOVERNANCE.md": "governance.html",
    "VERSIONING.md": "versioning.html",
    "../VERSIONING.md": "versioning.html",
    "CONTRIBUTING.md": "contributing.html",
    "../CONTRIBUTING.md": "contributing.html",
    "CHANGELOG.md": "changelog.html",
    "../CHANGELOG.md": "changelog.html",
    "vocabularies/market_types.md": "vocabularies/market-types.html",
    "../vocabularies/market_types.md": "vocabularies/market-types.html",
    "vocabularies/sports.md": "vocabularies/sports.html",
    "../vocabularies/sports.md": "vocabularies/sports.html",
    "vocabularies/segments.md": "vocabularies/segments.html",
    "../vocabularies/segments.md": "vocabularies/segments.html",
    "../vocabularies/": "vocabularies/",
    "vocabularies/": "vocabularies/",
    "../schema/": "schemas.html",
    "schema/": "schemas.html",
}


def slug(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "section"


def rewrite_href(href: str, depth: int) -> str:
    raw = href.split("#", 1)
    path, frag = raw[0], (f"#{raw[1]}" if len(raw) > 1 else "")
    if path in PAGE_MAP:
        dest = PAGE_MAP[path]
        if dest.startswith("http"):
            return dest + frag
        return ("../" * depth) + dest + frag
    if path.endswith(".schema.json") or path.endswith(".example.json"):
        cleaned = path
        while cleaned.startswith("../"):
            cleaned = cleaned[3:]
        return ("../" * depth) + cleaned + frag
    if path.startswith("http") or path.startswith("mailto:"):
        return href
    return href


def inline(md: str, depth: int) -> str:
    def link(m: re.Match) -> str:
        return f'<a href="{html.escape(rewrite_href(m.group(2), depth), quote=True)}">{inline(m.group(1), depth)}</a>'

    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, md)

    def code(m: re.Match) -> str:
        return f"<code>{html.escape(m.group(1))}</code>"

    md = re.sub(r"`([^`]+)`", code, md)
    md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)
    return md


def consume_wrap(text: str, i: int, lines: list[str]) -> tuple[str, int]:
    parts = [text]
    while i < len(lines):
        nxt = lines[i]
        if not nxt.startswith("  "):
            break
        if re.match(r"^[-*] ", nxt.lstrip()) or re.match(r"^\d+\. ", nxt.lstrip()):
            break
        parts.append(nxt.strip())
        i += 1
    return " ".join(parts), i


def md_to_html(md: str, depth: int) -> tuple[str, list[tuple[str, str]]]:
    toc: list[tuple[str, str]] = []
    out: list[str] = []
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_lists()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>")
            continue
        if line.strip() == "---":
            close_lists()
            out.append("<hr>")
            i += 1
            continue
        m = re.match(r"^(#{1,3}) (.+)$", line)
        if m:
            close_lists()
            level = len(m.group(1))
            text = inline(m.group(2), depth)
            sid = slug(m.group(2))
            if level == 2:
                toc.append((sid, re.sub(r"<[^>]+>", "", text)))
            out.append(f'<h{level} id="{sid}">{text}</h{level}>')
            i += 1
            continue
        m = re.match(r"^[-*] (.+)$", line)
        if m:
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            text, i = consume_wrap(m.group(1), i + 1, lines)
            out.append(f"<li>{inline(text, depth)}</li>")
            continue
        m = re.match(r"^(\d+)\. (.+)$", line)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            text, i = consume_wrap(m.group(2), i + 1, lines)
            out.append(f"<li>{inline(text, depth)}</li>")
            continue
        if not line.strip():
            close_lists()
            i += 1
            continue
        close_lists()
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("```") and not lines[i].startswith("- ") and not lines[i].startswith("* ") and not re.match(r"^\d+\. ", lines[i]) and lines[i].strip() != "---":
            para.append(lines[i])
            i += 1
        out.append("<p>" + inline(" ".join(para), depth) + "</p>")
    close_lists()
    return "\n".join(out), toc


def chrome(title: str, body: str, depth: int, current: str) -> str:
    root = "../" * depth if depth else "./"
    nav = []
    for href, label in NAV:
        dest = href if href.startswith("http") else root + href
        here = ' aria-current="page"' if href.rstrip("/") == current.rstrip("/") else ""
        nav.append(f'<a href="{html.escape(dest, quote=True)}"{here}>{html.escape(label)}</a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — OpenBook</title>
<meta name="theme-color" content="#e6d7b8">
<link rel="canonical" href="https://openbook-data-standards.github.io/openbook/{html.escape(current, quote=True)}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="logo" href="{root}">
    <span class="name">OpenBook</span>
    <span class="rule"></span>
    <span class="sub">Open sportsbook standard</span>
  </a>
  <nav>
    {"".join(nav)}
  </nav>
</div></header>
<main id="main"><div class="wrap page">
{body}
</div></main>
<footer><div class="wrap">
  <a class="logo" href="{root}" style="margin-bottom:12px">
    <span class="name">OpenBook</span>
    <span class="rule"></span>
    <span class="sub">Open sportsbook standard</span>
  </a>
  <div>Canonical text lives in the repository; this page is the readable copy.</div>
</div></footer>
</body>
</html>
"""


def write_md_page(src: Path, dest: Path, depth: int, current: str, source_label: str) -> None:
    html_body, toc = md_to_html(src.read_text(), depth)
    toc_html = ""
    if toc:
        items = "".join(f'<a href="#{html.escape(sid, quote=True)}">{html.escape(label)}</a>' for sid, label in toc)
        toc_html = f'<nav class="toc"><strong>On this sheet</strong>{items}</nav>'
    home = "../" * depth if depth else "./"
    inner = f'<p class="crumb"><a href="{home}">Home</a> · {html.escape(source_label)}</p>{toc_html}<article class="doc">{html_body}</article><p class="source">Source: {html.escape(source_label)}</p>'
    title = re.sub(r"^# ", "", src.read_text().splitlines()[0])
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(chrome(title, inner, depth, current))


def schemas_page() -> str:
    blocks = []
    for path in sorted((ROOT / "schema").glob("*.schema.json")):
        data = json.loads(path.read_text())
        title = data.get("title") or path.name
        desc = data.get("description") or ""
        req = ", ".join(data.get("required") or []) or "—"
        rel = f"schema/{path.name}"
        sid = path.name.removesuffix(".schema.json")
        blocks.append(
            f'<section class="schema-block" id="{html.escape(sid)}">'
            f"<h2>{html.escape(title)}</h2>"
            f"<p>{html.escape(desc)}</p>"
            f'<p><a href="{html.escape(rel, quote=True)}">{html.escape(path.name)}</a>'
            f" · required: <code>{html.escape(req)}</code></p>"
            f"<pre>{html.escape(path.read_text().rstrip())}</pre></section>"
        )
    inner = (
        '<p class="crumb"><a href="./">Home</a> · JSON Schemas</p>'
        '<article class="doc"><h1>JSON Schemas</h1>'
        "<p>Draft 2020-12. These files are the machine-normative field definitions. "
        "Each <code>$id</code> is this same URL on GitHub Pages.</p>"
        + "".join(blocks)
        + "</article>"
    )
    return chrome("JSON Schemas", inner, 0, "schemas.html")


def examples_page() -> str:
    blocks = []
    for path in sorted((ROOT / "examples").glob("*.json")):
        rel = f"examples/{path.name}"
        blocks.append(
            f'<section class="schema-block" id="{html.escape(path.stem)}">'
            f"<h2>{html.escape(path.name)}</h2>"
            f'<p><a href="{html.escape(rel, quote=True)}">{html.escape(rel)}</a></p>'
            f"<pre>{html.escape(path.read_text().rstrip())}</pre></section>"
        )
    inner = (
        '<p class="crumb"><a href="./">Home</a> · Examples</p>'
        '<article class="doc"><h1>Examples</h1>'
        "<p>Worked documents that validate against the schemas.</p>"
        + "".join(blocks)
        + "</article>"
    )
    return chrome("Examples", inner, 0, "examples.html")


def vocab_index() -> str:
    cards = [
        ("market-types.html", "Market types", "What can be bet: moneyline, spread, total, player props, outrights."),
        ("sports.html", "Sports", "Canonical sport:* ids."),
        ("segments.html", "Segments", "Slices inside a match: halves, quarters, innings, sets."),
    ]
    lis = "".join(
        f'<p><a href="{html.escape(href, quote=True)}"><strong>{html.escape(t)}</strong></a> — {html.escape(d)}</p>'
        for href, t, d in cards
    )
    inner = (
        '<p class="crumb"><a href="../">Home</a> · Vocabularies</p>'
        '<article class="doc"><h1>Controlled vocabularies</h1>'
        "<p>Readable, versioned ids. Short on the wire, formal as <code>urn:openbook:</code> in the spec.</p>"
        f"{lis}</article>"
    )
    return chrome("Vocabularies", inner, 1, "vocabularies/")


def main() -> None:
    write_md_page(ROOT / "spec/openbook.md", ROOT / "spec.html", 0, "spec.html", "spec/openbook.md")
    write_md_page(ROOT / "docs/decisions.md", ROOT / "decisions.html", 0, "decisions.html", "docs/decisions.md")
    write_md_page(ROOT / "docs/building-blocks.md", ROOT / "building-blocks.html", 0, "building-blocks.html", "docs/building-blocks.md")
    write_md_page(ROOT / "docs/industry-patterns.md", ROOT / "industry-patterns.html", 0, "industry-patterns.html", "docs/industry-patterns.md")
    write_md_page(ROOT / "GOVERNANCE.md", ROOT / "governance.html", 0, "governance.html", "GOVERNANCE.md")
    write_md_page(ROOT / "VERSIONING.md", ROOT / "versioning.html", 0, "versioning.html", "VERSIONING.md")
    write_md_page(ROOT / "CONTRIBUTING.md", ROOT / "contributing.html", 0, "contributing.html", "CONTRIBUTING.md")
    write_md_page(ROOT / "CHANGELOG.md", ROOT / "changelog.html", 0, "changelog.html", "CHANGELOG.md")
    write_md_page(ROOT / "vocabularies/market_types.md", ROOT / "vocabularies/market-types.html", 1, "vocabularies/market-types.html", "vocabularies/market_types.md")
    write_md_page(ROOT / "vocabularies/sports.md", ROOT / "vocabularies/sports.html", 1, "vocabularies/sports.html", "vocabularies/sports.md")
    write_md_page(ROOT / "vocabularies/segments.md", ROOT / "vocabularies/segments.html", 1, "vocabularies/segments.html", "vocabularies/segments.md")
    (ROOT / "vocabularies/index.html").write_text(vocab_index())
    (ROOT / "schemas.html").write_text(schemas_page())
    (ROOT / "examples.html").write_text(examples_page())
    (ROOT / ".nojekyll").write_text("")
    print("wrote HTML pages")


if __name__ == "__main__":
    main()
