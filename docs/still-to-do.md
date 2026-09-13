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

### Not decided yet (walk these; do not invent)

1. **Odds envelope** — team totals; draw price on 1X2; period status and
   cutoff as Pinnacle uses them on the odds call (vs fixture `eventStatus`).
2. **Specials** — special fixtures + special odds (contestants, category,
   units). Map to existing market/outright or a new object only after a
   question.
3. **Parlay / teaser flags on the event** — whether the event may be
   parlayed, same-event parlay period list, alternative teaser points.
4. **Live pairing** — liveStatus 0/1/2 and parent id vs what we already
   do with `superEvent`. Confirm, do not add a second model.
5. **Settled fixtures** — period settlement statuses (settled, re-settled,
   cancelled, deleted) vs grade delete/create.
6. **Sports catalog** — all sports Pinnacle lists, as OpenBook sport ids
   (vocab), not extra fixture keys.
7. **Get Line** — exact limit for one bet. OpenBook already has market
   `limit`; confirm that is enough.

### Not in the Pinnacle Lines fixture schema

Racing stall, cricket toss, and playoff series state are **not** on
Pinnacle’s documented fixture. They stay parked (**Q86**) until a real
payload has them. Do not add them to cover “all sports.”

## Later PRs (decided, not built)

- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Next question (not decided)

- First gap in the walk: team totals / draw price / specials (pick one).

## Done (Q32–Q88)

Q32–Q55 · **Q11** names · catalog place/league/`gender`/`ageGroup`/`surface`/`seed` · **Q88** `throws`/`bats` · **Q80** `lineup`.
