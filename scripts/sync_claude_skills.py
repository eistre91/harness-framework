#!/usr/bin/env python3
"""Synchronize explicitly managed Claude skill mirrors."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only without PyYAML.
    yaml = None


CODEX_METADATA_PATH = Path("agents") / "openai.yaml"
CLAUDE_DISABLE_MODEL_INVOCATION_KEY = "disable-model-invocation"
CLAUDE_DISABLE_MODEL_INVOCATION_PATTERN = re.compile(
    rf"^{re.escape(CLAUDE_DISABLE_MODEL_INVOCATION_KEY)}\s*:"
)

# This is the public ownership contract. The same marker is written to a
# generated Claude mirror as provenance, but the canonical .agents marker is
# authoritative for current ownership.
SYNC_METADATA_KEY = "agent-harness-framework/claude-sync"
SYNC_METADATA_VALUE = "agents-to-claude"
PORTABLE_FRONTMATTER_FIELDS = (
    "name",
    "description",
    "license",
    "compatibility",
)

TOP_LEVEL_FIELD_PATTERN = re.compile(
    r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$"
)
SYNC_METADATA_KEY_LINE_PATTERN = re.compile(
    rf"^(?P<indent>[ \t]+){re.escape(SYNC_METADATA_KEY)}\s*:"
)
SYNC_METADATA_LINE_PATTERN = re.compile(
    rf"^(?P<indent>[ \t]+){re.escape(SYNC_METADATA_KEY)}\s*:\s*"
    rf"(?P<value>{re.escape(SYNC_METADATA_VALUE)}|"
    rf"'{re.escape(SYNC_METADATA_VALUE)}'|"
    rf'"{re.escape(SYNC_METADATA_VALUE)}")'
    r"(?:[ \t]+#.*)?[ \t]*$"
)


class SyncError(RuntimeError):
    """Base class for actionable synchronization failures."""


class SyncValidationError(SyncError):
    """A plan contains an issue and therefore cannot be applied."""

    def __init__(self, root: Path, issues: list["PlanIssue"]) -> None:
        self.root = root
        self.issues = issues
        super().__init__(self._message())

    def _message(self) -> str:
        lines = ["Validation failed; no files were changed."]
        for issue in self.issues:
            lines.extend(issue.render(self.root))
        return "\n".join(lines)


class SyncWriteError(SyncError):
    """A validated plan could not be committed safely."""


@dataclass(frozen=True)
class FrontmatterBlock:
    key: str
    start: int
    end: int


@dataclass(frozen=True)
class FrontmatterDocument:
    lines: tuple[str, ...]
    blocks: tuple[FrontmatterBlock, ...]

    def block(self, key: str) -> FrontmatterBlock | None:
        for block in self.blocks:
            if block.key == key:
                return block
        return None


@dataclass(frozen=True)
class PlanIssue:
    category: str
    path: Path
    detail: str
    action: str

    def render(self, root: Path) -> list[str]:
        relative = self.path.relative_to(root).as_posix()
        return [
            f"- {self.category}: {relative}: {self.detail}",
            f"  Human decision required: {self.action}",
        ]


@dataclass(frozen=True)
class ManagedSkill:
    name: str
    agent_path: Path
    agent_text: str
    agent_frontmatter: str


@dataclass(frozen=True)
class PlannedWrite:
    path: Path
    content: bytes
    before: bytes | None
    mode: int | None
    action: str
    kind: str


@dataclass(frozen=True)
class SyncPlan:
    root: Path
    writes: tuple[PlannedWrite, ...]
    issues: tuple[PlanIssue, ...]

    @property
    def changed_paths(self) -> list[Path]:
        return [write.path for write in self.writes]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return leading YAML frontmatter and markdown body."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            frontmatter = "".join(lines[: index + 1]).rstrip("\r\n")
            body = "".join(lines[index + 1 :]).lstrip("\r\n")
            return frontmatter, body

    raise ValueError("skill frontmatter is missing a closing '---' delimiter")


def _frontmatter_document(frontmatter: str) -> FrontmatterDocument:
    lines = tuple(frontmatter.splitlines())
    if len(lines) < 2 or lines[0].strip() != "---" or lines[-1].strip() != "---":
        raise ValueError("skill frontmatter is malformed")

    blocks: list[FrontmatterBlock] = []
    current_key: str | None = None
    current_start: int | None = None

    for index, line in enumerate(lines[1:-1], start=1):
        match = TOP_LEVEL_FIELD_PATTERN.match(line) if not line.startswith((" ", "\t")) else None
        if match is not None:
            if current_key is not None and current_start is not None:
                blocks.append(FrontmatterBlock(current_key, current_start, index))
            current_key = match.group(1)
            current_start = index
            continue

        if current_key is None and line.strip() and not line.lstrip().startswith("#"):
            raise ValueError("invalid frontmatter line")

    if current_key is not None and current_start is not None:
        blocks.append(FrontmatterBlock(current_key, current_start, len(lines) - 1))

    keys = [block.key for block in blocks]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ValueError("duplicate frontmatter keys")

    return FrontmatterDocument(lines=lines, blocks=tuple(blocks))


def _parse_fallback_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _fallback_mapping(document: FrontmatterDocument) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for block in document.blocks:
        first_line = document.lines[block.start]
        match = TOP_LEVEL_FIELD_PATTERN.match(first_line)
        if match is None:  # pragma: no cover - guarded by document parsing.
            continue

        inline_value = (match.group(2) or "").strip()
        if block.key == "metadata":
            if inline_value:
                raise ValueError("metadata must be a YAML mapping")
            metadata: dict[str, Any] = {}
            for line in document.lines[block.start + 1 : block.end]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                nested = re.match(r"^[ \t]+([^:#][^:]*):[ \t]*(.*)$", line)
                if nested is None:
                    raise ValueError("metadata must be a YAML mapping")
                metadata[nested.group(1).strip()] = _parse_fallback_scalar(
                    nested.group(2)
                )
            mapping[block.key] = metadata
        elif inline_value in {"|", "|-", "|+", ">", ">-", ">+"}:
            mapping[block.key] = "\n".join(
                line.strip() for line in document.lines[block.start + 1 : block.end]
            )
        else:
            mapping[block.key] = _parse_fallback_scalar(inline_value)
    return mapping


def _frontmatter_mapping(document: FrontmatterDocument) -> dict[str, Any]:
    body = "\n".join(document.lines[1:-1])
    if yaml is None:
        return _fallback_mapping(document)

    try:
        loaded = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        raise ValueError("invalid YAML frontmatter") from exc

    mapping = {} if loaded is None else loaded

    if not isinstance(mapping, dict):
        raise ValueError("skill frontmatter must be a YAML mapping")
    return mapping


def _metadata_marker_from_document(
    document: FrontmatterDocument,
) -> tuple[Any, bool]:
    metadata_block = document.block("metadata")
    if metadata_block is None:
        return None, False

    try:
        mapping = _frontmatter_mapping(document)
    except ValueError:
        return _direct_malformed_marker_from_block(document, metadata_block)

    if isinstance(mapping, dict):
        metadata = mapping.get("metadata")
        if isinstance(metadata, dict) and SYNC_METADATA_KEY in metadata:
            return metadata[SYNC_METADATA_KEY], True

    return None, False


def _direct_malformed_marker_from_block(
    document: FrontmatterDocument,
    metadata_block: FrontmatterBlock,
) -> tuple[Any, bool]:
    """Find exact marker evidence in a malformed metadata mapping block."""

    metadata_line = document.lines[metadata_block.start]
    metadata_match = TOP_LEVEL_FIELD_PATTERN.match(metadata_line)
    if metadata_match is None:
        return None, False

    inline_value = (metadata_match.group(2) or "").strip()
    if inline_value and not inline_value.startswith("#"):
        return None, False

    child_lines = document.lines[metadata_block.start + 1 : metadata_block.end]
    indents: list[int] = []
    for line in child_lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        if indent <= len(metadata_line) - len(metadata_line.lstrip(" \t")):
            return None, False
        indents.append(indent)

    if not indents:
        return None, False

    child_indent = min(indents)
    for line in child_lines:
        if line.strip().startswith("-"):
            return None, False
        match = SYNC_METADATA_LINE_PATTERN.match(line)
        if match is not None and len(match.group("indent")) == child_indent:
            return SYNC_METADATA_VALUE, True

    return None, False


def _frontmatter_region(text: str) -> str | None:
    """Return only the closed frontmatter region, if one is present."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[: index + 1])
    return None


