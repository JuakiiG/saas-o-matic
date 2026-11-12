# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PreToolUse hook: no application code before its spec is approved.

Protocol (Claude Code hooks reference, checked on 2026-11-12):
- stdin: one JSON object with `tool_name` and `tool_input`.
- allow: exit 0 and print nothing, so the normal permission flow continues.
- deny / ask: exit 0 and print a `hookSpecificOutput` object.
- exit 2 blocks the call and shows stderr to the model.
Any other exit code would let the call through, so every failure ends in 2.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from oracle import specgate  # imported after the path is set just above

EDIT_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")
PATH_FIELDS = ("file_path", "notebook_path")
TEXT_FIELDS = ("content", "new_string", "new_source")
BLOCK = 2


class HookInputError(ValueError):
    """The payload is not something this hook can judge."""


def _tool_call(payload_text: str) -> tuple[str, dict[str, object]]:
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        raise HookInputError(f"la entrada no es JSON válido ({error.msg})") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("tool_name"), str):
        raise HookInputError("la entrada no trae `tool_name`")
    tool_input = payload.get("tool_input")
    return payload["tool_name"], tool_input if isinstance(tool_input, dict) else {}


def _target(tool_input: dict[str, object]) -> str:
    for field in PATH_FIELDS:
        value = tool_input.get(field)
        if isinstance(value, str) and value:
            return value
    raise HookInputError("la herramienta no indica qué fichero va a escribir")


def _new_text(tool_input: dict[str, object]) -> str:
    return "\n".join(str(tool_input[field]) for field in TEXT_FIELDS if field in tool_input)


def _decision_json(decision: specgate.Decision) -> str:
    output = {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision.action,
        "permissionDecisionReason": decision.reason,
    }
    return json.dumps({"hookSpecificOutput": output}, ensure_ascii=False)


def evaluate(payload_text: str, root: Path) -> tuple[int, str, str]:
    """Return (exit code, stdout, stderr) for one hook invocation."""
    try:
        tool, tool_input = _tool_call(payload_text)
        if tool not in EDIT_TOOLS:
            return 0, "", ""
        decision = specgate.decide(root, _target(tool_input), _new_text(tool_input))
    except HookInputError as error:
        return BLOCK, "", f"Control de specs: escritura bloqueada porque {error}.\n"
    if decision.action == "allow":
        return 0, "", ""
    return 0, _decision_json(decision), ""


def main() -> int:
    try:
        payload_text = sys.stdin.buffer.read().decode("utf-8")
        code, stdout, stderr = evaluate(payload_text, SCRIPTS.parent)
    except Exception as error:  # fail closed: an unexpected error must block, not let the write through
        code, stdout, stderr = BLOCK, "", f"Control de specs: error interno, escritura bloqueada ({error!r}).\n"
    sys.stdout.buffer.write(stdout.encode("utf-8"))
    sys.stderr.buffer.write(stderr.encode("utf-8"))
    return code


if __name__ == "__main__":
    sys.exit(main())
