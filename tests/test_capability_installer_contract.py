from pathlib import Path

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_capability_sources_are_current() -> None:
    capability_map = " ".join(read(ROOT / "docs/capability-map.md").split())
    installer = " ".join(read(ROOT / "docs/installer.md").split())
    coordination = " ".join(
        read(ROOT / "docs/multi-work-coordination.md").split()
    )

    assert "Status: active capability model and installer taxonomy" in capability_map
    assert "one Profile Change at a time" in installer
    assert "future-facing and non-authoritative" in coordination
    assert "implies no installable package" in coordination


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


def test_conceptual_docs_do_not_compete_with_installer_sources() -> None:
    installer_sources = [ROOT / "docs/installer.md"]
    installer_sources.extend(path for path, _ in CHECKLISTS.values())
    for path in installer_sources:
        contents = read(path)
        assert "docs/implementation-guide.md" not in contents
        assert "docs/framework.md" not in contents

    implementation_guide = " ".join(read(ROOT / "docs/implementation-guide.md").split())
    framework = " ".join(read(ROOT / "docs/framework.md").split())
    assert "map, not an installation checklist or a second procedure" in implementation_guide
    assert "Status: active conceptual framework" in framework


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
    assert "docs/capability-map.md" in sources
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
