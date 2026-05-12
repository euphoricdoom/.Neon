# RIGHTS_SCHEMA v0.1

**Status:** Draft v0.1  
**Scope:** portable contribution intelligence metadata  
**Legal posture:** evidence and declaration layer, not legal advice, not a guarantee of ownership

## Purpose

`RIGHTS_SCHEMA_v0.1` defines a portable metadata record for preserving human contribution, provenance, attribution, labor context, AI assistance, sharing intent, and evidence references as `.NeoN` artifacts move across tools, employers, platforms, and derivative chains.

This schema does **not** decide legal ownership. It records structured claims, confidence levels, evidence references, and declared intent so humans can carry contribution history forward.

> Attribution survives transformation.

## Core Principle

`.NeoN` is not a copyright court. It is a continuity substrate for contribution intelligence.

A rights record answers:

- What contribution is being claimed?
- Who or what contributed?
- What evidence supports the claim?
- What confidence level is attached?
- Was AI involved?
- Was employment or assigned labor involved?
- Is sharing/open source welcome, delayed, conditional, or negotiable?
- What can safely be exported publicly?

## Required Top-Level Fields

| Field | Type | Required | Meaning |
|---|---:|---:|---|
| `schema` | string | yes | Must be `neon.rights` |
| `schema_version` | string | yes | Must be `0.1` |
| `rights_record_id` | string | yes | Stable ID for this rights/contribution record |
| `artifact_ref` | string | yes | Artifact this record describes |
| `claim` | object | yes | Claim type, confidence, summary, and limitations |
| `contributors` | array | yes | Human, AI, organization, or tool contributors |
| `provenance` | object | yes | Origin, platform/context, sources, related artifacts |
| `ai_assistance` | object | yes | Whether AI was used and how |
| `labor_context` | object | yes | Employment/automation/value context |
| `sharing_intent` | object | yes | Attribution, license, openness, negotiation intent |
| `evidence` | array | yes | Links, hashes, timestamps, workbook rows, proof refs |
| `redaction` | object | yes | Public/private/redacted export behavior |
| `notes` | array | no | Freeform explanatory notes |

## Claim Types

Allowed `claim.claim_types` values:

| Claim Type | Meaning |
|---|---|
| `original_creation` | Creator claims original creation of an artifact or component. |
| `conceptual_origin` | Creator claims prior conceptual development or articulation. |
| `derivative_work` | Artifact derives from another artifact, idea, source, or workflow. |
| `ai_assisted_work` | AI materially assisted the work. |
| `labor_automation` | Artifact automates, compresses, or improves labor/workflow. |
| `contribution_record` | Record exists to preserve contribution history. |
| `similarity_assertion` | Creator asserts similarity to later/prior external work. |
| `reference_use` | Artifact references prior art, docs, examples, or public work. |

A record may include multiple claim types.

## Claim Confidence Classes

Confidence must travel with every claim. This prevents uncertain claims from appearing as verified facts.

| Confidence | Meaning |
|---|---|
| `verified` | Strong evidence exists and can be independently checked. |
| `correlated` | Timeline, access path, or feature overlap suggests a relationship, but does not prove it. |
| `asserted` | Creator/user asserts the claim; evidence may be incomplete. |
| `speculative` | Hypothesis or interpretation; must not be presented as fact. |
| `derived` | Relationship is intentionally declared as derivative/reference/remix. |

## Contributors

Contributor records should support humans, AI tools, organizations, employers, and software systems.

Required contributor fields:

- `contributor_id`
- `type`: `human`, `ai_tool`, `organization`, `software`, `unknown`
- `name`
- `roles`
- `contribution_summary`
- `attribution_preference`

Example roles:

- `originator`
- `designer`
- `implementer`
- `reviewer`
- `assistant`
- `employer_context`
- `reference_source`

## Provenance

The provenance object captures origin and lineage context.

Recommended fields:

- `created_at`
- `created_at_precision`: `exact`, `day`, `month`, `year`, `approximate`, `unknown`
- `creation_context`
- `platform_or_tool`
- `source_materials`
- `related_artifacts`
- `derivative_links`
- `prior_art_refs`

