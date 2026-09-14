# Fixture join key

Optional join key for one fixture (Q171). It is derived. It is not the
object `id`. The publisher-own `id` stays canonical. This recipe is not
a new field on the wire.

## Birth facts (frozen at first publication)

- `sport` id
- league anchor: `league.sameAs` when present, otherwise `league.id`
- `startDate` truncated to the minute in UTC
- participant anchors, in `order`: each row’s `sameAs` when present,
  otherwise that row’s `id`
- `league.competitionType`

## String

UTF-8, five fields after the version, separated by `|`:

`v1|{sport id}|{league anchor}|{start to the minute UTC}|{participant anchors comma-separated}|{competitionType}`

Start to the minute uses `YYYY-MM-DDTHH:MMZ` (UTC). Participant anchors
keep `order`. Do not include names, venues, or later score facts.

A worked case: [`corpus.md`](corpus.md).
