# .NeoN Testing Philosophy

The first releases of .NeoN should prioritize deterministic behavior over feature count.

## v0.1 Testing Goals

The reference implementation must reliably:

1. initialize a vault
2. create a `.neon` artifact
3. validate artifact structure
4. export a proof packet
5. verify artifact hashes
6. preserve lineage relationships

## Failure Conditions

The system fails if:

- lineage silently disappears
- artifact hashes drift unexpectedly
- proof packets become unverifiable
- private data leaks into public proof structures
- artifacts become unreadable without proprietary tooling

## Design Rule

A smaller trustworthy protocol is more valuable than a larger unstable one.
