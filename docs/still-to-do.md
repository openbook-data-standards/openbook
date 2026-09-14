# Still to do

Questions recorded through **Q143**. Catalog pass closed and on the wire.
**Q88** `throws` / `bats` are on `player`. **Q80** `lineup` is on the wire.
Protocol-fit pass closed (**Q89–Q95**). **Q96** vendor mapping / starter is
not this spec. Pinnacle Lines walk closed (**Q97–Q103**). Prop-row pass
closed (**Q104–Q117**) and on the wire. Plus-band pass closed
(**Q118–Q125**) and on the wire. Yes/no player pass closed
(**Q126–Q132**) and on the wire. Spec walk stopped, then unparked
(**Q133**, **Q134**).
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk)

**Q86 leftovers.** Racing stall and cricket toss are new catalog objects
(sport slices; names wait). Playoff series: round on `stage`; the lead is
a new live object (name waits). Not more keys on every fixture. No new
field in this pick.

## Goal (previous — yes/no player, closed)

**Player on yes/no rows** (anytime scorer / to score). Same `player` id as
over/under. No new market type. No new field. On the wire.

## Goal (previous — plus-bands, closed)

**Name winning-margin plus-bands.** Exact margins already use `participant`
+ outcome `line`. Plus-band extra is `atLeast`. On the wire.

### Wired

- **Q98** — optional `basis` on `market` and `odds/change`.
- **Q99** — spec: four places; no new fields.
- **Q101** — one fixture; `eventStatus` is live.
- **Q105–Q117** — typed prop outcome extras on `market`, `odds/change`,
  and `grade`.
- **Q119–Q125** — `atLeast` on `market`, `odds/change`, and `grade`.
  Plus-band row is `participant` + `atLeast`; exact keeps `line`; leftover
  `other` still allowed; pass closed.
- **Q126–Q132** — player on yes/no rows: same player id; always present;
  leftover `other` not used; `no` optional; one market, many rows; no
  market `line`; pass closed.

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
- **Q133** — stop this spec walk (superseded as the next area by Q134).
- **Q134** — unpark Q86 leftovers.
- **Q135** — all three leftovers in this pass.
- **Q136** — still not keys on every fixture (keep Q86).
- **Q137** — each leftover its own home.
- **Q138** — stall and toss are sport slices; series is not.
- **Q139** — series round on `stage`; the lead is live.
- **Q140** — live series lead is a new live object (not `score`).
- **Q141** — stall is not on the generic fixture or `participant` row.
- **Q142** — toss is not on the generic fixture.
- **Q143** — stall and toss are new catalog objects (not `sport`, not live).

### Parked

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- Stall and toss: two catalog objects, or one?

## Done (Q32–Q143)

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
**Q119–Q125** — plus-bands on the wire: `atLeast` on `market`,
`odds/change`, and `grade`; who + `atLeast`; not exact `line`; leftover
`other` still allowed; pass closed.
**Q126–Q132** — player on yes/no rows; pass closed; on the wire.
**Q133** — stop this spec walk.
**Q134** — unpark Q86 leftovers.
**Q135** — all three leftovers in this pass.
**Q136** — still not keys on every fixture.
**Q137** — each leftover its own home.
**Q138** — stall and toss are sport slices; series is not.
**Q139** — series round on `stage`; the lead is live.
**Q140** — live series lead is a new live object (not `score`).
**Q141** — stall not on generic fixture or `participant`.
**Q142** — toss not on the generic fixture.
**Q143** — stall and toss are new catalog objects.
