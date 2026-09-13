# OpenBook — design decisions

A running log of the decisions that shape the standard, in the order they were
taken, each with the options that were on the table and why one won. The
specification in [`../spec/openbook.md`](../spec/openbook.md) is revised to
match; where the two disagree, the newer decision here wins until the spec
catches up (tracked in [`../CHANGELOG.md`](../CHANGELOG.md)).

Status key: **decided** · **proposed** (awaiting confirmation) · **open**.

---

## Q1 — What OpenBook is for — decided

**One shared publication format any publisher emits odds in**, the way any
transit agency publishes GTFS.

- A **publisher** is whoever transmits: a sportsbook publishing its own odds,
  or a feed that carries sportsbooks' odds.
- Every price is tagged with its **source** (whose odds these are), which is
  separate from the publisher. One OpenBook feed can legitimately carry many
  sources — exactly as one GTFS feed carries many agencies via `agency_id`.
- Rejected: a provider→book distribution format (that is Sportradar's turf and
  needs vendor cooperation); an internal canonical model only (a schema, not a
  feed anyone publishes).

## Q2 — How consumers know two publishers mean the same match — decided (c)

Publishers use **their own ids**, but every fixture **must carry standard
facts** — sport, start time, participant names + country, league, period —
so consumers match across publishers deterministically.

- a) own ids, consumers match alone — rejected: makes comparison everyone's
  private problem (today's world).
- b) one central registry everyone must map to — rejected: someone has to run
  it; a central point of control and cost.
- **c) own ids + mandatory standard facts** — chosen. Faithful to GTFS (which
  standardises small enums, not entity ids) while fixing the one place betting
  differs from transit: everyone prices the *same* fixture.

## Q3 — Provenance on every price — decided (a)

Every price says how the publisher obtained it:
`official` (the book emitted it) · `licensed` (via a data agreement) ·
`observed` (captured from the book's public surface). Same number, very
different reliability and latency; consumers need to know.

## Q4 — Which ids are shared, which are publisher-own — decided (a)

- **Shared** (one list everyone uses, small and stable): sports, market types,
  periods/segments, sides.
- **Publisher-own** (large, changing): fixtures, leagues, teams, players.
- Industry check: the shared concepts are already agreed industry-wide *by
  name* (main lines, halves/quarters/innings, home/away/draw/over/under); only
  the ids differ. OpenBook supplies stable ids and publishes crosswalks.

## Q5 — What a shared id looks like — decided (both)

One id, two spellings, mechanically equivalent:

- **Short form on the wire:** `sport:soccer`, `market:total`,
  `segment:soccer:1st-half` — what every real feed does (Sportradar
  `sr:match:123`, GTFS plain ids).
- **Formal form in the spec:** `urn:openbook:sport:soccer` — globally unique,
  self-identifying in mixed documents, and registrable with IANA (a real path if
  this ever goes to a standards body).
- Rejected: numeric codes with a lookup table (Sportradar's way; unreadable).

## Q6 — External cross-reference ids — decided (a)

A publisher may attach any number of other systems' ids to an object
(Sportradar URN, Opta id, Wikidata QID, its own internal id). Optional, never
required, never the canonical key.

## Q7 — Standard facts every fixture carries — decided

**Required:** publisher's own fixture id · sport (shared id + name) · league
(own id + name + ISO country) · start time (ISO 8601) · participants (own id,
canonical name, ISO country, role: home / away / ordinal) · `sequence` ·
`dateModified`.
**Optional:** location (venue, city, country) · external ids · season / stage.

## Q8 — How changes are sent — decided (c, generalised) + granularity (e)

**Everything is diff-able, reference tier included.**

- Push streams send changes only: `fixture_change`, `odds_change`,
  `score_change`, `settlement`.
- Pull APIs accept `since=<sequence>` and return only what changed after it.
- A **snapshot** exists for initial load and recovery only — it is a diff from
  zero, not a separate format. (Betfair / Sportradar shape. GTFS-Realtime
  re-sends everything every poll; OpenBook improves on that.)
- **Granularity: field-level.** A change carries the object id plus only the
  fields that changed, with **JSON Merge Patch semantics (RFC 7386)**: field
  absent = unchanged, field `null` = removed. Odds diffs work at outcome level
  under the same rule.
- Rejected: snapshots only (heavy, latency = poll interval); object-level
  re-sends (cannot tell *what* changed).

## `since` — decided

`since` is a **monotonic sequence number the server issues**, never a time.
Time-based cursors break on clock skew, same-millisecond ties and late commits;
Pinnacle's `since` is an opaque server value for exactly this reason.
Timestamps stay on objects for humans and analytics; the cursor is for
correctness.

## Q9 — Timestamps — decided (a)

**ISO 8601 with explicit offset, everywhere** — reference tier and live tier
alike. Readability wins over the bytes saved by epoch integers. (Considered:
epoch ms on the live wire as GTFS-Realtime and Sportradar do; both fields as
KIBL does. Rejected for consistency.)

---

## Q10 — Countries and sub-national teams — decided (CLDR)

**Unicode CLDR territories** are the territory model: ISO 3166-1 alpha-2
codes underneath (`GB`, `US`), ISO 3166-2 subdivisions for sub-national teams
(`GB-ENG`, `GB-SCT`, `GB-WLS`, `GB-NIR`, `US-PR`), plus CLDR's pragmatic
extras (`XK` Kosovo, `EU`, `UN`) — and CLDR's **localized names in every
language**, which is what every OS and browser already uses to spell country
names. `iocCode`, `fifaCode` and `sameAs` (Wikidata) ride on the region record as
crosswalks, so a football consumer reads `ENG` and an Olympic consumer reads
`GBR` without OpenBook adopting either.

- a) ISO 3166-1 only — rejected: cannot represent England, Puerto Rico,
  Chinese Taipei.
- b) FIFA codes — rejected: football-only spellings (GER/NED/SUI diverge from
  ISO; BHR/SLV/MUS diverge from the IOC); no code for what FIFA does not
  recognise.
