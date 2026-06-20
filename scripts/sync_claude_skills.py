#!/usr/bin/env python3
"""Sync Claude Code skill mirrors from canonical .agents skill sources."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in missing dependency envs.
    yaml = None


CODEX_METADATA_PATH = Path("agents") / "openai.yaml"
CLAUDE_DISABLE_MODEL_INVOCATION_KEY = "disable-model-invocation"
CLAUDE_DISABLE_MODEL_INVOCATION_PATTERN = re.compile(
    rf"^{re.escape(CLAUDE_DISABLE_MODEL_INVOCATION_KEY)}\s*:"
)


@dataclass(frozen=True)
class SkillPair:
    agent_path: Path
    claude_path: Path
    claude_exists: bool


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


def expected_claude_skill_text(
    agent_text: str,
    claude_text: str,
    *,
    codex_allow_implicit_invocation: bool | None = None,
) -> str:
    """Build Claude skill text with Claude frontmatter and canonical agent body."""
    agent_frontmatter, agent_body = split_frontmatter(agent_text)
    claude_frontmatter, _ = split_frontmatter(claude_text)

    if not agent_frontmatter:
        raise ValueError("agent skill is missing YAML frontmatter")
    if not claude_frontmatter:
        raise ValueError("Claude skill is missing YAML frontmatter")

    claude_frontmatter = expected_claude_frontmatter(
        claude_frontmatter,
        codex_allow_implicit_invocation=codex_allow_implicit_invocation,
    )

    return f"{claude_frontmatter}\n\n{agent_body}"


def expected_new_claude_skill_text(
    agent_text: str,
    *,
    codex_allow_implicit_invocation: bool | None = None,
) -> str:
    """Build a new Claude skill mirror from the canonical agent skill."""
    agent_frontmatter, agent_body = split_frontmatter(agent_text)

    if not agent_frontmatter:
        raise ValueError("agent skill is missing YAML frontmatter")

    agent_frontmatter = expected_claude_frontmatter(
        agent_frontmatter,
        codex_allow_implicit_invocation=codex_allow_implicit_invocation,
    )

    return f"{agent_frontmatter}\n\n{agent_body}"


def expected_claude_frontmatter(
    frontmatter: str,
    *,
    codex_allow_implicit_invocation: bool | None,
) -> str:
    """Return Claude frontmatter with invocation policy synced when configured."""
    if codex_allow_implicit_invocation is None:
        return frontmatter

    disable_model_invocation = not codex_allow_implicit_invocation
    lines = frontmatter.splitlines()
    expected_lines: list[str] = []
    invocation_line_seen = False

    for index, line in enumerate(lines):
        if CLAUDE_DISABLE_MODEL_INVOCATION_PATTERN.match(line):
            if disable_model_invocation and not invocation_line_seen:
                expected_lines.append(
                    f"{CLAUDE_DISABLE_MODEL_INVOCATION_KEY}: true"
                )
                invocation_line_seen = True
            continue

        if (
            index == len(lines) - 1
            and line == "---"
            and disable_model_invocation
            and not invocation_line_seen
        ):
            expected_lines.append(f"{CLAUDE_DISABLE_MODEL_INVOCATION_KEY}: true")
            invocation_line_seen = True

        expected_lines.append(line)

    return "\n".join(expected_lines)


def codex_allow_implicit_invocation(skill_dir: Path) -> bool | None:
    """Return Codex implicit invocation policy from agents/openai.yaml if present."""
    metadata_path = skill_dir / CODEX_METADATA_PATH
    if not metadata_path.exists():
        return None

    if yaml is None:
        raise ValueError("PyYAML is required to parse agents/openai.yaml")

    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"{metadata_path}: Codex skill metadata must be a mapping")

    policy = metadata.get("policy") or {}
    if not isinstance(policy, dict):
        raise ValueError(f"{metadata_path}: policy must be a mapping")

    allow_implicit_invocation = policy.get("allow_implicit_invocation", True)
    if not isinstance(allow_implicit_invocation, bool):
        raise ValueError(
            f"{metadata_path}: policy.allow_implicit_invocation must be a boolean"
        )

    return allow_implicit_invocation


def discover_skill_pairs(root: Path) -> list[SkillPair]:
    """Return one .agents/.claude pair for each canonical skill source."""
    claude_root = root / ".claude" / "skills"
    agent_root = root / ".agents" / "skills"
    agent_paths = {path.parent.name: path for path in agent_root.glob("*/SKILL.md")}
    claude_paths = {path.parent.name: path for path in claude_root.glob("*/SKILL.md")}

    extra_claude_names = sorted(set(claude_paths) - set(agent_paths))
    if extra_claude_names:
        extra_paths = "\n".join(f"- {claude_paths[name]}" for name in extra_claude_names)
        raise FileNotFoundError(
            "Claude skill mirrors without matching .agents sources:\n"
            f"{extra_paths}\n"
            "Remove the orphaned Claude mirror or restore its .agents source."
        )

    pairs: list[SkillPair] = []

    for skill_name, agent_path in sorted(agent_paths.items()):
        claude_path = claude_root / skill_name / "SKILL.md"
        pairs.append(
            SkillPair(
                agent_path=agent_path,
                claude_path=claude_path,
                claude_exists=skill_name in claude_paths,
            )
        )

    return pairs


def support_file_paths(skill_dir: Path) -> dict[Path, Path]:
    """Return non-SKILL.md files in a skill directory keyed by relative path."""
    if not skill_dir.exists():
        return {}

    paths: dict[Path, Path] = {}
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.name == "SKILL.md":
            continue

        relative_path = path.relative_to(skill_dir)
        if relative_path == CODEX_METADATA_PATH:
            continue

        paths[relative_path] = path

    return {
        relative_path: paths[relative_path]
        for relative_path in sorted(paths)
    }


def sync_claude_skills(root: Path, *, check: bool) -> list[Path]:
    """Sync or check Claude skill mirror parity. Return paths that differ."""
    changed: list[Path] = []

    for pair in discover_skill_pairs(root):
        agent_text = pair.agent_path.read_text(encoding="utf-8")
        try:
            allow_implicit_invocation = codex_allow_implicit_invocation(
                pair.agent_path.parent
            )
            if pair.claude_exists:
                claude_text = pair.claude_path.read_text(encoding="utf-8")
                expected = expected_claude_skill_text(
                    agent_text,
                    claude_text,
                    codex_allow_implicit_invocation=allow_implicit_invocation,
                )
            else:
                claude_text = ""
                expected = expected_new_claude_skill_text(
                    agent_text,
                    codex_allow_implicit_invocation=allow_implicit_invocation,
                )
        except ValueError as exc:
            raise ValueError(f"{pair.claude_path}: {exc}") from exc

        if claude_text != expected:
            changed.append(pair.claude_path)
            if not check:
                pair.claude_path.parent.mkdir(parents=True, exist_ok=True)
                pair.claude_path.write_text(expected, encoding="utf-8")

        agent_support_files = support_file_paths(pair.agent_path.parent)
        claude_support_files = support_file_paths(pair.claude_path.parent)
        extra_claude_support = sorted(
            set(claude_support_files) - set(agent_support_files)
        )
        if extra_claude_support:
            extra_paths = "\n".join(
                f"- {claude_support_files[relative_path]}"
                for relative_path in extra_claude_support
            )
            raise FileNotFoundError(
                "Claude skill support files without matching .agents sources:\n"
                f"{extra_paths}\n"
                "Remove the orphaned Claude support file or restore its .agents source."
            )

        for relative_path, agent_support_path in sorted(agent_support_files.items()):
            claude_support_path = pair.claude_path.parent / relative_path
            agent_support_bytes = agent_support_path.read_bytes()
            if claude_support_path.exists():
                claude_support_bytes = claude_support_path.read_bytes()
            else:
                claude_support_bytes = b""

            if claude_support_bytes != agent_support_bytes:
                changed.append(claude_support_path)
                if not check:
                    claude_support_path.parent.mkdir(parents=True, exist_ok=True)
                    claude_support_path.write_bytes(agent_support_bytes)

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Sync .claude skill mirrors from canonical .agents skill sources "
            "while preserving existing Claude-specific frontmatter."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any Claude skill mirror is missing or out of sync",
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
        changed = sync_claude_skills(root, check=args.check)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")

    if args.check and changed:
        paths = "\n".join(f"- {path.relative_to(root)}" for path in changed)
        parser.exit(
            1,
            "Claude skill drift detected:\n"
            f"{paths}\n"
            "Run: python3 -m scripts.sync_claude_skills\n",
        )

    if changed:
        for path in changed:
            print(f"synced {path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
