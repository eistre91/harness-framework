#!/usr/bin/env sh
set -eu

# Canonical deterministic checks for this framework repo.

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

cd "$repo_root"

run() {
  echo "+ $*"
  "$@"
}

run ./scripts/verify-yaml.py
run env PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests
