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

- **Time** — RFC 3339 (ISO 8601 with an explicit offset), everywhere.
- **Currency** — ISO 4217. Each feed MUST declare **`baseCurrency`** once
  on the publisher record (and on a full snapshot of that record). Incremental
  messages do not repeat it. Money is `{amount}` in that currency. Odds are
  not money. Another currency is another subscription (Q44).
- **Language** — ISO 639-1.
- **Territory** — Unicode CLDR territory codes: ISO 3166-1 alpha-2 (`GB`),
  ISO 3166-2 for sub-national teams (`GB-ENG`, `US-PR`), CLDR extras (`XK`).
- **Odds and lines** — decimal **strings** on the wire, not JSON numbers.
  Decimal odds only (MUST be strictly greater than 1); American and
  fractional forms are presentation.
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
Once published in a frozen version, never re-pointed, removed, or
**reassigned**; only deprecated (Q35). Field names and list-values take the
same promise. Deprecation is `name` + `reason` + `replacement` + `sunset`;
removal from the live set only at MAJOR after the window (Q36).

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
  └ league                  publisher-own; competitionType: league · cup · tournament · series · exhibition
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

### 5.1 Delivery and recovery (Q33)

A publisher that claims Level L MUST honour all eight. These are protocol
guarantees, not JSON Schema.

1. **Retention horizon `R`.** `since=N` with `N ≥ R` MUST return a complete,
   ordered delta. `N < R` MUST respond HTTP **410** with RFC 9457 Problem
   Details pointing at the snapshot URL — not a 200 with a flag, and not a
   silent full snapshot (Q46).
2. **Snapshot is compaction; Merge Patch `null` is a tombstone.** Replaying
   snapshot + diffs MUST converge on the same document as a fresh snapshot.
3. **Ordering is per fixture.** `sequence` is per publisher, strictly
   increasing, unique. For one fixture, messages appear in increasing
   sequence. Cross-fixture display order is not guaranteed.
4. **Caught-up (push).** After snapshot + replay, the publisher MUST emit
   `action: snapshotComplete` on that stream, with `changes: {}`. Pull has
   no marker; the HTTP response *is* the batch (Q46).
5. **Bounded heartbeats (push).** The same stream carries `action:
   heartbeat` (`changes: {}`). The publisher record MUST declare
   `heartbeatMs` (maximum silence, milliseconds). Quiet longer than that, the
   consumer SHOULD treat the feed as down (Q46).
6. If intermediate ticks are dropped, that change MUST carry **`conflated:
   true`**. Sequence still increases (Q47).
7. **QoS 0 / 1 / 2** are the delivery vocabulary (at-most-once / at-least-once
   / exactly-once). MQTT is not required; other transports MUST name the
   equivalent.
8. **Dedup key** is `(publisher, sequence)`. Consumers MUST ignore duplicates.

### 5.2 Feed operations (Q41, Q48, Q49)

- Live documents SHOULD declare **`ttl`**: integer seconds, GBFS (Q48).
  Optional on the publisher record; required on the discovery document.
- A publisher SHOULD offer **one discovery URL** that returns
  `{ lastUpdated, ttl, feeds: [{ name, url }] }`
  ([`../schema/discovery.schema.json`](../schema/discovery.schema.json)).
  Snapshot, stream, and any publisher-hosted API docs are named feeds. The
  `publisher` object stays identity, not the catalog (Q49).
- A publisher MAY **co-serve** more than one OpenBook version at the same
  time (distinct URLs or topics per `openbookVersion`).

Two independent implementations (a producer and a consumer; not
[`../tools/validate.py`](../tools/validate.py)) are required to **freeze
1.0**, not to ship a 0.x minor.

## 5a. Status: three questions, three fields

- **Fixture status** — *is the event happening?* `eventStatus`: scheduled ·
  delayed · live · paused · suspended · postponed · ended · cancelled, with an
  optional `statusReason`. **`ended` happens once.**
- **Segment status** — *where is the match, and is this slice final?* Per
  segment on the score: pending · live · paused · **down** (+ `downAt`).
  **A segment goes down once. `down` is terminal** — there is no reopen and no
  second down; a validator MUST reject one.
- **Market status** — *can you bet it?* Per market per source: open ·
  suspended · closed · void, via `market/update`. Grading is not a market
  status; it is the `grade` object. **Taking a market off the board is
  `marketStatus`** (`suspended` · `closed` · `void`). Last odds MAY stay on
  the document. Dropping an outcome or price from the snapshot is Merge
  Patch **`null`** (tombstone). Never a sentinel price (`odds: "0"`).

Rules: `eventStatus: ended` ⇒ every segment `down`. A market whose segment is
`down` MUST be `closed` or `void`. A `grade` MAY only reference a `down`
segment.

