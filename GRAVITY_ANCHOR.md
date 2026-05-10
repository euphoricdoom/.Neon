# .NeoN Gravity Anchor

This file is the center of the repository.

If the project drifts, return here.

## One Sentence

.NeoN preserves the lineage of human-origin intelligence through transformation.

## Native Primitive

```text
.neon
```

A `.neon` artifact is a readable, portable, lineage-bearing intelligence object.

## Native Mark

```text
.N
```

The `.N` mark identifies traceable lineage objects.

## First Law

Attribution survives transformation.

## Core Loop

```text
create
→ derive
→ hash
→ store
→ export
→ verify
→ inspect
```

If this loop breaks, the protocol is broken.

## Canonical Runtime

```text
src/neon/cli.py
```

There is one reference CLI.

Old prototypes must not compete with the canonical runtime.

## Canonical Storage Root

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

## Canonical Address

```text
.neon://sha256/<digest>
```

Content creates address.
Address preserves continuity.

## Required v0.1 Commands

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
neon log
neon list
neon status
```

## Required Proof Packet

```text
proof-packet/
├── artifact.neon
├── manifest.json
├── hashes.txt
├── SUMMARY.md
├── lineage.json
└── verification.json
```

## Continuity Tests

The project must prove:

1. artifacts validate
2. hashes are deterministic
3. children preserve parents
4. CAS fetch preserves bytes
5. proof packets verify
6. graphs reveal ancestry

## What Belongs

Only work that strengthens:

- origin
- lineage
- proof
- portability
- determinism
- verification
- creator continuity

## What Does Not Belong Yet

Do not add:

- cloud sync
- marketplace
- tokens
- enterprise SaaS
- browser fork work
- AI agent orchestration
- speculative economics

Those may come later.

The primitive comes first.

## Evolution Rule

Compression first.
Fission under pressure.
Compatibility always.

## Implementation Rule

The protocol owns the format.
Implementations are temporary.

## Success Condition

The repo becomes legitimate when this works end-to-end:

```bash
neon init
neon register --title "Invoice Workflow" --creator "Carl Sowers"
neon derive --parent .neon-vault/artifacts/invoice-workflow.neon --title "AI Assisted Workflow" --creator "Carl Sowers"
neon hash .neon-vault/artifacts/ai-assisted-workflow.neon
neon store .neon-vault/artifacts/ai-assisted-workflow.neon
neon export .neon-vault/artifacts/ai-assisted-workflow.neon
neon verify .neon-vault/exports/ai-assisted-workflow-proof
neon graph .neon-vault/artifacts/ai-assisted-workflow.neon
```

If that loop is clean, .NeoN has a spine.
