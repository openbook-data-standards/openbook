# Protocol comparison — technical specs, and what fits OpenBook

A working review of the live-data and market-data protocols OpenBook is
shaped after, plus the highly regarded ones it cites but had not compared at
spec level. Betting-vendor APIs stay in [`industry-patterns.md`](industry-patterns.md).
This page is the technology comparison: encoding, identity, diffs,
recovery, topics, money, versioning, and governance.

Status: documentation only. Nothing here reopens a decided Q. Where a
foreign idea fits and is already on the wire, the decision is named. Where it
fits later (optional encoding, ops extras), it is marked **later**. Where it
does not fit, the reason is the OpenBook job: **one shared publication format**,
not a session protocol, not a committee repository, not an auction.

---

## 1. OpenBook, in one paragraph

Two tiers (GTFS split). Publisher-own entity ids plus mandatory standard
facts (Q2). Shared, readable vocabularies for sports, market types, segments,
sides (Q4/Q5). Every object carries `sequence` and `dateModified`. Changes are
JSON Merge Patch (RFC 7386). Push is described in AsyncAPI; MQTT is not
required. Pull is `since=<sequence>` and HTTP 410 + RFC 9457 when the cursor is
older than retention. Odds are decimal strings; money is `{amount}` in a
feed-level `baseCurrency`. Governance is open spec / closed engines (OpenRTB
/ FIX / GTFS). JSON Schema 2020-12 is machine-normative; within a frozen
major, compatibility is FULL-TRANSITIVE (Q32).

The rest of this page asks of each protocol: what it is technically, and
which pieces of that belong in that paragraph.

---

## 2. Fit at a glance

Verdicts: **adopted** (on the wire or in the spec), **shape only** (we took
the idea, not the encoding), **later** (optional, after 1.0), **rejected**.

### Structural templates (catalog + live)

- **GTFS / GTFS-Realtime** — **adopted** as the two-tier split and
  publisher-agnostic feed. Rejected: protobuf as v1 encoding (Q57); full-state
  re-send every poll; POSIX epoch times as the only clock.
- **GBFS 3.0** — **adopted** for ops: `ttl`, one discovery URL, co-serve
  versions (Q41/Q48/Q49). Rejected: nested `data` wrapper, snake_case, a
  required file-name enum for every feed.

### Live pub/sub

- **MQTT 5.0 / 3.1.1 (ISO/IEC 20922)** — **shape only**. QoS 0/1/2 and `+` /
  `#` wildcards are the delivery vocabulary (Q33). MQTT is not required.
- **WMO WIS 2.0** — **adopted** for topic grammar rules (lowercase, dashes, no
  dots, versioned levels) and the UN-scale pub/sub precedent (Q14/Q29).
  Rejected: notification-as-link-to-blob as the only payload; GeoJSON as the
  envelope.
- **AsyncAPI 3.0** — **adopted** for the push description (Q42).
- **CloudEvents 1.0** — **rejected** (Q52). OpenBook’s envelope is the message.

### Financial / market-data messaging

- **FIX (incl. 5.0 SP2 market data, session T11)** — **shape only**.
  Incremental New/Change/Delete, sequence, heartbeat, open spec / private
  engines. Rejected: tag=value or SBE as the v1 encoding; client TestRequest
  pair (Q46); a required session layer.
- **ISO 20022** — **rejected as the wire**. Useful as a reminder that money,
  identity and syntax should be separable. Does not fit as OpenBook’s
  encoding, naming, or governance.
- **OpenRTB 2.6** — **adopted** as the governance precedent (open spec,
  private engines, JSON, skip-unknown `ext`). Rejected: request/response
  auction, numeric enumerations, JSON numbers for money.

### Betting production feeds

- **Betfair Exchange Stream** — **adopted** as initial image + sequenced
  deltas, `heartbeatMs`, honest conflation. Named on the wire as
  `snapshotComplete`, `heartbeat`, `conflated` (Q46/Q47). Rejected: opaque
  `clk` tokens instead of an integer `sequence`; inferring caught-up.
- **Pinnacle / PS3838** — **adopted** for opaque-server `since` (as a
  sequence, not a time) and re-grade-as-new-id. Rejected: Team1/Team2 as
  identity; three price formats on the wire.
