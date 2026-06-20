from pathlib import Path

import pytest

from scripts.sync_claude_skills import (
    expected_claude_skill_text,
    split_frontmatter,
    sync_claude_skills,
)


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


def test_expected_claude_skill_text_preserves_claude_frontmatter() -> None:
    agent_text = """---
name: sample-skill
description: Shared description
---

# Shared Body
"""
    claude_text = """---
name: sample-skill
description: Claude-specific description
model: haiku
---

stale body
"""

    expected = expected_claude_skill_text(agent_text, claude_text)

    assert expected == """---
name: sample-skill
description: Claude-specific description
model: haiku
---

# Shared Body
"""


def test_expected_claude_skill_text_sets_user_invoked_from_codex_policy() -> None:
    agent_text = """---
name: deploy
description: Shared description
---

# Shared Body
"""
    claude_text = """---
name: deploy
description: Claude-specific description
model: haiku
---

stale body
"""

    expected = expected_claude_skill_text(
        agent_text,
        claude_text,
        codex_allow_implicit_invocation=False,
    )

    assert expected == """---
name: deploy
description: Claude-specific description
model: haiku
disable-model-invocation: true
---

# Shared Body
"""


def test_expected_claude_skill_text_clears_user_invoked_from_codex_policy() -> None:
    agent_text = """---
name: deploy
description: Shared description
---

# Shared Body
"""
    claude_text = """---
name: deploy
description: Claude-specific description
disable-model-invocation: true
model: haiku
---

stale body
"""

    expected = expected_claude_skill_text(
        agent_text,
        claude_text,
        codex_allow_implicit_invocation=True,
    )

    assert expected == """---
name: deploy
description: Claude-specific description
model: haiku
---

# Shared Body
"""


def test_sync_claude_skills_check_detects_drift(tmp_path: Path) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "sample-skill" / "SKILL.md"
    claude_skill = tmp_path / ".claude" / "skills" / "sample-skill" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: sample-skill
description: Shared
---

# Shared
""",
        encoding="utf-8",
    )
    claude_skill.write_text(
        """---
name: sample-skill
description: Claude-specific
model: haiku
---

stale
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=True)

    assert changed == [claude_skill]
    assert claude_skill.read_text(encoding="utf-8").endswith("stale\n")


def test_sync_claude_skills_updates_materialized_body(tmp_path: Path) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "sample-skill" / "SKILL.md"
    claude_skill = tmp_path / ".claude" / "skills" / "sample-skill" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: sample-skill
description: Shared
---

# Shared
""",
        encoding="utf-8",
    )
    claude_skill.write_text(
        """---
name: sample-skill
description: Claude-specific
model: haiku
---

stale
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert claude_skill.read_text(encoding="utf-8") == """---
name: sample-skill
description: Claude-specific
model: haiku
---

# Shared
"""


def test_sync_claude_skills_syncs_user_invoked_policy_from_codex_metadata(
    tmp_path: Path,
) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "deploy" / "SKILL.md"
    codex_metadata = (
        tmp_path / ".agents" / "skills" / "deploy" / "agents" / "openai.yaml"
    )
    claude_skill = tmp_path / ".claude" / "skills" / "deploy" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    codex_metadata.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: deploy
description: Shared
---

# Deploy
""",
        encoding="utf-8",
    )
    codex_metadata.write_text(
        """policy:
  allow_implicit_invocation: false
""",
        encoding="utf-8",
    )
    claude_skill.write_text(
        """---
name: deploy
description: Claude-specific
model: haiku
---

stale
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert claude_skill.read_text(encoding="utf-8") == """---
name: deploy
description: Claude-specific
model: haiku
disable-model-invocation: true
---

# Deploy
"""
    assert not (
        tmp_path / ".claude" / "skills" / "deploy" / "agents" / "openai.yaml"
    ).exists()


def test_sync_claude_skills_syncs_model_invoked_policy_from_codex_metadata(
    tmp_path: Path,
) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "review" / "SKILL.md"
    codex_metadata = (
        tmp_path / ".agents" / "skills" / "review" / "agents" / "openai.yaml"
    )
    claude_skill = tmp_path / ".claude" / "skills" / "review" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    codex_metadata.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: review
description: Shared
---

# Review
""",
        encoding="utf-8",
    )
    codex_metadata.write_text(
        """policy:
  allow_implicit_invocation: true
""",
        encoding="utf-8",
    )
    claude_skill.write_text(
        """---
name: review
description: Claude-specific
disable-model-invocation: true
model: haiku
---

# Review
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert claude_skill.read_text(encoding="utf-8") == """---
name: review
description: Claude-specific
model: haiku
---

# Review
"""


