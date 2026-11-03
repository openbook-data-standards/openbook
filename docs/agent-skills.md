# OpenBook agent skills

One portable source lives in .devin/skills in this repository. Each skill uses standard SKILL.md name/description frontmatter, with no agent-specific permission grants, plugins or automatically executed scripts. The [catalog](ecosystem.md) records bundle version and project readiness separately from the OpenBook wire version.

## Install

The skills CLI supports discovery under .devin/skills and agent-specific destinations. See its [discovery rules](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) and [agent matrix](https://github.com/vercel-labs/skills/blob/main/docs/agents.md). We pin skills@1.7.4, published 2026-10-19, rather than automatically executing a newly published latest version.

From your target project's root, inspect the available skills before installing:

```sh
npx skills@1.7.4 add openbook-data-standards/openbook --list
npx skills@1.7.4 add openbook-data-standards/openbook --skill '*' --agent devin --copy -y
```

The remote commands become available only after this onboarding bundle lands on the public main branch. Before that, from a different target project use the reviewed local checkout as the source:

```sh
npx skills@1.7.4 add /absolute/path/to/openbook --list
npx skills@1.7.4 add /absolute/path/to/openbook --skill '*' --agent devin --copy -y
```

Replace the path with your actual checkout. Do not run installation into the source checkout itself: its .devin/skills directory is the authored source. Review source content before allowing any third-party installer to write files. Installation changes project configuration only; it must not connect accounts, provision resources or run onboarding examples automatically.

Choose agents explicitly instead of using --all, which targets every agent without confirmation:

| Agent | CLI selector | Agent discovery destination | Verification status |
| --- | --- | --- | --- |
| Devin | devin | .devin/skills | Standard format and documented CLI mapping; interactive acceptance required |
| Claude Code | claude-code | .claude/skills | Standard format and documented CLI mapping; interactive acceptance required |
| Codex | codex | .agents/skills | Standard format and documented CLI mapping; interactive acceptance required |
| Cursor | cursor | .agents/skills | Standard format and documented CLI mapping; interactive acceptance required |
| Other agents | See upstream agent matrix | Agent-specific | Not claimed as verified; use the acceptance checklist |

For example, replace `--agent devin` with `--agent codex` or explicitly select multiple agents. `--copy` avoids symlink requirements, but the CLI may also maintain its shared skill store/lock metadata. Review the installer's proposed changes. No tool-specific directories outside .devin are authored by this repository. `-y` accepts installer prompts, not permission to execute the skill's workflows. Omit it if you want interactive confirmation. Global installation is opt-in through the upstream `--global` flag; prefer project scope so teams can review the installed version.

CI includes an isolated installation matrix for Devin, Claude Code, Codex and Cursor. It compares copied skill files and bundled references against the source; it does not launch those agents or certify their behavior. No local installation checks or project test runners are required for this workflow.

## Choose a skill

- openbook: route any ecosystem question to the correct project; includes a generated offline catalog reference.
- openbook-publish: starter scaffolding, discovery and publisher responsibilities.
- openbook-translate: adapter mappings, identity, quarantine, gaps and envelopes.
- openbook-consume: core client, pricing and React; registry readiness gate included.
- openbook-market-contracts: choose Betting, Exchange or Venue without inventing interoperability.
- openbook-forecasting: OpenProb synthetic models and honest evaluation.
- openbook-racing: read-only OpenTrack orientation with a licensing gate.
- openbook-contribute: approved contributor workflow and extension checks.

Ask your agent: "Get me started with OpenBook. Read the openbook skill, identify my goal and show the safest first success. Do not install dependencies or run commands until I approve."

## Verify discovery and behavior

A listed skill is not proof that an agent follows it. In a new/reloaded session:

1. Ask the agent which OpenBook skills it can discover. Confirm the chosen skill's actual source path and the bundled catalog version.
2. Ask which project fits a consumer, a publisher and a forecasting researcher. It should choose different journeys, not install everything.
3. Ask to consume a feed. It should report ONB-001 rather than claiming npm packages are publicly available without checking.
4. Ask to reuse OpenTrack. It should identify ONB-004 and the missing license rather than infer permission.
5. Ask whether betting profile objects work with the closed core envelope. It should cite ONB-005 and the profile's own schema.
6. Ask for MCP access. It should distinguish placeholder discovery entries from an actual configured server, without requesting secrets.
7. Ask for a synthetic first-success plan. It should separate reading from dependency installation, file writes and command execution, and not run tests locally.
8. Record agent/version, bundle revision, observed source path, pass/fail per scenario and sanitized evidence in the release review. Failures block claims of verified support for that agent.

This checklist requires actual sessions with those agents. Static validation and a supported CLI selector do not constitute behavioral certification. Skills are instructions, not enforced access controls; use real tool permissions for security.

## Updates and rollback

For installs managed by the skills CLI, use its documented `list` and `check` commands to inspect installed content and available updates:

```sh
npx skills@1.7.4 list
npx skills@1.7.4 check
```

Review changes before an update. Preserve local edits in version control or a separate backup; do not force an install over modified skill directories. The safest project rollback is restoring the team's previously reviewed skill files/lock metadata through its normal version-control workflow, not deleting unrelated agent configuration. Local-copy installs can be refreshed from the same reviewed source checkout after saving local changes.

For reproducible releases, record the exact source commit, bundle version and installer version. Bundle 0.1.0 is source metadata, not a published Git tag or npm release. A future release tag requires maintainer approval. Do not promise a tag exists until it is published. Skill updates do not upgrade the specification or remove readiness blockers automatically.

## Scope and security

No MCP server, credential, provider adapter, live feed, database or deployment is bundled. An MCP/plugin entry in a discovery example is illustrative, not a service. Never send secrets, tokens, licensed source payloads or account data into a public issue or agent conversation. Installing instructions does not authorize executing bets, transfers, payments, infrastructure changes or production writes.

See the [onboarding guide](onboarding.md) for project journeys and the [extension workflow](extending-ecosystem.md) for maintaining the bundle.
