#!/usr/bin/env python3
"""Render OpenBook markdown into GitHub Pages HTML. Canonical source stays the .md files."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV = [
    ("guide.html", "Guide"),
    ("examples.html", "Examples"),
    ("spec.html", "Spec"),
    ("taxonomy.html", "Taxonomy"),
    ("vocabularies/", "Vocabularies"),
    ("https://github.com/openbook-data-standards/openbook", "GitHub"),
]

PAGE_MAP = {
    "spec/openbook.md": "spec.html",
    "../spec/openbook.md": "spec.html",
    "guide.md": "guide.html",
    "docs/guide.md": "guide.html",
    "../docs/guide.md": "guide.html",
    "examples.md": "examples.html",
    "docs/examples.md": "examples.html",
    "../docs/examples.md": "examples.html",
    "taxonomy.md": "taxonomy.html",
    "docs/taxonomy.md": "taxonomy.html",
    "../docs/taxonomy.md": "taxonomy.html",
    "asyncapi.yaml": "spec/asyncapi.yaml",
    "../spec/asyncapi.yaml": "spec/asyncapi.yaml",
    "decisions.md": "decisions.html",
    "docs/decisions.md": "decisions.html",
    "../docs/decisions.md": "decisions.html",
    "building-blocks.md": "building-blocks.html",
    "docs/building-blocks.md": "building-blocks.html",
    "../docs/building-blocks.md": "building-blocks.html",
    "docs/industry-patterns.md": "industry-patterns.html",
    "../docs/industry-patterns.md": "industry-patterns.html",
    "docs/protocol-comparison.md": "protocol-comparison.html",
    "../docs/protocol-comparison.md": "protocol-comparison.html",
    "protocol-comparison.md": "protocol-comparison.html",
    "docs/roadmap.md": "roadmap.html",
    "../docs/roadmap.md": "roadmap.html",
    "roadmap.md": "roadmap.html",
    "industry-patterns.md": "industry-patterns.html",
    "GOVERNANCE.md": "governance.html",
    "../GOVERNANCE.md": "governance.html",
    "SECURITY.md": "security.html",
    "../SECURITY.md": "security.html",
    "VERSIONING.md": "versioning.html",
    "../VERSIONING.md": "versioning.html",
    "CONTRIBUTING.md": "contributing.html",
    "../CONTRIBUTING.md": "contributing.html",
    "CHANGELOG.md": "changelog.html",
    "../CHANGELOG.md": "changelog.html",
    "vocabularies/market_types.md": "vocabularies/#market-types",
    "../vocabularies/market_types.md": "vocabularies/#market-types",
    "vocabularies/sports.md": "vocabularies/#sports",
    "../vocabularies/sports.md": "vocabularies/#sports",
    "vocabularies/segments.md": "vocabularies/#segments",
    "../vocabularies/segments.md": "vocabularies/#segments",
    "vocabularies/positions.md": "vocabularies/#positions",
    "../vocabularies/positions.md": "vocabularies/#positions",
    "../vocabularies/": "vocabularies/",
    "vocabularies/": "vocabularies/",
    "../schema/": "schemas.html",
    "schema/": "schemas.html",
    "../examples/": "examples.html",
    "examples/": "examples.html",
    "../conformance/": "conformance/",
    "conformance/": "conformance/",
    "../conformance/README.md": "conformance/",
    "conformance/README.md": "conformance/",
}

# Bare names (guide.md) and ../docs/ paths must both rewrite. Dropping
# docs/taxonomy.md here leaves spec.html pointing at a dead .md URL.
for _src, _dst in (
    ("docs/taxonomy.md", "taxonomy.html"),
    ("../docs/taxonomy.md", "taxonomy.html"),
    ("taxonomy.md", "taxonomy.html"),
    ("guide.md", "guide.html"),
    ("examples.md", "examples.html"),
    ("decisions.md", "decisions.html"),
):
    if PAGE_MAP.get(_src) != _dst:
        raise RuntimeError(f"PAGE_MAP missing {_src!r} -> {_dst!r}")



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
    if "/maps/" in path or path.startswith("maps/"):
        cleaned = path
        while cleaned.startswith("../"):
            cleaned = cleaned[3:]
        return ("../" * depth) + cleaned + frag
    if "/register/" in path or path.startswith("register/"):
        cleaned = path
        while cleaned.startswith("../"):
            cleaned = cleaned[3:]
        return ("../" * depth) + cleaned + frag
    if path.startswith("http") or path.startswith("mailto:"):
        return href
    return href


def inline(md: str, depth: int) -> str:
    # Links and code carry their own escaping, so stash the finished HTML behind
    # NUL sentinels, escape the remaining literal prose (markdown syntax chars
    # like []()*` are untouched by html.escape), then restore. Without this,
    # a bare <, > or & in prose would emit broken HTML.
    stash: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    def link(m: re.Match) -> str:
        href = html.escape(rewrite_href(m.group(2), depth), quote=True)
        return keep(f'<a href="{href}">{inline(m.group(1), depth)}</a>')

    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, md)

    def code(m: re.Match) -> str:
        return keep(f"<code>{html.escape(m.group(1))}</code>")

    md = re.sub(r"`([^`]+)`", code, md)
    md = html.escape(md, quote=False)
    md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", md)
    md = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], md)
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
        if line.strip().startswith("<!-- include:") and line.strip().endswith("-->"):
            close_lists()
            rel = line.strip()[len("<!-- include:") :].removesuffix("-->").strip()
            src = ROOT / rel
            if not src.is_file() or not src.resolve().is_relative_to(ROOT):
                raise FileNotFoundError(f"include not found: {rel}")
            out.append("<pre>" + html.escape(src.read_text().rstrip()) + "</pre>")
            i += 1
            continue
        if line.startswith("```"):
            close_lists()
            lang = line[3:].strip()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            body = "\n".join(buf)
            if lang == "mermaid":
                out.append(f'<pre class="mermaid">{html.escape(body)}</pre>')
            else:
                out.append("<pre>" + html.escape(body) + "</pre>")
            continue
        if line.strip().startswith("|") and line.strip().count("|") >= 2:
            close_lists()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().count("|") >= 2:
                rows.append(lines[i])
                i += 1
            parsed: list[list[str]] = []
            for raw in rows:
                cells = [c.strip() for c in raw.strip().strip("|").split("|")]
                if parsed and all(re.match(r"^:?-{3,}:?$", c) for c in cells):
                    continue
                parsed.append(cells)
            if parsed:
                head, body_rows = parsed[0], parsed[1:]
                thead = "<thead><tr>" + "".join(f"<th>{inline(c, depth)}</th>" for c in head) + "</tr></thead>"
                tbody = "<tbody>" + "".join(
                    "<tr>" + "".join(f"<td>{inline(c, depth)}</td>" for c in row) + "</tr>"
                    for row in body_rows
                ) + "</tbody>"
                out.append(f'<div class="table-wrap"><table>{thead}{tbody}</table></div>')
            continue
        if line.startswith(">"):
            close_lists()
            quotes = []
            while i < len(lines) and lines[i].startswith(">"):
                quotes.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + inline(" ".join(quotes), depth) + "</blockquote>")
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
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("```") and not lines[i].startswith("- ") and not lines[i].startswith("* ") and not lines[i].startswith(">") and not lines[i].strip().startswith("|") and not re.match(r"^\d+\. ", lines[i]) and lines[i].strip() != "---":
            para.append(lines[i])
            i += 1
        out.append("<p>" + inline(" ".join(para), depth) + "</p>")
    close_lists()
    return "\n".join(out), toc


LOGO = '''<svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true">
      <rect class="ink" x="2" y="8" width="4" height="4"/>
      <rect fill="#276EF1" x="2" y="14" width="4" height="4"/>
      <rect class="ink" x="2" y="20" width="4" height="4"/>
      <rect class="ink" x="8" y="8" width="12" height="4"/>
      <rect fill="#276EF1" x="8" y="14" width="22" height="4"/>
      <rect class="ink" x="8" y="20" width="8" height="4"/>
    </svg>
    OpenBook'''

def toc_entry(text: str) -> tuple[str | None, str]:
    """Short TOC label: keep '5. Change', drop the slogan after ':' or '('."""
    plain = re.sub(r"<[^>]+>", "", text).strip()
    numbered = re.match(r"^(\d+[a-z]?)\.\s+(.+)$", plain, re.I)
    if numbered:
        title = re.split(r"\s*[:(,]", numbered.group(2), maxsplit=1)[0].strip()
        return numbered.group(1), title or numbered.group(2)
    return None, re.split(r"\s*[:(,]", plain, maxsplit=1)[0].strip() or plain


def toc_nav(toc: list[tuple[str, str]] | None) -> str:
    if not toc:
        return ""
    links = []
    for sid, label in toc:
        num, title = toc_entry(label)
        n = html.escape(num) if num else ""
        inner = f'<span class="n">{n}</span>{html.escape(title)}'
        links.append(f'<a href="#{html.escape(sid, quote=True)}">{inner}</a>')
    return f'<nav class="page-toc"><strong>On this page</strong>{"".join(links)}</nav>'


def page_frame(crumb: str, toc: list[tuple[str, str]] | None, article: str, source: str | None = None) -> str:
    src = f'<p class="source">{source}</p>' if source else ""
    return (
        f'<div class="page-layout">'
        f"{toc_nav(toc)}"
        f'<div class="page-main">{crumb}<article class="doc">{article}</article></div>'
        f"</div>{src}"
    )


def nav_current(current: str, href: str) -> str:
    cur = current.rstrip("/")
    dest = href.rstrip("/")
    return ' aria-current="page"' if cur == dest else ""


def chrome(title: str, body: str, depth: int, current: str, toc: list[tuple[str, str]] | None = None) -> str:
    root = "../" * depth if depth else "./"
    mermaid = ""
    if 'class="mermaid"' in body:
        mermaid = """
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({
    startOnLoad: true,
    theme: "dark",
    securityLevel: "strict",
    themeVariables: {
      background: "#0f141e",
      primaryColor: "#15233f",
      primaryTextColor: "#f4f7fb",
      primaryBorderColor: "#4c8dff",
      lineColor: "#8b93b0",
      secondaryColor: "#1c2438",
      tertiaryColor: "#171d2b",
      mainBkg: "#171d2b",
      nodeBorder: "#4c8dff",
      clusterBkg: "#171d2b",
      titleColor: "#f4f7fb",
      edgeLabelBackground: "#171d2b"
    }
  });
