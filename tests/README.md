# Test Suite

This folder contains executable invariants for the .NeoN reference implementation.

## Direction

Tests enforce continuity invariants. They must cover both success and failure behavior.

Planned test areas:

- **Schema validation** — artifacts match declared schemas
- **Proof packets** — export produces a complete and verifiable proof packet
- **Lineage cycles** — cycles in derivation chains are detected and rejected
- **Rights conflicts** — conflicting rights attributions are flagged
- **CAS integrity** — stored objects are retrievable and byte-identical
- **CLI surface** — all commands are present and parse correctly

## Current Tests

The following test files are present:

- `test_artifact_validation.py`
- `test_cas_fetch.py`, `test_cas_surface.py`
- `test_cli_command_surface.py`, `test_cli_compat_exports.py`, `test_cli_parser_smoke.py`
- `test_command_modules_import.py`
- `test_demo_loop.py`
- `test_doctor_command.py`
- `test_golden_phase_a.py`
- `test_hash.py`
- `test_invalid_cas_uri.py`
- `test_lifecycle_surface.py`
- `test_lineage_graph.py`
- `test_metrics.py`, `test_metrics_surface.py`
- `test_modules.py`
- `test_negative_verification.py`
- `test_parser_build_contract.py`
- `test_public_import_surface.py`
- `test_release_check_surface.py`
- `test_storage_surface.py`
- `test_symbolic_status_surface.py`
- `test_topology_surface.py`
- `test_verification_surface.py`
- `test_vertical_alignment.py`
- `test_workledger_flow.py`

## Running Tests

```bash
pip install -e .
pip install pytest
python -m pytest -q
```

## Source of Truth

Test requirements originate in the workbook. See [ROADMAP_LINKS.md](../ROADMAP_LINKS.md).
