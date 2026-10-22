"""Generator conformance: ten needs in, ten conforming workspaces out.

This is the test that turns "the method is copyable" from a claim into evidence.
Each input is a plain need in someone's own words; the generator must produce a
domain that passes every MUST without human editing.

    python -m unittest discover -s tests
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check  # noqa: E402
import new_domain  # noqa: E402

TEMPLATES = ROOT / "templates"
INPUTS = sorted((ROOT / "examples" / "inputs").glob("*.json"))
GOLDEN = ROOT / "examples" / "golden"


def seed_workspace(root: Path, lang: str = "en") -> Path:
    identity = TEMPLATES / ("AGENTS.zh.md" if lang == "zh" else "AGENTS.md")
    (root / "AGENTS.md").write_text(identity.read_text(encoding="utf-8"), encoding="utf-8")
    return root


def failures(ws: Path) -> list:
    return [f for f in check.run(ws) if f.level == "FAIL"]


class TestGeneratorConformance(unittest.TestCase):
    def test_ten_needs_produce_conforming_domains(self):
        self.assertGreaterEqual(len(INPUTS), 10, "keep at least ten inputs")
        for path in INPUTS:
            spec = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(input=path.name), tempfile.TemporaryDirectory() as tmp:
                ws = seed_workspace(Path(tmp), spec["lang"])
                with contextlib.redirect_stdout(io.StringIO()):
                    code = new_domain.main([
                        spec["name"],
                        "--need", spec["need"],
                        "--words", spec["words"],
                        "--lang", spec["lang"],
                        "--workspace", str(ws),
                        "--date", "2026-10-23",
                        "--yes",
                    ])
                self.assertEqual(code, 0, f"{path.name}: generator refused")
                self.assertEqual(failures(ws), [], f"{path.name}: not conforming")

    def test_generator_refuses_outside_a_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(io.StringIO()):
                code = new_domain.main([
                    "ca-x", "--need", "test", "--words", "test",
                    "--workspace", tmp, "--yes",
                ])
            self.assertEqual(code, 2)

    def test_generated_manual_names_the_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = seed_workspace(Path(tmp))
            with contextlib.redirect_stdout(io.StringIO()):
                new_domain.main(["ca-x", "--need", "keep a list", "--words", "list/item",
                                 "--workspace", str(ws), "--yes"])
            text = (ws / "ca-x" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("name: ca-x", text)
            self.assertIn("Use when", text)


class TestGoldenFixture(unittest.TestCase):
    def test_golden_domain_conforms_inside_a_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = seed_workspace(Path(tmp))
            shutil.copytree(GOLDEN / "ca-reading", ws / "ca-reading")
            self.assertEqual(failures(ws), [])

    def test_golden_reporter_runs(self):
        script = GOLDEN / "ca-reading" / "4-engine" / "report.py"
        result = subprocess.run(
            [sys.executable, str(script), "--week", "--field", "pages"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("records:", result.stdout)


if __name__ == "__main__":
    unittest.main()
