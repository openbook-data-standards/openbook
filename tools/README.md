# tools/

Non-normative runners. They are not the specification (Q40, Q57).

## validate.py

The OpenBook validator — **one runner** of the language-agnostic corpus
in [`../conformance/`](../conformance/), not a language oracle (Q40).
Run it to check that the schemas are sound, the examples conform, invalid
corpus cases are rejected, and stream topics follow the grammar.

```bash
pip install 'jsonschema>=4.18' referencing
python3 tools/validate.py
python3 tools/build_site.py
python3 tools/validate.py --topic openbook/v1/acme-feeds/odds/change/soccer/EVT-88213
```

Exit code 0 means conformant. CI runs it on every pull request
(`.github/workflows/validate.yml`). Step 7 is Q50: names in the spec (and a
few docs pages) MUST exist on a schema. Step 8 checks that
`tools/scaffold.py` still writes valid OpenBook documents.

To validate your own feed, point it at a folder of your documents and
messages — coming as `--examples <dir>`.

`tools/build_site.py` turns the markdown spec, vocabularies, and docs into
GitHub Pages HTML so the site can be read without opening GitHub.

## scaffold.py

Starter **publisher repository** tree (Q57): `openbook/publisher.json`,
`openbook/discovery.json`, optional MCP manifest
(`.well-known/mcp.json`) and plugin manifest. Not a pricing engine.

```bash
python3 tools/scaffold.py --id acme-feeds --name "Acme Feeds" --out ./acme-feeds
python3 tools/scaffold.py --id acme-feeds --out ./acme-feeds --git
python3 tools/scaffold.py --id acme-feeds --out ./acme-feeds --no-mcp --no-plugin
```
