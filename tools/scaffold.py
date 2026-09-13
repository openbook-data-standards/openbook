#!/usr/bin/env python3
"""Non-normative starter for an OpenBook publisher repository (Q57).

Writes identity + discovery, and optionally MCP / plugin manifests.
Does not implement a feed engine (open spec, closed code).

  python3 tools/scaffold.py --id acme-feeds --name "Acme Feeds" --out ./acme-feeds
  python3 tools/scaffold.py --id acme-feeds --out ./acme-feeds --no-mcp --no-plugin
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OPENBOOK_VERSION = "0.3.0-draft"
PUB_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MCP_SERVER_SCHEMA = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def now_rfc3339() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def stream_url(base: str) -> str:
    if base.startswith("https://"):
        return "wss://" + base[len("https://") :] + "/stream"
    if base.startswith("http://"):
        return "ws://" + base[len("http://") :] + "/stream"
    return base.rstrip("/") + "/stream"


def publisher_doc(args, stamp: str) -> dict:
    return {
        "openbookVersion": OPENBOOK_VERSION,
        "id": args.id,
        "sequence": 1,
        "dateModified": stamp,
        "name": args.name,
        "baseCurrency": args.currency,
        "heartbeatMs": 5000,
        "ttl": 60,
        "url": args.base_url,
        "sources": [
            {
                "id": args.source_id,
                "name": args.source_name,
                "sourceType": "sportsbook",
            }
        ],
    }


def discovery_doc(args, stamp: str) -> dict:
    base = args.base_url.rstrip("/")
    feeds = [
        {"name": "snapshot", "kind": "snapshot", "url": f"{base}/snapshot"},
        {"name": "stream", "kind": "stream", "url": stream_url(base)},
        {"name": "docs", "kind": "docs", "url": f"{base}/docs"},
    ]
    if args.mcp:
        feeds.append(
            {
                "name": f"{args.name} MCP",
                "kind": "mcp",
                "id": "openbook-mcp",
                "schemaUrl": MCP_SERVER_SCHEMA,
                "url": f"{base}/.well-known/mcp.json",
            }
        )
    if args.plugin:
        feeds.append(
            {
                "name": f"{args.name} plugin",
                "kind": "plugin",
                "id": "openbook",
                "schemaUrl": PLUGIN_SCHEMA,
                "url": f"{base}/plugins/openbook/plugin.json",
            }
        )
    return {"lastUpdated": stamp, "ttl": 60, "feeds": feeds}


def mcp_doc(args) -> dict:
    base = args.base_url.rstrip("/")
    return {
        "$schema": MCP_SERVER_SCHEMA,
        "name": args.mcp_name,
        "description": (
            "Read OpenBook sportsbook documents for this publisher. "
            "Payloads are OpenBook documents, not a parallel betting schema."
        ),
        "version": OPENBOOK_VERSION,
        "remotes": [{"type": "streamable-http", "url": f"{base}/mcp"}],
    }


def plugin_doc(args) -> dict:
    return {
        "$schema": PLUGIN_SCHEMA,
        "name": args.id,
        "description": (
            f"OpenBook plugin for {args.name}. "
            "Advertised on discovery; payloads stay OpenBook documents."
        ),
    }


def readme(args) -> str:
    mcp_bit = ""
    if args.mcp:
        mcp_bit += (
            f"- MCP manifest: `.well-known/mcp.json` (MCP Registry `server.json` shape).\n"
            f"  Point clients at `{args.base_url.rstrip('/')}/.well-known/mcp.json`.\n"
        )
    if args.plugin:
        mcp_bit += (
            "- Plugin manifest: `plugins/openbook/plugin.json` (Agent Plugins shape).\n"
        )
    return f"""# {args.name}

Starter **OpenBook publisher** tree. OpenBook is the data contract; this
repository is yours to implement (open spec, closed code).

## What you got

