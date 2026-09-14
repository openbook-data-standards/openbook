# Anchor policy

Not an OpenBook-run entity database (Q2, Q171). OpenBook mints no
player, team, or league ids. Publisher-own ids stay canonical.

## Wikidata

`sameAs` accepts Wikidata entity URLs. Required when a Wikidata entity
exists; `null` when it does not (spec §3.3).

## Community registers

`sameAs` MAY name **one** community register per sport when one exists.
This file does **not** list those registers. Do not invent that list
here.

## Out of scope here

- Fixture join encoding steps (see [`fingerprint.md`](fingerprint.md))
- Prefix tokens (see [`prefixes.json`](prefixes.json))
- Position token lists (still wait)
