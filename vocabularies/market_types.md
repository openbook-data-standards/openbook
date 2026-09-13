# OpenBook controlled vocabulary — market types

Version `0.1.0-draft`. **This is the core contribution of OpenBook** — the
cross-vendor market taxonomy that does not exist anywhere else today. Each entry
is a canonical `market:*` id, its shape, and the sides its outcomes take.
Segments (`1st-half`, `inning-1`, …) are applied separately via
`reference_segment`, not baked into the market id.

Format: `market:<id>` — Name · shape · sides.

## Main lines

- `market:moneyline` — Moneyline · binary/n-way · home, away, (draw)
- `market:spread` — Point Spread / Handicap · handicap · home, away
- `market:total` — Total (Over/Under) · over-under · over, under
- `market:team-total` — Team Total · over-under · over, under (per participant)
- `market:draw-no-bet` — Draw No Bet · binary · home, away
- `market:double-chance` — Double Chance · n-way · home-or-draw, away-or-draw, home-or-away

## Score props

- `market:correct-score` — Correct Score · correct-score · participant
- `market:both-teams-to-score` — Both Teams To Score · yes-no · yes, no
- `market:odd-even-total` — Total Odd/Even · yes-no · odd, even
- `market:winning-margin` — Winning Margin · n-way · participant
- `market:race-to` — Race To (N points) · binary · home, away

## Game props

- `market:first-to-score` — First To Score · n-way · home, away, none
- `market:will-there-be-overtime` — Overtime Yes/No · yes-no · yes, no
- `market:half-time-full-time` — Half-Time/Full-Time · n-way · participant

## Player props

- `market:player-points` — Player Points · over-under · over, under
- `market:player-assists` — Player Assists · over-under · over, under
- `market:player-rebounds` — Player Rebounds · over-under · over, under
- `market:player-anytime-scorer` — Anytime Scorer · yes-no · yes, no
- `market:player-passing-yards` — Passing Yards · over-under · over, under
- `market:player-shots-on-target` — Shots On Target · over-under · over, under

## Outrights

- `market:outright-winner` — Tournament / Outright Winner · n-way · participant
- `market:to-make-final` — To Reach The Final · yes-no · yes, no
- `market:group-winner` — Group Winner · n-way · participant

## Combinations

- `market:same-game-parlay` — Same-Game Parlay · composite · (references other market outcomes)
- `market:parlay` — Parlay / Accumulator · composite · (cross-fixture legs)
- `market:unknown` — Catch-all when the market type is not in this list (Q34).
  Consumers MUST accept unrecognised `market:*` values.

---

### Notes

- **Shape** drives how a client renders and how a settlement grades — a
  `handicap` market always has a `line`; an `over-under` always has `over`/`under`
  outcomes and a `line`; `n-way` enumerates `participant` outcomes.
- A concrete priced selection is identified by
  `(fixture, market_type, segment, line, side)` — see the odds_change schema.
- This list is deliberately small in v0.1. It grows through
  [`../CONTRIBUTING.md`](../CONTRIBUTING.md), with stable ids.
