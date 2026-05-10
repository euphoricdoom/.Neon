# .NeoN v0.1 Spec Freeze

This folder contains the frozen v0.1 protocol surface.

The goal is not feature completeness.

The goal is deterministic continuity.

## Frozen Surfaces

- artifact object shape
- canonical hashing rules
- CAS URI format
- proof packet structure
- lineage edge minimums
- WorkLedger command surface

## Rule

Breaking changes to this folder require an explicit version bump.

## v0.1 Loop

```text
create -> derive -> hash -> store -> export -> verify -> inspect
```

If this loop breaks, the protocol is broken.
