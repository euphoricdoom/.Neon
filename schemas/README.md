# JSON Schemas

This folder will hold stable, exported JSON schema definitions for .NeoN.

## Rule

A schema belongs here only when it is:

1. Defined and finalized in the workbook or Drive
2. Versioned (e.g., `rights_schema_v0.1.json`)
3. Ready to be referenced by validators and tests

Do not invent final schemas here. Schemas originate in Drive and are exported here when stable.

## Current State

Existing schemas live in `spec/v0.1/`:

- `spec/v0.1/artifact.schema.json`
- `spec/v0.1/proof-packet.schema.json`

The following schemas are planned but **missing** (v0.1 blockers):

- `rights_schema_v0.1.json`
- `disclosure_bundle_format_v0.1.json`

## Source of Truth

Schema definitions originate in the workbook and Drive. See [ROADMAP_LINKS.md](../ROADMAP_LINKS.md).
