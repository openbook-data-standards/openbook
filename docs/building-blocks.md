# Building blocks — the widely used standards OpenBook stands on

OpenBook reinvents nothing that already has a real standard. This is the list,
grouped by what each one is used for, with the reason it was chosen.

## Reference data: countries, names, languages, money, time

- **Unicode CLDR territories** — the territory model (decision Q10). ISO
  3166-1 alpha-2 codes underneath (`GB`, `US`), ISO 3166-2 subdivisions for
  sub-national teams (`GB-ENG`, `GB-SCT`, `GB-WLS`, `GB-NIR`, `US-PR`), the
  pragmatic extras (`XK` Kosovo, `EU`, `UN`), and localized territory names in
  every language — what every OS and browser uses. Sport-body codes ride
  alongside as crosswalks: **IOC** (`GBR`, `TPE`), **FIFA** (`ENG`, `SCO`),
  plus a **Wikidata** QID.
- **ISO 639-1** — language codes for per-language name variants (`en`, `es`).
- **ISO 4217** — `baseCurrency` once on the publisher / feed (Q44). Money
  on that feed is `{amount}` in that code; incremental messages do not
  repeat currency. ISO 20022 is not the OpenBook encoding (Q92).
- **ISO 8601 / RFC 3339** — every timestamp, with an explicit offset
  (`2026-09-19T14:00:00Z`). RFC 3339 is the strict internet profile of ISO 8601
  and is what parsers actually implement. See decision Q9.
- **IANA time-zone database** — venue-local time names (`Europe/London`) where
  display needs them; never used in place of an offset on the wire.
- **Unicode / UTF-8** — all text. Names keep their diacritics.
- **ISO 9 (Cyrillic) / ISO 843 (Greek)** — how to transliterate when matching
  or sorting; the wire field is `nameLatin` (Q11 / Q57).

## Neutral identifiers for entities

- **Wikidata QIDs** — the most widely used free, neutral identifiers for
  teams, players, leagues and venues (`Q9617` = Arsenal F.C.; resolvable at
  `https://www.wikidata.org/entity/Q9617`). Recommended external id. See Q12.
