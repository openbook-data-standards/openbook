# OpenBook — the specification

The normative document defining the **OpenBook** standard.
Version `0.2.0-draft` · 2026-09-12

This is the normative reference. The JSON Schemas in [`../schema/`](../schema/)
are the machine-normative field definitions; where prose and schema disagree,
the schema wins. The decisions behind every rule here are recorded in
[`../docs/decisions.md`](../docs/decisions.md).

Keywords **MUST**, **SHOULD**, **MAY** are used per RFC 2119.

---

## 1. What OpenBook is

OpenBook is **one shared format any publisher emits sportsbook data in**, the
way any transit agency publishes GTFS. It applies whenever odds that originate
from a sportsbook are emitted externally — by the sportsbook itself, or by a
feed that carries them.

- A **publisher** is whoever transmits an OpenBook feed.
- A **source** is whose odds a price is. Every price carries its source, and
  one feed MAY carry many sources (as one GTFS feed carries many agencies).
- A **consumer** reads one or more OpenBook feeds with a single importer.

OpenBook is independent of any sportsbook, data provider or software vendor.
It standardises the data contract only; how a publisher produces or prices
data is out of scope.

## 2. Conventions

- **Time** — ISO 8601 with an explicit offset, everywhere
  (`2026-09-19T14:00:00Z`).
- **Currency** — ISO 4217. **Language** — ISO 639-1.
- **Territory** — Unicode CLDR territory codes: ISO 3166-1 alpha-2 for
  countries (`GB`), ISO 3166-2 for sub-national teams (`GB-ENG`, `US-PR`),
  plus CLDR's extras (`XK`, `EU`). Names come from CLDR.
- **Odds** — decimal is the canonical form (`2.50`). Other formats are
  presentation and are not on the wire.
- **Text** — UTF-8; names keep their diacritics.
- **Field names** — full words, `snake_case`, no abbreviations.
- Every object and message carries `openbook_version`.

## 3. Identifiers

### 3.1 Shared ids (the vocabularies)

Sports, market types, segments and sides use ids owned by the standard. One
id, two equivalent spellings:

- **Short form, on the wire:** `sport:soccer`, `market:total`,
  `segment:soccer:1st-half`, `side:home`.
- **Formal form, in the spec:** `urn:openbook:sport:soccer`. Adding or
  removing the `urn:openbook:` prefix is the only difference.

Shared ids are lowercase, `:`-separated namespaces with `-` inside a segment.
Once published an id is never re-pointed or reused; it is deprecated.

### 3.2 Publisher-own ids (the entities)

Fixtures, leagues, participants (teams), players and venues carry the
**publisher's own id**, unique within that publisher. OpenBook does not mint
or own these. Cross-publisher identity comes from **standard facts** (§5) and
from the **shared entity id** (§3.3).

### 3.3 Shared entity id — Wikidata *(proposed, Q12 a)*

For leagues, participants, players, venues and territories, the **Wikidata
QID** (`Q9617`) is the shared cross-publisher entity id. It is **REQUIRED when
one exists and `null` when it does not**; the publisher's own id and the
standard facts are always present as the fallback. It is an identifier string
to pin, never a runtime dependency.

### 3.4 External ids

