# Vertical 07 — Runtime and CLI

Owns:
- command routing
- local runtime workflow
- human-readable continuity commands
- demo orchestration

Target runtime modules:
- `src/neon/cli.py`
- `src/neon/commands/`

Tests:
- command-level behavior
- invalid command behavior
- demo loop execution

Constraint:
The runtime should become thinner over time as primitives move into dedicated modules.
