# .NeoN Derivatives, Vectors, and Ratios

This document defines continuity-native topology metrics.

These are NOT legal ownership metrics.

They are structural continuity metrics.

## Goal

Measure:

- continuity growth
- derivation pressure
- lineage depth
- influence spread
- branch expansion
- continuity compression

without introducing opaque scoring systems.

## Core Idea

A `.neon` artifact is not isolated.

It exists inside a continuity field.

Each derivation changes the topology of that field.

## Primitive Metrics

### Parent Count

```text
incoming continuity references
```

### Child Count

```text
outgoing derivations
```

### Ancestor Count

```text
total reachable continuity history
```

### Descendant Count

```text
total reachable continuity expansion
```

### Lineage Depth

```text
maximum ancestry distance
```

## Continuity Vector

```text
(depth, ancestors, descendants)
```

Example:

```text
(4, 4, 12)
```

Meaning:

- depth 4
- four upstream continuity artifacts
- twelve downstream derivations

## Pressure Vector

```text
(parents, children)
```

Example:

```text
(1, 9)
```

Meaning:

- one incoming continuity source
- nine outgoing derivations

## Derivation Ratio

```text
descendants / ancestors
```

High values imply strong outward continuity expansion.

## Influence Ratio

```text
children / parents
```

High values imply strong direct derivative generation.

## Important Constraint

These metrics are:

- inspectable
- deterministic
- topology-oriented
- continuity-oriented

They are NOT:

- popularity scores
- social reputation systems
- market valuations
- AI quality metrics

## Compression Principle

Continuity vectors should remain human-readable.

Avoid opaque weighted scoring systems.

Prefer:

```text
small vectors
small ratios
small deterministic primitives
```

over giant hidden ranking algorithms.
