#!/usr/bin/env python3
"""End-to-end synthetic OpenBook flow, runnable from this checkout.

Simulates what the ecosystem tools do, using the repo's own example documents:

  publisher (openbook-starter output) -> adapter emits a change envelope
  (openbook-translate helpers) -> consumer applies the RFC 7386 Merge Patch
  and validates the updated document (any conformant consumer).

Requires only jsonschema (+ referencing). Not a test runner; a demonstration.
"""

import copy
import json
import pathlib

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def registry():
    schemas = {p.name: p for p in (ROOT / "schema").glob("*.schema.json")}
    return Registry().with_resources(
        [(name, Resource.from_contents(load(f"schema/{name}"))) for name in schemas]
    )


def merge_patch(target, patch):
    """RFC 7386."""
    if not isinstance(patch, dict):
        return copy.deepcopy(patch)
    result = copy.deepcopy(target) if isinstance(target, dict) else {}
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = merge_patch(result.get(key), value)
    return result


def main():
    reg = registry()

    # 1. Snapshot state: the fixture a consumer already holds.
    fixture = load("examples/fixture.example.json")

    # 2. The wire message: a fixture update envelope from the publisher.
    envelope = load("examples/fixture_update.example.json")
    Draft202012Validator(load("schema/change.schema.json"), registry=reg).validate(envelope)
    print(f"envelope ok: {envelope['object']}/{envelope['action']} seq={envelope['sequence']} id={envelope['id']}")
    assert envelope["id"] == fixture["id"], "envelope targets a different fixture"

    # 3. Consumer applies the Merge Patch.
    updated = merge_patch(fixture, envelope["changes"])

    # 4. The patched document must still validate against the object schema.
    Draft202012Validator(load("schema/fixture.schema.json"), registry=reg).validate(updated)
    print(f"patched fixture ok: startDate {fixture['startDate']} -> {updated['startDate']}")
    print(f"extension preserved: x_reason={updated['x_reason']!r}")


if __name__ == "__main__":
    main()
