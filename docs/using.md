# Using OpenBook

OpenBook is a **data contract**, not a library. You emit JSON that matches the
schemas, or you consume that JSON. This page is the short path; the
normative rules are in [`../spec/openbook.md`](../spec/openbook.md).

## 1. Read the contract

- Spec — [`spec.html`](../spec.html) (`spec/openbook.md`)
- Vocabularies — sports, market types, segments
- Schemas and worked examples — [`schemas.html`](../schemas.html)
- Push topics — [`../spec/asyncapi.yaml`](../spec/asyncapi.yaml)

## 2. Check documents

From a clone of this repository:

```bash
pip install 'jsonschema>=4.18' referencing
python3 tools/validate.py
python3 tools/validate.py --topic openbook/v1/acme-feeds/soccer/fixture/EVT-88213/odds/change
```

Exit code 0 means the **repo** is conformant (schemas, examples, topics, and
the Q50 name check). CI runs the same command. Pointing the runner at *your*
feed directory (`--examples <dir>`) is not built yet; until then, validate
your JSON against the files in [`../schema/`](../schema/) with any draft
2020-12 implementation.

## 3. Publish

1. Serve a **discovery** document
   ([`discovery.schema.json`](../schema/discovery.schema.json)):
   `{ lastUpdated, ttl, feeds: [{ name, url }] }`. Snapshot, stream, and any
   API docs you host are named feeds. The `publisher` object stays identity,
   not the catalog.
2. Put **`heartbeatMs`** on the publisher record (Level L). Optional **`ttl`**
   may sit there too; discovery is where `ttl` is required.
3. Name streams fixture-first:

   ```
   openbook/v1/<publisher>/<sport>/fixture/<id>/<object>/<action>
   ```

   `<action>` is the JSON enum token (`snapshotComplete` is camelCase on
   topic and payload).
4. Every message is one envelope: `openbookVersion`, `sequence`,
   `datePublished`, `publisher`, `object`, `action`, `sport`, `changes`
   (JSON Merge Patch). Control actions `snapshotComplete` and `heartbeat`
   carry `changes: {}`.
5. After snapshot + replay on push, emit `snapshotComplete`. Pull has no
   marker; the HTTP body *is* the batch.
6. Keep sending `heartbeat` on that stream. Quiet longer than `heartbeatMs`,
   the consumer SHOULD treat the feed as down.
7. If you skip ticks, that change carries `conflated: true`. Sequence still
   increases.
8. Pull `since=<sequence>`. If `since` is older than retention `R`, respond
   HTTP **410** with RFC 9457 Problem Details pointing at the snapshot URL —
   not a silent full snapshot.

Worked messages live in [`../examples/`](../examples/) (`heartbeat`,
`snapshot_complete`, `discovery`, `odds_change_conflated`).

## 4. Consume

- Merge `changes` per RFC 7386 (absent = unchanged, `null` = removed).
- Ignore unrecognised **fields** (Q37) and unrecognised growable **values**
  (Q34).
- Dedup on `(publisher, sequence)`.
- Honour `conflated`. After `heartbeatMs` of silence, treat the stream as
  down.
- On pull **410**, fetch the snapshot URL from the Problem Details body, then
  resume with `since`.

## 5. Conformance

A publisher or consumer is OpenBook-conformant when it accepts every **valid**
case and rejects every **invalid** case in
[`../conformance/`](../conformance/) (Q40). `tools/validate.py` is one runner,
not a language oracle. Freezing **1.0** still needs two independent
implementations, neither of which is that runner (Q41).