- c) IOC codes — rejected: multi-sport but still a sport body's list, and no
  England.
- d) UN M49 — rejected: numeric, unreadable, no sub-national teams.
- **e) CLDR** — chosen: ISO codes + the extras everyone actually needs +
  maintained localized names, for free.

## Q11 — Names — decided (v0.3)

There is **no ISO standard for team or person names.** The real standards
nearby: **vCard (RFC 6350 / ITU X.520)** for a person's name structure
(family · given · additional · prefix · suffix — also schema.org's
`familyName` etc.); the **Olympic Data Feed**, which gives every athlete
several display forms (`PrintName`, `TVName`, `TVInitialName`,
`LocalFamilyName`…); and **finance**, which standardises *identity* (ISIN,
LEI) and treats the name as a mutable attribute — our `sameAs` stance.
Wire names are camelCase (Q13 / Q38). Shape:

- `name` — canonical display name, UTF-8, diacritics allowed.
- `shortName`, `abbreviation` — optional.
- `alternateName[]` — other spellings a book might use (schema.org).
- `names` — optional per-language variants keyed by ISO 639-1 (`en`, `es`).
- `localName` — optional name in the native script (ODF LocalName).
- Persons: optional `givenName` / `familyName` / `additionalName` /
  `honorificPrefix` / `honorificSuffix` (schema.org `Person` / vCard N).

## Q12 — Shared entity id — decided (Wikidata QID)

**Wikidata QIDs** (`Q9617` = Arsenal F.C.) are the most widely used free,
neutral identifiers for teams, players, leagues and venues, resolvable at
`https://www.wikidata.org/entity/Q…`. **Decided:** the QID is the shared
cross-publisher entity id for leagues, participants, players, venues and
territories — **required when one exists, `null` when it does not** — with the
publisher's own id and the standard facts always present as the fallback. An
identifier string to pin, never a runtime dependency. Fixtures are not in
Wikidata and stay publisher-own + standard facts. (OpenStreetMap's
`wikidata=Q…` tags are the precedent.)

