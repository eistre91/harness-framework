#!/usr/bin/env python3
"""Shared repo-checks Stop hook behavior."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

MAX_REASON_CHARS = 12000


@dataclass(frozen=True)
class StopCheckResult:
    should_block: bool = False
    reason: str = ""

    @property
    def should_report(self) -> bool:
        return bool(self.reason) and not self.should_block


def run_repo_checks_on_stop(repo_root: Path, stdin_text: str) -> StopCheckResult:
    payload = load_payload(stdin_text)
    recursive_stop = payload.get("stop_hook_active") is True

    checks = repo_root / "scripts" / "repo-checks.sh"
    if not checks.is_file():
        return failure_result(
            (
                "scripts/repo-checks.sh is missing. Restore the canonical "
                "repo checks command."
            ),
            recursive_stop=recursive_stop,
        )

    try:
        result = subprocess.run(
            [str(checks)],
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except OSError as exc:
        return failure_result(
            f"Could not run scripts/repo-checks.sh: {exc}",
            recursive_stop=recursive_stop,
        )

    if result.returncode == 0:
        return StopCheckResult()

    return failure_result(
        format_failure(result.returncode, result.stdout),
        recursive_stop=recursive_stop,
    )


def load_payload(raw: str) -> dict[str, object]:
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


def failure_result(reason: str, *, recursive_stop: bool) -> StopCheckResult:
    if not recursive_stop:
        return StopCheckResult(should_block=True, reason=reason)
    return StopCheckResult(
        reason=(
            f"{reason}\n\n"
            "Reported without blocking because stop_hook_active=true; fix the "
            "failure before relying on Stop hook verification."
        ),
    )


def format_failure(returncode: int, output: str) -> str:
    output = output.strip()
    if len(output) > MAX_REASON_CHARS:
        output = output[-MAX_REASON_CHARS:]
        output = "[repo-checks output truncated]\n" + output

    message = "scripts/repo-checks.sh failed at Stop."
    if output:
        message = f"{message}\n\n{output}"
    else:
        message = f"{message}\n\nExit status: {returncode}"
    return message
