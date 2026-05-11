# .NeoN

**Continuity infrastructure for human-origin intelligence.**

.NeoN is a local-first protocol for preserving attribution, lineage, proof, and portability as human-created workflows, automations, prompts, systems, and AI-assisted artifacts transform over time.

> Attribution survives transformation.

## What Works Now

The current reference implementation supports the core continuity loop:

```text
create -> derive -> hash -> store -> export -> verify -> inspect
```

CLI surface:

```bash
neon init
neon register
neon derive
neon validate
neon hash
neon store
neon fetch
neon export
neon verify
neon graph
neon lineage
neon log
neon list
neon status
```

## Quickstart

```bash
pip install -e .

neon init
neon register --title "Invoice Workflow" --creator "Carl Sowers"
neon derive --parent .neon-vault/artifacts/invoice-workflow.neon --title "AI Assisted Workflow" --creator "Carl Sowers"
neon hash .neon-vault/artifacts/ai-assisted-workflow.neon
neon store .neon-vault/artifacts/ai-assisted-workflow.neon
neon export .neon-vault/artifacts/ai-assisted-workflow.neon
neon verify .neon-vault/exports/ai-assisted-workflow-proof
neon graph .neon-vault/artifacts/ai-assisted-workflow.neon
```

Inspect the living example chain:

```bash
neon lineage examples/chain/proof-enhanced-invoice-workflow.neon --root examples/chain
```

## Native Artifact

A `.neon` file is a readable, portable, lineage-bearing intelligence artifact.

Minimum shape:

```json
{
  "neon_version": "0.1.0-alpha",
  "kind": "artifact",
  "artifact_id": ".N/example",
  "title": "Example Artifact",
  "artifact_type": "workflow",
  "creator": { "name": "Creator" },
  "origin": { "created_at": "...", "statement": "..." },
  "lineage": { "parents": [], "events": [] },
  "proof": { "hash_algorithm": "sha256", "anchors": [] }
}
```

## Storage

.NeoN uses local content-addressed storage:

```text
.neon://sha256/<digest>
```

Vault layout:

```text
.neon-vault/
├── artifacts/
├── objects/sha256/
├── exports/
├── indexes/
├── proofs/
├── identity.json
└── ledger.sqlite
```

## Proof Packets

Exports are human-readable proof packets:

```text
proof-packet/
├── artifact.neon
├── manifest.json
├── hashes.txt
├── SUMMARY.md
├── lineage.json
└── verification.json
```

## Repository Map

```text
src/neon/              reference implementation
spec/v0.1/             frozen v0.1 schemas
examples/chain/        living lineage example
examples/golden/       golden reference objects
tests/                 executable invariants
GRAVITY_ANCHOR.md      project center
ROADMAP_V0_2.md        current execution contract
TRUST_PROTOCOL.md      timestamp/signature guidance
CS_SYMBOLIC_NOTATION.md symbolic compression layer
```

## Design Constraints

- local-first
- deterministic
- content-addressed
- implementation-neutral
- human-readable
- proof-oriented
- no cloud dependency
- no blockchain dependency
- no marketplace layer before the primitive is stable

## Status

Early alpha protocol seed.

Not legal advice. Not a completed licensing system. Not a replacement for contracts.

Current focus: make the continuity substrate boringly reliable.
