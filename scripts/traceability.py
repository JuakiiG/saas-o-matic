# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Prints the traceability matrix: which tests cite each EARS requirement of the specs.

Run from the repository root with `uv run scripts/traceability.py`. It only reads: the specs
of `ai-workspace/01-specs/` and the tests of `backend/tests/`, `frontend/src/` and
`frontend/e2e/`. Its output is the generated part of `ai-workspace/04-calidad/trazabilidad.md`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tracematrix import matrix  # imported after the path is set just above


def main() -> int:
    try:
        text = matrix.render(matrix.read_specs(ROOT), matrix.collect_tests(ROOT))
    except (OSError, UnicodeDecodeError, SyntaxError) as error:
        # A file that cannot be read or parsed leaves no matrix: a partial one would hide tests.
        sys.stderr.write(f"No se pudo generar la matriz: {error}\n")
        return 1
    sys.stdout.buffer.write(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
