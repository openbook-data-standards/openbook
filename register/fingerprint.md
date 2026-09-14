# Fixture join recipe

Not on the odds wire. Not a new JSON field. Publisher-own fixture id
stays canonical. The join key is never the object id (Q171, Q196).

## What the recipe will use (already decided)

Birth facts frozen at first publication:

- sport
- league anchor
- start to the minute UTC
- ordered participant anchors
- `competitionType`

## What this file does not decide

How those facts are encoded, hashed, or joined into a string is **not
written yet** (Q216, Q260). Do not invent a hash, a separator, or a
field name.

## Pinned example

When those steps exist they are checked against
[`../examples/fixture.example.json`](../examples/fixture.example.json)
(Q198, Q259).
