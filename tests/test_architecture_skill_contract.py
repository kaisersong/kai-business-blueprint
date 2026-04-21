from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_skill_architecture_rules_lock_dark_default_and_light_override() -> None:
    skill_text = _read("SKILL.md")

    assert "Use dark mode by default" in skill_text
    assert "Only use light mode when the user explicitly asks for it." in skill_text


def test_skill_architecture_rules_ban_toothpaste_layout_and_top_right_legend() -> None:
    skill_text = _read("SKILL.md")

    assert "Never force every node in a layer into one fixed row" in skill_text
    assert "Legend must live in a bottom safe area" in skill_text
    assert "Never place the legend as a floating overlay in the top-right corner." in skill_text
    assert "Do not use fixed-height wrappers or `overflow: hidden`" in skill_text


def test_design_system_requires_bottom_legend_and_no_clipping() -> None:
    design_text = _read("references/architecture-design-system.md")

    assert "暗黑模式是默认输出" in design_text
    assert "禁止通过把整层强行塞成一行" in design_text
    assert "Legend 默认放在左下或底部保留区" in design_text
    assert "禁止将 legend 放在 top-right 覆盖标题区或内容区" in design_text
    assert "不得使用固定高度裁切内容" in design_text
    assert "禁止使用 `overflow: hidden`" in design_text


def test_architecture_templates_are_references_not_fixed_geometry() -> None:
    serverless_text = _read("references/architecture-templates/serverless.md")
    microservices_text = _read("references/architecture-templates/microservices.md")

    assert "结构参考，不是必须死守的固定像素模板" in serverless_text
    assert "回退到 `freeflow`" in serverless_text
    assert "Legend 放在左下或底部保留区" in serverless_text

    assert "只是起始参考，不是必须照抄的固定布局" in microservices_text
    assert "回退到 `freeflow`" in microservices_text
    assert "Legend 放在左下或底部保留区" in microservices_text
