from pathlib import Path
import subprocess
import sys

import pytest

import scripts.sync_claude_skills as sync_module
from scripts.sync_claude_skills import (
    CODEX_METADATA_PATH,
    SYNC_METADATA_KEY,
    SYNC_METADATA_VALUE,
    SyncValidationError,
    SyncWriteError,
    apply_sync_plan,
    build_sync_plan,
    expected_claude_skill_text,
    expected_new_claude_skill_text,
    split_frontmatter,
    sync_claude_skills,
)


def markdown_document(frontmatter_lines: list[str], body: str) -> str:
    frontmatter = "\n".join(frontmatter_lines)
    return f"---\n{frontmatter}\n---\n\n{body}"


def managed_frontmatter(
    name: str,
    *,
    description: str | None = "Shared description",
    marker: bool = True,
    extra: list[str] | None = None,
) -> list[str]:
    lines = [f"name: {name}"]
    if description is not None:
        lines.append(f"description: {description}")
    if extra:
        lines.extend(extra)
    if marker:
        lines.extend(
            [
                "metadata:",
                f"  {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}",
            ]
        )
    return lines


def write_agent_skill(
    root: Path,
    name: str,
    *,
    body: str = "# Shared Skill\n",
    description: str | None = "Shared description",
    marker: bool = True,
    extra: list[str] | None = None,
) -> Path:
    path = root / ".agents" / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        markdown_document(
            managed_frontmatter(
                name,
                description=description,
                marker=marker,
                extra=extra,
            ),
            body,
        ),
        encoding="utf-8",
    )
    return path


def write_claude_skill(
    root: Path,
    name: str,
    *,
    body: str = "# Claude Skill\n",
    frontmatter: list[str] | None = None,
) -> Path:
    path = root / ".claude" / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is None:
        frontmatter = managed_frontmatter(name, marker=False)
    path.write_text(
        markdown_document(frontmatter, body),
        encoding="utf-8",
    )
    return path


def write_codex_policy(root: Path, name: str, value: object) -> Path:
    path = root / ".agents" / "skills" / name / "agents" / "openai.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"policy:\n  allow_implicit_invocation: {value}\n",
        encoding="utf-8",
    )
    return path


def test_split_frontmatter_removes_leading_skill_metadata() -> None:
    text = """---
name: sample-skill
description: Generic shared skill
---

# Sample Skill

Use this skill.
"""

    frontmatter, body = split_frontmatter(text)

    assert frontmatter == "---\nname: sample-skill\ndescription: Generic shared skill\n---"
    assert body == "# Sample Skill\n\nUse this skill.\n"


def test_expected_claude_skill_text_syncs_portable_fields_and_preserves_claude_fields(
) -> None:
    agent_text = markdown_document(
        managed_frontmatter(
            "sample-skill",
            extra=[
                "license: MIT",
                "compatibility: Requires git",
                "support_files:",
                "  - installer-only-metadata",
            ],
        ),
        "# Shared Body\n",
    )
    claude_text = markdown_document(
        [
            "# Keep this comment",
            "name: sample-skill",
            "description: Claude-specific description",
            "model: haiku",
            "allowed-tools: Read",
            "context: fork",
        ],
        "stale body\n",
    )

    expected = expected_claude_skill_text(
        agent_text,
        claude_text,
        include_sync_marker=True,
    )

    assert "description: Shared description" in expected
    assert "license: MIT" in expected
    assert "compatibility: Requires git" in expected
    assert "model: haiku" in expected
    assert "allowed-tools: Read" in expected
    assert "context: fork" in expected
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in expected
    assert "support_files:" not in expected
    assert expected.endswith("# Shared Body\n")


def test_expected_new_claude_skill_omits_unknown_source_frontmatter() -> None:
    agent_text = markdown_document(
        managed_frontmatter(
            "sample-skill",
            extra=[
                "support_files:",
                "  - installer-only-metadata",
            ],
        ),
        "# Shared Body\n",
    )

    expected = expected_new_claude_skill_text(
        agent_text,
        include_sync_marker=True,
    )

    assert "name: sample-skill" in expected
    assert "description: Shared description" in expected
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in expected
    assert "support_files:" not in expected