**Corrections without settling twice** (Q31): a downed segment's
`status` and `downAt` never change. A publisher correcting a result sends
`score/update` with `correction: true` and a `statusReason` — an erratum, not a
second settlement. Grades built on the old values are `grade/delete`d and
re-issued with `supersedes`, pointing (`basedOn`) at the correction's sequence.

## 6. Standard facts (matching across publishers)

Every fixture MUST carry: own `id` · `sport` (shared id + name) · `league`
(own id + name + territory + `competitionType`) · `startDate` ·
`participants[]` (own id, name, territory, **`role`**: home · away · neutral, **and `order`**, always present) ·
`sequence` · `dateModified`; and MAY carry `season`, `stage`, `location`,
`surface`, `identifier`. Fixture `participants[]` MAY carry `seed`. Consumers match on sport + league (name, territory) +
start_time + participants (names, territories), and on Wikidata QIDs when both
sides have them. `role` and `order` are facts the publisher asserts; the sign of a handicap is
derived from them. A feed's presentation order is never a fact.

## 7. Objects

Each reference document carries `openbookVersion`, `id`, `sequence`,
`dateModified`; exact types in the schemas.

- **`publisher`** — who transmits, `baseCurrency` (ISO 4217, once per feed),
  and the `sources[]` the feed carries (`{id, name, sourceType: sportsbook |
  exchange | model}`). GTFS `agency.txt`. Another currency is another
  subscription (Q44). Level L MUST declare **`heartbeatMs`**. Optional
  **`ttl`** (seconds) MAY also sit here; the discovery document is where
  `ttl` is required (Q46, Q48). Optional `registeredName` (Q60) and
  `inLanguage` (ISO 639-1, Q68).
- **`sport`**, **`segment`**, **`marketType`**, **`side`** — shared
  vocabularies ([`../vocabularies/`](../vocabularies/)). A sport MAY carry a
  default `limit`. Sport, market type, and segment are **`name` only** (Q59).
- **`region`** — `id` = CLDR territory code; `name`, `names{lang}`, `superEvent`,
  crosswalks `iocCode`, `fifaCode`, `sameAs`.
- **`league`** — own id, `name`, `sport`, `territory`, `competitionType`,
  optional `organizer`, `ruleset`, `sameAs`, optional `limit`. Team-style
  names: optional `shortName`, `registeredName` (Q59). Optional `gender`
  (`men` · `women` · `mixed` · `open`) and `ageGroup` (Q72, Q73).
- **`season`** — own id, `league`, `name` (display), `startDate`, `endDate`
  (Q60 / Q9).
- **`stage`** — own id, `season`, `name`, `parent`, `stageType` (phase · group ·
  round · matchday · leg · seriesGame), `order`, optional `startDate` /
  `endDate`.
- **`participant`** — own id, `participantType` (team · individual), `sport`,
  `territory`, `sameAs`. Required `name` (popular/board). Optional `shortName`,
  `names` (ISO 639-1), `nameLatin` (ISO 9 / ISO 843), `alternateName[]`.
  **Teams** MAY add `location` + `nickname`, `registeredName`,
  `abbreviation`. **Individuals** MAY add `givenName` / `familyName` (vCard
  RFC 6350 / ITU X.520); no `abbreviation`. No league field. Fixture
  `participants[]` copies `name` plus `role` and `order`.
- **`player`** — roster membership: own id, `participant` (the person),
  `team` (the team participant), `position`, `number`. No name fields.
- **`fixture`** — §6 plus `eventStatus`, `cutoffDate`, `superEvent` (a live
  event's pregame parent), optional display `name`, `location` (nested
  schema.org Place: `addressLocality` + `territory`, optional IANA `timeZone`,
  optional WGS 84 `latitude` / `longitude`), optional `surface`.
- **`market`** — a fixture's market as priced by one source: `fixture`,
  `marketType`, `segment`, `line`, `source`, `provenance` (`official` ·
  `licensed` · `observed`), `status`, **`limit`** `{amount}` in the feed's
  `baseCurrency` (required on the market document / snapshot), `outcomes[]`
  (`side`, `odds`, `line`, `active`). Identity: `(source, fixture, marketType,
  segment, line)`. Price-only ticks (`odds/change`) do not repeat `limit`
  unless it changed. **Most specific wins** (Q45): market `limit` → league
  `limit` → sport `limit`. A priced market MUST resolve to a limit.
- **`score`** — `fixture`, `eventStatus` (+ `statusReason`), `segments[]`
  (each `segment`, `status`, `downAt`), `currentSegment`, `clock` (`elapsed` /
  `remaining` in integer seconds, `running`, broadcast `display`), and
  `scores[]` — **one line per participant × unit** (`goals`, `corners`,
  `sets`, `games`, `runs`, `hits`…) with `total` and `bySegment`. The sport /
  league declares its `primaryUnit`. `server` for racket sports.
