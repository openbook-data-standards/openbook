# OpenBook controlled vocabulary — positions

Version `0.3.0-draft`. A **position** is a roster slot on `player`. Ids are
`position:<sport>:<token>`; the formal form is
`urn:openbook:position:<sport>:<token>`. The schema field `position` stays a
string. This list is growable, not a closed enum.

Tokens are book-style bands (goalkeeper, defender), not a full formation
chart. Sports without a list here still use the field; unrecognised values
are tolerated (**Q34**). Individual sports (tennis, golf, fights) have no
rows beyond the catch-all.

Catch-all: `position:unknown:unknown`. Consumers MUST accept unrecognised
`position:*` values. Additions go through `CONTRIBUTING.md`; ids are stable
once published.

For what a position is in plain language, see
[`../docs/taxonomy.md`](../docs/taxonomy.md).

## Catch-all

| Id | Name | Description |
| --- | --- | --- |
| `position:unknown:unknown` | Unknown | Sport or slot is not in this list. Prefer this over inventing an id. |

## Soccer — `sport:soccer`

| Id | Name | Description |
| --- | --- | --- |
| `position:soccer:goalkeeper` | Goalkeeper | Last line; typically does not play as an outfield band. |
| `position:soccer:defender` | Defender | Back line, including full-backs and centre-backs. |
| `position:soccer:midfielder` | Midfielder | Middle band, including wide midfield. |
| `position:soccer:forward` | Forward | Attack band, including wingers priced as attackers. |

## Futsal — `sport:futsal`

| Id | Name | Description |
| --- | --- | --- |
| `position:futsal:goalkeeper` | Goalkeeper | Last line. |
| `position:futsal:defender` | Defender | Back line. |
| `position:futsal:midfielder` | Midfielder | Middle band. |
| `position:futsal:forward` | Forward | Attack band. |

## Basketball — `sport:basketball`

| Id | Name | Description |
| --- | --- | --- |
| `position:basketball:guard` | Guard | Point and shooting guards as one band. |
| `position:basketball:forward` | Forward | Small and power forwards as one band. |
| `position:basketball:center` | Center | Centre. |

## Baseball — `sport:baseball`

| Id | Name | Description |
| --- | --- | --- |
| `position:baseball:pitcher` | Pitcher | Pitcher. |
| `position:baseball:catcher` | Catcher | Catcher. |
| `position:baseball:first-base` | First base | First base. |
| `position:baseball:second-base` | Second base | Second base. |
| `position:baseball:third-base` | Third base | Third base. |
| `position:baseball:shortstop` | Shortstop | Shortstop. |
| `position:baseball:left-field` | Left field | Left field. |
| `position:baseball:center-field` | Center field | Center field. |
| `position:baseball:right-field` | Right field | Right field. |
| `position:baseball:designated-hitter` | Designated hitter | Designated hitter. |

## American football — `sport:american-football`

| Id | Name | Description |
| --- | --- | --- |
| `position:american-football:quarterback` | Quarterback | Quarterback. |
| `position:american-football:running-back` | Running back | Running back, including fullback. |
| `position:american-football:wide-receiver` | Wide receiver | Wide receiver. |
| `position:american-football:tight-end` | Tight end | Tight end. |
| `position:american-football:offensive-line` | Offensive line | Tackle, guard, and centre as one band. |
| `position:american-football:defensive-line` | Defensive line | Defensive tackle and end as one band. |
| `position:american-football:linebacker` | Linebacker | Linebacker. |
| `position:american-football:defensive-back` | Defensive back | Corner and safety as one band. |
| `position:american-football:kicker` | Kicker | Place kicker. |
| `position:american-football:punter` | Punter | Punter. |

## Ice hockey — `sport:ice-hockey`

| Id | Name | Description |
| --- | --- | --- |
| `position:ice-hockey:goaltender` | Goaltender | Goaltender. |
| `position:ice-hockey:defenseman` | Defenseman | Defence pair. |
| `position:ice-hockey:forward` | Forward | Centre and wing as one band. |

## Cricket — `sport:cricket`

| Id | Name | Description |
| --- | --- | --- |
| `position:cricket:batter` | Batter | Specialist batter. |
| `position:cricket:bowler` | Bowler | Specialist bowler. |
| `position:cricket:wicket-keeper` | Wicket-keeper | Wicket-keeper. |
| `position:cricket:all-rounder` | All-rounder | Both batting and bowling as the listed role. |

## Rugby union — `sport:rugby-union`

| Id | Name | Description |
| --- | --- | --- |
| `position:rugby-union:forward` | Forward | Pack (1–8) as one band. |
| `position:rugby-union:back` | Back | Backs (9–15) as one band. |
| `position:rugby-union:scrum-half` | Scrum-half | Number 9 when listed separately. |
| `position:rugby-union:fly-half` | Fly-half | Number 10 when listed separately. |

## Rugby league — `sport:rugby-league`

| Id | Name | Description |
| --- | --- | --- |
| `position:rugby-league:forward` | Forward | Pack as one band. |
| `position:rugby-league:back` | Back | Backs as one band. |
| `position:rugby-league:hooker` | Hooker | Hooker when listed separately. |
| `position:rugby-league:halfback` | Halfback | Halfback when listed separately. |

## Australian rules — `sport:australian-rules`

| Id | Name | Description |
| --- | --- | --- |
| `position:australian-rules:defender` | Defender | Back line. |
| `position:australian-rules:midfielder` | Midfielder | Midfield, including wings. |
| `position:australian-rules:forward` | Forward | Attack. |
| `position:australian-rules:ruck` | Ruck | Ruck. |

## Handball — `sport:handball`

| Id | Name | Description |
| --- | --- | --- |
| `position:handball:goalkeeper` | Goalkeeper | Goalkeeper. |
| `position:handball:back` | Back | Left, right, and centre back as one band. |
| `position:handball:wing` | Wing | Wing. |
| `position:handball:pivot` | Pivot | Pivot / line player. |

## Field hockey — `sport:field-hockey`

| Id | Name | Description |
| --- | --- | --- |
| `position:field-hockey:goalkeeper` | Goalkeeper | Goalkeeper. |
| `position:field-hockey:defender` | Defender | Defence. |
| `position:field-hockey:midfielder` | Midfielder | Midfield. |
| `position:field-hockey:forward` | Forward | Attack. |

## Lacrosse — `sport:lacrosse`

| Id | Name | Description |
| --- | --- | --- |
| `position:lacrosse:goalkeeper` | Goalkeeper | Goalkeeper. |
| `position:lacrosse:defender` | Defender | Defence. |
| `position:lacrosse:midfielder` | Midfielder | Midfield. |
| `position:lacrosse:attacker` | Attacker | Attack. |
| `position:lacrosse:face-off` | Face-off | Face-off specialist when listed separately. |

## Water polo — `sport:water-polo`

| Id | Name | Description |
| --- | --- | --- |
| `position:water-polo:goalkeeper` | Goalkeeper | Goalkeeper. |
| `position:water-polo:field` | Field | Any outfield slot. |

## Volleyball — `sport:volleyball`

| Id | Name | Description |
| --- | --- | --- |
| `position:volleyball:setter` | Setter | Setter. |
| `position:volleyball:outside-hitter` | Outside hitter | Outside / left-side hitter. |
| `position:volleyball:middle-blocker` | Middle blocker | Middle blocker. |
| `position:volleyball:opposite` | Opposite | Opposite / right-side hitter. |
| `position:volleyball:libero` | Libero | Libero. |