- **Sportradar UOF** — **shape only**. URN-style ids, mapping as first-class,
  `odds/change` as the price verb, `snapshot_complete` as the caught-up
  marker. Rejected: numeric market ids + specifiers as the open taxonomy;
  timestamp recovery; AMQP as required transport; XML as the v1 encoding.
- **KIBL outbound** — **adopted** for the three families (reference /
  mapping / info), league `ruleset`, push/pull parity. Rejected: integer
  owner ids, timestamp `since`, three price formats.

### Governance, replication, names

- **OpenStreetMap / OsmChange** — **adopted** for id+version, create/modify/
  delete, replication sequence, Wikidata cross-refs, bottom-up vocabulary.
  Rejected: object-level re-send on modify (OpenBook is field-level Merge
  Patch).
- **OASIS CAP 1.2** — **adopted** for `msgType` / `references` on
  `market/update` (Q15).
- **Olympic Data Feed (ODF)** — **adopted** for person-name forms (Q11).
  Rejected: XML per-Games common codes as the shared id system.
- **Confluent Schema Registry FULL+TRANSITIVE** — **adopted** as the
  compatibility *idea*, adapted to JSON Schema instances (Q32). Rejected:
  Avro reader/writer resolution as the gate.
- **Unicode stability / ISO 3166 reuse of CS** — **adopted** as never-reuse
  (Q35).

### Explicitly not the job

- **JSON Patch (RFC 6902)** — rejected in favour of Merge Patch (Q8). Odds
  diffs are object-shaped; pointer ops would make the hot path unreadable.
- **FIX Simple Binary Encoding, GTFS protobuf, GRIB/BUFR** — **later** as
  an optional encoding. v1 stays readable JSON.
- **ISO 20022 XML/JSON repository, FpML, ITCH/OUCH, SIRI/NeTEx** —
  rejected as the publication format. Too heavy, too committee-bound, or
  too venue-specific. The lesson from GTFS beating SIRI is: a small feed
  that agencies can emit wins over a complete enterprise model.

---

## 3. GTFS / GTFS-Realtime

**What it is.** A static zip of CSV tables (agencies, routes, stops, trips,
stop_times) plus a realtime protobuf `FeedMessage`: header + repeated
`FeedEntity`, each of which is a `TripUpdate`, `VehiclePosition`, or `Alert`.
Ids in the realtime layer are the same strings as the static files. Header
`incrementality` is FULL or DIFFERENTIAL; in practice most agencies publish
FULL. Timestamps are POSIX. Entities can be `is_deleted`. Extensions occupy
protobuf field numbers 1000–1999.

**Tech that matches OpenBook.** Static catalog + live layer keyed to the
same ids. Many agencies in one feed (`agency_id` → OpenBook `source` on a
publisher). Publisher-agnostic: the spec does not care who produced the
timetable. Alerts are a first-class live object (OpenBook folded that into
`market/update` via CAP rather than a third payload type).

**What we improved on.** GTFS-RT’s common FULL poll re-sends the world.
OpenBook’s snapshot is compaction; afterwards only Merge Patch diffs move
(Q8/Q33). Epoch integers were considered and rejected for RFC 3339
everywhere (Q9). Protobuf is the right *later* encoding (GTFS itself
started as CSV); it is not v1.

**Fit.** This is the structural template. Keep citing it. Do not take the
protobuf or the poll-the-full-state habit.

---

## 4. GBFS 3.0

**What it is.** JSON files for shared mobility. Required auto-discovery
`gbfs.json`: `last_updated` (RFC 3339 as of 3.0), `ttl` (non-negative
seconds; 0 means always refresh), `version`, and `data.feeds[]` of
`{name, url}`. A publisher of several cities adds `manifest.json`.
`gbfs_versions.json` lists co-served versions. Near-realtime endpoints
should not be more than five minutes stale. Enums are lowercase. Ids are
printable ASCII.

**Tech that matches OpenBook.** Q41/Q48/Q49 are this, flattened and
camelCased: discovery is `{ lastUpdated, ttl, feeds: [{ name, url }] }`
with no nested `data` wrapper, because OpenBook is not a family of named
JSON files. Co-serve versions at distinct URLs or topics. `ttl` is integer
seconds.

