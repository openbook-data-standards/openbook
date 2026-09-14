# Betfair `marketType` → OpenBook market id

Public list: Betfair Exchange betting enums (`marketType` on a market
catalogue). Documentation: Betfair Exchange Stream API pages linked from
[`../docs/protocol-comparison.md`](../docs/protocol-comparison.md) §16.

The OpenBook market id does not encode the line or the segment. Map those
separately (`line`, `segment`).

| Betfair `marketType` | OpenBook | Reason |
| --- | --- | --- |
| `MATCH_ODDS` | `market:moneyline` | Who wins the segment. |
| `OVER_UNDER_05` | `market:total` | Line is 0.5, not in the id. |
| `OVER_UNDER_15` | `market:total` | Line is 1.5, not in the id. |
| `OVER_UNDER_25` | `market:total` | Line is 2.5, not in the id. |
| `ASIAN_HANDICAP` | `market:spread` | Handicap line is `line`. |
| `CORRECT_SCORE` | `market:correct-score` | Exact score rows. |
| `BOTH_TEAMS_TO_SCORE` | `market:both-teams-to-score` | Yes/no. |
| `DRAW_NO_BET` | `market:draw-no-bet` | Draw voids. |
| `DOUBLE_CHANCE` | `market:double-chance` | Two of three moneyline results. |
| `TEAM_A` | `market:unknown` | Not a market type; a selection / side. |
| `TEAM_B` | `market:unknown` | Not a market type; a selection / side. |
