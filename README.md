# OpenBook — an open standard for sportsbook data

**Status:** `v0.1.0-draft` · working draft, not yet published · started 2026-09-12
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
openbook/
  README.md               ← you are here
  spec/
    openbook.md           ← the normative reference specification
  schema/                 ← JSON Schema (draft 2020-12), the machine-normative field definitions
    reference_sport.schema.json
    fixture.schema.json
    market_type.schema.json
    odds_change.schema.json
  vocabularies/           ← the controlled vocabularies (the real contribution)
    sports.md
    market_types.md
  examples/               ← sample messages that validate against the schemas
    fixture.example.json
    odds_change.example.json
  GOVERNANCE.md           ← open-spec / closed-code, licensing, how it's governed
  VERSIONING.md           ← semver rules for the spec
  CONTRIBUTING.md
  CHANGELOG.md
  LICENSE                 ← CC BY 4.0 (spec text); implementations are the implementer's own
```

## Why this exists

No cross-vendor market taxonomy exists in betting. The books (bet365, FanDuel,
DraftKings) run proprietary catalogs; the providers (Sportradar, Genius, Stats
Perform) publish little or nothing usable, and each integrator re-maps every
feed by hand. The **market-type vocabulary** in [`vocabularies/`](vocabularies/)
is the piece nobody has published — the thing a fragmented industry could rally
around. Background and the full comparison: [`../DATA-STANDARDS.md`](../DATA-STANDARDS.md)
and the companion page [`../data-standards.html`](../data-standards.html).

## Roadmap to a real standard

1. **v0.x — this folder.** Nail the reference objects, the live messages, and a
   first market-type vocabulary. Validate with real drever feeds behind the
   scenes (private adapters).
2. **Split into its own public repo** (`openbook-spec`) once the shape settles —
   this folder is self-contained so a `git subtree split` can lift it out clean.
3. **Ship a validator + conformance suite** so "OpenBook-compliant" is testable.
4. **Land one external adopter** using the mapping layer.
5. **Governance** — start as a gravity play under an open licence; a consortium
   or standards body only once there are 2–3 non-competing adopters.

This folder is a **specification**, not drever code. It intentionally names no
internal system.
