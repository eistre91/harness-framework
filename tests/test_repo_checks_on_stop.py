from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_SOURCE = ROOT / "adapters" / "common-hooks" / "scripts" / "hooks"


def load_stop_module():
    script = HOOK_SOURCE / "repo_checks_on_stop.py"
    spec = importlib.util.spec_from_file_location("repo_checks_on_stop", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_repo_checks(repo: Path, body: str) -> Path:
    checks = repo / "scripts" / "repo-checks.sh"
    checks.parent.mkdir(parents=True, exist_ok=True)
    checks.write_text(body, encoding="utf-8")
    checks.chmod(0o755)
    return checks


def install_stop_adapter(repo: Path, platform: str) -> Path:
    scripts_hooks = repo / "scripts" / "hooks"
    scripts_hooks.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HOOK_SOURCE / "__init__.py", scripts_hooks / "__init__.py")
    shutil.copy2(
        HOOK_SOURCE / "repo_checks_on_stop.py",
        scripts_hooks / "repo_checks_on_stop.py",
    )

    platform_dir = ".codex" if platform == "codex" else ".claude"
    wrapper_dir = repo / platform_dir / "hooks"
    wrapper_dir.mkdir(parents=True, exist_ok=True)
    wrapper = wrapper_dir / "repo-checks-on-stop.py"
    shutil.copy2(
        ROOT / "adapters" / platform / "hooks" / "repo-checks-on-stop.py",
        wrapper,
    )
    if platform == "codex":
        shutil.copy2(ROOT / "adapters" / "codex" / "hooks.json", repo / ".codex")
    else:
        shutil.copy2(
            ROOT / "adapters" / "claude" / "settings.json",
            repo / ".claude",
        )
    return wrapper


def load_first_hook_command(config: Path) -> dict[str, object]:
    settings = json.loads(config.read_text(encoding="utf-8"))
    command = settings["hooks"]["Stop"][0]["hooks"][0]
    assert isinstance(command, dict)
    return command


def run_codex_declared_command(
    repo: Path,
    cwd: Path,
    stdin_text: str,
) -> subprocess.CompletedProcess[str]:
    command = load_first_hook_command(repo / ".codex" / "hooks.json")
    assert command["type"] == "command"
    assert isinstance(command["command"], str)
    return subprocess.run(
        command["command"],
        cwd=cwd,
        input=stdin_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        check=False,
    )


def run_claude_declared_command(
    repo: Path,
    cwd: Path,
    stdin_text: str,
) -> subprocess.CompletedProcess[str]:
    command = load_first_hook_command(repo / ".claude" / "settings.json")
    assert command["type"] == "command"
    assert command["command"] == "python3"
    args = command.get("args")
    assert isinstance(args, list)
    argv = [command["command"]]
    argv.extend(
        str(arg).replace("${CLAUDE_PROJECT_DIR}", str(repo))
        for arg in args
    )
    return subprocess.run(
        argv,
        cwd=cwd,
        input=stdin_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_load_payload_tolerates_missing_malformed_and_non_object_json() -> None:
    module = load_stop_module()

    assert module.load_payload("") == {}
    assert module.load_payload("not json") == {}
    assert module.load_payload("[]") == {}
    assert module.load_payload('{"hook_event_name":"Stop"}') == {
        "hook_event_name": "Stop",
    }


def test_run_repo_checks_on_stop_runs_from_repo_root(tmp_path: Path) -> None:
    module = load_stop_module()
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
pwd > scripts/check-cwd.txt
""",
    )

    result = module.run_repo_checks_on_stop(tmp_path, '{"hook_event_name":"Stop"}')

    assert result.should_block is False
    assert result.reason == ""
    assert (tmp_path / "scripts" / "check-cwd.txt").read_text(
        encoding="utf-8",
    ).strip() == str(tmp_path)


def test_run_repo_checks_on_stop_blocks_when_checks_are_missing(
    tmp_path: Path,
) -> None:
    module = load_stop_module()

    result = module.run_repo_checks_on_stop(tmp_path, "{}")

    assert result.should_block is True
    assert "scripts/repo-checks.sh is missing" in result.reason


def test_run_repo_checks_on_stop_blocks_with_failure_output(
    tmp_path: Path,
) -> None:
    module = load_stop_module()
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
echo "lint failed"
exit 7
""",
    )

    result = module.run_repo_checks_on_stop(tmp_path, "{}")

    assert result.should_block is True
    assert "scripts/repo-checks.sh failed at Stop" in result.reason
    assert "lint failed" in result.reason


