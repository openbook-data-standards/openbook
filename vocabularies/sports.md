# OpenBook controlled vocabulary — sports

Version `0.1.0-draft`. Each entry is a canonical `sport:*` id and its display
name. Human map: [`../docs/taxonomy.md`](../docs/taxonomy.md). Additions go
through the process in [`../CONTRIBUTING.md`](../CONTRIBUTING.md);
ids are stable and never re-pointed once published.

| Id | Name |
| --- | --- |
| `sport:soccer` | Soccer |
| `sport:basketball` | Basketball |
| `sport:baseball` | Baseball |
| `sport:american-football` | American Football |
| `sport:ice-hockey` | Ice Hockey |
| `sport:tennis` | Tennis |
| `sport:golf` | Golf |
| `sport:mma` | Mixed Martial Arts |
| `sport:boxing` | Boxing |
| `sport:cricket` | Cricket |
| `sport:rugby-union` | Rugby Union |
| `sport:rugby-league` | Rugby League |
| `sport:volleyball` | Volleyball |
| `sport:table-tennis` | Table Tennis |
| `sport:esports` | Esports |
| `sport:athletics` | Athletics (track & field) |
| `sport:motorsport` | Motorsport |
| `sport:unknown` | Catch-all when the sport is not in this list (Q34). Publishers SHOULD use this rather than inventing an id. Consumers MUST still accept unrecognised `sport:*` values. |

## Disciplines (sub-sport granularity)

Some sports carry disciplines beneath them. Athletics is the worked example —
the point is that OpenBook names them readably, where a source like the Olympic
Data Feed uses opaque codes (`ATH`, `ATM012`):

| Id | Event |
| --- | --- |
| `athletics:100m` | 100 metres |
| `athletics:110m-hurdles` | 110 metre hurdles |
| `athletics:long-jump` | Long jump |
| `athletics:high-jump` | High jump |
| `athletics:marathon` | Marathon |
| `athletics:decathlon` | Decathlon |
| `athletics:4x100m-relay` | 4 × 100 m relay |

A multi-sport Games (the Olympics) is a **competition**, not a sport:
`league:athletics:INT:olympics` with a season per Games
(`season:league:athletics:INT:olympics:2024-paris`), and one league per sport
contested.
