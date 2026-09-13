# OpenBook — an open standard for sportsbook data

**Status:** `v0.3.0-draft` · working draft, not yet published · started 2026-09-12
**Name:** OpenBook · **What it is:** an open standard for sportsbook & gambling data · **The document:** the OpenBook specification in [`spec/openbook.md`](spec/openbook.md)

OpenBook is an open standard for exchanging **sportsbook & gambling data** —
the reference catalog (sports, leagues, fixtures, markets) and the live wire
(odds, scores, settlement). It is modelled on the live-data feed standards that
already work in the open — **[GTFS / GTFS-Realtime](https://gtfs.org/documentation/realtime/reference/)**
for public transit, **[GBFS](https://gbfs.org/)** for shared mobility, and
**[MQTT](https://mqtt.org/) (ISO/IEC 20922)** for real-time pub/sub — not on
enterprise business-messaging standards.

> **Open spec, closed code.** OpenBook standardises the *data contract* — schemas
> and vocabularies. It says nothing about how a provider produces or prices the
> data. Anyone can implement it privately and keep their engine, models and
> pricing proprietary. See [`GOVERNANCE.md`](GOVERNANCE.md).

## The one idea

Two tiers, the same split GTFS uses:

- **Reference tier** — durable, bounded objects: sport, region, league, season,
  participant, player, segment, market type, side, **fixture**. The "timetable".
  (Analogous to GTFS static: agencies, routes, stops, trips.)
- **Live tier** — streamed diffs that point back at reference ids and carry only
  what changed: **odds, scores/state, settlement**. The "vehicle positions and
  arrival predictions". (Analogous to GTFS-Realtime.)

Everything is keyed by a **neutral, readable, namespaced id** owned by the
standard (e.g. `sport:soccer`, `market:total`, `fixture:<uuid>`). Every
provider's own id is carried on a mapping record — never used as the canonical
key.

## Layout

```
openbook/  (this repository)
  README.md               ← you are here
  index.html                ← project homepage (GitHub Pages)
  docs/
    decisions.md            ← the design decision log
  spec/
    openbook.md           ← the normative reference specification
  schema/                 ← JSON Schema (draft 2020-12), the machine-normative field definitions
    common.schema.json            shared $defs: ids, territory, wikidata, sequence, provenance
    publisher.schema.json         who transmits + the sources the feed carries
    sport.schema.json             region · participant (teams AND individuals) · stage · market_type
    fixture.schema.json           the base object + standard facts
    change.schema.json            the one message envelope: object / action, Merge Patch
    league.schema.json            any recurring competition, typed by competition_type
    odds_change.schema.json       payload of odds/change
    market.schema.json            a fixture's market for one source (snapshot / update document)
    score.schema.json             live state: three statuses, clock, score lines per participant x unit x segment
    grade.schema.json             the book's grade of one market from a down segment; never edited
    season.schema.json · player.schema.json
