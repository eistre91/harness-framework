#!/usr/bin/env sh
set -eu

# Canonical local verification for this repo.
# Replace the placeholder below with commands derived from README, CI,
# Makefile, tox, nox, package/project config, or existing scripts.
# Keep this aligned with CI where practical.

run() {
  echo "+ $*"
  "$@"
}

echo "No canonical verification command has been configured for this repo." >&2
echo "Replace this placeholder with commands derived from repo evidence." >&2
exit 1
