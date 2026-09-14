# Agent rules — OpenBook

OpenBook is an **important public open-source standard**. Treat it as frozen
unless a human has explicitly asked you to implement a named change.

## Do not invent anything

**Number one rule.** If a field name, object, enum, ISO, or behaviour was not
asked and answered, do not add it. Ask. Wait.

## Never change unless told

Do **not** edit spec, schemas, examples, vocabularies, conformance, site HTML,
tools, git history, branches, or pull requests unless the human has clearly said
to implement that change (for example: “add this file”, “record Q12”, “open a
PR for X”).

A question is not permission. A product idea is not permission. “Should we…”
is not permission. Inferring from a run name or a parallel agent is not
permission.

Default: **answer only**. No files, no commits, no PRs, no “helpful” extras.

## Ask first — one question at a time

Before doing **anything** (including writing files, running mutating git,
or opening a PR):

1. Ask **one** detailed question.
2. Wait for the answer.
3. Ask the next question if still blocked.
4. Only then do the exact work that was authorised.

Do not batch questions. Do not skip the queue because the task “seems obvious”.

## What you may do without asking

- Read the repo.
- Answer a question using what is already in the repo.
- Say what you would change, without changing it.

## After authorisation

Do the smallest change that matches the answer. Do not expand scope. Do not
touch unrelated files. Do not “finish” adjacent work.
