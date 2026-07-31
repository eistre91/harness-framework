#!/usr/bin/env python3
"""Validate harness asset manifests."""

from __future__ import annotations

import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print(
        "PyYAML is required. Run 'uv sync --locked' from the repository root.",
        file=sys.stderr,
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
ASSET_SECTIONS = ("assets", "adapters", "common_starter_pull_ins")
ALLOWED_TOP_LEVEL_KEYS = {
    "name",
    "description",
    "install_policy",
    "dependency_manifests",
    "capability_definition_source",
    "assets",
    "adapters",
    "common_starter_pull_ins",
    "defer_by_default",
    "excluded_from_capability_scope",
}
ALLOWED_ITEM_KEYS = {
    "id",
    "asset_type",
    "source",
    "default_target",
    "required",
    "required_when",
    "install_when",
    "use_when",
    "supports_capability_domains",
    "category",
    "read_before_install",
    "companion_files",
    "satisfy_by",
    "adapt",
    "notes",
}
ALLOWED_COMPANION_KEYS = {"source", "default_target"}
ALLOWED_ASSET_TYPES = {
    "adapter",
    "behavior",
    "bootstrap",
    "installable",
    "optional-reference",
}
SECTION_ALLOWED_ASSET_TYPES = {
    "assets": {"bootstrap", "installable", "behavior"},
    "adapters": {"adapter"},
    "common_starter_pull_ins": {"optional-reference", "behavior"},
}
SELECTION_FIELDS = ("required", "required_when", "install_when", "use_when")
ITEM_TEXT_FIELDS = ("required_when", "install_when", "use_when", "category", "notes")
ITEM_LIST_FIELDS = ("adapt", "satisfy_by")
TOP_LEVEL_LIST_FIELDS = ("defer_by_default", "excluded_from_capability_scope")
CAPABILITY_MAP_PATH = PurePosixPath("docs/capability-map.md")


class AssetOwner:
    def __init__(self, manifest: Path, section: str, asset_id: str) -> None:
        self.manifest = manifest
        self.section = section
        self.asset_id = asset_id


class OutputOwner:
    def __init__(
        self,
        manifest: Path,
        section: str,
        asset_id: str,
        companion_index: int | None = None,
    ) -> None:
        self.manifest = manifest
        self.section = section
        self.asset_id = asset_id
        self.companion_index = companion_index


def manifest_files(root: Path) -> Iterable[Path]:
    manifests_dir = root / "manifests"
    if not manifests_dir.exists():
        return []
    return sorted(manifests_dir.glob("*.yml"))


def load_manifest(path: Path) -> tuple[Any, list[str]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except yaml.YAMLError as exc:
        return None, [f"{path}: YAML parse error: {format_yaml_error(exc)}"]


def format_yaml_error(exc: yaml.YAMLError) -> str:
    mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
    if mark is not None:
        return f"line {mark.line + 1}, column {mark.column + 1}: {exc}"
    return str(exc)


def item_label(section: str, item: Any) -> str:
    if isinstance(item, dict) and item.get("id"):
        return f"{section} {item['id']!r}"
    return section


def is_portable_target(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value.startswith("/"):
        return False

    parts = PurePosixPath(value).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return False

    return True


def validate_portable_repo_path(
    manifest_path: Path,
    label: str,
    key: str,
    value: Any,
) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{manifest_path}: {label}: {key} must be a non-empty string"]
    if value.startswith("/"):
        return [f"{manifest_path}: {label}: {key} must be repo-relative: {value}"]

    parts = PurePosixPath(value).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return [f"{manifest_path}: {label}: {key} must not escape repo: {value}"]

    return []


def validate_text_field(
    manifest_path: Path,
    label: str,
    key: str,
    value: Any,
) -> list[str]:
    if isinstance(value, str) and value:
        return []
    return [f"{manifest_path}: {label}: {key} must be a non-empty string"]


def validate_string_list(
    manifest_path: Path,
    label: str,
    key: str,
    value: Any,
    *,
    non_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        return [f"{manifest_path}: {label}: {key} must be a list"]

    errors = []
    if non_empty and not value:
        errors.append(
            f"{manifest_path}: {label}: {key} must be a non-empty list"
        )

    for index, entry in enumerate(value):
        if not isinstance(entry, str) or not entry:
            errors.append(
                f"{manifest_path}: {label}: {key}[{index}] "
                "must be a non-empty string"
            )

    return errors


def markdown_anchor(value: str) -> str:
    anchor = value.strip().lower()
    anchor = re.sub(r"`([^`]*)`", r"\1", anchor)
    anchor = re.sub(r"[^a-z0-9 -]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    return anchor.strip("-")


def markdown_headings(path: Path) -> dict[str, str]:
    headings = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip()
        if heading:
            headings[markdown_anchor(heading)] = heading
    return headings


def validate_markdown_reference(
    root: Path,
    manifest_path: Path,
    key: str,
    value: Any,
) -> list[str]:
    label = "manifest"
    if not isinstance(value, str) or not value:
        return [f"{manifest_path}: {label}: {key} must be a non-empty string"]

    path_part, separator, anchor = value.partition("#")
    path_errors = validate_portable_repo_path(manifest_path, label, key, path_part)
    if path_errors:
        return path_errors

    resolved = root / path_part
    if not resolved.exists():
        return [f"{manifest_path}: {label}: {key} path does not exist: {path_part}"]

    if separator and not anchor:
        return [f"{manifest_path}: {label}: {key} anchor must be non-empty: {value}"]

    if anchor and anchor not in markdown_headings(resolved):
        return [f"{manifest_path}: {label}: {key} anchor does not exist: {value}"]

    return []


def validate_dependency_manifests(
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
) -> list[str]:
    key = "dependency_manifests"
    if key not in manifest:
        return []

    value = manifest[key]
    if not isinstance(value, list):
        return [f"{manifest_path}: manifest: {key} must be a list"]

    errors = []
    seen: set[str] = set()
    for index, entry in enumerate(value):
        entry_key = f"{key}[{index}]"
        path_errors = validate_portable_repo_path(
            manifest_path,
            "manifest",
            entry_key,
            entry,
        )
        if path_errors:
            errors.extend(path_errors)
            continue
        if not isinstance(entry, str):
            continue
        if entry in seen:
            errors.append(
                f"{manifest_path}: manifest: {entry_key} duplicates {entry!r}"
            )
            continue
        seen.add(entry)
        if not entry.startswith("manifests/") or not entry.endswith(".yml"):
            errors.append(
                f"{manifest_path}: manifest: {entry_key} must reference a "
                f"manifest yml: {entry}"
            )
            continue
        candidate = (root / entry).resolve()
        if not (root / entry).exists():
            errors.append(
                f"{manifest_path}: manifest: {entry_key} path does not exist: {entry}"
            )
        elif candidate == manifest_path.resolve():
            errors.append(
                f"{manifest_path}: manifest: {entry_key} must not reference "
                f"itself: {entry}"
            )

    return errors


def validate_source_path(
    root: Path,
    manifest_path: Path,
    section: str,
    item: Any,
    key: str,
    *,
    required: bool = False,
) -> list[str]:
    if not isinstance(item, dict):
        return []

    label = item_label(section, item)
    if key not in item:
        if required:
            return [f"{manifest_path}: {label}: missing {key}"]
        return []

    value = item[key]
    path_errors = validate_portable_repo_path(manifest_path, label, key, value)
    if path_errors:
        return path_errors

    if not (root / value).exists():
        return [f"{manifest_path}: {label}: {key} path does not exist: {value}"]

    return []


def validate_default_target(
    manifest_path: Path,
    section: str,
    item: Any,
    *,
    required: bool,
) -> list[str]:
    if not isinstance(item, dict):
        return []

    if "default_target" not in item:
        if required:
            label = item_label(section, item)
            return [f"{manifest_path}: {label}: missing default_target"]
        return []

    value = item["default_target"]
    if is_portable_target(value):
        return []

    label = item_label(section, item)
    return [f"{manifest_path}: {label}: invalid default_target: {value!r}"]


def validate_read_before_install(
    root: Path,
    manifest_path: Path,
    section: str,
    item: Any,
    *,
    required: bool = False,
) -> list[str]:
    if not isinstance(item, dict):
        return []

    label = item_label(section, item)
    if "read_before_install" not in item:
        if required:
            return [f"{manifest_path}: {label}: missing read_before_install"]
        return []

    value = item["read_before_install"]
    if not isinstance(value, list):
        return [f"{manifest_path}: {label}: read_before_install must be a list"]

    errors = []
    if not value:
        errors.append(
            f"{manifest_path}: {label}: read_before_install must be a non-empty list"
        )

    for index, entry in enumerate(value):
        entry_key = f"read_before_install[{index}]"
        path_errors = validate_portable_repo_path(
            manifest_path,
            label,
            entry_key,
            entry,
        )
        if path_errors:
            errors.extend(path_errors)
            continue
        if not (root / entry).exists():
            errors.append(
                f"{manifest_path}: {label}: {entry_key} path does not exist: {entry}"
            )

    return errors


def validate_companion_files(
    root: Path,
    manifest_path: Path,
    section: str,
    asset: Any,
) -> list[str]:
    if not isinstance(asset, dict) or "companion_files" not in asset:
        return []

    label = item_label(section, asset)
    companions = asset["companion_files"]
    errors = []
    if asset.get("asset_type") != "installable":
        errors.append(
            f"{manifest_path}: {label}: companion_files is only valid on installable entries"
        )

    if not isinstance(companions, list):
        errors.append(f"{manifest_path}: {label}: companion_files must be a list")
        return errors

    if not companions:
        errors.append(
            f"{manifest_path}: {label}: companion_files must be a non-empty list"
        )

    for index, companion in enumerate(companions):
        companion_label = f"{label} companion_files[{index}]"
        if not isinstance(companion, dict):
            errors.append(f"{manifest_path}: {companion_label} must be a mapping")
            continue

        unexpected_keys = sorted(set(companion) - ALLOWED_COMPANION_KEYS)
        for key in unexpected_keys:
            errors.append(
                f"{manifest_path}: {companion_label}: unexpected key: {key}"
            )

        errors.extend(
            validate_source_path(
                root,
                manifest_path,
                companion_label,
                companion,
                "source",
                required=True,
            )
        )
        errors.extend(
            validate_default_target(
                manifest_path,
                companion_label,
                companion,
                required=True,
            )
        )

    return errors


def validate_selection(
    manifest_path: Path,
    section: str,
    item: dict[str, Any],
) -> list[str]:
    asset_type = item.get("asset_type")
    if asset_type not in ALLOWED_ASSET_TYPES:
        return []

    if asset_type == "bootstrap":
        permitted = ("use_when",)
    elif asset_type in {"installable", "behavior"}:
        permitted = ("required", "required_when", "install_when")
    else:
        permitted = ("install_when",)

    label = item_label(section, item)
    present = [key for key in SELECTION_FIELDS if key in item]
    errors = []
    if len(present) == 0:
        errors.append(
            f"{manifest_path}: {label}: must define exactly one selection field "
            f"from {permitted}"
        )
    elif len(present) > 1:
        errors.append(
            f"{manifest_path}: {label}: selection fields are mutually exclusive; "
            f"found {present}"
        )

    disallowed = [key for key in present if key not in permitted]
    if disallowed:
        errors.append(
            f"{manifest_path}: {label}: selection field(s) {disallowed} "
            f"not permitted for asset_type {asset_type!r}"
        )

    if item.get("required") is False:
        errors.append(
            f"{manifest_path}: {label}: required: false is not a valid selection"
        )

    return errors


def validate_item_contract(
    manifest_path: Path,
    section: str,
    item: dict[str, Any],
) -> list[str]:
    label = item_label(section, item)
    errors = []

    unexpected_keys = sorted(set(item) - ALLOWED_ITEM_KEYS)
    for key in unexpected_keys:
        errors.append(f"{manifest_path}: {label}: unexpected key: {key}")

    asset_type = item.get("asset_type")
    if asset_type not in ALLOWED_ASSET_TYPES:
        errors.append(
            f"{manifest_path}: {label}: asset_type must be one of "
            f"{sorted(ALLOWED_ASSET_TYPES)}"
        )

    if asset_type in ALLOWED_ASSET_TYPES:
        allowed_types = SECTION_ALLOWED_ASSET_TYPES[section]
        if asset_type not in allowed_types:
            errors.append(
                f"{manifest_path}: {label}: {section} entries must use one of "
                f"{sorted(allowed_types)}"
            )

    if "supports_capability_domains" in item:
        errors.extend(
            validate_string_list(
                manifest_path,
                label,
                "supports_capability_domains",
                item["supports_capability_domains"],
            )
        )
        domains = item["supports_capability_domains"]
        if isinstance(domains, list):
            seen_domains: set[str] = set()
            for index, domain in enumerate(domains):
                if not isinstance(domain, str) or not domain:
                    continue
                if domain in seen_domains:
                    errors.append(
                        f"{manifest_path}: {label}: "
                        f"supports_capability_domains[{index}] duplicates {domain!r}"
                    )
                seen_domains.add(domain)

    if "required" in item and not isinstance(item["required"], bool):
        errors.append(f"{manifest_path}: {label}: required must be a boolean")

    for key in ITEM_TEXT_FIELDS:
        if key in item:
            errors.extend(validate_text_field(manifest_path, label, key, item[key]))

    for key in ITEM_LIST_FIELDS:
        if key in item:
            errors.extend(
                validate_string_list(
                    manifest_path,
                    label,
                    key,
                    item[key],
                    non_empty=key == "satisfy_by",
                )
            )

    errors.extend(validate_selection(manifest_path, section, item))

    if asset_type == "behavior" and "satisfy_by" not in item:
        errors.append(f"{manifest_path}: {label}: missing satisfy_by")

    if asset_type == "optional-reference" and "notes" not in item:
        errors.append(f"{manifest_path}: {label}: missing notes")

    return errors


def validate_asset_list(
    root: Path,
    manifest_path: Path,
    section: str,
    items: Any,
    seen_ids: dict[str, tuple[str, int]],
) -> list[str]:
    if items is None:
        return []
    if not isinstance(items, list):
        return [f"{manifest_path}: {section} must be a list"]

    errors = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{manifest_path}: {section}[{index}] must be a mapping")
            continue

        item_id = item.get("id")
        if isinstance(item_id, str) and item_id:
            if item_id in seen_ids:
                first_section, first_index = seen_ids[item_id]
                errors.append(
                    f"{manifest_path}: {section} {item_id!r}: duplicate id "
                    f"also used at {first_section}[{first_index}]"
                )
            else:
                seen_ids[item_id] = (section, index)
        else:
            errors.append(
                f"{manifest_path}: {section}[{index}]: id must be a non-empty string"
            )

        errors.extend(validate_item_contract(manifest_path, section, item))
        asset_type = item.get("asset_type")
        errors.extend(
            validate_source_path(
                root,
                manifest_path,
                section,
                item,
                "source",
                required=asset_type in {"bootstrap", "installable", "adapter"},
            )
        )
        errors.extend(
            validate_default_target(
                manifest_path,
                section,
                item,
                required=asset_type == "installable",
            )
        )
        errors.extend(
            validate_read_before_install(
                root,
                manifest_path,
                section,
                item,
                required=asset_type == "adapter",
            )
        )
        errors.extend(validate_companion_files(root, manifest_path, section, item))

    return errors


def validate_top_level_contract(
    root: Path,
    path: Path,
    manifest: dict[str, Any],
) -> list[str]:
    errors = []

    unexpected_keys = sorted(set(manifest) - ALLOWED_TOP_LEVEL_KEYS)
    for key in unexpected_keys:
        errors.append(f"{path}: manifest: unexpected key: {key}")

    for key in ("name", "description", "install_policy"):
        if key not in manifest:
            errors.append(f"{path}: manifest: missing {key}")
        else:
            errors.extend(validate_text_field(path, "manifest", key, manifest[key]))

    errors.extend(validate_dependency_manifests(root, path, manifest))

    has_definition = "capability_definition_source" in manifest
    has_dependencies = "dependency_manifests" in manifest
    if has_dependencies and not has_definition:
        errors.append(f"{path}: manifest: missing capability_definition_source")

    if has_definition:
        definition_source = manifest["capability_definition_source"]
        errors.extend(
            validate_markdown_reference(
                root,
                path,
                "capability_definition_source",
                definition_source,
            )
        )
        if isinstance(definition_source, str) and "#" not in definition_source:
            errors.append(
                f"{path}: manifest: capability_definition_source must include "
                "a heading anchor"
            )
        if not has_dependencies:
            errors.append(f"{path}: manifest: missing dependency_manifests")

    for key in TOP_LEVEL_LIST_FIELDS:
        if key in manifest:
            errors.extend(validate_string_list(path, "manifest", key, manifest[key]))

    if not any(
        isinstance(manifest.get(section), list) and manifest[section]
        for section in ASSET_SECTIONS
    ):
        errors.append(
            f"{path}: manifest must own at least one entry in "
            f"{', '.join(ASSET_SECTIONS)}"
        )

    return errors


def validate_manifest(root: Path, path: Path) -> list[str]:
    manifest, errors = load_manifest(path)
    if errors:
        return errors

    if not isinstance(manifest, dict):
        return [f"{path}: manifest must be a mapping"]

    errors = validate_top_level_contract(root, path, manifest)
    seen_ids: dict[str, tuple[str, int]] = {}
    for section in ASSET_SECTIONS:
        errors.extend(
            validate_asset_list(root, path, section, manifest.get(section), seen_ids)
        )

    return errors


def load_manifest_mappings(
    paths: Iterable[Path],
) -> dict[Path, dict[str, Any]]:
    manifests: dict[Path, dict[str, Any]] = {}
    for path in paths:
        manifest, errors = load_manifest(path)
        if not errors and isinstance(manifest, dict):
            manifests[path.resolve()] = manifest
    return manifests


def dependency_paths(
    root: Path,
    path: Path,
    manifest: dict[str, Any],
    manifests: dict[Path, dict[str, Any]],
) -> list[Path]:
    values = manifest.get("dependency_manifests")
    if not isinstance(values, list):
        return []

    dependencies = []
    for index, value in enumerate(values):
        key = f"dependency_manifests[{index}]"
        if validate_portable_repo_path(path, "manifest", key, value):
            continue
        if not isinstance(value, str):
            continue
        if not value.startswith("manifests/") or not value.endswith(".yml"):
            continue

        candidate = (root / value).resolve()
        if candidate != path.resolve() and candidate in manifests:
            dependencies.append(candidate)
    return dependencies


def display_manifest_path(path: Path, path_by_key: dict[Path, Path]) -> Path:
    return path_by_key.get(path, path)


def validate_dependency_cycles(
    root: Path,
    paths: list[Path],
    manifests: dict[Path, dict[str, Any]],
) -> list[str]:
    path_by_key = {path.resolve(): path for path in paths}
    states: dict[Path, int] = {}
    stack: list[Path] = []
    errors: list[str] = []

    def visit(path: Path) -> None:
        states[path] = 1
        stack.append(path)
        for target in dependency_paths(root, path, manifests[path], manifests):
            target_state = states.get(target, 0)
            if target_state == 0:
                visit(target)
            elif target_state == 1:
                cycle = stack[stack.index(target) :] + [target]
                rendered = " -> ".join(
                    str(display_manifest_path(entry, path_by_key)) for entry in cycle
                )
                errors.append(
                    f"{display_manifest_path(path, path_by_key)}: "
                    f"dependency cycle: {rendered}"
                )
        stack.pop()
        states[path] = 2

    for path in sorted(manifests):
        if states.get(path, 0) == 0:
            visit(path)

    return errors


def dependency_closure(
    root: Path,
    path: Path,
    manifests: dict[Path, dict[str, Any]],
) -> list[Path]:
    ordered: list[Path] = []
    visited: set[Path] = set()

    def visit(current: Path) -> None:
        if current in visited:
            return
        visited.add(current)
        for target in dependency_paths(root, current, manifests[current], manifests):
            visit(target)
        ordered.append(current)

    visit(path)
    return ordered


def load_canonical_prerequisites(
    root: Path,
) -> tuple[dict[str, set[str]], list[str]]:
    path = root / CAPABILITY_MAP_PATH
    if not path.exists():
        return {}, [f"{path}: canonical capability map does not exist"]

    prerequisites: dict[str, set[str]] = {}
    in_table_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if markdown_anchor(heading) == "canonical-prerequisites":
                in_table_section = True
                continue
            if in_table_section:
                break
        if not in_table_section or not line.strip().startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2:
            continue
        domain, required = cells
        if domain == "Capability domain" or set(domain) <= {"-", ":"}:
            continue
        if not domain:
            continue

        if required == "None":
            dependencies: set[str] = set()
        else:
            dependencies = {
                entry.strip()
                for entry in re.split(r"\s*(?:,|<br\s*/?>)\s*", required)
                if entry.strip()
            }
        if domain in prerequisites:
            return {}, [f"{path}: duplicate canonical capability domain {domain!r}"]
        prerequisites[domain] = dependencies

    if not prerequisites:
        return {}, [f"{path}: canonical prerequisite table is missing or empty"]

    errors = []
    for domain, dependencies in prerequisites.items():
        for dependency in sorted(dependencies):
            if dependency not in prerequisites:
                errors.append(
                    f"{path}: capability {domain!r} has unknown canonical "
                    f"prerequisite {dependency!r}"
                )
    return prerequisites, errors


def capability_domain_from_reference(
    root: Path,
    manifest: dict[str, Any],
) -> str | None:
    value = manifest.get("capability_definition_source")
    if not isinstance(value, str) or not value:
        return None

    path_part, separator, anchor = value.partition("#")
    if not separator or not anchor:
        return None
    resolved = root / path_part
    if not resolved.exists():
        return None
    return markdown_headings(resolved).get(anchor)


def validate_capability_projection(
    root: Path,
    paths: list[Path],
    manifests: dict[Path, dict[str, Any]],
) -> list[str]:
    capability_paths = {
        path: capability_domain_from_reference(root, manifest)
        for path, manifest in manifests.items()
        if "capability_definition_source" in manifest
    }
    has_domain_support = any(
        "supports_capability_domains" in item
        for manifest in manifests.values()
        for section in ASSET_SECTIONS
        for item in (
            manifest.get(section)
            if isinstance(manifest.get(section), list)
            else []
        )
        if isinstance(item, dict)
    )
    if not capability_paths and not has_domain_support:
        return []

    canonical, errors = load_canonical_prerequisites(root)
    if errors:
        return errors

    path_by_key = {path.resolve(): path for path in paths}
    manifests_by_domain: dict[str, list[Path]] = {}
    for path, domain in capability_paths.items():
        display_path = display_manifest_path(path, path_by_key)
        if domain is None:
            continue
        if domain not in canonical:
            errors.append(
                f"{display_path}: capability definition identifies unknown "
                f"domain {domain!r}"
            )
            continue
        manifests_by_domain.setdefault(domain, []).append(display_path)

    for domain, owners in sorted(manifests_by_domain.items()):
        if len(owners) > 1:
            rendered = ", ".join(str(owner) for owner in sorted(owners))
            errors.append(
                f"capability domain {domain!r} is implemented by multiple "
                f"manifests: {rendered}"
            )

    for path, domain in capability_paths.items():
        if domain not in canonical:
            continue
        actual_domains: set[str] = set()
        for dependency in dependency_paths(root, path, manifests[path], manifests):
            dependency_domain = capability_paths.get(dependency)
            if dependency_domain is None:
                errors.append(
                    f"{display_manifest_path(path, path_by_key)}: dependency "
                    f"{display_manifest_path(dependency, path_by_key)} does not "
                    "identify an implemented capability domain"
                )
                continue
            actual_domains.add(dependency_domain)

        expected_domains = canonical[domain]
        if actual_domains != expected_domains:
            errors.append(
                f"{display_manifest_path(path, path_by_key)}: capability {domain!r} "
                "dependency projection mismatch: expected "
                f"{sorted(expected_domains)}, found {sorted(actual_domains)}"
            )

    known_domains = set(canonical)
    for path, manifest in manifests.items():
        for section in ASSET_SECTIONS:
            items = manifest.get(section)
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                domains = item.get("supports_capability_domains")
                if not isinstance(domains, list):
                    continue
                for domain in domains:
                    if isinstance(domain, str) and domain and domain not in known_domains:
                        errors.append(
                            f"{display_manifest_path(path, path_by_key)}: "
                            f"{item_label(section, item)}: unknown supported "
                            f"capability domain {domain!r}"
                        )

    return errors


def format_asset_owner(owner: AssetOwner) -> str:
    return f"{owner.manifest}: {owner.section} {owner.asset_id!r}"


def format_output_owner(owner: OutputOwner) -> str:
    suffix = ""
    if owner.companion_index is not None:
        suffix = f" companion_files[{owner.companion_index}]"
    return f"{owner.manifest}: {owner.section} {owner.asset_id!r}{suffix}"


def closure_asset_owners(
    closure: list[Path],
    manifests: dict[Path, dict[str, Any]],
) -> list[AssetOwner]:
    owners: list[AssetOwner] = []
    for path in closure:
        manifest = manifests[path]
        for section in ASSET_SECTIONS:
            items = manifest.get(section)
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                asset_id = item.get("id")
                if isinstance(asset_id, str) and asset_id:
                    owners.append(AssetOwner(path, section, asset_id))
    return owners


def closure_output_owners(
    root: Path,
    closure: list[Path],
    manifests: dict[Path, dict[str, Any]],
) -> dict[str, list[OutputOwner]]:
    del root
    outputs: dict[str, list[OutputOwner]] = {}
    for path in closure:
        manifest = manifests[path]
        for section in ASSET_SECTIONS:
            items = manifest.get(section)
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict) or item.get("asset_type") != "installable":
                    continue
                asset_id = item.get("id")
                if not isinstance(asset_id, str) or not asset_id:
                    continue

                target = item.get("default_target")
                if is_portable_target(target):
                    canonical = str(PurePosixPath(target))
                    outputs.setdefault(canonical, []).append(
                        OutputOwner(path, section, asset_id)
                    )

                companions = item.get("companion_files")
                if not isinstance(companions, list):
                    continue
                for index, companion in enumerate(companions):
                    if not isinstance(companion, dict):
                        continue
                    companion_target = companion.get("default_target")
                    if not is_portable_target(companion_target):
                        continue
                    canonical = str(PurePosixPath(companion_target))
                    outputs.setdefault(canonical, []).append(
                        OutputOwner(path, section, asset_id, index)
                    )

    return outputs


def validate_dependency_compatibility(
    root: Path,
    paths: list[Path],
    manifests: dict[Path, dict[str, Any]],
) -> list[str]:
    path_by_key = {path.resolve(): path for path in paths}
    errors: list[str] = []
    reported_ids: set[tuple[str, str, str]] = set()
    reported_targets: set[tuple[str, str, str, str]] = set()

    for path in sorted(manifests):
        closure = dependency_closure(root, path, manifests)
        owners_by_id: dict[str, list[AssetOwner]] = {}
        for owner in closure_asset_owners(closure, manifests):
            owners_by_id.setdefault(owner.asset_id, []).append(
                AssetOwner(
                    display_manifest_path(owner.manifest, path_by_key),
                    owner.section,
                    owner.asset_id,
                )
            )

        for asset_id in sorted(owners_by_id):
            owners = owners_by_id[asset_id]
            first = owners[0]
            for other in owners[1:]:
                if first.manifest == other.manifest:
                    continue
                pair = tuple(sorted((str(first.manifest), str(other.manifest))))
                conflict_key = (asset_id, pair[0], pair[1])
                if conflict_key in reported_ids:
                    continue
                reported_ids.add(conflict_key)
                errors.append(
                    f"{display_manifest_path(path, path_by_key)}: "
                    f"dependency closure duplicate id {asset_id!r}: "
                    f"{format_asset_owner(first)} conflicts with "
                    f"{format_asset_owner(other)}"
                )
                break

        outputs = closure_output_owners(root, closure, manifests)
        for target in sorted(outputs):
            owners = outputs[target]
            if len(owners) < 2:
                continue
            first = owners[0]
            for other in owners[1:]:
                first_key = format_output_owner(first)
                other_key = format_output_owner(other)
                pair = tuple(sorted((first_key, other_key)))
                conflict_key = (target, pair[0], pair[1], str(path))
                if conflict_key in reported_targets:
                    continue
                reported_targets.add(conflict_key)
                errors.append(
                    f"{display_manifest_path(path, path_by_key)}: copied target "
                    f"collision for {target!r}: {first_key} conflicts with "
                    f"{other_key}"
                )

    return errors


def validate_manifests(root: Path) -> tuple[int, list[str]]:
    errors = []
    paths = list(manifest_files(root))

    for path in paths:
        errors.extend(validate_manifest(root, path))

    manifests = load_manifest_mappings(paths)
    errors.extend(validate_dependency_cycles(root, paths, manifests))
    errors.extend(validate_dependency_compatibility(root, paths, manifests))
    errors.extend(validate_capability_projection(root, paths, manifests))

    return len(paths), errors


def main() -> int:
    count, errors = validate_manifests(ROOT)

    if errors:
        print("Manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Manifest validation passed: {count} manifest files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
