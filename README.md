# Agent Harness Framework

This repository is a source package for fitting a portable agent harness to
another software repository.

The framework fits the smallest useful harness to the target repo's current
purpose: enough structure to provide immediate value, with explicit paths to
grow the harness as coordination, context, validation, and automation needs
appear.

The harness is not meant to be installed wholesale. It is meant to be fitted to
the target repo through inspection and collaboration:

1. inspect the target repo,
2. propose the next installation stage, starting with Level 1 by default,
3. ask only the human questions that materially affect the harness shape,
4. copy or adapt only the approved current-stage assets,
5. validate the installed stage and leave a durable handoff,
6. ask whether to stop or inspect the next stage,
7. remove temporary bootstrap material after installation.

## Start Here

Use these entrypoints by task:

- Framework maintenance in this repo: start with `AGENTS.md`, then
  `docs/principles.md`.
- Target-repo installation: start with `docs/installer.md`, then the current
  stage checklist under `docs/install/`.
- Framework shape and rationale: use `docs/framework.md`.
- Maturity definitions and failure signals: use `docs/maturity-model.md` when
  routed there.
- Broad installation reference: use `docs/implementation-guide.md` after the
  staged installer or a stage checklist routes you there.
- Portability and adaptation boundaries: use `docs/portable-assets.md` when
  adaptation scope is unclear.
- Platform adapters: use `docs/platform-support.md`, then only the relevant
  platform note or adapter README, when platform support is in scope.
- Asset boundaries: use the manifests in `manifests/` as the canonical source;
  do not infer installable file lists from this README.
- Attribution and license: see `REFERENCES.md` and `LICENSE`.

## Quickstart

Use this repo as a temporary bootstrap package for a target repo. Do not copy
everything permanently into the target repo.

### Option A: Keep Repos Side By Side

```sh
git clone git@github.com:eistre91/harness-framework.git
cd <target-repo>
```

Then ask an agent:

```text
Use ../harness-framework/docs/installer.md to fit the smallest useful agent
harness stage to this repo. Start with Level 1 unless I explicitly approve a
different current stage. Inspect this repo first, write and persist the current
stage proposal under /tmp by default, present the exact proposal text before
editing, ask for explicit approval or corrections, install only the approved
current-stage assets, validate the stage, and record the final proposal or
equivalent stage handoff under docs/harness/.
```

### Option B: Temporary Bootstrap Directory

Copy or unzip this repo into the target repo as `.harness-bootstrap/`, then ask
an agent:

```text
Use .harness-bootstrap/docs/installer.md to fit the smallest useful agent
harness stage to this repo. Start with Level 1 unless I explicitly approve a
different current stage. Inspect this repo first, write and persist the current
stage proposal under /tmp by default, present the exact proposal text before
editing, ask for explicit approval or corrections, install only the approved
current-stage assets, validate the stage, record the final proposal or
equivalent stage handoff under docs/harness/, and remove .harness-bootstrap/
after installation.
```

### Expected First Install

Most first trials should install only the Level 1 assets from
`manifests/level-1.yml`. The agent should adapt those files to the target repo
and explicitly defer anything else. Use `docs/install/level-1.md` as the Level
1 stage checklist.

Level 1 includes bounded work execution: work-brief shaping, implementation
guidance, review guidance, verification expectations, and the skill-use rules
for ordinary harness work. It also requires narrow Stop automation for the
target repo's desired hook-capable agent runtime(s), running
`scripts/repo-checks.sh`.

After Level 1 validates, the agent should ask whether to stop or inspect
context routing. Use `docs/install/level-2.md` when the human chooses
context-routing inspection.

## Asset Types

Bootstrap materials are used during installation and usually removed from the
target repo after the harness is fitted.

Installable assets are copied or adapted into the target repo only when the
Harness Fit Proposal justifies them.

Adapters are runtime-specific integrations for tools such as Codex, Claude,
Cursor, pre-commit, or CI. Install only the narrow adapter needed for required
Level 1 Stop automation unless the target repo uses another environment feature
or the human explicitly wants it.

`CLAUDE.md` is conditional on Claude Code support. When installed, it should
remain a thin pointer to `AGENTS.md`:

```md
@AGENTS.md
```

When multiple agentic coding tools are used, keep shared behavior in portable
files such as `AGENTS.md`, `.agents/skills`, and `scripts/repo-checks.sh`.
Adapters should be thin mirrors, wrappers, or callers that preserve the same
harness behavior across tools.

If platform-specific support is in scope, read `docs/platform-support.md` and
then only the platform note for the adapter being installed.

## Default Trial Target

For an initial trial, prefer the Level 1 harness defined in
`manifests/level-1.yml`. Add more only when repo evidence or human preference
justifies it.

## Repository Checks

Run this framework repo's own canonical checks before changing framework
manifests, docs, scripts, or skills:

```sh
./scripts/repo-checks.sh
```

The script is the source of truth for this framework repo's checks. In this
repo it validates YAML/frontmatter, manifest references, local documentation
references, and runs the Python tests. It requires Python 3 with PyYAML and
pytest available.

Install the lightweight development dependencies in a local virtual
environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

`scripts/repo-checks.sh` automatically uses `.venv/bin/python` when that
environment exists; otherwise it falls back to `python3`.

Do not copy this framework repo's `scripts/repo-checks.sh` into target repos.
The installable target-repo template is
`templates/core/scripts/repo-checks.sh`, which must be adapted from the target
repo's README, CI, existing scripts, and project config.

## License

This project is licensed under the MIT License. See `LICENSE`.
