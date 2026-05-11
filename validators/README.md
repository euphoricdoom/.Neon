# Validators

This folder will hold validator scripts for .NeoN artifacts, schemas, and proof packets.

## Planned Gates

Validators will enforce the following gates when implemented:

1. **Structure** — artifact fields match schema
2. **Hash** — content hash is deterministic and correct
3. **Lineage** — parent references are resolvable
4. **Rights** — rights attribution is present and valid
5. **Proof** — proof packet is complete and verifiable
6. **Privacy** — no disallowed fields present
7. **Marketplace readiness** — artifact meets marketplace entry criteria

## Current State

No validators are implemented yet. Implementation follows schema stabilization.

See `schemas/README.md` for schema status.

## Source of Truth

Validator requirements originate in the workbook. See [ROADMAP_LINKS.md](../ROADMAP_LINKS.md).
