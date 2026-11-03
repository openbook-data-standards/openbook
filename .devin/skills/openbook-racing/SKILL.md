---
name: openbook-racing
description: Explain OpenTrack horse-racing snapshot models, source identity and harness-data limitations while respecting its experimental-draft status.
---

# OpenTrack racing orientation

## Sources

Read the [OpenTrack README](https://github.com/openbook-data-standards/opentrack/blob/main/README.md), [manifest](https://github.com/openbook-data-standards/opentrack/blob/main/pyproject.toml), model definitions and [readiness catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Recheck the actual license state before changing the gate.

## Workflow

1. Start with licensing and status: OpenTrack is Apache-2.0 but an experimental draft, not a published standard. Recheck the actual license state before quoting it, and present draft maturity honestly rather than implying a finished contract.
2. Explain the experimental standalone Python 3.11+ immutable dataclasses: Runner, Selection, Market and RaceSnapshot. They are not a published standard, source-payload validators, identity-resolution service or a claim of OpenBook conformance.
3. Preserve source identifiers and statuses. Distinguish a provider's quoted value from usable fixed decimal odds. Starting-price/unknown products are not guaranteed fixed-odds quotes.
4. Preserve grouped markets, terms, unknown discipline, missing times and unresolved currency. Do not compare monetary limits without verified units. Observation time is not source scheduling/cutoff time.
5. Explain that harness/Standardbred is a validation focus, not proof any provider offers that data. Driver, start method, handicap and full market semantics require representative authorized evidence.
6. If the user authorizes implementation, reread the current source before proposing synthetic workflows. Keep provider clients/adapters, credentials, licensed captures and execution in separate projects.

## Evidence

Cite exact source revision, license and model fields actually present. List unresolved discipline, currency, timing or harness semantics rather than guessing them. A hypothetical-return arithmetic illustration is not payout, bet-acceptance or execution evidence.

## Boundaries

Do not run tests locally; CI owns test execution. No provider accounts, live feeds or execution are needed for orientation. Do not claim OpenBook conformance, infer provider capabilities or treat native ids as canonical cross-provider identity.
