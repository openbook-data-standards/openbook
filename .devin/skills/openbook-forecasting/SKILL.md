---
name: openbook-forecasting
description: Get started with OpenProb forecasting contracts, finite count distributions and synthetic evaluation while preserving chronology, abstentions, unresolved labels and honest performance claims.
---

# OpenProb forecasting orientation

## Sources

Read the [OpenProb README](https://github.com/openbook-data-standards/openprob/blob/main/README.md), [manifest](https://github.com/openbook-data-standards/openprob/blob/main/pyproject.toml), current source contracts/evaluation and [catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Inspect the actual CI workflow for the executed checks.

## Workflow

1. Explain that OpenProb is an Apache-2.0 experimental standalone Python package, not a published interoperability standard, provider client, betting system or claim of OpenBook/OpenVenue conformance. Python 3.11+ and the standard library suffice at runtime.
2. Read Target, Forecast, Label and CountDistribution at the reviewed commit. Target identity is caller-owned; the package does not resolve cross-provider identity. Finite count support assigns no mass above its bound.
3. If the user approves a synthetic demonstration, use the documented command from a reviewed checkout: PYTHONPATH=src python3 -B -m openprob. It prints illustrative forecasts/evaluation without provider access, cloud, credentials or an archive. Do not confuse it with a test runner or execute it without consent.
4. Explain training/information/generation/outcome chronology, label availability at cutoff, duplicate rejection and single-model-version evaluation. Unknown, void or disputed results are not automatically false labels.
5. Explain total/abstained/unresolved/scored counts, coverage, Brier score, log loss and calibration. Wrong certainty may produce infinite loss; empty scores are null. Correlated thresholds are not independent observations.
6. For a real study, propose a frozen model, temporal holdout, comparable baseline, source/data-rights review and honest disclosure of missing labels and source revisions. Storage and retained evidence are consumer responsibilities.

## Evidence

Report exact source revision, synthetic command/output if executed, counts and chronology assumptions. State limitations: descriptive scores do not prove significance, model skill, tradable prices, attainable returns or profitability. If commands were not run, label the result as source orientation only.

## Boundaries

Do not run tests locally; CI owns test execution. Do not fetch licensed data, execute third-party model code, connect accounts, place bets or archive source data without authorization. Do not invent provider integrations, confidence intervals, cross-provider identities or conformance claims.
