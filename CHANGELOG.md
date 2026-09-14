# Changelog

All notable changes to the OpenBook standard are recorded here.
Format follows Keep a Changelog; versioning follows [`VERSIONING.md`](VERSIONING.md).

## [Unreleased]

### Added
- [`docs/roadmap.md`](docs/roadmap.md) — three-year direction
  (non-normative). **Q171** register, not an entity database;
  **Q172** profiles as separate specifications; **Q173** feed list
  beside the validator, not on discovery (Q94 stands). No wire change.
- **Vocabularies** — every row in
  [`vocabularies/sports.md`](vocabularies/sports.md),
  [`vocabularies/segments.md`](vocabularies/segments.md) and
  [`vocabularies/market_types.md`](vocabularies/market_types.md) carries a
  description and settlement rule. Sports grow to what mainstream books
  price (futsal, badminton, handball, field hockey, snooker, darts,
  cycling, Australian rules, swimming, skiing, lacrosse, esports
  titles as disciplines). Every sport names `full-time` as the whole
  contest as graded. Market types include common score, game, player, and
  outright boards. Human map: [`docs/taxonomy.md`](docs/taxonomy.md).
- **`composite` market shape** — parlays and same-game parlays are that
  shape (legs are other market outcomes). Schema, spec, and
  [`examples/market_type.example.json`](examples/market_type.example.json).
- **Examples page** — [`docs/examples.md`](docs/examples.md) walks the
  existing `examples/` documents in `sequence` order (GTFS-style sample feed,
  not a sandbox). `publisher.example.json` lists `bigbook` so it matches the
  market and odds samples. No wire change.
- [`docs/protocol-comparison.md`](docs/protocol-comparison.md) — technical
  comparison of GTFS, GBFS, MQTT, WIS2, FIX, ISO 20022, OpenRTB, Betfair
  Stream, Sportradar UOF, OsmChange, CAP and ODF against the OpenBook wire
  (what is adopted, shape-only, later, or rejected).

### Changed
- **Maps leftover on the spec** (Q181–Q189, Q199–Q203, Q215) — public
  market / segment keys onto existing OpenBook ids, or the unknown
  catch-all plus a reason. One directory named for maps when files
  exist, not inside the vocab lists; one JSON file per public list;
  array of row objects; object keys wait; reason only on the unknown
  catch-all; public key at most once; order not significant. First
  public list name waits. No directory and no file until then. Not a
  feed document; not on the odds wire.
  [`spec/openbook.md`](spec/openbook.md) §3.5;
  [`docs/roadmap.md`](docs/roadmap.md).
- **Wording** — Q171 leftover **corpus case** is **pinned fixture
  example** (one example fixture the fingerprint recipe is checked
  against). Not the Q40 conformance corpus. Same decisions. No new
  rule.
- [`docs/protocol-comparison.md`](docs/protocol-comparison.md) §15 last
  bullet names the rejected thing (an OpenBook-run entity database);
  §16 records protocols studied after the first pass.
- [`GOVERNANCE.md`](GOVERNANCE.md) — 1.0 target quarter, post-1.0
  producer+consumer rule, one seat per employer, link to the roadmap.
- **Segments: one whole-contest word.** Cricket and motorsport use
  `full-time` (draft ids `full-match` / `full-session` dropped); athletics
  gains `full-time`. Never frozen, so no deprecation entry (Q35).
- `market:odd-even-total` is shape `n-way` (sides `odd` / `even`), not
  `yes-no`; `market:moneyline` is shape `n-way` (two- or three-way).
- [`docs/taxonomy.md`](docs/taxonomy.md): Side as a table, complete
  segment families, market families named by `marketCategory`.
- **Site layout** — header, homepage and doc pages share one wrap width so
  the logo lines up with the page; the crumb sits with the title; TOC
  numbers share a gutter.
