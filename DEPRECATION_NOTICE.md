# Deprecation Notice

The canonical CLI implementation is:

```text
src/neon/cli.py
```

Older prototype CLIs should be considered deprecated.

Reason:

.NeoN requires one canonical reference implementation to preserve protocol continuity and reduce semantic drift.

## Rule

The protocol owns the format.
The canonical CLI owns the reference behavior.

Multiple competing implementations create ambiguity.
