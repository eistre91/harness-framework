from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_verify_yaml():
    script = ROOT / "scripts" / "verify-yaml.py"
    spec = importlib.util.spec_from_file_location("verify_yaml", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def init_repo(repo: Path, gitignore: str = "") -> None:
    repo.mkdir(parents=True)
    subprocess.run(
        ["git", "init", "--quiet"],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    (repo / ".gitignore").write_text(gitignore, encoding="utf-8")


def git_add(repo: Path, *paths: Path, force: bool = False) -> None:
    command = ["git", "add"]
    if force:
        command.append("--force")
    command.extend(str(path.relative_to(repo)) for path in paths)
    subprocess.run(
        command,
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_git_source_set_checks_tracked_and_untracked_but_not_ignored(
    tmp_path: Path,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "repo with spaces"
    init_repo(repo, ".agents/\n.venv/\ndocs/ignored/\n")

    tracked_yaml = repo / "tracked.yaml"
    tracked_yaml.write_text("name: tracked\n", encoding="utf-8")
    tracked_markdown = repo / "tracked.md"
    tracked_markdown.write_text(
        "---\ntitle: tracked\n---\n# Tracked\n",
        encoding="utf-8",
    )
    untracked_yaml = repo / "new source.yaml"
    untracked_yaml.write_text("name: untracked\n", encoding="utf-8")
    ignored_yaml = repo / ".venv" / "cache.yaml"
    ignored_yaml.parent.mkdir()
    ignored_yaml.write_text("broken: [ignored\n", encoding="utf-8")
    ignored_markdown = repo / ".agents" / "note.md"
    ignored_markdown.parent.mkdir()
    ignored_markdown.write_text("---\ntitle: ignored\n---\n", encoding="utf-8")
    ignored_markdown_nested = repo / "docs" / "ignored" / "audit.md"
    ignored_markdown_nested.parent.mkdir(parents=True)
    ignored_markdown_nested.write_text("---\ntitle: ignored\n---\n", encoding="utf-8")
    git_add(repo, tracked_yaml, tracked_markdown)

    yaml_count, yaml_errors = module.validate_yaml_files(repo)
    frontmatter_count, frontmatter_errors = module.validate_frontmatter(repo)

    assert yaml_count == 2
    assert yaml_errors == []
    assert frontmatter_count == 1
    assert frontmatter_errors == []

    discovered = [path.relative_to(repo).as_posix() for path in module.repo_files(repo)]
    assert discovered == sorted(discovered)
    assert "new source.yaml" in discovered
    assert ".venv/cache.yaml" not in discovered
    assert ".agents/note.md" not in discovered
    assert "docs/ignored/audit.md" not in discovered


def test_sensitive_paths_are_filtered_even_when_force_added_and_not_opened(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "repo"
    init_repo(repo, "secrets/\n")

    valid = repo / "valid.yaml"
    valid.write_text("name: valid\n", encoding="utf-8")
    secret = repo / "secrets" / "local.yaml"
    secret.parent.mkdir()
    secret.write_text("secret: DO_NOT_OPEN_THIS_SENTINEL\n", encoding="utf-8")
    environment = repo / ".env.local"
    environment.write_text("TOKEN=DO_NOT_OPEN_THIS_SENTINEL\n", encoding="utf-8")
    key_material = repo / "certificate.pem"
    key_material.write_text("DO_NOT_OPEN_THIS_SENTINEL\n", encoding="utf-8")
    git_add(repo, valid, secret, environment, key_material, force=True)

    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == secret:
            raise AssertionError("the sensitive fixture was opened")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    count, errors = module.validate_yaml_files(repo)

    assert count == 1
    assert errors == []
    assert secret not in module.repo_files(repo)
    assert environment not in module.repo_files(repo)
    assert key_material not in module.repo_files(repo)


def test_duplicate_key_diagnostic_redacts_key_and_printed_output(
    tmp_path: Path,
    capsys,
) -> None:
    module = load_verify_yaml()
    sentinel = "DUPLICATE_SECRET_SENTINEL"
    source = f"safe: 1\n{sentinel}: first\n{sentinel}: second\n"

    errors = module.parse_yaml("config.yaml", source)

    assert len(errors) == 1
    assert "config.yaml: line 3, column 1" in errors[0]
    assert "duplicate key" in errors[0]
    assert "first occurrence at line 2, column 1" in errors[0]
    assert sentinel not in errors[0]
    assert f"{sentinel}: first" not in errors[0]

    repo = tmp_path / "repo"
    init_repo(repo)
    duplicate_file = repo / "duplicate.yaml"
    duplicate_file.write_text(source, encoding="utf-8")
    git_add(repo, duplicate_file)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert sentinel not in output


def test_duplicate_keys_in_frontmatter_are_rejected_without_the_key(
    tmp_path: Path,
) -> None:
    module = load_verify_yaml()
    sentinel = "FRONTMATTER_SECRET_SENTINEL"
    repo = tmp_path / "repo"
    init_repo(repo)
    document = repo / "document.md"
    document.write_text(
        f"---\n{sentinel}: first\n{sentinel}: second\n---\n# Document\n",
        encoding="utf-8",
    )
    git_add(repo, document)

    count, errors = module.validate_frontmatter(repo)

    assert count == 1
    assert len(errors) == 1
    assert "duplicate key" in errors[0]
    assert sentinel not in errors[0]


def test_malformed_yaml_diagnostic_redacts_source_line_and_printed_output(
    tmp_path: Path,
    capsys,
) -> None:
    module = load_verify_yaml()
    sentinel = "MALFORMED_SECRET_SENTINEL"
    source = f"settings: [{sentinel}\n"

    errors = module.parse_yaml("malformed.yaml", source)

    assert len(errors) == 1
    assert "malformed.yaml: line " in errors[0]
    assert "expected" in errors[0]
    assert sentinel not in errors[0]
    assert source.rstrip() not in errors[0]

    alias_sentinel = "UNDEFINED_ALIAS_SECRET_SENTINEL"
    alias_errors = module.parse_yaml(
        "alias.yaml",
        f"value: *{alias_sentinel}\n",
    )
    assert len(alias_errors) == 1
    assert alias_sentinel not in alias_errors[0]

    repo = tmp_path / "repo"
    init_repo(repo)
    malformed_file = repo / "malformed.yaml"
    malformed_file.write_text(source, encoding="utf-8")
    git_add(repo, malformed_file)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert sentinel not in output
    assert source.rstrip() not in output


def test_clean_export_without_git_metadata_is_validated(tmp_path: Path, monkeypatch) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "clean exported source"
    repo.mkdir()
    (repo / "manifest.yaml").write_text("name: exported\n", encoding="utf-8")
    docs = repo / "docs"
    docs.mkdir()
    (docs / "guide with spaces.md").write_text(
        "---\ntitle: exported\n---\n# Guide\n",
        encoding="utf-8",
    )
    secret = repo / "secrets" / "local.yaml"
    secret.parent.mkdir()
    secret.write_text("broken: [secret\n", encoding="utf-8")
    monkeypatch.setattr(module, "_git_source_files", lambda _root: None)

    yaml_count, yaml_errors = module.validate_yaml_files(repo)
    frontmatter_count, frontmatter_errors = module.validate_frontmatter(repo)

    assert yaml_count == 1
    assert yaml_errors == []
    assert frontmatter_count == 1
    assert frontmatter_errors == []
    assert all(path != secret for path in module.repo_files(repo))


def test_black_box_counts_and_redacted_failure_match_clean_export(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "ordinary checkout"
    clean_export = tmp_path / "clean export"
    init_repo(checkout, ".agents/\n.venv/\ndocs/ignored/\nsecrets/\n")
    (checkout / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts" / "verify-yaml.py", checkout / "scripts" / "verify-yaml.py")

    tracked_yaml = checkout / "tracked.yaml"
    tracked_yaml.write_text("name: tracked\n", encoding="utf-8")
    tracked_markdown = checkout / "tracked.md"
    tracked_markdown.write_text(
        "---\ntitle: tracked\n---\n# Tracked\n",
        encoding="utf-8",
    )
    untracked_yaml = checkout / "new.yaml"
    untracked_yaml.write_text("name: untracked\n", encoding="utf-8")
    (checkout / ".venv" / "ignored.yaml").parent.mkdir()
    (checkout / ".venv" / "ignored.yaml").write_text(
        "broken: [ignored\n",
        encoding="utf-8",
    )
    (checkout / ".agents" / "ignored.md").parent.mkdir()
    (checkout / ".agents" / "ignored.md").write_text(
        "---\ntitle: ignored\n---\n",
        encoding="utf-8",
    )
    secret = checkout / "secrets" / "local.yaml"
    secret.parent.mkdir(parents=True)
    secret.write_text(
        "broken: [secret\n",
        encoding="utf-8",
    )
    git_add(checkout, checkout / ".gitignore", checkout / "scripts" / "verify-yaml.py", tracked_yaml, tracked_markdown)

    for relative in (
        ".gitignore",
        "scripts/verify-yaml.py",
        "tracked.yaml",
        "tracked.md",
        "new.yaml",
    ):
        destination = clean_export / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(checkout / relative, destination)

    def run_validator(repo: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(repo / "scripts" / "verify-yaml.py")],
            cwd=repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    checkout_result = run_validator(checkout)
    clean_result = run_validator(clean_export)

    assert checkout_result.returncode == 0
    assert clean_result.returncode == 0
    assert checkout_result.stdout == clean_result.stdout
    assert checkout_result.stderr == clean_result.stderr == ""
    assert checkout_result.stdout == "YAML validation passed: 2 YAML files, 1 Markdown frontmatter blocks.\n"

    sentinel = "PARITY_SECRET_SENTINEL"
    malformed = f"broken: [{sentinel}\n"
    (checkout / "broken.yaml").write_text(malformed, encoding="utf-8")
    (clean_export / "broken.yaml").write_text(malformed, encoding="utf-8")

    checkout_result = run_validator(checkout)
    clean_result = run_validator(clean_export)

    assert checkout_result.returncode == 1
    assert clean_result.returncode == 1
    assert checkout_result.stderr == clean_result.stderr
    assert sentinel not in checkout_result.stdout + checkout_result.stderr


@pytest.mark.parametrize("tracked", [True, False])
def test_yaml_symlink_is_rejected_without_opening_ignored_target(
    tmp_path: Path,
    monkeypatch,
    capsys,
    tracked: bool,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / ("tracked repo" if tracked else "untracked repo")
    init_repo(repo, "secrets/\n")

    target = repo / "secrets" / "local.yaml"
    target.parent.mkdir()
    target.write_text("token: YAML_SYMLINK_TARGET_SENTINEL\n", encoding="utf-8")
    link = repo / "public.yaml"
    link.symlink_to(target)
    if tracked:
        git_add(repo, link)

    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == target:
            raise AssertionError("the symlink target was opened")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    count, errors = module.validate_yaml_files(repo)

    assert count == 1
    assert errors == [
        "public.yaml: symbolic-link YAML inputs are not supported",
    ]
    assert target not in module.repo_files(repo)
    assert str(target.relative_to(repo)) not in "\n".join(errors)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "YAML_SYMLINK_TARGET_SENTINEL" not in output


def test_markdown_symlink_is_rejected_without_opening_frontmatter_target(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "repo"
    init_repo(repo, "ignored/\n")

    target = repo / "ignored" / "target.md"
    target.parent.mkdir()
    target.write_text(
        "---\ntitle: MARKDOWN_SYMLINK_TARGET_SENTINEL\n---\n",
        encoding="utf-8",
    )
    link = repo / "public.md"
    link.symlink_to(target)
    git_add(repo, link)

    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == target:
            raise AssertionError("the Markdown symlink target was opened")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    count, errors = module.validate_frontmatter(repo)

    assert count == 1
    assert errors == [
        "public.md: symbolic-link Markdown inputs are not supported",
    ]
    assert str(target.relative_to(repo)) not in "\n".join(errors)


def test_exported_symlinks_and_dangling_links_are_rejected_without_target_reads(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "clean export"
    repo.mkdir()

    target_dir = repo / "secrets"
    target_dir.mkdir()
    yaml_target = target_dir / "secret.yaml"
    yaml_target.write_text(
        "token: EXPORT_SYMLINK_TARGET_SENTINEL\n",
        encoding="utf-8",
    )
    yaml_link = repo / "public.yaml"
    yaml_link.symlink_to(yaml_target)

    markdown_target = target_dir / "guide-target.md"
    markdown_target.write_text(
        "---\ntitle: EXPORT_MARKDOWN_TARGET_SENTINEL\n---\n",
        encoding="utf-8",
    )
    markdown_link = repo / "guide.md"
    markdown_link.symlink_to(markdown_target)

    dangling = repo / "dangling.yaml"
    dangling.symlink_to(repo / "does-not-exist.yaml")

    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path in {yaml_target, markdown_target}:
            raise AssertionError("an exported symlink target was opened")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "public.yaml: symbolic-link YAML inputs are not supported" in output
    assert "dangling.yaml: symbolic-link YAML inputs are not supported" in output
    assert "guide.md: symbolic-link Markdown inputs are not supported" in output
    assert "EXPORT_SYMLINK_TARGET_SENTINEL" not in output
    assert "EXPORT_MARKDOWN_TARGET_SENTINEL" not in output
    assert str(yaml_target.relative_to(repo)) not in output
    assert str(markdown_target.relative_to(repo)) not in output


def _ignored_fixture(repo: Path) -> Path:
    ignored = repo / ".agents" / "ignored.yaml"
    ignored.parent.mkdir(parents=True, exist_ok=True)
    ignored.write_text("token: GIT_FAILURE_IGNORED_SENTINEL\n", encoding="utf-8")
    return ignored


def test_git_rev_parse_failure_does_not_walk_ignored_files(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "checkout"
    init_repo(repo, ".agents/\n")
    ignored = _ignored_fixture(repo)

    def fail_git(*args, **kwargs):
        raise subprocess.CalledProcessError(128, args[0])

    monkeypatch.setattr(module.subprocess, "run", fail_git)
    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == ignored:
            raise AssertionError("ignored content was opened after Git failure")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Git source discovery failed" in output
    assert "git rev-parse --show-toplevel" in output
    assert "GIT_FAILURE_IGNORED_SENTINEL" not in output
    assert "Traceback" not in output


def test_git_ls_files_failure_does_not_walk_ignored_files(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "checkout"
    init_repo(repo, ".venv/\n")
    ignored = repo / ".venv" / "ignored.md"
    ignored.parent.mkdir()
    ignored.write_text(
        "---\ntitle: GIT_LS_FILES_IGNORED_SENTINEL\n---\n",
        encoding="utf-8",
    )

    def fail_ls_files(command, **kwargs):
        if command[1] == "rev-parse":
            return SimpleNamespace(stdout=f"{repo}\n")
        raise subprocess.CalledProcessError(128, command)

    monkeypatch.setattr(module.subprocess, "run", fail_ls_files)
    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == ignored:
            raise AssertionError("ignored content was opened after Git failure")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "git ls-files source discovery" in output
    assert "GIT_LS_FILES_IGNORED_SENTINEL" not in output
    assert "Traceback" not in output


def test_mismatched_git_top_level_fails_closed(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    module = load_verify_yaml()
    repo = tmp_path / "checkout"
    init_repo(repo, ".agents/\n")
    ignored = _ignored_fixture(repo)

    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda command, **kwargs: SimpleNamespace(stdout=f"{tmp_path}\n"),
    )
    original_read_text = Path.read_text

    def guarded_read_text(path: Path, *args, **kwargs):
        if path == ignored:
            raise AssertionError("ignored content was opened after top-level mismatch")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    assert module.main(repo) == 1
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "different top level" in output
    assert "GIT_FAILURE_IGNORED_SENTINEL" not in output


def test_metadata_free_export_under_unrelated_parent_repository_uses_export_walk(
    tmp_path: Path,
    monkeypatch,
) -> None:
    module = load_verify_yaml()
    parent = tmp_path / "parent checkout"
    init_repo(parent)
    export = parent / "source export"
    export.mkdir()
    source = export / "manifest.yaml"
    source.write_text("name: export\n", encoding="utf-8")

    def unexpected_git_call(*args, **kwargs):
        raise AssertionError("metadata-free export attempted Git discovery")

    monkeypatch.setattr(module.subprocess, "run", unexpected_git_call)

    assert module.main(export) == 0
    assert list(module.repo_files(export)) == [source]