- **Site nav** — shorter on-this-page labels (drop the slogan after `:` /
  `(`); numbered TOC rows align; top nav uses a current-page chip. Spec
  headings unchanged.
- **Docs readability** — three tracks: a non-technical
  [`docs/guide.md`](docs/guide.md), a human
  [`docs/taxonomy.md`](docs/taxonomy.md) for shared lists, and a
  table-and-diagram rewrite of [`spec/openbook.md`](spec/openbook.md)
  (no wire change). Vocabularies stay the id lists. Guide has a Saturday
  walkthrough; the decision log has a theme map; homepage has a reading
  path. Still site/docs only.
- **Q11** — names on the participant: required `name`; optional `shortName`,
  `names`, `nameLatin`, `alternateName`. Teams MAY add `location`,
  `nickname`, `registeredName`, `abbreviation`. Persons MAY add `givenName`
  / `familyName`; no `abbreviation`. Fixture `participants[]` copies `name`.
  `player` has no name fields.
- Logged catalog answers on the wire: league/venue `shortName` /
  `registeredName`; Place `timeZone`, `latitude`, `longitude`; publisher
  `inLanguage` / `registeredName`; league `gender` (`men` · `women` ·
  `mixed` · `open`) and `ageGroup`; fixture `surface`; participant `seed`.
- **Q88** — optional `throws` and `bats` on `player` (`left` · `right` ·
  `both`).
- **Q80** — `lineup` live object: fixture-keyed roster `player` ids.
- Plan: cover the Pinnacle Lines API
  ([`docs/still-to-do.md`](docs/still-to-do.md)). No wire change in that note.
- **Q97** — Pinnacle specials are markets; no new object (log only).
- **Q98** — optional `basis` on `market` and `odds/change` (same `scoreUnit`
  list as score/grade). Omit = sport/league `primaryUnit`. Identity includes
  `basis`. Not a new `market:*` id.
- **Q99** — spec only: period offline is a `marketStatus` fan-out; settled
  stays segment `down` + `grade`. No new fields.
- **Q100** — no parlay/teaser flags on the fixture (log only).
- **Q101** — one fixture; `eventStatus` is live. `superEvent` is not a
  live/pregame pair.
- **Q102** — keep `sport:*` ids; map vendor integers with `identifier` /
  `sameAs` (log only).
- **Q103** — market `limit` is enough; Get Line is out of scope (log only).
- **Q104** — typed prop outcomes (CS two counts, HT/FT two results, player
  on the outcome). Field names not in this pick (log only).
- **Q105** — names: `homeTotal` / `awayTotal`; `halfTime` / `fullTime`;
  `player` on the outcome; `side` tokens odd, even, none, home-or-draw,
  away-or-draw, home-or-away. Wired with Q106–Q117.
- **Q106–Q117** — those extras on `market`, `odds/change`, and `grade`.
  One market many rows; player is an id; HT/FT pair; listed CS both
  totals; listed winning margin who+number; no mixed boards; `none` is
  listed; prop-row pass closed.
- **Q118–Q125** — winning-margin plus-bands: `atLeast` (JSON number; 3
  means 3 or more) on `market`, `odds/change`, and `grade`. Plus-band
  row is `participant` + `atLeast` (not outcome `line`); exact margin
  keeps `line`; leftover `other` still allowed; pass closed.
- **Q126–Q133** — player yes/no rows (anytime scorer / to score): same
  `player` id; always present; leftover `other` not used; `no` optional;
  one market, many rows; no market `line`; no new field. Pairing on
  `market` / `odds/change` / `grade`. Spec walk stopped.
- **Q134–Q147** — Q86 leftovers on the wire: catalog `stall` (`fixture`,
  `participant`, `order` as the gate) and `toss` (`fixture`, `participant`
  who won); live `series` (fixture-keyed lead; `stage` is the printed
  round). Not on the generic fixture. Not `score`. Not `competitionType`
  series. Win counts and elected bat/bowl wait. Spec walk stopped.