</script>"""
    parts = []
    for href, label in NAV:
        dest = href if href.startswith("http") else f"{root}{href}"
        cur = nav_current(current, href) if not href.startswith("http") else ""
        parts.append(
            f'<a href="{html.escape(dest, quote=True)}"{cur}>{html.escape(label)}</a>'
        )
    links = "\n    ".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — OpenBook</title>
<meta name="theme-color" content="#0B1220">
<link rel="canonical" href="https://openbook-data-standards.github.io/openbook/{html.escape(current, quote=True)}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="logo" href="{root}">{LOGO}</a>
  <nav>
    {links}
  </nav>
</div></header>
<main id="main"><div class="wrap page">
{body}
</div></main>
<footer><div class="wrap">
  <a class="logo" href="{root}" style="margin-bottom:12px">
    {LOGO}
  </a>
  <div>Canonical text lives in the repository; this page is the readable copy.</div>
</div></footer>
{mermaid}
</body>
</html>
"""


def write_md_page(src: Path, dest: Path, depth: int, current: str, source_label: str) -> None:
    text = src.read_text()
    html_body, toc = md_to_html(text, depth)
    home = "../" * depth if depth else "./"
    inner = page_frame(
        f'<p class="crumb"><a href="{home}">Home</a> · {html.escape(source_label)}</p>',
        toc,
        html_body,
        f"Source: {html.escape(source_label)}",
    )
    title = re.sub(r"^# ", "", text.splitlines()[0])
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(chrome(title, inner, depth, current, toc))


