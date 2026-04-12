from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


def export_drawio(blueprint: dict[str, Any], target: Path) -> None:
    labels = [
        node["name"]
        for node in blueprint["library"].get("capabilities", [])
        + blueprint["library"].get("systems", [])
    ]
    cells = "".join(
        (
            f'<mxCell id="cell-{index}" value="{escape(label)}" vertex="1" parent="1">'
            f'<mxGeometry x="40" y="{40 + index * 70}" width="180" height="48" as="geometry"/>'
            "</mxCell>"
        )
        for index, label in enumerate(labels, start=1)
    )
    xml = (
        '<mxfile host="app.diagrams.net"><diagram name="Blueprint"><mxGraphModel>'
        f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{cells}</root>'
        "</mxGraphModel></diagram></mxfile>"
    )
    target.write_text(xml, encoding="utf-8")
