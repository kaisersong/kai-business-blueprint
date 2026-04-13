---
name: business-blueprint-skill
description: Use when turning presales requirements, meeting notes, or solution materials into editable business capability blueprints, swimlane flows, and application architecture diagrams. Use when generating blueprint JSON, static HTML viewers, or exporting to SVG, draw.io, Excalidraw, or Mermaid formats.
---

# Business Blueprint Skill

Use the Python scripts in this repository as the execution surface.

## Workflow Decision Tree

```
User provides raw requirements / meeting notes?
  → Does a canonical blueprint JSON already exist?
    → No:  --plan (generate JSON only)
    → Yes: --generate (JSON + viewer refresh)

User has an existing blueprint JSON to modify?
  → --edit (refresh viewer only)

User needs diagram files (SVG, draw.io, etc.)?
  → --validate first, then --export

User unsure about blueprint quality?
  → --validate
```

## Commands

1. Use `--plan` when starting from raw source material and no canonical blueprint exists yet.
2. Use `--generate` after a canonical blueprint exists and the user needs the static viewer package.
3. Use `--edit` to refresh the viewer for an existing blueprint revision.
4. Use `--validate` before claiming a blueprint is complete.
5. Use `--export` when downstream skills need SVG, draw.io, Excalidraw, or Mermaid artifacts.

## Handoff Rules

- Treat `solution.blueprint.json` as the only source of truth.
- Never treat `solution.viewer.html` as the source of truth.
- Preserve `editor.fieldLocks` and human-edited fields during regeneration.
- If `context.clarifyRequests` is non-empty, surface them instead of pretending the blueprint is complete.

## Export Formats

| Format | File | Use Case |
|--------|------|----------|
| SVG | `solution.exports/solution.svg` | Quick preview, embedding |
| draw.io | `solution.exports/solution.drawio` | Editable diagrams |
| Excalidraw | `solution.exports/solution.excalidraw` | Whiteboard-style diagrams |
| Mermaid | `solution.exports/solution.mermaid.md` | GitHub-native rendering |

## Collaboration Boundary

This skill produces **semantic intermediate artifacts**. Downstream skills consume them:

- `report-creator` consumes blueprint → assembles reports
- `slide-creator` consumes blueprint → assembles presentations
- Other skills may consume `relations` → generate PlantUML or other diagram syntax
- Downstream skills should **never directly edit** `solution.blueprint.json`

## Error Handling

- If source text is too ambiguous to extract any entities: run `--plan` with minimal output, then surface `clarifyRequests`.
- If `--validate` returns errors: fix structural issues before proceeding to `--export`.
- If `--validate` returns only warnings: proceed but note the warnings in any handoff.
- If Python version < 3.12: the package will refuse to install. Use `python3 -m business_blueprint.cli` with system Python as fallback.
