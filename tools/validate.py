#!/usr/bin/env python3
"""OpenBook validator — makes "OpenBook-conformant" a testable claim.

Checks, in order:
  1. every schema in schema/ is itself a valid JSON Schema (draft 2020-12)
  2. every $ref into common.schema.json resolves; every `required` names a real property
  3. no closed vocabulary is declared outside common.schema.json (single enum registry)
  4. every example in examples/ validates:
       - a message (has object+action) validates against change.schema.json, and its
         `changes` validates against the object's schema — in full for snapshot/create,
         as a Merge Patch (required relaxed) for update/change
       - a document validates against the schema named by its file stem
  5. stream topics follow the fixture-first grammar  openbook/v1/<publisher>/<sport>/fixture/<id>/<object>/<action>

Usage:  python3 tools/validate.py [--topic TOPIC ...]      exit 0 = conformant
"""
import json, re, sys, glob, os, copy
try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:
    sys.exit("needs: pip install 'jsonschema>=4.18' referencing")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR, EXAMPLE_DIR = os.path.join(ROOT, "schema"), os.path.join(ROOT, "examples")
OBJECT_SCHEMA = {"fixture": "fixture", "odds": "odds_change", "market": "market", "score": "score",
                 "grade": "grade", "league": "league", "season": "season", "stage": "stage",
                 "participant": "participant", "player": "player", "publisher": "publisher"}
FIXTURE_TOPIC = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/fixture/(?P<id>[^/#+]+)/(?P<object>fixture|odds|market|score|grade)/(?P<action>[a-z]+)$")
ENTITY_TOPIC  = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/(?P<object>league|season|stage|participant|player)/(?P<id>[^/#+]+)/(?P<action>[a-z]+)$")
PUB_TOPIC     = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/publisher/(?P<action>[a-z]+)$")

failures = []
def fail(msg): failures.append(msg); print("  FAIL", msg)
def ok(msg): print("  ok  ", msg)

schemas = {os.path.basename(p): json.load(open(p)) for p in sorted(glob.glob(f"{SCHEMA_DIR}/*.json"))}
registry = Registry()
for name, s in schemas.items():
    res = Resource(contents=s, specification=DRAFT202012)
    registry = registry.with_resource(name, res)
    if "$id" in s: registry = registry.with_resource(s["$id"], res)
# relative refs like "common.schema.json#/$defs/x" resolve against the schema's $id base
BASE = "https://openbook-data-standards.github.io/openbook/schema/"
registry = registry.with_resource(BASE + "common.schema.json", Resource(contents=schemas["common.schema.json"], specification=DRAFT202012))

def validator(schema): return Draft202012Validator(schema, registry=registry)

print("1. schemas are valid JSON Schema")
for name, s in schemas.items():
    try: Draft202012Validator.check_schema(s); ok(name)
    except Exception as e: fail(f"{name}: {e.message if hasattr(e,'message') else e}")

print("2. $refs resolve and required fields exist")
defs = set(schemas["common.schema.json"]["$defs"])
for name, s in schemas.items():
    for m in re.finditer(r'common\.schema\.json#/\$defs/([A-Za-z0-9_]+)', json.dumps(s)):
        if m.group(1) not in defs: fail(f"{name}: unresolved $ref common#/$defs/{m.group(1)}")
    props = set(s.get("properties", {}))
    for r in s.get("required", []):
        if r not in props: fail(f"{name}: required '{r}' is not a property")
ok("checked")

print("3. enums live only in common.schema.json")
def walk(o, path=""):
    if isinstance(o, dict):
        if "enum" in o: yield path
        for k, v in o.items(): yield from walk(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{path}[{i}]")
for name, s in schemas.items():
    if name == "common.schema.json": continue
    for p in walk(s): fail(f"{name}: inline enum at {p} — move it to common.schema.json $defs")
ok("checked")

ENVELOPE_FIELDS = ("openbookVersion", "sequence", "dateModified")

def for_changes(schema, full):
    """A document schema as it applies to a message's `changes`. The envelope
    already carries openbookVersion/sequence/dateModified, so those are never
    required inside `changes`. For snapshot/create the rest stays required; for
    update/change nothing is required (Merge Patch)."""
    s = copy.deepcopy(schema); s.pop("$id", None)
    req = [] if not full else [r for r in s.get("required", []) if r not in ENVELOPE_FIELDS]
    if req: s["required"] = req
    else: s.pop("required", None)
    return s

print("4. examples validate")
change_v = validator(schemas["change.schema.json"])
for path in sorted(glob.glob(f"{EXAMPLE_DIR}/*.json")):
    name = os.path.basename(path); doc = json.load(open(path))
    if "object" in doc and "action" in doc:
        errs = sorted(change_v.iter_errors(doc), key=lambda e: e.path)
        for e in errs: fail(f"{name}: envelope: {e.message} at /{'/'.join(map(str,e.path))}")
        target = OBJECT_SCHEMA.get(doc["object"])
        if target and f"{target}.schema.json" not in schemas:
            fail(f"{name}: no schema for object '{doc['object']}' (expected schema/{target}.schema.json)"); target = None
        if target:
            s = schemas[f"{target}.schema.json"]
            full = doc["action"] in ("snapshot", "create") and doc["object"] != "odds"
            v = validator(for_changes(s, full))
            for e in sorted(v.iter_errors(doc["changes"]), key=lambda e: e.path):
                fail(f"{name}: changes vs {target} ({'full' if full else 'patch'}): {e.message} at /changes/{'/'.join(map(str,e.path))}")
        if not errs: ok(f"{name}  ({doc['object']}/{doc['action']})")
    else:
        stem = name.split(".")[0]; s = schemas.get(f"{stem}.schema.json")
        if not s: fail(f"{name}: no schema for document type '{stem}'"); continue
        errs = sorted(validator(s).iter_errors(doc), key=lambda e: e.path)
        for e in errs: fail(f"{name}: {e.message} at /{'/'.join(map(str,e.path))}")
        if not errs: ok(f"{name}  (document: {stem})")

print("5. topic grammar")
objects = set(schemas["common.schema.json"]["$defs"]["objectType"]["enum"])
actions = set(schemas["common.schema.json"]["$defs"]["action"]["enum"])
def check_topic(t):
    m = FIXTURE_TOPIC.match(t) or ENTITY_TOPIC.match(t) or PUB_TOPIC.match(t)
    if not m: return "does not match grammar (fixture-first: .../<sport>/fixture/<id>/<object>/<action>)"
    g = m.groupdict(); obj = g.get("object", "publisher")
    if g["action"] not in actions: return f"unknown action '{g['action']}'"
    if g["action"] == "change" and obj != "odds": return "`change` is only for odds"
    return None
topics = sys.argv[sys.argv.index("--topic")+1:] if "--topic" in sys.argv else [
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/odds/change",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/fixture/update",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/market/update",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/grade/create",
    "openbook/v1/acme-feeds/soccer/league/LG-17/update",
    "openbook/v1/acme-feeds/publisher/update",
]
for t in topics:
    err = check_topic(t); fail(f"topic {t}: {err}") if err else ok(t)

print()
if failures: sys.exit(f"{len(failures)} problem(s) — not conformant")
print("conformant: all checks passed")
