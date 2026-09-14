# Still to do

## Goal

**Cover the Pinnacle Lines API in OpenBook.** If Pinnacle publishes it on
that feed, OpenBook can carry it. This is a plan, not a wire change.

Source of truth: Pinnacle Lines OpenAPI (sports, leagues, fixtures, odds,
specials, settled). Not a sports encyclopedia. Not the Pinnacle Bets API
(placing tickets is out of scope: OpenBook is a publication format).

Walk the feed in this order. Each row is decided only when asked and
answered. Do not invent names.

## Pinnacle Lines API — coverage plan

### Already in OpenBook (spine)

- Sports, leagues, fixtures, participants, start time, cutoff
- One fixture; `eventStatus` is live (Q93). Not a second live id.
- Segments (Pinnacle period numbers map here; do not copy their integers)
- Markets and decimal odds; moneyline / spread / total
- Grade; what was graded on (Pinnacle resulting unit → existing `basis`)
- `since` cursor; snapshot then deltas
- Publisher, discovery, heartbeat, lineup
- Names, place, league gender, age group, surface, seed, throws/bats

### Decided on this walk (not wired unless named)

- **Q89** — Pinnacle specials are **markets**. No new object.
- **Q92** — no parlay/teaser flags on the fixture.
- **Q94** — keep `sport:*` ids; map vendor integers with `identifier` /
  `sameAs`. Do not dump Pinnacle `/sports`.
- **Q95** — market `limit` is enough; Get Line is out of scope.

### Wired on this walk

- **Q90** — optional `basis` on `market` and `odds/change`.
- **Q91** — spec prose only (four places; no new fields).
- **Q93** — one fixture; `eventStatus` is live. `superEvent` is not a
  live/pregame pair.

### Not decided yet (walk these; do not invent)

This Lines API walk is **closed**. Parked: **Q86** (stall / toss / series
until a payload). Later: **Q55** schema-diff CI at 1.0+.

### Not in the Pinnacle Lines fixture schema

Racing stall, cricket toss, and playoff series state are **not** on
Pinnacle’s documented fixture. They stay parked (**Q86**) until a real
payload has them. Do not add them to cover “all sports.”

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- This Lines walk is closed. Parked: **Q86**. Later: **Q55**.

## Done (Q32–Q95)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup` · **Q89** specials = markets · **Q90** market `basis` · **Q91** statuses and settled · **Q92** omit parlay flags · **Q93** one fixture · **Q94** `sport:*` ids · **Q95** Get Line out of scope.
