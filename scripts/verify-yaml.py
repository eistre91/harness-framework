#!/usr/bin/env python3
"""Validate repository YAML files and Markdown frontmatter."""

from __future__ import annotations

import os
import re
import subprocess
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
SENSITIVE_DIR_NAMES = {"secrets"}
SENSITIVE_FILE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
YAML_SUFFIXES = {".yml", ".yaml"}
QUOTED_PARSER_TEXT = re.compile(
    r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\""
)


class UniqueKeyLoader(yaml.SafeLoader):
    pass


class DuplicateKeyError(yaml.YAMLError):
    """A duplicate mapping key with locations but without the key value."""

    def __init__(self, duplicate_mark, first_mark):
        self.problem = "duplicate key"
        self.problem_mark = duplicate_mark
        self.first_mark = first_mark
        super().__init__(self.problem)


def construct_mapping_without_duplicates(loader: UniqueKeyLoader, node, deep=False):
    seen = {}

    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise DuplicateKeyError(key_node.start_mark, seen[key])
        seen[key] = key_node.start_mark

    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping_without_duplicates,
)


def _resolved_root(root: Path | None) -> Path:
    return (ROOT if root is None else root).resolve()


def is_sensitive_path(path: Path, root: Path | None = None) -> bool:
    """Return whether a path is categorically unsafe to parse."""

    root = _resolved_root(root)
    relative = path.relative_to(root)
    if any(part in SENSITIVE_DIR_NAMES for part in relative.parts):
        return True

    filename = relative.name
    if filename == ".env" or filename.startswith(".env."):
        return True

    return path.suffix.lower() in SENSITIVE_FILE_SUFFIXES


def _sort_paths(paths: Iterable[Path], root: Path) -> list[Path]:
    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def _git_source_files(root: Path) -> list[Path] | None:
    """Return tracked and non-ignored untracked files, or None without Git."""

    try:
        top_level_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    top_level = Path(top_level_result.stdout.strip()).resolve()
    if top_level != root:
        return None

    try:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "--full-name",
                "-z",
            ],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    files = []
    for name in result.stdout.split("\0"):
        if not name:
            continue

        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            continue

        path = root / relative
        if path.is_file() and not is_sensitive_path(path, root):
            files.append(path)

    return _sort_paths(files, root)


def _walk_exported_source(root: Path) -> list[Path]:
    """Walk a clean source export when Git metadata is unavailable.

    An exported source tree has no Git state with which to distinguish tracked
    from ignored files, so remaining files are treated as source after the
    safety filters below. Callers must provide a clean export without local
    ignored content; categorically sensitive paths remain excluded either way.
    """

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            dirname
            for dirname in dirnames
            if dirname not in EXCLUDED_DIRS
            and not is_sensitive_path(Path(dirpath) / dirname, root)
        )

        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            if path.is_file() and not is_sensitive_path(path, root):
                files.append(path)

    return _sort_paths(files, root)


def repo_files(root: Path | None = None) -> Iterable[Path]:
    """Return the deterministic, hermetic source set for a repository."""

    root = _resolved_root(root)
    files = _git_source_files(root)
    if files is None:
        files = _walk_exported_source(root)
    return files


def parse_yaml(label: str, text: str) -> list[str]:
    errors = []

    try:
        list(yaml.load_all(text, Loader=UniqueKeyLoader))
    except yaml.YAMLError as exc:
        errors.append(f"{label}: {format_yaml_error(exc)}")

    return errors


def format_yaml_error(exc: yaml.YAMLError) -> str:
    mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
    location = ""
    if mark is not None:
        location = f"line {mark.line + 1}, column {mark.column + 1}: "

    if isinstance(exc, DuplicateKeyError):
        first_mark = exc.first_mark
        first_location = (
            f"first occurrence at line {first_mark.line + 1}, "
            f"column {first_mark.column + 1}"
        )
        return f"{location}duplicate key ({first_location})"

    context = _redact_parser_text(getattr(exc, "context", None))
    problem = _redact_parser_text(getattr(exc, "problem", None))
    details = "; ".join(part for part in (context, problem) if part)
    return f"{location}{details or 'invalid YAML'}"


def _redact_parser_text(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None

    single_line = " ".join(value.split())
    return QUOTED_PARSER_TEXT.sub("<redacted>", single_line)


def frontmatter_block(path: Path, root: Path | None = None) -> tuple[str, int] | None:
    root = _resolved_root(root)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "---":
        return None

    for index, line in enumerate(lines[1:], start=2):
        if line == "---":
            block = "\n".join(lines[1 : index - 1])
            return block, index

    rel = path.relative_to(root)
    raise ValueError(f"{rel}: frontmatter starts at line 1 but has no closing ---")


def validate_yaml_files(root: Path | None = None) -> tuple[int, list[str]]:
    root = _resolved_root(root)
    count = 0
    errors = []

    for path in repo_files(root):
        if path.suffix.lower() not in YAML_SUFFIXES:
            continue

        count += 1
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        errors.extend(parse_yaml(str(rel), text))

    return count, errors


def validate_frontmatter(root: Path | None = None) -> tuple[int, list[str]]:
    root = _resolved_root(root)
    count = 0
    errors = []

    for path in repo_files(root):
        if path.suffix.lower() != ".md":
            continue

        rel = path.relative_to(root)

        try:
            block = frontmatter_block(path, root)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if block is None:
            continue

        count += 1
        frontmatter, _end_line = block
        errors.extend(parse_yaml(f"{rel} frontmatter", frontmatter))

    return count, errors


def main(root: Path | None = None) -> int:
    root = _resolved_root(root)
    yaml_count, yaml_errors = validate_yaml_files(root)
    frontmatter_count, frontmatter_errors = validate_frontmatter(root)
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