- **Q148–Q156** — live `series` win counts on the wire: required `wins`
  (exactly two rows; leftover English, not `scores` / `participants`);
  each `participant` + `total` (games won, integer, 0 allowed). A win
  ticks when this game is down. Spec walk stopped. Toss elected and
  best-of length wait.
- **Q157–Q167** — toss `elected` (`bat` · `bowl`, required leftover
  English) and optional `needed` on live `series` (wins needed to take
  the series, integer ≥ 1). Not `total`. Not `line`. Spec walk stopped.
- **Q168** — next leftover unnamed; wait. Not Q55. Not wired in this pick.
- **Q169** — named leftovers on this spec are done. Spec walk stopped.
  Not Q55. Not a version cut.
- **Q170** — this walk is Q76 per-sport position vocab. Field stays
  `position`. Token lists wait. Not Q55. Not a version cut. Not wired
  in this pick.

- **Q174** — keep optional `position`; growable per-sport shared ids;
  unknown tokens tolerated (Q34). Not a closed world list. Not a second
  field. Not ISO. Token lists wait. Not wired in this pick.
- **Q175** — when tokens exist: one vocab file like the other shared
  lists. Schema `position` stays a string. Not a closed enum. No file in
  this pick. Token lists wait. Not wired in this pick.
- **Q176** — position ids use the Q5 short-form family, with the sport
  in the id like segments. Prefix and tokens wait. Not wired in this
  pick.
- **Q177** — first word of position ids is `position`. Tokens wait. Not
  wired in this pick.
- **Q178** — catch-all same pattern as segments (Q34). Token lists wait.
  Not wired in this pick.
- **Q179** — when the file exists it is named for positions, same folder
  as the other shared lists. No file in this pick. Token lists wait.
  Not wired in this pick.
- **Q180** — position-vocab shape is logged. Token lists wait. Spec walk
  stopped. Not Q55. Not a version cut. Not wired in this pick.
- **Q181** — this walk is the maps leftover. Public market / segment
  keys onto existing OpenBook ids, or the unknown catch-all with a
  reason. Not a wire change. No file in this pick.
- **Q182** — when files exist: one maps directory, not inside the vocab
  lists. No file in this pick. First public list waits. Not wired in
  this pick.
- **Q183** — that directory is named for maps. No file in this pick.
  First public list waits. Not wired in this pick.
- **Q184** — first public list name waits. No file in this pick. Do not
  invent a taxonomy. Not wired in this pick.
- **Q185** — a map row is public key plus an existing OpenBook id, or
  the unknown catch-all plus a reason. No file in this pick. Not wired
  in this pick.
- **Q186** — the reason is required only when the landing is the unknown
  catch-all. No file in this pick. Not wired in this pick.
- **Q187** — when files exist: one file per public list. First public
  list name still waits. No file in this pick. Not wired in this pick.
- **Q188** — when files exist: JSON, same as the shared vocab lists.
  First public list name still waits. No file in this pick. Not wired
  in this pick.
- **Q189** — JSON object keys wait. Do not invent names. Row meaning
  stays leftover English. No file in this pick. Not wired in this pick.
- **Q190** — this walk is the Q171 leftovers that live in this repo:
  prefix file; fixture fingerprint recipe and a pinned fixture example; anchor
  policy prose. Not maps. Not a new wire field. Files wait. Not wired
  in this pick.
- **Q191** — prefix file first (`propertyID` schemes). Fingerprint
  recipe, pinned fixture example, and anchor policy wait. No file in this pick.
  Not wired in this pick.
- **Q192** — when the file exists it is named for prefixes, in the
  register leftover, not inside the vocab lists. No file in this pick.
  Not wired in this pick.
- **Q193** — prefix tokens are plain like the existing `propertyID`
  examples. Not the Q5 short form. The list waits. Not wired in this
  pick.