def schemas_page() -> str:
    blocks = []
    toc: list[tuple[str, str]] = []
    for path in sorted((ROOT / "schema").glob("*.schema.json")):
        data = json.loads(path.read_text())
        title = data.get("title") or path.name
        desc = data.get("description") or ""
        req = ", ".join(data.get("required") or []) or "—"
        rel = f"schema/{path.name}"
        sid = path.name.removesuffix(".schema.json")
        toc.append((sid, sid))
        blocks.append(
            f'<section class="schema-block" id="{html.escape(sid)}">'
            f"<h2>{html.escape(title)}</h2>"
            f"<p>{html.escape(desc)}</p>"
            f'<p><a href="{html.escape(rel, quote=True)}">{html.escape(path.name)}</a>'
            f" · required: <code>{html.escape(req)}</code></p>"
            f"<pre>{html.escape(path.read_text().rstrip())}</pre></section>"
        )
    toc.append(("examples", "examples"))
    inner = page_frame(
        '<p class="crumb"><a href="./">Home</a> · JSON Schemas</p>',
        toc,
        "<h1>JSON Schemas</h1>"
        "<p>Draft 2020-12. These files are the machine-normative field definitions. "
        "Each <code>$id</code> is this same URL on GitHub Pages.</p>"
        + "".join(blocks)
        + '<h1 id="examples">Examples (raw files)</h1>'
        '<p>The sequence-order walkthrough is the <a href="examples.html">examples page</a>. '
        "These are the same files, listed for implementers.</p>"
        + "".join(example_blocks()),
    )
    return chrome("JSON Schemas", inner, 0, "schemas.html", toc)


def example_blocks() -> list[str]:
    blocks = []
    for path in sorted((ROOT / "examples").glob("*.json")):
        rel = f"examples/{path.name}"
        blocks.append(
            f'<section class="schema-block" id="{html.escape(path.stem)}">'
            f"<h2>{html.escape(path.name)}</h2>"
            f'<p><a href="{html.escape(rel, quote=True)}">{html.escape(rel)}</a></p>'
            f"<pre>{html.escape(path.read_text().rstrip())}</pre></section>"
        )
    return blocks


