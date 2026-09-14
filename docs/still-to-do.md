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
- Pregame vs live as separate fixtures; parent live event (`superEvent`)
- Segments (Pinnacle period numbers map here; do not copy their integers)
- Markets and decimal odds; moneyline / spread / total
- Grade; what was graded on (Pinnacle resulting unit → existing `basis`)
- `since` cursor; snapshot then deltas
- Publisher, discovery, heartbeat, lineup
- Names, place, league gender, age group, surface, seed, throws/bats

### Decided on this walk (not wired unless named)

- **Q89** — Pinnacle specials are **markets**. No new object.
- **Q90** — optional `basis` on every market (same `scoreUnit` list). Same
  `market:*` ids. Omit = sport/league `primaryUnit`. Not a new type.

### Not decided yet (walk these; do not invent)

1. **Odds envelope** — team totals and draw sides (vocab already has them);
   period status on the odds call vs fixture `eventStatus`.
2. **Parlay / teaser flags on the event** — whether the event may be
   parlayed, same-event parlay period list, alternative teaser points.
3. **Live pairing** — confirm `superEvent`; do not add a second model.
4. **Settled fixtures** — period settlement vs grade delete/create.
5. **Sports catalog** — Pinnacle’s sport list as OpenBook sport ids.
6. **Get Line** — confirm market `limit` is enough.

### Not in the Pinnacle Lines fixture schema

Racing stall, cricket toss, and playoff series state are **not** on
Pinnacle’s documented fixture. They stay parked (**Q86**) until a real
payload has them. Do not add them to cover “all sports.”

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- Odds envelope: team totals / draw sides, and period status vs `eventStatus`.

## Done (Q32–Q90)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup` · **Q89** specials = markets · **Q90** market `basis`.
