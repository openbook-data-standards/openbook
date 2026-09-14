# Betfair soccer period labels → OpenBook segment id

Public list: Betfair Exchange soccer market catalogues describe periods
in English (first half, second half, match odds). Documentation: Betfair
Exchange Stream API pages linked from
[`../docs/protocol-comparison.md`](../docs/protocol-comparison.md) §16.

| Betfair label | OpenBook | Reason |
| --- | --- | --- |
| First Half | `segment:soccer:1st-half` | First period of regulation. |
| Second Half | `segment:soccer:2nd-half` | Second period of regulation. |
| Match Odds | `segment:soccer:full-time` | Contest as graded. |
| Extra Time | `segment:soccer:extra-time` | Whole extra-time period. |
| Penalties | `segment:soccer:penalties` | Penalty shoot-out. |
| Innings 1 | `segment:unknown:unknown` | Soccer catalogue; not a soccer period. |
