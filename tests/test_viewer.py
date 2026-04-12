import json
from pathlib import Path

from business_blueprint.model import write_json
from business_blueprint.viewer import write_viewer_package


def test_write_viewer_package_creates_viewer_and_handoff(tmp_path: Path) -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "rev-1", "lastModifiedBy": "ai"},
        "context": {},
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {"fieldLocks": {}},
        "artifacts": {},
    }
    blueprint_path = tmp_path / "solution.blueprint.json"
    write_json(blueprint_path, blueprint)

    viewer_path = tmp_path / "solution.viewer.html"
    handoff_path = tmp_path / "solution.handoff.json"
    patch_path = tmp_path / "solution.patch.jsonl"

    write_viewer_package(blueprint_path, viewer_path, handoff_path, patch_path)

    assert viewer_path.exists()
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    assert handoff["revisionId"] == "rev-1"
    assert handoff["blueprintPath"].endswith("solution.blueprint.json")