def test_codex_policy_translates_explicit_invocation_policy(
    tmp_path: Path,
) -> None:
    agent_skill = write_agent_skill(tmp_path, "deploy")
    claude_skill = write_claude_skill(
        tmp_path,
        "deploy",
        frontmatter=[
            "name: deploy",
            "description: Claude deployment",
            "model: haiku",
        ],
    )
    write_codex_policy(tmp_path, "deploy", "false")

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    text = claude_skill.read_text(encoding="utf-8")
    assert "description: Shared description" in text
    assert "model: haiku" in text
    assert "disable-model-invocation: true" in text
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in text
    assert agent_skill.exists()


def test_codex_policy_true_removes_existing_claude_disable_flag(
    tmp_path: Path,
) -> None:
    claude_skill = write_claude_skill(
        tmp_path,
        "review",
        frontmatter=[
            "name: review",
            "description: Claude review",
            "disable-model-invocation: true",
        ],
    )
    write_agent_skill(tmp_path, "review")
    write_codex_policy(tmp_path, "review", "true")

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert "disable-model-invocation" not in claude_skill.read_text(
        encoding="utf-8"
    )


def test_absent_codex_policy_preserves_existing_claude_invocation_choice(
    tmp_path: Path,
) -> None:
    claude_skill = write_claude_skill(
        tmp_path,
        "review",
        frontmatter=[
            "name: review",
            "description: Claude review",
            "disable-model-invocation: true",
        ],
    )
    write_agent_skill(tmp_path, "review")

    sync_claude_skills(tmp_path, check=False)

    assert "disable-model-invocation: true" in claude_skill.read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize(
    "sidecar",
    [
        "interface:\n  display_name: Review\n",
        "policy: {}\n",
    ],
)
def test_non_invocation_codex_metadata_preserves_claude_choice(
    tmp_path: Path,
    sidecar: str,
) -> None:
    claude_skill = write_claude_skill(
        tmp_path,
        "review",
        frontmatter=[
            "name: review",
            "description: Claude review",
            "disable-model-invocation: true",
        ],
    )
    write_agent_skill(tmp_path, "review")
    sidecar_path = (
        tmp_path / ".agents" / "skills" / "review" / "agents" / "openai.yaml"
    )
    sidecar_path.parent.mkdir(parents=True)
    sidecar_path.write_text(sidecar, encoding="utf-8")

    sync_claude_skills(tmp_path, check=False)

    text = claude_skill.read_text(encoding="utf-8")
    assert "disable-model-invocation: true" in text


def test_falsey_codex_policy_blocks_every_planned_write(
    tmp_path: Path,
) -> None:
    first_claude = write_claude_skill(
        tmp_path,
        "first",
        body="# Old first\n",
        frontmatter=["name: first", "description: Old first"],
    )
    write_agent_skill(tmp_path, "first", body="# New first\n")
    write_agent_skill(tmp_path, "second", body="# New second\n")
    second_sidecar = (
        tmp_path / ".agents" / "skills" / "second" / "agents" / "openai.yaml"
    )
    second_sidecar.parent.mkdir(parents=True)
    second_sidecar.write_text("policy: false\n", encoding="utf-8")
    before_first = first_claude.read_bytes()

    with pytest.raises(SyncValidationError) as check_error:
        sync_claude_skills(tmp_path, check=True)
    with pytest.raises(SyncValidationError) as apply_error:
        sync_claude_skills(tmp_path, check=False)

    assert str(check_error.value) == str(apply_error.value)
    assert "policy must be a mapping" in str(check_error.value)
    assert first_claude.read_bytes() == before_first
    assert not (
        tmp_path / ".claude" / "skills" / "second" / "SKILL.md"
    ).exists()