def _malformed_marker_from_text(text: str) -> tuple[Any, bool]:
    region = _frontmatter_region(text)
    if region is None:
        return None, False

    lines = tuple(region.splitlines())
    top_level_fields: list[tuple[int, str]] = []
    for index, line in enumerate(lines[1:-1], start=1):
        match = TOP_LEVEL_FIELD_PATTERN.match(line) if not line.startswith((" ", "\t")) else None
        if match is not None:
            top_level_fields.append((index, match.group(1)))

    for field_index, (metadata_start, field_name) in enumerate(top_level_fields):
        if field_name != "metadata":
            continue
        metadata_end = (
            top_level_fields[field_index + 1][0]
            if field_index + 1 < len(top_level_fields)
            else len(lines) - 1
        )
        document = FrontmatterDocument(
            lines=lines,
            blocks=(FrontmatterBlock("metadata", metadata_start, metadata_end),),
        )
        marker = _direct_malformed_marker_from_block(
            document,
            document.blocks[0],
        )
        if marker[1]:
            return marker

    return None, False


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, str):
        if re.fullmatch(r"[A-Za-z0-9._/-]+", value):
            return value
        return json.dumps(value, ensure_ascii=False)
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if yaml is not None:
        rendered = yaml.safe_dump(
            value,
            allow_unicode=True,
            default_flow_style=True,
            sort_keys=False,
        ).strip()
        return rendered.removesuffix("...")
    return str(value)


