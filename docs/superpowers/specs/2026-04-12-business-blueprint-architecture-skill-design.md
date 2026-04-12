# Business Blueprint And Architecture Skill Design Spec

Date: 2026-04-12
Status: Draft for review
Owner: Codex

## Summary

`business-blueprint-skill` is a skill and lightweight generation engine for presales solution work. Its job is not to produce a full proposal document. Its job is to generate editable intermediate diagram artifacts that capture:

- business capability blueprints
- business process and swimlane flows
- application and integration architecture

The source of truth is a canonical JSON IR designed for AI collaboration. A static HTML viewer provides inspection and light editing. Python exporters convert the IR into delivery formats such as SVG, draw.io, and Excalidraw.

This product should be optimized for two kinds of users working on the same material:

- presales and solution managers who need fast visual blueprints for customer conversations
- enterprise or delivery architects who need to refine the same material into application and integration diagrams

## Product Positioning

### One-sentence description

`business-blueprint-skill` turns raw solution inputs into AI-friendly, editable blueprint IR plus lightweight visual working surfaces.

### What it is

- a diagram-oriented intermediate artifact generator
- a shared semantic model for business and architecture views
- a lightweight HTML workbench for inspection and small edits
- a Python-first export pipeline to downstream diagram formats
- a bridge layer for report, slide, Word, and HTML assembly workflows

### What it is not

- not a full proposal writer
- not a full-featured drawing platform
- not a Node-based web app
- not a required server-backed collaboration system
- not a deployment and security architecture tool for the first release

## Product Principles

### 1. IR first

The canonical blueprint JSON is the only source of truth. HTML, SVG, draw.io, and Excalidraw are projections.

### 2. AI-friendly over human-handwritten elegance

The canonical file should optimize for explicit semantics, stable identifiers, incremental edits, and machine validation. Human readability matters, but AI operability matters more.

### 3. Semantics separate from layout

Business meaning, graph structure, and view layout must live in different parts of the model. A layout tweak must not silently mutate solution meaning.

### 4. Python-first, zero-build delivery

The first release must run in sandboxes where Python is available but Node is not. The viewer should be static HTML. Exporters and validators should be Python scripts.

### 5. Intermediate artifacts only

This skill should produce reusable diagram assets, not a complete customer-facing report deck or long-form document. Other skills should consume the IR or exports to assemble final deliverables.

### 6. One semantic model, multiple linked views

Business capability maps, swimlane flows, and application architecture should be different projections over one linked model, not three isolated files.

## Primary Users And Jobs

### Primary users

- presales and solution managers
- enterprise architects
- delivery architects

### Primary jobs-to-be-done

- "Turn ambiguous customer needs into an editable business blueprint quickly."
- "Map business capabilities to actors, flows, and supporting systems without redrawing everything."
- "Hand the same solution model to downstream report, slide, or document generation workflows."

## Scope

### In scope for the first release

- capability blueprint generation
- swimlane and process flow generation
- application and integration architecture generation
- mixed input mode: text plus documents, with weak support for existing diagrams as reference
- a canonical JSON IR
- a static HTML viewer with light editing
- Python exporters for SVG, draw.io, and Excalidraw
- validation for structural integrity and mapping completeness
- common template pack plus industry packs

These three diagram types are the first-release scope because they were explicitly selected during the design discussion as the highest-value presales starting set. Other presales artifacts such as value maps, implementation roadmaps, comparison matrices, and deployment topology remain valid future extensions but are not part of this first contract.

### Explicitly out of scope for the first release

- full proposal writing
- Word or PowerPoint authoring
- complex freeform diagram editing
- deployment topology as a core diagram type
- security domain and network segmentation as a core diagram type
- required always-on server
- multi-user collaboration backend

## Inputs And Outputs

### Inputs

The skill should accept a mixed set of upstream materials:

- raw text requirements
- meeting notes
- RFP or bid material converted to text
- Markdown and similar planning documents
- existing diagrams as weak reference input

