# .NeoN Vertical Bridges

Verticals prevent chaos.

Bridges create flow.

This document defines how the verticals connect without collapsing into one tangled system.

## Core Bridge Loop

```text
Artifact Core
-> Storage and CAS
-> Proof and Verification
-> Continuity Graph
-> Metrics and Topology
-> Symbolic Compression
-> Runtime and CLI
-> Prototype Experience
-> Governance
-> Future Topology
```

## Bridge Rule

A bridge must be:

- explicit
- testable
- one-directional where possible
- small enough to inspect
- owned by the lower stable vertical unless it is pure presentation

## Bridge 1 — Artifact to Storage

### Flow

```text
.neon artifact -> canonical bytes -> sha256 -> CAS object
```

### Contract

- artifact serialization must be deterministic
- CAS stores bytes, not interpretations
- storage must not mutate artifact meaning

### Current implementation

- `src/neon/artifact.py`
- `src/neon/cas.py`
- `src/neon/storage.py`
- `neon store`

### Required tests

- canonical bytes stable
- CAS URI roundtrip
- fetch preserves bytes

---

## Bridge 2 — Artifact to Proof

### Flow

```text
.neon artifact -> manifest -> proof packet -> verification
```

### Contract

- proof packets reference artifact bytes by hash
- proof packets must fail if artifact bytes change
- proof metadata must not replace artifact content

### Current implementation

- `src/neon/proof.py`
- `neon export`
- `neon verify`

### Required tests

- proof export creates packet
- proof verify passes unchanged packet
- proof verify fails tampered packet

---

## Bridge 3 — Artifact to Continuity Graph

### Flow

```text
artifact.lineage.parents -> ancestry -> descendants -> graph
```

### Contract

- parents are artifact IDs
- missing parents must be visible, not hidden
- graph traversal must not rewrite artifacts

### Current implementation

- `src/neon/lineage.py`
- `neon lineage`
- `neon descendants`
- `neon graph`

### Required tests

- parent traversal
- descendant traversal
- missing parent behavior
- graph output shape

---

## Bridge 4 — Continuity Graph to Metrics

### Flow

```text
parents + ancestors + descendants -> vectors + ratios
```

### Contract

- metrics are topology-only
- metrics are not legal, market, popularity, or reputation scores
- metrics must be inspectable and deterministic

### Current implementation

- `src/neon/metrics.py`
- `neon metrics`

### Required tests

- vector shape
- zero-safe ratios
- metrics command output

---

## Bridge 5 — Metrics to Symbolic Compression

### Flow

```text
topology state -> compact symbolic state
```

### Contract

- symbols clarify state
- symbols do not replace plain output
- symbols do not enter hash-critical canonical bytes unless explicitly versioned later

### Current implementation

- `src/neon/symbols.py`
- `neon symbolic-status`

### Required tests

- symbolic state render
- invalid status rejection

---

## Bridge 6 — Runtime to Prototype Experience

### Flow

```text
commands -> demo loop -> human understanding
```

### Contract

- demo must run without manual source reading
- demo must create, derive, store, export, verify, and inspect
- demo output must teach the loop

### Current implementation

- `neon demo`
- `tests/test_demo_loop.py`

### Required tests

- demo creates artifacts
- demo exports proof
- demo verifies proof
- demo exposes lineage, descendants, metrics, and graph inspection

---

## Bridge 7 — Governance to Every Vertical

### Flow

```text
vertical ownership -> alignment map -> alignment checker -> CI
```

### Contract

- every declared ownership target must exist
- duplicate ownership must be detected
- governance must support implementation, not replace it

### Current implementation

- `VERTICAL_MAP.json`
- `scripts/check_vertical_alignment.py`
- `tests/test_vertical_alignment.py`
- `.github/workflows/ci.yml`

### Required tests

- vertical map validates
- CI runs tests

---

## Bridge 8 — Future Topology to Governance

### Flow

```text
future idea -> future topology doc -> protected backlog -> later implementation
```

### Contract

- future ideas are preserved
- future ideas must not become prototype requirements until promoted
- promotion requires implementation, tests, docs, and demo relevance

### Current implementation

- `WEIRD_LAYER_OUTLINE.md`
- `verticals/10-future-topology/`

### Required tests

None until a future concept becomes runtime behavior.

---

# Bridge Health Checklist

A bridge is healthy when:

1. both verticals are named,
2. the flow is explicit,
3. the contract is testable,
4. failure behavior is known,
5. docs do not overclaim,
6. prototype relevance is clear.

# Current Bridge Focus

```text
⚡ π.prototype-bridges
● ∫ artifact->storage
● ∫ artifact->proof
● ∫ artifact->graph
● ∫ graph->metrics
◐ ∫ metrics->symbolic
✓ ∫ runtime->prototype
✓ ∫ governance->verticals
```

# Next Bridge Work

1. Extract topology helpers out of `cli.py`.
2. Extract verification helpers out of `cli.py`.
3. Add command tests for metrics, descendants, and symbolic status.
4. Add docs for `neon demo` as the first complete prototype bridge.
