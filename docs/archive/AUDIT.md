# .NeoN Repository Audit

This file tracks whether implemented pieces, docs, examples, and tests agree.

## Current Symbolic State

```text
⚡ π.v0.2
● ∫ repo-audit
✓ λ.hashing
✓ λ.cas-foundation
✓ λ.proof-packets
✓ λ.lineage-traversal
✓ λ.symbolic-helpers
◐ λ.modular-decomposition
◐ λ.docs-compression
◐ λ.descendant-traversal
✗ θ.runtime-drift
† ƒ src/neon/cli_v2.py
```

## Implemented Pieces

| Piece | Status | Evidence |
| --- | --- | --- |
| Canonical CLI | Partial | `src/neon/cli.py` exists, but `src/neon/cli_v2.py` still creates drift. |
| Artifact primitives | Active | `src/neon/artifact.py` extracted. |
| CAS primitives | Active | `src/neon/cas.py` extracted. |
| Proof helpers | Active | `src/neon/proof.py` extracted. |
| Lineage graph | Active | `src/neon/lineage.py` exists. |
| Symbolic helpers | Active | `src/neon/symbols.py` exists. |
| Living chain | Active | `examples/chain/` exists. |
| Golden objects | Partial | `examples/golden/` exists; hashes and proof packets still need freezing. |
| Spec v0.1 | Partial | Schemas exist; spec needs examples and hash fixtures. |
| Trust protocol | Doctrine | OpenTimestamps and signed Git guidance exists, not automated. |

## Tests Present

- module invariants
- artifact validation
- deterministic hashing
- CAS fetch roundtrip
- invalid CAS URI rejection
- negative proof tamper test
- end-to-end WorkLedger flow
- lineage graph tests

## Gaps

1. `cli.py` still duplicates logic now extracted into modules.
2. `src/neon/cli_v2.py` should be removed or archived.
3. Descendant traversal is not exposed through CLI.
4. Symbolic output is not yet available from CLI.
5. Golden hashes are not frozen.
6. README is compressed but docs still overlap.
7. No GitHub Actions CI file yet.
8. No release checklist execution script yet.

## Decision

Continue cleanup in this order:

1. remove runtime drift,
2. add descendant traversal,
3. add symbolic status output,
4. wire CLI to extracted modules,
5. freeze golden hashes,
6. add CI,
7. compress overlapping docs.
