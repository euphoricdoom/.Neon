# .neon File Format v0.1

A `.neon` file is a readable JSON artifact that carries human-origin intelligence lineage.

Required fields:

- neon_version
- kind
- artifact_id
- title
- artifact_type
- creator
- origin
- lineage
- proof

Rules:

1. kind must be artifact.
2. artifact_id must begin with .N/.
3. lineage must include parents and events.
4. proof must declare sha256 as the default hash algorithm.
5. private content should not be published by default.
6. the file must remain understandable without proprietary software.

Core meaning:

- Artifact is what was created.
- Creator is who remains attached.
- Origin is when and why it began.
- Lineage is where it came from and what changed.
- Proof is why the claim can be checked.
