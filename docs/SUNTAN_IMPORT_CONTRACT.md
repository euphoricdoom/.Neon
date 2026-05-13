# Sun_Tan Import Contract

## Purpose

Allow `.Neon` to accept verified Sun_Tan origin-claim exports as staged continuity inputs.

This gives the unified product spine a real `.Neon`-side port:

```text
Loop / project-512d
→ Sun_Tan bridge packet
→ Sun_Tan origin claim export
→ .Neon import-suntan
```

## Command

```bash
neon import-suntan <claim.origin.json>
```

Optional staging directory:

```bash
neon import-suntan <claim.origin.json> --out-dir <folder>
```

## Accepted claim shape

Required fields:

- `claim_version`
- `claim_type`
- `source_system`
- `artifact_hash`
- `bridge_payload_hash`
- `bridge_signature`
- `policy`
- `lineage`

Required invariants:

- `claim_type` must be `TRUSTED_ORIGIN`
- `artifact_hash` must start with `sha256:`
- `bridge_payload_hash` must start with `sha256:`
- `bridge_signature` must be present
- `lineage` must be a list

## Behavior

`.Neon` validates and stages the claim into:

```text
<vault>/imports/suntan/
```

It also writes a receipt file containing:

- import type
- import timestamp
- source path
- imported path
- source system
- artifact hash
- bridge payload hash
- policy
- lineage

## Boundary

`.Neon` validates and stages Sun_Tan-origin claims.

Sun_Tan remains responsible for packet creation and packet verification before export.

Loop remains responsible for producing cognition/proof artifacts.
