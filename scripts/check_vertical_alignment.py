"""Check .NeoN vertical ownership alignment.

This script validates VERTICAL_MAP.json and reports files that are owned by
multiple verticals or referenced in the map but missing from the repository.

It intentionally does not require every repo file to be mapped yet. During the
prototype phase, it enforces correctness of declared ownership first.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "VERTICAL_MAP.json"


def load_map() -> dict:
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))


def main() -> int:
    data = load_map()
    verticals = data.get("verticals", {})
    seen: dict[str, str] = {}
    errors: list[str] = []

    for vertical_id, vertical in verticals.items():
        for owned in vertical.get("owns", []):
            if owned in seen:
                errors.append(f"duplicate ownership: {owned} in {seen[owned]} and {vertical_id}")
            seen[owned] = vertical_id

            path = ROOT / owned
            if owned.endswith("/"):
                if not path.is_dir():
                    errors.append(f"mapped directory missing: {owned}")
            else:
                if not path.exists():
                    errors.append(f"mapped file missing: {owned}")

    if errors:
        print("VERTICAL ALIGNMENT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VERTICAL ALIGNMENT OK")
    print(f"verticals={len(verticals)} owned_entries={len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
