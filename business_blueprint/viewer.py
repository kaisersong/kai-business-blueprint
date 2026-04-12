from __future__ import annotations

from pathlib import Path
import json

from .model import load_json, write_json


def write_viewer_package(
    blueprint_path: Path,
    viewer_path: Path,
    handoff_path: Path,
    patch_path: Path,
) -> None:
    blueprint = load_json(blueprint_path)
    asset_path = Path(__file__).parent / "assets" / "viewer.html"
    viewer_template = asset_path.read_text(encoding="utf-8")
    rendered = viewer_template.replace(
        "__BLUEPRINT_JSON__",
        json.dumps(blueprint, ensure_ascii=False),
    )
    viewer_path.write_text(rendered, encoding="utf-8")

    handoff = {
        "revisionId": blueprint["meta"]["revisionId"],
        "blueprintPath": str(blueprint_path),
        "viewerPath": str(viewer_path),
        "patchPath": str(patch_path),
    }
    write_json(handoff_path, handoff)
    if not patch_path.exists():
        patch_path.write_text("", encoding="utf-8")
