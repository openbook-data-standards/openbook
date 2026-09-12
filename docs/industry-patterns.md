# Industry patterns — what public betting APIs do, and what OpenBook takes

A review of publicly documented sports-betting APIs, looking for patterns
worth adopting and patterns to avoid. Vendor-neutral: every API here is
public, and each is judged only on its design.

## KIBL Sports Outbound (docs.kibl.io/api) — OpenAPI 3.0.3, 71 endpoints

**Worth adopting**

- **Three families of endpoint** — `/reference/*` (catalogs), `/mapping/*`
  (feed id ↔ canonical id, per `feed_source_id`) and `/info/*` (fixtures,
  markets, outcomes, states, lineups, injuries). This is exactly OpenBook's
  shared-vocab / mapping-record / live-tier split, running in production.
- **Push/pull parity** — every info row carries `routing_key`, the message
  topic it was published on, so the same row shape arrives by push and by
  pull. OpenBook: every object states the stream it belongs to.
- **Pull deltas** — `since_last_updated` on fixtures, states, markets,
  outcomes, injuries and news. The "diffs everywhere" rule, in practice.
  (OpenBook uses a sequence cursor rather than a timestamp; see decisions.)
- **League ruleset** — `clock_based`, `clock_ascending`, `score_based`,
  `segment_based`, `has_halftime`, `allow_ties`, `accepted_segments`,
  `final_eof_segment`. This is what lets a consumer validate scores and
  segments per league. OpenBook's `reference_league.ruleset` follows it.
- **Composite market mapping** — a feed's market id resolves to
  `market_type_id + segment_id + side_id`, scoped by sport and league.
- **Market row flags** — `is_opener`, `is_main`, `is_current`, `is_live`;
  a `uuid` per market row; `market_status_id`.
- **Response envelope** — `code`, `description`, `result[]`, `timestamp`,
  `request_uuid`.
- **Fixture nesting** — participants, states, outcomes, lineups and
  informations nested on the fixture; `parent_fixture_id`; `cutoff_time`.

**Not adopted, and why**

- Integer, owner-specific ids → OpenBook uses readable neutral slugs for shared
  vocabularies and publisher-own ids plus standard facts for entities.
- Abbreviated field names (`abrv`) → full words.
- `participants_flipped`, `rotation`, `ordering` → presentation hints;
  OpenBook derives side and order rather than copying a source's.
- Timestamp-based `since` → sequence cursor.
- Three price formats on the wire → decimal canonical, others optional.

## Pinnacle / PS3838 Lines API

- `since` is an **opaque server-issued value** returned with every response
  and handed back on the next call; unchanged periods are omitted, so
  consumers merge, never replace. The template for OpenBook's `since`.
- Period numbers per sport (416 across 62 sports) — evidence that segment
  numbering cannot be shared across vendors without a normalising family.
- `settlementId` changes on every re-settle: a re-grade is a new record, never
  a mutation. Adopted for settlements.
- Team1/Team2 with a per-league `homeTeamType` — evidence that home/away must
  be a derived fixture role, not a participant property.

## Betfair Exchange API and streaming

- The only openly documented end-to-end selection model:
  EventType → Competition → Event → Market → Runner (`selectionId` +
  `handicap`).
- Streaming: **initial image on subscribe, then sequenced deltas**. Adopted as
  OpenBook's change-delivery shape.
- Periods modelled as separate markets ("First Half Goals") — the opposite of
  Sportradar's specifier approach; OpenBook takes the middle path of a
  first-class segment.

## Sportradar Unified Odds Feed

- URN ids (`sr:match:8412480`) — the model for OpenBook's namespaced ids.
- Numeric market ids + **specifiers** (`total=2.5`, `quarternr=3`) — the one
  public market taxonomy; proprietary. OpenBook's market vocabulary is the open
  counterpart, with the segment as its own object rather than a specifier.
- `market_mapping` back to legacy feeds — a vendor standardising itself; the
  precedent for treating mapping as first-class.

## GTFS / GTFS-Realtime

- Static reference feed + realtime layer keyed to the same ids; many agencies
  per feed (`agency_id`); publisher-agnostic. The structural template.
- Realtime re-sends the full state every poll — OpenBook improves on this with
  sequenced diffs.
