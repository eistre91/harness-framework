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


def run_repo_checks_on_stop(repo_root: Path, stdin_text: str) -> StopCheckResult:
    payload = load_payload(stdin_text)
    if payload.get("stop_hook_active") is True:
        return StopCheckResult()

    checks = repo_root / "scripts" / "repo-checks.sh"
    if not checks.is_file():
        return StopCheckResult(
            should_block=True,
            reason=(
                "scripts/repo-checks.sh is missing. Restore the canonical repo "
                "checks command before ending the turn."
            ),
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
        return StopCheckResult(
            should_block=True,
            reason=f"Could not run scripts/repo-checks.sh: {exc}",
        )

    if result.returncode == 0:
        return StopCheckResult()

    return StopCheckResult(
        should_block=True,
        reason=format_failure(result.returncode, result.stdout),
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


def format_failure(returncode: int, output: str) -> str:
    output = output.strip()
    if len(output) > MAX_REASON_CHARS:
        output = output[-MAX_REASON_CHARS:]
        output = "[repo-checks output truncated]\n" + output

    message = (
        "scripts/repo-checks.sh failed at Stop. Fix the failures before "
        "ending the turn."
    )
    if output:
        message = f"{message}\n\n{output}"
    else:
        message = f"{message}\n\nExit status: {returncode}"
    return message
