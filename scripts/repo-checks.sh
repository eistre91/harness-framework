#!/usr/bin/env sh
set -eu

# Canonical deterministic checks for this framework repo.

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

cd "$repo_root"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required; run 'uv sync --locked' after installing uv" >&2
  exit 2
fi

run() {
  echo "+ $*"
  "$@"
}

run env PYTHONDONTWRITEBYTECODE=1 uv run --locked python -B scripts/verify-yaml.py
run env PYTHONDONTWRITEBYTECODE=1 uv run --locked python -B scripts/verify-manifests.py
run env PYTHONDONTWRITEBYTECODE=1 uv run --locked python -B scripts/verify-doc-refs.py
run env PYTHONDONTWRITEBYTECODE=1 uv run --locked python -B -m pytest tests
run env PYTHONDONTWRITEBYTECODE=1 uv run --locked mkdocs build --strict
