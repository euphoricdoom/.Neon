# .NeoN Reference Lifecycle v0.1

The reference lifecycle defines the minimum viable behavior for a `.neon` artifact.

## Lifecycle

```text
originated
    ↓
registered
    ↓
validated
    ↓
derived
    ↓
exported
    ↓
verified
    ↓
anchored
```

## originated
A human-origin contribution begins.

## registered
The contribution becomes a `.neon` artifact.

## validated
The artifact passes structural checks.

## derived
A child artifact references ancestry.

## exported
A portable proof packet is created.

## verified
Hashes and structure are confirmed.

## anchored
Optional external proof commitments are attached.

## Rule

Every lifecycle transition must preserve:

- artifact identity
- lineage continuity
- proof integrity
- portability

## Failure Conditions

The lifecycle fails if:

- lineage silently disappears
- hashes drift unexpectedly
- ancestry becomes unverifiable
- proof packets become unreadable

## Design Goal

A `.neon` artifact should survive:

- transport
- mutation
- forks
- organizational change
- platform collapse
- future implementation changes
