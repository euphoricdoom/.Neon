"""Lineage and continuity helpers for .NeoN."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


class LineageGraph:
    """Small in-memory lineage graph.

    Purpose:
    - resolve parents
    - resolve descendants
    - compute lineage depth
    - preserve continuity traversal
    """

    def __init__(self) -> None:
        self.parents: dict[str, list[str]] = {}
        self.children: dict[str, list[str]] = defaultdict(list)

    def add_artifact(self, artifact: dict[str, Any]) -> None:
        artifact_id = artifact["artifact_id"]
        parents = artifact.get("lineage", {}).get("parents", [])

        self.parents[artifact_id] = list(parents)

        for parent in parents:
            self.children[parent].append(artifact_id)

    def walk_parents(self, artifact_id: str) -> list[str]:
        visited: list[str] = []
        stack = list(self.parents.get(artifact_id, []))

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.append(current)
            stack.extend(self.parents.get(current, []))

        return visited

    def walk_descendants(self, artifact_id: str) -> list[str]:
        visited: list[str] = []
        stack = list(self.children.get(artifact_id, []))

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.append(current)
            stack.extend(self.children.get(current, []))

        return visited

    def lineage_depth(self, artifact_id: str) -> int:
        parents = self.parents.get(artifact_id, [])

        if not parents:
            return 0

        return 1 + max(self.lineage_depth(parent) for parent in parents)
