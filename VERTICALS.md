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

## What “Lenticular Plan” Means

Each vertical must be readable through multiple lenses at once:

- **Now:** what exists today
- **Prototype:** what must work for a usable demo
- **v0.2:** what must be stable for the next milestone
- **Later:** what is powerful but should not destabilize the current build
- **Tests:** how the vertical proves itself
- **Risks:** what can corrupt the vertical
- **Next actions:** the smallest useful moves

---

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Artifact validation and canonical serialization exist. |
| Prototype | Users can create readable artifacts through `neon register`, `neon derive`, and `neon demo`. |
| v0.2 | Artifact schema, examples, and validation rules are frozen under `spec/v0.1/`. |
| Later | Artifact subtypes: creator identity, workflow, prompt system, agent, license, release. |
| Tests | Validate required fields, canonical bytes, read/write roundtrip, bad artifact rejection. |
| Risks | Schema drift, hidden fields, over-modeling before the prototype is stable. |
| Next actions | Move remaining artifact logic out of `cli.py`; add subtype examples without changing the core schema. |

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
- `docs/specs/LINEAGE_SEMANTICS.md`
- `examples/chain/`

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | `neon lineage` and `neon descendants` expose ancestry and descendants. |
| Prototype | Demo artifacts can be inspected forward and backward from the CLI. |
| v0.2 | Graph traversal is moved out of `cli.py`; full graph JSON and Mermaid outputs are stable. |
| Later | Branching, merging, divergence, timeline views, pressure maps. |
| Tests | Parent walk, descendant walk, lineage depth, command-level lineage/descendant tests. |
| Risks | Cycles, missing parents, duplicate IDs, graph output that hides uncertainty. |
| Next actions | Add graph tests for missing parent behavior and Mermaid output. |

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Proof packet export and verification exist. Tamper rejection test exists. |
| Prototype | `neon demo` exports and verifies a proof packet automatically. |
| v0.2 | Proof packet shape is frozen with golden fixtures and hash expectations. |
| Later | OpenTimestamps receipts, signed release tags, external attestations. |
| Tests | Export/verify, tamper fail, missing manifest fail, malformed artifact fail. |
| Risks | Claiming legal force too early, overcomplicated identity, unverifiable external anchors. |
| Next actions | Add golden proof packet fixture; add negative test for missing manifest. |

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
- `docs/specs/CAS.md`
- `docs/specs/CANONICAL_HASHING.md`

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | CAS primitives and vault storage exist; store/fetch roundtrip test exists. |
| Prototype | Demo stores the derived artifact into CAS. |
| v0.2 | CAS lookup, fetch, and verification behavior are stable and documented. |
| Later | Import/export vault bundles, remote mirror compatibility, offline portable archives. |
| Tests | CAS URI parse, invalid URI reject, store/fetch byte equality, object path determinism. |
| Risks | Byte drift, path assumptions, mixing content address with mutable identity. |
| Next actions | Make `cli.py` import `storage.py` and `cas.py` directly; remove duplicate functions. |

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
- `docs/archive/DERIVATIVES.md`

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Metrics primitives exist; `neon metrics` exposes topology inspection. |
| Prototype | Demo prints metrics for the derived artifact. |
| v0.2 | Metrics are tested at module and command levels; docs clearly reject popularity/economic scoring. |
| Later | Branch divergence, continuity pressure maps, derivative entropy, compression indexes. |
| Tests | Vector shape, ratio safety, metrics CLI output, zero-parent cases. |
| Risks | Accidental gamification, fake precision, legal/economic overclaiming. |
| Next actions | Add command test for `neon metrics`; add examples for interpreting vectors. |

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Doctrine, helper module, examples, and `neon symbolic-status` exist. |
| Prototype | Symbolic status communicates repo/prototype state quickly. |
| v0.2 | Symbolic usage rules are stable; symbols appear in reports without entering hash-critical structures. |
| Later | Symbolic graph overlays, symbolic continuity reports, agent state packets. |
| Tests | Symbol lookup, symbolic state composition, invalid status rejection. |
| Risks | Becoming cryptic, polluting protocol schema, replacing plain language too early. |
| Next actions | Add symbolic output option for metrics or lineage after plain output is stable. |

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | CLI has the core loop plus demo, lineage, descendants, metrics, and symbolic status. |
| Prototype | `neon demo` creates and verifies a complete inspectable loop. |
| v0.2 | CLI is decomposed into small command modules and uses shared primitives. |
| Later | TUI, local web inspector, plugin boundary, external tool integration. |
| Tests | Demo loop, command-level lineage, descendants, metrics, verify, invalid inputs. |
| Risks | Monolithic `cli.py`, command inconsistency, confusing output. |
| Next actions | Extract `topology.py`, `verification.py`, and command handlers. |

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Demo command and test exist. |
| Prototype | One command shows create, derive, store, export, verify, inspect. |
| v0.2 | README walkthrough and demo output are polished enough for a new user. |
| Later | Visual proof inspector, artifact browser, guided creator onboarding. |
| Tests | `neon demo` creates expected files and supports inspection commands. |
| Risks | Demo feels like toy data, too much CLI noise, unclear value story. |
| Next actions | Add `DEMO.md`; improve demo narrative; include metrics and graph explanation. |

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
- `docs/archive/ROADMAP_V0_2.md`
- `STRUCTURE.md`
- `docs/archive/AUDIT.md`
- `CONTRIBUTING.md`
- `docs/README.md`

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Governance docs exist; audit tracks current truth. |
| Prototype | Governance prevents prototype work from drifting back into theory-only expansion. |
| v0.2 | Audit and roadmap match implementation; stale claims are removed or marked future. |
| Later | Release process, signed tags, issue templates, maintainer roles. |
| Tests | CI passes; docs examples match commands; audit is updated during release. |
| Risks | Too many top-level docs, doctrine repetition, stale claims. |
| Next actions | Compress overlapping docs; update AUDIT after each major sweep. |

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

### Lenticular Plan

| Lens | Plan |
| --- | --- |
| Now | Future concepts are documented but not part of prototype requirements. |
| Prototype | Future topology must not distract from the working continuity loop. |
| v0.2 | Future docs are clearly labeled as future, doctrine, or research. |
| Later | Runtime substrate, browser hooks, ancestry-aware AI, continuity-aware computation. |
| Tests | None required until a future concept becomes implementation. |
| Risks | Scope explosion, confusing prototype with grand architecture, premature browser work. |
| Next actions | Add future labels to speculative docs; keep v0.2 focused. |

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

# Cross-Vertical Review Cadence

Before any release candidate, review each vertical through this checklist:

1. Is the implementation real?
2. Is the behavior tested?
3. Is the documentation honest?
4. Is the vertical still strengthening the core loop?
5. Is anything in the vertical actually future topology pretending to be current behavior?

If any answer fails, the release is not ready.
