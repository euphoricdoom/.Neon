# PROOF_PACKET_STRUCTURE v0.1

**Status:** Draft v0.1  
**Scope:** portable audit bundles for .NeoN artifacts  
**Depends on:** `RIGHTS_SCHEMA_v0.1`

## Purpose

`PROOF_PACKET_STRUCTURE_v0.1` defines how `.NeoN` artifacts travel as portable, inspectable audit bundles.

A proof packet is designed to make provenance and contribution history:

- hard to dispute
- easy to inspect
- tamper-evident
- evidence-linked
- redaction-aware
- verifier-readable
- exportable across systems

A proof packet is not a legal judgment.

## Core Principle

Undeniable does not mean legally absolute.

It means:

- evidence can be inspected
- hashes can be checked
- timelines can be followed
- redactions are explicit
- claims include confidence levels
- verifier output is reproducible
- provenance relationships remain visible

## Packet Philosophy

A proof packet should feel like:

- a Git commit
- a notarized archive
- a provenance ledger
- a contribution graph
- a portable audit object

combined into one inspectable structure.

## Required Packet Sections

| Section | Purpose |
|---|---|
| Packet Identity | Defines packet ID, version, and export mode |
| Artifact Manifest | Lists included artifacts and references |
| Rights Manifest | Includes RIGHTS_SCHEMA-compatible records |
| Evidence Manifest | Lists evidence references and visibility |
| Hash Manifest | Provides tamper-evident hashes |
| Timeline Manifest | Captures chronological sequence |
| Redaction Manifest | Defines hidden/private/export-safe fields |
| Verifier Output | Machine + human-readable validation results |
| Export Manifest | Defines packet mode and intended audience |
| Non-Claims | Explicitly states protocol limitations |

## Minimal Packet Layout

```text
proof_packet/
├── manifest.json
├── SUMMARY.md
├── rights/
├── evidence/
├── hashes/
├── timeline/
├── verifier/
└── exports/
```

A packet may be archived as:

- `.zip`
- `.neon`
- `.tar`
- structured directory

## Packet Identity

Required fields:

- `packet_id`
- `packet_version`
- `created_at`
- `created_by`
- `export_mode`
- `packet_purpose`

Allowed export modes:

- `public`
- `private`
- `redacted`
- `proof_only`
- `internal`

## Artifact Manifest

The artifact manifest lists included artifacts and references.

Recommended fields:

- `artifact_id`
- `artifact_type`
- `artifact_path`
- `artifact_hash`
- `related_rights_record`
- `visibility`
- `description`

## Rights Manifest

Proof packets should embed or reference `RIGHTS_SCHEMA_v0.1` records.

A packet may contain:

- multiple contributors
- multiple rights records
- derivative relationships
- AI disclosure records
- labor automation records

## Evidence Manifest

Evidence entries should contain:

- `evidence_id`
- `type`
- `ref`
- `visibility`
- `confidence_weight`
- `description`

Allowed evidence types include:

- workbook entries
- GitHub issues/PRs
- commits
- timestamps
- hashes
- screenshots
- exports
- local notes
- proof packets
- URLs

## Hash Manifest

Hashes make the packet tamper-evident.

Recommended fields:

- `target`
- `algorithm`
- `hash`
- `created_at`

Recommended algorithms:

- `sha256`
- `sha512`

Hashing goal:

> Detect modification, not guarantee truth.

## Timeline Manifest

The timeline manifest preserves sequence continuity.

Recommended event fields:

- `timestamp`
- `event_type`
- `description`
- `related_artifact`
- `related_evidence`
- `confidence`

Example event types:

- `created`
- `modified`
- `published`
- `shared`
- `derived`
- `merged`
- `exported`
- `verified`

## Redaction Manifest

Every proof packet must explicitly declare what is hidden or omitted.

Required redaction behavior:

- hidden data must be declared
- omission should be visible
- private references should remain linkable internally
- public exports must not silently imply completeness

Recommended fields:

- `redacted_fields`
- `private_sections`
- `public_sections`
- `export_reason`
- `sensitive_categories`

## Verifier Output

A verifier should be able to inspect a packet and produce:

- schema validation results
- missing evidence warnings
- hash verification status
- redaction warnings
- unsupported reference warnings
- confidence summaries
- export safety warnings

Verifier outputs should include:

- machine-readable JSON
- human-readable summary

## Human Readability Rule

Every proof packet should include:

```text
SUMMARY.md
```

The summary should explain:

- what the packet contains
- what is being claimed
- what evidence exists
- what is uncertain
- what is redacted
- what the packet does NOT claim

A human should understand the packet without reading raw JSON.

## Non-Claims

Proof packets do not:

- guarantee legal ownership
- prove theft automatically
- replace courts/contracts/licenses
- guarantee compensation
- eliminate independent invention
- eliminate ambiguity
- prevent future disputes

## Packet Strength Model

A packet becomes stronger when:

- hashes match
- timelines align
- evidence corroborates claims
- provenance relationships remain coherent
- redactions are explicit
- confidence levels are honest
- verifier output is reproducible

The system gains trust through inspectability.

## Confidence Propagation

Verifier systems must not silently upgrade claim confidence.

Rules:

- `asserted` must remain `asserted` unless additional evidence exists
- `correlated` must not become `verified` automatically
- `speculative` claims must remain visibly speculative
- verifier output should explain why confidence changed

## Suggested Future Extensions

Future versions may add:

- digital signatures
- distributed verification
- organization attestations
- transparency logs
- contributor reputation
- executable policy manifests
- royalty routing
- derivative graph visualization

These are explicitly out of scope for v0.1.

## Minimal Manifest Example

```json
{
  "packet_id": "packet:example:001",
  "packet_version": "0.1",
  "export_mode": "redacted",
  "artifacts": [],
  "rights_records": [],
  "evidence": [],
  "hashes": [],
  "timeline": [],
  "redaction": {
    "redacted_fields": []
  },
  "verifier": {
    "status": "unverified"
  },
  "non_claims": [
    "This packet does not guarantee legal ownership."
  ]
}
```

## Acceptance Rule

A valid proof packet must:

- preserve provenance continuity
- preserve uncertainty honestly
- preserve redaction visibility
- remain inspectable by humans
- remain parseable by tools
- remain exportable across systems