def _marker_block() -> list[str]:
    return [
        "metadata:",
        f"  {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}",
    ]


def _metadata_block_with_marker(
    document: FrontmatterDocument,
) -> list[str]:
    block = document.block("metadata")
    if block is None:
        return _marker_block()

    mapping = _frontmatter_mapping(document)
    metadata = mapping.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Claude metadata is not a YAML mapping")

    lines = list(document.lines[block.start : block.end])
    first_match = TOP_LEVEL_FIELD_PATTERN.match(lines[0])
    inline_value = (first_match.group(2) or "").strip() if first_match else ""

    if inline_value and not inline_value.startswith("#"):
        metadata = dict(metadata)
        metadata[SYNC_METADATA_KEY] = SYNC_METADATA_VALUE
        result = ["metadata:"]
        for key, value in metadata.items():
            result.append(f"  {key}: {_yaml_scalar(value)}")
        return result

    for index, line in enumerate(lines):
        match = SYNC_METADATA_KEY_LINE_PATTERN.match(line)
        if match is not None:
            indent = line[: len(line) - len(line.lstrip())]
            lines[index] = f"{indent}{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}"
            return lines

    insert_at = len(lines)
    while insert_at > 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines.insert(insert_at, f"  {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}")
    return lines


def _replace_frontmatter_blocks(
    frontmatter: str,
    replacements: dict[str, list[str] | None],
    additions: list[list[str]],
) -> str:
    document = _frontmatter_document(frontmatter)
    lines = list(document.lines)

    for block in reversed(document.blocks):
        if block.key not in replacements:
            continue
        replacement = replacements[block.key]
        lines[block.start : block.end] = [] if replacement is None else replacement

    if additions:
        insert_at = len(lines) - 1
        for addition in additions:
            lines[insert_at:insert_at] = addition
            insert_at += len(addition)

    return "\n".join(lines)


