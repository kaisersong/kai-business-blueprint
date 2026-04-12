# Business Blueprint Skill V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working `business-blueprint-skill` repository that generates AI-friendly blueprint IR, renders a static HTML viewer, tracks revision-safe edits, validates linkage completeness, and exports SVG, draw.io, and Excalidraw artifacts.

**Architecture:** Start with a greenfield Python-first repository at `D:\projects\business-blueprint-skill`. Keep the code split into five focused layers: canonical model and validation, ingest and normalize, generation and handoff packaging, static viewer emission, and export adapters. Use the canonical `solution.blueprint.json` as the only source of truth; every other file is derived or collaboration metadata.

**Tech Stack:** Python 3.12+, standard library, pytest, static HTML/CSS/JavaScript, no Node, no required server

---

## Scope Check

The design spec is broad enough to tempt scope drift. This plan intentionally covers only the first release described in the spec:

1. canonical JSON IR
2. entity resolution and clarify requests
3. linkage-aware validation
4. static HTML viewer with explicit save loop
5. SVG, draw.io, and Excalidraw export
6. skill packaging and end-to-end tests

This plan does not include:

- a local Python save bridge
- deployment topology or security-domain diagrams
- multi-user collaboration
- OCR or full-fidelity diagram import

## File Structure

| File | Operation | Responsibility |
|------|-----------|----------------|
| `D:\projects\business-blueprint-skill\pyproject.toml` | Create | Python package metadata, scripts, test dependencies |
| `D:\projects\business-blueprint-skill\README.md` | Create | repo quick start and command examples |
| `D:\projects\business-blueprint-skill\business_blueprint\__init__.py` | Create | package version export |
| `D:\projects\business-blueprint-skill\business_blueprint\cli.py` | Create | top-level CLI entrypoint and command dispatch |
| `D:\projects\business-blueprint-skill\business_blueprint\model.py` | Create | canonical blueprint helpers, IDs, revision metadata |
| `D:\projects\business-blueprint-skill\business_blueprint\validate.py` | Create | structural validation and linkage completeness |
| `D:\projects\business-blueprint-skill\business_blueprint\normalize.py` | Create | entity resolution, alias merge, ambiguity detection |
| `D:\projects\business-blueprint-skill\business_blueprint\clarify.py` | Create | clarify request generation and answer application |
| `D:\projects\business-blueprint-skill\business_blueprint\generate.py` | Create | source-text ingest, template application, blueprint assembly |
| `D:\projects\business-blueprint-skill\business_blueprint\viewer.py` | Create | emit static viewer HTML and handoff package files |
| `D:\projects\business-blueprint-skill\business_blueprint\export_svg.py` | Create | SVG export from canonical views |
| `D:\projects\business-blueprint-skill\business_blueprint\export_drawio.py` | Create | draw.io XML export |
| `D:\projects\business-blueprint-skill\business_blueprint\export_excalidraw.py` | Create | Excalidraw JSON export |
| `D:\projects\business-blueprint-skill\business_blueprint\templates\common\base_blueprint.json` | Create | shared seed structure for generated blueprints |
| `D:\projects\business-blueprint-skill\business_blueprint\templates\retail\seed.json` | Create | retail starter entities and view defaults |
| `D:\projects\business-blueprint-skill\business_blueprint\assets\viewer.html` | Create | static workbench UI shell |
| `D:\projects\business-blueprint-skill\SKILL.md` | Create | user-facing skill instructions and decision logic |
| `D:\projects\business-blueprint-skill\agents\openai.yaml` | Create | skill UI metadata |
| `D:\projects\business-blueprint-skill\references\blueprint-schema.md` | Create | canonical schema reference |
| `D:\projects\business-blueprint-skill\references\industry-packs.md` | Create | template pack rules |
| `D:\projects\business-blueprint-skill\references\authoring-rules.md` | Create | viewer edit and handoff rules |
| `D:\projects\business-blueprint-skill\examples\sample.blueprint.json` | Create | golden example for docs and tests |
| `D:\projects\business-blueprint-skill\tests\test_cli_smoke.py` | Create | help and command dispatch smoke tests |
| `D:\projects\business-blueprint-skill\tests\test_validate.py` | Create | structural and linkage validation tests |
| `D:\projects\business-blueprint-skill\tests\test_normalize.py` | Create | entity resolution and ambiguity tests |
| `D:\projects\business-blueprint-skill\tests\test_generate.py` | Create | plan and generate pipeline tests |
| `D:\projects\business-blueprint-skill\tests\test_viewer.py` | Create | viewer save loop and handoff tests |
| `D:\projects\business-blueprint-skill\tests\test_exporters.py` | Create | export adapter tests |
| `D:\projects\business-blueprint-skill\tests\test_e2e.py` | Create | end-to-end generation and validate flow |

---

### Task 1: Initialize the Python repository and smoke-testable CLI

**Files:**
- Create: `D:\projects\business-blueprint-skill\pyproject.toml`
- Create: `D:\projects\business-blueprint-skill\README.md`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\__init__.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\cli.py`
- Create: `D:\projects\business-blueprint-skill\tests\test_cli_smoke.py`

- [ ] **Step 1: Write the failing CLI smoke test**

Write `D:\projects\business-blueprint-skill\tests\test_cli_smoke.py`:

```python
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_help_lists_supported_commands() -> None:
    result = run_cli("--help")
    assert result.returncode == 0
    assert "--plan" in result.stdout
    assert "--generate" in result.stdout
    assert "--validate" in result.stdout
