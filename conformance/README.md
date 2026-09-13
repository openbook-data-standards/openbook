# Conformance corpus

Language-agnostic JSON cases that any OpenBook implementation MUST pass.
The Python file [`../tools/validate.py`](../tools/validate.py) is **one
runner**, not a language oracle (Q40).

- **Valid** cases are the documents in [`../examples/`](../examples/). A
  conformant consumer and a conformant publisher both accept them.
- **Invalid** cases in [`invalid/`](invalid/) MUST be rejected. Each entry
  in [`manifest.json`](manifest.json) states why.

Cases are part of the specification (CC BY 4.0). A runner in any language may
read `manifest.json` and apply the schemas in [`../schema/`](../schema/).
Reference libraries, if published later, are optional and Apache-2.0.
