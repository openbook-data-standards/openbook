# OpenBook ecosystem catalog

Informational, not a wire specification. Generated from [ecosystem.json](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json); edit the catalog, not this page.

Bundle **0.1.0** · reviewed **2026-11-03**. Versions and distribution are observations, not promises of current registry availability.

Start with the [onboarding guide](https://github.com/openbook-data-standards/openbook/blob/main/docs/onboarding.md), [agent setup](https://github.com/openbook-data-standards/openbook/blob/main/docs/agent-skills.md), or [extension workflow](https://github.com/openbook-data-standards/openbook/blob/main/docs/extending-ecosystem.md).

Related projects below are conceptual relationships, not an install dependency graph. Standalone projects do not claim conformance to sibling standards.

## openbook

Sportsbook reference data, live change envelopes, schemas and controlled vocabularies.

- Repository: [openbook](https://github.com/openbook-data-standards/openbook).
- Type: standard; maturity: draft.
- Version: 0.3.0-draft.
- License: CC-BY-4.0 specification material; see repository LICENSE for tooling boundaries.
- Prerequisites: No runtime needed to read the standard; Python and jsonschema/referencing for CI validation.
- Distribution: Specification tag v0.3.0-draft; pin a reviewed commit for subsequent draft changes.
- Related projects: standalone / none required.
- Agent skill: `openbook`.
- First success: Trace publisher, fixture, market, price change and grade using the worked examples without connecting a provider.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openbook/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openbook/blob/main/docs/guide.md) · [source 3](https://github.com/openbook-data-standards/openbook/blob/main/spec/openbook.md).

## openbook-starter

Python publisher/discovery scaffolding CLI; not a feed server or provider adapter.

- Repository: [openbook-starter](https://github.com/openbook-data-standards/openbook-starter).
- Type: tool; maturity: early.
- Version: 0.1.0 (manifest; no release tag observed).
- License: Apache-2.0.
- Prerequisites: Python 3.11+; Isolated Python environment; Publisher identity and an explicit output directory.
- Distribution: Public source checkout; install with pip from the HTTPS Git URL until a PyPI release exists. The translations extra resolves openbook-translate from its tagged Git release.
- Related projects: openbook, openbook-translate.
- Agent skill: `openbook-publish`.
- First success: Generate publisher, discovery and snapshot documents in an empty scratch directory with --no-workflow; inspect them without publishing.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openbook-starter/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openbook-starter/blob/main/pyproject.toml).

## openbook-translate

Translation kernel with explicit mappings, validation, quarantine, gap counting and envelope helpers; vendor adapters remain separate.

- Repository: [openbook-translate](https://github.com/openbook-data-standards/openbook-translate).
- Type: library; maturity: early.
- Version: 0.1.0; pins OpenBook 0.3.0-draft.
- License: Apache-2.0 code; CC-BY-4.0 vendored schemas and vocabularies.
- Prerequisites: Python 3.11+; jsonschema; referencing.
- Distribution: Git release tag v0.1.0; upstream explicitly documents no PyPI uploads.
- Related projects: openbook.
- Agent skill: `openbook-translate`.
- First success: Inspect synthetic acme translation, preserved native identity, quarantine reason and gap report; no provider account required.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openbook-translate/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openbook-translate/blob/main/pyproject.toml).

## openbook-js

JavaScript core feed/cache client, cross-source pricing and optional React bindings.

- Repository: [openbook-js](https://github.com/openbook-data-standards/openbook-js).
- Type: library; maturity: early.
- Version: core/react 0.3.0; pricing 0.1.0 (manifests).
- License: Apache-2.0 code; CC-BY-4.0 vendored schemas.
- Prerequisites: Node.js 20+; npm workspaces; React 18+ only for React bindings.
- Distribution: Public source workspace. Registry lookups for @openbook/core, @openbook/pricing and @openbook/react returned 404 at review; do not advertise a working public npm install yet.
- Related projects: openbook.
- Agent skill: `openbook-consume`.
- First success: Using a verified source build, apply synthetic snapshot/change input and inspect the cached document; an empty UI is not success.
- Readiness blockers: ONB-001.
- Sources: [source 1](https://github.com/openbook-data-standards/openbook-js/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openbook-js/blob/main/package.json).

## openbook-betting

Venue coverage and bet-order lifecycle data contracts; not an execution service.

- Repository: [openbook-betting](https://github.com/openbook-data-standards/openbook-betting).
- Type: profile; maturity: draft.
- Version: draft; pins OpenBook 0.3.0-draft.
- License: CC-BY-4.0.
- Prerequisites: Understand core OpenBook and the profile's own change envelope.
- Distribution: Schemas and worked documents in the public repository; no runtime package required.
- Related projects: openbook.
- Agent skill: `openbook-market-contracts`.
- First success: Trace venue, coverage and a synthetic bet lifecycle against the profile schemas, not the closed core object enum.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openbook-betting/blob/main/README.md).

## openexchange

Exchange venues, market state, runners, back/lay depth, starting-price fields and fees.

- Repository: [openexchange](https://github.com/openbook-data-standards/openexchange).
- Type: standard; maturity: draft.
- Version: 0.1.0-draft.
- License: CC-BY-4.0.
- Prerequisites: Understand native runner identity, exact decimal odds and exchange back/lay semantics.
- Distribution: Public specification and JSON Schemas; no client, router or execution runtime.
- Related projects: openbook, openvenue.
- Agent skill: `openbook-market-contracts`.
- First success: Validate the five synthetic example documents under examples/ against the schemas using the walkthrough snippet, then explain a runner's depth and the venue fee contract.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openexchange/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openexchange/blob/main/spec/openexchange.md) · [source 3](https://github.com/openbook-data-standards/openexchange/blob/main/examples/README.md).

## openvenue

Canonical tokenized markets, equivalence, order books and all-in quote/routing contracts.

- Repository: [openvenue](https://github.com/openbook-data-standards/openvenue).
- Type: standard; maturity: draft.
- Version: 0.0.2-draft.
- License: CC-BY-4.0.
- Prerequisites: Understand canonical versus venue identity, instrument equivalence and fee-adjusted quotes.
- Distribution: Public specification, JSON Schemas and examples; not a supplied routing implementation.
- Related projects: openexchange.
- Agent skill: `openbook-market-contracts`.
- First success: Follow the two synthetic venue books through the quote request/decision examples without sending an order.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openvenue/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openvenue/blob/main/spec/openvenue.md).

## opentrack

Standalone horse-racing snapshot, runner, market and selection dataclasses; harness semantics remain under validation.

- Repository: [opentrack](https://github.com/openbook-data-standards/opentrack).
- Type: experimental-library; maturity: experimental.
- Version: 0.0.1 (manifest).
- License: Apache-2.0.
- Prerequisites: Python 3.11+; Standard library at runtime.
- Distribution: Public source checkout under Apache-2.0; experimental, not a published interoperability standard.
- Related projects: standalone / none required.
- Agent skill: `openbook-racing`.
- First success: Read model definitions and explain source identity, unknown discipline and quoted-value versus fixed-odds distinctions.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/opentrack/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/opentrack/blob/main/pyproject.toml) · [source 3](https://github.com/openbook-data-standards/opentrack/blob/main/LICENSE).

## openprob

Standalone forecasting contracts, finite count distributions, labels and descriptive evaluation.

- Repository: [openprob](https://github.com/openbook-data-standards/openprob).
- Type: experimental-library; maturity: experimental.
- Version: 0.1.0 (manifest; not a PyPI release).
- License: Apache-2.0.
- Prerequisites: Python 3.11+; Standard library at runtime.
- Distribution: Public source checkout and synthetic module example; no cloud, database or credentials required.
- Related projects: standalone / none required.
- Agent skill: `openbook-forecasting`.
- First success: Run the authorized synthetic module example and explain coverage, abstention, unresolved labels and chronology without making profitability claims.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/openprob/blob/main/README.md) · [source 2](https://github.com/openbook-data-standards/openprob/blob/main/pyproject.toml).

## .github

Public organization entry point; links to the canonical ecosystem catalog rather than maintaining another version matrix.

- Repository: [.github](https://github.com/openbook-data-standards/.github).
- Type: organization-profile; maturity: documentation.
- Version: Not a package.
- License: No repository license detected; follow licenses of linked projects.
- Prerequisites: None.
- Distribution: GitHub organization profile; not an installable product.
- Related projects: openbook.
- Agent skill: `openbook`.
- First success: Choose an onboarding goal and follow its canonical project guide.
- Readiness blockers: none recorded; not a runtime certification.
- Sources: [source 1](https://github.com/openbook-data-standards/.github/blob/main/profile/README.md).

## Readiness register

A skill install does not resolve these owner decisions. Do not remove a blocker until its source and distribution/compatibility evidence have been rechecked.

### ONB-001

The three documented npm packages returned public registry 404. Publishing is not authorized by onboarding work.

Owner: openbook-js release maintainers. Required: Package publication or a separately verified source-consumer distribution workflow.
