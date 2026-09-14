# Still to do

Questions recorded through **Q103**. Catalog pass closed and on the wire.
**Q88** `throws` / `bats` are on `player`. **Q80** `lineup` is on the wire.
Protocol-fit pass closed (**Q89–Q95**). **Q96** vendor mapping is not
this spec; `openbook-translate` tree is in packages (Apache-2.0).
`openbook-starter` is not built. Pinnacle Lines walk closed (**Q97–Q103**).
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

### Parked

- **Q86** — racing stall, cricket toss, playoff series until a payload.
- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).
- **Q96** — `openbook-starter` (translate ABC is built).

## Next question (not decided)

- This Lines walk is closed. Parked: **Q86**. Later: **Q55**.

## Done (Q32–Q103)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup` · **Q56** MCP/plugin discovery `kind`.
**Q89–Q95** protocol-fit: JSON v1 encoding; no GBFS data wrapper; no JSON
Patch; not ISO 20022; not FIX session; no spec-owned multi-publisher index;
protocol-fit pass closed.
**Q96** — vendor mapping is not this spec; `openbook-translate` is in
packages; `openbook-starter` is not built.
**Q97–Q103** — Pinnacle Lines: specials are markets; optional `basis`;
statuses/settled; omit parlay flags; one fixture; `sport:*` ids; Get Line
out of scope.
