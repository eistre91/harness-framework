from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]

CHECKLISTS = {
    "Bounded Work": (
        ROOT / "docs/install/bounded-work.md",
        "manifests/bounded-work.yml",
    ),
    "Focused Context": (
        ROOT / "docs/install/focused-context.md",
        "manifests/focused-context.yml",
    ),
    "Agent Action Boundaries": (
        ROOT / "docs/install/agent-action-boundaries.md",
        "manifests/agent-action-boundaries.yml",
    ),
    "Maintainability Feedback": (
        ROOT / "docs/install/maintainability-feedback.md",
        "manifests/maintainability-feedback.yml",
    ),
}

NUMBERED_MODEL_MIGRATION = ROOT / "docs/install/migrate-numbered-model.md"

ACTIVE_INSTALLER_PATHS = (
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "docs/capability-map.md",
    ROOT / "docs/installer.md",
    ROOT / "docs/portable-assets.md",
    ROOT / "docs/platform-support.md",
    ROOT / "docs/platforms/codex.md",
    ROOT / "docs/platforms/claude-code.md",
    ROOT / "docs/hook-pattern.md",
    ROOT / "templates/profile/docs/harness/README.md",
    ROOT / "templates/profile/docs/harness/fit-proposal.md",
)

RECONCILED_CONCEPTUAL_AND_INSTALLABLE_PATHS = (
    ROOT / "docs/principles.md",
    ROOT / "docs/framework.md",
    ROOT / "docs/implementation-guide.md",
    ROOT / "templates/core/docs/harness/README.md",
    ROOT / "templates/core/docs/harness/fit-proposal.md",
    ROOT / "templates/maintainability-feedback/docs/harness/maintainability.md",
    ROOT / "skills/core/harness-maintainability/SKILL.md",
)

