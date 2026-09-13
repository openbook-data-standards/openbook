# Versioning

OpenBook uses semantic versioning: `MAJOR.MINOR.PATCH`.

- **MAJOR** — a breaking change to the wire: a field removed or retyped, a
  required field added, a canonical id semantics change.
- **MINOR** — backward-compatible additions: new optional fields, new vocabulary
  entries (new sports, market types, segments), new live message types.
- **PATCH** — clarifications, documentation, examples; no schema change.

## Compatibility within a frozen major (Q32)

Once a **major is frozen** (1.0 and later), compatibility is **FULL-TRANSITIVE**:
every minor of that major is readable by a consumer built against any other
minor of that major, both directions, checked against all prior minors of that
major.

In practice:

- New fields MUST be optional or defaulted.
- No field is re-typed or removed within a major.
- The required set is permanent within a major (keep it small).

This is the Confluent Schema Registry FULL + TRANSITIVE *idea*, adapted to
JSON Schema (instance compatibility, not Avro reader/writer resolution). A
machine schema-diff gate is not part of this decision.

## Rules

- Every object and message carries `openbook_version`, the version it was
  produced against.
- Consumers **MUST** ignore unknown `x_`-prefixed fields, so MINOR additions never
  break an older consumer.
- Canonical ids, list-values and field names are permanent once shipped in a
  frozen version. They are deprecated, never deleted or re-pointed, and
  **never reused** for a new meaning (Q35).
- Pre-1.0 (`0.x`) the wire may still change between MINOR versions; the `-draft`
  suffix marks a version that is not yet frozen. Q32 is the intended 1.0
  contract; it is not a 0.x freeze.

The current version is recorded in [`CHANGELOG.md`](CHANGELOG.md).
