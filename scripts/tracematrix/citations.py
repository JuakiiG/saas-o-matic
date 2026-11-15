"""Citations of requirements in the tests: the grammar, and the tests of each kind of file."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass

# A citation: the spec and the id of a requirement or of a criterion, as ("SPEC-04", "E-16").
Citation = tuple[str, str]

# `SPEC-04/E-05 a E-11, E-40 y CA-05`: the ids that follow a spec, joined by a comma, by «y» or,
# for a range, by «a». An id that no spec precedes is prose, not a citation.
_ID = r"(?:E|CA)-\d+"
_JOINT = r"(?:, | y | a )"
ID_LIST = re.compile(rf"{_ID}(?:{_JOINT}{_ID})*")
_CITATION = re.compile(rf"(SPEC-\d+)/({ID_LIST.pattern})")
_STEP = re.compile(r"(, | y | a )")
_RANGE = " a "
# A test or a block of tests of Vitest or Playwright, at the start of its line.
_DECLARATION = re.compile(r"^(\s*)(describe|it|test)(\.describe|\.each)?\s*[(<]")


@dataclass(frozen=True)
class FoundTest:
    """A declared test and what it cites: in its own title or docstring, and through its blocks."""

    file: str
    line: int
    own: frozenset[Citation]
    inherited: frozenset[Citation]

    @property
    def cited(self) -> frozenset[Citation]:
        return self.own | self.inherited


def _between(first: str, last: str) -> list[str]:
    """Ids strictly between the two ends of a range; none if the ends are of different kinds."""
    kind, start = first.split("-")
    other, end = last.split("-")
    if kind != other:
        return []
    return [f"{kind}-{number:0{len(start)}d}" for number in range(int(start) + 1, int(end))]


def expand_ids(listing: str) -> list[str]:
    """Ids of a list such as `E-05 a E-07, E-40`, with its ranges written out."""
    parts = _STEP.split(listing)
    ids = [parts[0]]
    for joint, item in zip(parts[1::2], parts[2::2], strict=True):
        if joint == _RANGE:
            ids += _between(ids[-1], item)
        ids.append(item)
    return ids


def parse_citations(text: str) -> set[Citation]:
    """Citations written in a text."""
    return {(spec, item) for spec, listing in _CITATION.findall(text) for item in expand_ids(listing)}


def python_tests(label: str, text: str) -> list[FoundTest]:
    """Test functions of a pytest file, each with the citations of its docstring."""
    functions = [
        node
        for node in ast.walk(ast.parse(text))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
    ]
    return [
        FoundTest(label, node.lineno, frozenset(parse_citations(ast.get_docstring(node) or "")), frozenset())
        for node in sorted(functions, key=lambda node: node.lineno)
    ]


def _head(lines: list[str], start: int, indent: int, each: bool) -> str:
    """Lines that hold the title: from the call that takes it to the line that opens the body.

    The table of an `each` written over several lines comes before its title: it is skipped
    up to the line that closes it, at the indent of the declaration.
    """
    first = start
    if each and ")(" not in lines[start]:
        closing = " " * indent + "]"
        later = range(start + 1, len(lines))
        first = next((index for index in later if lines[index].startswith(closing)), start)
    head = []
    for line in lines[first:]:
        head.append(line)
        if line.rstrip().endswith(("{", ";")):
            break
    return "\n".join(head)


def typescript_tests(label: str, text: str) -> list[FoundTest]:
    """Tests declared in a Vitest or Playwright file formatted by Prettier.

    It relies on that format: what a block contains is indented deeper than the block, so a
    block ends where a declaration starts at its indent or less. A test written with `each`,
    or inside a loop, is one declaration, however many cases the runner makes of it.
    """
    lines = text.splitlines()
    blocks: list[tuple[int, frozenset[Citation]]] = []
    found = []
    for index, line in enumerate(lines):
        match = _DECLARATION.match(line)
        if match is None:
            continue
        indent = len(match.group(1))
        while blocks and blocks[-1][0] >= indent:
            blocks.pop()
        inherited = blocks[-1][1] if blocks else frozenset()
        own = frozenset(parse_citations(_head(lines, index, indent, match.group(3) == ".each")))
        if match.group(2) == "describe" or match.group(3) == ".describe":
            blocks.append((indent, inherited | own))
        else:
            found.append(FoundTest(label, index + 1, own, inherited))
    return found
