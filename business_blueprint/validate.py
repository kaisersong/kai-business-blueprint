from __future__ import annotations

from collections import Counter
from typing import Any

from .model import ensure_top_level_shape


def _issue(
    severity: str,
    error_code: str,
    message: str,
    affected_ids: list[str],
    suggested_fix: str,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "errorCode": error_code,
        "message": message,
        "affectedIds": affected_ids,
        "suggestedFix": suggested_fix,
    }


def validate_blueprint(payload: dict[str, Any]) -> dict[str, Any]:
    blueprint = ensure_top_level_shape(payload)
    issues: list[dict[str, Any]] = []

    all_ids: list[str] = []
    for collection in blueprint["library"].values():
        if isinstance(collection, list):
            all_ids.extend(
                item["id"]
                for item in collection
                if isinstance(item, dict) and "id" in item
            )

    duplicates = [item_id for item_id, count in Counter(all_ids).items() if count > 1]
    for item_id in duplicates:
        issues.append(
            _issue(
                "error",
                "DUPLICATE_ID",
                f"Duplicate identifier {item_id}.",
                [item_id],
                "Rename one of the duplicate entities.",
            )
        )

    capability_ids = {
        cap["id"] for cap in blueprint["library"]["capabilities"] if "id" in cap
    }
    flow_steps = blueprint["library"]["flowSteps"]
    systems = blueprint["library"]["systems"]

    unmapped_flow_steps = [
        step["id"]
        for step in flow_steps
        if not step.get("unmappedAllowed") and not step.get("capabilityIds")
    ]
    for step_id in unmapped_flow_steps:
        issues.append(
            _issue(
                "warning",
                "UNMAPPED_FLOW_STEP",
                f"Flow step {step_id} is not linked to a capability.",
                [step_id],
                "Add capabilityIds or mark the step unmappedAllowed.",
            )
        )

    unmapped_systems = [
        system["id"]
        for system in systems
        if not system.get("supportOnly")
        and system.get("category") != "external"
        and not system.get("capabilityIds")
    ]
    for system_id in unmapped_systems:
        issues.append(
            _issue(
                "warning",
                "UNMAPPED_SYSTEM",
                f"System {system_id} is not linked to any capability.",
                [system_id],
                "Link the system to one or more capabilities or mark it supportOnly.",
            )
        )

    invalid_cap_refs: list[tuple[str, str]] = []
    for step in flow_steps:
        for capability_id in step.get("capabilityIds", []):
            if capability_id not in capability_ids:
                invalid_cap_refs.append((step["id"], capability_id))
    for owner_id, capability_id in invalid_cap_refs:
        issues.append(
            _issue(
                "error",
                "MISSING_CAPABILITY_REFERENCE",
                f"{owner_id} references missing capability {capability_id}.",
                [owner_id, capability_id],
                "Create the capability or remove the bad reference.",
            )
        )

    summary = {
        "errorCount": sum(1 for issue in issues if issue["severity"] == "error"),
        "warningCount": sum(1 for issue in issues if issue["severity"] == "warning"),
        "infoCount": sum(1 for issue in issues if issue["severity"] == "info"),
        "capability_to_flow_coverage": 0
        if not flow_steps
        else round((len(flow_steps) - len(unmapped_flow_steps)) / len(flow_steps), 2),
        "capability_to_system_coverage": 0
        if not systems
        else round((len(systems) - len(unmapped_systems)) / len(systems), 2),
        "shared_capability_count": len(capability_ids),
    }
    return {"summary": summary, "issues": issues}