**What we did not take.** GBFS `name` MUST be a spec-defined base file
(`system_information`, `station_status`, …). OpenBook discovery names are
publisher-chosen (`snapshot`, `stream`, `docs`) because there is no fixed
file set. `manifest.json` for multi-system operators is **later** if a
single organisation publishes several OpenBook publishers; today one
discovery URL is one publisher.

**Fit.** Ops layer, not the odds model. Already on the wire.

---

## 5. MQTT 5.0 and ISO/IEC 20922

**What it is.** ISO/IEC 20922:2016 is MQTT **3.1.1**. MQTT **5.0** is the
OASIS successor WIS2 also depends on. Shared across both: UTF-8 topic names
with `/` levels; `+` (one level) and `#` (rest); QoS 0 at-most-once, 1
at-least-once, 2 exactly-once; ordering per topic for a given QoS. MQTT 5
adds reason codes, session expiry, message expiry, topic aliases, shared
subscriptions, and a Will delay.

**Tech that matches OpenBook.** Topic grammar and QoS names. Q33 item 7
uses 0/1/2 as vocabulary on any transport. Q14/Q29 topics are legal MQTT
filters: `openbook/v1/acme-feeds/soccer/fixture/+/odds/change`.

**What we did not take.** Requiring MQTT. Session expiry as a substitute
for Level L retention. Message Expiry Interval as a substitute for `ttl`
(GBFS `ttl` is already on documents). `$SYS` topics. Shared subscriptions
as a spec feature (an operator concern).

**Fit.** Transport vocabulary, not the payload. WIS2 is the existence
proof that a UN body can run this over the public internet; OpenBook can
ride the same brokers without becoming an MQTT standard.

---

## 6. WMO WIS 2.0

**What it is.** Since 1 January 2025, WMO members publish **WIS2 Notification
Messages** (GeoJSON) on MQTT topics:

`origin / a / wis2 / <centre-id> / data|metadata / core|recommended / <discipline> / …`

Rules: lowercase, dash-separated words, no dots, unique per level; major
version letter (`a`) only on rename/removal. Global Brokers republish so a
consumer subscribes once. The MQTT body is usually a small notification with
a `links[]` `rel=canonical` HTTP URL; tiny payloads may be embedded.

**Tech that matches OpenBook.** Versioned topic grammar, wildcards, a
neutral broker, centre-id ≈ publisher-id. OpenBook’s fixture-first order is
the same idea with a different key (everything about one match under `#`).

**What we did not take.** Notification-then-HTTP-GET as the only live
shape — odds cannot tolerate that extra hop. GeoJSON. Data-policy levels
(`core` / `recommended`) as topic slots (OpenBook’s analogue is
`provenance` on the market, not a topic level).

**Fit.** Strongest live-tier precedent. Already used for Q14/Q29.

---

## 7. FIX Protocol

**What it is.** The open protocol for electronic trading. Application
messages (market data, orders, allocations) over a **session layer**:
`MsgSeqNum`, Heartbeat (type 0), TestRequest (type 1) which must be answered
with a Heartbeat carrying `TestReqID`, ResendRequest, SequenceReset /
GapFill, `PossDupFlag`. Market data has a snapshot/full-refresh message and
`MarketDataIncrementalRefresh` (type X): repeating group with
`MDUpdateAction` New / Change / Delete, `MDEntryID` (reusable after delete),
optional `MDEntryRefID` when the id changes. Encodings: classic tag=value,
FIXML, and **Simple Binary Encoding** (schema-driven, fixed layout, optional
fields for forward compatibility).

**Tech that matches OpenBook.**

- Incremental New/Change/Delete ↔ `create` / `update` / `delete` (and
  `change` for odds).
- Sequence + heartbeat as liveness, not as application data.
- Dedup and gap handling as a consumer duty — OpenBook names the dedup key
  `(publisher, sequence)` instead of a session.
- Open spec, proprietary matching engines — the governance slogan on the
  homepage.
- Decimal prices, ISO 4217, instrument identity separate from the quote.

**What we did not take, on purpose.**

- A **session**. OpenBook is a publication format. Q46 rejected FIX
  TestRequest as the heartbeat design: the publisher declares `heartbeatMs`
  and emits `action: heartbeat`; the client does not ping to force a reply.
