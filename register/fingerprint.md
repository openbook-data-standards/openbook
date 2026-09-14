# Fixture join recipe

Not on the odds wire. Not a new JSON field. Publisher-own fixture id
stays canonical. The join key is never the object id (Q171, Q196).

The recipe is for optional matching across publishers. A consumer MAY
compute it. A publisher MUST NOT put it on the odds wire.

## Inputs (birth facts)

Frozen at first publication:

- sport
- league anchor
- start to the minute UTC
- ordered participant anchors
- `competitionType`

## Encoding

UTF-8, no BOM. Five lines, each ended with LF (including the last). No
CR. No extra blank line.

1. Sport id (`sport.id`), for example `sport:soccer`.
2. League anchor: `league.sameAs` when that value is an `http://` or
   `https://` URL; otherwise `league.id`.
3. `startDate` truncated to the minute in UTC: `YYYY-MM-DDTHH:MMZ`.
   Seconds and fractions are dropped, not rounded. The pin uses a `Z`
   timestamp; consumers MUST normalise other offsets to UTC first.
4. Participant anchors in `order` order, comma-separated, no spaces.
   Each participant is `sameAs` when that value is an `http://` or
   `https://` URL; otherwise the participant `id`.
5. `league.competitionType`.

The join digest is SHA-256 of that byte string, lowercase hex (64
characters). That digest is the optional join key. It is not a JSON
field name.

## Pinned example

Checked against
[`../examples/fixture.example.json`](../examples/fixture.example.json)
(Q198, Q259). Preimage:

```
sport:soccer
https://www.wikidata.org/entity/Q9448
2026-09-19T14:00Z
https://www.wikidata.org/entity/Q9617,https://www.wikidata.org/entity/Q50602
league
```

SHA-256 (lowercase hex):

`2b38ee78a5c6da604719b19ad86a0a6dce7deb6995cc7d210548fc39377a752c`
