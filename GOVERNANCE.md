# Governance & licensing

## Open spec, closed code

OpenBook is an open **standard** for sportsbook & gambling data; the document in
[`spec/`](spec/) is its **specification**. It standardises the data contract — the schemas in [`schema/`](schema/) and the
controlled vocabularies in [`vocabularies/`](vocabularies/). It says nothing
about how any implementer produces, models or prices the data behind a
conformant feed.

- **The specification** (this folder) is published under **CC BY 4.0** — see
  [`LICENSE`](LICENSE). Anyone may implement it, quote it, and build on it, with
  attribution.
- **Implementations** — parsers, pricing engines, trading models, back-office —
  are each implementer's own and stay proprietary. Conformance is about the wire,
  not the engine.
- The **conformance corpus** ([`conformance/`](conformance/)) is part of the
  specification (CC BY 4.0): language-agnostic JSON cases any implementation
  MUST pass. The in-repo validator is one runner, not a language oracle (Q40).
- Reference libraries and extra runners, if published later, carry Apache-2.0
  with a royalty-free patent grant, separate from the spec's CC BY licence.

## How it's governed (staged)

Modelled on how live-data standards actually reached adoption, not on standards
committees:

1. **Gravity play (now).** Published openly under one steward, no committee. The
   value is the vocabulary and the validator being good enough to adopt. This is
   how GTFS and OpenTelemetry won.
2. **Consortium (later).** A lightweight working group only once there are 2–3
   **non-competing** adopters, so the vocabulary reflects more than one house.
3. **Standards body (maybe).** A neutral home (or a betting module proposed to an
   existing body) only if the ecosystem asks for it. An ISO number is an outcome,
   not a starting move.

## Change control

- Vocabularies and schemas change through [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Canonical ids are **stable**: once an id is published it is never re-pointed or
  reused, only deprecated.
- Versioning follows [`VERSIONING.md`](VERSIONING.md).
- **1.0 freeze** requires two independent implementations — one producer and
  one consumer — that are not the in-repo validator (Q41). 0.x minors have
  no two-implementation gate.

## What this is not

- Not a product, and not affiliated with any existing platform (including any
  similarly named betting platform). Always written in full as a specification.
- Not tied to any one provider's ids or internal system. It names none.
