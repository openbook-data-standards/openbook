# Still to do

Questions recorded through **Q92**. Catalog pass closed. Log only.
Q46–Q49 are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).
- **Q11/Q57–Q64 wire** — schema may still disagree with the log (team
  location/nickname/registered name, team-only abbreviation, publisher
  registered name, Place time zone and language, WGS 84, league sex
  category and age group, fixture surface, fixture participant seed).
- **Q80** — match lineup live object (not this log patch).
- Racing draw/stall, cricket toss, playoff series state — not on generic
  fixture (**Q86**); later stage / sport slice.

## Next question (not decided)

- (none parked from this walk)

## Done (Q32–Q92)

Q32–Q55 · **Q11/Q57–Q87** catalog names/place/omits; fixture extras stop; catalog pass closed.
**Q88** — JSON is the v1 encoding; other encodings are not forbidden.
**Q89** — no GBFS-style data wrapper.
**Q90** — JSON Patch (RFC 6902) never; Merge Patch (Q8) stands.
**Q91** — ISO 20022 is not the OpenBook encoding.
**Q92** — FIX session is not the OpenBook session.