def test_unmanaged_agents_and_claude_skills_are_ignored(tmp_path: Path) -> None:
    agent_skill = write_agent_skill(tmp_path, "personal", marker=False)
    claude_skill = write_claude_skill(
        tmp_path,
        "native",
        frontmatter=[
            "name: native",
            "description: Claude-only",
            "model: haiku",
        ],
    )
    native_support = claude_skill.parent / "examples.md"
    native_support.write_text("Claude-only support\n", encoding="utf-8")

    assert sync_claude_skills(tmp_path, check=True) == []
    assert sync_claude_skills(tmp_path, check=False) == []
    assert not (
        tmp_path / ".claude" / "skills" / "personal" / "SKILL.md"
    ).exists()
    assert agent_skill.exists()
    assert native_support.read_text(encoding="utf-8") == "Claude-only support\n"


def test_managed_skill_creates_mirror_with_provenance_marker(
    tmp_path: Path,
) -> None:
    write_agent_skill(
        tmp_path,
        "new-skill",
        extra=["support_files:", "  - installer-only-metadata"],
    )

    claude_path = tmp_path / ".claude" / "skills" / "new-skill" / "SKILL.md"
    assert sync_claude_skills(tmp_path, check=True) == [claude_path]
    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_path]
    text = claude_path.read_text(encoding="utf-8")
    assert "name: new-skill" in text
    assert "description: Shared description" in text
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in text
    assert "support_files:" not in text


def test_managed_stale_mirror_updates_portable_content_only(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "sample-skill", body="# Canonical body\n")
    claude_skill = write_claude_skill(
        tmp_path,
        "sample-skill",
        body="stale body\n",
        frontmatter=[
            "# Claude-specific configuration",
            "name: sample-skill",
            "description: Local description",
            "model: haiku",
            "allowed-tools: Read",
        ],
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    text = claude_skill.read_text(encoding="utf-8")
    assert "# Claude-specific configuration" in text
    assert "description: Shared description" in text
    assert "model: haiku" in text
    assert "allowed-tools: Read" in text
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in text
    assert text.endswith("# Canonical body\n")


@pytest.mark.parametrize(
    "metadata_lines",
    [
        ["metadata:", "  - not a mapping"],
        ["metadata: scalar-value"],
        ["metadata: null"],
    ],
)
def test_non_mapping_claude_metadata_blocks_check_and_apply(
    tmp_path: Path,
    metadata_lines: list[str],
) -> None:
    write_agent_skill(tmp_path, "broken-metadata")
    claude_skill = write_claude_skill(
        tmp_path,
        "broken-metadata",
        frontmatter=[
            "name: broken-metadata",
            "description: Local description",
            *metadata_lines,
            "model: haiku",
        ],
    )
    before = claude_skill.read_bytes()

    with pytest.raises(SyncValidationError) as check_error:
        sync_claude_skills(tmp_path, check=True)
    with pytest.raises(SyncValidationError) as apply_error:
        sync_claude_skills(tmp_path, check=False)

    assert str(check_error.value) == str(apply_error.value)
    assert "invalid managed Claude mirror" in str(check_error.value)
    assert ".claude/skills/broken-metadata/SKILL.md" in str(check_error.value)
    assert "Claude metadata is not a YAML mapping" in str(check_error.value)
    assert claude_skill.read_bytes() == before
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" not in claude_skill.read_text(
        encoding="utf-8"
    )


def test_invalid_metadata_late_in_plan_blocks_earlier_repairs(
    tmp_path: Path,
) -> None:
    first_claude = write_claude_skill(
        tmp_path,
        "first",
        body="# Old first\n",
        frontmatter=["name: first", "description: Old first"],
    )
    write_agent_skill(tmp_path, "first", body="# New first\n")
    write_agent_skill(tmp_path, "second", body="# New second\n")
    second_claude = write_claude_skill(
        tmp_path,
        "second",
        frontmatter=[
            "name: second",
            "description: Second",
            "metadata:",
            "  - malformed",
        ],
    )
    before_first = first_claude.read_bytes()
    before_second = second_claude.read_bytes()

    with pytest.raises(SyncValidationError):
        sync_claude_skills(tmp_path, check=False)

    assert first_claude.read_bytes() == before_first
    assert second_claude.read_bytes() == before_second