- Tag=value and SBE as v1. Readable JSON is the GTFS lesson; SBE is in the
  same bucket as protobuf / GRIB: **later** optional encoding.
- `MDEntryID` reuse after delete. OpenBook never reassigns frozen ids (Q35);
  a deleted outcome is Merge Patch `null`, a new outcome is a new identity.
- Per-message currency and symbol blocks on the hot path (Q44: currency
  once per feed).

**Fit.** Cite FIX for incremental market data and for “open contract,
closed engine.” Do not become a FIX dialect. Sportsbook odds are a last-sale
tape with a catalog, not an order-entry session.

---

## 8. ISO 20022

**What it is.** A **metamodel** (ISO 20022-1) plus syntax bindings (XML in
part 4, ASN.1 in part 8, syntax-generation rules in part 9 including JSON).
Business components (Payment Instruction, Settlement Instruction, …) live
in a registered repository. JSON Schema 2020-12 generation is an active
2025 TSG/API SEG workstream; generated property names stay abbreviated (`amt`,
`Ccy`) to round-trip with XML. Amounts are an object of amount + currency.
Governance is a Registration Management Group, not gravity-play.

**Tech that looks tempting.** Syntax-agnostic model; JSON Schema 2020-12;
money as a typed object; versioned message definitions.

**Why it does not fit OpenBook’s wire.**

- OpenBook already chose JSON Schema 2020-12 **without** a separate abstract
  repository. The schemas in `schema/` *are* the model.
- Abbreviated names contradict Q13/Q38 (schema.org camelCase, full words).
- `{amt, Ccy}` on every amount contradicts Q44 (`baseCurrency` once;
  incremental messages do not repeat currency).
- Committee registration contradicts staged governance (gravity play now,
  consortium later). An ISO number is an outcome, not a starting move
  ([`GOVERNANCE.md`](../GOVERNANCE.md)).
- ISO 20022 is payment/securities *instructions*. OpenBook is a public
  market-data tape plus a sports catalog. Mapping odds into pacs/setr
  messages would be theatre.

**Fit.** Keep it on the “stands on” list as the warning: do not invent a
private money model, and do not confuse a metamodel committee with a feed
standard. Do not generate OpenBook from an ISO 20022 repository.

---

## 9. OpenRTB 2.6

**What it is.** IAB Tech Lab’s JSON bid request / bid response. Required
`BidRequest.id` + `imp[]`; each impression has `bidfloor` (JSON number, CPM)
and `bidfloorcur` (ISO 4217, default USD). Response `seatbid[].bid[]` with
`price` as a float. Unknown fields are ignored; `ext` is the official
extension object. HTTP 204 for no-bid. The spec is explicit that engines
behind the JSON stay private.

**Tech that matches OpenBook.** JSON as the interchange; ISO 4217;
ignore-unknown (Q37); `x_` / `ext` as the vendor hatch; CC-style open spec
with proprietary bidders. That last point is why the homepage groups
OpenRTB with FIX and GTFS.

**What we did not take.**

- Auction choreography. OpenBook is not a request for a quote; it is a
  signed tape of quotes a book already made.
- JSON numbers for money and prices. OpenBook uses decimal **strings** (Q39)
  because binary floats are how books lose pennies.
- Numeric enumerations (`mtype`, `nbr`). OpenBook’s vocabularies are
  readable slugs; adding a market type is not a breaking change (Q34).

**Fit.** Governance and extension policy. Not the message shape.

---

## 10. Betfair Exchange Stream

**What it is.** TLS socket / WebSocket. Subscribe, receive `ct=SUB_IMAGE`
(replace cache where `img=true`), then deltas. Opaque `initialClk` / `clk`
on every message including heartbeats; reconnect by sending them back for
`RESUB_DELTA`. `heartbeatMs` on the subscription; server heartbeats have
`ct=HEARTBEAT` and no data. `con=true` when ticks were folded. `conflateMs`
is a requested (and sometimes forced) rate.

**Tech that matches OpenBook.** This is Q8’s change-delivery template and
most of Q33/Q46/Q47: snapshot, then diffs; a caught-up marker
(`snapshotComplete`, not inferred); `heartbeat` on the same stream;
`conflated: true` when ticks were dropped; `heartbeatMs` on the publisher
record.

