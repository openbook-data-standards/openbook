# Examples — one match, in order

This is the OpenBook equivalent of [GTFS's example feed](https://gtfs.org/getting-started/example-feed/):
worked documents that already live in [`../examples/`](../examples/), shown
in `sequence` order, which is the order a consumer would apply them. They
validate against the schemas. They are **not** a live sandbox.

The sample match is **Arsenal v Manchester City**, fixture `EVT-88213`,
19 September 2026. Publisher `acme-feeds` is fictional. Source names in the
sample (`acme-book`, `pinnacle`, `bigbook`) are **labels on prices**, not a
requirement to use those books. OpenBook is vendor-neutral.

Plain-language story: the [guide](guide.md). Rules: the
[specification](../spec/openbook.md). Raw dump of every file:
[schemas § examples](../schema/).

---

## 1. Find the feed

A publisher SHOULD offer one discovery URL. `ttl` is how long a consumer
may cache this list. Snapshot, stream, and docs are named feeds — not the
publisher object.

Source: [`discovery.example.json`](../examples/discovery.example.json)

<!-- include:examples/discovery.example.json -->

## 2. Who is transmitting

The publisher record is identity: name, currency, heartbeat bound, and the
**sources** this feed carries. One feed, three books in the sample
(`acme-book`, `pinnacle`, `bigbook`).

Source: [`publisher.example.json`](../examples/publisher.example.json)

<!-- include:examples/publisher.example.json -->

## 3. The fixture (the catalogue)

Standard facts: sport, league, start time, participants with `role` and
`order`, Wikidata `sameAs` when it exists. This is the printed list, not a
price tick. Sequence `104870`.

Source: [`fixture.example.json`](../examples/fixture.example.json)

<!-- include:examples/fixture.example.json -->

## 4. Prices move

`odds/change` carries only what moved. Sequence `104871` — the first live
tick after the fixture. Three sources in one message in this sample —
licensed, official, and observed — so a consumer can tell them apart. A
suspended spread is a status, not a zero price.

Source: [`odds_change.example.json`](../examples/odds_change.example.json)

<!-- include:examples/odds_change.example.json -->

## 5. A priced market, as a document

A market snapshot for one source (`bigbook`). `limit` is on the document;
later price-only ticks do not have to repeat it. Sequence `104880`.

Source: [`market.example.json`](../examples/market.example.json)

<!-- include:examples/market.example.json -->

## 6. Caught up, then quiet is bounded

After snapshot + replay, the stream says `snapshotComplete` (`104900`).
Heartbeats on the same stream (`104901`) mean “still here”; silence longer
than `heartbeatMs` is an alarm, not a feature.

Sources: [`snapshot_complete.example.json`](../examples/snapshot_complete.example.json),
[`heartbeat.example.json`](../examples/heartbeat.example.json)

<!-- include:examples/snapshot_complete.example.json -->

<!-- include:examples/heartbeat.example.json -->

## 7. Kick-off delayed

A fixture update is a Merge Patch: only the fields that changed. `x_` is a
vendor extra; consumers ignore unrecognised fields. Sequence `104902`.

Source: [`fixture_update.example.json`](../examples/fixture_update.example.json)

<!-- include:examples/fixture_update.example.json -->

## 8. A market comes back on

After a goal, the observed spread re-opens. `msgType` / `reason` /
`references` point at the earlier sequence. Taking a market off (or putting
it back) is `market/update`, not a sentinel odds value. Sequence `105330`.

Source: [`market_update.example.json`](../examples/market_update.example.json)

<!-- include:examples/market_update.example.json -->

## 9. The score

Live, second half, 67:00 on the broadcast clock. First half is **down**
(final, once). Goals and corners are separate score lines. Sequence `105410`.

Source: [`score.example.json`](../examples/score.example.json)

<!-- include:examples/score.example.json -->

## 10. A grade

Once a segment is down, the book grades a market against it. This grade is
first-half total 1.5: over wins, under loses. A correction is a new grade with
`supersedes`, never an edit. Sequence `106001`.

Source: [`grade.example.json`](../examples/grade.example.json)

<!-- include:examples/grade.example.json -->

---

## The rest of the corpus

These files are in [`../examples/`](../examples/) too. They are the valid
half of the conformance suite. Catalogue objects use earlier sequences than
the match stream above; the conflated tick sits between `104871` and `104880`.

| File | Sequence | What it is |
| --- | --- | --- |
| [`market_type.example.json`](../examples/market_type.example.json) | 103900 | A canonical market type (`shape: composite`) |
| [`participant.example.json`](../examples/participant.example.json) | 104000 | A team or individual as a catalogue object |
| [`stage.example.json`](../examples/stage.example.json) | 104010 | A named slice of a season |
| [`player.example.json`](../examples/player.example.json) | 104100 | Roster membership |
| [`stall.example.json`](../examples/stall.example.json) | 104110 | Racing gate (`order`) |
| [`toss.example.json`](../examples/toss.example.json) | 104120 | Who won the cricket toss; `elected` bat |
| [`odds_change_conflated.example.json`](../examples/odds_change_conflated.example.json) | 104872 | A tick that skipped intermediates (`conflated: true`) |
| [`lineup.example.json`](../examples/lineup.example.json) | 105500 | Starting `player` ids for one fixture |
| [`series.example.json`](../examples/series.example.json) | 105510 | Live series lead; round on `stage`; two `wins` rows; `needed` 4 |

Invalid cases (must be rejected) live in [`../conformance/invalid/`](../conformance/).
Run `python3 tools/validate.py`.
