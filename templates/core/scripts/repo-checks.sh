#!/usr/bin/env sh
set -eu

# Canonical deterministic checks for this repo.
# Installed by the agent harness as the repo checks entrypoint.
# Scope: lint/typecheck/tests/build checks for product code, not harness validation.
# This is the target-repo template; do not replace it with the framework repo's
# own scripts/repo-checks.sh.
#
# Replace the placeholder below with commands derived from README, CI, existing
# scripts, package/project config, or other repo evidence.
# Keep this aligned with CI where practical.

run() {
  echo "+ $*"
  "$@"
}

echo "No canonical repo checks command has been configured for this repo." >&2
echo "Replace this placeholder with commands derived from repo evidence." >&2
exit 1
