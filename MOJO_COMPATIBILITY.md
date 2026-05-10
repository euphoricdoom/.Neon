# .NeoN Mojo Compatibility

.NeoN must remain compatible with Mojo as a future high-performance implementation target.

## Position

Python can be the first reference implementation.

Mojo should be treated as a future performance and systems implementation path.

The `.neon` protocol must not depend on Python-specific behavior.

## Compatibility Rules

1. `.neon` files remain plain UTF-8 JSON in v0.1.
2. Canonical hashing uses sorted JSON keys and SHA-256.
3. SQLite schema stays simple and portable.
4. No Python pickle, marshal, or language-specific serialization.
5. Proof packets remain normal folders with readable files.
6. CLI behavior should map cleanly to Mojo commands later.
7. Heavy compute modules should be isolated for future Mojo ports.

## Mojo-Friendly Surfaces

Good future Mojo targets:

- canonical hashing
- artifact validation
- fingerprinting
- similarity scoring
- graph traversal
- proof packet verification
- local indexing
- batch lineage analysis

Keep in Python for now:

- early CLI orchestration
- docs generation
- quick prototypes
- schema iteration

## Required Boundary

The protocol owns the format.

Implementations can be Python, Mojo, Rust, Go, JavaScript, or anything else.

## Future Layout

Possible future structure:

```text
src/neon/          Python reference implementation
mojo/neon/         Mojo performance implementation
spec/              language-neutral specs
examples/          portable .neon artifacts
```

## North Star

A `.neon` artifact created by Python must be readable and verifiable by Mojo.

A `.neon` artifact created by Mojo must be readable and verifiable by Python.
