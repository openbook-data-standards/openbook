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
`updated_at`.
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
names. `ioc_code`, `fifa_code` and `wikidata` ride on the region record as
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

## Q11 — Names — proposed (implemented in v0.3)

There is **no ISO standard for team or person names.** The real standards
nearby: **vCard (RFC 6350 / ITU X.520)** for a person's name structure
(family · given · additional · prefix · suffix — also schema.org's
`familyName` etc.); the **Olympic Data Feed**, which gives every athlete
several display forms (`PrintName`, `TVName`, `TVInitialName`,
`LocalFamilyName`…); and **finance**, which standardises *identity* (ISIN,
LEI) and treats the name as a mutable attribute — our `sameAs` stance.
Implemented shape:

- `name` — canonical display name, UTF-8, diacritics allowed.
- `short_name`, `abbreviation` — optional.
- `aliases[]` — the other spellings a book might use.
- `names` — optional per-language variants keyed by ISO 639-1 (`en`, `es`).
- `name_latin` — optional transliteration (ISO 9 for Cyrillic, ISO 843 for
  Greek) for sorting and matching.
- Persons: optional `given_name` / `family_name` (schema.org `Person`).

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

`market/update` carries CAP-style `msg_type` (alert · update · cancel),
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
**`competition_type`** (league · cup · tournament · series · exhibition). An
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

Every small shared vocabulary is a `*_type` field: `competition_type`,
`participant_type`, `market_type`, `stage_type`. No `kind` / `format`
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

## Q31 — Corrections without settling twice — proposed

A downed segment's `status` / `downAt` are frozen. A correction is
`score/update` with `correction: true` + `statusReason` (an erratum), and
affected grades are `grade/delete` + new `grade/create` with `supersedes`.
(Rejected: reopen → down again; absolutely immutable with no corrections.)
