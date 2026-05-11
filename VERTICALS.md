# .NeoN Main Verticals

This document defines the major product and protocol verticals for `.NeoN`.

The purpose is to prevent the project from becoming one tangled idea pile.

Each vertical has a job.
Each vertical must strengthen the continuity loop.

```text
create -> derive -> hash -> store -> export -> verify -> inspect
```

## North Star

.NeoN preserves the lineage of human-origin intelligence through transformation.

## Vertical 1 — Artifact Core

### Purpose
Define what a `.neon` object is.

### Owns
- artifact shape
- artifact IDs
- creator metadata
- origin statements
- lifecycle events
- parent references
- canonical JSON

### Current files
- `src/neon/artifact.py`
- `spec/v0.1/artifact.schema.json`
- `SPEC_NEON_FILE_FORMAT.md`

### Success condition
A `.neon` artifact is readable, validatable, portable, and deterministic.

---

## Vertical 2 — Continuity Graph

### Purpose
Make artifacts traceable across transformation.

### Owns
- ancestry traversal
- descendant traversal
- lineage depth
- graph export
- parent/child topology
- continuity trees

### Current files
- `src/neon/lineage.py`
- `LINEAGE_SEMANTICS.md`
- `examples/chain/`

### Success condition
A user can inspect where an artifact came from and what derived from it.

---

## Vertical 3 — Proof and Verification

### Purpose
Prove that artifacts and proof packets have not been silently altered.

### Owns
- proof packets
- manifest verification
- tamper detection
- negative verification tests
- release verification gates

### Current files
- `src/neon/proof.py`
- `VERIFICATION.md`
- `TRUST_PROTOCOL.md`
- `spec/v0.1/proof-packet.schema.json`

### Success condition
A proof packet can be exported, verified, and rejected when tampered with.

---

## Vertical 4 — Storage and CAS

### Purpose
Make artifacts locally durable and content-addressed.

### Owns
- `.neon-vault/`
- SQLite ledger
- CAS object paths
- `.neon://sha256/<digest>` URIs
- byte-preserving fetch/store

### Current files
- `src/neon/storage.py`
- `src/neon/cas.py`
- `CAS.md`
- `CANONICAL_HASHING.md`

### Success condition
An artifact can be stored by hash and fetched back without byte drift.

---

## Vertical 5 — Metrics and Topology

### Purpose
Describe continuity structure without turning it into popularity, market value, or legal ownership scoring.

### Owns
- continuity vectors
- pressure vectors
- derivation ratios
- influence ratios
- topology reports

### Current files
- `src/neon/metrics.py`
- `DERIVATIVES.md`

### Success condition
A user can inspect structural continuity metrics for an artifact.

---

## Vertical 6 — Symbolic Compression

### Purpose
Compress project, artifact, workflow, and agent state without losing semantic clarity.

### Owns
- Carl Sowers Symbolic Notation System
- symbolic status blocks
- symbolic CLI output
- continuity report compression

### Current files
- `CS_SYMBOLIC_NOTATION.md`
- `src/neon/symbols.py`
- `examples/symbolic-state-example.md`
- `reports/CONTINUITY_REPORT_TEMPLATE.md`

### Success condition
Symbols clarify state faster than prose without becoming cryptic.

---

## Vertical 7 — Runtime and CLI

### Purpose
Expose the protocol through a usable local command surface.

### Owns
- `neon` command
- demo loop
- user workflow commands
- command routing
- human-readable output

### Current files
- `src/neon/cli.py`
- `WORKLEDGER_COMMANDS.md`
- `README.md`

### Success condition
A new user can run `neon demo` and understand the continuity loop.

---

## Vertical 8 — Prototype Experience

### Purpose
Turn primitives into a demoable workflow.

### Owns
- `neon demo`
- walkthrough docs
- onboarding flow
- example artifacts
- proof packet demonstration

### Current files
- `examples/chain/`
- `tests/test_demo_loop.py`
- `README.md`

### Success condition
A user can run one command, inspect lineage, verify proof, and understand what happened.

---

## Vertical 9 — Governance and Project Discipline

### Purpose
Prevent drift while allowing controlled evolution.

### Owns
- gravity anchor
- roadmap
- audit ledger
- structure rules
- contribution rules
- docs compression

### Current files
- `GRAVITY_ANCHOR.md`
- `ROADMAP_V0_2.md`
- `STRUCTURE.md`
- `AUDIT.md`
- `CONTRIBUTING.md`
- `docs/README.md`

### Success condition
The repo can evolve without losing its center.

---

## Vertical 10 — Future Topology

### Purpose
Hold powerful future ideas without contaminating the current prototype.

### Owns
- browser substrate ideas
- ancestry-aware AI
- continuity reputation
- runtime lineage substrate
- weird layer experiments

### Current files
- `WEIRD_LAYER_OUTLINE.md`
- `RUNTIME_DIRECTION.md`
- `MOJO_COMPATIBILITY.md`
- `IDEA_BANK_100.md`

### Success condition
Future ideas are preserved but do not destabilize v0.2.

---

# Vertical Dependency Order

```text
Artifact Core
-> Storage and CAS
-> Proof and Verification
-> Continuity Graph
-> Metrics and Topology
-> Runtime and CLI
-> Prototype Experience
-> Symbolic Compression
-> Governance
-> Future Topology
```

## Build Rule

Do not build higher verticals by weakening lower verticals.

## Compression Rule

When a file touches multiple verticals, its primary vertical must be obvious.

## Prototype Rule

A vertical is not prototype-ready until it has:

- implementation
- test coverage
- docs
- demo relevance
- failure behavior where appropriate

## Current Focus

```text
⚡ π.prototype
● ∫ Runtime and CLI
● ∫ Prototype Experience
◐ ∫ Metrics and Topology
◐ ∫ Documentation Compression
✓ ∫ Artifact Core
✓ ∫ Storage and CAS
✓ ∫ Continuity Graph
✓ ∫ Proof and Verification
```
