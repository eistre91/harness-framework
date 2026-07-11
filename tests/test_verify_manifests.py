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


def write_file(root: Path, relative_path: str, content: str = "# Fixture\n") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_manifest(root: Path, name: str, body: str) -> Path:
    path = root / "manifests" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            (
                f"name: {name.removesuffix('.yml')}",
                "description: Fixture manifest.",
                "install_policy: Validate this fixture only.",
                body.rstrip(),
                "",
            )
        ),
        encoding="utf-8",
    )
    return path


def behavior_item(item_id: str) -> str:
    return f"""\
  - id: {item_id}
    asset_type: behavior
    required: true
    satisfy_by:
      - Satisfy {item_id}.
"""


def installable_item(
    item_id: str,
    source: str,
    target: str,
    *,
    selection: str = "required: true",
    companion: str = "",
) -> str:
    companion_block = f"\n    companion_files:\n{companion}" if companion else ""
    return f"""\
  - id: {item_id}
    asset_type: installable
    source: {source}
    default_target: {target}
    {selection}{companion_block}
"""


def test_validate_manifests_accepts_existing_sources_and_targets(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "templates/core/AGENTS.md", "# Agents\n")
    write_file(tmp_path, "skills/core/sample/extra.md", "# Extra\n")
    write_file(tmp_path, "docs/principles.md", "# Principles\n")
    write_manifest(
        tmp_path,
        "level-1.yml",
        """\
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
    )

    count, errors = module.validate_manifests(tmp_path)

    assert count == 1
    assert errors == []


def test_validate_manifests_accepts_prerequisite_and_definition_source(
    tmp_path: Path,
) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "templates/level-2/SPEC-MAP.md", "# Spec Map\n")
    write_file(
        tmp_path,
        "docs/maturity-model.md",
        "# Maturity\n\n## Level 2: Context Routing\n",
    )
    write_manifest(tmp_path, "level-1.yml", f"assets:\n{behavior_item('foundation')}")
    write_manifest(
        tmp_path,
        "level-2.yml",
        f"""\
prerequisite_manifest: manifests/level-1.yml
level_definition_source: docs/maturity-model.md#level-2-context-routing
assets:
{installable_item('spec-map', 'templates/level-2/SPEC-MAP.md', 'SPEC-MAP.md')}
""",
    )

    count, errors = module.validate_manifests(tmp_path)

    assert count == 2
    assert errors == []


def test_production_manifests_validate_and_keep_count_of_five() -> None:
    module = load_verify_manifests()

    count, errors = module.validate_manifests(module.ROOT)

    assert count == 5
    assert errors == []


def test_empty_mapping_requires_metadata_and_local_asset(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    (manifests / "empty.yml").write_text("{}\n", encoding="utf-8")

    _count, errors = module.validate_manifests(tmp_path)

    assert any("missing name" in error for error in errors)
    assert any("missing description" in error for error in errors)
    assert any("missing install_policy" in error for error in errors)
    assert any("must own at least one entry" in error for error in errors)


def test_empty_top_level_metadata_values_are_rejected(tmp_path: Path) -> None:
    module = load_verify_manifests()
    manifests = tmp_path / "manifests"
    manifests.mkdir()
    for field in ("name", "description", "install_policy"):
        values = {
            "name": "fixture",
            "description": "Fixture manifest.",
            "install_policy": "Validate this fixture.",
        }
        values[field] = '""'
        (manifests / f"empty-{field}.yml").write_text(
            f"name: {values['name']}\n"
            f"description: {values['description']}\n"
            f"install_policy: {values['install_policy']}\n"
            f"assets:\n{behavior_item(field)}",
            encoding="utf-8",
        )

    _count, errors = module.validate_manifests(tmp_path)

    for field in ("name", "description", "install_policy"):
        assert any(
            f"manifest: {field} must be a non-empty string" in error
            for error in errors
        )


def test_manifest_with_only_grouping_lists_is_not_valid(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_manifest(
        tmp_path,
        "grouping-only.yml",
        """\
defer_by_default:
  - later
excluded_from_level_asset_boundary:
  - also later
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("must own at least one entry" in error for error in errors)


def test_validate_manifests_reports_objective_drift(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_manifest(
        tmp_path,
        "level-1.yml",
        """\
assets:
  - id: duplicate
    asset_type: installable
    source: missing.md
    default_target: ../AGENTS.md
    required: true
  - id: duplicate
    asset_type: behavior
    required: true
    satisfy_by:
      - Explain the behavior.
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("source path does not exist: missing.md" in error for error in errors)
    assert any("invalid default_target: '../AGENTS.md'" in error for error in errors)
    assert any("duplicate id" in error for error in errors)


def test_validate_manifests_reports_contract_drift(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "docs/maturity-model.md", "# Maturity\n## Level 2: Context Routing\n")
    write_manifest(
        tmp_path,
        "level-2.yml",
        """\
prerequisite_manifest: manifests/missing.yml
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
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("unexpected key: unknown_top_level" in error for error in errors)
    assert any(
        "prerequisite_manifest path does not exist: manifests/missing.yml" in error
        for error in errors
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


def test_base_is_rejected_after_prerequisite_rename(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_manifest(tmp_path, "level-1.yml", f"assets:\n{behavior_item('foundation')}")
    write_manifest(
        tmp_path,
        "level-2.yml",
        f"base: manifests/level-1.yml\nassets:\n{behavior_item('context')}\n",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("unexpected key: base" in error for error in errors)


def test_selection_and_section_boundaries_are_enforced(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "docs/bootstrap.md")
    write_file(tmp_path, "templates/valid.md")
    write_manifest(
        tmp_path,
        "invalid.yml",
        """\
assets:
  - id: wrong-section
    asset_type: optional-reference
    install_when: A condition.
    notes: It has notes.
  - id: missing-selection
    asset_type: behavior
    satisfy_by:
      - Explain it.
  - id: required-false
    asset_type: behavior
    required: false
    satisfy_by:
      - Explain it.
  - id: multiple-selection
    asset_type: behavior
    required: true
    install_when: Also selected.
    satisfy_by:
      - Explain it.
  - id: bootstrap-selection
    asset_type: bootstrap
    source: docs/bootstrap.md
    required_when: This is not a bootstrap selector.
adapters:
  - id: wrong-adapter-section
    asset_type: behavior
    install_when: A condition.
    satisfy_by:
      - Explain it.
common_starter_pull_ins:
  - id: wrong-common-section
    asset_type: installable
    source: templates/valid.md
    default_target: valid.md
    install_when: A condition.
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("assets entries must use one of" in error for error in errors)
    assert any("must define exactly one selection field" in error for error in errors)
    assert any("required: false is not a valid selection" in error for error in errors)
    assert any("selection fields are mutually exclusive" in error for error in errors)
    assert any("not permitted for asset_type 'bootstrap'" in error for error in errors)
    assert any("adapters entries must use one of" in error for error in errors)
    assert any("common_starter_pull_ins entries must use one of" in error for error in errors)


def test_type_specific_required_fields_are_enforced(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "templates/present.md")
    write_file(tmp_path, "adapters/present")
    write_file(tmp_path, "docs/read-first.md")
    write_manifest(
        tmp_path,
        "invalid.yml",
        """\
assets:
  - id: no-installable-source
    asset_type: installable
    default_target: missing-source.md
    required_when: Needed.
  - id: no-installable-target
    asset_type: installable
    source: templates/present.md
    install_when: Eligible.
  - id: no-behavior-guidance
    asset_type: behavior
    required: true
  - id: empty-supplemental-guidance
    asset_type: installable
    source: templates/present.md
    default_target: supplemental.md
    install_when: Eligible.
    satisfy_by: []
    read_before_install: []
  - id: invalid-companions
    asset_type: behavior
    required: true
    satisfy_by:
      - Explain it.
    companion_files: []
common_starter_pull_ins:
  - id: no-reference-notes
    asset_type: optional-reference
    install_when: Eligible.
adapters:
  - id: no-adapter-source-or-guidance
    asset_type: adapter
    install_when: Eligible.
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("no-installable-source" in error and "missing source" in error for error in errors)
    assert any("no-installable-target" in error and "missing default_target" in error for error in errors)
    assert any("no-behavior-guidance" in error and "missing satisfy_by" in error for error in errors)
    assert any("satisfy_by must be a non-empty list" in error for error in errors)
    assert any("read_before_install must be a non-empty list" in error for error in errors)
    assert any("companion_files is only valid on installable" in error for error in errors)
    assert any("companion_files must be a non-empty list" in error for error in errors)
    assert any("no-reference-notes" in error and "missing notes" in error for error in errors)
    assert any("no-adapter-source-or-guidance" in error and "missing source" in error for error in errors)
    assert any("no-adapter-source-or-guidance" in error and "missing read_before_install" in error for error in errors)


def test_companion_files_require_source_and_target(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "templates/present.md")
    write_manifest(
        tmp_path,
        "invalid.yml",
        f"""\
assets:
{installable_item(
    "bad-companion",
    "templates/present.md",
    "present.md",
    companion="      - source: missing-companion.md\n",
)}
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("companion_files[0]" in error and "path does not exist" in error for error in errors)
    assert any("companion_files[0]" in error and "missing default_target" in error for error in errors)


def test_two_manifest_prerequisite_cycle_reports_ordered_path(tmp_path: Path) -> None:
    module = load_verify_manifests()
    a_path = write_manifest(
        tmp_path,
        "a.yml",
        f"prerequisite_manifest: manifests/b.yml\nassets:\n{behavior_item('a')}\n",
    )
    b_path = write_manifest(
        tmp_path,
        "b.yml",
        f"prerequisite_manifest: manifests/a.yml\nassets:\n{behavior_item('b')}\n",
    )

    _count, errors = module.validate_manifests(tmp_path)

    cycle_errors = [error for error in errors if "prerequisite cycle" in error]
    assert len(cycle_errors) == 1
    assert (
        f"prerequisite cycle: {a_path} -> {b_path} -> {a_path}"
        in cycle_errors[0]
    )


def test_long_prerequisite_cycle_reports_all_manifests(tmp_path: Path) -> None:
    module = load_verify_manifests()
    paths = {}
    for current, prerequisite in (("a", "b"), ("b", "c"), ("c", "a")):
        paths[current] = write_manifest(
            tmp_path,
            f"{current}.yml",
            f"prerequisite_manifest: manifests/{prerequisite}.yml\nassets:\n"
            f"{behavior_item(current)}\n",
        )

    _count, errors = module.validate_manifests(tmp_path)

    cycle_errors = [error for error in errors if "prerequisite cycle" in error]
    assert len(cycle_errors) == 1
    assert (
        f"prerequisite cycle: {paths['a']} -> {paths['b']} -> "
        f"{paths['c']} -> {paths['a']}"
        in cycle_errors[0]
    )


def test_self_and_missing_prerequisites_keep_clear_diagnostics(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_manifest(
        tmp_path,
        "self.yml",
        f"prerequisite_manifest: manifests/self.yml\nassets:\n{behavior_item('self')}\n",
    )
    write_manifest(
        tmp_path,
        "missing.yml",
        f"prerequisite_manifest: manifests/not-present.yml\nassets:\n{behavior_item('missing')}\n",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any("must not reference itself" in error for error in errors)
    assert any("path does not exist: manifests/not-present.yml" in error for error in errors)


def test_transitive_duplicate_id_and_canonical_target_collisions_fail(tmp_path: Path) -> None:
    module = load_verify_manifests()
    for source in ("templates/grandparent.md", "templates/middle.md", "templates/current.md"):
        write_file(tmp_path, source)
    write_manifest(
        tmp_path,
        "grandparent.yml",
        f"assets:\n{installable_item('shared-id', 'templates/grandparent.md', 'grandparent.md')}\n",
    )
    write_manifest(
        tmp_path,
        "middle.yml",
        f"prerequisite_manifest: manifests/grandparent.yml\nassets:\n"
        f"{installable_item('middle-id', 'templates/middle.md', 'middle.md')}\n",
    )
    write_manifest(
        tmp_path,
        "current.yml",
        f"prerequisite_manifest: manifests/middle.yml\nassets:\n"
        f"{installable_item('shared-id', 'templates/current.md', './grandparent.md')}\n",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any(
        "duplicate id 'shared-id'" in error
        and "grandparent.yml" in error
        and "current.yml" in error
        for error in errors
    )
    assert any(
        "collision for 'grandparent.md'" in error
        and "grandparent.yml" in error
        and "current.yml" in error
        and error.count("assets 'shared-id'") == 2
        for error in errors
    )


def test_local_and_companion_target_collisions_fail_even_for_same_source(
    tmp_path: Path,
) -> None:
    module = load_verify_manifests()
    write_file(tmp_path, "templates/shared.md")
    write_manifest(
        tmp_path,
        "local.yml",
        """\
assets:
  - id: first
    asset_type: installable
    source: templates/shared.md
    default_target: AGENTS.md
    required: true
    companion_files:
      - source: templates/shared.md
        default_target: docs/shared.md
  - id: second
    asset_type: installable
    source: templates/shared.md
    default_target: ./AGENTS.md
    required: true
  - id: third
    asset_type: installable
    source: templates/shared.md
    default_target: docs/shared.md
    required: true
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any(
        "collision for 'AGENTS.md'" in error
        and "assets 'first'" in error
        and "assets 'second'" in error
        for error in errors
    )
    assert any(
        "collision for 'docs/shared.md'" in error
        and "assets 'first' companion_files[0]" in error
        and "assets 'third'" in error
        for error in errors
    )


def test_same_id_in_unrelated_manifests_is_valid(tmp_path: Path) -> None:
    module = load_verify_manifests()
    write_manifest(tmp_path, "first.yml", f"assets:\n{behavior_item('shared')}\n")
    write_manifest(tmp_path, "second.yml", f"assets:\n{behavior_item('shared')}\n")

    count, errors = module.validate_manifests(tmp_path)

    assert count == 2
    assert errors == []


def test_validate_manifests_rejects_paths_that_escape_repo(tmp_path: Path) -> None:
    module = load_verify_manifests()
    outside = tmp_path.parent / "outside-manifest-source.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    write_manifest(
        tmp_path,
        "optional-assets.yml",
        f"""\
assets:
  - id: escaped-source
    asset_type: installable
    source: ../{outside.name}
    default_target: AGENTS.md
    install_when: Eligible.
adapters:
  - id: escaped-read-before
    asset_type: adapter
    source: scripts
    install_when: Eligible.
    read_before_install:
      - /{outside.as_posix().lstrip('/')}
""",
    )

    _count, errors = module.validate_manifests(tmp_path)

    assert any(
        "source must not escape repo: ../outside-manifest-source.md" in error
        for error in errors
    )
    assert any(
        "read_before_install[0] must be repo-relative" in error for error in errors
    )
