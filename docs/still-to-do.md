# Still to do

**Working on: maps leftover (Q181–).** Public key plus an existing
OpenBook id, or the unknown catch-all plus a reason (**Q185**). One
directory named for maps, not inside the vocab lists (**Q182**,
**Q183**). First public list name waits (**Q184**). Not a wire change.
No file now. Not Q55. Not position token lists.

Questions recorded through **Q185**. Catalog pass closed and on the wire.
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
(**Q157**). Toss-elected and best-of pass closed (**Q157–Q166**) and on
the wire (`elected`, `needed`). Spec walk stopped (**Q167**), then the
next leftover was unnamed (**Q168**). Named leftovers exhausted; spec
walk stopped (**Q169**), then Q76 position vocab unparked (**Q170**).
Roadmap pass closed (**Q171–Q173**): register not an entity database;
profiles are separate specifications; feed list is validator tooling.
Position-vocab shape closed (**Q174–Q179**). Spec walk stopped
(**Q180**), then the maps leftover unparked (**Q181**).
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk)

**Maps leftover — this is the open walk.** Public key plus an existing
OpenBook id, or the unknown catch-all plus a reason (**Q181**, **Q185**).
One directory named for maps, not inside the vocab lists (**Q182**,
**Q183**). Cite at least one public taxonomy. First public list name
waits (**Q184**). Not a wire change. No file now.

## Goal (previous — Q76 position vocab shape, closed)

**Per-sport position vocab (Q76).** Field stays `position`. Growable
per-sport shared ids (**Q174**). One vocab file when lists exist,
named for positions (**Q175**, **Q179**). Short-form like Q5; sport in
the id like segments (**Q176**). First word is `position` (**Q177**).
Catch-all like segments (**Q178**). Token lists wait. No file.

## Goal (previous — roadmap, closed)

**Closed.** Roadmap logged. Register is prefixes + optional fixture
fingerprint + anchors, not an OpenBook-run entity database (**Q171**).
Profiles are separate specifications (**Q172**). Feed list lives beside
the validator (**Q173**). Q76 position vocab was the leftover walk
(**Q170**); shape now logged (**Q174–Q179**). No wire change.

## Goal (previous — named leftovers, closed)

Named leftovers through `elected` / `needed` were treated as done
(**Q169**), then Q76 vocab unparked.

## Goal (previous — toss elected and best-of, closed)

Elected: on `toss`; required `elected` (`bat` · `bowl`). Best-of:
optional `needed` on live `series`; wins needed to take the series; ≥ 1
when present; not `total`.

## Goal (previous — series win counts, closed)

Exactly two rows on live `series`, both required; same `participant` ids
as this fixture. A win ticks when this game is down. The number is games
won (integer, 0 allowed) on `total`. Array name is `wins`.

## Goal (previous — Q86 leftovers, closed)

Racing `stall` and cricket `toss`: two catalog objects. Playoff series:
round on `stage`; live `series` is the lead. Not more keys on every
fixture. Win counts on the wire (**Q148–Q155**). Elected `elected` and
`needed` on the wire (**Q157–Q166**).

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
- **Q157–Q166** — `elected` on `toss` (`bat` · `bowl`); optional `needed`
  on live `series`; pass closed.

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
- **Q167** — stop this spec walk (superseded as the next area by Q168).
- **Q168** — next leftover unnamed; wait.
- **Q169** — named leftovers exhausted; stop this spec walk (superseded by Q170).
- **Q170** — this walk is Q76 per-sport position vocab. Field stays `position`. Token lists wait.
- **Q171** — register, not registry.
- **Q172** — profiles are separate specifications.
- **Q173** — feed list beside the validator (Q94 stands).
- **Q174** — keep optional `position`; growable per-sport shared ids; unknown OK (**Q34**); not a second field; not ISO; token lists wait.
- **Q175** — one vocab file like the other shared lists; schema `position` stays a string; no enum; no file in this pick.
- **Q176** — short-form family as Q5; sport in the id like segments; prefix and tokens wait.
- **Q177** — first word is `position`; tokens wait.
- **Q178** — catch-all same pattern as segments (**Q34**); lists wait.
- **Q179** — named for positions, same folder as the other shared lists; no file in this pick.
- **Q180** — stop this spec walk. Shape logged. Token lists wait.
- **Q181** — maps leftover this walk. Not a wire change. No file in this pick.
- **Q182** — one maps directory, not inside the vocab lists; no file in this pick; first public list waits.
- **Q183** — directory named for maps; no file in this pick; first public list waits.
- **Q184** — first public list name waits; no file in this pick; do not invent a taxonomy.
- **Q185** — map row: public key plus existing OpenBook id, or unknown catch-all plus a reason; no file in this pick.

### Parked

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).
- **Q171** — namespace prefix file; fixture fingerprint recipe and a
  corpus case; anchor policy prose.
- **Q172** — profile repositories (prediction-market, reporting,
  integrity, register) that pin a core major.
- **Q173** — hosted validator and a feed list beside it, not on
  discovery.

## Next question (not decided)

**Next question: Q186.** When is the reason required? Rec: only when the landing is the unknown catch-all; no file now. A pasted letter is not implement. Wire is a separate ask.

## Done (Q32–Q185)

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
**Q157–Q166** — toss `elected` and series `needed` on the wire.
**Q167** — stop this spec walk.
**Q168** — next leftover unnamed; wait.
**Q169** — named leftovers exhausted; stop.
**Q170** — Q76 per-sport position vocab this walk; field stays `position`; token lists wait.
**Q171–Q173** — roadmap: register not a registry; profiles separate;
feed list beside the validator. Not on the wire.
**Q174** — keep optional `position`; growable per-sport shared ids; lists wait.
**Q175** — one vocab file like the other shared lists; schema stays a string; no file now.
**Q176** — short-form like Q5; sport in the id like segments; prefix and tokens wait.
**Q177** — first word is `position`; tokens wait.
**Q178** — catch-all same pattern as segments; lists wait.
**Q179** — named for positions, same folder as the other shared lists; no file now.
**Q180** — stop this spec walk; token lists wait.
**Q181** — maps leftover this walk; not a wire change; no file now.
**Q182** — one maps directory, not inside the vocab lists; no file now.
**Q183** — directory named for maps; no file now; first public list waits.
**Q184** — first public list name waits; do not invent a taxonomy.
**Q185** — map row: public key plus existing OpenBook id, or unknown plus a reason.
