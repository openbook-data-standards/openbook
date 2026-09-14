# OpenBook controlled vocabulary — market types

Version `0.1.0-draft`. **This is the core contribution of OpenBook** — the
cross-vendor market taxonomy that does not exist anywhere else today. Each entry
is a canonical `market:*` id, its shape, and the sides its outcomes take.
Segments (`1st-half`, `inning-1`, …) are applied separately via
`reference_segment`, not baked into the market id.

For what these words mean without ids, see
[`../docs/taxonomy.md`](../docs/taxonomy.md).

## Main lines

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:moneyline` | Moneyline | binary/n-way | home, away, (draw) |
| `market:spread` | Point Spread / Handicap | handicap | home, away |
| `market:total` | Total (Over/Under) | over-under | over, under |
| `market:team-total` | Team Total | over-under | over, under (per participant) |
| `market:draw-no-bet` | Draw No Bet | binary | home, away |
| `market:double-chance` | Double Chance | n-way | home-or-draw, away-or-draw, home-or-away |

## Score props

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:correct-score` | Correct Score | correct-score | participant |
| `market:both-teams-to-score` | Both Teams To Score | yes-no | yes, no |
| `market:odd-even-total` | Total Odd/Even | yes-no | odd, even |
| `market:winning-margin` | Winning Margin | n-way | participant |
| `market:race-to` | Race To (N points) | binary | home, away |

## Game props

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:first-to-score` | First To Score | n-way | home, away, none |
| `market:will-there-be-overtime` | Overtime Yes/No | yes-no | yes, no |
| `market:half-time-full-time` | Half-Time/Full-Time | n-way | participant |

## Player props

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:player-points` | Player Points | over-under | over, under |
| `market:player-assists` | Player Assists | over-under | over, under |
| `market:player-rebounds` | Player Rebounds | over-under | over, under |
| `market:player-anytime-scorer` | Anytime Scorer | yes-no | yes, no |
| `market:player-passing-yards` | Passing Yards | over-under | over, under |
| `market:player-shots-on-target` | Shots On Target | over-under | over, under |

## Outrights

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:outright-winner` | Tournament / Outright Winner | n-way | participant |
| `market:to-make-final` | To Reach The Final | yes-no | yes, no |
| `market:group-winner` | Group Winner | n-way | participant |

## Combinations

| Id | Name | Shape | Sides |
| --- | --- | --- | --- |
| `market:same-game-parlay` | Same-Game Parlay | composite | references other market outcomes |
| `market:parlay` | Parlay / Accumulator | composite | cross-fixture legs |
| `market:unknown` | Catch-all (Q34) | — | Consumers MUST accept unrecognised `market:*` values |

---

### Notes

- **Shape** drives how a client renders and how a settlement grades — a
  `handicap` market always has a `line`; an `over-under` always has `over`/`under`
  outcomes and a `line`; `n-way` enumerates `participant` outcomes.
- A concrete priced selection is identified by
  `(fixture, marketType, segment, line, side, basis)` — see the odds_change
  schema. `basis` is what the market counts (goals, corners); it is not a new
  `market:*` id.
- This list is deliberately small in v0.1. It grows through
  [`../CONTRIBUTING.md`](../CONTRIBUTING.md), with stable ids.