## AI Assistance

The schema is honest about AI-assisted work.

Recommended fields:

- `used`: boolean
- `tools`: list of tool/model records
- `role`: `none`, `brainstorming`, `drafting`, `coding`, `review`, `refinement`, `analysis`, `unknown`
- `human_reviewed`: boolean
- `prompt_refs`: list of safe prompt/workflow references
- `disclosure_note`

## Labor / Employment Context

The schema can record labor-origin situations without pretending to settle employment law.

Recommended fields:

- `created_during_employment`: boolean or null
- `employer_or_client`: string or null
- `assigned_task_related`: boolean or null
- `automates_assigned_task`: boolean or null
- `estimated_hours_saved`
- `value_claim_summary`
- `recognition_or_compensation_sought`: boolean
- `negotiation_preference`
- `legal_status_note`

Required posture:

> This is a provenance and negotiation record. It is not an automatic legal judgment.

## Sharing / Licensing Intent

`.NeoN` should support open sharing without erasing leverage.

Recommended fields:

- `attribution_required`: boolean
- `open_source_compatible`: boolean
- `commercial_negotiation_preferred`: boolean
- `collaboration_welcome`: boolean
- `license_mode`: `undecided`, `all_rights_reserved`, `open_source`, `source_available`, `negotiable`, `internal_use`, `custom`
- `future_release_condition`
- `usage_notes`

## Evidence References

Evidence records should be portable pointers, not assumptions.

Allowed evidence types:

- `workbook_evidence_id`
- `github_issue`
- `github_pr`
- `commit`
- `file_hash`
- `timestamp`
- `conversation_export`
- `local_note`
- `proof_packet`
- `external_url`
- `other`

Evidence fields:

- `type`
- `ref`
- `description`
- `visibility`: `public`, `private`, `redacted`, `restricted`
- `confidence_weight`: `low`, `medium`, `high`

## Redaction / Export Safety

Every rights record must declare public/private export behavior.

Recommended fields:

- `public_fields`
- `private_fields`
- `redacted_fields`
- `export_mode`: `public`, `private`, `redacted`, `proof_only`
- `redaction_note`

## Example Claim Postures

### Proper correlated similarity claim

> Creator claims prior conceptual development of a memory-system design before a similar platform feature appeared. Evidence supports timeline and feature overlap. Appropriation is unverified.

Confidence: `correlated` or `asserted`, not `verified`.

### Proper labor automation claim

> Worker created an automation related to assigned work. The record preserves origin, labor savings, and compensation/recognition preference. It does not decide legal ownership.

Confidence may be `verified` for existence/hours evidence and `asserted` for value interpretation.

## Non-Claims

This schema does not claim to:

- override employment contracts
- override copyright law
- prove theft by itself
- guarantee compensation
- guarantee ownership
- replace legal advice
- prevent fair use, reference, or independent invention

## Compatibility With .NeoN Artifacts

A `.neon` artifact may reference a rights record by ID or embed it under a `rights` or `contribution_intelligence` field. The rights record should be exportable inside proof packets and should preserve redaction rules when exported.

## Minimal Valid Record Shape

```json
{
  "schema": "neon.rights",
  "schema_version": "0.1",
  "rights_record_id": "rights:example:001",
  "artifact_ref": ".N/example",
  "claim": {
    "claim_types": ["contribution_record"],
    "confidence": "asserted",
    "summary": "Creator asserts contribution history for this artifact.",
    "limitations": "This record preserves provenance and does not determine legal ownership."
  },
  "contributors": [],
  "provenance": {},
  "ai_assistance": { "used": false },
  "labor_context": {},
  "sharing_intent": {},
  "evidence": [],
  "redaction": { "export_mode": "redacted" }
}
```

## Acceptance Rule

A valid v0.1 record must be honest about confidence, evidence, and limitations. If the record contains uncertain claims, those claims must be marked `asserted`, `correlated`, or `speculative` and must not be framed as verified legal fact.