- **Q194** — prefix catch-all is an unknown bucket (Q34). List waits.
  `propertyID` stays a string. Not wired in this pick.
- **Q195** — prefix-file shape is logged. The list waits. Next leftover
  in this walk is the fingerprint recipe. No file in this pick. Not
  wired in this pick.
- **Q196** — fingerprint is leftover English only. No new field.
  Publisher-own id stays canonical. Not wired in this pick.
- **Q197** — when the recipe exists it is named for fingerprint, in the
  register leftover, not inside the vocab lists. No file in this pick.
  Not wired in this pick.
- **Q198** — fingerprint location is logged. Recipe text waits. Next
  leftover in this walk is the pinned fixture example. No file in this pick. Not
  wired in this pick.
- **Q199** — when files exist: a JSON array of row objects. Keys still
  wait. First public list name still waits. No file in this pick. Not
  wired in this pick.
- **Q200** — the reason is leftover English (a free string). Do not
  invent a reason list. No file in this pick. Not wired in this pick.
- **Q201** — when the landing is an existing OpenBook id, a reason is
  forbidden. No file in this pick. Not wired in this pick.
- **Q202** — in one file, a public key appears at most once. No file in
  this pick. Not wired in this pick.
- **Q203** — row order is not significant. Do not invent a sort. No file
  in this pick. Not wired in this pick.
- **Q204** — maps leftover shape is logged. First public list name
  waits. Spec walk stopped. Not Q55. Not a version cut. Not wired in
  this pick.
- **Q205** — next leftover unnamed; wait. Not Q55. Not wired in this
  pick.
- **Q206** — named leftovers on this walk exhausted; stay stopped. Not
  Q55. Not a version cut. Not wired in this pick.
- **Q207** — do not unpark Q172 profile pointers as this walk. Not Q55.
  Not wired in this pick.
- **Q208** — do not unpark Q173 hosted validator as this walk. Not Q55.
  Not wired in this pick.
- **Q209** — position token lists still wait. Not Q55. Not wired in this
  pick.
- **Q210** — first maps public list name still waits. Not Q55. Not wired
  in this pick.
- **Q211** — stay `0.3.0-draft`. Not a version cut. Not Q55. Not wired
  in this pick.
- **Q212** — Q55 stays parked until 1.0+. Not wired in this pick.
- **Q213** — Q96 stays not this spec. Not wired in this pick.
- **Q214** — Q79 / Q81 stay omit. Not wired in this pick.
- **Q215** — no maps directory or file until a list is named. Not wired
  in this pick.
- **Q216** — do not invent the Q171 fingerprint recipe or prefix-file
  contents. Not wired in this pick.
- **Q217** — this question pass closes. No further leftover questions
  until a leftover is named. Not wired in this pick.
- **Q218** — first public list leftover English: market types from a
  public exchange already cited in this spec (Betfair Stream). No rows.
  No JSON object keys. No file. Not wired in this pick.
- **Q219** — when a file exists it is named for that public list. JSON
  object keys still wait. No file. Not wired in this pick.
- **Q220** — public key leftover English: the exchange’s market type
  id. JSON object keys still wait. No file. Not wired in this pick.
- **Q221** — landing leftover English: an existing OpenBook market type
  id. Not a fixture. Not a registry. JSON object keys still wait. No
  file. Not wired in this pick.
- **Q222** — unknown path leftover English: the existing unknown
  catch-all market type plus a reason. No second unknown. JSON object
  keys still wait. No file. Not wired in this pick.
- **Q223** — this first list lands only on an OpenBook market type id.
  Not a sport id. Not a segment id. No file. Not wired in this pick.
- **Q224** — leftover English stays. JSON object keys still wait. Do
  not invent names. No file. Not wired in this pick.
- **Q225** — no maps directory or file until JSON object keys exist.
  Naming leftover English does not unpark them. Not wired in this pick.