**What we changed.** Integer `sequence` instead of opaque `clk` (Pinnacle’s
cursor lesson, made sortable). Per-fixture ordering, not a global clock
`pt`. Merge Patch field diffs instead of Betfair’s runner-ladder arrays.
Caught-up is an explicit `action`, not “the SUB_IMAGE ended.”

**Fit.** Closest *betting* live wire. Already absorbed.

---

## 11. Sportradar Unified Odds Feed

**What it is.** AMQP feed plus HTTP recovery. Ids are URNs (`sr:match:8412480`).
Markets are a numeric id plus `specifiers` (`total=2.5|quarternr=3`);
identity is (market id + normal specifiers), not extended specifiers.
Recovery is HTTP `initiate_request` (optionally `after=<epoch ms>`); replayed
messages arrive on AMQP and end with XML `<snapshot_complete request_id=…>`.
`odds_change` is the price message. A `market_mapping` layer points at legacy
feeds. Producers (`liveodds`, `pre`, …) are separate products.

**Tech that matches OpenBook.** Namespaced ids (Q5 short form
`sport:soccer`, formal `urn:openbook:sport:soccer`). Mapping as a
first-class idea (Q6 `identifier`). `odds/change` as the reserved price
action (Q16). `snapshotComplete` as the recovery terminator (Q46; Sportradar
snake_case, OpenBook camelCase). Separate recovery from the live socket.

**What we did not take.** Numeric market tables — unreadable, proprietary,
the thing an *open* vocabulary exists to replace. Specifiers that smuggle
segment and line into a string; OpenBook makes `segment` and `line` fields
on the market. Timestamp `after=` recovery (Q9 / `since` as sequence).
Required AMQP. XML.

**Fit.** The public betting taxonomy to study, not to copy. OpenBook’s
market vocabulary is the open counterpart, with segment as its own object.

---

## 12. Pinnacle / PS3838 and KIBL

Covered as APIs in [`industry-patterns.md`](industry-patterns.md). The
protocol-level takeaways:

- **Pinnacle `since`** — server-issued, opaque, handed back; unchanged rows
  omitted. OpenBook keeps the contract and makes the value a monotonic
  integer so consumers can reason about gaps (Q33).
- **Pinnacle `settlementId`** — changes on every re-settle. OpenBook `grade`
  is immutable; a correction is `grade/delete` + `grade/create` with
  `supersedes` (Q31).
- **Pinnacle Team1/Team2 + `homeTeamType`** — proof that home/away is a
  fixture role, not a participant property (Q22).
- **KIBL three families** — `/reference`, `/mapping`, `/info` is OpenBook’s
  vocab / `identifier` / live split in production. League `ruleset` (clock,
  segments, ties) is `league.ruleset`. Push/pull parity via `routing_key` is
  “topic and payload say the same thing” (§8).

---

## 13. OpenStreetMap, CAP, ODF, Confluent

**OsmChange.** `<create>` / `<modify>` / `<delete>` plus `id`, `version`,
`changeset`, and a replication sequence. Planet-scale diffs since 2012.
OpenBook’s object/action set is this, with Merge Patch instead of
re-sending the whole element. Wikidata tags are Q12.

**CAP 1.2.** `msgType` Alert / Update / Cancel / Ack / Error and `references`
to the message being amended. OpenBook uses `alert` · `update` · `cancel`
on `market/update` (Q15). Ack/Error stay out: those are session, not
publication.

**ODF.** Per-Games XML with `CompetitionCode`, `DocumentCode` (RSC),
`DocumentType` (`DT_SCHEDULE`, `DT_PARTIC`, …), `Version`, `ModificationIndicator`.
Person names: `PrintName`, `TVName`, `LocalFamilyName` / `LocalGivenName`.
OpenBook took the name *forms* (Q11) and refused the common-code tables as
the shared id (Wikidata + publisher-own + standard facts instead). ODF is
the right model for a single organiser’s Games; it is the wrong model for
every book on earth.

**Confluent FULL+TRANSITIVE.** Every schema in a subject is compatible with
all others in both directions. OpenBook Q32 is that idea on JSON *instances*:
minors only add optional fields; the required set is frozen. There is no
Avro resolution. Schema-diff CI is a later PR at 1.0+ (Q55).

