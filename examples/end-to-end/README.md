# End-to-end: one synthetic fixture, publisher to consumer

This directory proves the ecosystem pieces compose. It uses only synthetic
documents already shipped in this repository — no provider account, no live
feed, no services. Each stage maps to the public tool that owns it:

```text
openbook-starter          openbook-translate            any consumer
─────────────────         ─────────────────────         ─────────────
publisher.json            adapter emits a change        merge_patch() +
discovery.json            envelope (RFC 7386 patch)     schema validation
snapshot.json  ────────►  over a stream/topic  ──────►  updated document
       (this walkthrough uses the repo's shipped examples at each seam)
```

## Run it

```sh
pip install 'jsonschema>=4.18' referencing
python3 examples/end-to-end/walkthrough.py
```

Expected output:

```text
envelope ok: fixture/update seq=104902 id=EVT-88213
patched fixture ok: startDate 2026-09-19T14:00:00Z -> 2026-09-19T14:15:00Z
extension preserved: x_reason='kick-off delayed 15 minutes'
```

## The three seams

1. **Publish — [openbook-starter](https://github.com/openbook-data-standards/openbook-starter).**
   `openbook start` writes `publisher.json`, `discovery.json` and an initial
   `snapshot.json`. The starter scaffolds documents; it does not host a feed.
   In this walkthrough, [`../fixture.example.json`](../fixture.example.json)
   plays the role of snapshot state a consumer already holds.

2. **Translate — [openbook-translate](https://github.com/openbook-data-standards/openbook-translate).**
   A provider adapter maps vendor records to canonical documents and emits
   change envelopes (`change_envelope`, `merge_patch` helpers; the synthetic
   `acme` adapter is the reference implementer). Here
   [`../fixture_update.example.json`](../fixture_update.example.json) is the
   envelope on the wire: `object=fixture`, `action=update`, `changes` an
   RFC 7386 Merge Patch.

3. **Consume — any conformant reader.** Apply `changes` to the held document,
   re-validate against `schema/fixture.schema.json`. `x_` extension fields
   flow through untouched. For JavaScript consumers this is what
   [openbook-js](https://github.com/openbook-data-standards/openbook-js)
   `OpenBookClient` + document cache does; the demo uses plain Python so it
   runs without any published package.

## What this does and does not prove

- Proves: snapshot + envelope → valid updated document, extension fields
  preserved, ids and sequences agree across the seam.
- Does not prove: a hosted feed, sequencing under loss/replay, provider
  mapping correctness, or the JS packages' public availability (that is
  named blocker ONB-001 in `docs/ecosystem.json`).
