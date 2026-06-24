#!/usr/bin/env python3
"""Validate harness asset manifests."""

from __future__ import annotations

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


def validate_manifest(root: Path, path: Path) -> list[str]:
    manifest, errors = load_manifest(path)
    if errors:
        return errors

    if not isinstance(manifest, dict):
        return [f"{path}: manifest must be a mapping"]

    errors = []
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