- **GeoNames** ids — places (cities, venues' locations) when a publisher has
  them.
- **schema.org** `SportsEvent` / `SportsTeam` / `SportsOrganization` /
  `Person` — the sports vocabulary Google structured data uses. OpenBook
  aligns field names with it where it can (`homeTeam`, `awayTeam`,
  `startDate`, `location`, `alternateName`). See Q13.

## Identifiers and schemas

- **RFC 8141 (URN)** — the formal spelling of every shared id:
  `urn:openbook:sport:soccer`; short form `sport:soccer` on the wire. Decision
  Q5.
- **RFC 9562 UUID v7** — recommended (not required) when a publisher mints
  fixture ids: time-ordered, globally unique, sorts by creation time.
- **JSON Schema (2020-12)** — the machine-normative definition of every object
  and message ([`../schema/`](../schema/)).
- **Semantic Versioning** — versioning of the standard
  ([`../VERSIONING.md`](../VERSIONING.md)).

## The wire

- **JSON** — the required v1 encoding (Q89). Additional encodings MAY exist
  later as optional bindings; this repo’s scaffolding stays JSON.
- **RFC 7386 JSON Merge Patch** — the semantics of every change message:
  absent = unchanged, `null` = removed. Decision Q8. JSON Patch (RFC 6902)
  is never an alternate (Q91).
- **OpenAPI 3.1** — a publisher who offers HTTP publishes **their own** pull
  docs; this repo does not ship `openapi.yaml` (Q54). Spec still names
  `since=` and HTTP 410. Discovery `kind` `docs` lists those URLs (Q56).
- **MCP (Model Context Protocol)** — a client/tooling surface, not a
  second sportsbook wire. Discovery `kind` `mcp` points at the server's
  own manifest (MCP Registry `server.json` / `/.well-known/mcp.json`).
  Connection, packages and remotes stay in that document (Q56).
- **Vendor mapping** — not this spec (Q96). Inbound books stay unknown;
  OpenBook is the output language. Planned separate Apache-2.0 packages
  (openbook-starter, openbook-translate). Native ids on a successful map
  use `identifier`. FHIR-style concept maps sit beside the resource, not
  inside it.
- **Agent Plugins** — optional plugin-directory format (`plugin.json` plus
  fixed component locations). Discovery `kind` `plugin` points at the
  manifest; OpenBook does not fork the layout (Q56).
- **AsyncAPI 3.0** — describes the push side (the change streams)
  ([`../spec/asyncapi.yaml`](../spec/asyncapi.yaml); Q42).
- **CloudEvents** — never (Q52). OpenBook's own change envelope is the
  message.
- **FIX session** — never (Q93). Recovery is Q33/Q46, not FIX Logon /
  TestRequest.
- **RFC 9457 Problem Details** — the error format for a stale `since`
  (HTTP 410) and other pull errors.
- **WIS2 topic hierarchy** (WMO) — the model for OpenBook's stream-naming grammar:
  fixed, versioned levels; lowercase, dash-separated, no dots. See Q14.
- **CAP 1.2** (OASIS Common Alerting Protocol) — the model for suspension /
  re-open / void messages: `msgType` Alert/Update/Cancel plus `references` to
  the message being amended. See Q15.
- **OsmChange** (OpenStreetMap replication diffs) — create/modify/delete with
  `id` + `version` and a replication sequence; the planet-scale precedent for
  diffs everywhere.
- **MQTT (ISO/IEC 20922)**, **Server-Sent Events**, **WebSocket**, **AMQP** —
  transports. OpenBook standardises the message, not the transport; any of
  these may carry it.

## The models OpenBook is shaped after

- **GTFS / GTFS-Realtime** — static reference layer + live changes keyed to it;
  publisher-agnostic; many agencies per feed. The structural template.
- **Betfair Exchange streaming** — initial image + sequenced deltas. The
  change-delivery template.
- **Pinnacle `since` cursor** — opaque server-issued delta cursor. The
  pull-delta template.
- **Sportradar UOF** — the one public betting market taxonomy; URN ids;
  specifiers; a mapping layer. Studied, borrowed from selectively.
- **OpenStreetMap** — bottom-up governed vocabulary; id + version on every
  object; minutely diffs; Wikidata cross-references. The governance and
  replication template.
- **WMO WIS 2.0** — a UN body running real-time MQTT pub/sub for 193 members
  since 2025, with a versioned topic grammar. The live-tier precedent.

## Sources

- ISO 3166-2:GB — https://en.wikipedia.org/wiki/ISO_3166-2:GB ·
  IOC / FIFA / ISO code comparison — https://simple.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes
- Wikidata: sports team `Q12973014`, sports venue `Q1076486`, property
  `P54` member of sports team — https://www.wikidata.org
- CloudEvents — https://github.com/cloudevents/spec · CNCF —
  https://www.cncf.io/projects/cloudevents/
- AsyncAPI — https://www.asyncapi.com · OpenAPI — https://spec.openapis.org
- MCP Registry `server.json` —
  https://github.com/modelcontextprotocol/registry · schema —
  https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json
- Agent Plugins — https://agent-plugins.org
- RFC 3339, RFC 7386, RFC 8141, RFC 9457, RFC 9562 — https://www.rfc-editor.org
- GTFS-Realtime — https://gtfs.org/documentation/realtime/reference/
- FIX Protocol — https://www.fixtrading.org/standards/ (not the OpenBook
  session; Q93)
- ISO 20022 — https://www.iso20022.org/ (not the OpenBook encoding; Q92)
- OpenRTB — https://iabtechlab.com/standards/openrtb/
- OsmChange — https://wiki.openstreetmap.org/wiki/OsmChange · Planet diffs —
  https://wiki.openstreetmap.org/wiki/Planet.osm/diffs
- WIS2 guide — https://wmo-im.github.io/wis2-guide/guide/wis2-guide-APPROVED.html ·
  topic hierarchy — https://wmo-im.github.io/wis2-topic-hierarchy/standard/wis2-topic-hierarchy-STABLE.html
- CAP 1.2 — https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html
