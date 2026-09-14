# Still to do

Questions recorded through **Q123**. Catalog pass closed and on the wire.
**Q88** `throws` / `bats` are on `player`. **Q80** `lineup` is on the wire.
Protocol-fit pass closed (**Q89–Q95**). **Q96** vendor mapping / starter is
not this spec. Pinnacle Lines walk closed (**Q97–Q103**). Prop-row pass
closed (**Q104–Q117**) and on the wire.
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk)

**Name winning-margin plus-bands.** Exact margins already use `participant`
+ outcome `line`. Plus-band extra named; not wired.

### Wired

- **Q98** — optional `basis` on `market` and `odds/change`.
- **Q99** — spec: four places; no new fields.
- **Q101** — one fixture; `eventStatus` is live.
- **Q105–Q117** — typed prop outcome extras on `market`, `odds/change`,
  and `grade`.

### Log only

- **Q97** — specials are markets.
- **Q100** — no parlay/teaser flags on the fixture.
- **Q102** — keep `sport:*` ids; map vendor integers with `identifier` /
  `sameAs`.
- **Q103** — market `limit` is enough; Get Line is out of scope.
- **Q104** — typed prop outcomes. Field names **Q105**.
- **Q111** — listing `order` / `seed` stay 1; `sequence` may be 0
  (already true on the schema).
- **Q118** — plus-band walk.
- **Q119** — plus-band extra is atLeast (JSON number). Not wired.
- **Q120** — plus-band row always has who and atLeast.
- **Q121** — plus-band has atLeast, not exact line.
- **Q122** — atLeast on market, odds/change, and grade. Not wired.
- **Q123** — pass not closed.
### Parked

- **Q86** — racing stall, cricket toss, playoff series until a payload.
- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- After atLeast, is leftover other still allowed on winning margin?

## Done (Q32–Q123)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup` · **Q56** MCP/plugin discovery `kind`.
**Q89–Q95** protocol-fit: JSON v1 encoding; no GBFS data wrapper; no JSON
Patch; not ISO 20022; not FIX session; no spec-owned multi-publisher index;
protocol-fit pass closed.
**Q96** — vendor mapping / starter / translate packages are not this spec.
**Q97–Q103** — Pinnacle Lines: specials are markets; optional `basis`;
statuses/settled; omit parlay flags; one fixture; `sport:*` ids; Get Line
out of scope.
**Q104** — typed prop outcomes.
**Q105–Q117** — extras on market / odds/change / grade: homeTotal /
awayTotal; halfTime / fullTime; player id; extra side tokens; row rules;
pass closed.
**Q118** — plus-band walk.
**Q119** — plus-band extra is atLeast.
**Q120** — plus-band row always has who and atLeast.
**Q121** — plus-band has atLeast, not exact line.
**Q122** — atLeast on market, odds/change, and grade (not built).
**Q123** — plus-band pass not closed.
