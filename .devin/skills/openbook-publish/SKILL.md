---
name: openbook-publish
description: Scaffold an OpenBook publisher safely with openbook-starter, inspect discovery and snapshot documents, and distinguish scaffolding from hosting a complete feed.
---

# Publish OpenBook documents

## Sources

Read the [starter README](https://github.com/openbook-data-standards/openbook-starter/blob/main/README.md), [starter manifest](https://github.com/openbook-data-standards/openbook-starter/blob/main/pyproject.toml), [onboarding journey](https://github.com/openbook-data-standards/openbook/blob/main/docs/onboarding.md) and [readiness catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Read source CLI behavior before recommending flags.

## Workflow

1. Confirm the user wants publisher documents, not a server, importer or provider adapter. Inspect target rules and choose Python 3.11+ in an isolated environment.
2. Check the current distribution. The repository is public and documents HTTPS Git installation; no PyPI release is established by the catalog. Prefer a reviewed HTTPS checkout and record its commit.
3. Ask approval for installing the reviewed source and writing to an empty scratch directory. Agree on publisher id, name, currency and base URL. An example.invalid address is a placeholder, not hosted infrastructure.
4. Run openbook start only with approved values, --no-input, an explicit --dir and --no-workflow. Never use --force over existing files. Its CLI creates an openbook directory beneath the chosen root.
5. Inspect publisher.json, discovery.json and snapshot.json. The initial snapshot is the publisher document, not a complete sports/odds feed. Ensure discovery names only endpoints actually intended to exist; verify their real paths before publication.
6. Explain separately what hosting, ongoing publication and source translation require. The starter translations extra pulls the tagged translation kernel from Git; a separate tagged install is also fine if authorized. Do not enable scheduled workflows implicitly.

## Evidence

Show sanitized output paths, publisher/source identity, base currency and exact discovery snapshot URL. State that --no-workflow avoided automation, that no files were uploaded and that no live feed was started. Capture the reviewed source commit. Stop and name a blocker if the destination is not empty or a distribution cannot be verified.

## Boundaries

Do not run tests locally; CI owns test execution. Follow repository rules and obtain permission for installs, writes, hosting and any remote operation. Never overwrite user files, infer credentials, publish licensed payloads or promise a complete feed from scaffolding. Do not alter the standard or publish a package as part of this skill.
