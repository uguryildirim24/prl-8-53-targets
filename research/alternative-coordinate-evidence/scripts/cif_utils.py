"""Minimal deterministic PDBx/mmCIF reader for this evidence package.

It supports quoted tokens, comments, semicolon text fields, scalar items and loops.
It intentionally does not attempt to implement dictionaries or save frames.
"""
from __future__ import annotations

import shlex
from pathlib import Path
from typing import Iterator


def tokens(path: Path) -> Iterator[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(";"):
            value = [line[1:]]
            i += 1
            while i < len(lines) and not lines[i].startswith(";"):
                value.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError(f"unterminated semicolon field in {path}")
            yield "\n".join(value)
            i += 1
            continue
        lexer = shlex.shlex(line, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        yield from lexer
        i += 1


def read_cif(path: Path) -> tuple[dict[str, str], dict[str, list[dict[str, str]]]]:
    stream = list(tokens(path))
    scalars: dict[str, str] = {}
    categories: dict[str, list[dict[str, str]]] = {}
    i = 0
    controls = {"loop_", "stop_", "global_"}
    while i < len(stream):
        token = stream[i]
        lower = token.lower()
        if lower == "loop_":
            i += 1
            tags: list[str] = []
            while i < len(stream) and stream[i].startswith("_"):
                tags.append(stream[i])
                i += 1
            if not tags:
                raise ValueError(f"loop without tags in {path}")
            values: list[str] = []
            while i < len(stream):
                candidate = stream[i]
                c_lower = candidate.lower()
                # A quoted loop value may itself begin with an underscore. Since
                # tokenization intentionally drops quote markers, only recognize a
                # new data name/control at a complete row boundary.
                at_row_boundary = len(values) % len(tags) == 0
                if at_row_boundary and (candidate.startswith("_") or c_lower in controls or c_lower.startswith(("data_", "save_"))):
                    break
                values.append(candidate)
                i += 1
            if len(values) % len(tags):
                raise ValueError(f"loop value count mismatch near {tags[0]} in {path}")
            category = tags[0].split(".", 1)[0]
            rows = categories.setdefault(category, [])
            for start in range(0, len(values), len(tags)):
                rows.append(dict(zip(tags, values[start:start + len(tags)])))
            continue
        if token.startswith("_"):
            if i + 1 >= len(stream):
                raise ValueError(f"missing scalar value for {token} in {path}")
            scalars[token] = stream[i + 1]
            i += 2
            continue
        i += 1
    return scalars, categories
