"""Repository hygiene: commit messages, line endings and the private folder."""

from __future__ import annotations

import re
from pathlib import Path

from oracle import report
from oracle.repo import git, run

BLOCK = "Higiene del repo"
PRIVATE = ".private"
_SIGNATURES = re.compile(r"^\s*co-authored-by:|\bgenerated with\b|\N{ROBOT FACE}", re.IGNORECASE | re.MULTILINE)
_BAD_ENDINGS = ("crlf", "mixed")


def _has_commits(root: Path) -> bool:
    code, _ = run(["git", "rev-parse", "--verify", "--quiet", "HEAD"], root)
    return code == 0


def check_trailers(root: Path) -> report.Result:
    """No commit carries a co-author trailer or a tool signature (CLAUDE.md, "Commits")."""
    name = "Ningún commit con trailer de coautoría ni firma de herramienta"
    if not _has_commits(root):
        return report.passed(BLOCK, name, ["el repositorio no tiene commits"])
    log = git(root, "log", "--format=%h%x1f%s%x1f%B%x1e")
    problems = []
    for entry in filter(str.strip, log.split("\x1e")):
        short, subject, body = entry.strip().split("\x1f", 2)
        if _SIGNATURES.search(body):
            problems.append(f"{short} {subject}")
    return report.from_problems(BLOCK, name, problems)


def check_line_endings(root: Path) -> report.Result:
    """No tracked text file has CRLF, in the index or in the working tree."""
    name = "Ningún CRLF en ficheros versionados de texto"
    problems = []
    for entry in filter(None, git(root, "ls-files", "--eol", "-z").split("\0")):
        info, _, path = entry.partition("\t")
        index, worktree = info.split()[:2]
        if index.split("/")[-1] in _BAD_ENDINGS or worktree.split("/")[-1] in _BAD_ENDINGS:
            problems.append(f"{path}: {index} {worktree}")
    return report.from_problems(BLOCK, name, problems)


def check_private(root: Path) -> report.Result:
    """The private folder is ignored, is not tracked and never was."""
    name = f"`{PRIVATE}/` nunca versionado"
    problems = []
    if git(root, "ls-files", "--", PRIVATE).strip():
        problems.append(f"hay ficheros de {PRIVATE}/ versionados")
    ignored, _ = run(["git", "check-ignore", "--quiet", f"{PRIVATE}/probe"], root)
    if ignored != 0:
        problems.append(f"{PRIVATE}/ no está en .gitignore")
    if _has_commits(root):
        commits = git(root, "log", "--all", "--format=%h", "--", PRIVATE).split()
        if commits:
            problems.append(f"{PRIVATE}/ aparece en el historial: {', '.join(commits)}")
    return report.from_problems(BLOCK, name, problems)