def write_redirect(path: Path, url: str, canonical: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f'<meta http-equiv="refresh" content="0;url={html.escape(url, quote=True)}">'
        f'<link rel="canonical" href="https://openbook-data-standards.github.io/openbook/{html.escape(canonical, quote=True)}">'
        f"<title>Moved</title></head><body>"
        f'<p>Moved to <a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>.</p>'
        "</body></html>\n"
    )


def vocab_index() -> str:
    sections = [
        (ROOT / "vocabularies/market_types.md", "market-types", "Market types", "vocabularies/market_types.md"),
        (ROOT / "vocabularies/sports.md", "sports", "Sports", "vocabularies/sports.md"),
        (ROOT / "vocabularies/segments.md", "segments", "Segments", "vocabularies/segments.md"),
        (ROOT / "vocabularies/positions.md", "positions", "Positions", "vocabularies/positions.md"),
    ]
    toc_items = [("how-to-read", "How to read")] + [(sid, label) for _, sid, label, _ in sections]
    parts = []
    for src, sid, label, source_label in sections:
        body, _ = md_to_html(src.read_text(), 1)
        body = body.replace("<h1 ", "<h2 ", 1).replace("</h1>", "</h2>", 1)
        parts.append(f'<section id="{html.escape(sid)}">{body}<p class="source">Source: {html.escape(source_label)}</p></section>')
    inner = page_frame(
        '<p class="crumb"><a href="../">Home</a> · Vocabularies</p>',
        toc_items,
        "<h1>Controlled vocabularies</h1>"
        '<section id="how-to-read"><p>This page is the <strong>id list</strong> '
        "computers use. For what the words mean in plain language, start with the "
        '<a href="../taxonomy.html">taxonomy</a>. The technical contract is the '
        '<a href="../spec.html">specification</a>.</p>'
        "<p>Readable, versioned ids. Short on the wire, formal as <code>urn:openbook:</code> in the spec. Market types, sports, segments and positions follow.</p></section>"
        + "".join(parts),
    )
    return chrome("Vocabularies", inner, 1, "vocabularies/", toc_items)


def main() -> None:
    write_md_page(ROOT / "docs/guide.md", ROOT / "guide.html", 0, "guide.html", "docs/guide.md")
    write_md_page(ROOT / "docs/examples.md", ROOT / "examples.html", 0, "examples.html", "docs/examples.md")
    write_md_page(ROOT / "docs/taxonomy.md", ROOT / "taxonomy.html", 0, "taxonomy.html", "docs/taxonomy.md")
    write_md_page(ROOT / "spec/openbook.md", ROOT / "spec.html", 0, "spec.html", "spec/openbook.md")
    write_md_page(ROOT / "docs/decisions.md", ROOT / "decisions.html", 0, "decisions.html", "docs/decisions.md")
    write_md_page(ROOT / "docs/building-blocks.md", ROOT / "building-blocks.html", 0, "building-blocks.html", "docs/building-blocks.md")
    write_md_page(ROOT / "docs/industry-patterns.md", ROOT / "industry-patterns.html", 0, "industry-patterns.html", "docs/industry-patterns.md")
    write_md_page(ROOT / "docs/protocol-comparison.md", ROOT / "protocol-comparison.html", 0, "protocol-comparison.html", "docs/protocol-comparison.md")
    write_md_page(ROOT / "docs/roadmap.md", ROOT / "roadmap.html", 0, "roadmap.html", "docs/roadmap.md")
    write_md_page(ROOT / "GOVERNANCE.md", ROOT / "governance.html", 0, "governance.html", "GOVERNANCE.md")
    write_md_page(ROOT / "SECURITY.md", ROOT / "security.html", 0, "security.html", "SECURITY.md")
    write_md_page(ROOT / "VERSIONING.md", ROOT / "versioning.html", 0, "versioning.html", "VERSIONING.md")
    write_md_page(ROOT / "CONTRIBUTING.md", ROOT / "contributing.html", 0, "contributing.html", "CONTRIBUTING.md")
    write_md_page(ROOT / "CHANGELOG.md", ROOT / "changelog.html", 0, "changelog.html", "CHANGELOG.md")
    (ROOT / "vocabularies/index.html").write_text(vocab_index())
    write_redirect(ROOT / "vocabularies/market-types.html", "./#market-types", "vocabularies/#market-types")
    write_redirect(ROOT / "vocabularies/sports.html", "./#sports", "vocabularies/#sports")
    write_redirect(ROOT / "vocabularies/segments.html", "./#segments", "vocabularies/#segments")
    write_redirect(ROOT / "vocabularies/positions.html", "./#positions", "vocabularies/#positions")
    (ROOT / "schemas.html").write_text(schemas_page())
    write_md_page(ROOT / "conformance/README.md", ROOT / "conformance/index.html", 1, "conformance/", "conformance/README.md")
    (ROOT / ".nojekyll").write_text("")
    print("wrote HTML pages")


if __name__ == "__main__":
    main()