def _source_blocks(
    agent_frontmatter: str,
) -> tuple[FrontmatterDocument, dict[str, list[str]]]:
    document = _frontmatter_document(agent_frontmatter)
    portable = {}
    for field in PORTABLE_FRONTMATTER_FIELDS:
        block = document.block(field)
        if block is not None:
            portable[field] = list(document.lines[block.start : block.end])
    return document, portable


def _merge_claude_frontmatter(
    claude_frontmatter: str,
    *,
    agent_frontmatter: str | None = None,
    codex_allow_implicit_invocation: bool | None = None,
    include_sync_marker: bool = False,
) -> str:
    document = _frontmatter_document(claude_frontmatter)
    replacements: dict[str, list[str] | None] = {}
    additions: list[list[str]] = []

    if agent_frontmatter is not None:
        _, source_blocks = _source_blocks(agent_frontmatter)
        for field in PORTABLE_FRONTMATTER_FIELDS:
            if field in source_blocks:
                if document.block(field) is None:
                    additions.append(source_blocks[field])
                else:
                    replacements[field] = source_blocks[field]
            elif document.block(field) is not None:
                replacements[field] = None

    if include_sync_marker:
        if document.block("metadata") is None:
            additions.append(_marker_block())
        else:
            replacements["metadata"] = _metadata_block_with_marker(document)

    if codex_allow_implicit_invocation is False:
        mapped_policy = [
            f"{CLAUDE_DISABLE_MODEL_INVOCATION_KEY}: true"
        ]
        if document.block(CLAUDE_DISABLE_MODEL_INVOCATION_KEY) is None:
            additions.append(mapped_policy)
        else:
            replacements[CLAUDE_DISABLE_MODEL_INVOCATION_KEY] = mapped_policy
    elif codex_allow_implicit_invocation is True:
        replacements[CLAUDE_DISABLE_MODEL_INVOCATION_KEY] = None

    return _replace_frontmatter_blocks(claude_frontmatter, replacements, additions)


def expected_claude_frontmatter(
    frontmatter: str,
    *,
    codex_allow_implicit_invocation: bool | None,
) -> str:
    """Return Claude frontmatter with an explicit invocation policy applied."""
    expected = _merge_claude_frontmatter(
        frontmatter,
        codex_allow_implicit_invocation=codex_allow_implicit_invocation,
    )
    _validate_generated_frontmatter(expected)
    return expected


def _validate_generated_frontmatter(
    frontmatter: str,
    *,
    require_sync_marker: bool = False,
) -> None:
    """Ensure planned Claude frontmatter is valid before it reaches a write."""

    document = _frontmatter_document(frontmatter)
    mapping = _frontmatter_mapping(document)
    if not require_sync_marker:
        return

    metadata = mapping.get("metadata")
    if not isinstance(metadata, dict) or metadata.get(SYNC_METADATA_KEY) != SYNC_METADATA_VALUE:
        raise ValueError("generated Claude frontmatter is missing the sync marker")


def expected_claude_skill_text(
    agent_text: str,
    claude_text: str,
    *,
    codex_allow_implicit_invocation: bool | None = None,
    include_sync_marker: bool = False,
) -> str:
    """Merge portable source fields and body into an existing Claude mirror."""
    agent_frontmatter, agent_body = split_frontmatter(agent_text)
    claude_frontmatter, _ = split_frontmatter(claude_text)

    if not agent_frontmatter:
        raise ValueError("agent skill is missing YAML frontmatter")
    if not claude_frontmatter:
        raise ValueError("Claude skill is missing YAML frontmatter")

    _frontmatter_mapping(_frontmatter_document(agent_frontmatter))
    _frontmatter_mapping(_frontmatter_document(claude_frontmatter))
    expected_frontmatter = _merge_claude_frontmatter(
        claude_frontmatter,
        agent_frontmatter=agent_frontmatter,
        codex_allow_implicit_invocation=codex_allow_implicit_invocation,
        include_sync_marker=include_sync_marker,
    )
    _validate_generated_frontmatter(
        expected_frontmatter,
        require_sync_marker=include_sync_marker,
    )
    return f"{expected_frontmatter}\n\n{agent_body}"


