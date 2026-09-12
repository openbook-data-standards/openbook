# OpenBook — the specification

The normative document defining the **OpenBook** standard.
Version `0.3.0-draft` · 2026-09-12

The JSON Schemas in [`../schema/`](../schema/) are the machine-normative field
definitions; where prose and schema disagree, the schema wins. Every rule here
traces to a decision in [`../docs/decisions.md`](../docs/decisions.md).
Keywords **MUST**, **SHOULD**, **MAY** are used per RFC 2119.

---

## 1. What OpenBook is

OpenBook is **one shared format any publisher emits sportsbook data in**, the
way any transit agency publishes GTFS. It applies whenever odds that originate
from a sportsbook are emitted externally — by the sportsbook itself or by a
feed that carries them.

- A **publisher** is whoever transmits an OpenBook feed.
- A **source** is whose odds a price is. Every price carries its source; one
  feed MAY carry many sources (as one GTFS feed carries many agencies).
- A **consumer** reads any number of OpenBook feeds with one importer.

OpenBook is independent of any sportsbook, data provider or software vendor.
It standardises the data contract only.

## 2. Conventions

- **Time** — ISO 8601 with an explicit offset, everywhere.
- **Currency** — ISO 4217. **Language** — ISO 639-1.
- **Territory** — Unicode CLDR territory codes: ISO 3166-1 alpha-2 (`GB`),
  ISO 3166-2 for sub-national teams (`GB-ENG`, `US-PR`), CLDR extras (`XK`).
- **Odds** — decimal is canonical; other formats are presentation only.
- **Text** — UTF-8; names keep their diacritics.
- **Field names** — full words, `snake_case`. Small shared vocabularies are
  `*_type` fields: `competition_type`, `participant_type`, `market_type`,
  `stage_type`.
- Every object and message carries `openbook_version`.

## 3. Identifiers

### 3.1 Shared ids — the vocabularies
Sports, segments, market types and sides use ids owned by the standard, in two
equivalent spellings: **short on the wire** (`sport:soccer`, `market:total`,
`segment:soccer:1st-half`, `side:home`) and **formal in the spec**
(`urn:openbook:sport:soccer`). Lowercase, `:`-separated, `-` inside a segment.
Once published, never re-pointed; only deprecated.

### 3.2 Publisher-own ids — the entities
Leagues, seasons, stages, fixtures, participants, players and venues carry the
**publisher's own id**, unique within that publisher. OpenBook mints none.

### 3.3 Shared entity id — Wikidata
For leagues, participants, players, venues and territories the **Wikidata QID**
is the shared cross-publisher entity id: **REQUIRED when one exists, `null`
when it does not**. A string to pin, never a runtime dependency.

### 3.4 External ids
Any object MAY carry `external_ids`: `{system, id}` pairs. Optional, never
canonical.

## 4. The hierarchy

```
sport                       shared vocabulary
  └ league                  publisher-own; competition_type: league · cup · tournament · series · exhibition
      └ season              publisher-own; one edition (2025-26, F1 2026)
          └ stage           publisher-own; a named slice of a season (model open — decisions Q20)
              └ fixture     publisher-own; the priced event
                  └ segment shared vocabulary; a slice INSIDE a match (1st half, set 3, Q1)
participant / player        publisher-own; belong to a SPORT, linked to leagues only through fixtures
```

- A **league** is any recurring competition — the Premier League, the FA Cup,
  the NBA Cup, the F1 World Championship — typed by `competition_type`. It MAY
  name an `organizer` (the NBA, UEFA, the FIA): one organizer runs several
  competitions.
- A **participant** belongs to a sport, never to a league: the same team plays
  the league, the cup and the continental competition in one week.
- In Formula 1, Qualifying, Sprint and Race are three **fixtures** in one
  round; their sessions (Q1/Q2/Q3) are **segments**.

## 5. Change: everything is diff-able

- Every object and message carries **`sequence`** — a monotonic integer the
  publisher's server issues per feed — and **`updated_at`**.
- **Push** streams (§8) send changes only. **Pull** endpoints accept
  `since=<sequence>` and return only what changed after it. `since` is never a
  timestamp.
- A **snapshot** is the state as of a sequence, for initial load and recovery;
  a diff from zero, not a separate format.
- **Field-level granularity, JSON Merge Patch (RFC 7386) semantics**: a change
  carries the object id plus only the fields that changed; absent = unchanged;
  `null` = removed. Consumers MUST merge and MUST NOT assume a message re-sends
  unchanged state.
- **Odds are push-first.** Publishers SHOULD deliver `odds/change` by push and
  MAY additionally offer a `since=` pull. `market/snapshot` gives a fixture's
  current prices for initial load and recovery.

## 6. Standard facts (matching across publishers)

