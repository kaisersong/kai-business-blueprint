from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def export_excalidraw(blueprint: dict[str, Any], target: Path) -> None:
    elements = []
    labels = blueprint["library"].get("capabilities", []) + blueprint["library"].get(
        "systems",
        [],
    )
    for index, node in enumerate(labels):
        elements.append(
            {
                "id": node["id"],
                "type": "rectangle",
                "x": 40,
                "y": 40 + index * 80,
                "width": 180,
                "height": 56,
                "strokeColor": "#1c5bd9",
                "backgroundColor": "#d8e8ff",
                "fillStyle": "solid",
                "seed": index + 1,
                "version": 1,
                "versionNonce": index + 10,
                "isDeleted": False,
            }
        )
    payload = {
        "type": "excalidraw",
        "version": 2,
        "source": "business-blueprint-skill",
        "elements": elements,
    }
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
