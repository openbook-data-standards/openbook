# OpenBook display profile

A derived **UI view** of serving data. Version `0.3.0-draft` · decision **Q56**.
The JSON Schema in [`../schema/display.schema.json`](../schema/display.schema.json)
is machine-normative. Keywords **MUST**, **SHOULD**, **MAY** are used per RFC 2119.

This is **not** a second serving protocol. The publisher wire stays in
[`openbook.md`](openbook.md): decimal `odds`, `sequence`, Merge Patch,
fixture-first topics. Display sits on top.

---

## 1. Why a second document

The serving wire is for **importers**: books, feeds, traders, regulators.
A sportsbook screen, a TV board, and a mobile betslip need extra things that
are **not facts**:

- American / fractional / implied spellings of the same decimal price (Q39).
- Labels in one language (`inLanguage`).
- A stable sort for tabs and columns (`displayOrder`).
- An optional betslip `selectionId`.

KIBL’s flipped-participants / rotation / ordering hints and Pinnacle’s three
price formats on the live API are the industry versions of this split.
OpenBook keeps them **off** the serving objects so a feed’s presentation
order is never a fact (§6 of the serving spec).

## 2. Rules

- **Same ids.** `fixture`, `source`, `marketType`, `segment`, `line`, `side`
  are copied from serving. Display MUST NOT mint a parallel identity.
- **`basedOn`** is the serving `sequence` this view was built from. A display
  document MUST NOT invent or round a price that is not on that sequence.
- **Canonical price stays `odds`** (decimal string, strictly greater than 1).
  `displayOdds` is how that price is **shown** under `oddsFormat`
  (`decimal` · `american` · `fractional` · `implied`).
- **`profile` MUST be `display`.** Serving documents omit `profile`.
- **Not on the push grammar.** Display is not an `object` / `action`. Do not
  publish `…/fixture/<id>/display/…` topics. A publisher MAY list a display
  URL on the discovery document (`name` + `url`) next to snapshot and stream.
- **Anyone MAY derive it.** A consumer MAY build a display document locally
  from a serving snapshot. A publisher MAY also emit one. Both MUST cite
  `basedOn`.
- **Q37 still applies.** Strict when you write this schema; readers ignore
  unknown fields. No separate consumer-view schema (Q51).

## 3. Document

One document is **one fixture × one source**, in one `inLanguage` and one
`oddsFormat`. Switching language or odds format is another document (same
pattern as another `baseCurrency` being another subscription).

Required: `openbookVersion`, `profile`, `basedOn`, `dateModified`,
`inLanguage`, `oddsFormat`, `fixture`, `source`, `markets[]`.

Each market MAY carry `name`, `marketCategory`, `isMain`, `displayOrder`.
Each outcome MUST carry serving `side` + `odds`, and MAY carry `name`,
`displayOdds`, `impliedProbability`, `displayOrder`, `selectionId`.

`ttl` SHOULD be short (often `1`) so a UI does not freeze a stale board.

## 4. Conformance

A display document is OpenBook-conformant when it validates against
[`display.schema.json`](../schema/display.schema.json) and the rules in §2.
Level R / Level L in the serving spec are unchanged: they describe the
publisher feed, not this view.
