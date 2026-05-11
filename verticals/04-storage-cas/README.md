# Vertical 04 — Storage and CAS

Owns:
- vault layout
- CAS storage
- ledger storage
- content-addressed fetch/store

Target runtime modules:
- `src/neon/storage.py`
- `src/neon/cas.py`

Tests:
- byte-preserving roundtrip
- CAS URI behavior
- deterministic object paths
