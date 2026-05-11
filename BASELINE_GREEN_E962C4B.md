# .NeoN Green Baseline — e962c4b

This baseline marks the first stable post-extraction checkpoint after the CLI/runtime split.

## Commit

```text
e962c4bec6e2975333aa58ebfd3b5325e3cb9ff9
```

## Branch

```text
green-baseline-e962c4b
```

## Stabilized Surface

```text
✓ thin CLI
✓ extracted command layer
✓ lifecycle substrate
✓ topology substrate
✓ verification substrate
✓ CAS/storage compatibility
✓ release_check.py in CI
✓ parser surface locked
✓ public import surface locked
✓ module export surfaces locked
✓ legacy helper compatibility locked
```

## Rule Going Forward

Every refactor that changes a runtime boundary must add or preserve a regression guard before the next extraction.

## Current Phase

```text
⚡ π.stabilized-prototype
✓ λ.release-check
✓ λ.cli-surface
✓ λ.command-surface
✓ λ.runtime-extraction
● ∫ guarded-refinement
```
