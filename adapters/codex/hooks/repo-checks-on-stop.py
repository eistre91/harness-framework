#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    from scripts.hooks.repo_checks_on_stop import run_repo_checks_on_stop

    result = run_repo_checks_on_stop(ROOT, sys.stdin.read())
    if result.should_block:
        print(json.dumps({"decision": "block", "reason": result.reason}))
    raise SystemExit(0)
