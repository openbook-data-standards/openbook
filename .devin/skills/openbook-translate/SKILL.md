---
name: openbook-translate
description: Build or explain OpenBook provider adapters with explicit mapping tables, preserved native identity, schema validation, quarantine reasons, gap reports and envelope helpers.
---

# Translate one vendor record

## Sources

Read the [kernel README and adapter contract](https://github.com/openbook-data-standards/openbook-translate/blob/main/README.md), [manifest](https://github.com/openbook-data-standards/openbook-translate/blob/main/pyproject.toml), [core specification](https://github.com/openbook-data-standards/openbook/blob/main/spec/openbook.md) and [catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Consult the source at the chosen release, not only main, before coding against it.

## Workflow

1. Establish the permitted synthetic or licensed input, source id, adapter name, exact kernel release and pinned spec version. Python 3.11+ is required with jsonschema and referencing.
2. If installation is authorized, use the reviewed Git tag (documented v0.1.0), not an assumed PyPI package. Vendor-specific adapters live separately; the synthetic acme adapter is not a production vendor integration.
3. Read Translator, Documents, Vendor and Quarantine contracts. Translate one record at a time; inspect parsed-input and reverse-support behavior. Preserve native identity in identifier using the adapter's propertyID.
4. Use declarative mapping tables and existing vocabularies. Count unmapped values and retain source evidence instead of silently dropping records or inventing canonical mappings. Distinguish vocabulary catch-alls from quarantined unsupported records.
5. Use documented quarantine reasons for invalid/unsupported input. Inspect schema validation and envelope helpers at the pinned version; do not hand-invent transport fields or sequence semantics.
6. With consent, demonstrate one synthetic success and one unmapped/quarantine case; show the gap report. Put adapter contract-suite and golden-capture verification in CI, without using real proprietary payloads in public fixtures.

## Evidence

Return exact kernel/spec revision, sanitized input, translated document, preserved native id, quarantine reason and counted gap. For reverse support, state what was actually observed; do not claim round-trip correctness from code inspection alone. Name missing mapping decisions and their required evidence.

## Boundaries

Do not run tests locally; CI owns test execution. Do not install, change adapters, retain source payloads or execute examples without approval. Never guess identities, skip unmapped records, expose credentials or copy licensed feeds into public code. The kernel supplies tools, not provider clients, mapping decisions or a hosted publisher.
