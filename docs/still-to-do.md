# Still to do

**Working on: maps first public list (Q218–).** Leftover English: market
types from a public exchange already cited in this spec (Betfair
Stream). When a file exists it is named for that list (**Q219**). Public
key leftover English: the exchange’s market type id (**Q220**). Landing
leftover English: an existing OpenBook market type id (**Q221**), only a
market type id (**Q223**); unknown path is the existing unknown
catch-all plus a reason (**Q222**). Do not invent rows or JSON object
keys (**Q189**, **Q224**). No file. Not a registry. Stay `0.3.0-draft`.
Q55 parked.

Questions recorded through **Q224**. Catalog pass closed and on the wire.
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
(**Q180**), then the maps leftover unparked (**Q181**). Q171 leftovers
in this repo logged (**Q190–Q198**). Maps leftover shape closed
(**Q181–Q189**, **Q199–Q203**). Spec walk stopped (**Q204**). Next leftover
unnamed; wait (**Q205**). Named leftovers exhausted (**Q206–Q214**). No
maps directory or file until a list is named (**Q215**). Do not invent
the Q171 recipe (**Q216**). Question pass closed (**Q217**). First public
list leftover English named (**Q218**). File named for that list
(**Q219**). Public key leftover English: the exchange’s market type id
(**Q220**). Landing leftover English: an existing OpenBook market type
id (**Q221**), only a market type id (**Q223**); unknown path is the
existing unknown catch-all plus a reason (**Q222**). JSON object keys
still wait (**Q224**).
Q46–Q49 and **Q56** are on the wire. **Q50** is the docs-vs-schema name check in
`tools/validate.py`.

## Goal (this walk)

**First public maps list — leftover English (Q218–Q224).** Market types
from a public exchange already cited in this spec (Betfair Stream).
When a file exists it is named for that list. Public key leftover
English: the exchange’s market type id. Landing leftover English: an
existing OpenBook market type id, only a market type id; unknown path
is the existing unknown catch-all plus a reason. Do not invent rows or
JSON object keys. No file. Not a registry. Not Q55.

## Goal (previous — maps leftover, closed)

**Maps leftover.** Public key plus an existing OpenBook id, or the
unknown catch-all plus a reason (**Q181**, **Q185**). Reason only on the
unknown catch-all (**Q186**, **Q201**); leftover English, not a token
list (**Q200**). One directory named for maps, not inside the vocab
lists (**Q182**, **Q183**). One JSON file per public list when files
exist (**Q187**, **Q188**): a JSON array of row objects (**Q199**);
object keys wait (**Q189**); a public key at most once per file
(**Q202**); row order not significant (**Q203**). First public list
leftover English: market types from a public exchange already cited
(Betfair Stream) (**Q218**). Shape is on the spec (§3.5). Not a feed
document. No file until keys exist (**Q189**, **Q215**).

## Goal (previous — Q171 leftovers in this repo)

Prefix file first (`propertyID` schemes) (**Q191**). Named for prefixes,
in the register leftover, not inside the vocab lists (**Q192**). Plain
tokens like the existing `propertyID` examples (**Q193**). Catch-all
unknown bucket (**Q194**, **Q34**). Prefix-file shape logged; list
waits. Fingerprint recipe is leftover English; no new field (**Q196**).
Named for fingerprint, in the register leftover (**Q197**). Fingerprint
location logged; recipe text waits. Next leftover is the pinned fixture example
(**Q198**). Anchor policy wait. No file. No new wire field.

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
- **Q186** — reason required only when the landing is the unknown catch-all; no file in this pick.
- **Q187** — one file per public list when files exist; name still waits (**Q184**); no file in this pick.
- **Q188** — when files exist, JSON, same as the shared vocab lists; name still waits; no file in this pick.
- **Q189** — JSON object keys wait; do not invent names; row meaning stays leftover English (**Q185**); no file in this pick.
- **Q190** — Q171 leftovers in this repo logged. Files wait. No new wire field.
- **Q191** — prefix file first (`propertyID` schemes); fingerprint, pinned fixture example, and anchors wait; no file in this pick.
- **Q192** — named for prefixes, in the register leftover, not inside the vocab lists; no file in this pick.
- **Q193** — plain tokens like the existing `propertyID` examples; not Q5 short form; list waits.
- **Q194** — unknown bucket (**Q34**); list waits; `propertyID` stays a string.
- **Q195** — prefix-file shape logged; list waits; next leftover is the fingerprint recipe.
- **Q196** — fingerprint is leftover English only; no new field; publisher-own id stays canonical.
- **Q197** — named for fingerprint, in the register leftover, not inside the vocab lists; no file in this pick.
- **Q198** — fingerprint location logged; recipe text waits; next leftover is the pinned fixture example.
- **Q199** — when files exist, a JSON array of row objects; keys wait; name waits; no file in this pick.
- **Q200** — reason is leftover English (a free string); do not invent a reason list; no file in this pick.
- **Q201** — reason forbidden when the landing is an existing OpenBook id; no file in this pick.
- **Q202** — in one file, a public key at most once; no file in this pick.
- **Q203** — row order is not significant; do not invent a sort; no file in this pick.
- **Q204** — stop this spec walk. Maps shape logged. First public list name waits. No file.
- **Q205** — next leftover unnamed; wait. Not Q55.
- **Q206** — named leftovers on this walk exhausted; stay stopped. Not Q55.
- **Q207** — do not unpark Q172 profile pointers as this walk. Not Q55.
- **Q208** — do not unpark Q173 hosted validator as this walk. Not Q55.
- **Q209** — position token lists still wait. Not Q55.
- **Q210** — first maps public list name still waits (**Q184**). Not Q55.
- **Q211** — stay `0.3.0-draft`. Not a version cut. Not Q55.
- **Q212** — Q55 stays parked until 1.0+.
- **Q213** — Q96 stays not this spec.
- **Q214** — Q79 / Q81 stay omit.
- **Q215** — no maps directory or file until a list is named.
- **Q216** — do not invent the Q171 fingerprint recipe or prefix-file contents.
- **Q217** — this question pass closes. No further leftover questions until a leftover is named.
- **Q218** — first public list leftover English: market types from a public exchange already cited (Betfair Stream); no rows; no JSON keys; no file.
- **Q219** — when a file exists it is named for that public list; keys wait; no file.
- **Q220** — public key leftover English: the exchange’s market type id; JSON names wait; no file.
- **Q221** — landing leftover English: an existing OpenBook market type id; not a fixture; not a registry; JSON names wait; no file.
- **Q222** — unknown path: existing unknown catch-all market type plus a reason; no second unknown; JSON names wait; no file.
- **Q223** — this first list lands only on an OpenBook market type id; not sport; not segment; no file.
- **Q224** — leftover English stays; JSON object keys still wait; do not invent names; no file.