- `openbook/publisher.json` — who transmits, `baseCurrency`, sources.
- `openbook/discovery.json` — one catalog: snapshot, stream, docs{', MCP, plugin' if args.mcp or args.plugin else ''}.
{mcp_bit}
Replace `example.invalid` (or `--base-url`) with your host. Discovery `url`
values must be the documents you actually serve.

## Rules that matter

- Odds, scores and grades stay OpenBook documents (`object` / `action`).
- An MCP server or plugin MUST NOT invent a parallel market schema.
- Vendor extras are `x_`-prefixed fields.
- `python3 tools/validate.py` in the [OpenBook spec repo](https://github.com/openbook-data-standards/openbook)
  is one runner; copy `openbook/*.json` into a folder of examples once
  `--examples` lands, or validate them against the schemas there.

## Next

```bash
git add .
git commit -m "Initial OpenBook publisher tree."
```

Fill snapshot/stream from your engine. The scaffold does not price or emit odds.
"""


def gitignore() -> str:
    return "\n".join(
        [
            ".DS_Store",
            "__pycache__/",
            ".venv/",
            "venv/",
            "*.pyc",
            "",
        ]
    )


def write_tree(args) -> None:
    out = Path(args.out).resolve()
    if out.exists():
        if any(out.iterdir()) and not args.force:
            sys.exit(f"refusing to write into non-empty directory: {out} (use --force)")
    else:
        out.mkdir(parents=True)
    stamp = now_rfc3339()
    dump(out / "openbook" / "publisher.json", publisher_doc(args, stamp))
    dump(out / "openbook" / "discovery.json", discovery_doc(args, stamp))
    if args.mcp:
        dump(out / ".well-known" / "mcp.json", mcp_doc(args))
    if args.plugin:
        dump(out / "plugins" / "openbook" / "plugin.json", plugin_doc(args))
    (out / "README.md").write_text(readme(args), encoding="utf-8")
    (out / ".gitignore").write_text(gitignore(), encoding="utf-8")
    if args.git:
        git_dir = out / ".git"
        if not git_dir.exists():
            subprocess.run(["git", "init"], cwd=out, check=True, capture_output=True)
    print(f"wrote OpenBook publisher starter at {out}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Write a starter OpenBook publisher repository (non-normative, Q57)."
    )
    p.add_argument("--id", required=True, help="publisher id (lowercase, dash-separated)")
    p.add_argument("--out", required=True, help="directory to create or fill")
    p.add_argument("--name", default="", help="display name (default: id)")
    p.add_argument("--currency", default="GBP", help="ISO 4217 baseCurrency (default GBP)")
    p.add_argument("--base-url", default="", help="public origin (default https://example.invalid/<id>)")
    p.add_argument("--source-id", default="", help="first source id (default: <id>-book)")
    p.add_argument("--source-name", default="", help="first source name (default: name)")
    p.add_argument("--mcp-name", default="", help="MCP reverse-DNS name (default com.example/<id>)")
    p.add_argument("--mcp", dest="mcp", action="store_true", default=True)
    p.add_argument("--no-mcp", dest="mcp", action="store_false")
    p.add_argument("--plugin", dest="plugin", action="store_true", default=True)
    p.add_argument("--no-plugin", dest="plugin", action="store_false")
    p.add_argument("--git", action="store_true", help="git init in --out")
    p.add_argument("--force", action="store_true", help="allow writing into a non-empty --out")
    args = p.parse_args(argv)
    if not PUB_ID.match(args.id):
        sys.exit("--id must match ^[a-z0-9][a-z0-9-]*$")
    if not re.match(r"^[A-Z]{3}$", args.currency):
        sys.exit("--currency must be ISO 4217 alpha (GBP, EUR, USD)")
    args.name = args.name or args.id
    args.base_url = (args.base_url or f"https://example.invalid/{args.id}").rstrip("/")
    args.source_id = args.source_id or f"{args.id}-book"
    args.source_name = args.source_name or args.name
    args.mcp_name = args.mcp_name or f"com.example/{args.id}"
    write_tree(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
