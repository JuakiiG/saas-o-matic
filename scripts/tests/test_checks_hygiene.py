"""Tests of the repository hygiene block, against throwaway git repositories."""

from __future__ import annotations

import unittest
from pathlib import Path

from oracle import checks_hygiene, report
from tests import support

# Assembled so that the commit messages of this repository never contain the trailer.
TRAILER = "Co-Authored" + "-By: Some Tool <tool@example.invalid>"


class HygieneTest(unittest.TestCase):
    def repo(self, ignore_private: bool = True) -> Path:
        root = support.make_repo(self, support.BORRADOR)
        support.git_init(root)
        support.write(root / ".gitignore", ".private/\n" if ignore_private else "")
        support.commit_all(root, "docs: primer commit")
        return root

    def test_clean_repository_passes_the_three_checks(self) -> None:
        root = self.repo()
        support.write(root / ".private" / "notes.md", "privado\n")
        for check in (checks_hygiene.check_trailers, checks_hygiene.check_line_endings, checks_hygiene.check_private):
            with self.subTest(check=check.__name__):
                self.assertEqual(check(root).status, report.OK)

    def test_coauthor_trailer_fails_and_names_the_commit(self) -> None:
        root = self.repo()
        support.write(root / "a.md", "x\n")
        support.commit_all(root, f"docs: con trailer\n\n{TRAILER}")
        result = checks_hygiene.check_trailers(root)
        self.assertEqual(result.status, report.FAIL)
        self.assertIn(support.git(root, "rev-parse", "--short", "HEAD").strip(), result.details[0])

    def test_tool_signature_fails(self) -> None:
        root = self.repo()
        support.write(root / "a.md", "x\n")
        support.commit_all(root, "docs: firmado\n\nGenerated " + "with [Some Tool](https://example.invalid)")
        self.assertEqual(checks_hygiene.check_trailers(root).status, report.FAIL)

    def test_mentioning_the_rule_in_prose_is_not_a_trailer(self) -> None:
        root = self.repo()
        support.write(root / "a.md", "x\n")
        support.commit_all(root, "docs: regla sin trailers de coautoría\n\nSe quita la línea de coautoría.")
        self.assertEqual(checks_hygiene.check_trailers(root).status, report.OK)

    def test_crlf_in_a_tracked_text_file_fails(self) -> None:
        root = self.repo()
        (root / "crlf.md").write_bytes(b"uno\r\ndos\r\n")
        support.commit_all(root, "docs: con crlf")
        result = checks_hygiene.check_line_endings(root)
        self.assertEqual(result.status, report.FAIL)
        self.assertIn("crlf.md", result.details[0])

    def test_binary_files_are_not_text(self) -> None:
        root = self.repo()
        (root / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\r\n")
        support.commit_all(root, "docs: binario")
        self.assertEqual(checks_hygiene.check_line_endings(root).status, report.OK)

    def test_tracked_private_folder_fails(self) -> None:
        root = self.repo(ignore_private=False)
        support.write(root / ".private" / "notes.md", "privado\n")
        support.commit_all(root, "docs: privado por error")
        result = checks_hygiene.check_private(root)
        self.assertEqual(result.status, report.FAIL)

    def test_private_folder_that_is_not_ignored_fails_even_if_untracked(self) -> None:
        root = self.repo(ignore_private=False)
        self.assertEqual(checks_hygiene.check_private(root).status, report.FAIL)

    def test_private_folder_removed_but_present_in_history_fails(self) -> None:
        root = self.repo(ignore_private=False)
        support.write(root / ".private" / "notes.md", "privado\n")
        support.commit_all(root, "docs: privado por error")
        support.git(root, "rm", "-r", "-q", "--cached", ".private")
        support.write(root / ".gitignore", ".private/\n")
        support.commit_all(root, "chore: deja de versionar")
        self.assertEqual(checks_hygiene.check_private(root).status, report.FAIL)


if __name__ == "__main__":
    unittest.main()
