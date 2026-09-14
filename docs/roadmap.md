# Roadmap (2026-Q4 → 2029-Q3)

Non-normative. Current rules live in [`../spec/openbook.md`](../spec/openbook.md).
This page is where the specification goes next, and where it does not.
Evidence for the later protocols sits in
[`protocol-comparison.md`](protocol-comparison.md) §16.

The catalog walk stopped at **Q167**. The wire stays frozen until a named
board. What follows is a new area: adoption, identity matching, and
profiles that pin this spec rather than rewrite it.

## Thesis

The wire is nearly done. The vocabulary is the product. Every aggregator
and every supplier has a private market taxonomy and a private fixture
crosswalk. Nobody publishes one. OpenBook already owns sports, segments,
market types and sides.

Q2 stays right to reject a **central** entity database; Q171 adds a **federated register** without making OpenBook the owner of player, team or league ids. OpenBook owns a cheap centre: scheme prefixes, never-reuse, and a derivation rule for one entity nobody else registers — the fixture.
Leagues, teams and players stay publisher-own, pinned to Wikidata when a
QID exists (**Q171**).

Branch by audience, not by feature. Core stays the public odds wire and
freezes at 1.0. Regulator reporting, a prediction-market bridge, integrity
alerts and a federated register each become a **separate specification**
that pins a core major and a vocabulary release (**Q171**, **Q172**). A
list of known feeds lives beside the validator, not on the discovery
document (**Q173**, Q94 stands).

No clean-slate 2.0. Envelope stable; enumerations move.

## Product map

| Repo / directory | When | What |
| --- | --- | --- |
| this repository (core) | now → 1.0 in year 2 | Public odds, scores, grades wire |
| `vocabularies/` | monthly | Sports, segments, market types, sides |
| `crosswalks/` | year 1 | Maps from those ids to public taxonomies |
| `register/` | year 1 | Scheme prefixes, never-reuse, redirects |
| openbook-register | year 2 | Fingerprint recipe, anchors, snapshots |
| openbook-pm | year 1 | Event-contract ↔ market / selection |
| openbook-reg | year 2 | Bet-level reporting that carries OpenBook ids |
| openbook-integrity | year 2 | CAP-shaped alert envelope |
| openbook-validator | year 1 | Hosted runner, badge, feed list |
| openbook-mcp | year 1 | Consumer: serve any OpenBook feed to agents |
| openbook-translate, openbook-starter | year 1 | Public, Apache-2.0; no vendor adapters (Q96) |

Git stays trunk `main`, one pull request per decision pass.

## Year 1 — 2026-Q4 → 2027-Q3

Make it un-ignorable. One producer and one consumer that are not
`tools/validate.py`, both public. Vocabulary maps published. Register
foundations with no entity database.

**Q4 2026.** Sibling tooling public. A `crosswalks/` directory: each
public taxonomy maps onto existing OpenBook ids, or onto the unknown
catch-all with a reason. CI checks the map. Q171–Q173 logged.

**Q1 2027.** Namespace register (scheme prefixes on `identifier`
`propertyID`). Optional fixture fingerprint from frozen birth facts
(sport, league anchor, start to the minute UTC, ordered participant
anchors, `competitionType`). Anchor policy: Wikidata, plus one community
register per sport when one exists. Property proposals on Wikidata for
provider ids that have none today.

**Q2 2027.** Hosted validator and a badge. Feed list beside that runner
(**Q173**). First producer via a community translate adapter. First
consumer: an MCP server that reads OpenBook documents.

**Q3 2027.** Prediction-market profile 0.1. Core 1.0 release candidate:
smallest required set; two implementations live; maps to at least four
taxonomies.

Exit: producer + consumer public and badged · maps to ≥ 4 taxonomies ·
≥ 10 prefixes · fingerprint in the spec with a corpus case · ≥ 3 listed
feeds · tooling on an index.

## Year 2 — 2027-Q4 → 2028-Q3

Freeze small. Convene narrow. Open a regulator door.

Core 1.0 frozen; Q55 schema-diff CI turns on. Change process: issue →
pull request → vote-to-test (one producer and one consumer committed) →
public test ≥ 7 days → vote-to-adopt. One seat per employer when a
working group forms. Two test days a year against the hosted validator.

Spin `register/` into openbook-register. Partner with an existing
community football register rather than minting people and clubs.
Add one non-football sport the same way. Publish a static resolver from
fingerprint to known publisher ids.

openbook-reg 0.1: bet records that carry OpenBook ids, shaped to sit
inside existing national reporting files — one source model, N exports.
Doors, in order: a young market with a sports code table; a regulator
that already codes events and markets; a CEN reporting revision; GLI-33
with no format today. Recognised, not created, by a regulator.

openbook-integrity 0.1: CAP-shaped envelope that names a fixture
fingerprint and a market id.

Exit: 1.0 frozen · change process used ≥ 3 times · working group of ≥ 3
organisations · ≥ 1 published snapshot with a community register · ≥ 1
written regulator or lab conversation · ≥ 5 badged feeds.

## Year 3 — 2028-Q4 → 2029-Q3

Decide the register on evidence. Neutral home only if funders exist.

**Gate, 2028-Q4.** Do ≥ 2 publishers exchange fingerprints and anchors in
production, and does ≥ 1 aggregator or exchange consume them?

- Yes — a jointly governed open sports register: prefix allocation, no
  per-id fee, never delete, retire and redirect, logged merges. OpenBook
  holds one seat and contributes the fingerprint rule. It does not hold
  the keys.
- No — stay at the spec layer. Revisit annually.

A foundation home only with ≥ 3 funders. Profiles may take separate
homes. Revenue: conformance review and badge renewal, test-day fees,
sponsored listings. Never spec access, never per-id fees.

Later, after 1.0: generated protobuf or SBE from the same schemas; MQTT
reason-code equivalence. Parked unless pulled: bet-slip portability,
horse-racing sport id, per-sport player-position lists (Q76).

Exit: gate recorded · ≥ 10 badged feeds across ≥ 3 publishers ·
openbook-reg referenced in ≥ 1 guidance or draft · hosting funded · the
steward is not a single point of failure.

## Will not

- An OpenBook-run database of players, teams or leagues (Q2 option b;
  **Q171** is the federated register).
- A clean-slate 2.0.
- Modelling all of sport. Map outward.
- Official vendor adapters (Q96).
- A governance seat for a supplier with exclusive league rights before
  per-employer caps exist.
- Competing on micro-betting transport or official-data pricing.