def expected_new_claude_skill_text(
    agent_text: str,
    *,
    codex_allow_implicit_invocation: bool | None = None,
    include_sync_marker: bool = False,
) -> str:
    """Build a new Claude mirror from portable source fields."""
    agent_frontmatter, agent_body = split_frontmatter(agent_text)
    if not agent_frontmatter:
        raise ValueError("agent skill is missing YAML frontmatter")

    document, source_blocks = _source_blocks(agent_frontmatter)
    _frontmatter_mapping(document)

    lines = ["---"]
    for field in PORTABLE_FRONTMATTER_FIELDS:
        if field in source_blocks:
            lines.extend(source_blocks[field])

    if include_sync_marker:
        lines.extend(_marker_block())

    if codex_allow_implicit_invocation is False:
        lines.append(f"{CLAUDE_DISABLE_MODEL_INVOCATION_KEY}: true")

    lines.append("---")
    frontmatter = "\n".join(lines)
    _validate_generated_frontmatter(
        frontmatter,
        require_sync_marker=include_sync_marker,
    )
    return f"{frontmatter}\n\n{agent_body}"


def _codex_allow_implicit_invocation(skill_dir: Path) -> bool | None:
    """Return Codex implicit invocation policy from agents/openai.yaml."""
    metadata_path = skill_dir / CODEX_METADATA_PATH
    if not metadata_path.exists():
        return None

    if yaml is None:
        raise ValueError("PyYAML is required to parse agents/openai.yaml")

    try:
        loaded = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError("unable to read Codex metadata") from exc
    except yaml.YAMLError as exc:
        raise ValueError("invalid Codex metadata YAML") from exc
    metadata = {} if loaded is None else loaded
    if not isinstance(metadata, dict):
        raise ValueError("Codex skill metadata must be a mapping")

    if "policy" not in metadata:
        return None

    policy = metadata["policy"]
    if not isinstance(policy, dict):
        raise ValueError("policy must be a mapping")

    if "allow_implicit_invocation" not in policy:
        return None

    allow_implicit_invocation = policy["allow_implicit_invocation"]
    if not isinstance(allow_implicit_invocation, bool):
        raise ValueError("policy.allow_implicit_invocation must be a boolean")

    return allow_implicit_invocation


def _support_file_paths(
    skill_dir: Path,
    *,
    include_codex_metadata: bool,
) -> dict[Path, Path]:
    """Return role-appropriate non-entrypoint files by relative path."""
    if not skill_dir.exists() or not skill_dir.is_dir():
        return {}

    paths: dict[Path, Path] = {}
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(skill_dir)
        if relative_path == Path("SKILL.md"):
            continue
        if not include_codex_metadata and relative_path == CODEX_METADATA_PATH:
            continue
        paths[relative_path] = path

    return {relative_path: paths[relative_path] for relative_path in sorted(paths)}


def support_file_paths(skill_dir: Path) -> dict[Path, Path]:
    """Backward-compatible public wrapper for support-file discovery."""
    return _support_file_paths(skill_dir, include_codex_metadata=False)


def _canonical_support_file_paths(skill_dir: Path) -> dict[Path, Path]:
    return _support_file_paths(skill_dir, include_codex_metadata=False)


def _mirror_support_file_paths(skill_dir: Path) -> dict[Path, Path]:
    return _support_file_paths(skill_dir, include_codex_metadata=True)


def _sync_marker_from_text(text: str) -> tuple[Any, bool]:
    try:
        frontmatter, _ = split_frontmatter(text)
        if not frontmatter:
            return None, False
        document = _frontmatter_document(frontmatter)
        return _metadata_marker_from_document(document)
    except ValueError:
        return _malformed_marker_from_text(text)


def _source_has_managed_marker(text: str) -> bool:
    value, _ = _sync_marker_from_text(text)
    return value == SYNC_METADATA_VALUE


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _issue(
    category: str,
    path: Path,
    detail: str,
    action: str,
) -> PlanIssue:
    return PlanIssue(category=category, path=path, detail=detail, action=action)


