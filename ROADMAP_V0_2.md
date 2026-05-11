# .NeoN Roadmap to v0.2

This roadmap moves .NeoN from protocol seed to continuity substrate.

## North Star

.NeoN preserves the lineage of human-origin intelligence through transformation.

## Current Phase — Kernel Hardening

The project has passed the post-extraction green baseline.

Baseline:

```text
e962c4bec6e2975333aa58ebfd3b5325e3cb9ff9
```

Branch:

```text
green-baseline-e962c4b
```

Current development rule:

```text
Every refactor that changes a runtime boundary must add or preserve a regression guard before the next extraction.
```

Current emphasis:

- keep `neon.cli` thin but compatible
- keep command handlers extracted
- harden kernel modules with tests
- add diagnostic commands like `neon doctor`
- add golden fixtures before deeper command splits

## v0.2 Target

By v0.2, .NeoN must be:

- deterministic
- local-first
- content-addressed
- lineage-native
- verifiable
- implementation-neutral
- test-backed
- documented
- diagnostically inspectable

## Required Command Surface

```bash
neon init
neon doctor
neon demo
neon register
neon derive
neon validate
neon hash
neon store
neon fetch
neon export
neon verify
neon graph
neon lineage
neon descendants
neon metrics
neon log
neon list
neon status
neon symbolic-status
```

## Phase 1 — Foundation

Goal: establish the irreversible primitive.

Deliverables:
- thin public CLI at `src/neon/cli.py`
- extracted command handlers under `src/neon/commands/`
- canonical `.neon` artifact structure
- deterministic SHA-256 hashing
- CAS address format `.neon://sha256/<digest>`
- basic proof packet structure
- unit and end-to-end tests

Exit criteria:
- create -> derive -> hash -> store -> export -> verify -> inspect works end-to-end

## Phase 2 — Structural Support

Goal: make the protocol durable and installable.

Deliverables:
- working `pyproject.toml`
- installable `neon` command
- frozen `spec/v0.1/` folder
- green baseline branch
- release notes discipline
- `neon doctor` diagnostic command

Exit criteria:
- fresh clone can install, run, diagnose, and verify the continuity loop

## Phase 3 — Structural Continuity

Goal: strengthen continuity guarantees.

Deliverables:
- negative verification tests
- tamper detection tests
- broken lineage tests
- invalid CAS URI tests
- CLI compatibility surface tests
- command surface tests
- OpenTimestamps workflow
- signed release guidance

Exit criteria:
- the system fails safely when continuity breaks

## Phase 4 — Wiring

Goal: connect runtime, storage, lineage, and verification.

Deliverables:
- verify CAS URIs directly
- graph JSON export
- graph Mermaid export
- artifact resolution layer
- CAS resolution layer
- lineage traversal layer
- descendants traversal layer
- topology metrics layer

Exit criteria:
- artifacts can be resolved and inspected across path, title, ID, lineage, descendants, and proof packet where appropriate

## Phase 5 — Testing

Goal: shake the structure.

Deliverables:
- large lineage test
- recursive derivation test
- malformed artifact tests
- deterministic proof packet tests
- golden artifact fixtures
- golden lineage output
- golden metrics output
- mutation tests

Exit criteria:
- tests prove deterministic behavior, failure behavior, and stable public surfaces

## Phase 6 — Bug Testing and Cleanup

Goal: remove entropy.

Deliverables:
- delete duplicate runtime files
- compress overlapping docs
- normalize naming
- remove stale references
- split `commands/core.py` into command lanes only after golden fixtures exist
- full regression run through `scripts/release_check.py`

Exit criteria:
- one runtime, one core spec, one gravity anchor, one command surface, one release gate

## Phase 7 — Documentation

Goal: preserve the knowledge.

Deliverables:
- five-minute quickstart
- CLI usage guide
- `neon doctor` guide
- proof packet guide
- CAS guide
- trust protocol guide
- architecture diagrams
- contributor doctrine

Exit criteria:
- a new contributor can understand, install, diagnose, run, and verify the project in under 10 minutes

## Agent Roles

### Protocol Architect
Owns invariants, specs, and primitive boundaries.

### Runtime Engineer
Owns CLI, vault behavior, CAS, and command ergonomics.

### Verification Engineer
Owns tests, negative tests, golden artifacts, and determinism.

### Trust Engineer
Owns OpenTimestamps, signed release workflow, and proof discipline.

### Repo Custodian
Owns cleanup, naming, structure, and drift prevention.

### Documentation Architect
Owns quickstart, diagrams, and contributor onboarding.

## Non-Goals Before v0.2

Do not add:

- cloud sync
- token systems
- marketplace
- enterprise SaaS
- browser fork work
- AI agent orchestration
- speculative economics

The primitive comes first.

## Success Condition

v0.2 succeeds when this loop is boringly reliable:

```text
create -> derive -> hash -> store -> export -> verify -> inspect
```

And when a user can diagnose the substrate with:

```bash
neon doctor
```

If that loop is clean, .NeoN has a substrate.
