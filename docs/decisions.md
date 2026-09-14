# OpenBook — design decisions

A running log of the decisions that shape the standard, in the order they were
taken, each with the options that were on the table and why one won.

> **This is not the spec.** Current rules live in
> [`../spec/openbook.md`](../spec/openbook.md). Meanings of sports, bets and
> slices live in [`taxonomy.md`](taxonomy.md). This log is *why* those rules
> exist. Where the two disagree, the newer decision here wins until the spec
> catches up (tracked in [`../CHANGELOG.md`](../CHANGELOG.md)).

Status key: **decided** · **proposed** (awaiting confirmation) · **open**.

## Map (jump to a theme)

| Theme | Questions |
| --- | --- |
| What OpenBook is | Q1 · Q2 · Q3 |
| Ids | Q4 · Q5 · Q6 · Q12 · Q53 |
| Catalogue shape | Q7 · Q19 · Q20 · Q21 · Q22 |
| Names and places | Q10 · Q11 · Q13 · Q57–Q70 |
| Live wire | Q8 · Q14 · Q16 · Q17 · Q29 · Q33 · Q46 · Q47 |
| Status, scores, grades | Q15 · Q23 · Q25 · Q27 · Q28 · Q30 · Q31 · Q43 |
| Money and limits | Q39 · Q44 · Q45 |
| Compatibility and ops | Q32 · Q34–Q37 · Q40–Q42 · Q48 · Q49 |
| What we omit | Q71–Q82 · Q86 · Q87 |
| Tooling around the spec | Q96 |

The entries below stay in the order they were taken.

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

## Q11 — Names — decided (Q57 unpack)

There is **no ISO** for a display name. Cite a real standard when one exists;
if none exists, say so (Q57d). Identity is **Q12** (Wikidata), not the string.
Names are mutable. FIFA/ODF/Sportradar/GLEIF all split **id** from **many
labels**.

**Catalog `participant` vs fixture vs `player` (looks correct):** a
participant is a team or an individual (Q21/Q22). Fixture `participants[]` is
that same id plus **role** and **order**, and **copies `name`** so a snapshot
reads without a join. `player` is roster only (person on team); it has **no**
name fields.

**Teams:** `name` required (popular/board). Optional: `location` + `nickname`
(NFL `market`/`name`; empty for Arsenal), `registeredName` (FIFA
international long / registry — not ISO), `shortName`, `abbreviation`.
Sportradar soccer is `name`/`short_name`/`abbreviation` with city on the
**venue**, not the team. NFL uses the split.

**Persons:** `name` is popular/board (`Erling Haaland`, `Ronaldinho`).
Optional `givenName` / `familyName` (vCard RFC 6350 / ITU X.520, schema.org).
Optional `shortName`. No `abbreviation`.

**Both:** optional `names` keyed by **ISO 639-1**; optional `nameLatin`
(method: **ISO 9** Cyrillic, **ISO 843** Greek); other spellings in
`alternateName` (schema.org).

Rejected: required city+nickname; legal name as the only `name`; Print/TV
scoreboard copies from ODF; ISO numbers invented for nicknames.

**Supersedes:** Q11 proposed (v0.3 snake_case list). CamelCase is Q38. Schema
and spec match this names list.

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

## Q56 — MCP and plugins are discovery feeds, not a second wire — decided

A publisher MAY advertise **additional surfaces** (an MCP server, an Agent
Plugin, other client tooling) on the **same discovery document** as the
OpenBook feeds (Q49). Each entry is still `{ name, url }`. Optional
**`kind`** (`snapshot` · `stream` · `docs` · `mcp` · `plugin`), **`id`**,
and **`schemaUrl`** say what the URL is.

- `mcp` and `plugin` URLs point at **that surface's own manifest**, not an
  OpenBook document. OpenBook does not wrap MCP, does not ship MCP or Agent
  Plugins schemas, and does not add `mcp` to `objectType` or the topic
  grammar.
- An MCP/plugin that exposes OpenBook data uses OpenBook document shapes as
  the payload. That is the data standard for adding a plugin: advertise it
  on discovery; keep the wire.

