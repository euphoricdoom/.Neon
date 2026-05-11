# .NeoN Core Spec

## Name
.NeoN

## Native file
`.neon`

## Native mark
`.N`

## Sentence
.NeoN preserves the lineage of human-origin intelligence.

## Rule
Attribution survives automation.

## Primitive
A `.neon` file is a portable, readable, lineage-bearing intelligence artifact.

## Flow
```text
human contribution -> .neon artifact -> hash -> ledger event -> proof packet -> optional public anchor
```

## Objects
```text
Artifact  = what was created
Commit    = what changed
Ledger    = what happened
Lineage   = where it came from
Proof     = why it can be trusted
Impact    = what value it created
Identity  = who remains attached
Anchor    = public evidence that a claim existed
```

## First product
WorkLedger: a local-first vault and CLI for creating, validating, linking, hashing, and exporting `.neon` artifacts.

## Local root
```text
.neon-vault/
├── ledger.sqlite
├── artifacts/
├── proofs/
├── exports/
├── indexes/
└── identity.json
```

## Required commands
```bash
neon init
neon register
neon validate
neon derive
neon log
neon export
neon verify
neon sign
neon anchor
neon status
```

## Trust model
Local-first truth.
Portable proof packets.
Optional public anchoring.
Private content stays private by default.

## Proof tiers
```text
0 claim
1 timestamped
2 hashed
3 signed
4 anchored
5 independently attested
```

## Design rules
1. Local first.
2. Agnostic by design.
3. Human-readable before optimized.
4. Proof before economics.
5. Lineage before marketplace.
6. Redaction before exposure.
7. Public anchors store commitments, not secrets.
8. The creator carries the lineage, not the platform.

## Build order
```text
1 file format
2 validator
3 vault
4 ledger
5 proof packet
6 derive/link
7 signatures
8 browser capture
9 fingerprinting
10 impact records
```

## Difference
Most systems track files, money, users, or tasks.

.NeoN tracks the chain from human idea to deployed intelligence system.

## First victory
A creator can generate a `.neon` proof packet that says:

```text
I made this.
Here is when.
Here is the hash.
Here is the lineage.
Here is the proof.
```

## North star
Persistent human-origin intelligence lineage.