- **Q226** — many public keys may share one OpenBook market type id.
  Public key at most once stays. No file. Not wired in this pick.
- **Q227** — do not invent rows. Rows wait. No file. Not wired in this
  pick.
- **Q228** — omitted public key is unmapped. Unknown catch-all is only
  for rows that exist. No file. Not wired in this pick.
- **Q229** — no second public list this walk. No file. Not wired in
  this pick.
- **Q230** — first-list leftover English closes until a later question
  names JSON object keys. Not wired in this pick.
- **Q231** — next leftover unnamed; wait. Not wired in this pick.
- **Q232** — do not invent JSON object keys. Keys still wait. Not wired
  in this pick.
- **Q233** — do not unpark the Q171 fingerprint recipe or prefix-file
  contents. Not wired in this pick.
- **Q234** — named leftovers on this walk exhausted; stay stopped. Not
  wired in this pick.
- **Q235** — stay `0.3.0-draft`. Not a version cut. Not wired in this
  pick.
- **Q236** — this question pass closes. No further leftover questions
  until a leftover is named. Not wired in this pick.
- **Q237** — next leftover is JSON object keys for the first maps
  file. Names wait until a later question. Not wired in this pick.
- **Q238** — three leftover-English slots: public key, landing, and
  reason. Do not invent JSON names in this pick. Not wired in this pick.
- **Q239** — name the JSON keys on this walk, in a later question. This
  pick does not invent names. Not wired in this pick.
- **Q240** — public-key JSON name is camelCase leftover English. Do not
  overload identifier. No file. Not wired in this pick.
- **Q241** — landing JSON name is `id`. No file. Not wired in this pick.
- **Q242** — reason JSON name is `reason`. No file. Not wired in this
  pick.

### Removed
- `localName`, `additionalName`, `honorificPrefix`, `honorificSuffix` on
  participant (pre-1.0; Q11). Native script is `nameLatin`.

### Added
- **Input bounds** — shared primitives in
  [`schema/common.schema.json`](schema/common.schema.json) carry `maxLength` /
  `maxItems`, so conformant parsers reject oversized input; covered by
  `conformance/invalid/alternate-name-too-long.json`.
- **Q96** — vendor mapping, starter CLI, and translate ABC are **not**
  this spec; planned names openbook-starter / openbook-translate
  ([`docs/decisions.md`](docs/decisions.md)). Repos not created in this
  change.
- **Q95** — protocol-fit pass closed; next work is a new area, not more
  take/don't-take pins from that comparison list
  ([`docs/decisions.md`](docs/decisions.md)).
- **Q94** — no spec-owned multi-publisher index; one discovery URL per
  publisher (Q49); an aggregator is itself a publisher (Q1)
  ([`docs/decisions.md`](docs/decisions.md)).
- **Q93** — FIX session is not the OpenBook session; Q33/Q46 stand
  ([`docs/decisions.md`](docs/decisions.md)).
- **Q92** — ISO 20022 is not the OpenBook model or encoding; Q13/Q38/Q44
  stand ([`docs/decisions.md`](docs/decisions.md)).
- **Q91** — JSON Patch (RFC 6902) is never an alternate change encoding; Merge
  Patch (Q8) stands ([`docs/decisions.md`](docs/decisions.md)).
- **Q90** — no GBFS-style data wrapper; discovery stays `{ lastUpdated, ttl,
  feeds }` at the root (Q49); objects and change messages stay themselves
  ([`docs/decisions.md`](docs/decisions.md)).
- **Q89** — JSON (`application/json`) is the required v1 encoding; additional
  encodings MAY exist later as optional bindings; scaffolding stays JSON
  ([`docs/decisions.md`](docs/decisions.md)).
- **Security model** — [`SECURITY.md`](SECURITY.md) states what the standard
  secures (closed schemas, canonical-id integrity) and what it delegates to
  deployments (TLS, authn/authz, rate limiting, schema-fetch integrity).
