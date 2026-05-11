# .NeoN Trust Protocol

.NeoN needs two trust tracks:

1. Timestamped public existence proofs
2. Signed Git history for human accountability

## Track 1: OpenTimestamps

All important `.NeoN` protocol documents, specs, golden artifacts, and proof packet examples should be timestamped.

Targets:

- docs/specs/CORE_SPEC.md
- GRAVITY_ANCHOR.md
- docs/specs/CAS.md
- SPEC_NEON_FILE_FORMAT.md
- docs/specs/LINEAGE_SEMANTICS.md
- docs/specs/CANONICAL_HASHING.md
- examples/golden/*.neon
- future spec/v0.1/*

## Rule

Timestamp commitments, not private content.

OpenTimestamps should prove that a file hash existed at a time.

It should not reveal private creator artifacts unless the creator chooses to publish them.

## Suggested Workflow

```bash
sha256sum docs/specs/CORE_SPEC.md > timestamps.txt
otstamp docs/specs/CORE_SPEC.md
```

This produces:

```text
docs/specs/CORE_SPEC.md.ots
```

The `.ots` receipt should be committed beside the public file when appropriate.

## Track 2: Signed Git Commits

Maintainers should use signed commits for protocol-changing work.

Recommended:

```bash
git config --global commit.gpgsign true
git config --global user.signingkey <KEY_ID>
```

Then verify with:

```bash
git log --show-signature
```

## Policy

Protocol-changing commits should eventually be signed.

Examples:

- file format changes
- hashing rule changes
- proof packet changes
- lineage semantics changes
- CAS changes
- release tags

## Release Tags

Release tags should be signed:

```bash
git tag -s v0.1-alpha -m "Release .NeoN v0.1-alpha"
git push origin v0.1-alpha
```

## Why This Matters

.NeoN is a provenance protocol.

Its own repo must model provenance discipline.

## Immediate Standard

No private data on public timestamp rails.

Public protocol artifacts may be timestamped.

Maintainer release tags should be signed.
