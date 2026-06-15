# Minimal Agent Harness Framework

This repository is a source package for applying a small, portable agent
harness to another software repository.

The harness is not meant to be installed wholesale. It is meant to be fitted to
the target repo through inspection and collaboration:

1. inspect the target repo,
2. propose the smallest useful harness maturity target,
3. ask only the human questions that materially affect the harness shape,
4. copy or adapt selected templates, skills, and adapters,
5. remove temporary bootstrap material after installation.

## Start Here

- `docs/framework.md` explains the framework and principles.
- `docs/implementation-guide.md` explains how to apply the framework to a repo.
- `docs/maturity-model.md` summarizes the layered adoption model.
- `docs/portable-assets.md` explains what can transfer between repos and what
  must be adapted.
- `docs/platform-support.md` explains when to add platform-specific adapters
  and how to keep them thin.
- `manifests/bootstrap.yml` lists bootstrap-only assets used during
  installation.
- `manifests/level-0.yml` is the canonical list of default starter assets.
- `manifests/level-1.yml` is the canonical additive list for bounded work
  execution.
- `manifests/optional-assets.yml` lists optional pull-ins.

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
Use ../harness-framework/docs/implementation-guide.md to fit a minimal harness
to this repo. Inspect this repo first, write and persist a Harness Fit Proposal
under /tmp by default, present the exact proposal text before editing, ask for
explicit approval or corrections, install only the approved assets, and record
the final proposal or equivalent decision log under docs/harness/.
```

### Option B: Temporary Bootstrap Directory

Copy or unzip this repo into the target repo as `.harness-bootstrap/`, then ask
an agent:

```text
Use .harness-bootstrap/docs/implementation-guide.md to fit a minimal harness to
this repo. Inspect this repo first, write and persist a Harness Fit Proposal
under /tmp by default, present the exact proposal text before editing, ask for
explicit approval or corrections, install only the approved assets, record the
final proposal or equivalent decision log under docs/harness/, and remove
.harness-bootstrap/ after installation.
```

### Expected First Install

Most first trials should install only the Level 0 assets from
`manifests/level-0.yml`. The agent should adapt those files to the target repo
and explicitly defer anything else.

If a first trial targets Level 1 behavior without installing every canonical
Level 1 manifest asset, describe it as a partial starter fit, not simply a
"Level 1 harness."

## Asset Types

Bootstrap materials are used during installation and usually removed from the
target repo after the harness is fitted.

Installable assets are copied or adapted into the target repo only when the
Harness Fit Proposal justifies them.

Adapters are runtime-specific integrations for tools such as Codex, Claude,
Cursor, pre-commit, or CI. Do not install adapters unless the target repo uses
that environment or the human explicitly wants it.

`CLAUDE.md` is conditional on Claude Code support. When installed, it should
remain a thin pointer to `AGENTS.md`:

```md
@AGENTS.md
```

When multiple agentic coding tools are used, keep shared behavior in portable
files such as `AGENTS.md` and `scripts/verify.sh`. Adapters should be thin
wrappers that preserve the same harness behavior across tools.

If platform-specific support is in scope, read `docs/platform-support.md` and
then only the platform note for the adapter being installed.

## Default Trial Target

For an initial trial, prefer the Level 0 harness defined in
`manifests/level-0.yml`. Add more only when repo evidence or human preference
justifies it.
