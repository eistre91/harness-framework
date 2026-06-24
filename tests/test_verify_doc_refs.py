from __future__ import annotations

import importlib.util
from pathlib import Path


def load_verify_doc_refs():
    script = Path(__file__).resolve().parents[1] / "scripts" / "verify-doc-refs.py"
    spec = importlib.util.spec_from_file_location("verify_doc_refs", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_doc_refs_reports_missing_local_markdown_link(
    tmp_path: Path,
) -> None:
    module = load_verify_doc_refs()
    (tmp_path / "README.md").write_text(
        "Read [the guide](docs/missing.md).\n",
        encoding="utf-8",
    )

    _count, errors = module.validate_doc_refs(tmp_path)

    assert errors == [
        "README.md:1: referenced path does not exist: docs/missing.md",
    ]


def test_validate_doc_refs_ignores_fenced_code_and_target_paths(
    tmp_path: Path,
) -> None:
    module = load_verify_doc_refs()
    (tmp_path / "README.md").write_text(
        """\
Target work goes under `docs/work/`.

```text
Use docs/missing.md while trying an example.
```
""",
        encoding="utf-8",
    )

    _count, errors = module.validate_doc_refs(tmp_path)

    assert errors == []


def test_validate_doc_refs_accepts_skill_relative_support_files(
    tmp_path: Path,
) -> None:
    module = load_verify_doc_refs()
    skill = tmp_path / "skills" / "optional" / "diagnose" / "SKILL.md"
    support = tmp_path / "skills" / "optional" / "diagnose" / "scripts" / "loop.sh"
    skill.parent.mkdir(parents=True)
    support.parent.mkdir(parents=True)
    support.write_text("#!/usr/bin/env sh\n", encoding="utf-8")
    skill.write_text(
        """\
---
support_files:
  - scripts/loop.sh
---

Copy `scripts/loop.sh` before editing.
""",
        encoding="utf-8",
    )

    _count, errors = module.validate_doc_refs(tmp_path)

    assert errors == []


def test_validate_doc_refs_checks_parent_relative_markdown_links(
    tmp_path: Path,
) -> None:
    module = load_verify_doc_refs()
    docs = tmp_path / "docs"
    docs.mkdir()
    (tmp_path / "README.md").write_text("# Readme\n", encoding="utf-8")
    (docs / "guide.md").write_text(
        "Read [root](../README.md) and [missing](../missing.md).\n",
        encoding="utf-8",
    )

    _count, errors = module.validate_doc_refs(tmp_path)

    assert errors == [
        "docs/guide.md:1: referenced path does not exist: ../missing.md",
    ]