Rejected: inline `mcpServers` in discovery (duplicates MCP's own config);
a new live `object` for MCP; `.well-known/openbook-mcp` as a second
discovery URL; wrapping change messages as MCP-only payloads with a
parallel betting schema; shipping MCP `server.json` schema in this repo
(same as Q54 for OpenAPI).

**Supersedes:** Q49 “named feeds” by adding `kind` / `schemaUrl` / `id`
and naming MCP/plugin. Q52 (no wrap) and Q54 (foreign docs stay at their
own URL) stand.
## Q57 — Name fields unpacked — decided (closes Q11)

Walk: participant vs `player` vs fixture row; team strings; person strings;
citation rule. Recorded as **Q11 decided**. No schema in this patch.

**Q57d:** every field cites a real standard or **none**. Same rule for other
objects later. ISO 639-1, ISO 9, ISO 843, ISO 3166/CLDR (Q10), vCard, schema.org
`alternateName` are real. Display `name`, `nickname`, `abbreviation` have
**no ISO**.

Rejected: invent ISO numbers; drop fields that lack ISO.

**Supersedes:** Q11 “proposed”.

## Q59 — Names on other objects — decided

League and venue use the **team** name package (`name` plus optional
`shortName` / `registeredName`; venue city is not a nickname). Territory
stays **Q10**. Sport, market type, and segment are **`name` only** (vocab
lists).

Rejected: copy city+nickname onto vocab slugs; unpack league names as a
totally different model.

**Supersedes:** none of Q11; extends it.

## Q60 — Season, stage, publisher names — decided

**Season:** `name` is display (`2025/26`, `F1 2026`). There is no ISO for
that label. The machine is `startDate` / `endDate` (**Q9** RFC 3339).
Rejected: required ISO 8601 interval string (duplicates the dates); required
`startYear` as a fake season code.

**Stage:** `name` only; optional `startDate` / `endDate` as already in the
schema. No ISO pattern for “Matchday 7”.

**Publisher:** `name` plus optional `registeredName`. ISO 17442 is the LEI
(the id), not the name string.

Rejected: required stage-name grammar.

**Supersedes:** none.

## Q62 — Venue location — decided (nested Place)

Fixture `location` stays a nested schema.org **Place**: `name`,
`addressLocality`, `territory` (**Q10**), `sameAs`. GeoNames or Wikidata MAY
sit on `sameAs` / `identifier`. Stadium **name** has no ISO. City is on the
venue (Sportradar), not the team.

Rejected: GeoNames required; a first-class catalog `venue` object in this
walk.

**Supersedes:** none of Q10 or Q59.

## Q64 — IANA time zone on Place — decided

Optional `timeZone` (`Europe/London`) from the **IANA time-zone database**.
Every timestamp remains RFC 3339 with an explicit offset (**Q9**). The zone
is display (“stadium clock”); it does not replace the offset.

Rejected: no TZ field; TZ required on every location.

**Supersedes:** none of Q9.

## Q66 — Fixture name — decided

`name` on a fixture is an **optional** display string (“Arsenal vs Chelsea”).
No ISO. The facts are `participants[]` and `startDate`. schema.org
`SportsEvent.name`.

Rejected: required composed title; forbid the field.

**Supersedes:** none.

## Q68 — Feed language — decided

Optional `inLanguage` on the **publisher** (ISO 639-1). A bare `name` is in
that language. Other languages use `names`. schema.org `inLanguage`.

Rejected: `name` is always English; no feed language.

**Supersedes:** none of Q11.

## Q69 — Place address — decided

`addressLocality` (city string) + `territory` (**Q10**). No street, no
postal code. City name has no ISO; GeoNames remains optional (**Q62**).

Rejected: full PostalAddress; required UN/LOCODE.

**Supersedes:** none of Q62.

## Q70 — Place coordinates — decided

Optional `latitude` / `longitude` in **WGS 84** (schema.org GeoCoordinates,
EPSG:4326). Not required.

Rejected: no coordinates; required on every Place.

**Supersedes:** none of Q62.

## Q71 — Venue capacity — decided (omit)

No capacity field. Seat count is not a price-feed fact. No ISO.

Rejected: optional or required capacity.

**Supersedes:** none of Q62.

## Q72 — Competition sex category — decided

Optional on the **league** as **`gender`**: `men` · `women` · `mixed` ·
`open`. Vocab, not ISO 5218. Not a field on the person.

Rejected: person-level FIFA Gender; both; omit (would hide WSL vs EPL).

**Supersedes:** none.

## Q73 — Age-grade competitions — decided

Optional `ageGroup` on the **league** (`open`, `U21`, `U19`, …). Growable
vocab (**Q34**). No ISO. Not date of birth on the person.

Rejected: name-only; person DOB as the league key.

**Supersedes:** none of Q72.

## Q74 — Date of birth — decided (omit)

No date of birth on the wire. Age-grade competitions are **Q73**. PII.

Rejected: optional or required DOB.

**Supersedes:** none.

## Q75 — Height and weight — decided (omit)

No height or weight. Shirt `number` and `position` stay on `player`.

Rejected: optional SI measurements; required.

**Supersedes:** none.

## Q76 — Player position — decided (free string)

`player.position` stays an optional free string. No ISO. Unknown values
are tolerated (**Q34**). A per-sport vocab is later, not this walk.

Rejected: required shared position ids now; drop the field.

**Supersedes:** none.

## Q77 — Team colours / kit — decided (omit)

No kit or colour fields. Presentation, not a price fact.

Rejected: optional hex; required.

**Supersedes:** none of Q62.

## Q78 — Team home stadium — decided (omit)

No home-venue on the team. The match venue is fixture `location` (**Q62**).
Home/away is fixture **role** (**Q22**).

Rejected: optional or required home Place on the club.

**Supersedes:** none of Q62.

## Q79 — Manager / coach — decided (omit for now)

No coach object. Add a role later if manager markets need it (**Q35** never
reuse names).

Rejected: optional or required coach now.

**Supersedes:** none.

## Q80 — Match lineup — decided (lineup object)

`player` is **roster** (season membership). Starting XI is a live **`lineup`**
object, fixture-keyed, not fields on the catalog fixture. The ids are roster
**`player`** ids. Formation, substitutions, and predicted lineup stay omitted
(**Q82**).

Rejected: starter ids on the fixture now; never a match XI; person ids
without the roster row.

**Supersedes:** none. Spec already says `player` is for lineups/props; match
XI is not the roster row.

## Q81 — Match officials — decided (omit for now)

No referee object. Add later if those markets exist (**Q35**).

Rejected: optional or required officials now.

**Supersedes:** none.

## Q82 — Encyclopedia fields — decided (omit)

Omit from OpenBook (not a price feed). Presentation, PII, or another
sport’s wiki. **Q74 / Q75 stay omit** (DOB, height/weight).

Omit includes: venue roof, pitch size, attendance, weather; team mascot,
owner, founded, social, photos, stock ticker, LEI, rivalries, derby flag,
retired numbers; person nationality besides territory, passport names, salary,
transfer fee, draft pick, agent, headshot; formation, substitutions, VAR,
ball type; TV/streaming/radio, hashtags, sponsors, ticket price, prize
money; xG/possession/shots, ranking tables, medal tables; coverage flags,
predicted lineup, highlight clips. Kit, home stadium, coach, officials,
capacity already omitted in Q71/Q77–Q79/Q81.

Not in this omit (later questions): pitch **surface**, **seed**, racing
**draw/stall**, cricket **toss**, playoff **series state**.

Rejected: keep asking those encyclopedia fields one by one.

**Supersedes:** none; does not reopen Q74/Q75.

## Q84 — Playing surface — decided

Optional `surface` on the **fixture**: `grass` · `clay` · `hard` · `turf` ·
`ice` · `indoor` · … Growable vocab (**Q34**). No ISO. This match’s court,
not the club’s usual lawn.

Rejected: Place only; omit; required on every fixture.

**Supersedes:** none of Q62. Not in the Q82 omit list.

## Q85 — Tournament seed — decided

Optional integer `seed` on the **fixture participant** row. This draw, not
the person. No ISO.

Rejected: seed on the catalog person; omit; seed only on the stage.

**Supersedes:** none of Q22.

## Q86 — Generic fixture extras — decided (stop here)

The generic fixture’s extra named fields stop at **`surface`** (Q84) and
**`seed`** on the participant row (Q85). No `metadata` bag. Racing draw,
cricket toss, playoff series state are **not** more keys on every fixture.
They wait for stage, a later live object, or a sport-specific slice. Vendor
junk stays `x_` (**Q37**).

Rejected: keep bolting optionals onto fixture; a `metadata` object.

**Supersedes:** none. Closes the “leftover” list from Q82 as *not on fixture*.

## Q87 — Catalog pass closed — decided

This walk of names, place, omits, surface, seed, and the junk-drawer rule
is **closed**. Further questions are a **new area**, not more keys on the
generic fixture.

Rejected: unpack stage/series immediately; jump to Q46 wire in this
question.

**Supersedes:** none.

## Q88 — Throwing/shooting and batting hand — decided

Optional on **`player`** (roster), not the person: **`throws`** (throwing or
shooting) and **`bats`**. Each is `left` · `right` · `both`. No ISO.
`both` is switch / either hand.

Rejected: one `hand` field; ISO 5218-style sex codes; person-level FIFA
Gender as a stand-in.

**Supersedes:** none of Q75/Q76.

## Q89 — JSON is the v1 encoding; other encodings are not forbidden — decided (A)

The required v1 encoding is **JSON** (`application/json`). The spec, JSON
Schemas, examples, discovery document, conformance corpus, validator, site,
and AsyncAPI `defaultContentType` describe this encoding only. OpenBook
scaffolding does not ship `.proto`, SBE, or another codec in v1.

Additional encodings (protobuf, SBE, or anything else) **MAY** exist later
as optional bindings, generated from the existing JSON Schemas — the same
pattern OpenRTB uses (JSON default, protobuf optional). This log does **not**
forbid them and does not require them.

A later encoding is a new binding of the same objects, not a second data
model. Decimal strings (**Q39**), Merge Patch (**Q8**), and RFC 3339 (**Q9**)
stay the contract.

Rejected: protobuf/SBE as the v1 encoding; JSON-only forever; shipping
`.proto` now; leaving this as unnumbered industry-pattern prose.

**Supersedes:** none of Q8/Q39/Q40. Pins `docs/industry-patterns.md` “JSON in
v1; binary later”.

## Q90 — No GBFS-style data wrapper — decided (A)

GBFS wraps every file in `last_updated` / `ttl` / `version` / `data`.
OpenBook does not. Discovery is `{ lastUpdated, ttl, feeds }` at the root
(**Q49**). Object documents and change messages are the object (**Q8**).
They are not nested under a GBFS-style data member, on HTTP pull or on
sockets.

Rejected: wrap HTTP pull only; wrap every message including MQTT / WebSocket
/ SSE; leave this unsaid because Q49 named discovery.

**Supersedes:** none of Q49. GBFS-shaped means `ttl` and the discovery
fields, not the GBFS file envelope.

## Q91 — JSON Patch (RFC 6902) — decided (never)

Change semantics stay **JSON Merge Patch (RFC 7386)** (**Q8**). RFC 6902
JSON Patch is **not** an alternate change encoding, on pull or on sockets.

Rejected: optional second patch language; JSON Patch on HTTP pull only;
leave RFC 6902 unsaid because Q8 named Merge Patch.

**Supersedes:** none of Q8. Same kind of pin as Q52 (envelope) and Q90
(no second wrapper).

## Q92 — ISO 20022 is not the OpenBook model or encoding — decided (never)

The wire stays JSON Schema, schema.org-aligned camelCase (**Q13** / **Q38**),
and Q44 money (`{amount}` plus feed `baseCurrency`). ISO 20022 XML and the
ISO 20022 JSON trial are **not** the OpenBook encoding. They do not rename
money fields and they do not replace JSON Schema.

Rejected: adopt the ISO 20022 JSON trial money shape; add an ISO 20022
mapping document in this question; leave ISO 20022 unsaid because Q13/Q38/Q44
named names and money.

**Supersedes:** none of Q13/Q38/Q44.

## Q93 — FIX session is not the OpenBook session — decided (never)

Session and recovery stay **Q33** / **Q46**: `snapshotComplete`,
`heartbeat` + `heartbeatMs`, stale `since` is HTTP 410. FIX Logon /
Heartbeat / TestRequest / Logout, and sequence reset, are **not** the
OpenBook session. A later SBE binding (**Q89**) would still carry OpenBook
heartbeats, not FIX Logon.

Rejected: adopt FIX TestRequest / Heartbeat / Logout on the socket; add a
FIX-session mapping document in this question; leave this unsaid because
Q46 rejected a client TestRequest pair.

**Supersedes:** none of Q46.

## Q94 — No spec-owned multi-publisher manifest — decided (A)

Each publisher has **one discovery URL** (**Q41** / **Q49**). That document
lists that publisher's feeds, not other publishers. An aggregator is itself
a publisher (**Q1**) and lists its own feeds. There is no spec-owned
GBFS-style manifest of many publishers.

Rejected: an OpenBook manifest of many publishers' discovery URLs; putting
other publishers' discovery URLs on this publisher's discovery document;
leave this unsaid because Q49 named one URL per publisher.

**Supersedes:** none of Q1/Q49.

## Q95 — Protocol-fit pass closed — decided

This walk of encoding, wrappers, patch language, ISO 20022, FIX session,
and discovery index is **closed**. Further questions are a **new area**,
not more take/don't-take pins from that comparison list.

Rejected: keep minting never-X questions from memory; unpack another
protocol in this question.

**Supersedes:** none.

## Q96 — Vendor mapping and starter are not this spec — decided

OpenBook is the **target language**. Mapping 487 / KIBL / Optic / LinePros /
MollyBet (or any unknown inbound) onto it is **not** the specification,
the way FHIR keeps concept maps beside Patient and GTFS does not ship a
vendor translator.

Planned Python tooling (not in this repo; names only, repos not created
in this change):

- **openbook-starter** — copyable example + CLI `openbook start`. Writes
  documents only under `openbook/`: publisher, discovery, `snapshot.json`
  (the publisher document). Discovery lists only URLs that exist
  (snapshot, not placeholder stream/docs). Identity: flags, prompt if
  missing; `--no-input` for scripts. One default source
  `{publisher-id}-book`. `--base-url` or prompt. `openbook/README.md`
  only. Refuse if `openbook/` exists unless `--force`. Apache-2.0.
  Python 3.11. v1 CLI is `start` only. Optional extra
  `openbook-starter[translations]` depends on openbook-translate; `start`
  does not edit the caller's pyproject. Game-props / player-props /
  futures packages wait.
- **openbook-translate** — ABC: one record, sync `translate` (vendor →
  OpenBook documents) and `reverse` (OpenBook → vendor bytes + optional
  dict). Inbound: raw bytes + optional parsed dict + source id. Unmapped:
  quarantine (raw + reason), not raise/skip. Success MUST carry native id
  on `identifier` so reverse can round-trip. Official implementer is a
  synthetic **acme** adapter for contract tests. Community MAY publish
  `openbook-translate-kibl` etc.; this project will not. Vendored copy of
  `schema/*.json` plus an `openbook-spec-version` stamp; `update` CI goes
  red when the spec moved (notify only; no git writes from a cluster).
  Apache-2.0 code; schemas remain CC BY with NOTICE.

No auto-rewrite of feed JSON when the spec moves (0.x-draft will move
often). `openbook start` MAY write `.github/workflows/openbook-update.yml`:
daily cron + `workflow_dispatch` is the check; the *meaning* is protocol
change; the job fails (GitHub CI red), it does not commit.

Rejected: Django-cookiecutter of a sportsbook in the spec repo; in-cluster
commits; official vendor adapters; a second reverse-only package; putting
adapter classes in `spec/openbook.md`.

**Supersedes:** none of Q1/Q6/Q49/Q56. Mapping stays off the wire.

## Q97 — Pinnacle specials — decided (markets)

A Pinnacle special that is one priced question (contestants, cutoff) is an
OpenBook **market** on a fixture. No new object. HT/FT is one n-way, not an
SGP. SGP/parlay is combining markets.

Rejected: a Pinnacle-only specials object; treat HT/FT as a same-game parlay.

**Supersedes:** none of the market vocabulary.

## Q98 — Market unit classifier — decided (optional `basis`)

A market is **shape × unit × segment**, not a new type per unit.

- **`marketType`** is the shape (`market:total`, `market:correct-score`,
  `market:draw-no-bet`, `market:half-time-full-time`, `market:moneyline`, …).
  A 3-way moneyline is `market:moneyline` with a draw side, not a new id.
- **`basis`** is what it counts — the same `scoreUnit` list as score and
  grade (`corners`, `goals`, `runs`, …). Optional on the priced market. If
  omitted, sport/league `primaryUnit` (the sport default: goals, points,
  runs, …).
- **`segment`** is the slice (`1st-half`, full game, first five innings, …).

Same fixture. Identity: `(source, fixture, marketType, segment, line, basis)`.
Grade already requires `basis`; the priced market names the same thing.

Rejected: `market:corner-total` / `market:corner-dnb` and friends; Pinnacle
cloned “Corners” events; required `basis` on every goals market.

This decision does **not** add new `scoreUnit` values. `bookings` and
home-runs stay until a payload names them.

**Supersedes:** none. Completes Q26 for priced markets.

## Q99 — Statuses and settled — decided (keep the four places)

Four jobs, four places. No new fields.

- **Event lifecycle** — `eventStatus` on fixture and score.
- **Match progress** — `score` only: `currentSegment`, `segmentStatus`
  (`pending` · `live` · `paused` · `down`), `clock`, `scores[]`. Not on
  odds. `paused` is halt on the field, not odds offline.
- **Betting** — per-market `marketStatus` (`open` · `suspended` ·
  `closed` · `void`). A period going offline is a fan-out: those markets
  with that `segment` change status (Sportradar `bet_stop`). Prefer
  touching only the affected markets; bulk only when the book took the
  whole period down. Outcome `active` stays on the outcome.
- **Book’s call** — the `grade` object. Not a market status.

Pinnacle `/fixtures/settled` period rows map to a segment going `down`
once (Q28) with final `bySegment` numbers. Pinnacle `/bets` maps to
`grade`. Deleted event is `fixture/delete`, not a fake settled period.
Corrections stay Q31 (`score` erratum; `grade/delete` + new grade with
`supersedes`).

Rejected: betting-open on the fixture; a stored betting flag on the
segment (Pinnacle period `status` as state); `marketStatus: settled`;
a `settlement` object / `settlementId`; progress fields on the odds
envelope.

**Supersedes:** none of Q25 / Q27–Q31 / Q43. Confirms that mapping for
the Pinnacle Lines walk.

## Q100 — Parlay / teaser flags — decided (omit)

Do not put parlay or teaser flags on the fixture. If a book publishes a
parlay or same-game parlay, it is a **market** (`market:parlay` /
`market:same-game-parlay`). Whether two lines may be combined is book
policy (Pinnacle `/line/parlay`, Bets API) — out of scope.

Rejected: `parlayRestriction` / `altTeaser` on the fixture; flags on
each market for “may be parlayed.”

**Supersedes:** none of Q97.

## Q101 — One fixture — decided (C)

Pregame and live are **one fixture**. `eventStatus` is scheduled / live /
ended. No second id. No `parentId`. `superEvent` is not a live→pregame
pair (that was a Pinnacle clone).

Rejected: two fixtures linked by `superEvent`; copying `parentId`; a
corners child event (corners is `basis` on the same fixture, Q98).

**Supersedes:** the walk note that pregame and live are separate fixtures.

## Q102 — Sports catalog — decided (A)

OpenBook sport ids stay `sport:*` (`sport:soccer`, `sport:unknown`, …).
A vendor integer (Pinnacle `sportId`) maps with `identifier` / `sameAs`.
Add a sport to the vocab when it is priced, not by dumping `/sports`.
Consumers MUST accept unrecognised `sport:*` values (Q34).

Rejected: Pinnacle sport integers as OpenBook ids; import their full list
now.

**Supersedes:** none of the sports vocabulary.

## Q103 — Get Line — decided (A)

Market `limit` is enough on the feed (Q45). Pinnacle `/line` is a ticket
check before placing — Bets API, out of scope. No second limit object, no
min-stake field in this pick.

Rejected: copying Get Line onto the market; adding min stake as well as
max `limit`.

**Supersedes:** none of Q45.

## Q104 — Game-prop outcome shapes — decided (A)

Industry encodes props as runner/contestant **strings** or new market ids.
OpenBook does not. Typed extras per shape, same `market:*` ids, same
`basis` / `segment`:

- Correct score: two counts on the outcome (home amount, away amount)
  plus the existing `other` bucket. Corners CS is `basis`, not a new type.
- HT/FT: two results on the outcome (HT, FT), each home / away / draw.
- Winning margin: who + a number or band. Band field not named yet.
- Double chance / odd-even / first-to-score none: grow `side` with tokens
  the vocab already claims. Tokens not added until named in a later Q.
- Player over/under: existing over/under + roster `player` on the outcome.
  Do not explode a new `market:*` per player stat in this pick.

Rejected: one free-text selection string as identity (Pinnacle contestant /
Betfair runner); new `market:*` per prop, period, or unit (Odds API / UOF).

No new field names in this pick. Wire waits for the names.

**Supersedes:** none of Q98. Completes “every shape on corners” for
selections.

## Q105 — Prop outcome names — decided (A)

- Correct score: **`homeTotal`**, **`awayTotal`** (JSON numbers, same as
  `scores[].total`). `side: other` is the unlisted bucket.
- HT/FT: **`halfTime`**, **`fullTime`**, each a `side` of `home` · `away` ·
  `draw`.
- Winning margin: existing **`participant`** + **`line`**. Plus-bands
  (`3+`) are `side: other` until a band is named.
- Player over/under: **`player`** (roster own id).
- `side` tokens to add: **`odd`**, **`even`**, **`none`**,
  **`home-or-draw`**, **`away-or-draw`**, **`home-or-away`**.

Rejected: `homeScore` / `awayScore`; contestant string; `playerId`.

**Supersedes:** Q104 “names later”.

## Q106 — Wire Q105 — decided (A)

The Q105 fields and `side` tokens go on **`market`**, **`odds/change`**,
and **`grade`** outcomes. Same extras on all three so a grade can name
the same selection the market priced.

Not wired in this pick.

Rejected: market-only (grade cannot match); a new object for prop
selections.

**Supersedes:** Q105 “not wired”.

## Q107 — One market, many rows — decided (A)

Correct score, HT/FT, and winning margin are **one market** with many
rows. No handicap number on that market. The row carries the score
(`homeTotal` / `awayTotal`), the HT/FT pair, or the margin (`participant`
+ outcome `line`). Plus-bands stay `side: other` until a band is named
(Q105).

Player over/under still has its number on the market (the 24.5).

Not wired in this pick.

Rejected: a separate market per score, HT/FT combo, or margin band.

**Supersedes:** none of Q106. Says where `line` sits for those boards.

## Q108 — Player on the row is an id — decided (A)

Player over/under names the person with their OpenBook id only. The
name lives on the player record, not on the price row.

Not wired in this pick.

Rejected: id plus name on every price row.

**Supersedes:** Q105 “roster own id” (same meaning, now explicit).

## Q109 — HT/FT is home, away, or draw — decided (A)

On a half-time/full-time row, `halfTime` and `fullTime` are only
**home**, **away**, or **draw**. Not over, odd, other, or the rest of
`side`.

Not wired in this pick.

Rejected: the full `side` list on those two fields.

**Supersedes:** Q105 “each a side of home · away · draw” (same three,
now exclusive).

## Q110 — HT/FT is always a pair — decided (A)

An HT/FT row always has both `halfTime` and `fullTime`. A listed
result is a pair (home then draw, away then home, …).

Not wired in this pick.

Rejected: one of the two missing.

**Supersedes:** none of Q109.

## Q111 — Listing is 1; sequence may be 0 — decided (A)

`order` and `seed` stay **1-based** (first listed is 1; top seed is 1).
`sequence` still allows **0** (cursor / `since` from the start). Clocks
and scores still use 0 as a quantity.

Already on the wire. No schema change.

Rejected: 0-based `order` / `seed`; `sequence` minimum 1; one origin for
every integer.

**Supersedes:** none of Q22. Confirms the existing minima.

## Q112 — Listed correct score is both totals — decided (A)

A listed correct-score row always has both `homeTotal` and `awayTotal`.
The leftover bucket (`side: other`) has neither.

Not wired in this pick.

Rejected: one total missing on a listed row.

**Supersedes:** none of Q105.

## Q113 — Listed winning margin is who plus the number — decided (A)

A listed winning-margin row always has **`participant`** and the outcome
**`line`**. Plus-bands (`3+`) stay `side: other` with neither until a
band is named (Q105).

Not wired in this pick.

Rejected: who or the number missing on a listed row.

**Supersedes:** none of Q107.

## Q114 — A row does not mix boards — decided (A)

A row only carries the extras for that board. Correct-score totals do
not appear on an HT/FT row, and so on.

Not wired in this pick.

Rejected: mixing extras from different boards on one row.

**Supersedes:** none of Q105–Q113.

## Q115 — Player over/under always names the player — decided (A)

Every player over/under row has `player` (the OpenBook id, Q108).

Not wired in this pick.

Rejected: the id missing on that row.

**Supersedes:** none of Q108.

## Q116 — None is not the leftover — decided (A)

`none` is a real listed selection (nobody scores / no booking). Leftover
stays `other` (unlisted score, plus-bands until named).

Not wired in this pick.

Rejected: `none` as the leftover bucket.

**Supersedes:** none of Q105.

## Q117 — Prop-row pass closed — decided (A)

Names and row rules for typed prop outcomes stop here. Plus-bands stay
`side: other` until a band is named. Wire is Q105–Q116 on `market`,
`odds/change`, and `grade`.

Rejected: keep asking row-rule questions in this pass.

**Supersedes:** Q106 “not wired in this pick”.

## Q118 — Next area is plus-bands — decided (A)

This walk names winning-margin plus-bands (`3+`). They stay `side: other`
until the name in a later Q. Not wired in this pick.

Rejected: a new feed walk; stop for a Q86 payload.

**Supersedes:** Q117 “until a band is named” (this is that walk).

## Q119 — Plus-band name is atLeast — decided (A)

The plus-band extra is **`atLeast`**, a JSON number (same as
`homeTotal`). 3 means 3 or more. Exact winning-margin rows still use
outcome `line`.

Not wired in this pick.

Rejected: reuse `line` as the floor.

**Supersedes:** Q105 “until a band is named”; Q118 “name later”.

## Q120 — Plus-band is who plus atLeast — decided (A)

A plus-band row always has **`participant`** and **`atLeast`**. It is
not leftover `other`.

Not wired in this pick.

Rejected: who or `atLeast` missing on that row.

**Supersedes:** Q113 leftover for named plus-bands.

## Q121 — Plus-band does not carry exact line — decided (A)

A plus-band row has `atLeast`, not outcome `line`. An exact margin has
`line`, not `atLeast`. Same Q114 mix rule.

Not wired in this pick.

Rejected: both on one row.

**Supersedes:** none of Q114.

## Q122 — Wire atLeast — decided (A)

`atLeast` goes on **`market`**, **`odds/change`**, and **`grade`**
outcomes. Same extras on all three so a grade can name the plus-band
the market priced.

Not wired in this pick.

Rejected: market-only.

**Supersedes:** Q119 “not wired”.

## Q123 — Plus-band pass not closed — decided (B)

Do not close this pass. Name and row rules are not finished.

Not wired in this pick.

Rejected: close here.

**Supersedes:** none of Q122.

## Q124 — Leftover other still allowed on winning margin — decided (A)

`other` stays the unlisted remainder on winning margin. `atLeast` is
only when they list a plus-band.

Not wired in this pick.

Rejected: only exact `line` rows and `atLeast` rows; no leftover.

**Supersedes:** none of Q116.

## Q125 — Plus-band pass closed — decided (A)

Names and row rules for plus-bands stop here. Wire waits until
implement (`atLeast` on `market`, `odds/change`, and `grade`, Q122).
Later pick wired those extras.

Rejected: keep asking plus-band questions in this pass.

**Supersedes:** Q123 (pass not closed).

## Q126 — Next area is player on yes/no — decided (A)

Player yes/no rows (anytime scorer / to score) name the person with the
same OpenBook `player` id as player over/under. No new market type.

Not wired in this pick.

Rejected: a new book feed walk; stop until plus-bands merge.

**Supersedes:** Q117 “pass closed” as the next area, not the prop extras.

## Q127 — Player id always on yes/no player rows — decided (A)

Every yes/no player row has `player`. Same rule as player over/under
(Q115).

Not wired in this pick.

Rejected: optional on some yes/no rows.

**Supersedes:** none of Q115 or Q126.

## Q128 — Leftover other is not used on yes/no player boards — decided (A)

Yes/no player rows are only `yes` / `no` for a named player. Leftover
`other` is not used on these boards.

Not wired in this pick.

Rejected: `other` allowed (someone else, or unlisted).

**Supersedes:** none of Q124 (winning-margin leftover still allowed).

## Q129 — No is optional on yes/no player boards — decided (A)

They may list only `yes`. `no` is optional.

Not wired in this pick.

Rejected: both `yes` and `no` required for each named player.

**Supersedes:** none of Q128.

## Q130 — Yes/no player is one market, many rows — decided (A)

A yes/no player board is **one market** with many named-player rows.
Same idea as Q107 for correct score / HT/FT / winning margin.

Not wired in this pick.

Rejected: one market per player.

**Supersedes:** none of Q107 (player over/under still has its number on
the market).

## Q131 — Yes/no player market omits line — decided (A)

A yes/no player market has no `line`. Anytime scorer / to score has no
threshold like player over/under (the 24.5).

Not wired in this pick.

Rejected: keep a market `line`.

**Supersedes:** none of Q107 (player over/under still has its number).

## Q132 — Yes/no player pass closed — decided (A)

Names and row rules for yes/no player rows stop here: same `player` id
as over/under; always present; leftover `other` is not used; `no` is
optional; one market, many rows; no market `line`. Wire waits until
implement. No new field.

Later pick wired those extras (spec, pairing, example). No new field.

Rejected: keep asking yes/no player questions in this pass.

**Supersedes:** Q126 as an open walk (the area is decided; the pass is
closed).

## Q133 — Stop this spec walk — decided (A)

No new board until named. Q86 stays parked (needs a payload). Yes/no
player row rules are written in this pick (no new field).

Rejected: unpark Q86; a new book-feed walk.

**Supersedes:** Q132 as an open “what is next”.

## Q134 — Unpark Q86 leftovers — decided (A)

This walk is the Q86 leftovers: racing stall, cricket toss, playoff
series. They are still **not** more keys on every fixture (Q86). Names
and home (stage, live object, or sport slice) wait for later Qs.

Not wired in this pick.

Rejected: stay stopped (Q133); unpark Q55.

**Supersedes:** Q133 “Q86 stays parked”; Q133 “no new board until named”.

## Q135 — All three leftovers in this pass — decided (D)

This pass covers racing stall, cricket toss, and playoff series. One
pass, three leftovers. Names and home still wait.

Not wired in this pick.

Rejected: series only; stall only; toss only.

**Supersedes:** none of Q134 (the leftovers list). Says the pass is all
three, not one first.

## Q136 — Still not keys on every fixture — decided (A)

Stall, toss, and series stay off the generic fixture. Keep Q86. Home is
stage, a live object, or a sport slice, decided per leftover.

Not wired in this pick.

Rejected: reopen Q86; put them on the generic fixture.

**Supersedes:** none of Q86 (same rule, now for this walk).

## Q137 — Each leftover its own home — decided (A)

Stall, toss, and series each have their own home. Not one object that
holds all three. Not all three on `stage`.

Not wired in this pick.

Rejected: one new live object for all three; all three on `stage`.

**Supersedes:** none of Q136.

## Q138 — Stall and toss are sport slices; series is not — decided (A)

Stall and toss are sport-specific. Series is a separate home (stage or
live), not a racing or cricket field.

Not wired in this pick.

Rejected: all three are sport-specific, including series; none are
sport-specific.

**Supersedes:** none of Q137.

## Q139 — Series round on stage; lead is live — decided (C)

The printed round stays on `stage` (`seriesGame`). The series lead (who
is up 2–1) is live. Not the round name copied again.

Not wired in this pick. Live object name waits.

Rejected: `stage` only; live only (drop the round from `stage`).

**Supersedes:** none of Q138.
