# .NeoN Lineage Semantics v0.1

Lineage is the physics engine of .NeoN.

A `.neon` artifact is not just a record. It is a position in an intelligence lineage graph.

## Core Lineage Edge Types

### originated
The first recorded appearance of an artifact.

### derived_from
A new artifact was created from a prior artifact.

### influenced_by
A new artifact was shaped by another artifact, but does not directly descend from it.

### forked_from
A new branch of an artifact was intentionally created.

### merged_from
Multiple artifacts were combined into a new artifact.

### transformed_from
An artifact was substantially changed while retaining ancestry.

### attested_by
A person or system made a claim about an artifact or lineage edge.

### anchored_by
A hash, timestamp, or external proof was attached to an artifact or claim.

## Lineage Edge Shape

Every edge should eventually contain:

- edge_id
- edge_type
- source_artifact_id
- target_artifact_id
- created_at
- actor
- summary
- confidence_tier
- evidence

## Confidence Tiers

0. claim only
1. timestamped
2. hashed
3. signed
4. publicly anchored
5. independently attested

## Core Rule

Lineage can be incomplete, but it must not pretend to be stronger than its proof.

## Design Constraint

A lineage edge is a claim with evidence, not magic truth.

## v0.1 Requirement

The first implementation must support:

- originated
- derived_from
- exported_as_proof
- verified_hash

Everything else can be modeled later.
