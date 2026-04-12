from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from .clarify import build_clarify_requests
from .model import load_json, new_revision_meta, write_json
from .normalize import merge_or_create_system


def load_seed(repo_root: Path, industry: str) -> dict[str, Any]:
    seed_path = repo_root / "business_blueprint" / "templates" / industry / "seed.json"
    return load_json(seed_path)


def create_blueprint_from_text(
    source_text: str,
    industry: str,
    repo_root: Path,
) -> dict[str, Any]:
    blueprint = deepcopy(load_seed(repo_root, industry))
    blueprint["meta"] = {
        "title": "Generated Blueprint",
        "industry": industry,
        **new_revision_meta(parent_revision_id=None, modified_by="ai"),
    }
    blueprint["context"]["sourceRefs"] = [{"type": "inline-text", "excerpt": source_text}]

    if "会员" in source_text and not any(
        cap["name"] == "会员运营" for cap in blueprint["library"]["capabilities"]
    ):
        blueprint["library"]["capabilities"].append(
            {
                "id": "cap-membership",
                "name": "会员运营",
                "level": 1,
                "description": "管理会员拉新、促活和留存。",
                "ownerActorIds": ["actor-store-guide"],
                "supportingSystemIds": ["sys-crm"],
            }
        )

    if "导购" in source_text and not blueprint["library"]["actors"]:
        blueprint["library"]["actors"].append(
            {"id": "actor-store-guide", "name": "门店导购"}
        )

    if "CRM" in source_text.upper():
        system = merge_or_create_system(
            blueprint["library"]["systems"],
            raw_name="CRM",
            description="客户关系管理系统",
        )
        if "cap-membership" not in system.setdefault("capabilityIds", []):
            system["capabilityIds"].append("cap-membership")
        system.setdefault("category", "business-app")

    if not blueprint.get("views"):
        blueprint["views"] = [
            {
                "id": "view-capability",
                "type": "business-capability-map",
                "title": "业务能力蓝图",
                "includedNodeIds": [
                    entity["id"]
                    for entity in blueprint["library"]["capabilities"]
                    + blueprint["library"]["systems"]
                ],
                "includedRelationIds": [],
                "layout": {},
                "annotations": [],
            },
            {
                "id": "view-architecture",
                "type": "application-architecture",
                "title": "应用架构图",
                "includedNodeIds": [entity["id"] for entity in blueprint["library"]["systems"]],
                "includedRelationIds": [],
                "layout": {},
                "annotations": [],
            },
        ]

    blueprint["context"]["clarifyRequests"] = build_clarify_requests(blueprint)
    return blueprint


def write_plan_output(
    output_path: Path,
    source_text: str,
    industry: str,
    repo_root: Path,
) -> dict[str, Any]:
    blueprint = create_blueprint_from_text(source_text, industry, repo_root)
    write_json(output_path, blueprint)
    return blueprint
