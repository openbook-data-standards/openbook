# Industry patterns — what public betting APIs do, and what OpenBook takes

A review of publicly documented sports-betting APIs, looking for patterns
worth adopting and patterns to avoid. Vendor-neutral: every API here is
public, and each is judged only on its design.

The technology comparison of GTFS, GBFS, MQTT, WIS2, FIX, ISO 20022,
OpenRTB, Betfair streaming, Sportradar UOF, OsmChange, CAP and ODF — specs,
not vendor APIs — is [`protocol-comparison.md`](protocol-comparison.md).

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

## Beyond betting — OpenStreetMap and the weather system

Two open data systems at planet scale that solved the same problems OpenBook
faces: a bottom-up vocabulary, diffs everywhere, and real-time pub/sub run by
a neutral body.

### OpenStreetMap

- **Three primitives + free key/value tags** (nodes, ways, relations). The tag
  vocabulary is **not fixed by a committee** — it is documented on a wiki,
  proposed and refined by the community, and enforced by validators. Lesson for
  the market-type vocabulary: a curated, documented core plus a sanctioned
  extension mechanism (OpenBook `x_` fields) beats trying to enumerate the world
  up front.
- **Every object carries `id` + `version`; every edit belongs to a
  `changeset`.** Version increments on each change — optimistic concurrency at
  planet scale. OpenBook's `sequence` + `dateModified` on every object is the same
  idea.
- **Minutely replication diffs** in the **OsmChange** format: `<create>`,
  `<modify>`, `<delete>` blocks; each element carries `id`, `version`,
  `changeset`; a `delete` needs only those three; a replication **state /
  sequence number** tells a consumer where it is. This is "diffs everywhere"
  running for the whole planet since 2012. One conscious difference: OsmChange
  `modify` re-sends the whole element (object-level); OpenBook sends only the
  changed fields (JSON Merge Patch).
- **`wikidata=Q…` tags** on map objects — the cross-reference-by-QID pattern
  OpenBook adopts for entities (decision Q12).
- Licence: **ODbL** (share-alike) for the *data*. Note the distinction OpenBook
  keeps: the *specification* is CC BY; each publisher's *data* licence is its
  own.

### The weather system (WMO, ICAO, OASIS)

- **WIS 2.0** — since 1 January 2025 the World Meteorological Organization's
  193 members exchange real-time data by **MQTT publish/subscribe over the
  public internet**, replacing a private-link network (GTS). Notifications are
  small messages carrying a link to the data (or a small embedded payload);
  **Global Brokers** re-publish every node's notifications so a consumer
  subscribes once. A UN body running a live pub/sub data standard is the
  strongest possible precedent for OpenBook's live tier.
- **WIS2 topic hierarchy** — a fixed, versioned topic grammar:
  `channel / version / system / centre-id / notification-type / data-policy /
  discipline / …`, e.g.
  `origin/a/wis2/ca-eccc-msc/data/core/weather/surface-based-observations/synop`.
  Rules: lowercase, dash-separated words, no dots, unique per level; a major
  version bump only on rename/removal, minor on additions. OpenBook should have
  the same kind of grammar for its streams (open decision Q14).
- **CAP 1.2 (OASIS Common Alerting Protocol)** — the alert message standard:
  `alert` → `info` → `area`/`resource`; `msgType` of Alert / Update / Cancel /
  Ack / Error; `urgency`, `severity`, `certainty`; and **`references` to the
  prior message an update or cancel applies to**. This is the right model for
  market suspensions, re-openings and voids (open decision Q15).
- **METAR / TAF** — terse fixed-vocabulary text read by humans and machines
  for decades, now paired with machine forms (IWXXM XML, JSON APIs). The
  dual-form idea OpenBook uses for ids (short slug on the wire, formal URN in
  the spec).
- **GRIB / BUFR** — binary, table-driven, self-describing formats for volume
  data. Efficient but need the tables. OpenBook stays readable JSON in v1; a
  binary encoding could become an optional transport binding later, as GTFS
  did with protobuf.
- **NWS API** — JSON-LD + GeoJSON payloads: web-standard encodings rather than
  bespoke ones.
