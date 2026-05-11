# .NeoN Canonical Hashing Rules v0.1

Proof systems fail if hashing is inconsistent.

The `.neon` protocol requires deterministic hashing behavior.

## Canonical Rules

1. UTF-8 encoding only.
2. JSON object keys must be sorted.
3. Line endings normalized to LF.
4. No trailing whitespace significance.
5. SHA-256 is the default hashing algorithm.
6. Hashes are computed from canonical serialized bytes.

## Why

Two equivalent `.neon` artifacts must produce the same hash.

## v0.1 Goal

The reference CLI should eventually expose:

```bash
neon hash artifact.neon
```

and produce deterministic output across systems.

## Design Constraint

Canonical hashing rules must remain stable once v1.0 is frozen.