- **Feed monitoring** — [`spec/openbook.md`](spec/openbook.md) §5.3 names the
  liveness, continuity, freshness, and conformance signals a consumer alarms on.
- **Q32** — FULL-TRANSITIVE compatibility within a frozen major
  ([`VERSIONING.md`](VERSIONING.md)).
- **Q33** — Level L delivery/recovery: all eight guarantees MUST
  ([`spec/openbook.md`](spec/openbook.md) §5.1).
- **Q34** — catch-all `unknown`/`other`; consumers MUST tolerate unrecognised
  values.
- **Q35** — never reuse frozen ids, list-values, or field names;
  [`vocabularies/deprecated.md`](vocabularies/deprecated.md).
- **Q36** — machine-readable deprecation (reason, replacement, sunset);
  removal only at MAJOR after the window.
- **Q37** — closed when you write, open when you read; `x_` still vendor extras.
- **Q38** — camelCase is canonical; current-doc snake_case drift fixed.
- **Q39** — odds and lines are decimal strings; money is
  `{amount, currency}`; decimal odds only on the wire.
- **Q40** — conformance gate is spec + schema + language-agnostic corpus
  ([`conformance/`](conformance/)); the Python validator is one runner.
- **Q41** — GBFS-style ops principles (`ttl`, one discovery URL, co-serve
  versions); two independent implementations freeze 1.0 only.
- **Q42** — AsyncAPI describes the push streams
  ([`spec/asyncapi.yaml`](spec/asyncapi.yaml)); CloudEvents and DNS-style
  ids deferred.
- **Q43** — off the board is `marketStatus`; outcome removal is Merge Patch
  `null`; `odds: "0"` is not a takedown.
- **Q44** — `baseCurrency` once per feed; money is `{amount}`; another
  currency is another subscription.
- **Q45** — priced markets MUST carry `limit`; sport/league defaults
  optional; most specific wins.
- **Q46** — `snapshotComplete` and `heartbeat` on the wire; publisher
  `heartbeatMs`; pull stale `since` is HTTP 410 + RFC 9457.
- **Q47** — optional envelope `conflated: true` when ticks were dropped.
- **Q48** — `ttl` integer seconds (GBFS); optional on publisher, required on
  discovery.
- **Q49** — GBFS-shaped discovery document
  (`schema/discovery.schema.json`).
- **Q50** — one-way docs-vs-schema name CI in `tools/validate.py` (spec/docs
  names MUST exist on a schema; extra schema fields allowed).
- **Q51** — no consumer-view schema file.
- **Q52** — CloudEvents wrap never.
- **Q53** — DNS-style ids never; Q4/Q5 stand.
- **Q54** — no OpenAPI file in this repo; `since=` / 410 stay in the spec.
- **Q55** — later PR: schema-diff CI at 1.0+ only.
- **Q56** — MCP servers and additional plugins are discovery feeds
  (`kind` `mcp` / `plugin`, plus `id` / `schemaUrl`). OpenBook does not wrap
  MCP or ship its schema; payloads stay OpenBook documents.
- **Q11 / Q57** — names decided (log only): board `name`; optional team
  location/nickname/registeredName; person given/family; `shortName`; team-only
  `abbreviation`; `names` / `nameLatin`; fixture copies `name`. Cite ISO or none.
- **Q59** — league/venue use the team name package; sport/market/segment `name`
  only.
- **Q60** — season `name` is display; dates are Q9. Stage `name` + optional
  dates. Publisher `name` + optional `registeredName`.
- **Q62** — fixture `location` stays nested Place; GeoNames optional; no
  first-class venue object in this walk.