```

- [ ] **Step 2: Run the smoke test to verify it fails**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_cli_smoke.py -q
```

Expected: FAIL with `ModuleNotFoundError` or `No module named business_blueprint`.

- [ ] **Step 3: Create the minimal package and CLI implementation**

Write `D:\projects\business-blueprint-skill\pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "business-blueprint-skill"
version = "0.1.0"
description = "Python-first blueprint IR generator and exporter"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
test = ["pytest>=8.0.0"]

[project.scripts]
business-blueprint = "business_blueprint.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Write `D:\projects\business-blueprint-skill\README.md`:

```markdown
# business-blueprint-skill

Python-first generation engine and skill for business blueprint and architecture IR.

## Quick Start

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pip install -e .[test]
python -m business_blueprint.cli --help
```
```

Write `D:\projects\business-blueprint-skill\business_blueprint\__init__.py`:

```python
__all__ = ["__version__"]

__version__ = "0.1.0"
```

Write `D:\projects\business-blueprint-skill\business_blueprint\cli.py`:

```python
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Generate only the canonical blueprint JSON.")
    parser.add_argument("--generate", help="Generate the canonical blueprint JSON and viewer.")
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Export SVG, draw.io, and Excalidraw artifacts.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--industry", default="common", help="Template pack name.")
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Install the repo in editable mode and rerun the smoke test**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pip install -e .[test]
python -m pytest tests/test_cli_smoke.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit the bootstrap**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add pyproject.toml README.md business_blueprint\__init__.py business_blueprint\cli.py tests\test_cli_smoke.py
git commit -m "feat: bootstrap blueprint skill python cli"
```

---

### Task 2: Define the canonical model, revision metadata, and structural validation

**Files:**
- Create: `D:\projects\business-blueprint-skill\business_blueprint\model.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\validate.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\templates\common\base_blueprint.json`
- Create: `D:\projects\business-blueprint-skill\tests\test_validate.py`
- Modify: `D:\projects\business-blueprint-skill\business_blueprint\cli.py`

- [ ] **Step 1: Write failing validation tests for duplicate IDs and linkage completeness**

Write `D:\projects\business-blueprint-skill\tests\test_validate.py`:

```python
from business_blueprint.validate import validate_blueprint


def test_validate_reports_duplicate_ids() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [
                {"id": "cap-order", "name": "Order"},
                {"id": "cap-order", "name": "Order Duplicate"},
            ],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "DUPLICATE_ID" for issue in result["issues"])


def test_validate_reports_unmapped_first_party_system() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [{"id": "cap-order", "name": "Order"}],
            "flowSteps": [],
            "systems": [
                {"id": "sys-crm", "name": "CRM", "category": "business-app", "supportOnly": False}
            ],
        },
        "relations": [],
        "views": [
            {"id": "view-arch", "type": "application-architecture", "includedNodeIds": ["sys-crm"], "includedRelationIds": [], "layout": {}, "annotations": []}
        ],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "UNMAPPED_SYSTEM" for issue in result["issues"])
```

- [ ] **Step 2: Run the validation tests to verify they fail**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_validate.py -q
```

Expected: FAIL with `ImportError` for `business_blueprint.validate`.

- [ ] **Step 3: Implement the canonical model helpers and validator**

Write `D:\projects\business-blueprint-skill\business_blueprint\model.py`:

```python
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any


TOP_LEVEL_KEYS = ["version", "meta", "context", "library", "relations", "views", "editor", "artifacts"]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def new_revision_meta(parent_revision_id: str | None = None, modified_by: str = "ai") -> dict[str, str | None]:
    revision_id = f"rev-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    return {
        "revisionId": revision_id,
        "parentRevisionId": parent_revision_id,
        "lastModifiedAt": utc_now(),
        "lastModifiedBy": modified_by,
    }


def ensure_top_level_shape(payload: dict[str, Any]) -> dict[str, Any]:
    result = {key: deepcopy(payload.get(key, {} if key not in {"relations", "views"} else [])) for key in TOP_LEVEL_KEYS}
    result["library"].setdefault("capabilities", [])
    result["library"].setdefault("actors", [])
    result["library"].setdefault("flowSteps", [])
    result["library"].setdefault("systems", [])
    return result
```

Write `D:\projects\business-blueprint-skill\business_blueprint\validate.py`:

```python
from __future__ import annotations

from collections import Counter
from typing import Any

from .model import ensure_top_level_shape