def test_run_repo_checks_on_stop_reports_recursive_stop_failure_without_blocking(
    tmp_path: Path,
) -> None:
    module = load_stop_module()
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
echo "still failing"
exit 1
""",
    )

    result = module.run_repo_checks_on_stop(tmp_path, '{"stop_hook_active": true}')

    assert result.should_block is False
    assert result.should_report is True
    assert "still failing" in result.reason
    assert "stop_hook_active=true" in result.reason


def test_run_repo_checks_on_stop_exits_silently_on_recursive_stop_pass(
    tmp_path: Path,
) -> None:
    module = load_stop_module()
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
exit 0
""",
    )

    result = module.run_repo_checks_on_stop(tmp_path, '{"stop_hook_active": true}')

    assert result.should_block is False
    assert result.should_report is False
    assert result.reason == ""


def test_codex_declared_command_maps_failure_to_stop_block_from_subdirectory(
    tmp_path: Path,
) -> None:
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
echo "wrapper failure"
exit 1
""",
    )
    wrapper = install_stop_adapter(tmp_path, "codex")
    subprocess.run(
        ["git", "init"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subdir = tmp_path / "nested" / "work"
    subdir.mkdir(parents=True)

    assert wrapper == tmp_path / ".codex" / "hooks" / "repo-checks-on-stop.py"
    result = run_codex_declared_command(
        tmp_path,
        subdir,
        '{"hook_event_name":"Stop"}',
    )

    assert result.returncode == 0
    assert result.stderr == ""
    output = json.loads(result.stdout)
    assert output["decision"] == "block"
    assert "wrapper failure" in output["reason"]


def test_codex_declared_command_reports_recursive_failure_without_blocking(
    tmp_path: Path,
) -> None:
    write_repo_checks(
        tmp_path,
        """\
#!/usr/bin/env sh
echo "recursive failure"
exit 1
""",
    )
    install_stop_adapter(tmp_path, "codex")
    subprocess.run(
        ["git", "init"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subdir = tmp_path / "nested" / "work"
    subdir.mkdir(parents=True)

    result = run_codex_declared_command(
        tmp_path,
        subdir,
        '{"hook_event_name":"Stop","stop_hook_active":true}',
    )

    assert result.returncode == 0
    assert result.stderr == ""
    output = json.loads(result.stdout)
    assert "decision" not in output
    assert "recursive failure" in output["systemMessage"]


def test_claude_declared_command_handles_repo_paths_with_spaces_and_passes(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo with spaces"
    repo.mkdir()
    write_repo_checks(
        repo,
        """\
#!/usr/bin/env sh
exit 0
""",
    )
    install_stop_adapter(repo, "claude")
    subdir = repo / "nested" / "work"
    subdir.mkdir(parents=True)

    result = run_claude_declared_command(
        repo,
        subdir,
        '{"hook_event_name":"Stop"}',
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_claude_declared_command_reports_recursive_failure_without_blocking(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo with spaces"
    repo.mkdir()
    write_repo_checks(
        repo,
        """\
#!/usr/bin/env sh
echo "claude recursive failure"
exit 1
""",
    )
    install_stop_adapter(repo, "claude")
    subdir = repo / "nested" / "work"
    subdir.mkdir(parents=True)

    result = run_claude_declared_command(
        repo,
        subdir,
        '{"hook_event_name":"Stop","stop_hook_active":true}',
    )

    assert result.returncode == 0
    assert result.stderr == ""
    output = json.loads(result.stdout)
    assert "decision" not in output
    assert "claude recursive failure" in output["systemMessage"]
