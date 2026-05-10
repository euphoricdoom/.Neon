"""Carl Sowers Symbolic Notation System helpers for .NeoN.

Symbols are operational state compression, not decoration.
"""

from __future__ import annotations

SYMBOLS = {
    "hot_context": "⚡",
    "active": "●",
    "dormant": "○",
    "partial": "◐",
    "solved": "✓",
    "blocked": "✗",
    "type": "◇",
    "build": "∫",
    "merge": "∪",
    "flow": "⇒",
    "cause": "∵",
    "effect": "∴",
    "path": "≡",
    "negation": "∅",
    "always": "∀",
    "workflow": "λ",
    "files": "ƒ",
    "hypothesis": "θ",
    "primary": "α",
    "secondary": "β",
    "project": "π",
    "method": "μ",
    "delta": "δ",
    "sum": "Σ",
    "loop": "∞",
    "variance": "±",
    "meta": "§",
    "critical": "‡",
    "deprecated": "†",
    "reference": "°",
    "section": "¶",
}

VALID_STATUS = {
    SYMBOLS["hot_context"],
    SYMBOLS["active"],
    SYMBOLS["dormant"],
    SYMBOLS["partial"],
    SYMBOLS["solved"],
    SYMBOLS["blocked"],
}


def symbolic_state(status: str, subject: str, operator: str | None = None) -> str:
    """Return a compact symbolic state line.

    Example: symbolic_state("⚡", "v0.2", "π") -> "⚡ π.v0.2"
    """
    if status not in VALID_STATUS:
        raise ValueError(f"invalid symbolic status: {status}")
    if operator:
        return f"{status} {operator}.{subject}"
    return f"{status} {subject}"