def _issue(severity: str, error_code: str, message: str, affected_ids: list[str], suggested_fix: str) -> dict[str, Any]:
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
            all_ids.extend(item["id"] for item in collection if isinstance(item, dict) and "id" in item)

    duplicates = [item_id for item_id, count in Counter(all_ids).items() if count > 1]
    for item_id in duplicates:
        issues.append(_issue("error", "DUPLICATE_ID", f"Duplicate identifier {item_id}.", [item_id], "Rename one of the duplicate entities."))

    capability_ids = {cap["id"] for cap in blueprint["library"]["capabilities"]}
    flow_steps = blueprint["library"]["flowSteps"]
    systems = blueprint["library"]["systems"]

    unmapped_flow_steps = [
        step["id"]
        for step in flow_steps
        if not step.get("unmappedAllowed") and not step.get("capabilityIds")
    ]
    for step_id in unmapped_flow_steps:
        issues.append(_issue("warning", "UNMAPPED_FLOW_STEP", f"Flow step {step_id} is not linked to a capability.", [step_id], "Add capabilityIds or mark the step unmappedAllowed."))

    unmapped_systems = [
        system["id"]
        for system in systems
        if not system.get("supportOnly") and system.get("category") != "external" and not system.get("capabilityIds")
    ]
    for system_id in unmapped_systems:
        issues.append(_issue("warning", "UNMAPPED_SYSTEM", f"System {system_id} is not linked to any capability.", [system_id], "Link the system to one or more capabilities or mark it supportOnly."))

    invalid_cap_refs = []
    for step in flow_steps:
        for capability_id in step.get("capabilityIds", []):
            if capability_id not in capability_ids:
                invalid_cap_refs.append((step["id"], capability_id))
    for owner_id, capability_id in invalid_cap_refs:
        issues.append(_issue("error", "MISSING_CAPABILITY_REFERENCE", f"{owner_id} references missing capability {capability_id}.", [owner_id, capability_id], "Create the capability or remove the bad reference."))

    summary = {
        "errorCount": sum(1 for issue in issues if issue["severity"] == "error"),
        "warningCount": sum(1 for issue in issues if issue["severity"] == "warning"),
        "infoCount": sum(1 for issue in issues if issue["severity"] == "info"),
        "capability_to_flow_coverage": 0 if not flow_steps else round((len(flow_steps) - len(unmapped_flow_steps)) / len(flow_steps), 2),
        "capability_to_system_coverage": 0 if not systems else round((len(systems) - len(unmapped_systems)) / len(systems), 2),
        "shared_capability_count": len(capability_ids),
    }
    return {"summary": summary, "issues": issues}
