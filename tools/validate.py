#!/usr/bin/env python3
"""OpenBook validator — makes "OpenBook-conformant" a testable claim.

Checks, in order:
  1. every schema in schema/ is itself a valid JSON Schema (draft 2020-12)
  2. every $ref into common.schema.json resolves; every `required` names a real property
  3. no closed vocabulary is declared outside common.schema.json (single enum registry)
  4. every example in examples/ validates:
       - a message (has object+action) validates against change.schema.json, and its
         `changes` validates against the object's schema — in full for snapshot/create,
         as a Merge Patch (required relaxed) for update/change/snapshotComplete/heartbeat
       - a document validates against the schema named by its file stem
  5. stream topics follow the fixture-first grammar  openbook/v1/<publisher>/<sport>/fixture/<id>/<object>/<action>
  6. conformance/manifest.json: valid paths exist; invalid cases are rejected
  7. one-way name check (Q50): camelCase / property-like names in spec and
     selected docs MUST exist on a schema (properties, $defs, or enums). Extra
     schema fields are allowed. The decision log is history and is not scanned.
  8. protocol-fit gates (Q57+): encoding and “never” verdicts the schemas
     can prove.

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
FIXTURE_TOPIC = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/fixture/(?P<id>[^/#+]+)/(?P<object>fixture|odds|market|score|grade)/(?P<action>[a-zA-Z]+)$")
ENTITY_TOPIC  = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/(?P<object>league|season|stage|participant|player)/(?P<id>[^/#+]+)/(?P<action>[a-zA-Z]+)$")
PUB_TOPIC     = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/publisher/(?P<action>[a-zA-Z]+)$")

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
    update/change/snapshotComplete/heartbeat nothing is required (Merge Patch)."""
    s = copy.deepcopy(schema); s.pop("$id", None)
    req = [] if not full else [r for r in s.get("required", []) if r not in ENVELOPE_FIELDS]
    if req: s["required"] = req
    else: s.pop("required", None)
    return s

change_v = validator(schemas["change.schema.json"])

def instance_errors(path):
    """Schema errors for one document or message. Empty list = valid."""
    name = os.path.basename(path)
    doc = json.load(open(path))
    out = []
    if "object" in doc and "action" in doc:
        errs = sorted(change_v.iter_errors(doc), key=lambda e: e.path)
        for e in errs:
            out.append(f"{name}: envelope: {e.message} at /{'/'.join(map(str, e.path))}")
        target = OBJECT_SCHEMA.get(doc["object"])
        if target and f"{target}.schema.json" not in schemas:
            out.append(f"{name}: no schema for object '{doc['object']}' (expected schema/{target}.schema.json)")
            target = None
        if target and "changes" in doc:
            s = schemas[f"{target}.schema.json"]
            full = doc["action"] in ("snapshot", "create") and doc["object"] != "odds"
            v = validator(for_changes(s, full))
            for e in sorted(v.iter_errors(doc["changes"]), key=lambda e: e.path):
                out.append(f"{name}: changes vs {target} ({'full' if full else 'patch'}): {e.message} at /changes/{'/'.join(map(str, e.path))}")
    else:
        stem = name.split(".")[0]
        s = schemas.get(f"{stem}.schema.json")
        if not s:
            return [f"{name}: no schema for document type '{stem}'"]
        for e in sorted(validator(s).iter_errors(doc), key=lambda e: e.path):
            out.append(f"{name}: {e.message} at /{'/'.join(map(str, e.path))}")
    return out

print("4. examples validate")
for path in sorted(glob.glob(f"{EXAMPLE_DIR}/*.json")):
    name = os.path.basename(path)
    errs = instance_errors(path)
    for e in errs:
        fail(e)
    if not errs:
        doc = json.load(open(path))
        if "object" in doc and "action" in doc:
            ok(f"{name}  ({doc['object']}/{doc['action']})")
        else:
            ok(f"{name}  (document: {name.split('.')[0]})")

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
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/fixture/snapshotComplete",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/market/update",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/grade/create",
    "openbook/v1/acme-feeds/soccer/league/LG-17/update",
    "openbook/v1/acme-feeds/publisher/update",
    "openbook/v1/acme-feeds/publisher/heartbeat",
]
for t in topics:
    err = check_topic(t); fail(f"topic {t}: {err}") if err else ok(t)

print("6. conformance corpus")
man_path = os.path.join(ROOT, "conformance", "manifest.json")
man = json.load(open(man_path))
for case in man["valid"]:
    p = os.path.join(ROOT, case["path"])
    if not os.path.isfile(p):
        fail(f"manifest valid missing: {case['path']}")
    else:
        ok(f"valid {case['path']}")
for case in man["invalid"]:
    p = os.path.join(ROOT, case["path"])
    if not os.path.isfile(p):
        fail(f"manifest invalid missing: {case['path']}")
        continue
    errs = instance_errors(p)
    if errs:
        ok(f"{case['path']}  (rejected)")
    else:
        fail(f"{case['path']}: expected reject ({case.get('reason', '')}) but validated")