`Weak reference input` has a strict meaning in this product. Existing diagrams may be used to suggest candidate entities, labels, and relations, but they must not be treated as canonical truth unless converted back into the blueprint IR. The first release should support:

- structured diagram sources that can be parsed into text or XML hints
- screenshots or pasted images only as visual reference for AI summarization
- human descriptions of existing diagrams as ordinary text input

The first release should not promise lossless round-trip import from arbitrary PPT, Visio, or screenshot-based diagrams.

### Outputs

The default solution package should center on a single canonical file and one viewer:

- `solution.blueprint.json` as the canonical IR
- `solution.viewer.html` as a static viewer and light editor
- `solution.exports/` for derived artifacts such as SVG, draw.io, Excalidraw, PNG
- `solution.patch.jsonl` for edit traceability and merge-safe handoff
- `solution.handoff.json` describing the active revision and viewer handoff context

### Save loop and canonical handoff

The save loop is a core product contract, not an implementation detail.

In the default serverless mode, the viewer cannot silently overwrite files in place. The required workflow is:

1. open `solution.viewer.html` with a specific `solution.blueprint.json`
2. edit the model in the viewer
3. use an explicit save action that exports a new revision package containing the updated `solution.blueprint.json`, `solution.patch.jsonl`, and `solution.handoff.json`
4. treat the exported `solution.blueprint.json` as the only valid source for the next AI pass

The next AI pass must reject stale input when a newer handoff revision exists. The viewer must therefore write revision metadata into the canonical file and the handoff manifest:

- `meta.revisionId`
- `meta.parentRevisionId`
- `meta.lastModifiedAt`
- `meta.lastModifiedBy`

If a future optional Python local bridge supports direct save, it may update the canonical file in place. The handoff contract stays the same: downstream AI always reads the latest canonical JSON, never the HTML and never an old cached revision.

## Canonical IR

### Why JSON instead of SVG

SVG is a rendering format, not a semantic contract. It is poor as the canonical source because it hides meaning inside geometry and styling. The canonical source should remain JSON so that AI can safely add, remove, and remap entities and relations without reparsing a visual artifact.

### Relationship to report IR

This design should borrow the `report-creator` idea that the IR is the human-AI contract and the upstream truth. It should not borrow the report IR block syntax directly. Reports are prose-first. This product is graph-first and view-first. The blueprint IR therefore needs entity and relation modeling instead of Markdown component blocks as the primary structure.

### Top-level structure

The canonical file should use this top-level shape:

```json
{
  "version": "1.0",
  "meta": {},
  "context": {},
  "library": {},
  "relations": [],
  "views": [],
  "editor": {},
  "artifacts": {}
}
```

### Top-level responsibilities

- `meta`: title, industry, language, timestamps, template pack
- `context`: goals, scope, assumptions, constraints, source references
- `library`: canonical entities such as capabilities, actors, stages, systems, data objects, channels, flow steps
- `relations`: typed graph relations between entities
- `views`: visual projections for each diagram
- `editor`: viewer state and collaboration metadata such as theme, zoom preference, panel state, field locks
- `artifacts`: export references and non-canonical cached metadata

### Base entity contract

Every canonical entity should carry a stable identifier and predictable fields:

```json
{
  "id": "sys-crm",
  "kind": "system",
  "name": "CRM",
  "label": "客户关系管理",
  "description": "负责客户档案、商机与跟进管理",
  "aliases": ["Salesforce", "客户系统"],
  "tags": ["sales", "customer"],
  "properties": {},
  "resolution": {
    "status": "canonical",
    "canonicalName": "CRM"
  },
  "sourceRefs": []
}
```

The purpose of the base contract is consistency. AI should know where to update naming, descriptions, custom properties, and references without having to infer structure from each entity type.

### Entity resolution protocol

Stable IDs only work if the system has an explicit merge and disambiguation policy. The first release should use this protocol during ingest and normalize:

1. extract candidate entities with raw names exactly as seen in sources
2. normalize each candidate into a tentative `canonicalName`, `kind`, and alias list
3. compare against existing entities of the same `kind`
4. merge into an existing entity only when the candidate matches on at least one strong signal and no conflict signal blocks the merge
5. create a new entity when evidence indicates a distinct concept
6. mark the entity `resolution.status = "ambiguous"` and trigger clarification when the system cannot safely merge or split

Strong merge signals include:

- exact alias match
- exact external product name match
- same source-system identifier from imported structured input
- same kind plus highly similar normalized name in the same business context

Conflict signals include:

- same normalized name but incompatible kinds
- same vendor term used to describe both a platform and a module
- contradictory source descriptions
- two entities that appear in the same relation slot in one source

The canonical entity should preserve aliases and provenance so a later AI pass can understand why the merge happened.

## Core Semantic Library

### Capability blueprint entities

Capabilities should support hierarchical and stage-based modeling. Minimum fields:

- `id`
- `name`
- `level`
- `parentId`
- `stageId` or `domainId`
- `description`
- `maturity`
- `ownerActorIds`
- `supportingSystemIds`

### Swimlane and process entities

Process views should reuse shared actors and define flow steps as canonical entities. Minimum flow step fields:

- `id`
- `name`
- `actorId`
- `capabilityIds`
- `systemIds`
- `stepType`
- `inputRefs`
- `outputRefs`

Flow relations should be stored in the shared relation graph with explicit types such as:

- `precedes`
- `branches_to`
- `triggers`
- `handoff_to`

### Application and integration entities

Systems should represent channels, business apps, platforms, or external systems. Minimum system fields:

- `id`
- `name`
- `category`
- `domain`
- `description`
- `capabilityIds`

Integrations should be modeled as explicit typed relations or integration entities with at least:

- `id`
- `sourceId`
- `targetId`
- `integrationType`
- `direction`
- `label`
- `payloads`
- `frequency`

### Cross-view linkage rule

Capabilities should act as the main business anchor:

- flow steps may reference one or more capabilities
- systems may reference one or more capabilities
- reports and slide skills may later traverse capability-to-flow-to-system mappings

This linkage is what makes the three diagrams part of one solution model instead of three unrelated drawings.

### Minimum linkage completeness

The first release should turn the linkage principle into executable constraints:

- every non-trivial flow step must reference at least one capability unless explicitly marked `unmappedAllowed`
- every first-party business system in the application architecture must reference at least one capability unless explicitly marked `supportOnly`
- every capability that appears in a flow or architecture view should be present in the capability map view
- if both swimlane and application architecture views exist, at least one capability must bridge the two views

Validation should compute a linkage completeness summary with at least:

- `capability_to_flow_coverage`
- `capability_to_system_coverage`
- `shared_capability_count`
- `unmapped_flow_step_ids`
- `unmapped_system_ids`

The goal is not perfect completeness. The goal is to prevent silent drift into three disconnected diagrams.

## Views

Each visual projection should be defined in `views` and should reference canonical entities instead of copying them. Minimum fields:

- `id`
- `type`
- `title`
- `includedNodeIds`
- `includedRelationIds`
- `layout`
- `annotations`

The first release should define exactly three view types:

- `business-capability-map`
- `swimlane-flow`
- `application-architecture`

### Layout rule

`views[].layout` should contain only layout hints such as grouping, order, coordinates, lane assignment, and visual hierarchy. It must not silently redefine semantic relationships.

## Workflow

The workflow should use five logical phases:

### 1. Ingest

Read raw requirements, meeting notes, and supporting documents. Extract candidate goals, roles, capabilities, flows, systems, and integrations. Preserve source traceability in `context.sourceRefs` and entity-level `sourceRefs`.

### 2. Clarify

Ask a small number of high-value follow-up questions only when critical information is missing. Typical missing areas are:

- primary actors
- core business flow
- existing system boundaries
- target business stages or domains

Clarifications should be written back into the canonical model inputs instead of remaining implicit in chat history.

The first release should define `critical` concretely. Clarification is required when any of these are true:

- no primary actors can be identified
- no business capabilities can be identified
- no main business flow can be assembled
- no existing or target systems can be identified for an architecture view
- entity resolution leaves unresolved ambiguity on a core system or core capability

In headless or batch mode, the system should not invent an interactive sub-protocol. It should stop generation after producing a machine-readable clarification request set in `context.clarifyRequests` and a partial draft state. When answers arrive, they should be written into:

- `context.clarifications`
- `context.assumptions`
- affected canonical entities and relations

### 3. Normalize

Convert mixed raw input into canonical entities and typed relations. Normalize synonyms and map messy source language into stable entity categories.

### 4. Compose

Project the shared semantic graph into the three supported view types. Each view should reference the same underlying entities and relations while storing its own layout hints.

### 5. Render and export

Generate or refresh the static HTML viewer. Export delivery formats from the canonical model through Python scripts.

## HTML Viewer And Light Editor

The HTML viewer should be a workbench, not a full diagram suite.

### Responsibilities

- switch between capability map, swimlane flow, and application architecture
- inspect nodes, relations, source references, and linked objects
- support zoom, pan, filter, and legend toggles
- allow light semantic edits such as labels, descriptions, tags, lane assignment, grouping, and simple add or remove operations
- allow limited layout adjustment that writes back layout hints
- run validation and expose machine-readable validation results
- export current or full-solution artifacts

### Non-responsibilities

- no complex freehand or arbitrary drawing surface
- no DOM-as-source-of-truth behavior
- no long-form document editing
- no dependency on a required server

### Runtime model

The viewer should be a static self-contained HTML asset. The default workflow should not require a running web server. In restricted environments, the user should be able to load JSON into the viewer and export an updated JSON file back out.

An optional Python local bridge may be added later for direct save workflows, but the first release must not depend on it.

The viewer must visibly display the active revision ID and whether there are unsaved edits. It must also make the exported handoff package explicit so users do not mistakenly continue from stale canonical input.

## AI Editing Protocol

The product should explicitly optimize for continued model handoff.

### Stable IDs everywhere

All entities, relations, and views should have stable identifiers. AI should never need to rely on positional descriptions such as "the third box from the left."

### Semantic edits separate from layout edits

- semantic updates modify `library` and `relations`
- layout updates modify `views[].layout`

### Source and assumption tracking

Important facts should carry `sourceRefs`. AI-inferred assumptions should be recorded in `context.assumptions` so downstream workflows can distinguish evidence from synthesis.

### Human edit protection and patch log

The first release must not allow AI regeneration to silently overwrite human edits. The minimum required mechanism is:

- the viewer writes `solution.patch.jsonl` on save
- the canonical JSON tracks field-level human locks or human-edited markers for semantic fields touched in the viewer
- regeneration commands preserve locked or human-edited fields unless the user explicitly requests overwrite

The patch log should use records like:

```json
{"op":"update_node","id":"cap-membership","fields":{"name":"会员增长与运营"}}
{"op":"add_relation","type":"supports","source":"sys-crm","target":"cap-membership"}
{"op":"move_node","viewId":"application-architecture","id":"sys-crm","x":420,"y":180}
```

This is not optional infrastructure. It is part of the collaboration contract between human edits and later AI passes.

## Validation

Validation should be machine-readable and Python-based. It should catch errors that matter for AI collaboration and downstream export.

The first release should validate at least:

- orphan capabilities
- flow steps without actors
- flow steps without upstream or downstream links where links are expected
- key capabilities without supporting systems
- linkage completeness coverage and unmapped flow or system entities
- integrations without valid source or target systems
- view references to missing entities or relations
- unresolved ambiguous entities
- duplicate IDs

Validation output should be structured so that another AI pass can fix problems programmatically.

