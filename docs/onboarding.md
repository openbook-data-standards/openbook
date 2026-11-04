# Get started with the OpenBook ecosystem

This is an informational guide to the public OpenBook Data Standards family, not a new specification. Start with your goal; you do not need to install every project. The contracts are public, while implementations, provider adapters, models, strategies and licensed data can remain private.

## Start here

1. Read the [plain-language OpenBook guide](guide.md) and [worked documents](examples.md).
2. Check the generated [ecosystem catalog and readiness register](ecosystem.md) for current project roles, licenses, prerequisites, distribution and named blockers.
3. Choose a journey below. Start with synthetic documents, not real accounts or live execution.
4. Optionally [install the agent skills](agent-skills.md). Skills provide instructions, not credentials or service access.
5. Record the exact repository commit or release you use, the expected result and the actual result. A successful install alone is not a successful integration.

No Neon account, shared cloud, database or hosted OpenBook account is required to understand the contracts. Neon is an example of skill onboarding, not a dependency of this ecosystem.

## Ecosystem map

OpenBook is the sportsbook reference/live contract. A separately maintained provider adapter can use openbook-translate to produce OpenBook documents. A publisher hosts those documents over its chosen transport. openbook-js consumes OpenBook snapshots and changes; pricing and React bindings are optional. openbook-starter only scaffolds publisher/discovery documents, not the hosting or translation service.

The sibling contracts cover different surfaces: OpenBook Betting describes coverage and order lifecycle; OpenExchange preserves exchange state, runners, depth and fees; OpenVenue describes tokenized market equivalence and all-in quotes. These are not interchangeable schemas or supplied execution engines.

OpenTrack and OpenProb are standalone experimental models. Neither establishes conformance to core OpenBook or automatic interoperability with the other projects. Both are Apache-2.0; they remain experimental drafts, so quote that status rather than presenting them as finished standards.

## Understand the standard

Start with the [guide](guide.md), [taxonomy](taxonomy.md), [examples](examples.md), then the [specification](../spec/openbook.md) and [schemas](../schema/).

Distinguish publisher (transmits), source (whose price), consumer (reads), reference objects (durable context), and live changes. Fixture status, segment finality and market availability answer different questions. Preserve source/native identity and timestamps; do not invent cross-provider identity resolution.

First success: follow one fixture from reference documents to a market update and grade, citing the actual example fields. Explain what changes, what stays cached and which source owns each price. No runtime or credentials are required for this reading journey.