def _discover_managed_sources(
    root: Path,
) -> tuple[list[ManagedSkill], set[str], list[PlanIssue]]:
    agent_root = root / ".agents" / "skills"
    if not agent_root.exists():
        return [], set(), []
    if not agent_root.is_dir():
        return [], set(), [
            _issue(
                "invalid canonical skills root",
                agent_root,
                "expected a directory",
                "ask the human operator to restore the .agents/skills directory.",
            )
        ]

    sources: list[ManagedSkill] = []
    candidate_names: set[str] = set()
    issues: list[PlanIssue] = []

    paths = sorted(agent_root.glob("*/SKILL.md"), key=lambda path: path.as_posix())
    for agent_path in paths:
        try:
            agent_text = agent_path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(
                _issue(
                    "unreadable canonical skill",
                    agent_path,
                    str(exc),
                    "ask the human operator to make the canonical skill readable.",
                )
            )
            continue

        if not _source_has_managed_marker(agent_text):
            continue

        skill_name = agent_path.parent.name
        candidate_names.add(skill_name)
        try:
            agent_frontmatter, _ = split_frontmatter(agent_text)
            if not agent_frontmatter:
                raise ValueError("agent skill is missing YAML frontmatter")
            document = _frontmatter_document(agent_frontmatter)
            mapping = _frontmatter_mapping(document)
            name = mapping.get("name")
            if not isinstance(name, str):
                raise ValueError("canonical skill must declare a string name")
            if name != skill_name:
                raise ValueError(
                    f"canonical name {name!r} does not match directory {skill_name!r}"
                )
        except (OSError, ValueError) as exc:
            issues.append(
                _issue(
                    "invalid managed canonical skill",
                    agent_path,
                    str(exc),
                    "ask the human operator to repair the canonical skill before syncing.",
                )
            )
            continue

        sources.append(
            ManagedSkill(
                name=skill_name,
                agent_path=agent_path,
                agent_text=agent_text,
                agent_frontmatter=agent_frontmatter,
            )
        )

    return sources, candidate_names, issues


def _claude_skill_dirs(root: Path) -> list[Path]:
    claude_root = root / ".claude" / "skills"
    if not claude_root.exists() or not claude_root.is_dir():
        return []
    return sorted(
        (path for path in claude_root.iterdir() if path.is_dir()),
        key=lambda path: path.as_posix(),
    )


def _add_planned_write(
    root: Path,
    path: Path,
    content: bytes,
    *,
    kind: str,
    writes: list[PlannedWrite],
    issues: list[PlanIssue],
) -> None:
    current: bytes | None
    mode: int | None
    if path.exists():
        if not path.is_file():
            issues.append(
                _issue(
                    "destination is not a file",
                    path,
                    "the planned mirror path is occupied by a directory or special file",
                    "ask the human operator to resolve the destination conflict.",
                )
            )
            return
        try:
            current = path.read_bytes()
            mode = stat.S_IMODE(path.stat().st_mode)
        except OSError as exc:
            issues.append(
                _issue(
                    "unreadable destination",
                    path,
                    str(exc),
                    "ask the human operator to make the destination readable.",
                )
            )
            return
    else:
        current = None
        mode = None

    parent = path.parent
    while parent != root and parent != parent.parent:
        if parent.exists() and not parent.is_dir():
            issues.append(
                _issue(
                    "destination parent is not a directory",
                    parent,
                    "a parent path blocks the planned mirror",
                    "ask the human operator to resolve the destination conflict.",
                )
            )
            return
        parent = parent.parent

    if current == content:
        return

    writes.append(
        PlannedWrite(
            path=path,
            content=content,
            before=current,
            mode=mode,
            action="create" if current is None else "update",
            kind=kind,
        )
    )