def test_sync_claude_skills_check_detects_missing_claude_mirror(
    tmp_path: Path,
) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "new-skill" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: new-skill
description: New shared skill
---

# New Skill
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=True)

    assert changed == [tmp_path / ".claude" / "skills" / "new-skill" / "SKILL.md"]


def test_sync_claude_skills_creates_missing_claude_mirror(tmp_path: Path) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "new-skill" / "SKILL.md"
    claude_skill = tmp_path / ".claude" / "skills" / "new-skill" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: new-skill
description: New shared skill
---

# New Skill
""",
        encoding="utf-8",
    )

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_skill]
    assert claude_skill.read_text(encoding="utf-8") == agent_skill.read_text(
        encoding="utf-8"
    )


def test_sync_claude_skills_rejects_orphaned_claude_mirror(
    tmp_path: Path,
) -> None:
    claude_skill = tmp_path / ".claude" / "skills" / "old-skill" / "SKILL.md"
    claude_skill.parent.mkdir(parents=True)
    claude_skill.write_text(
        """---
name: old-skill
description: Old Claude skill
---

# Old Skill
""",
        encoding="utf-8",
    )

    with pytest.raises(FileNotFoundError, match="without matching .agents sources"):
        sync_claude_skills(tmp_path, check=False)

    assert claude_skill.exists()


def test_sync_claude_skills_check_detects_missing_support_file(
    tmp_path: Path,
) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "work-brief" / "SKILL.md"
    support_file = tmp_path / ".agents" / "skills" / "work-brief" / "template.md"
    claude_skill = tmp_path / ".claude" / "skills" / "work-brief" / "SKILL.md"
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: work-brief
description: Shared
---

# Work Brief
""",
        encoding="utf-8",
    )
    support_file.write_text("# Template\n", encoding="utf-8")
    claude_skill.write_text(agent_skill.read_text(encoding="utf-8"), encoding="utf-8")

    changed = sync_claude_skills(tmp_path, check=True)

    assert changed == [tmp_path / ".claude" / "skills" / "work-brief" / "template.md"]


def test_sync_claude_skills_copies_support_files(tmp_path: Path) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "work-brief" / "SKILL.md"
    support_file = tmp_path / ".agents" / "skills" / "work-brief" / "template.md"
    claude_skill = tmp_path / ".claude" / "skills" / "work-brief" / "SKILL.md"
    claude_support_file = (
        tmp_path / ".claude" / "skills" / "work-brief" / "template.md"
    )
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: work-brief
description: Shared
---

# Work Brief
""",
        encoding="utf-8",
    )
    support_file.write_text("# Template\n", encoding="utf-8")
    claude_skill.write_text(agent_skill.read_text(encoding="utf-8"), encoding="utf-8")

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_support_file]
    assert claude_support_file.read_text(encoding="utf-8") == "# Template\n"


def test_sync_claude_skills_copies_support_files_as_bytes(tmp_path: Path) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "binary" / "SKILL.md"
    support_file = tmp_path / ".agents" / "skills" / "binary" / "asset.bin"
    claude_skill = tmp_path / ".claude" / "skills" / "binary" / "SKILL.md"
    claude_support_file = tmp_path / ".claude" / "skills" / "binary" / "asset.bin"
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: binary
description: Shared
---

# Binary
""",
        encoding="utf-8",
    )
    support_file.write_bytes(b"\x00\xffskill asset")
    claude_skill.write_text(agent_skill.read_text(encoding="utf-8"), encoding="utf-8")

    changed = sync_claude_skills(tmp_path, check=False)

    assert changed == [claude_support_file]
    assert claude_support_file.read_bytes() == b"\x00\xffskill asset"


def test_sync_claude_skills_rejects_orphaned_support_file(
    tmp_path: Path,
) -> None:
    agent_skill = tmp_path / ".agents" / "skills" / "work-brief" / "SKILL.md"
    claude_skill = tmp_path / ".claude" / "skills" / "work-brief" / "SKILL.md"
    orphaned_support_file = (
        tmp_path / ".claude" / "skills" / "work-brief" / "old_template.md"
    )
    agent_skill.parent.mkdir(parents=True)
    claude_skill.parent.mkdir(parents=True)
    agent_skill.write_text(
        """---
name: work-brief
description: Shared
---

# Work Brief
""",
        encoding="utf-8",
    )
    claude_skill.write_text(agent_skill.read_text(encoding="utf-8"), encoding="utf-8")
    orphaned_support_file.write_text("# Old Template\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="support files without matching"):
        sync_claude_skills(tmp_path, check=False)

    assert orphaned_support_file.exists()