Any object MAY carry `external_ids`: a list of `{system, id}` pairs
(`sportradar`, `opta`, a provider's own key). Optional, never canonical.

## 4. The two tiers, and change

- **Reference tier** — durable, bounded objects (§6). Delivered as documents.
- **Live tier** — prices, scores, settlement, market status (§7).

**Everything is diff-able, reference tier included.**

- Every object and message carries **`sequence`** — a monotonic integer the
  publisher's server issues per feed — and **`updated_at`**.
- **Push** streams send changes only. **Pull** endpoints accept
  `since=<sequence>` and return only what changed after it. `since` is never a
  timestamp.
- A **snapshot** is the state as of a sequence; it exists for initial load and
  recovery and is a diff from zero, not a separate format.
- **Change granularity is field-level**, with **JSON Merge Patch (RFC 7386)**
  semantics: a change message carries the object's id plus only the fields that
  changed; a field absent is unchanged; a field `null` is removed.
- Consumers MUST merge diffs and MUST NOT assume a message re-sends unchanged
  state.

## 5. Standard facts (how consumers match across publishers)

Every `reference_fixture` MUST carry:

- publisher's own `id`
- `sport` — shared id + `name`
- `league` — own id + `name` + `territory`
- `start_time`
- `participants[]` — each with own id, `name`, `territory`, and `role`
  (`home` · `away` · an ordinal for n-participant events)
- `sequence`, `updated_at`

and MAY carry `location` (venue, city, territory), `external_ids`, `season`,
`stage`. Consumers match on sport + league (name, territory) + start_time +
participants (names, territories), and on shared entity ids when both sides
have them. Home/away, side order and handicap sign are **derived** by the
consumer from these facts; a publisher's presentation order is never a fact.

## 6. Reference objects

Each is a document with `openbook_version`, `id`, `sequence`, `updated_at`,
the fields below, and optional `wikidata` / `external_ids`. Exact types are in
the schemas.

- **`publisher`** — the feed's own record: `id`, `name`, `url`, `contact`,
  the `sources[]` it carries (`{id, name, kind: sportsbook|exchange|model}`).
  Analogous to GTFS `agency.txt`.
- **`reference_sport`** *(shared vocab)* — `id`, `name`, `abbreviation`,
  `active`. Disciplines hang beneath (`athletics:110m-hurdles`).
- **`reference_segment`** *(shared vocab)* — `id`, `sport`, `name`,
  `ordinal`, `family`. A first-class object, never encoded in a market id.
- **`reference_market_type`** *(shared vocab)* — `id`, `name`, `genre`,
  `shape`, `category`, `sides[]`, prop flags. The controlled market vocabulary
  is [`../vocabularies/market_types.md`](../vocabularies/market_types.md).
- **`reference_side`** *(shared vocab)* — `home`, `away`, `draw`, `over`,
  `under`, `yes`, `no`, `participant`.
- **`reference_region`** — `id` = the CLDR territory code, `name`,
  `names{lang}`, `parent`, plus crosswalks `ioc_code`, `fifa_code`,
  `wikidata`.
- **`reference_league`** — own `id`, `name`, `sport`, `territory`,
  `ruleset` (clock/score/segment model), `wikidata`.
- **`reference_participant`** — own `id`, `name`, `short_name`, `aliases[]`,
  `names{lang}`, `territory`, `type` (`team` · `individual`), `wikidata`.
  Home/away is not a participant property.
- **`reference_player`** — own `id`, `name`, `given_name`, `family_name`,
  `participant`, `position`, `wikidata`.
- **`reference_fixture`** — §5, plus `state`, `cutoff_time`, `parent`.

## 7. Live messages

Every live message carries `openbook_version`, `sequence`, `timestamp`,
`publisher`, and references reference ids. Semantics are JSON Merge Patch.

- **`fixture_change`** — `fixture` + only the changed fixture fields (a moved
  start time, a state flip, a lineup change).
- **`odds_change`** — `fixture`, then `markets[]`, each with `market_type`,
  `segment`, optional `line`, `status`, **`source`**, **`provenance`**
  (`official` · `licensed` · `observed`), and `outcomes[]` (`side`,
  `odds`, optional `line`, `active`). A priced selection is identified by
  `(source, fixture, market_type, segment, line, side)`.
- **`score_change`** — `fixture`, `state`, `clock`, `scores[]`.
- **`settlement`** — per market/outcome `result` (`win` · `lose` · `void` ·
  `half-win` · `half-lose`) with a `settlement_id`. A re-settle is a **new**
  id, never a mutation. `settlement_rollback` references a prior
  `settlement_id`.
- **`market_status`** *(proposed, Q15)* — CAP-shaped: `msg_type`
  (`alert` · `update` · `cancel`), the market key, `status` (`open` ·
  `suspended` · `closed` · `void`), optional `reason`, and `references[]` to
  the message(s) it amends or cancels.

## 8. Streams *(proposed, Q14)*

Stream (topic) names follow a fixed, versioned grammar modelled on the WMO
WIS2 topic hierarchy:

`openbook / <version> / <publisher-id> / <message-type> / <sport> [/ <league>]`

e.g. `openbook/v1/acme-books/odds_change/soccer/gb-premier-league`. Levels are
lowercase, dash-separated, no dots, unique per level. Consumers subscribe with
wildcards at any level. Transport (MQTT, AMQP, WebSocket, SSE) is not part of
the standard; the message is.

## 9. Extensions

A publisher MAY add fields under an `x_` prefix. Consumers MUST ignore unknown
`x_` fields. New sports, segments and market types are proposed to the shared
vocabularies, not invented per feed.

## 10. Conformance

- **Level R** — reference documents validate against the reference schemas
  and carry the standard facts of §5.
- **Level L** — live messages validate against the live schemas, carry
  `sequence`, reference only ids present in the reference tier, and honour
  Merge Patch semantics.

A validator and conformance suite ship separately.

## 11. Versioning

Semantic versioning per [`../VERSIONING.md`](../VERSIONING.md). Pre-1.0 the
wire may change between minor versions; the `-draft` suffix marks an unfrozen
version.