def test_valid_claude_metadata_preserves_comments_order_and_unknown_values(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "preserved")
    claude_skill = write_claude_skill(
        tmp_path,
        "preserved",
        frontmatter=[
            "# Claude configuration",
            "name: preserved",
            "description: Local description",
            "metadata:",
            "  # Keep this provenance note",
            "  zeta: retained",
            "  nested:",
            "    second: value",
            "    first: 1",
            "  alpha: retained",
            "model: haiku",
        ],
    )

    sync_claude_skills(tmp_path, check=False)

    text = claude_skill.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(text)
    document = sync_module._frontmatter_document(frontmatter)
    mapping = sync_module._frontmatter_mapping(document)

    assert mapping["metadata"][SYNC_METADATA_KEY] == SYNC_METADATA_VALUE
    assert mapping["metadata"]["zeta"] == "retained"
    assert mapping["metadata"]["nested"] == {"second": "value", "first": 1}
    assert mapping["metadata"]["alpha"] == "retained"
    assert text.index("zeta: retained") < text.index("alpha: retained")
    assert "# Keep this provenance note" in text
    assert "model: haiku" in text


def test_omitted_portable_field_is_removed_from_mirror(tmp_path: Path) -> None:
    write_agent_skill(tmp_path, "sample-skill")
    claude_skill = write_claude_skill(
        tmp_path,
        "sample-skill",
        frontmatter=[
            "name: sample-skill",
            "description: Local description",
            "compatibility: Claude-only compatibility",
            "model: haiku",
        ],
    )

    sync_claude_skills(tmp_path, check=False)

    text = claude_skill.read_text(encoding="utf-8")
    assert "compatibility:" not in text
    assert "model: haiku" in text


def test_managed_support_files_sync_as_bytes(tmp_path: Path) -> None:
    write_agent_skill(tmp_path, "binary")
    source_support = (
        tmp_path / ".agents" / "skills" / "binary" / "assets" / "asset.bin"
    )
    source_support.parent.mkdir(parents=True)
    source_support.write_bytes(b"\x00\xffskill asset")

    changed = sync_claude_skills(tmp_path, check=False)

    mirror_support = (
        tmp_path / ".claude" / "skills" / "binary" / "assets" / "asset.bin"
    )
    assert changed == [
        tmp_path / ".claude" / "skills" / "binary" / "SKILL.md",
        mirror_support,
    ]
    assert mirror_support.read_bytes() == b"\x00\xffskill asset"


def test_unmanaged_claude_support_file_is_accepted(tmp_path: Path) -> None:
    native_skill = write_claude_skill(
        tmp_path,
        "native",
        frontmatter=["name: native", "description: Native Claude skill"],
    )
    support = native_skill.parent / "native-only.md"
    support.write_text("Native support\n", encoding="utf-8")

    assert sync_claude_skills(tmp_path, check=False) == []
    assert support.exists()


def test_managed_extra_support_file_blocks_all_writes(tmp_path: Path) -> None:
    first = write_agent_skill(tmp_path, "first", body="# New first\n")
    first_claude = write_claude_skill(
        tmp_path,
        "first",
        body="# Old first\n",
        frontmatter=["name: first", "description: Old first"],
    )
    orphan = first_claude.parent / "old.md"
    orphan.write_text("orphan\n", encoding="utf-8")
    before_first = first_claude.read_bytes()
    before_orphan = orphan.read_bytes()

    with pytest.raises(SyncValidationError) as exc_info:
        sync_claude_skills(tmp_path, check=False)

    assert "no files were changed" in str(exc_info.value)
    assert "Human decision required" in str(exc_info.value)
    assert first.exists()
    assert first_claude.read_bytes() == before_first
    assert orphan.read_bytes() == before_orphan


