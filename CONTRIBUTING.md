# Contributing to OpenBook

This is an early working draft. The most valuable contributions right now are to
the **vocabularies** — especially [`vocabularies/market_types.md`](vocabularies/market_types.md),
the market taxonomy no one else has published.

## Proposing a change

1. Open an issue describing the change and the real-world feed(s) that motivate
   it. Vocabulary additions should cite at least one provider that carries the
   sport / market / segment. A new `propertyID` prefix goes in
   [`register/prefixes.md`](register/prefixes.md) and is never reused. A map
   from a public taxonomy goes in [`crosswalks/`](crosswalks/) and must land on
   an existing OpenBook id or the unknown catch-all with a reason.
2. For a schema change, update the JSON Schema in [`schema/`](schema/) **and** the
   prose in [`spec/openbook.md`](spec/openbook.md) in the same change; the schema
   is machine-normative and must not drift from the prose.
3. Add or update an example in [`examples/`](examples/) that validates against the
   changed schema, and list it in [`conformance/manifest.json`](conformance/manifest.json).
   If the change makes a previously legal document illegal, add an **invalid**
   case under `conformance/invalid/`.
4. Note the change in [`CHANGELOG.md`](CHANGELOG.md) under "Unreleased".
   Names you put in `spec/openbook.md` (and the scanned docs pages) MUST exist
   on a schema; `python3 tools/validate.py` checks that (Q50).

## Rules that don't bend

- **Ids, list-values and field names are stable** once shipped in a frozen
  version (Q35). Never re-point or reuse a published name; deprecate instead.
  Retired names go in [`vocabularies/deprecated.md`](vocabularies/deprecated.md).
- **No abbreviations** in canonical names (`reference_sport`, not `ref_sport`).
- **No provider ids as canonical ids.** A provider mapping goes on the `source`
  record.
- **Country is ISO 3166, time is RFC 3339 / ISO 8601, currency is ISO 4217
  (`baseCurrency` once per feed), odds and lines are decimal strings, money
  is `{amount}` in that currency.** Don't reinvent a primitive that already
  has a standard.
- **Segments are separate objects**, never encoded into a market id.

## Style

- Markdown prose over tables where a list will do.
- Every normative statement uses MUST / SHOULD / MAY per RFC 2119.
