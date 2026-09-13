# OpenBook in plain language

This page is for people who need to **understand** OpenBook, not implement it.
No RFC keywords. No topic grammar. Those live in the
[specification](../spec/openbook.md).

The shared lists of sports, bet types, and match slices live in the
[taxonomy](taxonomy.md) — separate again, so you can talk about “what a total
is” without talking about JSON.

---

## What it is

OpenBook is a **shared way to write down sportsbook data** so that:

- a sportsbook can publish its own prices
- a feed can carry many books in one stream
- a consumer (trader, screen, researcher, regulator, another book) can read
  every publisher with **one** importer

It is only the data contract. How a book prices, models, or hedges stays
private. Think of a bus timetable standard: every agency publishes the same
*shape* of file; nobody has to reveal how they schedule the buses.

```mermaid
flowchart LR
  book[Sportsbook] --> feed[OpenBook feed]
  aggregator[Odds feed] --> feed
  feed --> trader[Trader]
  feed --> screen[Screen / TV]
  feed --> other[Another book]
```

Three roles:

| Role | Everyday meaning |
| --- | --- |
| Publisher | Whoever *transmits* the feed (a book, or a company that carries books) |
| Source | Whose odds a price actually is — every price names this |
| Consumer | Whoever *reads* feeds |

One feed may carry many sources, the way one transit file can list many bus
operators.

---

## Two layers, like a matchday board

| Layer | What it is | Sportsbook feel |
| --- | --- | --- |
| Catalogue | The durable facts: which league, which teams, which match, which kind of bet | The printed fixture list |
| Live wire | Only what *changed*: a price tick, a goal, a market coming off | The board that keeps updating |

You do not re-send the whole board every time Arsenal’s moneyline moves a
tick. You send the tick. If someone joins late, they get a **snapshot** (the
board as it stands) and then the ticks from that point on.

```mermaid
flowchart TB
  snap[Snapshot: the board as it is] --> replay[Catch-up ticks]
  replay --> live[Live ticks]
```

---

## How a match is organised

A **fixture** is the thing you price: Arsenal vs Chelsea, Saturday 15:00.

Around it:

```mermaid
flowchart TB
  sport[Sport: soccer] --> league[League: Premier League]
  league --> season[Season: 2025-26]
  season --> stage[Stage: Matchday 8]
  stage --> fixture[Fixture: Arsenal vs Chelsea]
  fixture --> segment[Segments: 1st half, 2nd half, full time]
  sport --> team[Participants: Arsenal, Chelsea]
```

- A **league** is any recurring competition — league, cup, tournament, series.
  The FA Cup and the Premier League are both leagues in this sense.
- A **participant** is a team *or* a person (a tennis player, a driver). The
  same club can play the league and the cup in one week, so participants belong
  to a sport, not to a single league.
- A **player** is roster membership: this person, in this team, this number.
- A **segment** is a *slice inside* the match (first half, set 3, Q1). It is
  not a separate match.

Formula 1 is the useful exception: Qualifying, Sprint and Race are three
**fixtures** in one round. Q1 / Q2 / Q3 are segments of Qualifying.

The shared names for sports, segments and bet types are the
[taxonomy](taxonomy.md). Team names and match ids stay the publisher’s own;
OpenBook does not mint those.

---

## Three kinds of “what’s going on?”

These are easy to mix up. They answer three different questions.

| Question | Everyday | Example |
| --- | --- | --- |
| Is the event happening? | Fixture status | scheduled → live → ended |
| Where is the match, and is this slice finished? | Segment status | 1st half live; full time **down** (final) |
| Can you still bet this market? | Market status | open / suspended / closed / void |

**Down** on a segment means that slice is finished for grading. It happens
once. A wrong score later is an *erratum* (a correction), not a second
whistle.

Taking a market off the board is a market status — not a fake price of zero.

```mermaid
flowchart LR
  subgraph match [The match]
    scheduled --> live --> ended
  end
  subgraph slice [A slice of the match]
    pending --> playing[live]
    playing --> down[down: final]
  end
  subgraph board [This bet]
    open --> suspended
    open --> closed
    open --> voided[void]
  end
```

---

## What you subscribe to

Everything about one match hangs off that match. If you care about Arsenal vs
Chelsea, you follow that fixture: prices, score, markets coming off, grades.

You do not need MQTT, or any particular pipe. OpenBook names the *message*,
not the transport.

---

## Where to go next

| If you want… | Read |
| --- | --- |
| Shared names for sports, bets, slices | [Taxonomy](taxonomy.md) then the [id lists](../vocabularies/) |
| The rules implementers must follow | [The specification](../spec/openbook.md) |
| Why a rule exists | [Decision log](decisions.md) |
| Machine-checkable shapes | [JSON Schemas](../schema/) |