def test_extra_claude_codex_sidecar_is_a_human_decision(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "sample-skill", body="# New body\n")
    claude_skill = write_claude_skill(
        tmp_path,
        "sample-skill",
        body="# Old body\n",
        frontmatter=["name: sample-skill", "description: Old"],
    )
    extra_sidecar = (
        tmp_path
        / ".claude"
        / "skills"
        / "sample-skill"
        / "agents"
        / "openai.yaml"
    )
    extra_sidecar.parent.mkdir(parents=True)
    extra_sidecar.write_text("native: claude\n", encoding="utf-8")
    before_skill = claude_skill.read_bytes()
    before_sidecar = extra_sidecar.read_bytes()

    with pytest.raises(SyncValidationError) as check_error:
        sync_claude_skills(tmp_path, check=True)
    with pytest.raises(SyncValidationError) as apply_error:
        sync_claude_skills(tmp_path, check=False)

    assert str(check_error.value) == str(apply_error.value)
    assert "managed Claude support file has no canonical source" in str(
        check_error.value
    )
    assert ".claude/skills/sample-skill/agents/openai.yaml" in str(
        check_error.value
    )
    assert claude_skill.read_bytes() == before_skill
    assert extra_sidecar.read_bytes() == before_sidecar


def test_canonical_codex_sidecar_maps_policy_without_being_copied(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "deploy")
    canonical_sidecar = write_codex_policy(tmp_path, "deploy", "false")

    changed = sync_claude_skills(tmp_path, check=False)

    claude_dir = tmp_path / ".claude" / "skills" / "deploy"
    claude_skill = claude_dir / "SKILL.md"
    assert changed == [claude_skill]
    assert "disable-model-invocation: true" in claude_skill.read_text(
        encoding="utf-8"
    )
    assert not (claude_dir / CODEX_METADATA_PATH).exists()
    assert sync_module.support_file_paths(canonical_sidecar.parent.parent) == {}


def test_invalid_late_metadata_causes_no_partial_writes(tmp_path: Path) -> None:
    first_claude = write_claude_skill(
        tmp_path,
        "first",
        body="# Old first\n",
        frontmatter=["name: first", "description: Old first"],
    )
    write_agent_skill(tmp_path, "first", body="# New first\n")
    write_agent_skill(tmp_path, "second", body="# New second\n")
    invalid_policy = (
        tmp_path / ".agents" / "skills" / "second" / "agents" / "openai.yaml"
    )
    invalid_policy.parent.mkdir(parents=True)
    invalid_policy.write_text(
        "policy:\n  allow_implicit_invocation: sometimes\n",
        encoding="utf-8",
    )
    before = first_claude.read_bytes()

    with pytest.raises(SyncValidationError, match="policy.allow_implicit_invocation"):
        sync_claude_skills(tmp_path, check=False)

    assert first_claude.read_bytes() == before


def test_managed_orphan_mirror_requires_human_decision(tmp_path: Path) -> None:
    claude_skill = write_claude_skill(
        tmp_path,
        "old-skill",
        frontmatter=managed_frontmatter("old-skill"),
    )
    before = claude_skill.read_bytes()

    with pytest.raises(SyncValidationError) as exc_info:
        sync_claude_skills(tmp_path, check=False)

    message = str(exc_info.value)
    assert "has no canonical source" in message
    assert "Human decision required" in message
    assert "Decide whether to remove the mirror" in message
    assert claude_skill.read_bytes() == before


def test_removing_source_marker_blocks_until_mirror_is_resolved(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "retired", marker=False)
    claude_skill = write_claude_skill(
        tmp_path,
        "retired",
        frontmatter=managed_frontmatter("retired"),
    )

    with pytest.raises(SyncValidationError, match="has no canonical source"):
        sync_claude_skills(tmp_path, check=False)

    assert claude_skill.exists()


def _malformed_marker_document(name: str, marker: str) -> str:
    return f"""---
name: {name}
description: Shared description
metadata:
  {marker}
  broken: [
---

# Body
"""