- **Q64** — optional IANA `timeZone` on Place; timestamps stay Q9.
- **Q66** — fixture `name` optional display; participants + `startDate` are facts.
- **Q68** — optional publisher `inLanguage` (ISO 639-1); bare `name` is in that language.
- **Q69** — Place is city + Q10 territory; no street/postal.
- **Q70** — optional WGS 84 lat/long on Place.
- **Q71** — no venue capacity field.
- **Q72** — optional league category men/women/mixed/open; not on the person.
- **Q73** — optional league `ageGroup` (U21, …); growable vocab.
- **Q74** — no date of birth on the wire.
- **Q75** — no height/weight; number/position stay on `player`.
- **Q76** — `player.position` free string; no ISO; vocab later.
- **Q77** — no kit/colour fields.
- **Q78** — no home stadium on the team; match venue is fixture location.
- **Q79** — no coach/manager object for now.
- **Q80** — match XI is a later live object; `player` stays roster.
- **Q81** — no referee/officials for now.
- **Q82** — omit encyclopedia fields (weather, TV, bios extras, stats dumps,
  etc.); Q74/Q75 stay omit.
- **Q84** — optional fixture `surface` (grass/clay/hard/…).
- **Q85** — optional `seed` on the fixture participant row.
- **Q86** — generic fixture extras stop at surface + seed; no metadata bag.
- **Q87** — catalog pass closed; next work is a new area, not more fixture keys.
- [`docs/still-to-do.md`](docs/still-to-do.md) — catalog names/place/`gender`
  on the wire; Q55 remains a later PR (1.0+).

- Schemas for the objects the spec names but had no schema: `season`, `player`
  (roster membership), `market` (snapshot/update document), `score` (Q23) and
  **`grade`** (replaces `settlement`; Q27/Q28).
- **Three statuses** (Q25/Q30): `eventStatus`, per-segment `segmentStatus`
  (`down` once, terminal), `marketStatus`; `statusReason` vocabulary.
- **Units on every score line** (Q26): `scoreUnit` vocabulary; `primaryUnit` on
  sport and league ruleset.
- **Fixture-first topics** (Q29): `openbook/v1/<publisher>/<sport>/fixture/<id>/<object>/<action>`.
- Corrections as errata (`correction: true`), never a second down (Q31).
- `vocabularies/segments.md` — per-sport segment ids.
- Examples: `score.example.json`, `grade.example.json`.

## [0.3.0-draft] — 2026-09-12

Breaking rename of the live wire around decisions Q14–Q21. Not frozen.

### Changed
- **Object/action streams**: `openbook/v1/<publisher>/<object>/<action>/<sport>/<id>`,
  keyed by fixture for fixture-scoped objects. Actions: snapshot · create ·
  update · delete, plus `change` for odds only.
- **One change envelope** (`schema/change.schema.json`) replaces the per-message
  schemas: `odds/change` replaces `odds_change`; `fixture/update` replaces
  `fixture_change`; `market/update` (CAP-style `msgType` / `references`)
  replaces `market_status`.
- **Odds push-first**: `odds/change` SHOULD be pushed, a `since=` pull MAY be
  offered; `market/snapshot` for recovery.
- **Hierarchy**: sport → league (`competitionType`, optional `organizer`) →
  season → stage (open, Q20) → fixture → segment. **Participants belong to a
  sport**, not a league.
- `*Type` naming for small vocabularies: `competitionType`,
  `participantType`, `marketType`, `stageType`.

- **Field names are camelCase and follow schema.org** (Q13 d): `startDate`,
  `dateModified`, `datePublished`, `alternateName`, `sameAs` (Wikidata URL,
  replaces `wikidata`), `identifier` (PropertyValue list, replaces
  `external_ids`), `superEvent`, `eventStatus`, `location` (Place); `*Type`
  vocabularies. Documents may carry JSON-LD `@context` / `@type`.
- **Participants**: one object for teams and individuals (`participantType`);
  every fixture participant carries `role` (home · away · neutral) **and**
  `order` (Q22). Name model after vCard/X.520 and ODF (Q11): `shortName`,
  `abbreviation`, `alternateName`, `localName`, `familyName`, `givenName`…
