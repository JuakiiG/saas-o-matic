"""Tests of how the oracle starts the tools it runs."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from oracle import repo
from tests import support

TOOL = "oracle-probe-tool"
GREETING = "probe ok"


class RunTest(unittest.TestCase):
    def _folder_with_tool(self) -> Path:
        """A folder holding the tool the way Node ships npm: a POSIX script and its `.cmd` twin."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        folder = Path(temporary.name)
        script = support.write(folder / TOOL, f"#!/bin/sh\necho {GREETING}\n")
        script.chmod(0o755)
        support.write(folder / f"{TOOL}.cmd", f"@echo {GREETING}\n")
        return folder

    def test_a_tool_shipped_as_a_script_and_a_cmd_file_starts_on_every_system(self) -> None:
        folder = self._folder_with_tool()
        path = str(folder) + os.pathsep + os.environ.get("PATH", "")
        with mock.patch.dict(os.environ, {"PATH": path}):
            try:
                code, output = repo.run([TOOL], folder)
            except repo.OracleError as error:
                self.fail(f"the tool could not be started: {error}")
        self.assertEqual((code, output.strip()), (0, GREETING))

    def test_a_tool_that_is_not_installed_is_an_oracle_error(self) -> None:
        folder = self._folder_with_tool()
        with self.assertRaises(repo.OracleError) as raised:
            repo.run(["oracle-tool-that-does-not-exist"], folder)
        self.assertIn("no se encuentra", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
