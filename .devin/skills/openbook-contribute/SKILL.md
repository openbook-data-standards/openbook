---
name: openbook-contribute
description: Contribute authorized OpenBook ecosystem documentation and skills, extend the shared catalog, and keep generated pages, evidence, blockers and CI aligned without changing contracts implicitly.
---

# Contribute and extend OpenBook

## Sources

Read the target repository's actual AGENTS/rules and contributor instructions first. For this repository use [AGENTS](https://github.com/openbook-data-standards/openbook/blob/main/AGENTS.md), [CONTRIBUTING](https://github.com/openbook-data-standards/openbook/blob/main/CONTRIBUTING.md), [extension workflow](https://github.com/openbook-data-standards/openbook/blob/main/docs/extending-ecosystem.md), [agent acceptance checklist](https://github.com/openbook-data-standards/openbook/blob/main/docs/agent-skills.md) and [catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json).

## Workflow

1. Confirm explicit authorization for the named work. A question, review finding or skill installation is not permission to modify a standard, publish a package, push or open a PR. Follow the user's repository and branch rules.
2. Before adding a project, read its public README, manifest, license, tags and actual workflows. Record sources and maturity honestly. No private integrations or licensed source payloads belong in the catalog.
3. Edit docs/ecosystem.json as the sole version/readiness inventory. Use an existing skill when suitable; otherwise add a compact portable skill under .devin/skills and list its name. Do not duplicate authored skills across editor directories.
4. Add a goal-based human journey with prerequisites, authorization boundaries, synthetic expected output and failure evidence. Attach external decisions to named ONB-nnn blockers with owners; never remove a blocker merely because it is inconvenient.
5. Update review date and onboarding bundle version appropriately. Generate catalogs with python3 tools/build_onboarding.py, statically check with --check, then regenerate HTML with python3 tools/build_site.py. These commands are documentation/static checks, not project tests. Do not patch generated copies manually.
6. When authorized, use --check --upstream for read-only public inventory/source-link drift. It requires gh authentication and does not certify package availability, agent behavior or runtime compatibility.
7. Review all generated and new files. CI owns tests. Complete actual agent sessions before claiming behavioral certification, and release/push/PR only when explicitly authorized.

## Evidence

Report catalog/skill counts, static-check output, regenerated pages, exact source revision and named owner blockers. Distinguish local static verification, CI results, installation discovery and actual agent behavior. Do not report green CI without checking a real authorized remote run.

## Boundaries

Do not run tests locally; CI owns test execution. Do not edit normative schemas, vocabularies, spec decisions or conformance as incidental onboarding cleanup. Core/profile compatibility, licensing, package publication and sibling-repository changes require their own approval. Never deploy or execute financial operations as verification.