- **`grade`** — the book's judgement for one market × one source, graded from
  a `down` segment: `gradeId`, `segment`, `marketType`, `line`, `basis` (the
  unit graded on — Pinnacle's *resultingUnit*, generalised), `basedOn` (the
  score sequence used), `outcomes[]` with `win` · `lose` · `void` · `half-win`
  · `half-lose`. Never edited: a correction is `grade/delete` + a new grade
  with `supersedes`.

## 8. Streams: fixture-first, then object / action

Every message is **one object and one action**; topic and payload say the same
thing. Topics are fixture-first so that *everything about one match* is a
single subscription.

```
fixture-scoped   openbook / v1 / <publisher-id> / <sport> / fixture / <fixture-id> / <object> / <action>
                 object ∈ fixture · odds · market · score · grade
entity           openbook / v1 / <publisher-id> / <sport> / <object> / <id> / <action>
                 object ∈ league · season · stage · participant · player
publisher        openbook / v1 / <publisher-id> / publisher / <action>
```

- **`<action>`** — the JSON enum token: `snapshot` · `create` · `update` ·
  `delete`, plus **`change` (odds only)**, plus control actions
  **`snapshotComplete`** and **`heartbeat`** (Q46). `snapshotComplete` is
  camelCase on both topic and payload.
- **`<sport>`** — the shared slug without prefix (`soccer`).
- Rules (after WMO WIS2): lowercase, `-` inside a level, no dots, unique per
  level; `+` matches one level, `#` the rest; `v1` bumps only on a breaking
  change to the grammar. Exception: `<action>` matches the JSON enum, so
  `snapshotComplete` is mixed-case.

```
openbook/v1/acme-feeds/soccer/fixture/EVT-88213/#                         everything about one match
openbook/v1/acme-feeds/soccer/fixture/EVT-88213/odds/change               one match's price moves
openbook/v1/acme-feeds/soccer/fixture/EVT-88213/fixture/snapshotComplete    snapshot + replay finished
openbook/v1/acme-feeds/soccer/fixture/+/odds/change                       all soccer price moves, one publisher
openbook/v1/+/soccer/fixture/+/score/update                               every soccer score update, every publisher
openbook/v1/acme-feeds/soccer/league/LG-17/update                         a league record changed
openbook/v1/acme-feeds/publisher/heartbeat                                    feed-wide heartbeat
```

The same grammar is described for tooling in
[`asyncapi.yaml`](asyncapi.yaml) (Q42). MQTT is not required.

### 8.1 The change envelope
One envelope for every message ([`../schema/change.schema.json`](../schema/change.schema.json)):
`openbookVersion`, `sequence`, `datePublished`, `publisher`, `object`, `action`,
`sport`, `id`, and `changes` — a Merge Patch against the object's document
schema. `odds/change` carries its `markets[]` diff in `changes`
([`odds_change.schema.json`](../schema/odds_change.schema.json)).
`snapshotComplete` and `heartbeat` carry `changes: {}`. If intermediate ticks
were dropped, that envelope MUST set **`conflated`: `true`** (Q47).
`market/update` MAY carry `msgType` (`alert` · `update` · `cancel`), `reason`
and `references[]` to prior sequences, after OASIS CAP 1.2. A void is a `market/update` to `void`; a corrected grade is `grade/delete` +
`grade/create` with `supersedes`.

## 9. Extensions
Publishers MAY add `x_`-prefixed fields for vendor-specific extras.
Publishers validate **strictly** against the schema (closed when you write).
Consumers MUST ignore unrecognized **fields**, whether `x_`-prefixed or added
in a later minor (Q37). Growable lists (`sport:*`, `market:*`, `segment:*`,
`side`, `scoreUnit`, `statusReason`) have a catch-all (`unknown` / `other`).
A conformant consumer MUST accept unrecognised **values** (carry them; MUST
NOT crash). Adding a market type is not a breaking change (Q34). Publishers
SHOULD use the catch-all rather than inventing an id; publisher-side
validation MAY warn. New sports, segments and market types are also proposed
to the shared vocabularies.

## 10. Conformance
- **Level R** — reference documents validate and carry the §6 facts.
- **Level L** — messages validate, carry `sequence`, reference only known ids,
  honour Merge Patch semantics, deliver `odds/change` by push, and honour
  §5.1.

The gate is this spec, the JSON Schemas, and the language-agnostic corpus
in [`../conformance/`](../conformance/) (Q40). Valid cases MUST be
accepted; invalid cases MUST be rejected. [`../tools/validate.py`](../tools/validate.py)
is one runner, not a language oracle.

## 11. Versioning
Semantic versioning per [`../VERSIONING.md`](../VERSIONING.md). `-draft`
marks an unfrozen version. Within a frozen major, compatibility is
**FULL-TRANSITIVE** (Q32): minors only add optional fields; the required set
does not shrink or grow. Freezing **1.0** requires two independent
implementations (Q41).
