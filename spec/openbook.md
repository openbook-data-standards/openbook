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
- **Field names** — camelCase, and **schema.org's name wherever schema.org has
  the property**: `startDate`, `dateModified`, `datePublished`, `alternateName`,
  `sameAs`, `identifier`, `superEvent`, `organizer`, `location`. Small shared
  vocabularies are `*Type` fields: `competitionType`, `participantType`,
  `marketType`, `stageType`, `sourceType`. Documents MAY carry JSON-LD
  `@context` / `@type`, so an OpenBook document is also valid schema.org data.
- Every object and message carries `openbookVersion`.

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

### 3.3 Shared entity id — `sameAs` (Wikidata)
For leagues, participants, venues and territories, **`sameAs`** holds the
Wikidata entity URL (`https://www.wikidata.org/entity/Q9617`) — the shared
cross-publisher entity id: **REQUIRED when one exists, `null` when it does
not**. A string to pin, never a runtime dependency.

### 3.4 External ids — `identifier`
Any object MAY carry `identifier`: a list of schema.org `PropertyValue`
(`{propertyID, value}`). Optional, never canonical.

## 4. The hierarchy

```
sport                       shared vocabulary
  └ league                  publisher-own; competition_type: league · cup · tournament · series · exhibition
      └ season              publisher-own; one edition (2025-26, F1 2026)
          └ stage           publisher-own; a named slice of a season; RECURSIVE (parent) with stageType
              └ fixture     publisher-own; the priced event
                  └ segment shared vocabulary; a slice INSIDE a match (1st half, set 3, Q1)
participant                 publisher-own; a TEAM or an INDIVIDUAL; belongs to a SPORT, linked to leagues only through fixtures
player                      publisher-own; roster membership of a person in a team (lineups, player props)
```

- A **league** is any recurring competition — the Premier League, the FA Cup,
  the NBA Cup, the F1 World Championship — typed by `competitionType`. It MAY
  name an `organizer` (the NBA, UEFA, the FIA): one organizer runs several
  competitions.
- A **participant** is a team *or* an individual (`participantType`); a tennis
  player, an F1 driver, a golfer is a participant. It belongs to a sport, never
  to a league: the same team plays the league, the cup and the continental
  competition in one week. `player` exists only as roster membership.
- A **stage** is recursive: Champions League → *Knockout* (phase) →
  *Quarter-final* (round) → *Leg 2* (leg); NBA → *Playoffs* (phase) →
  *Conference Semifinals* (round) → *Game 3* (seriesGame). A fixture names its
  **leaf** stage; the chain is walked via `parent`.
- In Formula 1, Qualifying, Sprint and Race are three **fixtures** in one
  round; their sessions (Q1/Q2/Q3) are **segments**.

## 5. Change: everything is diff-able

- Every object and message carries **`sequence`** — a monotonic integer the
  publisher's server issues per feed — and **`dateModified`**.
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
(own id + name + territory + `competitionType`) · `startDate` ·
`participants[]` (own id, name, territory, **`role`**: home · away · neutral, **and `order`**, always present) ·
`sequence` · `dateModified`; and MAY carry `season`, `stage`, `location`,
`identifier`. Consumers match on sport + league (name, territory) +
start_time + participants (names, territories), and on Wikidata QIDs when both
sides have them. `role` and `order` are facts the publisher asserts; the sign of a handicap is
derived from them. A feed's presentation order is never a fact.

## 7. Objects

Each reference document carries `openbookVersion`, `id`, `sequence`,
`dateModified`; exact types in the schemas.

- **`publisher`** — who transmits, and the `sources[]` the feed carries
  (`{id, name, kind: sportsbook | exchange | model}`). GTFS `agency.txt`.
- **`sport`**, **`segment`**, **`marketType`**, **`side`** — shared
  vocabularies ([`../vocabularies/`](../vocabularies/)).
- **`region`** — `id` = CLDR territory code; `name`, `names{lang}`, `superEvent`,
  crosswalks `iocCode`, `fifaCode`, `sameAs`.
- **`league`** — own id, `name`, `sport`, `territory`, `competitionType`,
  optional `organizer`, `ruleset`, `sameAs`.
- **`season`** — own id, `league`, `name`, `start_date`, `end_date`.
- **`stage`** — own id, `season`, `name`, `parent`, `stageType` (phase · group ·
  round · matchday · leg · seriesGame), `order`.
- **`participant`** — own id, `participantType` (team · individual), `sport`,
  `territory`, `sameAs`, and the **name model**: `name` (full), `shortName`
  ("Man City", "C. Alcaraz"), `abbreviation` ("MCI"), `alternateName[]`,
  `localName` (native script), `names{lang}`; for individuals the vCard /
  X.520 parts `familyName`, `givenName`, `additionalName`, `honorificPrefix`,
  `honorificSuffix` (after ODF's Print / TV / Local name forms). No league field.
- **`player`** — roster membership: own id, `participant` (the person),
  `team` (the team participant), `position`, `number`.
- **`fixture`** — §6 plus `eventStatus`, `cutoffDate`, `superEvent` (a live
  event's pregame parent), `location` (a schema.org Place).
- **`market`** — a fixture's market as priced by one source: `fixture`,
  `marketType`, `segment`, `line`, `source`, `provenance` (`official` ·
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
`openbookVersion`, `sequence`, `timestamp`, `publisher`, `object`, `action`,
`sport`, `id`, and `changes` — a Merge Patch against the object's document
schema. `odds/change` carries its `markets[]` diff in `changes`
([`odds_change.schema.json`](../schema/odds_change.schema.json)).
`market/update` MAY carry `msgType` (`alert` · `update` · `cancel`), `reason`
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
