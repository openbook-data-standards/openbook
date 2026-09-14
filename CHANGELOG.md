# Changelog

All notable changes to the OpenBook standard are recorded here.
Format follows Keep a Changelog; versioning follows [`VERSIONING.md`](VERSIONING.md).

## [Unreleased]

### Added
- **Examples page** — [`docs/examples.md`](docs/examples.md) walks the
  existing `examples/` documents in `sequence` order (GTFS-style sample feed,
  not a sandbox). `publisher.example.json` lists `bigbook` so it matches the
  market and odds samples. No wire change.
- [`docs/protocol-comparison.md`](docs/protocol-comparison.md) — technical
  comparison of GTFS, GBFS, MQTT, WIS2, FIX, ISO 20022, OpenRTB, Betfair
  Stream, Sportradar UOF, OsmChange, CAP and ODF against the OpenBook wire
  (what is adopted, shape-only, later, or rejected).

### Changed
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
- **Q148** — this walk is live series win counts. Names wait. Toss elected
  still waits. Not wired in this pick.
- **Q149** — win counts are one row per series side on live `series`; same
  `participant` ids as this fixture. Count names wait. Not wired.
- **Q150** — exactly two rows, both required; this fixture’s two
  participants. Not wired.
- **Q151** — a win ticks when this game is down; not while live. Not
  wired.
- **Q152** — the number is games won; integer; 0 allowed; no draw column.
  Not wired.
- **Q153** — each row’s count is `total`. Array name waits. Not wired.
- **Q154** — array name leftover English at implement; not `scores`; not
  `participants`. Not wired.


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