The validation result should use a stable JSON shape like:

```json
{
  "summary": {
    "errorCount": 0,
    "warningCount": 0,
    "infoCount": 0
  },
  "issues": [
    {
      "severity": "warning",
      "errorCode": "UNMAPPED_SYSTEM",
      "message": "System sys-crm is not linked to any capability.",
      "affectedIds": ["sys-crm"],
      "suggestedFix": "Link the system to one or more capabilities or mark it supportOnly."
    }
  ]
}
```

## Template Packs

The skill should support:

- one common template pack
- industry packs for domains such as retail, manufacturing, government, finance, and education

Industry packs should provide:

- capability scaffolds
- common actor sets
- common system categories
- visual grouping defaults
- terminology alignment

Industry packs should shape the initial model, but must not lock the user into rigid, separate code paths per industry.

The boundary is strict:

- packs may contribute schema-valid seed data, labels, aliases, grouping presets, and view configuration defaults
- packs may not alter the canonical schema
- packs may not introduce renderer-specific code branches that change core editor or exporter behavior by industry
- renderer differences should come from data and configuration, not separate logic trees

## Command Surface

The repository should expose a script-level command surface that mirrors the split between canonical generation and downstream rendering:

- `--plan "need"`: generate only the canonical blueprint JSON
- `--generate <input>`: generate or refresh the canonical JSON plus viewer
- `--edit <blueprint.json>`: generate or refresh the viewer only
- `--export <blueprint.json>`: export SVG, draw.io, Excalidraw, PNG
- `--validate <blueprint.json>`: validate the canonical model
- `--from <file>`: ingest source material from file
- `--industry <pack>`: apply a template pack

This keeps the product aligned with the `report-creator` pattern while respecting the graph-first nature of blueprint artifacts.

### Skill versus script boundary

The flags above are the internal tool surface for Python scripts in the repository. They are not the primary user-facing protocol.

The user-facing interaction is the skill:

- when the user provides raw presales material, the skill chooses `--plan` or `--generate`
- when the user provides an existing blueprint revision, the skill chooses `--edit`, `--validate`, or `--export`
- when another skill needs diagram artifacts, it should consume `solution.blueprint.json` directly or ask this skill to refresh exports

The skill should own the decision logic for which script mode to run. Users may still run the scripts directly, but that is an implementation convenience, not the primary collaboration contract.

## Repository Shape

The repository should contain both the skill and the generation assets:

```text
business-blueprint-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── generate_blueprint.py
│   ├── export_svg.py
│   ├── export_drawio.py
│   ├── export_excalidraw.py
│   └── validate_blueprint.py
├── references/
│   ├── blueprint-schema.md
│   ├── industry-packs.md
│   └── authoring-rules.md
├── assets/
│   └── viewer.html
├── templates/
│   ├── common/
│   ├── retail/
│   ├── manufacturing/
│   └── ...
└── examples/
    └── sample.blueprint.json
```

The first implementation should stay zero-build. If a richer editor exists later, it should remain optional and should not replace the static HTML path as the default runtime.

## Collaboration Boundary With Other Skills

This skill owns diagram-oriented semantic intermediate artifacts.

Downstream skills should consume `solution.blueprint.json` first and exports second:

- report skills assemble reports around blueprint artifacts
- slide skills assemble presentation flows around blueprint artifacts
- document skills place blueprint artifacts into Word or HTML deliverables
- review skills check whether blueprint artifacts are complete and coherent

Derived files such as SVG and draw.io should be treated as delivery artifacts, not as the collaborative source of truth.

## Recommended First Implementation Slice

The safest first slice is:

- define the canonical JSON schema
- generate a retail-flavored example blueprint from text input
- render three basic static views in one HTML workbench
- support export to SVG first
- add draw.io and Excalidraw exporters next
- add machine-readable validation before expanding view complexity

This keeps the first milestone small while preserving the right architectural spine.
