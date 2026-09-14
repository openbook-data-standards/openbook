# Join-key corpus case

Source document: [`../examples/fixture.example.json`](../examples/fixture.example.json).

Birth facts on that document:

- sport id `sport:soccer`
- league anchor `https://www.wikidata.org/entity/Q9448`
- start to the minute UTC `2026-09-19T14:00Z`
- participant anchors in `order`: `https://www.wikidata.org/entity/Q9617`, then `https://www.wikidata.org/entity/Q50602`
- `competitionType` `league`

Expected join key:

```
v1|sport:soccer|https://www.wikidata.org/entity/Q9448|2026-09-19T14:00Z|https://www.wikidata.org/entity/Q9617,https://www.wikidata.org/entity/Q50602|league
```

`tools/validate.py` recomputes the key from the example and checks this
block.
