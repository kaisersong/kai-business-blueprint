---
name: business-blueprint-skill
description: Generate editable business capability blueprints, swimlane flows, and application architecture artifacts for presales solution work. Use when Codex needs to turn requirements, meeting notes, or solution materials into canonical blueprint JSON, static HTML review surfaces, or draw.io/Excalidraw/SVG outputs.
---

# Business Blueprint Skill

Use the Python scripts in this repository as the execution surface.

## Workflow

1. Use `--plan` when starting from raw source material and no canonical blueprint exists yet.
2. Use `--generate` after a canonical blueprint exists and the user needs the static viewer package.
3. Use `--edit` to refresh the viewer for an existing blueprint revision.
4. Use `--validate` before claiming a blueprint is complete.
5. Use `--export` when downstream skills need SVG, draw.io, or Excalidraw artifacts.

## Handoff Rules

- Treat `solution.blueprint.json` as the only source of truth.
- Never treat `solution.viewer.html` as the source of truth.
- Preserve `editor.fieldLocks` and human-edited fields during regeneration.
- If `context.clarifyRequests` is non-empty, surface them instead of pretending the blueprint is complete.
