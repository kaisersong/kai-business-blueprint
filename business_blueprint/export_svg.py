from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


def export_svg(blueprint: dict[str, Any], target: Path) -> None:
    labels = [
        node["name"]
        for node in blueprint["library"].get("capabilities", [])
        + blueprint["library"].get("systems", [])
    ]
    rows = "".join(
        f'<text x="24" y="{40 + index * 28}" font-size="14" fill="#18212f">{escape(label)}</text>'
        for index, label in enumerate(labels)
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" '
        f'height="{max(200, 80 + len(labels) * 28)}">{rows}</svg>'
    )
    target.write_text(svg, encoding="utf-8")
