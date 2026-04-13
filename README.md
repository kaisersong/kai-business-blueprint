# business-blueprint-skill

Python-first generation engine and skill for business blueprint and architecture artifacts.

Turns raw presales inputs (requirements, meeting notes, RFPs) into editable business capability blueprints, swimlane flows, and application architecture diagrams — as canonical JSON IR, static HTML viewers, and exports (SVG, draw.io, Excalidraw).

## Dependencies

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | >= 3.12 | Only dependency |
| External packages | None | All Python modules use standard library only |

## Quick Start

```bash
# Install
cd business-blueprint-skill
pip install -e .

# CLI entry point
business-blueprint --help

# Or run directly
python -m business_blueprint.cli --help
```

## Commands

| Flag | Purpose |
|------|---------|
| `--plan "text"` | Generate canonical blueprint JSON from raw text |
| `--generate <output>` | Generate JSON + static HTML viewer package |
| `--edit <blueprint.json>` | Refresh viewer for existing blueprint |
| `--export <blueprint.json>` | Export SVG, draw.io, Excalidraw artifacts |
| `--validate <blueprint.json>` | Validate blueprint, output structured results |
| `--from <file>` | Source material from file path |
| `--industry <pack>` | Apply template pack (default: `common`) |

## Outputs

| File | Role |
|------|------|
| `solution.blueprint.json` | Canonical IR — single source of truth |
| `solution.viewer.html` | Static viewer + light editor |
| `solution.exports/` | SVG, draw.io, Excalidraw exports |
| `solution.patch.jsonl` | Edit traceability log |
| `solution.handoff.json` | Revision manifest for AI handoff |

## Project Structure

```
business-blueprint-skill/
├── SKILL.md                      # Skill definition (routing layer)
├── business_blueprint/           # Python engine (zero external deps)
│   ├── cli.py                    # CLI entry point
│   ├── generate.py               # Blueprint generation from text
│   ├── model.py                  # Data model & top-level shape
│   ├── validate.py               # Machine-readable validation
│   ├── clarify.py                # Clarification request builder
│   ├── normalize.py              # Entity resolution & synonym merging
│   ├── viewer.py                 # HTML viewer package writer
│   ├── export_svg.py             # SVG exporter
│   ├── export_drawio.py          # draw.io exporter
│   ├── export_excalidraw.py      # Excalidraw exporter
│   ├── templates/                # Industry packs (common, retail)
│   └── assets/                   # viewer.html template
├── references/                   # Schema, authoring rules, industry packs
├── tests/                        # Test suite
└── examples/                     # Sample blueprint JSON
```
