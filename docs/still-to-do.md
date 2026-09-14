# Still to do

Questions recorded through **Q116**. Catalog pass closed and on the wire.
**Q88** `throws` / `bats` are on `player`. **Q80** `lineup` is on the wire.
Protocol-fit pass closed (**Q89–Q95**). **Q96** vendor mapping / starter is
not this spec. Pinnacle Lines walk closed (**Q97–Q103**).
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk — closed)

**Cover the Pinnacle Lines API in OpenBook.** If Pinnacle publishes it on
that feed, OpenBook can carry it. Industry shape, not a Pinnacle clone.
Not the Pinnacle Bets API.

### Wired

- **Q98** — optional `basis` on `market` and `odds/change`.
- **Q99** — spec: four places; no new fields.
- **Q101** — one fixture; `eventStatus` is live.

### Log only

- **Q97** — specials are markets.
- **Q100** — no parlay/teaser flags on the fixture.
- **Q102** — keep `sport:*` ids; map vendor integers with `identifier` /
  `sameAs`.
- **Q103** — market `limit` is enough; Get Line is out of scope.
- **Q104** — typed prop outcomes. Field names **Q105**.
- **Q105** — homeTotal / awayTotal; halfTime / fullTime; player on the
  outcome; extra side tokens.
- **Q106** — those extras on market, odds/change, and grade. Not wired.
- **Q107** — CS / HT/FT / winning margin are one market, many rows.
- **Q108** — player on the row is the OpenBook id only.
- **Q109** — HT/FT half and full are only home, away, or draw.
- **Q110** — HT/FT row always has both half and full.
- **Q111** — listing `order` / `seed` stay 1; `sequence` may be 0.
- **Q112** — listed correct score always has both totals.
- **Q113** — listed winning margin always has who and the number.
- **Q114** — a row does not mix boards.
- **Q115** — player over/under always has the player id.
- **Q116** — none is a listed selection; leftover stays other.

### Parked

- **Q86** — racing stall, cricket toss, playoff series until a payload.
- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- Close this pass of prop row rules?

## Done (Q32–Q116)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup` · **Q56** MCP/plugin discovery `kind`.
**Q89–Q95** protocol-fit: JSON v1 encoding; no GBFS data wrapper; no JSON
Patch; not ISO 20022; not FIX session; no spec-owned multi-publisher index;
protocol-fit pass closed.
**Q96** — vendor mapping / starter / translate packages are not this spec.
**Q97–Q103** — Pinnacle Lines: specials are markets; optional `basis`;
statuses/settled; omit parlay flags; one fixture; `sport:*` ids; Get Line
out of scope.
**Q104** — typed prop outcomes.
**Q105** — names: homeTotal / awayTotal; halfTime / fullTime; player on
the outcome; extra side tokens.
**Q106** — wire those extras onto market / odds/change / grade (not
built).
**Q107** — CS / HT/FT / winning margin: one market, many rows.
**Q108** — player on the row is the OpenBook id only.
**Q109** — HT/FT half and full are only home, away, or draw.
**Q110** — HT/FT row always has both half and full.
**Q111** — listing order / seed stay 1; sequence may be 0.
**Q112** — listed correct score always has both totals.
**Q113** — listed winning margin always has who and the number.
**Q114** — a row does not mix boards.
**Q115** — player over/under always has the player id.
**Q116** — none is a listed selection; leftover stays other.