def _process_managed_skill(
    root: Path,
    skill: ManagedSkill,
    *,
    writes: list[PlannedWrite],
    issues: list[PlanIssue],
) -> None:
    claude_dir = root / ".claude" / "skills" / skill.name
    claude_path = claude_dir / "SKILL.md"

    if claude_dir.exists() and not claude_dir.is_dir():
        issues.append(
            _issue(
                "managed mirror directory conflict",
                claude_dir,
                "the Claude skill directory path is occupied by a file",
                "ask the human operator to resolve the destination conflict.",
            )
        )
        return

    claude_text: str | None = None
    expected_skill_text: str | None = None
    if claude_path.exists():
        if not claude_path.is_file():
            issues.append(
                _issue(
                    "invalid managed Claude mirror",
                    claude_path,
                    "the mirror entrypoint is not a regular file",
                    "ask the human operator to repair the Claude mirror.",
                )
            )
        else:
            try:
                claude_text = claude_path.read_text(encoding="utf-8")
                allow_implicit_invocation = _codex_allow_implicit_invocation(
                    skill.agent_path.parent
                )
                expected_skill_text = expected_claude_skill_text(
                    skill.agent_text,
                    claude_text,
                    codex_allow_implicit_invocation=allow_implicit_invocation,
                    include_sync_marker=True,
                )
            except (OSError, ValueError) as exc:
                issues.append(
                    _issue(
                        "invalid managed Claude mirror",
                        claude_path,
                        str(exc),
                        "ask the human operator to repair or consciously recreate the Claude frontmatter.",
                    )
                )
    else:
        try:
            allow_implicit_invocation = _codex_allow_implicit_invocation(
                skill.agent_path.parent
            )
            expected_skill_text = expected_new_claude_skill_text(
                skill.agent_text,
                codex_allow_implicit_invocation=allow_implicit_invocation,
                include_sync_marker=True,
            )
        except (OSError, ValueError) as exc:
            issues.append(
                _issue(
                    "invalid managed canonical skill",
                    skill.agent_path,
                    str(exc),
                    "ask the human operator to repair the canonical skill before syncing.",
                )
            )

    if expected_skill_text is not None:
        _add_planned_write(
            root,
            claude_path,
            expected_skill_text.encode("utf-8"),
            kind="skill mirror",
            writes=writes,
            issues=issues,
        )

    agent_support_files = _canonical_support_file_paths(skill.agent_path.parent)
    claude_support_files = _mirror_support_file_paths(claude_dir)
    extra_claude_support = sorted(
        set(claude_support_files) - set(agent_support_files)
    )
    for relative_path in extra_claude_support:
        extra_path = claude_support_files[relative_path]
        issues.append(
            _issue(
                "managed Claude support file has no canonical source",
                extra_path,
                "the file is outside the canonical .agents skill",
                "ask the human operator whether to remove it or restore the canonical support file.",
            )
        )

    for relative_path, agent_support_path in sorted(agent_support_files.items()):
        claude_support_path = claude_dir / relative_path
        try:
            support_bytes = agent_support_path.read_bytes()
        except OSError as exc:
            issues.append(
                _issue(
                    "unreadable canonical support file",
                    agent_support_path,
                    str(exc),
                    "ask the human operator to make the canonical support file readable.",
                )
            )
            continue
        _add_planned_write(
            root,
            claude_support_path,
            support_bytes,
            kind="support file",
            writes=writes,
            issues=issues,
        )


def build_sync_plan(root: Path) -> SyncPlan:
    """Build and validate all synchronization operations without writing."""
    root = root.resolve()
    sources, candidate_names, issues = _discover_managed_sources(root)
    managed_names = set(candidate_names)
    managed_names.update(source.name for source in sources)

    for claude_dir in _claude_skill_dirs(root):
        if claude_dir.name in managed_names:
            continue
        claude_path = claude_dir / "SKILL.md"
        if not claude_path.is_file():
            continue
        try:
            claude_text = claude_path.read_text(encoding="utf-8")
        except OSError:
            continue
        marker, has_marker = _sync_marker_from_text(claude_text)
        if marker != SYNC_METADATA_VALUE or not has_marker:
            continue
        issues.append(
            _issue(
                "managed Claude mirror has no canonical source",
                claude_path,
                "the mirror carries generated-sync provenance but no marked .agents skill exists",
                "ask the human operator whether to remove the mirror or restore and mark its canonical .agents source.",
            )
        )

    writes: list[PlannedWrite] = []
    for source in sorted(sources, key=lambda item: item.name):
        _process_managed_skill(root, source, writes=writes, issues=issues)

    writes.sort(key=lambda write: write.path.relative_to(root).as_posix())
    return SyncPlan(root=root, writes=tuple(writes), issues=tuple(issues))


