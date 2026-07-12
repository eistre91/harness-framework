#!/usr/bin/env python3
"""Validate repository YAML files and Markdown frontmatter."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Literal

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Run 'uv sync' from the repository root.",
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


class GitDiscovery:
    """The result of attempting Git-aware source discovery."""

    __slots__ = ("state", "files", "reason")

    def __init__(
        self,
        state: Literal["absent", "success", "failed"],
        files: tuple[Path, ...] = (),
        reason: str | None = None,
    ) -> None:
        self.state = state
        self.files = files
        self.reason = reason


class SourceDiscoveryError(RuntimeError):
    """Git metadata exists but the authoritative source set was unavailable."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Git source discovery failed: {reason}")


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


def _root_has_git_metadata(root: Path) -> bool:
    """Return whether the selected root has local Git metadata."""

    metadata = root / ".git"
    try:
        metadata.lstat()
    except FileNotFoundError:
        return False
    except OSError:
        # An inaccessible .git path is still local metadata. Fail closed rather
        # than treating it as permission for an exported-tree walk.
        return True
    return True


def _source_candidate(path: Path, root: Path) -> Path | None:
    """Return a safe source candidate without following a file symlink."""

    if is_sensitive_path(path, root):
        return None

    if path.is_symlink():
        # Keep eligible symlinks in the source set so the validator can report a
        # deterministic rejection. Never ask a symlink whether it is a file.
        if path.suffix.lower() in YAML_SUFFIXES or path.suffix.lower() == ".md":
            return path
        return None

    if path.is_file():
        return path
    return None


def _git_source_files(root: Path) -> GitDiscovery:
    """Return the Git discovery state and, on success, its authoritative files."""

    if not _root_has_git_metadata(root):
        return GitDiscovery("absent")

    try:
        top_level_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return GitDiscovery(
            "failed",
            reason="git rev-parse --show-toplevel could not complete",
        )

    try:
        top_level = Path(top_level_result.stdout.strip()).resolve()
    except (OSError, RuntimeError):
        return GitDiscovery(
            "failed",
            reason="git rev-parse --show-toplevel returned an unusable top level",
        )
    if top_level != root:
        return GitDiscovery(
            "failed",
            reason="git rev-parse --show-toplevel resolved a different top level",
        )

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
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return GitDiscovery(
            "failed",
            reason="git ls-files source discovery could not complete",
        )

    files = []
    for name in result.stdout.split("\0"):
        if not name:
            continue

        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            continue

        path = root / relative
        candidate = _source_candidate(path, root)
        if candidate is not None:
            files.append(candidate)

    return GitDiscovery("success", tuple(_sort_paths(files, root)))


def _walk_exported_source(root: Path) -> list[Path]:
    """Walk a clean source export when Git metadata is unavailable.

    An exported source tree has no Git state with which to distinguish tracked
    from ignored files, so remaining files are treated as source after the
    safety filters below. Callers must provide a clean export without local
    ignored content; categorically sensitive paths remain excluded either way.
    """

    files = []

    def visit(directory: Path) -> None:
        try:
            with os.scandir(directory) as entries:
                entries = sorted(entries, key=lambda entry: entry.name)
                for entry in entries:
                    path = Path(entry.path)

                    # Check the directory entry itself before asking whether it
                    # is a directory or file. This keeps symlink targets out of
                    # exported-tree discovery as well as validation.
                    if entry.is_symlink():
                        candidate = _source_candidate(path, root)
                        if candidate is not None:
                            files.append(candidate)
                        continue

                    try:
                        is_directory = entry.is_dir(follow_symlinks=False)
                    except OSError:
                        continue
                    if is_directory:
                        if entry.name in EXCLUDED_DIRS or is_sensitive_path(
                            path, root
                        ):
                            continue
                        visit(path)
                        continue

                    try:
                        is_file = entry.is_file(follow_symlinks=False)
                    except OSError:
                        continue
                    if is_file:
                        candidate = _source_candidate(path, root)
                        if candidate is not None:
                            files.append(candidate)
        except OSError:
            return

    visit(root)

    return _sort_paths(files, root)


def repo_files(root: Path | None = None) -> Iterable[Path]:
    """Return the deterministic, hermetic source set for a repository."""

    root = _resolved_root(root)
    discovery = _git_source_files(root)
    # Keep compatibility with focused callers that stub the old list/None
    # result while the concrete implementation uses an explicit state model.
    if discovery is None:
        if _root_has_git_metadata(root):
            raise SourceDiscoveryError(
                "Git source discovery returned no state for a checkout"
            )
        return _walk_exported_source(root)
    if isinstance(discovery, (list, tuple)):
        return list(discovery)
    if discovery.state == "absent":
        return _walk_exported_source(root)
    if discovery.state == "failed":
        raise SourceDiscoveryError(
            discovery.reason or "Git source discovery returned no source set"
        )
    return list(discovery.files)


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
    if path.is_symlink():
        rel = path.relative_to(root)
        raise ValueError(f"{rel}: symbolic-link Markdown inputs are not supported")
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
        if path.is_symlink():
            errors.append(f"{rel}: symbolic-link YAML inputs are not supported")
            continue
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

        if path.is_symlink():
            count += 1
            errors.append(f"{rel}: symbolic-link Markdown inputs are not supported")
            continue

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
    try:
        yaml_count, yaml_errors = validate_yaml_files(root)
        frontmatter_count, frontmatter_errors = validate_frontmatter(root)
    except SourceDiscoveryError as exc:
        print("YAML validation failed:", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
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