- **Stages are recursive** (Q20): `stage.schema.json` with `parent` and
  `stageType` (phase · group · round · matchday · leg · seriesGame).
- Schema files renamed: `reference_participant` → `participant`,
  `reference_region` → `region`, `reference_sport` → `sport`.

### Added
- `schema/stage.schema.json`; `examples/participant.example.json`,
  `examples/stage.example.json`.
- `schema/change.schema.json`, `schema/league.schema.json`;
  `examples/fixture_update.example.json`, `examples/market_update.example.json`.

### Removed
- `schema/fixture_change.schema.json`, `schema/market_status.schema.json` and
  their examples (folded into the envelope).

## [0.2.0-draft] — 2026-09-12

Not frozen; the wire may change before 1.0.

### Added
- `docs/decisions.md` — the design decision log (Q1–Q9 decided; Q7 proposed;
  Q10–Q13 open): purpose, matching via standard facts, provenance, shared vs
  publisher-own ids, slug + URN id spelling, external ids, diffs everywhere
  with JSON Merge Patch semantics, sequence-based `since`, ISO 8601 everywhere.
- `docs/building-blocks.md` — the widely used standards OpenBook builds on
  (ISO 3166-1/-2, 639-1, 4217, 8601/RFC 3339, Wikidata, schema.org, RFC 7386,
  RFC 8141, UUID v7, JSON Schema, OpenAPI, AsyncAPI, CloudEvents, RFC 9457).
- `docs/industry-patterns.md` — review of public betting APIs (KIBL, Pinnacle,
  Betfair, Sportradar, GTFS-Realtime): patterns adopted and avoided.

- `docs/industry-patterns.md`: OpenStreetMap (tag governance, id+version,
  OsmChange minutely diffs, Wikidata cross-refs) and the weather system (WMO
  WIS 2.0 MQTT pub/sub and topic hierarchy, OASIS CAP 1.2 alerts, METAR/TAF,
  GRIB/BUFR, NWS API). Decisions Q14 (stream grammar) and Q15 (alerts) opened.

### Changed (the v0.2 spec rewrite)
- Fixtures, leagues, teams and players are **publisher-own ids + standard
  facts** (Q2/Q4/Q7); the v0.1 neutral minted fixture id is gone.
- `source` + `provenance` on every market (Q1/Q3); `sequence` + `updated_at`
  on every object; `fixture_change` and `market_status` messages; `since=` as
  a sequence cursor; JSON Merge Patch semantics for all changes (Q8).
- Wikidata QID as the shared entity id on leagues, participants, players,
  venues, territories — required when it exists, null otherwise (Q12).
- New schemas: `common`, `publisher`, `reference_region`,
  `reference_participant`, `fixture_change`, `market_status`; `fixture` and
  `odds_change` rewritten. New examples for `fixture_change`, `market_status`.
- Proposed and implemented provisionally: stream grammar (Q14), CAP-shaped
  market_status (Q15).
- Region model per Q10: CLDR territories (ISO 3166-1/-2 + `XK`/`EU`/`UN`) with
  CLDR localized names; `ioc_code` / `fifa_code` / `wikidata` crosswalks.

## [0.1.0-draft] — 2026-09-12

Initial scaffold. Not frozen; the wire may change before 1.0.

### Added
- The two-tier model (reference + live) and core conventions
  (readable namespaced ids, ISO 8601 / 4217 / 3166, decimal odds).
- Reference objects: sport, region/location, league, season, participant,
  player, segment, market type, side, fixture.
- Live messages: `odds_change`, `score_change`, `settlement`, `market_status`.
- JSON Schemas for `reference_sport`, `fixture`, `market_type`, `odds_change`.
- Controlled vocabularies (starter): sports (with athletics disciplines),
  market types.
- Governance model (open spec / closed code, staged governance), versioning
  rules, contributing guide, and validating examples.
