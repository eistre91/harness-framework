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
2. read its Current Harness Profile, installed harness state, and the Capability
   Map prerequisites,
3. follow the installer's no-profile routing when no profile exists; otherwise
   select one Profile Change,
4. persist an exact fit proposal,
5. obtain human approval for only its named files and behavior,
6. realize and validate the selected outcome,
7. update the Current Harness Profile only when evidence supports it,
8. leave a durable handoff and stop, and
9. remove temporary bootstrap material after installation.

## Start Here

Use these entrypoints by task:

- Framework maintenance in this repo: start with `AGENTS.md`, then
  `docs/principles.md`.
- Target-repo installation or migration: start with `docs/installer.md`, then
  its routed capability checklist or numbered-model migration guide under
  `docs/install/`.
- Framework shape and rationale: use `docs/framework.md`.
- Capability outcomes and prerequisites: use `docs/capability-map.md`.
- Historical numbered model: `docs/maturity-model.md`; do not use it to install
  or describe current target-repo state.
- Broad implementation reference: use `docs/implementation-guide.md` for a
  cross-cutting question after reading the active installer sources.
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
harness Profile Change to this repo. If no Current Harness Profile exists,
follow the installer's no-profile routing: migrate an existing numbered-model
installation when its behavior or records are present; otherwise propose
Bounded Work only. Inspect this repo first, write and persist one exact
proposal under /tmp by default, present it before editing, ask for explicit
approval or corrections, change only the approved files and behavior, validate
the selected outcome, update the Current Harness Profile only when evidence
supports it, leave a durable handoff under docs/harness/, and stop.
```

### Option B: Temporary Bootstrap Directory

Copy or unzip this repo into the target repo as `.harness-bootstrap/`, then ask
an agent:

```text
Use .harness-bootstrap/docs/installer.md to fit the smallest useful agent
harness Profile Change to this repo. If no Current Harness Profile exists,
follow the installer's no-profile routing: migrate an existing numbered-model
installation when its behavior or records are present; otherwise propose
Bounded Work only. Inspect this repo first, write and persist one exact
proposal under /tmp by default, present it before editing, ask for explicit
approval or corrections, change only the approved files and behavior, validate
the selected outcome, update the Current Harness Profile only when evidence
supports it, leave a durable handoff under docs/harness/, stop, and remove
.harness-bootstrap/ after installation.
```

### Expected First Install

Most first trials should add only Bounded Work from
`manifests/bounded-work.yml`. The agent should adapt only the approved selected
scope and explicitly defer anything else. Use
`docs/install/bounded-work.md` as the capability checklist.

Bounded Work includes work-brief shaping, implementation
guidance, review guidance, verification expectations, and the skill-use rules
for ordinary harness work. It also requires narrow Stop automation for the
target repo's desired hook-capable agent runtime(s), running
`scripts/repo-checks.sh`.

After Bounded Work validates and enters the Current Harness Profile, stop. A
later human-selected Profile Change may use `docs/install/focused-context.md`,
`docs/install/agent-action-boundaries.md`, or
`docs/install/maintainability-feedback.md`. These capabilities are independent
branches that require Bounded Work; none is selected merely because it exists.

## Asset Types

Bootstrap materials are used during installation and usually removed from the
target repo after the harness is fitted.

Installable assets are copied or adapted into the target repo only when the
Harness Fit Proposal justifies them.

Adapters are runtime-specific integrations for tools such as Codex, Claude,
Cursor, pre-commit, or CI. Install only the narrow adapter selected for the
current capability realization and exact approved scope.

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

For an initial trial, prefer Bounded Work as defined in
`manifests/bounded-work.yml`. Add another capability only through a later
dependency-valid Profile Change justified by observed evidence or a credible
anticipated need.

## Repository Checks

Run this framework repo's own canonical checks before changing framework
manifests, docs, scripts, or skills:

```sh
./scripts/repo-checks.sh
```

The script is the source of truth for this framework repo's checks. In this
repo it validates YAML/frontmatter, manifest references, local documentation
references, and runs the Python tests. It requires Python 3.14 or newer and
uv 0.11.x (0.11.28 is pinned in CI). The direct development dependency floors
are recorded in `pyproject.toml`; `uv.lock` records the exact resolved
versions used by local checks and CI.

Install uv using its official installation instructions, then create the
locked development environment:

```sh
uv sync --locked
```

`scripts/repo-checks.sh` runs all Python checks through `uv run --locked`, so
local checks and CI use the same interpreter and dependency policy. To
deliberately update dependency resolution, edit the direct dependency floors
or run `uv lock --upgrade`, review the resulting `uv.lock`, and rerun the
canonical checks. CI uses `uv sync --locked` and will fail if the lockfile is
out of date.

Do not copy this framework repo's `scripts/repo-checks.sh` into target repos.
The installable target-repo template is
`templates/core/scripts/repo-checks.sh`, which must be adapted from the target
repo's README, CI, existing scripts, and project config.

## License

This project is licensed under the MIT License. See `LICENSE`.
