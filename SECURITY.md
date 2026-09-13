# Security policy

OpenBook is a data **specification**, not a running service, so security has a
specific meaning here: the spec, schemas, and tooling must not lead a careful
implementer into an unsafe implementation. Runtime security of any feed belongs
to the systems that implement OpenBook, not to this repository.

## What the standard secures

- **The schema is the input boundary.** Object schemas are closed
  (`additionalProperties: false`), so an unknown field is rejected rather than
  silently trusted, and `x_`-prefixed vendor extras are the only escape hatch.
  Primitives are pinned to types that already have safe parsers — odds and lines
  are decimal **strings**, not floats; country is ISO 3166; time is RFC 3339. A
  schema that fails to constrain a field it should is a security bug in the spec.
- **Canonical id integrity.** Ids, list-values, and field names are never
  re-pointed or reused once frozen; they are only deprecated. Re-pointing a
  published id would let a stale consumer mis-resolve an entity, so id stability
  is a security property of the standard, not only an ergonomic one.

## What the standard delegates (deployment's responsibility)

OpenBook deliberately says nothing about these; an implementer MUST provide them:

- **Transport encryption** — serve feeds over TLS. The spec names topics and
  documents, not sockets.
- **Authentication & authorisation** — who may publish to, or subscribe to, a
  feed.
- **Rate limiting and abuse control**, and retention limits on `since=` pulls.
- **Integrity of fetched schemas** — pin or verify the schema files you validate
  against, so a conformant parser checks input against authentic contracts.

## Reporting a problem

If you find a problem in the specification, schemas, or tooling that could lead
to unsafe implementations — for example a schema that fails to constrain a
field it should, or validator behavior that passes malformed data — please
report it privately:

- GitHub: **Security → Report a vulnerability** on this repository, or
- open a regular issue if the problem is not sensitive.

Please do not disclose a sensitive issue publicly until it has been addressed.