@pytest.mark.parametrize(
    ("name", "marker", "managed"),
    [
        ("wrong-value", f"{SYNC_METADATA_KEY}: not-managed", False),
        ("comment-value", f"# {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}", False),
        ("nested-value", f"nested:\n    {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}", False),
        ("exact-value", f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}", True),
    ],
)
def test_malformed_canonical_marker_requires_exact_direct_value(
    tmp_path: Path,
    name: str,
    marker: str,
    managed: bool,
) -> None:
    path = tmp_path / ".agents" / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(_malformed_marker_document(name, marker), encoding="utf-8")

    plan = build_sync_plan(tmp_path)

    if managed:
        assert any(
            issue.path == path and issue.category == "invalid managed canonical skill"
            for issue in plan.issues
        )
        with pytest.raises(SyncValidationError) as check_error:
            sync_claude_skills(tmp_path, check=True)
        with pytest.raises(SyncValidationError) as apply_error:
            sync_claude_skills(tmp_path, check=False)
        assert str(check_error.value) == str(apply_error.value)
    else:
        assert plan.issues == ()
        assert plan.writes == ()
        assert sync_claude_skills(tmp_path, check=False) == []
        assert not (tmp_path / ".claude" / "skills" / name).exists()


def test_valid_unmarked_body_example_does_not_enroll_canonical_skill(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agents" / "skills" / "body-example" / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        """---
name: body-example
description: Shared description
---

```yaml
metadata:
  agent-harness-framework/claude-sync: agents-to-claude
```
""",
        encoding="utf-8",
    )

    assert build_sync_plan(tmp_path).issues == ()
    assert sync_claude_skills(tmp_path, check=False) == []
    assert not (tmp_path / ".claude" / "skills" / "body-example").exists()


def test_marker_false_candidates_do_not_block_or_mutate_managed_drift(
    tmp_path: Path,
) -> None:
    managed = write_agent_skill(tmp_path, "managed", body="# New body\n")
    managed_mirror = write_claude_skill(
        tmp_path,
        "managed",
        body="# Old body\n",
        frontmatter=["name: managed", "description: Old"],
    )
    false_candidate = tmp_path / ".agents" / "skills" / "native" / "SKILL.md"
    false_candidate.parent.mkdir(parents=True)
    false_candidate.write_text(
        _malformed_marker_document(
            "native",
            f"{SYNC_METADATA_KEY}: not-managed",
        ),
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [managed_mirror]
    assert managed.exists()
    assert managed_mirror.read_text(encoding="utf-8").endswith("# New body\n")
    assert not (tmp_path / ".claude" / "skills" / "native").exists()


def test_exact_malformed_orphan_marker_requires_human_decision(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".claude" / "skills" / "orphan" / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        _malformed_marker_document("orphan", f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}"),
        encoding="utf-8",
    )
    before = path.read_bytes()

    with pytest.raises(SyncValidationError) as check_error:
        sync_claude_skills(tmp_path, check=True)
    with pytest.raises(SyncValidationError) as apply_error:
        sync_claude_skills(tmp_path, check=False)

    assert str(check_error.value) == str(apply_error.value)
    assert "managed Claude mirror has no canonical source" in str(check_error.value)
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "content",
    [
        _malformed_marker_document(
            "wrong",
            f"{SYNC_METADATA_KEY}: not-managed",
        ),
        _malformed_marker_document(
            "nested",
            f"nested:\n    {SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}",
        ),
        """---
name: body
description: Native
---

agent-harness-framework/claude-sync: agents-to-claude
""",
    ],
)
def test_false_orphan_marker_candidates_remain_unmanaged(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / ".claude" / "skills" / "native" / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(content, encoding="utf-8")
    before = path.read_bytes()

    assert build_sync_plan(tmp_path).issues == ()
    assert sync_claude_skills(tmp_path, check=True) == []
    assert sync_claude_skills(tmp_path, check=False) == []
    assert path.read_bytes() == before


def test_missing_mirror_provenance_marker_is_repaired(tmp_path: Path) -> None:
    write_agent_skill(tmp_path, "sample-skill")
    claude_skill = write_claude_skill(
        tmp_path,
        "sample-skill",
        frontmatter=[
            "name: sample-skill",
            "description: Shared description",
            "model: haiku",
        ],
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert f"{SYNC_METADATA_KEY}: {SYNC_METADATA_VALUE}" in claude_skill.read_text(
        encoding="utf-8"
    )


def test_malformed_existing_mirror_requires_human_repair(tmp_path: Path) -> None:
    write_agent_skill(tmp_path, "broken")
    claude_skill = tmp_path / ".claude" / "skills" / "broken" / "SKILL.md"
    claude_skill.parent.mkdir(parents=True)
    claude_skill.write_text("---\nname: broken\n", encoding="utf-8")
    before = claude_skill.read_bytes()

    with pytest.raises(SyncValidationError, match="Repair or consciously recreate"):
        sync_claude_skills(tmp_path, check=False)

    assert claude_skill.read_bytes() == before


def test_canonical_name_must_match_skill_directory(tmp_path: Path) -> None:
    write_agent_skill(tmp_path, "directory-name")
    path = tmp_path / ".agents" / "skills" / "directory-name" / "SKILL.md"
    path.write_text(
        markdown_document(
            managed_frontmatter("different-name"),
            "# Body\n",
        ),
        encoding="utf-8",
    )

    with pytest.raises(SyncValidationError, match="does not match directory"):
        sync_claude_skills(tmp_path, check=False)

    assert not (
        tmp_path / ".claude" / "skills" / "directory-name" / "SKILL.md"
    ).exists()


def test_check_and_apply_report_identical_validation_diagnostics(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "sample-skill")
    claude_skill = write_claude_skill(tmp_path, "sample-skill")
    orphan = claude_skill.parent / "orphan.md"
    orphan.write_text("orphan\n", encoding="utf-8")

    with pytest.raises(SyncValidationError) as check_error:
        sync_claude_skills(tmp_path, check=True)
    with pytest.raises(SyncValidationError) as apply_error:
        sync_claude_skills(tmp_path, check=False)

    assert str(check_error.value) == str(apply_error.value)


def test_cli_check_reports_actionable_plan_for_agents_and_humans(
    tmp_path: Path,
) -> None:
    write_agent_skill(tmp_path, "sample-skill")
    write_claude_skill(tmp_path, "sample-skill")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/sync_claude_skills.py",
            "--check",
            "--root",
            str(tmp_path),
        ],
        cwd=Path(__file__).parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Claude skill drift detected:" in result.stderr
    assert "update" in result.stderr
    assert "run:" in result.stderr


def test_paths_containing_spaces_are_supported(tmp_path: Path) -> None:
    root = tmp_path / "repo with spaces"
    write_agent_skill(root, "sample-skill")

    changed = sync_claude_skills(root, check=False)

    assert changed == [root / ".claude" / "skills" / "sample-skill" / "SKILL.md"]


def test_apply_rolls_back_if_commit_fails_mid_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_agent_skill(tmp_path, "sample-skill")
    source_support = (
        tmp_path / ".agents" / "skills" / "sample-skill" / "template.md"
    )
    source_support.write_text("new support\n", encoding="utf-8")
    claude_skill = write_claude_skill(
        tmp_path,
        "sample-skill",
        body="# Old body\n",
        frontmatter=["name: sample-skill", "description: Old"],
    )
    claude_support = claude_skill.parent / "template.md"
    claude_support.write_text("old support\n", encoding="utf-8")
    before_skill = claude_skill.read_bytes()
    before_support = claude_support.read_bytes()
    plan = build_sync_plan(tmp_path)

    original_atomic_replace = sync_module._atomic_replace
    calls = 0

    def fail_on_second_write(path: Path, content: bytes, mode: int | None) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated commit failure")
        original_atomic_replace(path, content, mode)

    monkeypatch.setattr(
        sync_module,
        "_atomic_replace",
        fail_on_second_write,
    )

    with pytest.raises(SyncWriteError, match="attempted rollback"):
        apply_sync_plan(plan)

    assert claude_skill.read_bytes() == before_skill
    assert claude_support.read_bytes() == before_support