---

## 14. Encodings OpenBook considered and parked

- **RFC 7386 Merge Patch** — adopted (Q8). Absent = unchanged, `null` =
  tombstone. Arrays replace wholesale, which is why odds diffs are
  outcome-level objects, not a patched array of numbers.
- **RFC 6902 JSON Patch** — rejected. Pointer ops (`/outcomes/0/odds`) are
  brittle under reordering and unreadable on a tick.
- **CloudEvents** — rejected (Q52). Required `specversion`, `id`, `source`,
  `type` duplicate `openbookVersion`, `sequence`, `publisher`,
  `object`/`action`. Wrapping would make every consumer depend on a second
  spec for no extra fact.
- **Protobuf / SBE / GRIB** — later optional binding (Q57), same path GTFS
  took. v1 JSON stays the source of truth; a binary encoding would be generated
  from the schemas, not a second model.
- **OpenAPI in this repo** — rejected (Q54). Pull shape is `since=` and 410;
  each publisher publishes their own OpenAPI. AsyncAPI for push stays.

---

## 15. What fits ours — the short list

Already absorbed, keep:

1. GTFS two-tier split and many-sources-per-feed.
2. GBFS discovery + `ttl` + co-served versions.
3. MQTT QoS names and wildcard topic grammar; WIS2 level rules.
4. Betfair image + deltas, heartbeat interval, honest conflation,
   explicit caught-up.
5. Pinnacle server cursor and immutable re-grade.
6. Sportradar URN-style ids, mapping records, `odds/change`,
   `snapshotComplete`.
7. KIBL reference / mapping / info and league ruleset.
8. OsmChange object/action + sequence; OSM/Wikidata cross-refs.
9. CAP `msgType` + `references` for market status.
10. ODF name forms; vCard/schema.org field names.
11. OpenRTB/FIX/GTFS open-spec closed-engine rule.
12. Confluent FULL-TRANSITIVE as instance compatibility; Unicode never-reuse.

Fits, but only **later** (do not put on the v1 wire):

- A generated protobuf or SBE binding of the same schemas.
- GBFS-style `manifest` if one operator publishes many publishers.
- MQTT 5 reason codes as an *equivalent* when the transport is MQTT
  (already allowed: “other transports MUST name the equivalent” of QoS).

Does **not** fit — do not reopen:

- CloudEvents wrap (Q52).
- DNS-style third id spelling (Q53).
- In-repo OpenAPI as the pull standard (Q54).
- ISO 20022 as the model or the JSON naming.
- FIX session / TestRequest.
- JSON numbers for odds or money.
- Timestamp cursors.
- Numeric market-type tables with specifier strings.
- A central entity registry (Q2 rejected option b).

---

## Sources

- GTFS-Realtime reference and proto — https://gtfs.org/documentation/realtime/reference/ · https://gtfs.org/documentation/realtime/proto/
- GBFS 3.0 — https://gbfs.org/documentation/reference/ · https://github.com/MobilityData/gbfs/blob/v3.0/gbfs.md
- MQTT 5.0 — https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html · ISO/IEC 20922:2016 = MQTT 3.1.1
- WIS2 topic hierarchy — https://wmo-im.github.io/wis2-topic-hierarchy/standard/wis2-topic-hierarchy-STABLE.html
- FIX 5.0 SP2 MarketDataIncrementalRefresh — https://fiximate.fixtrading.org/ · SBE — https://github.com/FIXTradingCommunity/fix-simple-binary-encoding
- ISO 20022 APIs — https://www.iso20022.org/about-iso-20022/apis-and-iso-20022
- OpenRTB 2.6 — https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md
- Betfair Exchange Stream — https://betfair-developer-docs.atlassian.net/wiki/spaces/1smk3cen4v3lu3yomq5qye0ni/pages/2687396/Exchange+Stream+API
- Sportradar UOF recovery and specifiers — https://docs.sportradar.com/uof/
- ODF General Messages — https://odf.olympictech.org/
- RFC 7386, RFC 6902, RFC 9457, RFC 8141 — https://www.rfc-editor.org
- CloudEvents 1.0 — https://github.com/cloudevents/spec