Every fixture MUST carry: own `id` · `sport` (shared id + name) · `league`
(own id + name + territory + `competition_type`) · `start_time` ·
`participants[]` (own id, name, territory, `role`: home · away · ordinal) ·
`sequence` · `updated_at`; and MAY carry `season`, `stage`, `location`,
`external_ids`. Consumers match on sport + league (name, territory) +
start_time + participants (names, territories), and on Wikidata QIDs when both
sides have them. Home/away, side order and the sign of a handicap are
**derived** from these facts; a publisher's presentation order is never a fact.

## 7. Objects

Each reference document carries `openbook_version`, `id`, `sequence`,
`updated_at`; exact types in the schemas.

- **`publisher`** — who transmits, and the `sources[]` the feed carries
  (`{id, name, kind: sportsbook | exchange | model}`). GTFS `agency.txt`.
- **`sport`**, **`segment`**, **`market_type`**, **`side`** — shared
  vocabularies ([`../vocabularies/`](../vocabularies/)).
- **`region`** — `id` = CLDR territory code; `name`, `names{lang}`, `parent`,
  crosswalks `ioc_code`, `fifa_code`, `wikidata`.
- **`league`** — own id, `name`, `sport`, `territory`, `competition_type`,
  optional `organizer`, `ruleset`, `wikidata`.
- **`season`** — own id, `league`, `name`, `start_date`, `end_date`.
- **`stage`** — own id, `season`, `name`, `parent`, `stage_type` *(open, Q20)*.
- **`participant`** — own id, `name`, `short_name`, `aliases[]`,
  `names{lang}`, `territory`, `participant_type` (team · individual), `sport`,
  `wikidata`. No league field.
- **`player`** — own id, `name`, `given_name`, `family_name`, `participant`,
  `sport`, `position`, `wikidata`.
- **`fixture`** — §6 plus `state`, `cutoff_time`, `parent`.
- **`market`** — a fixture's market as priced by one source: `fixture`,
  `market_type`, `segment`, `line`, `source`, `provenance` (`official` ·
  `licensed` · `observed`), `status`, `outcomes[]` (`side`, `odds`, `line`,
  `active`). Identity: `(source, fixture, market_type, segment, line)`.
- **`score`** — `fixture`, `state`, `clock`, `scores[]`.
- **`settlement`** — per market/outcome `result` (`win` · `lose` · `void` ·
  `half-win` · `half-lose`) with a `settlement_id`; a re-settle is a new id.

## 8. Streams: object / action

Every message is **one object and one action**; topic and payload say the same
thing.

`openbook / v1 / <publisher-id> / <object> / <action> / <sport> / <id>`

- **`<object>`** — `fixture` · `odds` · `market` · `score` · `settlement` ·
  `league` · `season` · `stage` · `participant` · `player` · `publisher`.
- **`<action>`** — `snapshot` · `create` · `update` · `delete`, plus
  **`change`, used only by `odds`**: a price move is an event, not a document
  edit.
- **`<sport>`** — the shared slug without prefix (`soccer`).
- **`<id>`** — for fixture-scoped objects (`fixture`, `odds`, `market`,
  `score`, `settlement`) the **fixture id**; otherwise the object's own id;
  omitted for `publisher`.
- Rules (after WMO WIS2): lowercase, `-` inside a level, no dots, unique per
  level; `+` matches one level, `#` the rest; `v1` bumps only on a breaking
  change to the grammar.

```
openbook/v1/acme-feeds/odds/change/soccer/EVT-88213      one match's price moves
openbook/v1/acme-feeds/odds/change/soccer/+              all soccer price moves, one publisher
openbook/v1/+/fixture/update/soccer/#                    every fixture change, every publisher
openbook/v1/acme-feeds/market/update/soccer/EVT-88213    suspensions / re-opens on one match
openbook/v1/acme-feeds/league/update/soccer/LG-17        a league record changed
```

### 8.1 The change envelope
One envelope for every message ([`../schema/change.schema.json`](../schema/change.schema.json)):
`openbook_version`, `sequence`, `timestamp`, `publisher`, `object`, `action`,
`sport`, `id`, and `changes` — a Merge Patch against the object's document
schema. `odds/change` carries its `markets[]` diff in `changes`
([`odds_change.schema.json`](../schema/odds_change.schema.json)).
`market/update` MAY carry `msg_type` (`alert` · `update` · `cancel`), `reason`
and `references[]` to prior sequences, after OASIS CAP 1.2. A void or a
re-settle is `settlement/delete` + `settlement/create`.

## 9. Extensions
Publishers MAY add `x_`-prefixed fields; consumers MUST ignore unknown ones.
New sports, segments and market types are proposed to the shared vocabularies.

## 10. Conformance
- **Level R** — reference documents validate and carry the §6 facts.
- **Level L** — messages validate, carry `sequence`, reference only known ids,
  honour Merge Patch semantics, and deliver `odds/change` by push.

## 11. Versioning
Semantic versioning per [`../VERSIONING.md`](../VERSIONING.md). `-draft`
marks an unfrozen version.
