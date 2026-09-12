# Versioning

OpenBook uses semantic versioning: `MAJOR.MINOR.PATCH`.

- **MAJOR** — a breaking change to the wire: a field removed or retyped, a
  required field added, a canonical id semantics change.
- **MINOR** — backward-compatible additions: new optional fields, new vocabulary
  entries (new sports, market types, segments), new live message types.
- **PATCH** — clarifications, documentation, examples; no schema change.

Rules:

- Every object and message carries `openbook_version`, the version it was
  produced against.
- Consumers **MUST** ignore unknown `x_`-prefixed fields, so MINOR additions never
  break an older consumer.
- Canonical ids are permanent. An id is deprecated, never deleted or re-pointed.
- Pre-1.0 (`0.x`) the wire may still change between MINOR versions; the `-draft`
  suffix marks a version that is not yet frozen.

The current version is recorded in [`CHANGELOG.md`](CHANGELOG.md).
