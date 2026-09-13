# tools/validate.py

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
(`.github/workflows/validate.yml`). To validate your own feed, point it at a
folder of your documents and messages — coming as `--examples <dir>`.

`tools/build_site.py` turns the markdown spec, vocabularies, and docs into
GitHub Pages HTML so the site can be read without opening GitHub.
