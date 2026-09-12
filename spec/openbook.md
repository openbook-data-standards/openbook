# OpenBook — the specification

The normative document defining the **OpenBook** standard.
Version `0.1.0-draft` · 2026-09-12

This is the normative reference. The JSON Schemas in [`../schema/`](../schema/)
are the machine-normative field definitions; where prose and schema disagree,
the schema wins. Field lists below give the shape; the schema gives the exact
types and which fields are required.

Keywords **MUST**, **SHOULD**, **MAY** are used per RFC 2119.

---

## 1. Conventions

- **Identifiers** are readable, namespaced slugs owned by the standard, lowercase
  with `:` as the namespace separator and `-` inside a segment:
  `sport:soccer`, `region:GB`, `league:soccer:GB:premier-league`,
  `market:total`, `segment:baseball:inning-1`, `participant:soccer:GB:arsenal`,
  `fixture:<uuid>`. An id **MUST** be treated as an opaque whole.
- **Time** is ISO 8601 with an explicit offset (`2026-09-12T18:30:00Z`).
- **Currency** is ISO 4217 (`USD`). **Country** is ISO 3166-1 alpha-2 (`GB`).
- **Odds** are decimal (`2.50`) as the canonical form. Display formats
  (American, Hong Kong, Malay, Indonesian) are presentation and are **not** part
  of the wire.
- **Language** for display text is ISO 639-1, defaulting to `en`.
- Every object **MUST** carry `openbook_version`.

## 2. The two tiers

- **Reference tier** (§4): durable, bounded objects. Delivered as documents;
  refreshed when they change. Never carries prices or live state.
- **Live tier** (§5): streamed messages that carry only diffs and reference the
  ids from the reference tier. Ordered, with a monotonic sequence and a change
  signal ("doorbell"). Modeled on GTFS-Realtime: the live feed never re-sends the
  reference tier.

A conformant producer **MUST** publish the reference tier and **MAY** publish any
subset of the live messages, provided each references valid reference ids.

## 3. Mapping (how a source becomes OpenBook)

Every provider id resolves to a canonical id through a **mapping record**
(`reference_map`). A mapping record has: the canonical id, the source
(`provider`, an opaque provider key), the provider's own id, a `confidence`
(`exact` · `derived` · `name_match`), and a `status` (`mapped` · `needs_review`
· `rejected`). A provider's id **MUST NOT** be used as a canonical id. This is
what lets OpenBook stay neutral while ingesting any feed.

## 4. Reference objects

Each object below is a document with `id`, the fields listed, and OPTIONAL
`source` mapping metadata. Full field/type detail is in the matching schema.

### 4.1 `reference_sport`
A sport. Fields: `id` (`sport:*`), `name`, `abbreviation`, `active`.
The sport vocabulary is versioned; see [`../vocabularies/sports.md`](../vocabularies/sports.md).

### 4.2 `reference_region` / `reference_location`
A country and its sub-regions. `reference_region.id` is `region:<ISO-3166-1-a2>`.
Fields: `id`, `name`. Location adds `region` (the parent region id).

### 4.3 `reference_league`
A competition. Fields: `id`, `sport`, `region`, `name`, `abbreviation`,
`active`, and a `ruleset` object (clock, scoring, segment model). Country is a
linked `region`, **never** embedded in `name`.

### 4.4 `reference_season`
Fields: `id`, `league`, `name`, `start_date`, `end_date`, `active`.

### 4.5 `reference_participant`
A team or individual. Fields: `id`, `sport`, `type` (`team` · `individual`),
`name`, `abbreviation`, `aliases` (array), `associations` (array of
`{participant, kind}` for parent/child links). **Home/away is not a property of
a participant** — it is a role assigned on the fixture (§4.10).

### 4.6 `reference_player`
Fields: `id`, `participant` (their team, if any), `sport`, `position`, `name`,
`active`.

### 4.7 `reference_segment`
A slice of a match (half, quarter, inning, set). Fields: `id`, `sport`, `name`,
`ordinal`, `family` (the normalised grouping across vendor numbering). Segments
are first-class objects, not encoded in market ids.

### 4.8 `reference_market_type`
What can be bet. Fields: `id` (`market:*`), `name`, `genre`, `shape` (how the
outcome is priced — e.g. `binary`, `over-under`, `handicap`, `n-way`), `category`
(`main-line` · `score-prop` · `game-prop` · `player-prop` · `outright` ·
`parlay-special` · `same-game-parlay`), and prop flags. The controlled market
vocabulary is [`../vocabularies/market_types.md`](../vocabularies/market_types.md).

### 4.9 `reference_side`
A canonical outcome role: `home`, `away`, `over`, `under`, `draw`, `yes`, `no`,
`participant` (for n-way). The **sign of a handicap and the order of sides are
derived by the standard**, never taken from a source's presentation.

### 4.10 `reference_fixture`
One match — the base object. Fields: `id` (`fixture:<uuid>`), `sport`, `league`,
`season`, `start_time`, `cutoff_time`, `state`, `participants` (array of
`{participant, role}` where `role` is `home`/`away`/an ordinal), and OPTIONAL
`parent` (a live event's pregame parent).

**Fixture identity:** a fixture id is minted by whichever schedule sees the match
first and is source-independent. Producers **MUST** deduplicate on
`(sport, start_time, participant-set)` before minting a new id, so a match only
one minor source carries still gets one clean identity.

## 5. Live messages

Each live message carries `openbook_version`, `sequence` (monotonic per feed),
`timestamp`, and references reference ids. Producers **SHOULD** emit a change
signal per message. Consumers **MUST** merge diffs and **MUST NOT** assume a
message re-sends unchanged state.

### 5.1 `odds_change`
A price diff. Carries `fixture`, and a list of `markets`, each with
`market_type`, OPTIONAL `segment`, OPTIONAL `line` (the handicap/total value),
`status` (`open` · `suspended` · `closed`), and `outcomes` — each with `side`,
`odds` (decimal), OPTIONAL `line`, and `active`. A priced instance is identified
by `(fixture, market_type, segment, line, side)`. Schema:
[`../schema/odds_change.schema.json`](../schema/odds_change.schema.json).

### 5.2 `score_change`
The live status: `fixture`, `state` (`pre` · `live` · `ended` · `suspended`),
`clock` (`{segment, elapsed}`), and `scores` (per participant, per segment).
One producer, one shape, one signal.

### 5.3 `settlement`
Per market/outcome result: `fixture`, and `results` — each with `market_type`,
`segment`, `line`, `side`, `result` (`win` · `lose` · `void` · `half-win` ·
`half-lose`), and `settlement_id`. A re-settle is a **new** `settlement_id`,
never a mutation. A companion `settlement_rollback` references a prior
`settlement_id`.

### 5.4 `market_status`
A standalone open/suspend/close diff for markets without a price change.

## 6. Extensions

A producer **MAY** add fields under an `x_` prefix or a namespaced `extensions`
object. Consumers **MUST** ignore unknown `x_` fields. New sports, leagues,
segments and market types are added to the vocabularies, not invented per-feed.

## 7. Conformance

An implementation is **OpenBook-conformant at level R** if its reference documents
validate against the reference schemas, and **at level L** if its live messages
validate against the live schemas and reference only ids present in the
reference tier. A conformance suite ships separately (roadmap item 3).

## 8. Versioning

Semantic versioning per [`../VERSIONING.md`](../VERSIONING.md). `openbook_version`
on every object states the version it was produced against.