print("7. docs names exist on a schema (Q50, one-way)")
TICK = re.compile(r"`([^`]+)`")
IDENT = re.compile(r"^[a-z][a-zA-Z0-9]*$")
# Not JSON fields: protocol, literals, foreign vocab, ISO 639 examples.
NOT_FIELDS = frozenset({
    "http", "https", "urn", "null", "true", "false", "spec", "version",
    "en", "es", "v1", "since",
    "homeTeam", "awayTeam", "tools",
})
NAME_DOCS = (
    os.path.join(ROOT, "spec", "openbook.md"),
    os.path.join(ROOT, "spec", "asyncapi.yaml"),
    os.path.join(ROOT, "docs", "building-blocks.md"),
    os.path.join(ROOT, "docs", "still-to-do.md"),
)

def schema_names():
    props, enums, defs, stems = set(), set(), set(), set()
    def walk(o):
        if isinstance(o, dict):
            if "$defs" in o and isinstance(o["$defs"], dict):
                defs.update(o["$defs"].keys())
            if "properties" in o and isinstance(o["properties"], dict):
                props.update(k for k in o["properties"] if not str(k).startswith("@"))
            if "enum" in o and isinstance(o["enum"], list):
                for x in o["enum"]:
                    s = str(x)
                    enums.add(s)
                    enums.add(s.split(":")[-1])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for name, s in schemas.items():
        stems.add(name.removesuffix(".schema.json"))
        walk(s)
    voc_dir = os.path.join(ROOT, "vocabularies")
    voc_tick = re.compile(r"`((?:sport|market|segment|side):[a-z0-9:-]+)`")
    for p in glob.glob(os.path.join(voc_dir, "*.md")):
        for m in voc_tick.finditer(open(p).read()):
            s = m.group(1)
            enums.add(s)
            enums.add(s.split(":")[-1])
    return props | enums | defs | stems

known_names = schema_names()
mentioned = {}
for path in NAME_DOCS:
    rel = os.path.relpath(path, ROOT)
    for i, line in enumerate(open(path), 1):
        for raw in TICK.findall(line):
            if "." in raw:
                continue  # file / version ticks, not field names
            tok = raw.split()[0].split("=")[0].split("/")[0].split(":")[0].rstrip("[]{}(),.*")
            if IDENT.match(tok) and tok not in NOT_FIELDS:
                mentioned.setdefault(tok, []).append(f"{rel}:{i}")
missing_names = sorted(n for n in mentioned if n not in known_names)
if missing_names:
    for n in missing_names:
        fail(f"name `{n}` in docs is not on a schema ({mentioned[n][0]})")
else:
    ok(f"{len(mentioned)} documented names present on a schema")

print("8. protocol fit")
# Q57 — v1 is JSON; no second encoding tree in this repo.
asyncapi_path = os.path.join(ROOT, "spec", "asyncapi.yaml")
asyncapi_text = open(asyncapi_path).read()
if re.search(r"(?m)^defaultContentType:\s*application/json\s*$", asyncapi_text):
    ok("Q57 AsyncAPI defaultContentType is JSON")
else:
    fail("Q57 AsyncAPI defaultContentType must be application/json")
schema_files = [os.path.basename(p) for p in glob.glob(os.path.join(SCHEMA_DIR, "*"))]
non_json = [n for n in schema_files if not n.endswith(".schema.json")]
if non_json:
    fail(f"Q57 schema/ must be *.schema.json only: {non_json}")
else:
    ok("Q57 schema/ is JSON Schema only")
binary_hits = []
for pat in ("**/*.proto", "**/*.sbe.xml"):
    for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if rel.split(os.sep)[0] == ".git":
            continue
        binary_hits.append(rel)
if binary_hits:
    fail(f"Q57 binary schema in repo before 1.0: {binary_hits}")
else:
    ok("Q57 no protobuf/SBE files in the spec repo")

changes_type = schemas["change.schema.json"].get("properties", {}).get("changes", {}).get("type")
if changes_type == "object":
    ok("Q58 changes is a Merge Patch object")
else:
    fail("Q58 change.schema.json changes must be type object (not a JSON Patch array)")

money = schemas["common.schema.json"]["$defs"]["money"]
money_props = set(money.get("properties", {}))
if money.get("required") == ["amount"] and money_props == {"amount"} and money.get("additionalProperties") is False:
    ok("Q59 money is amount only (no per-object currency)")
else:
    fail("Q59 money must be {amount} only with additionalProperties false")

ACTIONS = {"snapshot", "create", "update", "delete", "change", "snapshotComplete", "heartbeat"}
action_enum = set(schemas["common.schema.json"]["$defs"]["action"]["enum"])
if action_enum == ACTIONS:
    ok("Q60 action enum is publication actions only (no TestRequest)")
else:
    fail(f"Q60 action enum drifted: {sorted(action_enum)}")

disc = schemas["discovery.schema.json"]
if set(disc.get("required", [])) == {"lastUpdated", "ttl", "feeds"} and "data" not in disc.get("properties", {}) and disc.get("additionalProperties") is False:
    ok("Q61 discovery is flat (no nested data wrapper)")
else:
    fail("Q61 discovery must be lastUpdated, ttl, feeds with additionalProperties false")

change_props = set(schemas["change.schema.json"].get("properties", {}))
if "specversion" not in change_props and schemas["change.schema.json"].get("additionalProperties") is False:
    ok("Q62 envelope has no CloudEvents attributes")
else:
    fail("Q62 change envelope must not include CloudEvents attributes")

print()
if failures: sys.exit(f"{len(failures)} problem(s) — not conformant")
print("conformant: all checks passed")
