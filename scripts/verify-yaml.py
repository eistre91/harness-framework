#!/usr/bin/env python3
"""Validate repository YAML files and Markdown frontmatter."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Install it with: python3 -m pip install PyYAML",
        file=sys.stderr,
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "__pycache__", "node_modules"}
YAML_SUFFIXES = {".yml", ".yaml"}


class DuplicateKeyError(yaml.YAMLError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping_without_duplicates(loader: UniqueKeyLoader, node, deep=False):
    seen = {}

    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            first_mark = seen[key]
            raise DuplicateKeyError(
                f"duplicate key {key!r} first seen at line {first_mark.line + 1}, "
                f"column {first_mark.column + 1}"
            )
        seen[key] = key_node.start_mark

    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping_without_duplicates,
)


def repo_files() -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(
            dirname for dirname in dirnames if dirname not in EXCLUDED_DIRS
        )

        for filename in sorted(filenames):
            yield Path(dirpath) / filename


def parse_yaml(label: str, text: str) -> list[str]:
    errors = []

    try:
        list(yaml.load_all(text, Loader=UniqueKeyLoader))
    except yaml.YAMLError as exc:
        errors.append(f"{label}: {format_yaml_error(exc)}")

    return errors


def format_yaml_error(exc: yaml.YAMLError) -> str:
    mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
    if mark is not None:
        return f"line {mark.line + 1}, column {mark.column + 1}: {exc}"
    return str(exc)


def frontmatter_block(path: Path) -> tuple[str, int] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "---":
        return None

    for index, line in enumerate(lines[1:], start=2):
        if line == "---":
            block = "\n".join(lines[1 : index - 1])
            return block, index

    rel = path.relative_to(ROOT)
    raise ValueError(f"{rel}: frontmatter starts at line 1 but has no closing ---")


def validate_yaml_files() -> tuple[int, list[str]]:
    count = 0
    errors = []

    for path in repo_files():
        if path.suffix not in YAML_SUFFIXES:
            continue

        count += 1
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        errors.extend(parse_yaml(str(rel), text))

    return count, errors


def validate_frontmatter() -> tuple[int, list[str]]:
    count = 0
    errors = []

    for path in repo_files():
        if path.suffix != ".md":
            continue

        rel = path.relative_to(ROOT)

        try:
            block = frontmatter_block(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if block is None:
            continue

        count += 1
        frontmatter, _end_line = block
        errors.extend(parse_yaml(f"{rel} frontmatter", frontmatter))

    return count, errors


def main() -> int:
    yaml_count, yaml_errors = validate_yaml_files()
    frontmatter_count, frontmatter_errors = validate_frontmatter()
    errors = yaml_errors + frontmatter_errors

    if errors:
        print("YAML validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"YAML validation passed: {yaml_count} YAML files, "
        f"{frontmatter_count} Markdown frontmatter blocks."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