```

Write `D:\projects\business-blueprint-skill\business_blueprint\templates\common\base_blueprint.json`:

```json
{
  "version": "1.0",
  "meta": {},
  "context": {
    "goals": [],
    "scope": [],
    "assumptions": [],
    "constraints": [],
    "sourceRefs": [],
    "clarifyRequests": [],
    "clarifications": []
  },
  "library": {
    "capabilities": [],
    "actors": [],
    "flowSteps": [],
    "systems": []
  },
  "relations": [],
  "views": [],
  "editor": {
    "fieldLocks": {},
    "theme": "enterprise-default"
  },
  "artifacts": {}
}
```

Modify `D:\projects\business-blueprint-skill\business_blueprint\cli.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .model import load_json
from .validate import validate_blueprint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Generate only the canonical blueprint JSON.")
    parser.add_argument("--generate", help="Generate the canonical blueprint JSON and viewer.")
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Export SVG, draw.io, and Excalidraw artifacts.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--industry", default="common", help="Template pack name.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.validate:
        payload = load_json(Path(args.validate))
        print(json.dumps(validate_blueprint(payload), ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the validation tests to verify they pass**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_validate.py -q
```

Expected: PASS with `2 passed`.

- [ ] **Step 5: Commit the canonical model layer**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add business_blueprint\model.py business_blueprint\validate.py business_blueprint\cli.py business_blueprint\templates\common\base_blueprint.json tests\test_validate.py
git commit -m "feat: add canonical blueprint model and validator"
```

---

### Task 3: Implement entity resolution and clarify request generation

**Files:**
- Create: `D:\projects\business-blueprint-skill\business_blueprint\normalize.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\clarify.py`
- Create: `D:\projects\business-blueprint-skill\tests\test_normalize.py`

- [ ] **Step 1: Write failing tests for alias merge and ambiguity detection**

Write `D:\projects\business-blueprint-skill\tests\test_normalize.py`:

```python
from business_blueprint.clarify import build_clarify_requests
from business_blueprint.normalize import merge_or_create_system


def test_merge_or_create_system_uses_alias_match() -> None:
    systems = [
        {
            "id": "sys-crm",
            "kind": "system",
            "name": "CRM",
            "aliases": ["Salesforce"],
            "resolution": {"status": "canonical", "canonicalName": "CRM"},
        }
    ]

    merged = merge_or_create_system(systems, raw_name="Salesforce", description="customer platform")

    assert merged["id"] == "sys-crm"
    assert len(systems) == 1


def test_build_clarify_requests_flags_ambiguous_systems() -> None:
    blueprint = {
        "context": {},
        "library": {
            "systems": [
                {
                    "id": "sys-1",
                    "name": "ERP",
                    "resolution": {"status": "ambiguous", "canonicalName": "ERP"},
                }
            ]
        },
    }

    requests = build_clarify_requests(blueprint)

    assert requests[0]["code"] == "AMBIGUOUS_SYSTEM"
    assert requests[0]["affectedIds"] == ["sys-1"]
```

- [ ] **Step 2: Run the normalize tests to verify they fail**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_normalize.py -q
```

Expected: FAIL with `ImportError` for `business_blueprint.normalize`.

- [ ] **Step 3: Implement entity resolution and clarify helpers**

Write `D:\projects\business-blueprint-skill\business_blueprint\normalize.py`:

```python
from __future__ import annotations

from typing import Any


def _normalized(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def merge_or_create_system(systems: list[dict[str, Any]], raw_name: str, description: str) -> dict[str, Any]:
    normalized_name = _normalized(raw_name)
    for system in systems:
        aliases = system.get("aliases", [])
        names = [system.get("name", ""), *aliases]
        if any(_normalized(candidate) == normalized_name for candidate in names):
            if raw_name not in aliases and raw_name != system.get("name"):
                system.setdefault("aliases", []).append(raw_name)
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
    entity["resolution"] = {"status": "ambiguous", "canonicalName": canonical_name}
    return entity
```

Write `D:\projects\business-blueprint-skill\business_blueprint\clarify.py`:

```python
from __future__ import annotations

from typing import Any


def build_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    library = blueprint.get("library", {})

    if not library.get("actors"):
        requests.append(
            {
                "code": "MISSING_PRIMARY_ACTOR",
                "question": "Which primary business actors should appear in the solution?",
                "affectedIds": [],
            }
        )

    if not library.get("capabilities"):
        requests.append(
            {
                "code": "MISSING_CAPABILITY",
                "question": "Which business capabilities must be represented in the blueprint?",
                "affectedIds": [],
            }
        )

    for system in library.get("systems", []):
        if system.get("resolution", {}).get("status") == "ambiguous":
            requests.append(
                {
                    "code": "AMBIGUOUS_SYSTEM",
                    "question": f"Clarify whether {system['name']} is a distinct system or an alias of another system.",
                    "affectedIds": [system["id"]],
                }
            )

    return requests
```

- [ ] **Step 4: Run the normalize tests to verify they pass**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_normalize.py -q
```

Expected: PASS with `2 passed`.

- [ ] **Step 5: Commit the resolution and clarify layer**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add business_blueprint\normalize.py business_blueprint\clarify.py tests\test_normalize.py
git commit -m "feat: add entity resolution and clarify rules"
```

---

### Task 4: Implement blueprint generation from text input and retail seed templates

**Files:**
- Create: `D:\projects\business-blueprint-skill\business_blueprint\generate.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\templates\retail\seed.json`
- Create: `D:\projects\business-blueprint-skill\tests\test_generate.py`
- Modify: `D:\projects\business-blueprint-skill\business_blueprint\cli.py`

- [ ] **Step 1: Write failing generation tests for `--plan` and retail seed output**

Write `D:\projects\business-blueprint-skill\tests\test_generate.py`:

```python
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_plan_writes_blueprint_json(tmp_path: Path) -> None:
    source = tmp_path / "brief.txt"
    source.write_text("零售客户需要会员运营、门店导购和CRM集成。", encoding="utf-8")
    output = tmp_path / "solution.blueprint.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "business_blueprint.cli",
            "--plan",
            str(output),
            "--from",
            str(source),
            "--industry",
            "retail",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["meta"]["industry"] == "retail"
    assert any(cap["name"] == "会员运营" for cap in payload["library"]["capabilities"])
```

- [ ] **Step 2: Run the generation test to verify it fails**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_generate.py -q
```

Expected: FAIL because `--plan` does not write the output file.

- [ ] **Step 3: Implement the generator and retail seed**

Write `D:\projects\business-blueprint-skill\business_blueprint\generate.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

from .clarify import build_clarify_requests
from .model import load_json, new_revision_meta, write_json
from .normalize import merge_or_create_system


def load_seed(repo_root: Path, industry: str) -> dict[str, Any]:
    seed_path = repo_root / "business_blueprint" / "templates" / industry / "seed.json"
    return load_json(seed_path)


def create_blueprint_from_text(source_text: str, industry: str, repo_root: Path) -> dict[str, Any]:
    blueprint = load_seed(repo_root, industry)
    blueprint["meta"] = {
        "title": "Generated Blueprint",
        "industry": industry,
        **new_revision_meta(parent_revision_id=None, modified_by="ai"),
    }
    blueprint["context"]["sourceRefs"] = [{"type": "inline-text", "excerpt": source_text}]

    if "会员" in source_text and not any(cap["name"] == "会员运营" for cap in blueprint["library"]["capabilities"]):
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
        blueprint["library"]["actors"].append({"id": "actor-store-guide", "name": "门店导购"})

    if "CRM" in source_text:
        merge_or_create_system(blueprint["library"]["systems"], raw_name="CRM", description="客户关系管理系统")

    blueprint["context"]["clarifyRequests"] = build_clarify_requests(blueprint)
    return blueprint


def write_plan_output(output_path: Path, source_text: str, industry: str, repo_root: Path) -> dict[str, Any]:
    blueprint = create_blueprint_from_text(source_text, industry, repo_root)
    write_json(output_path, blueprint)
    return blueprint
```

Write `D:\projects\business-blueprint-skill\business_blueprint\templates\retail\seed.json`:

```json
{
  "version": "1.0",
  "meta": {},
  "context": {
    "goals": [],
    "scope": [],
    "assumptions": [],
    "constraints": [],
    "sourceRefs": [],
    "clarifyRequests": [],
    "clarifications": []
  },
  "library": {
    "capabilities": [
      {
        "id": "cap-store-ops",
        "name": "门店运营",
        "level": 1,
        "description": "支撑门店日常经营和导购协作。",
        "ownerActorIds": [],
        "supportingSystemIds": []
      }
    ],
    "actors": [],
    "flowSteps": [],
    "systems": []
  },
  "relations": [],
  "views": [
    {
      "id": "view-capability",
      "type": "business-capability-map",
      "title": "业务能力蓝图",
      "includedNodeIds": ["cap-store-ops"],
      "includedRelationIds": [],
      "layout": {},
      "annotations": []
    }
  ],
  "editor": {
    "fieldLocks": {},
    "theme": "enterprise-default"
  },
  "artifacts": {}
}
```

Modify `D:\projects\business-blueprint-skill\business_blueprint\cli.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .generate import write_plan_output
from .model import load_json
from .validate import validate_blueprint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Output blueprint json path.")
    parser.add_argument("--generate", help="Generate the canonical blueprint JSON and viewer.")
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Export SVG, draw.io, and Excalidraw artifacts.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--industry", default="common", help="Template pack name.")
    return parser


def _read_source_text(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    return path.read_text(encoding="utf-8") if path.exists() else value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.plan:
        source_text = _read_source_text(args.from_path)
        write_plan_output(Path(args.plan), source_text, args.industry, Path.cwd())
        return 0

    if args.validate:
        payload = load_json(Path(args.validate))
        print(json.dumps(validate_blueprint(payload), ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the generation test to verify it passes**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_generate.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit the generation pipeline**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add business_blueprint\generate.py business_blueprint\templates\retail\seed.json business_blueprint\cli.py tests\test_generate.py
git commit -m "feat: generate blueprint json from text input"
```

---

### Task 5: Build the static viewer and explicit save loop

**Files:**
- Create: `D:\projects\business-blueprint-skill\business_blueprint\viewer.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\assets\viewer.html`
- Create: `D:\projects\business-blueprint-skill\tests\test_viewer.py`
- Modify: `D:\projects\business-blueprint-skill\business_blueprint\cli.py`

- [ ] **Step 1: Write failing tests for viewer generation and handoff metadata**

Write `D:\projects\business-blueprint-skill\tests\test_viewer.py`:

```python
import json
from pathlib import Path

from business_blueprint.model import write_json
from business_blueprint.viewer import write_viewer_package


def test_write_viewer_package_creates_viewer_and_handoff(tmp_path: Path) -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "rev-1", "lastModifiedBy": "ai"},
        "context": {},
        "library": {"capabilities": [], "actors": [], "flowSteps": [], "systems": []},
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
```

- [ ] **Step 2: Run the viewer test to verify it fails**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_viewer.py -q
```

Expected: FAIL with `ImportError` for `business_blueprint.viewer`.

- [ ] **Step 3: Implement the viewer package writer and static HTML**

Write `D:\projects\business-blueprint-skill\business_blueprint\viewer.py`:

```python
from __future__ import annotations

from pathlib import Path
import json

from .model import load_json, write_json


def write_viewer_package(blueprint_path: Path, viewer_path: Path, handoff_path: Path, patch_path: Path) -> None:
    blueprint = load_json(blueprint_path)
    asset_path = Path(__file__).parent / "assets" / "viewer.html"
    viewer_template = asset_path.read_text(encoding="utf-8")
    rendered = viewer_template.replace("__BLUEPRINT_JSON__", json.dumps(blueprint, ensure_ascii=False))
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
```

Write `D:\projects\business-blueprint-skill\business_blueprint\assets\viewer.html`:

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>Business Blueprint Viewer</title>
    <style>
      body { font-family: "Segoe UI", sans-serif; margin: 0; background: #f5f7fb; color: #18212f; }
      header { display: flex; justify-content: space-between; padding: 16px 20px; background: #0f2742; color: white; }
      main { display: grid; grid-template-columns: 260px 1fr; min-height: calc(100vh - 64px); }
      aside, section { padding: 20px; }
      aside { background: white; border-right: 1px solid #d9e1ec; }
      .badge { display: inline-block; padding: 4px 8px; background: #d8e8ff; border-radius: 999px; font-size: 12px; }
      textarea { width: 100%; min-height: 160px; }
      button { padding: 10px 14px; border: none; border-radius: 8px; background: #1c5bd9; color: white; cursor: pointer; }
    </style>
  </head>
  <body>
    <script>
      const blueprint = __BLUEPRINT_JSON__;
      let patchLog = [];

      function updateSummary() {
        document.getElementById("revision-id").textContent = blueprint.meta.revisionId || "unknown";
        document.getElementById("dirty-state").textContent = patchLog.length ? "Unsaved edits" : "Saved";
        document.getElementById("json-view").value = JSON.stringify(blueprint, null, 2);
      }

      function renameTitle() {
        const nextValue = document.getElementById("title-input").value.trim();
        blueprint.meta.title = nextValue || blueprint.meta.title || "Generated Blueprint";
        blueprint.editor = blueprint.editor || {};
        blueprint.editor.fieldLocks = blueprint.editor.fieldLocks || {};
        blueprint.editor.fieldLocks["meta.title"] = "human";
        patchLog.push({ op: "update_meta", fields: { title: blueprint.meta.title } });
        updateSummary();
      }

      function exportRevision() {
        const blob = new Blob([JSON.stringify(blueprint, null, 2)], { type: "application/json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "solution.blueprint.json";
        link.click();
      }

      window.addEventListener("DOMContentLoaded", () => {
        document.getElementById("title-input").value = blueprint.meta.title || "";
        document.getElementById("rename-button").addEventListener("click", renameTitle);
        document.getElementById("save-button").addEventListener("click", exportRevision);
        updateSummary();
      });
    </script>
    <header>
      <div>
        <strong>Business Blueprint Viewer</strong>
        <div class="badge">Revision <span id="revision-id"></span></div>
      </div>
      <div id="dirty-state">Saved</div>
    </header>
    <main>
      <aside>
        <label for="title-input">Title</label>
        <input id="title-input" />
        <div style="margin-top: 12px;">
          <button id="rename-button" type="button">Apply Title</button>
        </div>
        <div style="margin-top: 12px;">
          <button id="save-button" type="button">Export Revision Package</button>
        </div>
      </aside>
      <section>
        <label for="json-view">Current canonical JSON</label>
        <textarea id="json-view" readonly></textarea>
      </section>
    </main>
  </body>
</html>
```

Modify `D:\projects\business-blueprint-skill\business_blueprint\cli.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .generate import write_plan_output
from .model import load_json
from .validate import validate_blueprint
from .viewer import write_viewer_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Output blueprint json path.")
    parser.add_argument("--generate", help="Output viewer html path.")
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Export SVG, draw.io, and Excalidraw artifacts.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--industry", default="common", help="Template pack name.")
    return parser


def _read_source_text(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    return path.read_text(encoding="utf-8") if path.exists() else value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.plan:
        source_text = _read_source_text(args.from_path)
        write_plan_output(Path(args.plan), source_text, args.industry, Path.cwd())
        return 0

    if args.generate:
        blueprint_path = Path(args.from_path or "solution.blueprint.json")
        viewer_path = Path(args.generate)
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=viewer_path.with_name("solution.handoff.json"),
            patch_path=viewer_path.with_name("solution.patch.jsonl"),
        )
        return 0

    if args.edit:
        blueprint_path = Path(args.edit)
        viewer_path = blueprint_path.with_suffix(".viewer.html")
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=blueprint_path.with_name("solution.handoff.json"),
            patch_path=blueprint_path.with_name("solution.patch.jsonl"),
        )
        return 0

    if args.validate:
        payload = load_json(Path(args.validate))
        print(json.dumps(validate_blueprint(payload), ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the viewer test to verify it passes**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_viewer.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit the viewer and save loop**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add business_blueprint\viewer.py business_blueprint\assets\viewer.html business_blueprint\cli.py tests\test_viewer.py
git commit -m "feat: add static viewer and revision handoff package"
```

---

### Task 6: Implement SVG, draw.io, and Excalidraw export adapters

**Files:**
- Create: `D:\projects\business-blueprint-skill\business_blueprint\export_svg.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\export_drawio.py`
- Create: `D:\projects\business-blueprint-skill\business_blueprint\export_excalidraw.py`
- Create: `D:\projects\business-blueprint-skill\tests\test_exporters.py`
- Modify: `D:\projects\business-blueprint-skill\business_blueprint\cli.py`

- [ ] **Step 1: Write failing exporter tests**

Write `D:\projects\business-blueprint-skill\tests\test_exporters.py`:

```python
import json
from pathlib import Path

from business_blueprint.export_drawio import export_drawio
from business_blueprint.export_excalidraw import export_excalidraw
from business_blueprint.export_svg import export_svg


BLUEPRINT = {
    "meta": {"title": "Demo"},
    "library": {
        "capabilities": [{"id": "cap-membership", "name": "会员运营"}],
        "actors": [],
        "flowSteps": [],
        "systems": [{"id": "sys-crm", "name": "CRM", "capabilityIds": ["cap-membership"]}],
    },
    "views": [
        {
            "id": "view-capability",
            "type": "business-capability-map",
            "title": "业务能力蓝图",
            "includedNodeIds": ["cap-membership", "sys-crm"],
            "includedRelationIds": [],
            "layout": {},
            "annotations": [],
        }
    ],
}


def test_export_svg_writes_svg_markup(tmp_path: Path) -> None:
    target = tmp_path / "diagram.svg"
    export_svg(BLUEPRINT, target)
    assert target.read_text(encoding="utf-8").startswith("<svg")


def test_export_drawio_writes_mxfile(tmp_path: Path) -> None:
    target = tmp_path / "diagram.drawio"
    export_drawio(BLUEPRINT, target)
    assert "<mxfile" in target.read_text(encoding="utf-8")


def test_export_excalidraw_writes_json(tmp_path: Path) -> None:
    target = tmp_path / "diagram.excalidraw"
    export_excalidraw(BLUEPRINT, target)
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["type"] == "excalidraw"
```

- [ ] **Step 2: Run the exporter tests to verify they fail**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_exporters.py -q
```

Expected: FAIL with `ImportError` for exporter modules.

- [ ] **Step 3: Implement minimal export adapters**

Write `D:\projects\business-blueprint-skill\business_blueprint\export_svg.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any


def export_svg(blueprint: dict[str, Any], target: Path) -> None:
    labels = [node["name"] for node in blueprint["library"].get("capabilities", []) + blueprint["library"].get("systems", [])]
    rows = "".join(
        f'<text x="24" y="{40 + index * 28}" font-size="14" fill="#18212f">{label}</text>'
        for index, label in enumerate(labels)
    )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{max(200, 80 + len(labels) * 28)}">{rows}</svg>'
    target.write_text(svg, encoding="utf-8")
```

Write `D:\projects\business-blueprint-skill\business_blueprint\export_drawio.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any


def export_drawio(blueprint: dict[str, Any], target: Path) -> None:
    labels = [node["name"] for node in blueprint["library"].get("capabilities", []) + blueprint["library"].get("systems", [])]
    cells = "".join(
        f'<mxCell id="cell-{index}" value="{label}" vertex="1" parent="1"><mxGeometry x="40" y="{40 + index * 70}" width="180" height="48" as="geometry"/></mxCell>'
        for index, label in enumerate(labels, start=1)
    )
    xml = f'<mxfile host="app.diagrams.net"><diagram name="Blueprint"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>{cells}</root></mxGraphModel></diagram></mxfile>'
    target.write_text(xml, encoding="utf-8")
```

Write `D:\projects\business-blueprint-skill\business_blueprint\export_excalidraw.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def export_excalidraw(blueprint: dict[str, Any], target: Path) -> None:
    elements = []
    labels = blueprint["library"].get("capabilities", []) + blueprint["library"].get("systems", [])
    for index, node in enumerate(labels):
        elements.append(
            {
                "id": node["id"],
                "type": "rectangle",
                "x": 40,
                "y": 40 + index * 80,
                "width": 180,
                "height": 56,
                "strokeColor": "#1c5bd9",
                "backgroundColor": "#d8e8ff",
                "fillStyle": "solid",
                "seed": index + 1,
                "version": 1,
                "versionNonce": index + 10,
                "isDeleted": False,
            }
        )
    payload = {"type": "excalidraw", "version": 2, "source": "business-blueprint-skill", "elements": elements}
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
```

Modify `D:\projects\business-blueprint-skill\business_blueprint\cli.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .export_drawio import export_drawio
from .export_excalidraw import export_excalidraw
from .export_svg import export_svg
from .generate import write_plan_output
from .model import load_json
from .validate import validate_blueprint
from .viewer import write_viewer_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Output blueprint json path.")
    parser.add_argument("--generate", help="Output viewer html path.")
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Blueprint path to export from.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--industry", default="common", help="Template pack name.")
    return parser


def _read_source_text(value: str | None) -> str:
    if not value:
        return ""
    path = Path(value)
    return path.read_text(encoding="utf-8") if path.exists() else value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.plan:
        source_text = _read_source_text(args.from_path)
        write_plan_output(Path(args.plan), source_text, args.industry, Path.cwd())
        return 0

    if args.generate:
        blueprint_path = Path(args.from_path or "solution.blueprint.json")
        viewer_path = Path(args.generate)
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=viewer_path.with_name("solution.handoff.json"),
            patch_path=viewer_path.with_name("solution.patch.jsonl"),
        )
        return 0

    if args.edit:
        blueprint_path = Path(args.edit)
        viewer_path = blueprint_path.with_suffix(".viewer.html")
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=blueprint_path.with_name("solution.handoff.json"),
            patch_path=blueprint_path.with_name("solution.patch.jsonl"),
        )
        return 0

    if args.export:
        blueprint_path = Path(args.export)
        blueprint = load_json(blueprint_path)
        export_dir = blueprint_path.with_name("solution.exports")
        export_dir.mkdir(parents=True, exist_ok=True)
        export_svg(blueprint, export_dir / "solution.svg")
        export_drawio(blueprint, export_dir / "solution.drawio")
        export_excalidraw(blueprint, export_dir / "solution.excalidraw")
        return 0

    if args.validate:
        payload = load_json(Path(args.validate))
        print(json.dumps(validate_blueprint(payload), ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the exporter tests to verify they pass**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_exporters.py -q
```

Expected: PASS with `3 passed`.

- [ ] **Step 5: Commit the export adapters**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add business_blueprint\export_svg.py business_blueprint\export_drawio.py business_blueprint\export_excalidraw.py business_blueprint\cli.py tests\test_exporters.py
git commit -m "feat: add svg drawio and excalidraw exporters"
```

---

### Task 7: Package the skill, references, and end-to-end workflow tests

**Files:**
- Create: `D:\projects\business-blueprint-skill\SKILL.md`
- Create: `D:\projects\business-blueprint-skill\agents\openai.yaml`
- Create: `D:\projects\business-blueprint-skill\references\blueprint-schema.md`
- Create: `D:\projects\business-blueprint-skill\references\industry-packs.md`
- Create: `D:\projects\business-blueprint-skill\references\authoring-rules.md`
- Create: `D:\projects\business-blueprint-skill\examples\sample.blueprint.json`
- Create: `D:\projects\business-blueprint-skill\tests\test_e2e.py`

- [ ] **Step 1: Write the failing end-to-end test**

Write `D:\projects\business-blueprint-skill\tests\test_e2e.py`:

```python
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_generate_and_export_end_to_end(tmp_path: Path) -> None:
    source = tmp_path / "brief.txt"
    source.write_text("零售客户需要会员运营、门店导购和CRM集成。", encoding="utf-8")
    blueprint = tmp_path / "solution.blueprint.json"
    viewer = tmp_path / "solution.viewer.html"

    subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--plan", str(blueprint), "--from", str(source), "--industry", "retail"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--generate", str(viewer), "--from", str(blueprint)],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--export", str(blueprint)],
        cwd=ROOT,
        check=True,
    )

    assert viewer.exists()
    assert (tmp_path / "solution.exports" / "solution.svg").exists()
    validation = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--validate", str(blueprint)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(validation.stdout)
    assert "summary" in payload
```

- [ ] **Step 2: Run the end-to-end test to verify it fails**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest tests/test_e2e.py -q
```

Expected: FAIL because the skill docs and example files do not exist yet.

- [ ] **Step 3: Add the skill package and reference docs**

Write `D:\projects\business-blueprint-skill\SKILL.md`:

```markdown
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
```

Write `D:\projects\business-blueprint-skill\agents\openai.yaml`:

```yaml
display_name: Business Blueprint Skill
short_description: Generate AI-friendly business blueprint IR and exports
default_prompt: Generate editable business capability, swimlane, and application architecture artifacts from presales inputs.
```

Write `D:\projects\business-blueprint-skill\references\blueprint-schema.md`:

```markdown
# Blueprint Schema Reference

The canonical file contains:

- `meta`
- `context`
- `library`
- `relations`
- `views`
- `editor`
- `artifacts`

Entity collections in `library`:

- `capabilities`
- `actors`
- `flowSteps`
- `systems`
```

Write `D:\projects\business-blueprint-skill\references\industry-packs.md`:

```markdown
# Industry Packs

Industry packs may provide:

- schema-valid seed data
- aliases and terminology defaults
- grouping defaults

Industry packs may not:

- change the canonical schema
- add renderer-specific behavior
- replace the common validation rules
```

Write `D:\projects\business-blueprint-skill\references\authoring-rules.md`:

```markdown
# Authoring Rules

- The viewer save action must export a new canonical revision package.
- `solution.patch.jsonl` records human edits.
- `editor.fieldLocks` protects human-edited semantic fields.
- Validation must run before downstream completion claims.
```

Write `D:\projects\business-blueprint-skill\examples\sample.blueprint.json`:

```json
{
  "version": "1.0",
  "meta": {
    "title": "Retail Membership Blueprint",
    "industry": "retail",
    "revisionId": "rev-example",
    "parentRevisionId": null,
    "lastModifiedAt": "2026-04-12T00:00:00Z",
    "lastModifiedBy": "ai"
  },
  "context": {
    "goals": ["提升会员运营效率"],
    "scope": [],
    "assumptions": [],
    "constraints": [],
    "sourceRefs": [],
    "clarifyRequests": [],
    "clarifications": []
  },
  "library": {
    "capabilities": [
      {
        "id": "cap-membership",
        "name": "会员运营",
        "level": 1,
        "description": "管理会员生命周期。",
        "ownerActorIds": ["actor-store-guide"],
        "supportingSystemIds": ["sys-crm"]
      }
    ],
    "actors": [{"id": "actor-store-guide", "name": "门店导购"}],
    "flowSteps": [],
    "systems": [
      {
        "id": "sys-crm",
        "name": "CRM",
        "category": "business-app",
        "capabilityIds": ["cap-membership"]
      }
    ]
  },
  "relations": [],
  "views": [],
  "editor": {
    "fieldLocks": {},
    "theme": "enterprise-default"
  },
  "artifacts": {}
}
```

- [ ] **Step 4: Run the end-to-end test and full suite**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
python -m pytest -q
```

Expected: PASS with all tests green.

- [ ] **Step 5: Commit the packaged skill**

Run:

```powershell
Set-Location D:\projects\business-blueprint-skill
git add SKILL.md agents\openai.yaml references\blueprint-schema.md references\industry-packs.md references\authoring-rules.md examples\sample.blueprint.json tests\test_e2e.py
git commit -m "feat: package blueprint skill and end to end workflow"
```

---

## Self-Review

### Spec coverage

- Canonical IR: covered by Tasks 2, 3, and 4.
- Save loop and revision handoff: covered by Task 5.
- Entity resolution and clarify rules: covered by Task 3.
- Validation shape and linkage completeness: covered by Task 2.
- Exporters: covered by Task 6.
- Skill packaging and downstream collaboration boundary: covered by Task 7.

### Placeholder scan

No `TODO`, `TBD`, or "implement later" placeholders remain in the plan. Every task includes exact files, commands, and minimal code.

### Type consistency

- Canonical file name remains `solution.blueprint.json` across all tasks.
- Handoff metadata uses `revisionId`, `parentRevisionId`, `lastModifiedAt`, and `lastModifiedBy` consistently.
- Human edit protection uses `editor.fieldLocks` and `solution.patch.jsonl` consistently across the viewer, skill docs, and references.
