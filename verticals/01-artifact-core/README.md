# Vertical 01 — Artifact Core

Owns:
- artifact schema
- artifact serialization
- artifact IDs
- canonical JSON
- lifecycle events

Target runtime modules:
- `src/neon/artifact.py`
- `spec/v0.1/artifact.schema.json`

Tests:
- artifact validation
- canonical hashing
- read/write roundtrip
