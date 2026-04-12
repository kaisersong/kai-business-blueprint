from __future__ import annotations

from typing import Any


def _normalized(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def merge_or_create_system(
    systems: list[dict[str, Any]],
    raw_name: str,
    description: str,
) -> dict[str, Any]:
    normalized_name = _normalized(raw_name)
    for system in systems:
        aliases = system.get("aliases", [])
        names = [system.get("name", ""), *aliases]
        if any(_normalized(candidate) == normalized_name for candidate in names):
            if raw_name not in aliases and raw_name != system.get("name"):
                system.setdefault("aliases", []).append(raw_name)
            if description and not system.get("description"):
                system["description"] = description
            return system

    created = {
        "id": f"sys-{normalized_name or 'unknown'}",
        "kind": "system",
        "name": raw_name,
        "aliases": [],
        "description": description,
        "resolution": {"status": "canonical", "canonicalName": raw_name},
        "capabilityIds": [],
    }
    systems.append(created)
    return created


def mark_ambiguous(entity: dict[str, Any], canonical_name: str) -> dict[str, Any]:
    entity["resolution"] = {
        "status": "ambiguous",
        "canonicalName": canonical_name,
    }
    return entity