To see the pieces compose, run [`examples/end-to-end/walkthrough.py`](https://github.com/openbook-data-standards/openbook/blob/main/examples/end-to-end/walkthrough.py): it applies a shipped fixture-update envelope to the snapshot fixture with an RFC 7386 Merge Patch and re-validates — the same flow starter scaffolding, a translate adapter, and a consumer perform at each seam.

## Publish a feed

Use [openbook-starter](https://github.com/openbook-data-standards/openbook-starter) with Python 3.11+ in an isolated environment. Its README documents public HTTPS Git installation until a PyPI release exists.

The following is a source-checkout workflow, not a claim that a PyPI package exists. Review and record the checkout commit before installing. Dependency installation and writing the scratch directory require the user's consent.

```sh
git clone https://github.com/openbook-data-standards/openbook-starter.git
cd openbook-starter
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install .
openbook start --id acme-feeds --name "Acme Feeds" --currency GBP --base-url https://example.invalid/acme-feeds --dir ./scratch --no-input --no-workflow
```

Use an empty scratch destination; do not pass `--force` over existing work. The example.invalid URL is intentionally non-routable. Before publishing, replace it with hosting you control and verify the actual URL path. The starter does not upload files or start a service.

First success: inspect scratch/openbook/publisher.json, discovery.json and snapshot.json. The snapshot initially represents the publisher, not a populated odds feed. Discovery should list only the endpoint you will really provide. `--no-workflow` avoids installing scheduled automation. No live provider credentials are needed.

For translation support, the starter's `translations` extra pulls the kernel from its tagged Git release; you can also install `openbook-translate` separately at a reviewed tag.

## Translate provider data

Use [openbook-translate](https://github.com/openbook-data-standards/openbook-translate), Python 3.11+, jsonschema and referencing. The kernel documents Git releases rather than PyPI uploads.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install "openbook-translate @ git+https://github.com/openbook-data-standards/openbook-translate@v0.1.0"
```

Inspect its documented synthetic acme adapter and contract cases first. Supply only authorized source data. Production/vendor adapters live separately and are not supplied by the kernel.

For an authorized synthetic demonstration, obtain the sample from the same release tag. This reads a synthetic fixture from the repository; it does not invoke its test suite, contact a provider or write translated data to disk:

```sh
git clone --branch v0.1.0 https://github.com/openbook-data-standards/openbook-translate.git
cd openbook-translate
python3 - <<'PY'
import json
from pathlib import Path
from openbook_translate.acme import AcmeTranslator

translator = AcmeTranslator()
fixture = json.loads(Path("tests/data/fixture.example.json").read_text())
record = {"id": "A-88213", "type": "fixture", "openbook": fixture}
result = translator.translate(json.dumps(record).encode(), source_id="acme-book")
print(json.dumps(result.documents[0], indent=2))
without_sport = {key: value for key, value in fixture.items() if key != "sport"}
unknown = {"id": "A-unknown", "type": "fixture", "sport": "CURL", "openbook": without_sport}
translator.translate(json.dumps(unknown).encode(), source_id="acme-book")
print(json.dumps(translator.gaps.to_dict(), indent=2))
print(translator.translate(b"not json", source_id="acme-book").reason)
PY
```

Expected evidence: the first document retains native id A-88213 under adapter acme; the gap report records CURL as an unmapped sport; malformed JSON yields parse-error. The synthetic adapter retains unknown sport evidence rather than silently losing the record. This example is derived from the tagged adapter API and supplied synthetic contract cases; executing it still needs consent and is not claimed as run by this guide's static checks.

Build explicit mappings, retain native identifiers, count unknown vocabulary values and quarantine unsupported records with reasons. Do not silently drop records or guess a league, segment, participant or market. Keep any reverse mapping's identity intact.

First success: with an approved synthetic example, capture the translated document, its preserved native identifier, and one unmapped/quarantine result with a reason. Show the gap report. The reusable adapter contract suite belongs in the adapter's CI; do not run tests locally under this project's workflow.

## Consume data or build a display

Use [openbook-js](https://github.com/openbook-data-standards/openbook-js). Its core package reads WebSocket, SSE or HTTP snapshot sources and caches documents after applying Merge Patch. Pricing and React packages are optional. The repository declares Node.js 20+; React bindings require React 18+.

At the catalog review, public registry requests for @openbook/core, @openbook/pricing and @openbook/react all returned 404 (ONB-001). Do not tell a newcomer that the README's npm install commands are already a working public distribution path. Package publication needs release-maintainer authorization. A source-workspace build is a contributor option, but has not been certified here as an external consumer-install workflow.

The read-only journey is available now: inspect the source/package READMEs and core examples, identify snapshot versus stream input, then explain the cache key and a document update. A runnable onboarding acceptance gate remains blocked until a distribution path is verified.

When a usable build is available, first success means a synthetic snapshot creates a known cached document and a synthetic change updates that same document. Record before/after values and source identity. Empty hooks/UI can simply mean no source was configured; they do not prove a working feed. Placeholder socket URLs in examples are not hosted public feeds.

## Exchange, routing and order-lifecycle contracts

Choose the model for the information you must preserve:

- [OpenExchange](https://github.com/openbook-data-standards/openexchange): venue state, native runner identity, back/lay depth, starting-price fields and fee profiles. Read its specification and schemas, then run the synthetic `examples/` corpus — a venue, fee profile, market book and back/lay order books — through its validation walkthrough.
- [OpenVenue](https://github.com/openbook-data-standards/openvenue): canonical tokenized instruments, evidence of equivalence, order books, and all-in quotes including fees. Follow its supplied two-venue example documents; no router or wallet connection is required.
- [OpenBook Betting](https://github.com/openbook-data-standards/openbook-betting): venue, coverage and synthetic bet lifecycles. Its profile objects use their own envelope schema because core closes object types — recorded as decision Q284 in the core decision log. Validate against the profile, not a silently modified core schema.

First success: identify the exact contract and show which native state, fees and lifecycle transitions it preserves. Do not merge superficially similar contracts, infer quote equivalence, synthesize complementary prices without evidence, or submit an order. Execution, accounts, payments and wallets are outside this onboarding.

## Forecasting and evaluation

[OpenProb](https://github.com/openbook-data-standards/openprob) is Apache-2.0 experimental Python with no cloud, database or credentials required. Python 3.11+ and the standard library are sufficient for the synthetic module example from a reviewed checkout:

```sh
git clone https://github.com/openbook-data-standards/openprob.git
cd openprob
PYTHONPATH=src python3 -B -m openprob
```

First success: inspect the forecasts and illustrative evaluation printed to stdout. Explain chronology, abstention, unresolved labels, coverage, Brier/log loss and correlated thresholds. This is an example, not a test runner, retained research archive, proof of model skill or profitability claim. Obtain consent before executing it. The repository CI runs ruff and unittest on every push and pull request.

## Horse-racing models

[OpenTrack](https://github.com/openbook-data-standards/opentrack) contains experimental Python 3.11+ immutable dataclasses for runners, selections, markets and race snapshots. It is not a provider client, canonical identity service, OpenBook conformance implementation or execution system.

Read the public models to understand source identifiers, source quoted values versus usable fixed odds, unknown discipline and unverified currency. Harness-specific details still need representative evidence. First success is a source-backed explanation of those boundaries. The project is Apache-2.0; it remains experimental, so quote its draft status rather than presenting it as a finished standard.

## Troubleshooting and evidence

- Installation failure: record the exact package, reviewed tag/commit, runtime and sanitized error. Do not substitute an unrelated similarly named package.
- Missing data: distinguish missing source configuration, missing snapshots, unmapped records, suspended markets and stale observations. Do not turn any of them into a fake price of zero.
- Schema rejection: identify the project/version and matching envelope schema; profile support is not automatic.
- Missing access: state the exact permission needed. The public synthetic paths should not require provider accounts. Never request secrets in chat or print environment values.
- Stale guidance: update the catalog source and review date, then regenerate the catalog and bundled reference. Do not patch generated copies independently.

A useful handoff includes goal, project, exact revision, environment, sanitized input, expected output, observed output, relevant schema and remaining blocker. Never include licensed payloads or secrets without permission.

## Contribute and extend

Read [CONTRIBUTING](../CONTRIBUTING.md), [AGENTS](../AGENTS.md) and the target repository's own rules. Changes to normative contracts require explicit approval; onboarding work does not grant it. Keep schemas, prose, examples and conformance cases aligned when a contract change is authorized. CI owns test execution; do not run tests locally.

To add a project, skill or journey, use the [extension workflow](extending-ecosystem.md). The [catalog](ecosystem.md) is the single version/readiness inventory, not a second wire vocabulary. No package publication, deployment or production operation is implied by a documentation release.