def _ensure_parent(path: Path, created_dirs: list[Path]) -> None:
    missing: list[Path] = []
    parent = path.parent
    while not parent.exists():
        missing.append(parent)
        parent = parent.parent
    if not parent.is_dir():
        raise OSError(f"destination parent is not a directory: {parent}")

    for directory in reversed(missing):
        directory.mkdir()
        created_dirs.append(directory)


def _atomic_replace(path: Path, content: bytes, mode: int | None) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.sync-",
        dir=str(path.parent),
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _current_file_bytes(path: Path) -> bytes | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise OSError(f"path is no longer a regular file: {path}")
    return path.read_bytes()


def _rollback(
    applied: list[PlannedWrite],
    created_dirs: list[Path],
) -> list[str]:
    errors: list[str] = []
    for write in reversed(applied):
        try:
            if write.before is None:
                write.path.unlink(missing_ok=True)
            else:
                _atomic_replace(write.path, write.before, write.mode)
        except OSError as exc:
            errors.append(f"{write.path}: {exc}")

    for directory in reversed(created_dirs):
        try:
            directory.rmdir()
        except OSError:
            pass
    return errors


def apply_sync_plan(plan: SyncPlan) -> None:
    """Commit a validated plan with atomic replacements and rollback."""
    applied: list[PlannedWrite] = []
    created_dirs: list[Path] = []
    try:
        for write in plan.writes:
            current = _current_file_bytes(write.path)
            if current != write.before:
                raise OSError(
                    f"{write.path} changed after the synchronization plan was built"
                )
            _ensure_parent(write.path, created_dirs)
            _atomic_replace(write.path, write.content, write.mode)
            applied.append(write)
    except OSError as exc:
        rollback_errors = _rollback(applied, created_dirs)
        detail = f"apply failed; attempted rollback after: {exc}"
        if rollback_errors:
            detail += "; rollback also failed for " + ", ".join(rollback_errors)
        raise SyncWriteError(detail) from exc


def _format_drift(plan: SyncPlan) -> str:
    lines = ["Claude skill drift detected:"]
    for write in plan.writes:
        relative = _relative(plan.root, write.path)
        lines.append(f"- {write.action} {relative} ({write.kind})")
    lines.append("Review the plan, then run: python3 -m scripts.sync_claude_skills")
    return "\n".join(lines)


def sync_claude_skills(root: Path, *, check: bool) -> list[Path]:
    """Check or apply a validated Claude mirror plan."""
    plan = build_sync_plan(root)
    if plan.issues:
        raise SyncValidationError(plan.root, list(plan.issues))

    if check:
        return plan.changed_paths

    apply_sync_plan(plan)
    return plan.changed_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Sync Claude mirrors for explicitly marked .agents skills while "
            "preserving Claude-specific frontmatter."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any managed Claude mirror is missing or out of sync",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repo root containing .agents/skills and .claude/skills",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        plan = build_sync_plan(root)
        if plan.issues:
            raise SyncValidationError(plan.root, list(plan.issues))

        if args.check:
            changed = plan.changed_paths
        else:
            apply_sync_plan(plan)
            changed = plan.changed_paths
    except (OSError, ValueError, SyncError) as exc:
        parser.exit(1, f"error: {exc}\n")

    if args.check and changed:
        parser.exit(1, f"{_format_drift(plan)}\n")

    if changed:
        for path in changed:
            print(f"synced {path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
