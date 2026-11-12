"""Spec gate: which paths are application code and whether their specs are approved.

Shared by the PreToolUse hook and by the oracle, so that both apply one rule
(CLAUDE.md, "Spec antes que código"). Standard library only.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

SPECS_DIR = ("ai-workspace", "01-specs")
APPROVED = "aprobada"
UNKNOWN = "desconocido"

# Top-level folder -> specs that must all be approved before writing code in it.
BLOCKS: dict[str, tuple[str, ...]] = {
    "backend": ("SPEC-01", "SPEC-02", "SPEC-03"),
    "frontend": ("SPEC-04",),
}
# Inside a gated folder, only documentation and placeholders are not code.
EXEMPT_SUFFIXES = (".md",)
EXEMPT_NAMES = (".gitkeep",)
# The gate itself: changing these needs a human, or the AI could open the door.
PROTECTED = (
    (".claude", "settings.json"),
    (".claude", "settings.local.json"),
    ("scripts", "hooks"),
    ("scripts", "oracle", "specgate.py"),
)

_STATE_ROW = re.compile(
    r"^\|\s*\*\*Estado\*\*\s*\|\s*`(aprobada|borrador)`\s*\(\d{4}-\d{2}-\d{2}\)", re.MULTILINE
)
_APPROVAL_WORD = re.compile(r"\baprobada\b", re.IGNORECASE)


@dataclass(frozen=True)
class Decision:
    """What to do with a write: `allow`, `deny` or `ask` (human confirmation)."""

    action: str
    reason: str = ""


def specs_dir(root: Path) -> Path:
    return root.joinpath(*SPECS_DIR)


def spec_state(directory: Path, spec_id: str) -> str:
    """State declared in the header of a spec; `desconocido` if it cannot be read."""
    matches = sorted(directory.glob(f"{spec_id}-*.md"))
    if len(matches) != 1:
        return UNKNOWN
    try:
        text = matches[0].read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return UNKNOWN
    found = _STATE_ROW.search(text)
    return found.group(1) if found else UNKNOWN


def relative_parts(root: Path, target: str) -> tuple[str, ...] | None:
    """Case-folded path parts of `target` below `root`, or None if it is outside.

    Backslashes count as separators on every system, `..` is resolved and the
    comparison ignores case, because Windows and macOS file systems do.
    """
    raw = target.replace("\\", "/")
    base = os.path.normpath(str(root).replace("\\", "/"))
    full = os.path.normpath(raw if os.path.isabs(raw) else os.path.join(base, raw))
    parts = _below(base, full)
    if parts is None:
        # The same folder can be reached through a link or a mapped drive.
        parts = _below(os.path.realpath(base), os.path.realpath(full))
    return parts


def _below(base: str, full: str) -> tuple[str, ...] | None:
    base_parts = tuple(part.casefold() for part in Path(base).parts)
    full_parts = tuple(part.casefold() for part in Path(full).parts)
    if full_parts[: len(base_parts)] != base_parts:
        return None
    return full_parts[len(base_parts) :]


def block_for(parts: tuple[str, ...]) -> str | None:
    """Gated block a path belongs to, or None if it is not application code."""
    if len(parts) < 2 or parts[0] not in BLOCKS:
        return None
    name = parts[-1]
    if name in EXEMPT_NAMES or name.endswith(EXEMPT_SUFFIXES):
        return None
    return parts[0]


def pending_specs(directory: Path, block: str) -> list[str]:
    """Specs of the block that are not approved yet, with their state."""
    states = ((spec, spec_state(directory, spec)) for spec in BLOCKS[block])
    return [f"{spec} ({state})" for spec, state in states if state != APPROVED]


def _is_protected(parts: tuple[str, ...]) -> bool:
    return any(parts[: len(prefix)] == prefix for prefix in PROTECTED)


def decide(root: Path, target: str, new_text: str) -> Decision:
    """Decide whether a tool may write `new_text` to `target`."""
    parts = relative_parts(root, target)
    if not parts:
        return Decision("allow")
    shown = "/".join(parts)
    if _is_protected(parts):
        return Decision("ask", f"{shown} forma parte del control de specs: lo confirma el Tech Lead.")
    if parts[: len(SPECS_DIR)] == SPECS_DIR and _APPROVAL_WORD.search(new_text):
        return Decision("ask", f"{shown}: el cambio escribe «aprobada»; aprobar una spec es del Tech Lead.")
    block = block_for(parts)
    if block is None:
        return Decision("allow")
    pending = pending_specs(specs_dir(root), block)
    if not pending:
        return Decision("allow")
    reason = (
        f"Bloqueado: {shown} es código del bloque {block} y sus specs no están aprobadas: "
        f"{', '.join(pending)}. Spec antes que código (CLAUDE.md)."
    )
    return Decision("deny", reason)
