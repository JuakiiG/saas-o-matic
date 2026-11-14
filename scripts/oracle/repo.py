"""Access to the repository: processes, git and file reading."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

# What cmd.exe itself assumes when PATHEXT is not set.
_DEFAULT_PATHEXT = ".COM;.EXE;.BAT;.CMD"


class OracleError(Exception):
    """A check could not be carried out; the oracle reports it as a failure."""


def find_executable(name: str) -> str | None:
    """Path of a tool that the operating system can start, or None if it is not on the PATH.

    Node installs `npm`, a POSIX shell script, next to `npm.cmd`. Windows cannot start a file
    without one of the PATHEXT extensions, and with Python 3.12.0 `shutil.which("npm")` returns
    that script before the `.cmd` file, so on Windows the twin with an extension is preferred.
    """
    found = shutil.which(name)
    if found is None or sys.platform != "win32":
        return found
    extensions = [ext for ext in os.environ.get("PATHEXT", _DEFAULT_PATHEXT).split(os.pathsep) if ext]
    if found.upper().endswith(tuple(ext.upper() for ext in extensions)):
        return found
    for extension in extensions:
        if os.path.isfile(found + extension):
            return found + extension
    return found


def run(command: list[str], cwd: Path) -> tuple[int, str]:
    """Run a tool without a shell and return its exit code and combined output."""
    executable = find_executable(command[0])
    if executable is None:
        raise OracleError(f"no se encuentra `{command[0]}` en el PATH")
    try:
        done = subprocess.run(
            [executable, *command[1:]],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as error:
        raise OracleError(f"no se pudo ejecutar `{' '.join(command)}`: {error}") from error
    return done.returncode, done.stdout


def git(root: Path, *args: str) -> str:
    """Run git and return its output; a git failure is an oracle error."""
    code, output = run(["git", "-c", "core.quotepath=off", *args], root)
    if code != 0:
        raise OracleError(f"`git {' '.join(args)}` terminó con código {code}: {output.strip()}")
    return output


def listed_files(root: Path) -> list[str]:
    """Tracked files plus untracked ones that git does not ignore, with `/` separators."""
    output = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    return sorted({name for name in output.split("\0") if name})


def read_text(path: Path) -> str | None:
    """Text of a file, or None if it is missing or is not UTF-8 text."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def tail(output: str, lines: int = 15) -> str:
    """Last lines of a tool output, enough to see why it failed."""
    return "\n".join(output.strip().splitlines()[-lines:])
