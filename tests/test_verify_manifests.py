from __future__ import annotations

import importlib.util
from pathlib import Path


def load_verify_manifests():
    script = Path(__file__).resolve().parents[1] / "scripts" / "verify-manifests.py"
    spec = importlib.util.spec_from_file_location("verify_manifests", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_manifests_accepts_existing_sources_and_targets(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    source = tmp_path / "templates" / "core" / "AGENTS.md"
    companion = tmp_path / "skills" / "core" / "sample" / "extra.md"
    read_before = tmp_path / "docs" / "principles.md"
    source.parent.mkdir(parents=True)
    companion.parent.mkdir(parents=True)
    read_before.parent.mkdir(parents=True)
    source.write_text("# Agents\n", encoding="utf-8")
    companion.write_text("# Extra\n", encoding="utf-8")
    read_before.write_text("# Principles\n", encoding="utf-8")
    (manifests / "level-0.yml").write_text(
        """\
name: level-0
assets:
  - id: agents-entrypoint
    asset_type: installable
    source: templates/core/AGENTS.md
    default_target: AGENTS.md
    required: true
    companion_files:
      - source: skills/core/sample/extra.md
        default_target: .agents/skills/sample/extra.md
    read_before_install:
      - docs/principles.md
""",
        encoding="utf-8",
    )

    count, errors = module.validate_manifests(tmp_path)

    assert count == 1
    assert errors == []


def test_validate_manifests_reports_objective_drift(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    (manifests / "level-0.yml").write_text(
        """\
name: level-0
assets:
  - id: duplicate
    asset_type: installable
    source: missing.md
    default_target: ../AGENTS.md
    required: true
  - id: duplicate
    asset_type: behavior
""",
        encoding="utf-8",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("source path does not exist: missing.md" in error for error in errors)
    assert any("invalid default_target: '../AGENTS.md'" in error for error in errors)
    assert any("duplicate id" in error for error in errors)


def test_validate_manifests_rejects_paths_that_escape_repo(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    outside = tmp_path.parent / "outside-manifest-source.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    (manifests / "optional-assets.yml").write_text(
        f"""\
name: optional-assets
assets:
  - id: escaped-source
    asset_type: installable
    source: ../{outside.name}
    default_target: AGENTS.md
adapters:
  - id: escaped-read-before
    asset_type: adapter
    source: scripts
    read_before_install:
      - /{outside.as_posix().lstrip('/')}
""",
        encoding="utf-8",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("source must not escape repo: ../outside-manifest-source.md" in error for error in errors)
    assert any("read_before_install[0] must be repo-relative" in error for error in errors)
