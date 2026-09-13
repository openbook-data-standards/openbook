# Deprecated names (Q35 / Q36)

Once a frozen id, list-value, field name, or message type is shipped it is
never reused. A deprecation is machine-readable: `name`, `reason`,
`replacement`, `sunset` (an RFC 3339 full-date). The name MUST NOT be
removed from the live set until a MAJOR after that sunset.

Registry: [`deprecated.json`](deprecated.json). Empty until something is
retired. Each array item matches `common.schema.json#/$defs/deprecation`.
