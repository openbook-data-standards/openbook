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

## Q11 — Names — open

There is **no ISO standard for team or person names.** Proposed shape:

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

## Q13 — Field-name alignment with schema.org — open

schema.org `SportsEvent` / `SportsTeam` / `Person` is the vocabulary Google's
structured data uses (`homeTeam`, `awayTeam`, `competitor`, `startDate`,
`location`, `alternateName`). Proposal: align OpenBook field names with it
where there is no reason not to, so OpenBook data maps onto the web's existing
sports vocabulary for free.

## Q14 — Stream naming grammar — proposed (implemented provisionally in v0.2)

Modelled on the WIS2 topic hierarchy: a fixed, versioned set of levels,
lowercase, dash-separated, no dots, unique per level. Proposal:

`openbook / <version> / <publisher-id> / <message-type> / <sport> [/ <league>]`

e.g. `openbook/v1/acme-books/odds_change/soccer/gb-premier-league`.
Consumers subscribe with wildcards at any level. A major version bump only on
rename or removal of a level value; additions are minor.

## Q15 — Suspensions, re-opens and voids as alerts — proposed (implemented provisionally in v0.2)

Modelled on CAP 1.2: a `market_status` message carries `msg_type`
(`alert` · `update` · `cancel`), the market key, a status
(`suspended` · `open` · `closed` · `void`), an optional reason vocabulary, and
`references` to the message it amends or cancels — so a re-open points at the
suspension it lifts and a void points at the settlement it reverses.