### Parked

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).
- **Q171** — namespace prefix file; fixture fingerprint recipe and a
  pinned fixture example; anchor policy prose.
- **Q172** — profile repositories (prediction-market, reporting,
  integrity, register) that pin a core major.
- **Q173** — hosted validator and a feed list beside it, not on
  discovery.

## Next question (not decided)

**Next questions: Q225–Q227.** Maps directory still waits until keys exist; many public keys may share one landing; do not invent rows. Recs in chat. A pasted letter is not implement. Wire is a separate ask.

## Done (Q32–Q224)

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
**Q186** — reason required only when the landing is the unknown catch-all.
**Q187** — one file per public list when files exist; name still waits.
**Q188** — when files exist, JSON, same as the shared vocab lists.
**Q189** — JSON object keys wait; do not invent names.
**Q190** — Q171 leftovers in this repo logged; files wait; no new wire field.
**Q191** — prefix file first; fingerprint, pinned fixture example, and anchors wait; no file now.
**Q192** — named for prefixes, in the register leftover, not inside the vocab lists; no file now.
**Q193** — plain tokens like the existing `propertyID` examples; list waits.
**Q194** — unknown bucket; list waits; field stays a string.
**Q195** — prefix shape logged; list waits; next leftover is the fingerprint recipe.
**Q196** — fingerprint is leftover English only; no new field.
**Q197** — named for fingerprint, in the register leftover; no file now.
**Q198** — fingerprint location logged; recipe text waits; next leftover is the pinned fixture example.
**Q199** — when files exist, a JSON array of row objects.
**Q200** — reason is leftover English (a free string); not a token list.
**Q201** — reason forbidden when the landing is an existing OpenBook id.
**Q202** — in one file, a public key at most once.
**Q203** — row order is not significant; do not invent a sort.
**Q204** — stop this spec walk; maps shape logged; first public list name waits.
**Q205** — next leftover unnamed; wait.
**Q206** — named leftovers on this walk exhausted; stay stopped.
**Q207** — do not unpark Q172 profile pointers as this walk.
**Q208** — do not unpark Q173 hosted validator as this walk.
**Q209** — position token lists still wait.
**Q210** — first maps public list name still waits.
**Q211** — stay `0.3.0-draft`.
**Q212** — Q55 stays parked until 1.0+.
**Q213** — Q96 stays not this spec.
**Q214** — Q79 / Q81 stay omit.
**Q215** — no maps directory or file until a list is named.
**Q216** — do not invent the Q171 fingerprint recipe or prefix-file contents.
**Q217** — this question pass closes.
**Q218** — first public list leftover English: market types from a public exchange already cited (Betfair Stream); no file.
**Q219** — when a file exists it is named for that public list.
**Q220** — public key leftover English: the exchange’s market type id.
**Q221** — landing leftover English: an existing OpenBook market type id.
**Q222** — unknown path: existing unknown catch-all plus a reason.
**Q223** — this first list lands only on a market type id.
**Q224** — JSON object keys still wait.
