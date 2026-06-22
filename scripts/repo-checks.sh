#!/usr/bin/env sh
set -eu

# Canonical deterministic checks for this framework repo.

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

cd "$repo_root"

python_bin="python3"
if [ -x "$repo_root/.venv/bin/python" ]; then
  python_bin="$repo_root/.venv/bin/python"
fi

run() {
  echo "+ $*"
  "$@"
}

run env PYTHONDONTWRITEBYTECODE=1 "$python_bin" -B scripts/verify-yaml.py
run env PYTHONDONTWRITEBYTECODE=1 "$python_bin" -B -m pytest tests
