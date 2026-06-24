#!/usr/bin/env python3
"""Validate local repository path references in framework text files."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]

ROOT_FILES = ("README.md", "TODO.md", "AGENTS.md", "CLAUDE.md")
SCAN_GLOBS = (
    "docs/**/*.md",
    "templates/**/*.md",
    "skills/**/*.md",
    "manifests/**/*.yml",
)
EXCLUDED_PARTS = {".git", "__pycache__", "node_modules"}
EXCLUDED_PREFIXES = (Path("docs") / "ignored",)
LOCAL_SCHEMES = {"", "file"}

INTENTIONAL_TARGET_PREFIXES = (
    ".agent/work/",
    ".agents/skills/",
    ".claude/",
    ".claude/skills/",
    ".harness-bootstrap/",
    "docs/harness/",
    "docs/routing/",
    "docs/project/",
    "docs/work/",
    "skills/harness-creator/",
)
INTENTIONAL_TARGET_FILES = {
    ".gitignore",
    ".harness.yml",
    "CONTEXT.md",
    "SPEC-MAP.md",
    "docs/install/level-1.md",
    "docs/routing",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
PATH_RE = re.compile(
    r"(?<![\w./-])("
    r"(?:docs|manifests|templates|skills|scripts|tests|adapters)/"
    r"[A-Za-z0-9._/<>{}-]*[A-Za-z0-9_<>{}/-]"
    r"|(?:AGENTS|CLAUDE|README|TODO|REFERENCES|CONTEXT|SPEC-MAP)\.md"
    r"|LICENSE"
    r"|\.gitignore"
    r"|\.harness\.yml"
    r"|\.agents/[A-Za-z0-9._/<>{}-]*[A-Za-z0-9_<>{}/-]"
    r"|\.agent/[A-Za-z0-9._/<>{}-]*[A-Za-z0-9_<>{}/-]"
    r"|\.claude/[A-Za-z0-9._/<>{}-]*[A-Za-z0-9_<>{}/-]"
    r"|\.harness-bootstrap/[A-Za-z0-9._/<>{}-]*[A-Za-z0-9_<>{}/-]"
    r")"
)


def scan_files(root: Path) -> list[Path]:
    paths: set[Path] = set()

    for filename in ROOT_FILES:
        path = root / filename
        if path.exists():
            paths.add(path)

    for pattern in SCAN_GLOBS:
        for path in root.glob(pattern):
            if should_scan(path, root):
                paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def should_scan(path: Path, root: Path) -> bool:
    if not path.is_file():
        return False

    rel = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    return not any(is_relative_to(rel, prefix) for prefix in EXCLUDED_PREFIXES)


def is_relative_to(path: Path, prefix: Path) -> bool:
    try:
        path.relative_to(prefix)
    except ValueError:
        return False
    return True


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.splitlines()
    stripped = []
    in_fence = False

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            stripped.append("")
            continue
        stripped.append("" if in_fence else line)

    return "\n".join(stripped)


def strip_inline_code(line: str) -> str:
    return CODE_SPAN_RE.sub(lambda match: " " * len(match.group(0)), line)


def code_spans(line: str) -> list[str]:
    return [match.group(1) for match in CODE_SPAN_RE.finditer(line)]


def clean_reference(value: str) -> str:
    value = unquote(value.strip())
    value = value.strip("'\"")
    return value.rstrip(".,;:)")


def normalize_reference(value: str) -> str | None:
    value = clean_reference(value)
    if not value:
        return None

    split = urlsplit(value)
    if split.scheme and split.scheme not in LOCAL_SCHEMES:
        return None
    if split.netloc:
        return None

    path = split.path
    if not path or path.startswith("#"):
        return None
    if path.startswith("/tmp") or path.startswith("/"):
        return None
    if "<" in path or ">" in path:
        return None

    return path


def should_ignore_reference(path: str) -> bool:
    if path in INTENTIONAL_TARGET_FILES:
        return True
    return any(
        path == prefix[:-1] or path.startswith(prefix)
        for prefix in INTENTIONAL_TARGET_PREFIXES
    )


def resolve_markdown_reference(root: Path, source: Path, path: str) -> Path:
    candidate = Path(path)
    if candidate.parts and candidate.parts[0] in {
        "adapters",
        "docs",
        "manifests",
        "scripts",
        "skills",
        "templates",
        "tests",
    }:
        return root / candidate
    return (source.parent / candidate).resolve()


def path_is_inside_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return False
    return True


def markdown_reference_exists(root: Path, source: Path, path: str) -> bool:
    resolved = resolve_markdown_reference(root, source, path)
    return path_is_inside_root(root, resolved) and resolved.exists()


def plain_reference_exists(root: Path, source: Path, path: str) -> bool:
    root_candidate = root / path
    source_candidate = source.parent / path
    return (
        path_is_inside_root(root, root_candidate)
        and root_candidate.exists()
        or path_is_inside_root(root, source_candidate)
        and source_candidate.exists()
    )


def is_plain_reference_candidate(path: str) -> bool:
    if path in {"AGENTS.md", "CLAUDE.md", "README.md", "TODO.md", "LICENSE"}:
        return True
    if path.endswith("/"):
        return True
    return "." in Path(path).name


def validate_reference(
    root: Path,
    source: Path,
    line_number: int,
    reference: str,
    *,
    markdown_link: bool,
) -> list[str]:
    path = normalize_reference(reference)
    if path is None or should_ignore_reference(path):
        return []

    exists = (
        markdown_reference_exists(root, source, path)
        if markdown_link
        else plain_reference_exists(root, source, path)
    )
    if exists:
        return []

    rel_source = source.relative_to(root)
    return [f"{rel_source}:{line_number}: referenced path does not exist: {path}"]


def line_references(line: str) -> list[tuple[str, bool]]:
    references = []

    without_code = strip_inline_code(line)
    for match in MARKDOWN_LINK_RE.finditer(without_code):
        references.append((match.group(1), True))

    plain_line = MARKDOWN_LINK_RE.sub(" ", without_code)
    for match in PATH_RE.finditer(plain_line):
        reference = match.group(1)
        if is_plain_reference_candidate(reference):
            references.append((reference, False))

    for span in code_spans(line):
        for match in PATH_RE.finditer(span):
            references.append((match.group(1), False))

    return references


def validate_file(root: Path, path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = strip_fenced_code_blocks(text)
    errors = []
    seen: set[tuple[int, str, bool]] = set()

    for line_number, line in enumerate(text.splitlines(), start=1):
        for reference, markdown_link in line_references(line):
            key = (line_number, reference, markdown_link)
            if key in seen:
                continue
            seen.add(key)
            errors.extend(
                validate_reference(
                    root,
                    path,
                    line_number,
                    reference,
                    markdown_link=markdown_link,
                )
            )

    return errors


def validate_doc_refs(root: Path) -> tuple[int, list[str]]:
    paths = scan_files(root)
    errors = []

    for path in paths:
        errors.extend(validate_file(root, path))

    return len(paths), errors


def main() -> int:
    count, errors = validate_doc_refs(ROOT)

    if errors:
        print("Doc reference validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Doc reference validation passed: {count} text files.")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    sys.exit(main())
