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


def test_installer_sources_do_not_route_through_conceptual_docs() -> None:
    installer_sources = [ROOT / "docs/installer.md"]
    installer_sources.extend(path for path, _ in CHECKLISTS.values())
    for path in installer_sources:
        contents = read(path)
        assert "docs/implementation-guide.md" not in contents
        assert "docs/framework.md" not in contents


def test_each_capability_checklist_routes_to_authoritative_sources() -> None:
    for path, manifest in CHECKLISTS.values():
        contents = read(path)
        assert "docs/installer.md" in contents
        assert "docs/capability-map.md" in contents
        assert manifest in contents


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