LEGACY_INSTALLER_CONTRACT_TERMS = (
    "current stage",
    "stage proposal",
    "stage handoff",
    "installation mode:",
    "asset completeness",
    "behavioral completeness",
    "current numbered checklist",
    "target maturity behavior",
    "overlay mode",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_capability_cutover_sources_are_current_and_transition_is_resolved() -> None:
    capability_map = " ".join(read(ROOT / "docs/capability-map.md").split())
    decision = " ".join(
        read(
            ROOT / "docs/adr/0001-replace-maturity-levels-with-capability-map.md"
        ).split()
    )
    installer = " ".join(read(ROOT / "docs/installer.md").split())
    transition = " ".join(
        read(ROOT / "docs/capability-map-transition.md").split()
    )
    todo = " ".join(read(ROOT / "TODO.md").split())

    assert "Status: active capability model and installer taxonomy" in capability_map
    assert "framework documentation transition is still in progress" not in capability_map
    assert "The framework replaced its numbered maturity taxonomy" in decision
    assert "numbered model remains the active installer contract" not in decision
    assert "remaining framework-doc reconciliation" not in installer
    assert "Remaining Implementation Decisions" not in transition
    assert "Resolved: Capability Profiles Replaced Maturity Levels" in todo
    assert "Deferred: Maturity Levels Versus Capability Profiles" not in todo


def test_installer_owns_one_profile_change_workflow() -> None:
    installer = " ".join(read(ROOT / "docs/installer.md").split())

    required_contract = (
        "one Profile Change at a time",
        "the only eligible addition is Bounded Work",
        "pause the selected change",
        "Offer one missing prerequisite as a separate current Profile Change",
        "Reject the removal while any such dependent remains current",
        "inspect every existing always-loaded agent instruction surface",
        "leave the Current Harness Profile unchanged",
        "recommends stopping",
    )

    for phrase in required_contract:
        assert phrase in installer


def test_numbered_model_migration_is_routed_as_documentation_only() -> None:
    installer = " ".join(read(ROOT / "docs/installer.md").split())
    migration = " ".join(read(NUMBERED_MODEL_MIGRATION).split())
    readme = " ".join(read(ROOT / "README.md").split())
    profile = " ".join(
        read(ROOT / "templates/profile/docs/harness/README.md").split()
    )

    assert "`docs/install/migrate-numbered-model.md`" in installer
    assert "one-time documentation migration" in installer
    assert "without authorizing a capability installation" in installer
    assert "follow the installer's no-profile routing" in readme
    assert "migrate an existing numbered-model installation" in readme

    required_contract = (
        "currently installed behavior and evidence",
        "Inspect the actual installed surfaces",
        "Level 1 | Bounded Work",
        "Level 2 | Focused Context",
        "Level 3 | Agent Action Boundaries",
        "Level 4 | Maintainability Feedback",
        "Preserve exact control and sensor scope",
        "propose `No installed Harness Profile`",
        "wait for explicit approval before editing",
        "no harness behavior or capability realization will change",
        "kept distinct from the original installation provenance",
        "Do not rewrite an old stage proposal",
        "Recommend stopping",
    )

    for phrase in required_contract:
        assert phrase in migration

    assert "Capability Map and profile contract version or commit" in profile
    assert "Initial harness source version or commit" in profile


def test_active_installer_sources_do_not_publish_legacy_stage_contract() -> None:
    active_paths = list(ACTIVE_INSTALLER_PATHS)
    active_paths.extend(path for path, _ in CHECKLISTS.values())

    for path in active_paths:
        contents = read(path).lower()
        taxonomy_text = contents.replace("docs/level-5-orchestration.md", "")
        assert (
            re.search(r"\blevel-[0-9]+\b|\blevel [0-9]+\b", taxonomy_text)
            is None
        )
        assert (
            re.search(
                r"\b(canonical|starter|overlay) (install|installation|mode)\b",
                contents,
            )
            is None
        )
        for term in LEGACY_INSTALLER_CONTRACT_TERMS:
            assert term not in contents, f"{path.relative_to(ROOT)} contains {term!r}"

    active_manifests = (
        ROOT / "manifests/bounded-work.yml",
        ROOT / "manifests/focused-context.yml",
        ROOT / "manifests/agent-action-boundaries.yml",
        ROOT / "manifests/maintainability-feedback.yml",
        ROOT / "manifests/optional-assets.yml",
    )
    for path in active_manifests:
        contents = read(path).lower()
        assert "overlay mode" not in contents


def test_reconciled_conceptual_docs_do_not_compete_with_installer_sources() -> None:
    installer_sources = [ROOT / "docs/installer.md"]
    installer_sources.extend(path for path, _ in CHECKLISTS.values())
    for path in installer_sources:
        contents = read(path)
        assert "docs/maturity-model.md" not in contents
        assert "docs/implementation-guide.md" not in contents
        assert "docs/framework.md" not in contents

    maturity_model = " ".join(read(ROOT / "docs/maturity-model.md").split())
    implementation_guide = " ".join(read(ROOT / "docs/implementation-guide.md").split())
    framework = " ".join(read(ROOT / "docs/framework.md").split())
    assert "retired numbered model" in maturity_model
    assert "not an active installer taxonomy" in maturity_model
    assert "map, not an installation checklist or a second procedure" in implementation_guide
    assert "Status: active conceptual framework" in framework


def test_reconciled_conceptual_and_installable_sources_do_not_emit_legacy_taxonomy() -> None:
    for path in RECONCILED_CONCEPTUAL_AND_INSTALLABLE_PATHS:
        contents = read(path).lower()
        taxonomy_text = contents.replace(
            "docs/adr/0001-replace-maturity-levels-with-capability-map.md", ""
        )
        assert re.search(r"\blevel-[0-9]+\b|\blevel [0-9]+\b", taxonomy_text) is None
        assert "maturity" not in taxonomy_text
        assert "completeness" not in taxonomy_text
        for term in LEGACY_INSTALLER_CONTRACT_TERMS:
            assert term not in taxonomy_text, (
                f"{path.relative_to(ROOT)} contains {term!r}"
            )


def test_each_capability_checklist_crosses_the_same_installer_seam() -> None:
    for capability, (path, manifest) in CHECKLISTS.items():
        contents = read(path)
        assert capability in contents
        assert "`docs/installer.md`" in contents
        assert "`docs/capability-map.md`" in contents
        assert f"`{manifest}`" in contents
        assert "Current Harness Profile" in contents
        assert "failed or incomplete validation" in contents
        assert "Do not inspect another capability" in contents


def test_bootstrap_routes_only_to_capability_checklists() -> None:
    bootstrap = yaml.safe_load(read(ROOT / "manifests/bootstrap.yml"))
    sources = {asset["source"] for asset in bootstrap["assets"]}
    checklist_entries = [
        asset
        for asset in bootstrap["assets"]
        if asset["id"].endswith("-installer-checklist")
    ]

    assert {asset["source"] for asset in checklist_entries} == {
        str(path.relative_to(ROOT)) for path, _ in CHECKLISTS.values()
    }
    assert all("level-" not in asset["id"] for asset in checklist_entries)
    assert "docs/capability-map.md" in sources
    assert "docs/maturity-model.md" not in sources
    assert "docs/framework.md" not in sources
    assert "docs/implementation-guide.md" not in sources


def test_bounded_work_manifest_activates_profile_contracts() -> None:
    bounded_work = yaml.safe_load(read(ROOT / "manifests/bounded-work.yml"))
    sources = {
        asset["id"]: asset.get("source") for asset in bounded_work["assets"]
    }

    assert sources["harness-doc-index"] == (
        "templates/profile/docs/harness/README.md"
    )
    assert sources["harness-fit-proposal-record"] == (
        "templates/profile/docs/harness/fit-proposal.md"
    )

    for source in (
        "templates/profile/docs/harness/README.md",
        "templates/profile/docs/harness/fit-proposal.md",
    ):
        assert "Framework migration note" not in read(ROOT / source)
