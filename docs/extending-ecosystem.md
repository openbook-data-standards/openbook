# Extend the ecosystem guide and agent bundle

This onboarding system is deliberately additive. The source catalog is [ecosystem.json](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json), validated by [ecosystem.schema.json](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.schema.json). Neither belongs to the normative wire schemas. Maintainers named by repository CODEOWNERS review changes. No new service, package registry or custom installer is required.

## Source of truth

- docs/ecosystem.json: public inventory, observed versions, licensing, prerequisites, distribution, evidence sources, skill routing and owner blockers.
- docs/onboarding.md: human journeys and first-success evidence.
- .devin/skills: authored portable skills. Only the openbook/references/ecosystem.md file is generated.
- docs/ecosystem.md: generated catalog and readiness register. Do not edit directly.
- docs/agent-skills.md: distribution and agent acceptance checklist.
- tools/build_onboarding.py: static schema/link/skill checks, catalog generation and optional upstream inventory/source-link audit.
- tools/build_site.py: the existing site generator; renders onboarding pages using the site's navigation and styling.
- Organization .github/profile/README.md: a concise entry point linking here, not a second version matrix.

## Add a public project

1. Confirm the repository is public and belongs in the family. Read its own rules, README, license, manifests, tags, example data and CI. Never include private integrations, credentials or licensed provider payloads in this catalog.
2. Add one projects entry. Record observed versions separately from published releases. Distinguish a standard, profile, implementation library, tool and experimental model.
3. Link authoritative source files. Do not infer package publication from package.json/pyproject.toml. Check the public registry before advertising an install command. Record a missing license as pending, not open source.
4. Route to an existing skill where possible. related_projects records conceptual relationships, not guaranteed runtime dependencies or cross-project conformance.
5. Add a journey with prerequisites, authorization points, a synthetic first-success example, expected evidence, failure guidance and project boundaries. If it cannot run, explain why rather than inventing success.
6. Attach unresolved external decisions to a named ONB-nnn blocker with an owner and required decision. Link that id from each affected project. Do not silently remove an unresolved item.
7. Update reviewed_on and bump bundle_version for the released onboarding change. catalog_version changes only when this informational catalog structure changes.
8. Regenerate and statically check the assets, rebuild the site, and review the resulting diff. Follow each repository's branch rules; current OpenBook work branches from fresh origin/main and targets main.

## Project entry template

Copy an existing entry and adapt this structure. Replace every placeholder with reviewed evidence; do not add this template as a real project.

```json
{
  "id": "public-repository-name",
  "kind": "library",
  "summary": "What it does and what it does not do.",
  "version": "Observed manifest version; separately state verified release tag",
  "license": "Verified SPDX license or license pending",
  "maturity": "experimental",
  "prerequisites": ["Verified runtime requirement"],
  "distribution": "Verified distribution path, or exact blocker",
  "related_projects": [],
  "skill": "openbook",
  "first_success": "Small synthetic workflow and concrete expected evidence",
  "sources": ["https://github.com/openbook-data-standards/public-repository-name/blob/main/README.md"],
  "blockers": []
}
```

For an owner-gated item, add a blocker with id, owner, requires and detail, then reference its id from the project. Keep evidence dates honest. Package publication, license selection, normative compatibility changes and changes to sibling repos need their own authorization.

## Add or revise a skill

Prefer small, goal-oriented skills to one skill per file or API operation. Place a new skill under .devin/skills/openbook-topic/SKILL.md and add its name to the catalog's skills list. All skill bodies must remain useful when copied alone; do not rely on a sibling skill or a path back into the source checkout. Use bundled relative references only within the installed skill directory, and authoritative public links elsewhere.

Use this minimal portable template, replacing the name, description and workflow:

```markdown
---
name: openbook-topic
description: Describe the user's goal and when this skill should be selected.
---

# OpenBook topic

## Sources

Read the target project's authoritative public README/specification and current ecosystem catalog before acting.

## Workflow

1. Confirm the user's goal, exact revision and required environment.
2. Check distribution, licensing and compatibility gates.
3. Propose the smallest synthetic workflow; obtain approval for installs, writes or execution.
4. Carry out only authorized steps and capture sanitized evidence.

## Evidence

Report the exact revision, expected result, observed result and remaining named blockers. An install alone is not success.

## Boundaries

Do not invent fields, identities or compatibility. Do not expose secrets or run production operations. Do not run tests locally; CI owns test execution. Follow the repository's own rules and stop at missing authorization.
```

Include real Markdown links in the authored skill's Sources section, not just the template's prose. Do not add permission grants, hooks, subagent requirements or automatically executed scripts. Include known failure modes and explicit expected results appropriate to the task. For any bundled references, keep their license/attribution and source revision clear.

## Build and check

The builder uses the existing jsonschema/referencing validation dependencies; no additional package is needed. These are documentation generation and static integrity commands, not project test runners:

```sh
python3 tools/build_onboarding.py
python3 tools/build_onboarding.py --check
python3 tools/build_site.py
python3 tools/build_onboarding.py --check --site
git diff --check
```

The read-only checker enforces catalog structure, unique ids, cross-project references, blocker links, declared skill coverage, portable frontmatter, safety/evidence sections, local Markdown links and exact generated catalog freshness. The optional --site gate checks rendered onboarding links, anchors and navigation after the HTML build. It does not run example programs, install packages, call production services or certify agent behavior.

When online and authorized to make read-only GitHub API calls:

```sh
python3 tools/build_onboarding.py --check --upstream
```

This uses authenticated gh to compare all active public organization repositories against the catalog and verify authoritative source-file links. It fails for new uncatalogued repositories, missing/archived projects and unavailable sources. Authentication/rate-limit failures are failures, not proof a project disappeared. It does not crawl private repository contents. Version, license and registry-readiness changes still require source review; this audit does not automatically rewrite those claims.

CI performs static checks, regression cases, generated-site freshness and isolated copy-install checks for the four initial agent selectors on pull requests. Installation checks compare skill files and bundled references without launching agents; behavioral acceptance remains separate. A separate scheduled/manual read-only audit detects upstream inventory drift; it never opens issues, contacts people or writes back. All project tests remain in CI. Do not run tests locally.

## Release checklist

1. Recheck every changed distribution/license/compatibility claim against its linked source. Resolve blockers only with evidence and owner approval.
2. Regenerate catalog references and HTML; review new files as well as tracked changes.
3. Verify skill discovery with the pinned CLI in list-only mode. Do not install into the authored source directory.
4. Run the interactive agent acceptance checklist from agent-skills.md on each agent for which the release claims verified behavior. Record exact agent, bundle/source revision, scenario results and sanitized evidence in the release/PR review.
5. Obtain green CI after an explicitly authorized push/PR. No publication, PR, push or deployment is implied by a local build.
6. Publish a Git tag or package only with separate release authorization. Link the approved source revision in installation guidance; keep older reviewed bundles available for rollback.

If a gate cannot be completed, name it and withhold that readiness claim. A format-compatible skill bundle is not a claim that all agents have passed behavioral certification.
