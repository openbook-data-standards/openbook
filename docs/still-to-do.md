# Still to do

Questions recorded through **Q163**. Catalog pass closed and on the wire.
**Q88** `throws` / `bats` are on `player`. **Q80** `lineup` is on the wire.
Protocol-fit pass closed (**Q89–Q95**). **Q96** vendor mapping / starter is
not this spec. Pinnacle Lines walk closed (**Q97–Q103**). Prop-row pass
closed (**Q104–Q117**) and on the wire. Plus-band pass closed
(**Q118–Q125**) and on the wire. Yes/no player pass closed
(**Q126–Q132**) and on the wire. Q86 leftovers pass closed
(**Q134–Q146**) and on the wire (`stall`, `toss`, live `series`). Spec
walk stopped (**Q147**), then unparked for series win counts (**Q148**).
Series win-count pass closed (**Q148–Q155**) and on the wire (`wins`). Spec
walk stopped (**Q156**), then unparked for toss elected then best-of
(**Q157**).
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk)

**Toss elected closed; best-of length next.** Elected: on `toss`, one
required token (bat or bowl), leftover English at implement. Best-of: on
live `series`; wins needed to take the series. Names wait.

## Goal (previous — series win counts, closed)

Exactly two rows on live `series`, both required; same `participant` ids
as this fixture. A win ticks when this game is down. The number is games
won (integer, 0 allowed) on `total`. Array name is `wins`. Toss elected
still waits.

## Goal (previous — Q86 leftovers, closed)

Racing `stall` and cricket `toss`: two catalog objects. Playoff series:
round on `stage`; live `series` is the lead. Not more keys on every
fixture. Win counts on the wire (**Q148–Q155**). Elected bat/bowl
waits.

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
- **Q134–Q146** — `stall` and `toss` catalog objects; live `series` lead;
  pass closed.
- **Q148–Q155** — live `series` `wins` (exactly two rows; `participant` +
  `total`); pass closed.

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
- **Q147** — stop this spec walk (superseded as the next area by Q148).
- **Q156** — stop this spec walk (superseded as the next area by Q157).
- **Q157** — toss elected then best-of this pass; elected first; names wait.
- **Q158** — elected sits on existing `toss`.
- **Q159** — one token, bat or bowl; field name leftover English at
  implement.
- **Q160** — elected required on `toss`.
- **Q161** — elected rules closed; then best-of.
- **Q162** — best-of sits on live `series`.
- **Q163** — the number is wins needed to take the series.

### Parked

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- Whether that number is required, and leftover English vs reuse `total`.

## Done (Q32–Q163)

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
**Q134–Q146** — Q86 leftovers; `stall` / `toss` / live `series` on the wire;
pass closed.
**Q147** — stop this spec walk.
**Q148–Q155** — series win counts on the wire (`wins`).
**Q156** — stop this spec walk.
**Q157** — toss elected then best-of this pass.
**Q158** — elected sits on existing `toss`.
**Q159** — one token, bat or bowl.
**Q160** — elected required on `toss`.
**Q161** — elected rules closed.
**Q162** — best-of sits on live `series`.
**Q163** — wins needed to take the series.
