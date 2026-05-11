# .NeoN Repository Structure

This document explains what belongs where.

## Core Rule

Every file must strengthen one of these:

- continuity
- lineage
- proof
- deterministic storage
- symbolic compression
- verification
- contributor clarity

If a file does not strengthen one of those, it belongs in an archive or parking lot.

## Source

```text
src/neon/
├── cli.py       # canonical command surface
├── lineage.py   # graph traversal primitives
├── symbols.py   # Carl Sowers symbolic notation helpers
└── __init__.py
```

## Specification

```text
spec/v0.1/
├── README.md
├── artifact.schema.json
└── proof-packet.schema.json
```

Spec files are versioned protocol surfaces.
Breaking changes require a version bump.

## Examples

```text
examples/chain/   # living continuity chain
examples/golden/  # stable reference objects
```

Examples are not decoration.
They are reference behavior.

## Tests

```text
tests/
```

Tests enforce continuity invariants.
They must cover both success and failure behavior.

## Docs

```text
docs/README.md
```

The docs index is the compressed navigation surface.
Top-level docs may exist only when they carry core doctrine, protocol contracts, or execution status.

## Sacred Top-Level Files

```text
README.md
GRAVITY_ANCHOR.md
ROADMAP_V0_2.md
CORE_SPEC.md
TRUST_PROTOCOL.md
CS_SYMBOLIC_NOTATION.md
STRUCTURE.md
```

These define the project spine.

## Drift Rule

Duplicate runtime implementations are forbidden.

The canonical runtime is:

```text
src/neon/cli.py
```

Older prototypes must be removed, archived, or clearly deprecated.

## Compression Rule

When two documents explain the same thing, either:

1. merge them,
2. make one an index to the other,
3. archive the weaker one,
4. or delete the duplicate.

Do not preserve repetition as history.
Use Git history for history.
