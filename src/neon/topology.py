"""Topology helpers for .NeoN continuity graphs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neon.metrics import ContinuityMetrics


def read_neon(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid .neon object: root must be an object: {path}")
    return data


def index_neon_files(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in root.rglob("*.neon"):
        try:
            data = read_neon(path)
        except SystemExit:
            continue
        artifact_id = data.get("artifact_id")
        if isinstance(artifact_id, str):
            index[artifact_id] = path
    return index


def ancestry_chain(start: Path, search_root: Path) -> list[dict[str, Any]]:
    index = index_neon_files(search_root)
    chain: list[dict[str, Any]] = []
    seen: set[str] = set()

    def visit(path: Path) -> None:
        data = read_neon(path)
        artifact_id = data.get("artifact_id")
        if not isinstance(artifact_id, str):
            raise SystemExit(f"Artifact missing artifact_id: {path}")
        if artifact_id in seen:
            return
        seen.add(artifact_id)
        for parent_id in data.get("lineage", {}).get("parents", []):
            parent_path = index.get(parent_id)
            if parent_path is None:
                chain.append({"artifact_id": parent_id, "title": "<missing>", "path": None})
            else:
                visit(parent_path)
        chain.append({"artifact_id": artifact_id, "title": data.get("title", ""), "path": str(path)})

    visit(start)
    return chain


def descendant_chain(start: Path, search_root: Path) -> list[dict[str, Any]]:
    index = index_neon_files(search_root)
    start_data = read_neon(start)
    start_id = start_data.get("artifact_id")
    if not isinstance(start_id, str):
        raise SystemExit(f"Artifact missing artifact_id: {start}")

    by_parent: dict[str, list[Path]] = {}
    for path in index.values():
        data = read_neon(path)
        for parent_id in data.get("lineage", {}).get("parents", []):
            by_parent.setdefault(parent_id, []).append(path)

    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    def visit(parent_id: str) -> None:
        for child_path in by_parent.get(parent_id, []):
            child = read_neon(child_path)
            child_id = child.get("artifact_id")
            if not isinstance(child_id, str) or child_id in seen:
                continue
            seen.add(child_id)
            out.append({"artifact_id": child_id, "title": child.get("title", ""), "path": str(child_path)})
            visit(child_id)

    visit(start_id)
    return out


def artifact_metrics(start: Path, search_root: Path) -> ContinuityMetrics:
    data = read_neon(start)
    artifact_id = data.get("artifact_id")
    if not isinstance(artifact_id, str):
        raise SystemExit(f"Artifact missing artifact_id: {start}")

    parent_count = len(data.get("lineage", {}).get("parents", []))
    ancestors = ancestry_chain(start, search_root)
    descendants = descendant_chain(start, search_root)
    ancestor_count = max(0, len(ancestors) - 1)
    descendant_count = len(descendants)
    lineage_depth = ancestor_count
    child_count = 0

    for item in descendants:
        item_path = item.get("path")
        if not item_path:
            continue
        child_data = read_neon(Path(item_path))
        if artifact_id in child_data.get("lineage", {}).get("parents", []):
            child_count += 1

    return ContinuityMetrics(
        artifact_id=artifact_id,
        parent_count=parent_count,
        child_count=child_count,
        ancestor_count=ancestor_count,
        descendant_count=descendant_count,
        lineage_depth=lineage_depth,
    )


def graph_edges(artifact: dict[str, Any]) -> list[tuple[str, str]]:
    child = artifact["artifact_id"]
    return [(parent, child) for parent in artifact.get("lineage", {}).get("parents", [])]
