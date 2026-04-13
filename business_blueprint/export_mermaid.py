from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


def export_mermaid(blueprint: dict[str, Any], target: Path) -> None:
    library = blueprint.get("library", {})
    capabilities = library.get("capabilities", [])
    systems = library.get("systems", [])
    actors = library.get("actors", [])
    flow_steps = library.get("flowSteps", [])
    views = blueprint.get("views", [])

    sections: list[str] = []

    # ── Capability Map View ──
    cap_view = next((v for v in views if v.get("type") == "business-capability-map"), None)
    if cap_view or capabilities:
        lines = ["---", "title: 业务能力蓝图", "---", "graph TD"]
        for cap in capabilities:
            label = escape(cap.get("name", cap["id"]))
            lines.append(f'    {cap["id"]}["{label}"]')
        # Sub-system grouping
        sys_ids = {s["id"]: s.get("name", s["id"]) for s in systems}
        for sys in systems:
            lines.append(f'    {sys["id"]}["{escape(sys.get("name", sys["id"]))}"]')
            for cap_id in sys.get("capabilityIds", []):
                lines.append(f'    {sys["id"]} --> {cap_id}')
        sections.append("\n".join(lines))

    # ── Swimlane Flow View ──
    swim_view = next((v for v in views if v.get("type") == "swimlane-flow"), None)
    if swim_view or (actors and flow_steps):
        lines = ["---", "title: 泳道流程图", "---"]
        actor_ids = {a["id"] for a in actors}
        for actor in actors:
            lines.append(f'    subgraph {actor["id"]}["{escape(actor.get("name", actor["id"]))}"]')
            actor_flows = [f for f in flow_steps if f.get("actorId") == actor["id"]]
            for i, flow in enumerate(actor_flows):
                label = escape(flow.get("name", flow["id"]))
                lines.append(f'        {flow["id"]}["{label}"]')
            if not actor_flows:
                lines.append("        empty[无流程]")
            lines.append("    end")
        # Flow ordering
        for i in range(len(flow_steps) - 1):
            lines.append(f'    {flow_steps[i]["id"]} --> {flow_steps[i + 1]["id"]}')
        sections.append("\n".join(lines))

    # ── Application Architecture View ──
    arch_view = next((v for v in views if v.get("type") == "application-architecture"), None)
    if arch_view or systems:
        lines = ["---", "title: 应用架构图", "---", "graph TD"]
        for sys in systems:
            label = escape(sys.get("name", sys["id"]))
            category = sys.get("category", "")
            shape = f'{{"{label}"}}' if category == "database" else f'["{label}"]'
            lines.append(f'    {sys["id"]}{shape}')
        for cap in capabilities:
            lines.append(f'    {cap["id"]}["{escape(cap.get("name", cap["id"]))}"]')
        for sys in systems:
            for cap_id in sys.get("capabilityIds", []):
                lines.append(f'    {sys["id"]} --> {cap_id}')
        # Explicit relations
        for rel in blueprint.get("relations", []):
            src = rel.get("sourceId", rel.get("source", ""))
            tgt = rel.get("targetId", rel.get("target", ""))
            rel_type = rel.get("type", "supports")
            label = escape(rel.get("label", rel_type))
            lines.append(f'    {src} -- "{label}" --> {tgt}')
        sections.append("\n".join(lines))

    content = "\n\n".join(sections) + "\n"
    target.write_text(content, encoding="utf-8")
