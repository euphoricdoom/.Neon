# .NeoN Verification Contract

A protocol repository must prove its own continuity.

This document defines what must be true before a release can be considered stable.

## Core Verification Loop

```text
create
→ derive
→ hash
→ store
→ export
→ verify
→ inspect
```

If this loop fails, the release fails.

## Required Test Categories

### Artifact Integrity

Verify:

- deterministic canonical serialization
- artifact validation
- stable slug generation
- read/write roundtrip correctness

### CAS Integrity

Verify:

- SHA-256 determinism
- CAS URI correctness
- invalid CAS URI rejection
- deterministic CAS path generation

### Proof Integrity

Verify:

- proof packet shape
- proof packet export
- tampered proof packet rejection
- verification failure behavior

### Continuity Integrity

Verify:

- parent traversal
- descendant traversal
- lineage depth
- ancestry preservation

### Symbolic Integrity

Verify:

- symbolic status composition
- invalid symbolic status rejection
- stable symbolic operators

## Negative Verification

The protocol must fail safely.

Required failure tests:

- malformed JSON
- missing lineage
- invalid proof packet
- invalid CAS URI
- tampered export
- invalid symbolic status

## Release Gate

A release candidate must:

1. pass all tests,
2. export a valid proof packet,
3. verify a living lineage chain,
4. preserve deterministic hashes,
5. preserve canonical schemas,
6. maintain continuity traversal.

## Philosophy

Verification is not optional.

Continuity claims without proof are narrative.
