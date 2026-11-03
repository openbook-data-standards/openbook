---
name: openbook-consume
description: Consume OpenBook snapshots or streams using the JavaScript core cache, optional pricing and React bindings, while checking package availability and proving actual document updates.
---

# Consume an OpenBook feed

## Sources

Read the [client README](https://github.com/openbook-data-standards/openbook-js/blob/main/README.md), [workspace manifest](https://github.com/openbook-data-standards/openbook-js/blob/main/package.json), [onboarding guide](https://github.com/openbook-data-standards/openbook/blob/main/docs/onboarding.md) and [catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Read package-level APIs at the actual revision before proposing code.

## Workflow

1. Confirm framework-free consumption versus React display versus cross-source pricing. Node.js 20+ is declared; React 18+ is needed only for the binding. Use only relevant packages.
2. Gate on distribution: the public @openbook/core, @openbook/pricing and @openbook/react lookups returned 404 at catalog review (ONB-001). Perform an authorized read-only registry check before claiming this changed. Do not substitute an unrelated package. Publishing needs separate release approval.
3. Until a distribution path is verified, offer source/API orientation and name the runtime blocker. A contributor workspace build is not automatically a validated external consumer-install workflow.
4. With a usable reviewed build and permission, choose a synthetic snapshot or stream, then inspect OpenBookClient, its source seam and cache by object/id. Apply actual documented envelopes and Merge Patch semantics, not vendor wire data.
5. Prove a known document appears after the snapshot and changes after an update. Record before/after and source identity. In React, a provider without url/source/client intentionally returns empty hooks; that is not success.
6. On failure, distinguish missing source configuration, snapshot absence, schema/version mismatch, stream sequencing and market suspension. Do not convert missing/stale data to fake zero prices. Confirm profile-envelope support explicitly rather than assuming generic compatibility.

## Evidence

Show exact source/package revision, registry or source-build readiness, chosen transport, sanitized input and cache before/after. State whether pricing/React was actually used. An example URL is not a public live service; a successful install or empty UI does not establish feed connectivity.

## Boundaries

Do not run tests locally; CI owns test execution. Get approval for installs, builds, file changes and network connections. Do not expose tokens, connect private feeds, modify customer apps, publish packages or deploy as part of onboarding. Do not invent API signatures, identity or compatibility.
