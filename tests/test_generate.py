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
