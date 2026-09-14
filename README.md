# OpenBook — an open standard for sportsbook data

<p>
<img src="assets/logo.svg" alt="OpenBook" height="40">
</p>

<p>
<a href="https://github.com/openbook-data-standards/openbook/actions/workflows/validate.yml"><img alt="validate" src="https://github.com/openbook-data-standards/openbook/actions/workflows/validate.yml/badge.svg"></a>
<img alt="version" src="https://img.shields.io/badge/spec-v0.3.0--draft-276EF1">
<img alt="status" src="https://img.shields.io/badge/status-draft-A8620A">
<a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/spec%20license-CC%20BY%204.0-000000"></a>
</p>

**Homepage:** https://openbook-data-standards.github.io/openbook/


**Status:** `v0.3.0-draft` · working draft, not yet published · started 2026-09-12
**Name:** OpenBook · **What it is:** an open standard for sportsbook & gambling data · **The documents:** [plain-language guide](docs/guide.md) · [examples](docs/examples.md) · [taxonomy](docs/taxonomy.md) · [specification](spec/openbook.md)

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
    guide.md              ← plain-language walkthrough (non-normative)
    examples.md           ← one match, in order (GTFS-style sample feed)
    taxonomy.md           ← shared lists explained without wire rules
    decisions.md            ← the design decision log
  spec/
    openbook.md           ← the normative reference specification
    asyncapi.yaml         ← push streams (Q42); MQTT not required
  schema/                 ← JSON Schema (draft 2020-12), the machine-normative field definitions
    common.schema.json            shared $defs: ids, territory, wikidata, sequence, provenance
    publisher.schema.json         who transmits + the sources the feed carries
    sport.schema.json             region · participant (teams AND individuals) · stage · marketType
    fixture.schema.json           the base object + standard facts
    change.schema.json            the one message envelope: object / action, Merge Patch
    league.schema.json            any recurring competition, typed by competitionType
    odds_change.schema.json       payload of odds/change
    market.schema.json            a fixture's market for one source (snapshot / update document)
    score.schema.json             live state: three statuses, clock, score lines per participant x unit x segment
    grade.schema.json             the book's grade of one market from a down segment; never edited
    season.schema.json · player.schema.json
    discovery.schema.json         one URL lists snapshot, stream, docs, MCP, plugins (Q49, Q56)
  examples/               ← valid worked documents (also the valid corpus)
  conformance/            ← language-agnostic corpus (manifest + invalid cases)
  tools/validate.py       ← one runner; not a language oracle
