"""Tests of the PreToolUse hook: stdin payload in, exit code and decision out."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from hooks import pre_tool_use
from tests import support

HOOK = Path(pre_tool_use.__file__).resolve()


def payload(tool: str, **tool_input: str) -> str:
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input})


def decision(stdout: str) -> tuple[str, str]:
    output = json.loads(stdout)["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    return output["permissionDecision"], output["permissionDecisionReason"]


class EvaluateTest(unittest.TestCase):
    def test_denies_code_without_approved_spec(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        for tool, fields in (
            ("Write", {"file_path": str(root / "backend" / "app" / "probe.py"), "content": "x = 1\n"}),
            ("Edit", {"file_path": str(root / "backend" / "tests" / "test_probe.py"), "new_string": "x"}),
            ("Write", {"file_path": str(root / "frontend" / "src" / "app" / "probe.ts"), "content": ""}),
            ("Write", {"file_path": str(root / "frontend" / "src" / "app" / "probe.spec.ts"), "content": ""}),
            ("NotebookEdit", {"notebook_path": str(root / "backend" / "notes.ipynb"), "new_source": ""}),
        ):
            with self.subTest(tool=tool, fields=fields):
                code, stdout, stderr = pre_tool_use.evaluate(payload(tool, **fields), root)
                self.assertEqual((code, stderr), (0, ""))
                action, reason = decision(stdout)
                self.assertEqual(action, "deny")
                self.assertIn("SPEC-0", reason)

    def test_windows_separators_are_understood_everywhere(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        target = str(root / "backend" / "app" / "probe.py").replace("/", "\\")
        code, stdout, _ = pre_tool_use.evaluate(payload("Write", file_path=target, content=""), root)
        self.assertEqual(code, 0)
        self.assertEqual(decision(stdout)[0], "deny")

    def test_allows_silently_what_the_gate_does_not_cover(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        target = str(root / "ai-workspace" / "03-proceso" / "sesion-03.md")
        result = pre_tool_use.evaluate(payload("Write", file_path=target, content="x"), root)
        self.assertEqual(result, (0, "", ""))

    def test_allows_code_once_its_block_is_approved(self) -> None:
        root = support.make_repo(self, support.BACKEND_OK)
        target = str(root / "backend" / "app" / "main.py")
        result = pre_tool_use.evaluate(payload("Write", file_path=target, content="x"), root)
        self.assertEqual(result, (0, "", ""))

    def test_asks_before_touching_the_gate_or_approving_a_spec(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        spec = str(root / support.SPECS_DIR / support.SPEC_NAMES["SPEC-01"])
        for tool, fields in (
            ("Edit", {"file_path": str(root / ".claude" / "settings.json"), "new_string": "{}"}),
            ("Write", {"file_path": str(root / "scripts" / "hooks" / "pre_tool_use.py"), "content": ""}),
            ("Edit", {"file_path": spec, "old_string": "`borrador`", "new_string": "`aprobada`"}),
        ):
            with self.subTest(fields=fields):
                code, stdout, _ = pre_tool_use.evaluate(payload(tool, **fields), root)
                self.assertEqual(code, 0)
                self.assertEqual(decision(stdout)[0], "ask")

    def test_fails_closed_on_input_it_cannot_understand(self) -> None:
        root = support.make_repo(self, support.ALL_OK)
        for text in ("", "not json", "[]", payload("Write", content="no path"), '{"tool_name": "Edit"}'):
            with self.subTest(text=text):
                code, stdout, stderr = pre_tool_use.evaluate(text, root)
                self.assertEqual((code, stdout), (2, ""))
                self.assertTrue(stderr.strip())

    def test_other_tools_are_none_of_its_business(self) -> None:
        root = support.make_repo(self, support.BORRADOR)
        result = pre_tool_use.evaluate(payload("Bash", command="ls backend"), root)
        self.assertEqual(result, (0, "", ""))


class ScriptTest(unittest.TestCase):
    """Runs the real script; only cases that do not depend on the state of the real specs."""

    def run_hook(self, stdin: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HOOK)], input=stdin, capture_output=True, text=True, encoding="utf-8", check=False
        )

    def test_script_allows_a_log_file_of_this_repository(self) -> None:
        target = str(HOOK.parents[2] / "ai-workspace" / "03-proceso" / "probe.md")
        done = self.run_hook(payload("Write", file_path=target, content="x"))
        self.assertEqual((done.returncode, done.stdout), (0, ""))

    def test_script_blocks_with_exit_code_2_on_garbage(self) -> None:
        done = self.run_hook("not json")
        self.assertEqual(done.returncode, 2)
        self.assertEqual(done.stdout, "")
        self.assertTrue(done.stderr.strip())


if __name__ == "__main__":
    unittest.main()
