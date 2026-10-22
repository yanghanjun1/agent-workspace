"""Tests for the conformance checker. Standard library only.

    python -m unittest discover -s tests

Each test builds a throwaway workspace, breaks exactly one rule, and asserts
that the matching MUST fires. A checker that cannot fail is not a checker.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check  # noqa: E402


IDENTITY_OK = """# AGENTS.md - test workspace

## 我是谁
测试助手。

## 谁归我
| 域 | 目录 | 一句话 | 手册 |
|---|---|---|---|
| 测试 | `ca-x/` | 测试用 | `ca-x/SKILL.md` |

## 任务 -> 读哪个技能
| 主人说什么 | 读 |
|---|---|
| 测试 / 试一下 | `ca-x` |
"""

SKILL_OK = """---
name: ca-x
description: Use when 主人提测试/试一下，或要跑一次测试。
---

# ca-x

## 何时加载
- 测试

## 记录格式
- 一行一条
"""

LOG_OK = """# 事件日志

## 2026-10-23
- 今天做了：跑通第一个域
"""

DECISIONS_OK = """# 决策日志

- 2026-10-23 · 从「无」→「有」· 因为需要一个测试域
"""


def make_ws(tmp: str, identity: str | None = IDENTITY_OK, domain: str | None = "ca-x",
            skill: str | None = SKILL_OK, log: str | None = LOG_OK,
            decisions: str | None = DECISIONS_OK) -> Path:
    ws = Path(tmp)
    if identity is not None:
        (ws / "AGENTS.md").write_text(identity, encoding="utf-8")
    if domain is not None:
        dom = ws / domain
        dom.mkdir(exist_ok=True)
        if skill is not None:
            (dom / "SKILL.md").write_text(skill, encoding="utf-8")
        if log is not None:
            (dom / "log.md").write_text(log, encoding="utf-8")
        if decisions is not None:
            (dom / "decisions.md").write_text(decisions, encoding="utf-8")
    return ws


def failures(findings: list) -> list:
    return [f for f in findings if f.level == "FAIL"]


def rules(findings: list) -> set:
    return {f.rule for f in failures(findings)}


class TestConforming(unittest.TestCase):
    def test_clean_workspace_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp)
            self.assertEqual(failures(check.run(ws)), [])

    def test_output_survives_cp936_console(self):
        # The real constraint is a Chinese Windows console, not ASCII: filenames
        # may be Chinese, but decorative glyphs (check marks, arrows) crash it.
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, log=None)
            for finding in check.run(ws):
                str(finding).encode("gbk")


class TestM0(unittest.TestCase):
    def test_domain_is_not_a_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, identity=None)
            self.assertIn("M0", rules(check.run(ws)))

    def test_nested_workspace_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_ws(tmp)
            inner = Path(tmp) / "inner"
            inner.mkdir()
            (inner / "AGENTS.md").write_text(IDENTITY_OK, encoding="utf-8")
            self.assertIn("M0", rules(check.run(inner)))


class TestM1(unittest.TestCase):
    def test_identity_over_budget(self):
        filler = "\n".join(f"filler line number {i:03d}" for i in range(250))
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, identity=IDENTITY_OK + "\n" + filler + "\n")
            self.assertIn("M1", rules(check.run(ws)))

    def test_no_routing_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, identity="# AGENTS.md\n\n## 我是谁\n测试助手。\n")
            self.assertIn("M1", rules(check.run(ws)))

    def test_secret_in_identity(self):
        secret = "\nkey: sk-abcdefghijklmnopqrstuvwx\n"
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, identity=IDENTITY_OK + secret)
            self.assertIn("M1", rules(check.run(ws)))


class TestM2(unittest.TestCase):
    def test_name_mismatch(self):
        skill = SKILL_OK.replace("name: ca-x", "name: ca-y")
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, skill=skill)
            self.assertIn("M2", rules(check.run(ws)))

    def test_description_too_short(self):
        skill = SKILL_OK.replace(
            "description: Use when 主人提测试/试一下，或要跑一次测试。",
            "description: test")
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, skill=skill)
            self.assertIn("M2", rules(check.run(ws)))


class TestM3(unittest.TestCase):
    def test_empty_event_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, log="# 事件日志\n")
            self.assertIn("M3", rules(check.run(ws)))

    def test_missing_decision_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, decisions=None)
            self.assertIn("M3", rules(check.run(ws)))


class TestM4(unittest.TestCase):
    def test_entry_without_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, decisions="# 决策日志\n\n- 随手记的一条，没有日期\n")
            self.assertIn("M4a", rules(check.run(ws)))


class TestM5(unittest.TestCase):
    def test_numbers_without_script(self):
        skill = SKILL_OK + "\n## 统计口径\n- 按周统计阅读页数\n"
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, skill=skill)
            self.assertIn("M5", rules(check.run(ws)))

    def test_script_reference_missing(self):
        skill = SKILL_OK + "\n## 统计口径\n- 周报统计跑 `4-引擎/nope.py`\n"
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, skill=skill)
            self.assertIn("M5", rules(check.run(ws)))

    def test_script_reference_present(self):
        skill = SKILL_OK + "\n## 统计口径\n- 周报统计跑 `4-引擎/digest.py`\n"
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, skill=skill)
            (ws / "ca-x" / "4-引擎").mkdir()
            (ws / "ca-x" / "4-引擎" / "digest.py").write_text("# stub\n", encoding="utf-8")
            self.assertNotIn("M5", rules(check.run(ws)))


class TestM6(unittest.TestCase):
    def test_identity_copies_manual(self):
        shared = "口径：按周一起算，不按自然周"
        identity = IDENTITY_OK + f"\n{shared}\n"
        skill = SKILL_OK + f"\n{shared}\n"
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_ws(tmp, identity=identity, skill=skill)
            self.assertIn("M6", rules(check.run(ws)))


if __name__ == "__main__":
    unittest.main()
