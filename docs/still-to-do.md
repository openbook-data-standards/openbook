# Still to do

Phase B questions on this branch are recorded through **Q55**. **Q56** was
log only: no schema, examples, or CI in this patch. Do not add wire names to
schemas until that is asked.

## Later PRs (decided, not built)

- **Q50** — one-way docs-vs-schema name CI (spec/docs names MUST exist on a
  schema).
- **Q55** — schema-diff CI for frozen majors only (1.0+).

## Not decided here

- Wire/schema for Q46–Q49 (`snapshotComplete`, `heartbeat` / `heartbeatMs`,
  410, `conflated`, `ttl`, discovery JSON).

## Done on this walk (Q32–Q55)

Q32 FULL-TRANSITIVE · Q33 eight MUST (prose) · Q34 unknown/other · Q35 never
reuse · Q36 deprecation window · Q37 closed write / open read · Q38 camelCase
· Q39 decimal strings · Q40 corpus · Q41 GBFS principles · Q42 AsyncAPI ·
Q43 takedown = marketStatus + tombstone · Q44 `baseCurrency` · Q45 market
`limit` / most-specific-wins · Q46 `snapshotComplete` / `heartbeat` / 410 ·
Q47 `conflated` · Q48 `ttl` · Q49 GBFS discovery · Q50 name CI later · Q51 no
consumer schema · Q52 CloudEvents never · Q53 no DNS ids · Q54 no in-repo
OpenAPI · Q55 schema-diff CI at 1.0.
