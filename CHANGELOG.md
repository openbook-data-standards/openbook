# Changelog

All notable changes to the OpenBook standard are recorded here.
Format follows Keep a Changelog; versioning follows [`VERSIONING.md`](VERSIONING.md).

## [Unreleased]

### Added
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
- **Q46** — `snapshotComplete` on push; `heartbeat` + `heartbeatMs`; pull stale
  `since` is HTTP 410 + RFC 9457 (log only; no schema in this patch).
- **Q47** — `conflated: true` when ticks were dropped.
- **Q48** — `ttl` seconds (GBFS).
- **Q49** — GBFS-shaped discovery document.
- **Q50** — later PR: one-way docs-vs-schema name CI.
- **Q51** — no consumer-view schema file.
- **Q52** — CloudEvents wrap never.
- **Q53** — DNS-style ids never; Q4/Q5 stand.
- **Q54** — no OpenAPI file in this repo; `since=` / 410 stay in the spec.
- **Q55** — later PR: schema-diff CI at 1.0+ only.
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
- [`docs/still-to-do.md`](docs/still-to-do.md) — Q11 closed; Q46–Q49 wire not
  built.

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
  `fixture_change`; `market/update` (CAP-style `msg_type` / `references`)
  replaces `market_status`.
- **Odds push-first**: `odds/change` SHOULD be pushed, a `since=` pull MAY be
  offered; `market/snapshot` for recovery.
- **Hierarchy**: sport → league (`competition_type`, optional `organizer`) →
  season → stage (open, Q20) → fixture → segment. **Participants belong to a
  sport**, not a league.
- `*_type` naming for small vocabularies: `competition_type`,
  `participant_type`, `market_type`, `stage_type`.

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
