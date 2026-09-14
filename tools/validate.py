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
  8. maps/*.json is a JSON array of map rows (schema/maps.schema.json);
     publicKey is unique in a file; named landings must not carry reason.
  9. register/prefixes.json is a JSON array of plain propertyID tokens
     (schema/prefixes.schema.json) and includes the unknown bucket.
 10. register/fingerprint.md encoding matches the pinned fixture example.

Usage:  python3 tools/validate.py [--topic TOPIC ...]      exit 0 = conformant
"""
import hashlib, json, re, sys, glob, os, copy
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
                 "participant": "participant", "player": "player", "publisher": "publisher",
                 "lineup": "lineup", "stall": "stall", "toss": "toss", "series": "series"}
FIXTURE_TOPIC = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/fixture/(?P<id>[^/#+]+)/(?P<object>fixture|odds|market|score|grade|lineup|series)/(?P<action>[a-zA-Z]+)$")
ENTITY_TOPIC  = re.compile(r"^openbook/v1/(?P<publisher>[a-z0-9][a-z0-9-]*)/(?P<sport>[a-z0-9-]+)/(?P<object>league|season|stage|participant|player|stall|toss)/(?P<id>[^/#+]+)/(?P<action>[a-zA-Z]+)$")
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
            full = doc["action"] in ("snapshot", "create")
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
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/lineup/update",
    "openbook/v1/acme-feeds/soccer/fixture/EVT-88213/series/update",
    "openbook/v1/acme-feeds/unknown/stall/STL-4/update",
    "openbook/v1/acme-feeds/cricket/toss/TOSS-1/update",
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
    "homeTeam", "awayTeam", "tools", "openbook",
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
    voc_tick = re.compile(r"`((?:sport|market|segment|side|position):[a-z0-9:-]+)`")
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

print("8. maps files")
maps_schema_name = "maps.schema.json"
if maps_schema_name not in schemas:
    fail("schema/maps.schema.json missing")
else:
    maps_v = validator(schemas[maps_schema_name])
    maps_dir = os.path.join(ROOT, "maps")
    map_paths = sorted(glob.glob(os.path.join(maps_dir, "*.json")))
    if not map_paths:
        fail("maps/ has no JSON files")
    for path in map_paths:
        rel = os.path.relpath(path, ROOT)
        doc = json.load(open(path))
        errs = sorted(maps_v.iter_errors(doc), key=lambda e: list(e.path))
        if errs:
            for e in errs:
                fail(f"{rel}: {e.message} at /{'/'.join(map(str, e.path))}")
        elif not isinstance(doc, list):
            fail(f"{rel}: maps file must be a JSON array")
        else:
            keys = [row.get("publicKey") for row in doc if isinstance(row, dict)]
            if len(keys) != len(set(keys)):
                fail(f"{rel}: publicKey must be unique in one file")
            else:
                ok(rel)
    bad_maps = os.path.join(ROOT, "conformance", "invalid", "maps-reason-on-named.json")
    if os.path.isfile(bad_maps):
        bad_doc = json.load(open(bad_maps))
        bad_errs = list(maps_v.iter_errors(bad_doc))
        if bad_errs:
            ok("conformance/invalid/maps-reason-on-named.json  (rejected)")
        else:
            fail("conformance/invalid/maps-reason-on-named.json: expected reject but validated")

print("9. prefix file")
pref_schema_name = "prefixes.schema.json"
pref_path = os.path.join(ROOT, "register", "prefixes.json")
if pref_schema_name not in schemas:
    fail("schema/prefixes.schema.json missing")
elif not os.path.isfile(pref_path):
    fail("register/prefixes.json missing")
else:
    pref_v = validator(schemas[pref_schema_name])
    pref_doc = json.load(open(pref_path))
    pref_errs = sorted(pref_v.iter_errors(pref_doc), key=lambda e: list(e.path))
    if pref_errs:
        for e in pref_errs:
            fail(f"register/prefixes.json: {e.message} at /{'/'.join(map(str, e.path))}")
    elif "unknown" not in pref_doc:
        fail("register/prefixes.json: missing unknown bucket")
    else:
        ok("register/prefixes.json")
    bad_pref = os.path.join(ROOT, "conformance", "invalid", "prefixes-missing-unknown.json")
    if os.path.isfile(bad_pref):
        bad_doc = json.load(open(bad_pref))
        if "unknown" not in bad_doc:
            ok("conformance/invalid/prefixes-missing-unknown.json  (rejected)")
        else:
            fail("conformance/invalid/prefixes-missing-unknown.json: expected missing unknown")

print("10. fixture join recipe pin")
PINNED_SHA256 = "2b38ee78a5c6da604719b19ad86a0a6dce7deb6995cc7d210548fc39377a752c"


def _join_anchor(obj):
    if not isinstance(obj, dict):
        return None
    same = obj.get("sameAs")
    if isinstance(same, str) and same.startswith(("http://", "https://")):
        return same
    oid = obj.get("id")
    return oid if isinstance(oid, str) and oid else None


def fixture_join_preimage(doc):
    sport = (doc.get("sport") or {}).get("id")
    league = doc.get("league") or {}
    start = doc.get("startDate")
    parts = doc.get("participants")
    if not isinstance(sport, str) or not sport:
        raise ValueError("sport.id missing")
    league_anchor = _join_anchor(league)
    if not league_anchor:
        raise ValueError("league anchor missing")
    if not isinstance(start, str) or len(start) < 16:
        raise ValueError("startDate missing")
    minute = start[:16] + "Z"
    if not isinstance(parts, list) or not parts:
        raise ValueError("participants missing")
    ordered = sorted(parts, key=lambda p: p.get("order") if isinstance(p, dict) else 0)
    anchors = []
    for p in ordered:
        a = _join_anchor(p)
        if not a:
            raise ValueError("participant anchor missing")
        anchors.append(a)
    ctype = league.get("competitionType")
    if not isinstance(ctype, str) or not ctype:
        raise ValueError("competitionType missing")
    return "\n".join([sport, league_anchor, minute, ",".join(anchors), ctype]) + "\n"


fp_md = os.path.join(ROOT, "register", "fingerprint.md")
fx_path = os.path.join(ROOT, "examples", "fixture.example.json")
if not os.path.isfile(fp_md):
    fail("register/fingerprint.md missing")
elif not os.path.isfile(fx_path):
    fail("examples/fixture.example.json missing")
else:
    try:
        preimage = fixture_join_preimage(json.load(open(fx_path)))
        digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        fail(f"examples/fixture.example.json: join preimage: {e}")
        digest = None
    if digest is not None:
        if digest != PINNED_SHA256:
            fail(f"pinned join digest {digest} != {PINNED_SHA256}")
        elif PINNED_SHA256 not in open(fp_md).read():
            fail("register/fingerprint.md missing pinned SHA-256 hex")
        else:
            ok("register/fingerprint.md pin")

print()
if failures: sys.exit(f"{len(failures)} problem(s) — not conformant")
print("conformant: all checks passed")
