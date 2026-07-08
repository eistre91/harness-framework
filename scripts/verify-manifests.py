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
        "PyYAML is required. Install it with: python3 -m pip install PyYAML",
        file=sys.stderr,
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
ASSET_SECTIONS = ("assets", "adapters", "common_starter_pull_ins")
ALLOWED_TOP_LEVEL_KEYS = {
    "name",
    "description",
    "install_policy",
    "base",
    "level_definition_source",
    "assets",
    "adapters",
    "common_starter_pull_ins",
    "defer_by_default",
    "excluded_from_level_asset_boundary",
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
    "maturity",
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
ALLOWED_MATURITY_VALUES = {
    "level-1",
    "level-2",
    "level-3",
    "level-4",
    "level-5",
}
ITEM_TEXT_FIELDS = ("required_when", "install_when", "use_when", "category", "notes")
ITEM_LIST_FIELDS = ("adapt", "satisfy_by")
TOP_LEVEL_LIST_FIELDS = ("defer_by_default", "excluded_from_level_asset_boundary")


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
) -> list[str]:
    if not isinstance(value, list):
        return [f"{manifest_path}: {label}: {key} must be a list"]

    errors = []
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


def markdown_anchors(path: Path) -> set[str]:
    anchors = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip()
        if heading:
            anchors.add(markdown_anchor(heading))
    return anchors


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

    if anchor and anchor not in markdown_anchors(resolved):
        return [f"{manifest_path}: {label}: {key} anchor does not exist: {value}"]

    return []


def validate_manifest_base(
    root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
) -> list[str]:
    if "base" not in manifest:
        return []

    value = manifest["base"]
    errors = validate_source_path(root, manifest_path, "manifest", manifest, "base")
    if errors:
        return errors

    if isinstance(value, str) and (
        not value.startswith("manifests/") or not value.endswith(".yml")
    ):
        return [
            f"{manifest_path}: manifest: base must reference a manifest yml: {value}"
        ]

    if isinstance(value, str) and (root / value).resolve() == manifest_path.resolve():
        return [f"{manifest_path}: manifest: base must not reference itself: {value}"]

    return []


def validate_source_path(
    root: Path,
    manifest_path: Path,
    section: str,
    item: Any,
    key: str,
) -> list[str]:
    if not isinstance(item, dict) or key not in item:
        return []

    value = item[key]
    label = item_label(section, item)
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
) -> list[str]:
    if not isinstance(item, dict) or "read_before_install" not in item:
        return []

    label = item_label(section, item)
    value = item["read_before_install"]
    if not isinstance(value, list):
        return [f"{manifest_path}: {label}: read_before_install must be a list"]

    errors = []
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
    asset: Any,
) -> list[str]:
    if not isinstance(asset, dict) or "companion_files" not in asset:
        return []

    label = item_label("asset", asset)
    companions = asset["companion_files"]
    if not isinstance(companions, list):
        return [f"{manifest_path}: {label}: companion_files must be a list"]

    errors = []
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
            )
        )
        errors.extend(
            validate_default_target(
                manifest_path,
                companion_label,
                companion,
                required=False,
            )
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

    if section == "adapters" and asset_type != "adapter":
        errors.append(
            f"{manifest_path}: {label}: adapters entries must use asset_type adapter"
        )

    if "maturity" in item and item["maturity"] not in ALLOWED_MATURITY_VALUES:
        errors.append(
            f"{manifest_path}: {label}: maturity must be one of "
            f"{sorted(ALLOWED_MATURITY_VALUES)}"
        )

    if "required" in item and not isinstance(item["required"], bool):
        errors.append(f"{manifest_path}: {label}: required must be a boolean")

    for key in ITEM_TEXT_FIELDS:
        if key in item:
            errors.extend(validate_text_field(manifest_path, label, key, item[key]))

    for key in ITEM_LIST_FIELDS:
        if key in item:
            errors.extend(validate_string_list(manifest_path, label, key, item[key]))

    return errors


def required_installable_with_source(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    return (
        item.get("asset_type") == "installable"
        and item.get("required") is True
        and "source" in item
    )


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
        errors.extend(validate_source_path(root, manifest_path, section, item, "source"))
        errors.extend(
            validate_default_target(
                manifest_path,
                section,
                item,
                required=required_installable_with_source(item),
            )
        )
        errors.extend(validate_read_before_install(root, manifest_path, section, item))
        errors.extend(validate_companion_files(root, manifest_path, item))

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

    for key in ("name", "description"):
        if key in manifest:
            errors.extend(validate_text_field(path, "manifest", key, manifest[key]))

    if "install_policy" in manifest:
        errors.extend(
            validate_text_field(
                path,
                "manifest",
                "install_policy",
                manifest["install_policy"],
            )
        )

    errors.extend(validate_manifest_base(root, path, manifest))

    if "level_definition_source" in manifest:
        errors.extend(
            validate_markdown_reference(
                root,
                path,
                "level_definition_source",
                manifest["level_definition_source"],
            )
        )

    for key in TOP_LEVEL_LIST_FIELDS:
        if key in manifest:
            errors.extend(validate_string_list(path, "manifest", key, manifest[key]))

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


def validate_manifests(root: Path) -> tuple[int, list[str]]:
    errors = []
    paths = list(manifest_files(root))

    for path in paths:
        errors.extend(validate_manifest(root, path))

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
