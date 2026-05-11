"""Continuity derivative, vector, and ratio metrics for .NeoN.

These metrics are intentionally small and inspectable.
They describe lineage topology without pretending to measure legal value.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContinuityMetrics:
    artifact_id: str
    parent_count: int
    child_count: int
    ancestor_count: int
    descendant_count: int
    lineage_depth: int

    @property
    def derivation_ratio(self) -> float:
        """Descendants per ancestor, with zero-safe denominator."""
        return self.descendant_count / max(1, self.ancestor_count)

    @property
    def influence_ratio(self) -> float:
        """Direct children per direct parent, with zero-safe denominator."""
        return self.child_count / max(1, self.parent_count)

    @property
    def continuity_vector(self) -> tuple[int, int, int]:
        """A compact vector: depth, ancestors, descendants."""
        return (self.lineage_depth, self.ancestor_count, self.descendant_count)

    @property
    def pressure_vector(self) -> tuple[int, int]:
        """A compact vector: incoming lineage pressure, outgoing derivation pressure."""
        return (self.parent_count, self.child_count)


def summarize_metrics(metrics: ContinuityMetrics) -> str:
    return (
        f"{metrics.artifact_id} "
        f"vector={metrics.continuity_vector} "
        f"pressure={metrics.pressure_vector} "
        f"derivation_ratio={metrics.derivation_ratio:.2f} "
        f"influence_ratio={metrics.influence_ratio:.2f}"
    )