## Q13 — Field-name alignment with schema.org — decided (d: full alignment)

schema.org `SportsEvent` / `SportsTeam` / `Person` is the vocabulary Google's
structured data uses (`homeTeam`, `awayTeam`, `competitor`, `startDate`,
`location`, `alternateName`). Proposal: align OpenBook field names with it
where there is no reason not to, so OpenBook data maps onto the web's existing
sports vocabulary for free.

## Q14 — Stream grammar — decided (object / action, keyed by fixture)

`openbook / v1 / <publisher-id> / <object> / <action> / <sport> / <id>`

- `<object>`: fixture · odds · market · score · settlement · league · season ·
  stage · participant · player · publisher.
- `<action>`: snapshot · create · update · delete, plus `change` for odds only.
- `<id>`: the **fixture id** for fixture-scoped objects (odds, market, score,
  settlement, fixture); the object's own id otherwise. Fixture ids are
  publisher-own — fine, because a subscription is always to one publisher's
  stream; cross-publisher identity comes from the standard facts.
- WIS2 rules: lowercase, dashes, no dots, unique per level; `+` and `#`.
- Rejected: a league level keyed by Wikidata QID (Dan: key odds by fixture);
  a flat `fixture_change`-style message-type list (object/action is uniform,
  like OsmChange's create/modify/delete).

## Q15 — Suspensions, re-opens and voids — decided (market/update)

`market/update` carries CAP-style `msgType` (alert · update · cancel),
`reason`, and `references[]` to prior sequences. Voids and re-settles are
`settlement/delete` + `settlement/create` (a new settlement id, never a
mutation).

## Q16 — Name of the price stream — decided (c)

`odds/change` — Sportradar's word. `change` is the one action reserved for
odds: a price move is an event, not a document edit. (Considered:
`price/tick`, `market/update`.)

## Q17 — Delivery of odds — decided (b)

Push preferred: publishers SHOULD deliver `odds/change` by push and MAY offer a
`since=` pull. `market/snapshot` is the recovery / initial-load state.
(Considered: push-only with no pull at all.)

## Q18 — Topic tail — decided (a)

`…/<sport>/<fixture-id>` for fixture-scoped objects. `+` at the fixture level
= every fixture in that sport from that publisher. (Considered: a league level
before the fixture; keying by league QID.)

## Q19 — League vs competition — decided (b)

Keep **`league`** as the object name for any recurring competition, typed by
**`competitionType`** (league · cup · tournament · series · exhibition). An
optional `organizer` (the NBA, UEFA, the FIA) can be named, because one
organizer runs several competitions (NBA season, NBA Cup, All-Star Game).
(Considered: renaming the object to `competition`.)

## Q20 — Stages — decided (a: one recursive object)

`stage` is a named slice of a season with an optional `parent` stage and a
`stageType`: phase · group · round · matchday · leg · seriesGame. Stages nest
to any depth (Knockout → Quarter-final → Leg 2; Playoffs → Conference
Semifinals → Game 3; F1 season → Round 14). A fixture names its leaf stage.
(Rejected: separate `stage` + `round` objects.)

## Q21 — Participants belong to a sport — decided (a)

`participant.sport` is required and there is no league field; a team is linked
to leagues only through its fixtures (Arsenal plays the league, the cup and the
Champions League in one week).

## Naming convention — decided

Every small shared vocabulary is a `*Type` field: `competitionType`,
`participantType`, `marketType`, `stageType`. No `kind` / `format`
synonyms.

## Q22 — Teams and individuals are both participants; role and order — decided

One `participant` object with `participantType` team · individual. `player`
is roster membership only. On a fixture every participant carries **both**
`role` (home · away · neutral) **and** `order` (integer, always present) —
facts asserted by the publisher, never inferred from presentation.
schema.org `homeTeam` / `awayTeam` are derivable from `role`; `participants[]`
stays the source of truth because it can express a 20-car grid.

## Naming convention — revised (Q13 d)

camelCase everywhere; schema.org's property name wherever one exists
(`startDate`, `dateModified`, `datePublished`, `alternateName`, `sameAs`,
`identifier`, `superEvent`, `organizer`, `location`, `eventStatus`); small
shared vocabularies are `*Type` fields. Documents may carry JSON-LD
`@context` / `@type`.

## Q23 — Score model — decided (a: everything)

One `score` document per fixture (`score/update`): `eventStatus`, the current
`segment`, a `clock` (`elapsed` / `remaining` in **integer seconds** within the
current segment, `running`, and a broadcast `display` string), and `scores[]`
per participant with `total`, `bySegment` (segment id → score) and free
sport-specific `stats` counts. Racket sports add `server`.

- Considered: clock as a `"45:00"` string only (unparseable across sports);
  scores as a flat per-participant number only (loses per-segment grading).

## Q24 — Settlement model — superseded by Q27/Q28/Q30 (see below)

A `settlement` is the grade of one market for one source: `settlementId`,
`dateSettled`, `basis` (what it graded on), and `outcomes[]` with a
`settlementResult` (win · lose · void · half-win · half-lose). **Immutable**: a
re-settle is a new `settlementId` that names the one it `supersedes`
(Pinnacle's re-settle-as-new-id semantics); a void is a settlement whose
outcomes are `void`. Delivered as `settlement/create`; a rollback is
`settlement/delete`.

## Segments vocabulary — added

`vocabularies/segments.md`: named per-sport slices (`segment:soccer:1st-half`,
`segment:ice-hockey:regulation`, `segment:motorsport:q3`). Every sport has
`full-time`; `regulation` where overtime rules make the distinction matter.

## Q25 — Fixture status — decided (a)

A real feed's state table (Universal, Scheduled, Started, Halftime, Second
Half, Postponed, Suspended, Rain Delay, Delay, Cancelled, Final, Deleted,
Retired) mixes four things: lifecycle, progress within the match, reason, and
non-states. OpenBook splits them: `eventStatus` (scheduled · delayed · live ·
paused · suspended · postponed · ended · cancelled) + optional `statusReason`
(weather · crowd · injury · retirement · walkover · forfeit · technical ·
scheduling · correction · other). Halftime / Second Half are `segment` +
`clock`; Deleted is `fixture/delete`; Retired is `ended` + `retirement`.

## Q26 — Units on every score line — decided (a)

`scores[]` is one line per participant × `unit` (goals · points · runs · hits ·
errors · sets · games · frames · strokes · laps · position · time · corners ·
yellowCards · redCards · wickets · overs · rounds · knockdowns · aces · faults),
each with `total` and `bySegment`. The sport / league declares `primaryUnit`.
A corners market settles from the feed by half; tennis carries sets, games and
points at once. Generalises Pinnacle's `resultingUnit`.

## Q27 — Settlement vs grade — decided (two things)

Pinnacle separates the **result** (`/fixtures/settled`: per-period scores,
settlementId, status) from the **grade** (`/bets`: WON / LOSE / REFUNDED).
OpenBook does too — but the result is not a separate object (Q28).

## Q28 — "Down", once — decided (a)

A segment goes **down** as a state on the score (`segments[].status: down`,
`downAt`). No `settlement` object, no `settlementId`, no `resettled`.
**A fixture ends once and a segment goes down once**; `down` is terminal and a
validator rejects a second one. Grades reference the segment and the score
`sequence` they graded from (`basedOn`).

## Q29 — Topic order — decided (a: fixture-first)

`openbook/v1/<publisher>/<sport>/fixture/<fixture-id>/<object>/<action>`, so
everything about one match is one `#` subscription. Entities:
`…/<sport>/<object>/<id>/<action>`; publisher: `…/publisher/<action>`.
(Supersedes the object-first order in Q14/Q18.)

## Q30 — Three statuses — decided

Fixture status (`eventStatus`), segment status (`segmentStatus`: pending ·
live · paused · down) and market status (`marketStatus`: open · suspended ·
closed · void) are three fields answering three questions. Graded is not a
market status; it is the `grade` object.

## Q31 — Corrections without settling twice — decided (a: erratum)

A downed segment's `status` / `downAt` are frozen. A correction is
`score/update` with `correction: true` + `statusReason` (an erratum), and
affected grades are `grade/delete` + new `grade/create` with `supersedes`.
(Rejected: reopen → down again; absolutely immutable with no corrections.)

## Q32 — Schema compatibility within a major — decided (FULL-TRANSITIVE)

Once a major is **frozen** (1.0+), every minor of that major is readable by a
consumer built against any other minor of that major, **both directions**,
checked against **all** prior minors of that major — Confluent
FULL + TRANSITIVE, adapted to JSON Schema as *instance* compatibility (JSON
Schema has no Avro reader/writer resolution).

- New fields MUST be optional or defaulted.
- No field is re-typed or removed within a major.
- The required set is permanent within a major (keep it small).
- Adding a required field is a MAJOR.

Rejected: BACKWARD only; FORWARD only; SemVer prose with no compatibility
rule.

**Consequences:** a CI schema-diff gate is a later Phase-B item, not this
change. `additionalProperties: false` on publisher schemas stays until the
strict-write / open-read question. Pre-1.0 `-draft` may still break.

**Supersedes:** none of Q1–Q31; tightens [`../VERSIONING.md`](../VERSIONING.md).

## Q33 — Delivery and recovery — decided (all eight MUST)

Level L is a contract, not a sketch. A conformant live publisher MUST:

1. Advertise a retention horizon `R`; `since ≥ R` is complete and ordered;
   `since < R` is not a silent hole (send the client to a snapshot).
2. Treat snapshot as compaction and Merge Patch `null` as a tombstone;
   snapshot + diffs MUST converge.
3. Keep `sequence` unique and increasing per publisher; guarantee order
   **per fixture**.
4. Emit a caught-up marker after snapshot + replay.
5. Bound heartbeats (quiet ≠ dead).
6. Flag conflation when ticks are dropped.
7. Use QoS 0/1/2 as vocabulary (MQTT not required).
8. Dedup on `(publisher, sequence)`.

Rejected: a thinner MUST set; leaving the wire as a sketch.

**Consequences:** names of the caught-up message, heartbeat interval field,
and how pull returns “too old” are later items. This change is spec prose.

**Supersedes:** Q8/Q17 on snapshot-for-recovery by making completeness
normative.

## Q34 — Unknown values — decided (catch-all + must-tolerate)

Growable lists get an `unknown` / `other` bucket, **and** a conformant
consumer MUST accept unrecognised values (carry through; MUST NOT crash).
Adding a bet type is never a breaking change.

- Vocab: `sport:unknown`, `market:unknown`, `segment:unknown:unknown`.
- Schema enums: `side` and `scoreUnit` include `other` (`statusReason` already
  had `other`).
- Publisher validation MAY still warn on unregistered ids.

Rejected: catch-all but reject surprise values; no catch-all; closed lists
as breaking.

**Supersedes:** nothing; refines Q4 vocabularies and §9.

## Q35 — Stability — decided (permanent; never reuse)

Once shipped in a **frozen** version, an id, list-value, or field name is never
removed, moved, re-typed, or **reassigned**. Fixes are new aliases. Retired
names live in [`../vocabularies/deprecated.md`](../vocabularies/deprecated.md)
(empty until something is retired). “Never reuse” survives MAJOR: the string
is not given a new meaning. Removal of a name from the *live* set is a later
deprecation-window question.

Cautionary: ISO 3166 `CS` reuse. Model: Unicode stability.

Rejected: ids-only; reuse allowed at MAJOR; leave CONTRIBUTING as ids-only.

**Consequences:** pre-1.0 `-draft` is not this promise yet (`VERSIONING.md`).

**Supersedes:** CONTRIBUTING “ids are stable” by extending it to field names
and list-values.

## Q36 — Deprecation — decided (marker + window; remove only at MAJOR)

A deprecation is machine-readable: `name`, `reason`, `replacement`, `sunset`
(date). It applies to fields, list-values, and message types. A window is
REQUIRED; removal from the live set only at MAJOR, and only after sunset.
The string still MUST NOT be reused (Q35).

The registry is [`../vocabularies/deprecated.json`](../vocabularies/deprecated.json);
the shape is `common.schema.json#/$defs/deprecation`.

Rejected: CHANGELOG-only; no window; never remove even at MAJOR.

**Supersedes:** the “removal is a later question” line in Q35.

## Q37 — Strict when you write, open when you read — decided

Publishers validate **strictly** against the schema (catch typos). Consumers
MUST ignore unrecognized **fields**, whether `x_`-prefixed or added in a
later minor. `x_` remains reserved for vendor-specific extras.

Rejected: closed-when-you-read (MINORs break old validators); open-when-you-write
(typos become data).

**Consequences:** shipped schemas keep `additionalProperties: false` +
`patternProperties: ^x_` as the **publisher** contract. A consumer that
validates incoming documents MUST ignore unknown properties (or use a
consumer-view schema). That split is the JSON Schema form of Protobuf “skip
unknown.”

**Supersedes:** §9 / VERSIONING “ignore unknown `x_`-prefixed fields” by
widening ignore to all unrecognized fields.

## Q38 — Naming is camelCase; remaining snake_case is drift — decided

Canonical field names are camelCase, schema.org where a property exists
(Q13). Snake_case in prose is drift. A CI check that flags names in docs
that are not on a schema is a later item (Q50).

This change (and Q11) matches the schemas (`openbookVersion`,
`datePublished`, `startDate`, `marketType`, `competitionType`,
`shortName`, `msgType`). Older log entries that quote a superseded
message name (`odds_change`, `settlement`) stay as history.

Rejected: leave mixed spellings; CI in this same patch.

**Supersedes:** none of Q13; implements it.

## Q39 — Odds, lines and money are decimal strings — decided

Odds and lines are decimal **strings** on the wire, not JSON numbers.
Money, when it appears, is `{amount, currency}` (`amount` a decimal string,
`currency` ISO 4217). Decimal odds are the only wire form (MUST be strictly
greater than 1); American and fractional are display. Times stay RFC 3339 /
ISO 8601 with an explicit offset (Q9).

Rejected: JSON numbers for odds/lines; deferring the money shape; strings for
odds only.

**Supersedes:** spec §2 “decimal is canonical” by fixing the JSON type.

## Q40 — Spec, schema, validator, language-agnostic corpus — decided

The conformance gate is the spec, the JSON Schemas, and a
**language-agnostic corpus** ([`../conformance/`](../conformance/)).
[`../tools/validate.py`](../tools/validate.py) is one runner. No language
is an oracle. Reference libraries MAY exist later (Apache-2.0); they are
not the spec.

Rejected: schema-only / self-certify; a blessed language library as the gate.

**Supersedes:** GOVERNANCE “reference tooling published later” by naming
the corpus now. The two-implementation 1.0 gate is a later question.

## Q41 — GBFS-style ops; two implementations at 1.0 only — decided

Three feed-ops principles, after GBFS: a cache lifetime (`ttl` in GBFS
terms), **one discovery URL** that lists a publisher's feeds, and publishers
MAY **co-serve** more than one OpenBook version. Field names and the
discovery document shape are later.

Two independent implementations — one **producer** and one **consumer**,
neither of which is the in-repo runner — are the **1.0 freeze** gate
only. They are not required per MINOR, and not during 0.x.

Rejected: no two-implementation rule at all; two impls per MINOR; defer
the ops principles until after 1.0.

**Supersedes:** the last sentence of Q40.

## Q42 — AsyncAPI describes the streams; CloudEvents and DNS ids deferred — decided

The push streams are described in AsyncAPI 3
([`../spec/asyncapi.yaml`](../spec/asyncapi.yaml)) against the existing
fixture-first topics and the change envelope. MQTT is still not required.

**Deferred:** wrapping messages as CloudEvents; a DNS-style id namespace
(would reopen Q4).

Rejected: deferring AsyncAPI as well; shipping CloudEvents in this change.

**Supersedes:** building-blocks “CloudEvents under consideration” — now
explicitly deferred.

## Q43 — Off the board is marketStatus; tombstone is null; never odds 0 — decided

Taking a market off the board is **`marketStatus`** (`suspended` · `closed`
· `void`). Last odds MAY remain. Removing an outcome or `odds` field from
the document is Merge Patch **`null`** (Q33 tombstone). `odds: "0"` is
not a takedown; it is an illegal price (Q39).

Rejected: requiring odds to be nulled whenever status is not `open`;
`"0"` as a takedown synonym.

**Supersedes:** none of Q33; names how takedown vs tombstone share the
wire.

## Q44 — Feed has baseCurrency once; money is amount; odds are not money — decided

Each feed **MUST** declare `baseCurrency` (ISO 4217) on the publisher
record. A full snapshot of that record carries it; incremental messages
do not. Money is `{amount}` in that currency (same pattern as a last-sale
tape: currency is the listing, not the tick). Decimal odds are not money
and never carry currency. Another currency is a **different subscription**.

Rejected: `{amount, currency}` on every money object; inherit-if-omitted
on the hot path.

**Supersedes:** Q39's `{amount, currency}` money shape. Odds-as-strings
stands.

## Q45 — Markets have a limit; most specific wins — decided

A priced market document **MUST** carry `limit` `{amount}` in the feed's
`baseCurrency`. Sport and league MAY carry a default `limit`. **Most
specific wins:** market → league → sport. `odds/change` does not repeat
`limit` unless it changed (same tape rule as Q44).

Rejected: required on every tick; no inheritance; optional everywhere.

**Supersedes:** none.

## Q46 — Caught-up, heartbeat, stale since — decided

Wire names for Q33 items 4, 5, and 1.

- **Caught-up (push MUST).** After snapshot + replay, emit `action: snapshotComplete`. Pull has **no** marker; the HTTP response is the batch.
- **Heartbeat (push).** Same stream: `action: heartbeat`. Interval on the publisher record as `heartbeatMs`.
- **Stale `since` (pull).** If `since < R`, HTTP **410** plus RFC 9457 Problem Details pointing at the snapshot URL. Not a 200 with a flag; not a silent full snapshot.

Rejected: infer caught-up like Betfair; CloudEvents-style control object; 200 + `sinceStatus`; transport-only ping; client TestRequest pair (FIX).

**Supersedes:** Q33 consequences (“names … are later items”).

## Q47 — Honest conflation — decided (`conflated`)

Q33 item 6. If intermediate ticks were dropped, the change that skipped them carries `conflated: true`. Sequence still increases.

Rejected: a separate `action: conflated`; infer from a `sequence` hole; publisher-level `conflationMs` only.

**Supersedes:** Q33 item 6 unnamed.

## Q48 — Cache lifetime field — decided (`ttl`)

Q41’s cache lifetime is `ttl`, integer seconds, GBFS.

Rejected: `maxAge`; HTTP `Cache-Control` only; `expiresAt` timestamp.

**Supersedes:** Q41 “field names … are later” for this field.

## Q49 — Discovery document — decided (GBFS-shaped)

Q41’s one discovery URL returns `{ lastUpdated, ttl, feeds: [{ name, url }] }`. Snapshot, stream, and any publisher-hosted API docs are named feeds. The `publisher` object stays identity, not the catalog.

Rejected: extend `publisher` with `feeds[]`; `.well-known/openbook` pointing only at OpenAPI/AsyncAPI; prose-only with no JSON shape.

**Supersedes:** Q41 “discovery document shape are later”.

## Q50 — Docs-vs-schema name CI — decided (one-way)

If spec/docs mention a field name, it MUST exist on a schema. CI fails the PR.
Extra schema fields are allowed. Scanned: `spec/openbook.md`, `spec/asyncapi.yaml`,
`docs/building-blocks.md`, `docs/still-to-do.md`. The decision log is history
and is not scanned. Implemented in [`../tools/validate.py`](../tools/validate.py).

Rejected: never (CONTRIBUTING only); bidirectional (every schema field named in the spec); CI on this patch.

**Supersedes:** Q38 “a CI check … is a later item” by naming the rule.

## Q51 — Consumer-view schema — decided (none)

Q37 stands. One publisher schema stays `additionalProperties: false`. “Ignore unknown” is spec/conformance text. No `*-consumer.schema.json`.

Rejected: a second consumer schema; `additionalProperties: true` for everyone; two `$id`s on one file.

**Supersedes:** Q37 “or use a consumer-view schema”.

## Q52 — CloudEvents wrap — decided (never)

OpenBook’s envelope is enough (`sequence`, `publisher`, `object`/`action`, `datePublished`). No CloudEvents wrap. Not deferred.

Rejected: wrap now; optional MAY wrap; keep deferred until 1.0.

**Supersedes:** Q42 “CloudEvents … deferred”.

## Q53 — DNS-style ids — decided (never)

Q4 and Q5 stand. Two spellings only: `sport:soccer` on the wire, `urn:openbook:sport:soccer` in the spec. No DNS-style third form.

Rejected: defer to 1.0; adopt DNS now; optional third spelling.

**Supersedes:** Q42 “DNS-style id namespace deferred”. Does not reopen Q4 or Q5.

## Q54 — Pull OpenAPI — decided (not in this repo)

No `openapi.yaml` in the spec repo. Spec keeps `since=` and **410**. A publisher who offers HTTP publishes **their own** OpenAPI; discovery lists those URLs.

Rejected: in-repo OpenAPI as the standard pull API; strike `since=`/410 from the spec; non-normative example as the spec.

**Supersedes:** building-blocks’ “OpenAPI 3.1 describes the pull side” as a file we ship. AsyncAPI for **push** (Q42) stands.

## Q55 — Schema-diff CI — decided (later PR, 1.0+ only)

A CI schema-diff gate (required field added, re-type, remove) is a **later PR**, and only for **frozen majors** (1.0+). 0.x-draft may still break (Q32).

Rejected: run it on 0.x now; never; this patch.

**Supersedes:** Q32 “a CI schema-diff gate is a later Phase-B item” by naming when.

## Q57 — v1 encoding is JSON; binary later — decided

The v1 encoding is **JSON**. JSON Schema 2020-12 is the model; AsyncAPI
describes the push as JSON. Protobuf (GTFS-Realtime), FIX Simple Binary
Encoding, and GRIB/BUFR are **later** optional bindings, generated from these
schemas — not a second hand-written model, and not shipped in this repo
before 1.0.

Rejected: protobuf as v1; SBE as v1; a parallel binary schema tree.

**Supersedes:** none of Q8/Q42; names the encoding the protocol comparison
left as “later”.

## Q58 — JSON Patch never — decided

`changes` is a JSON **object** with Merge Patch semantics (Q8). RFC 6902 JSON
Patch (an array of pointer ops) is never the OpenBook change format.

Rejected: RFC 6902 as an alternative encoding; optional MAY Patch.

**Supersedes:** none of Q8; puts the “never” on the corpus.
