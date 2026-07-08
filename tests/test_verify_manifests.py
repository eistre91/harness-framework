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
    (manifests / "level-1.yml").write_text(
        """\
name: level-1
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


def test_validate_manifests_accepts_base_and_definition_source(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    docs = tmp_path / "docs"
    docs.mkdir()
    source = tmp_path / "templates" / "level-2" / "SPEC-MAP.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Spec Map\n", encoding="utf-8")
    (docs / "maturity-model.md").write_text(
        """\
# Maturity

## Level 2: Context Routing
""",
        encoding="utf-8",
    )
    (manifests / "level-1.yml").write_text(
        """\
name: level-1
description: Foundation.
assets: []
""",
        encoding="utf-8",
    )
    (manifests / "level-2.yml").write_text(
        """\
name: level-2
description: Context routing.
base: manifests/level-1.yml
level_definition_source: docs/maturity-model.md#level-2-context-routing
assets:
  - id: spec-map
    asset_type: installable
    source: templates/level-2/SPEC-MAP.md
    default_target: SPEC-MAP.md
    required: true
""",
        encoding="utf-8",
    )

    count, errors = module.validate_manifests(tmp_path)

    assert count == 2
    assert errors == []


def test_validate_manifests_reports_objective_drift(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    (manifests / "level-1.yml").write_text(
        """\
name: level-1
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


def test_validate_manifests_reports_contract_drift(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    docs = tmp_path / "docs"
    docs.mkdir()
    docs.joinpath("maturity-model.md").write_text(
        """\
# Maturity

## Level 2: Context Routing
""",
        encoding="utf-8",
    )
    (manifests / "level-2.yml").write_text(
        """\
name: level-2
description: Context routing.
base: manifests/missing.yml
level_definition_source: docs/maturity-model.md#missing-anchor
unknown_top_level: true
defer_by_default:
  - valid entry
  - false
assets:
  - id: malformed
    asset_type: required-file
    source: docs/maturity-model.md
    required: "yes"
    maturity: level-seven
    install_when: []
    adapt: explain the change
    unexpected_item_key: true
""",
        encoding="utf-8",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("unexpected key: unknown_top_level" in error for error in errors)
    assert any(
        "base path does not exist: manifests/missing.yml" in error for error in errors
    )
    assert any(
        "level_definition_source anchor does not exist" in error for error in errors
    )
    assert any(
        "defer_by_default[1] must be a non-empty string" in error
        for error in errors
    )
    assert any("asset_type must be one of" in error for error in errors)
    assert any("required must be a boolean" in error for error in errors)
    assert any("maturity must be one of" in error for error in errors)
    assert any("install_when must be a non-empty string" in error for error in errors)
    assert any("adapt must be a list" in error for error in errors)
    assert any("unexpected key: unexpected_item_key" in error for error in errors)


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
