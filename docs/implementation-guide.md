# Minimal Agent Harness Implementation Guide

Date: 2026-06-14

This guide turns the minimal agent harness framework into an implementation
process. The framework explains what the harness is and why it is shaped that
way. This guide explains how an agent and human should collaboratively fit the
starter harness to a real repository.

The central rule is:

> Harness implementation is repo diagnosis plus collaborative workflow design,
> not blind template installation.

The harness is a leverage layer for humans. It encodes team taste, risk
tolerance, engineering standards, review habits, and workflow assumptions. An
agent should not silently impose those choices. It should inspect the repo,
propose the smallest useful harness layer, explain trade-offs, ask targeted
questions, and implement only the agreed starter shape.

## Intended Use

Use this guide when applying the minimal harness framework to a repository that
does not already have a mature agent harness.

The first implementation should normally aim for Level 0 or Level 1 maturity,
possibly with a small number of selected pieces from higher levels when the
repo already has clear evidence for them.

Do not use this guide as permission to install every harness component. The
default posture is to keep the harness small, useful, and easy for the team to
understand.

## Implementation Principles

### Collaborate Before Editing

Before creating or changing files, the agent should present a Harness Fit
Proposal to the human.

The proposal should explain:

- what the agent observed in the repo,
- what maturity level the repo appears to have now,
- what maturity level the installation should target,
- what files will be created or edited,
- what defaults the agent inferred from evidence,
- what gaps were found,
- what is intentionally deferred,
- what questions need human judgment.

The agent should not ask questions whose answers can be discovered from the
repo. It should inspect first, infer defaults, and ask only questions that
materially affect the harness shape.

### Start Lower Than Feels Ambitious

Most repos should start with a lower maturity layer and expand over time.

Adding a large harness too early creates harness debt:

- too many docs,
- too many instructions,
- too many hooks,
- too much process,
- too many artifacts nobody maintains.

A small harness that is used is more valuable than a complete harness that
people work around.

### Surface Gaps Without Owning Every Gap

Harness implementation may reveal missing engineering hygiene. For example:

- no documented test command,
- no linting,
- no CI,
- no clear work tracker,
- stale README instructions,
- no obvious sensitive-file policy.

The agent should surface these gaps, but should not automatically turn harness
installation into a broad modernization project.

Separate gaps into:

```text
Affects harness now:
  must be resolved or explicitly defaulted to install the starter harness

Future improvement:
  worth recording, but not part of this installation
```

Example:

```text
Observed gap:
  No lint command found.

Recommendation:
  Do not add linting during harness installation unless the team explicitly
  wants that. Use the existing test command in scripts/verify.sh and record
  linting as a future improvement.
```

### Argue For Complexity

Complexity should be argued for, not assumed.

When proposing a component beyond Level 0, the agent should state:

- what failure it prevents,
- what signal proves the repo needs it,
- what maintenance cost it adds,
- what simpler option was considered,
- what would justify removing or simplifying it later.

### Make Deferrals Explicit

Deferring a component is a design decision, not neglect.

For each deferred component, record:

```text
Deferred:
  SPEC-MAP.md

Why:
  The repo has only one small project-doc area and agents can navigate it
  directly.

Signal to add later:
  Agents repeatedly ask where feature-specific context lives, or docs grow
  enough that task routing becomes ambiguous.
```

## Implementation Flow

The agent should follow this sequence.

### 1. Inspect The Repo

Read enough to understand current workflow and verification without consuming
unnecessary context.

Suggested inspection targets:

- repo root listing,
- `README*`,
- existing `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.codex/`, `.agents/`,
- CI workflows such as `.github/workflows/*`,
- package or project config:
  - Python: `pyproject.toml`, `setup.cfg`, `setup.py`, `tox.ini`,
    `noxfile.py`, `requirements*.txt`, `Pipfile`, `uv.lock`,
  - Node: `package.json`, lockfiles,
  - other stacks: obvious build/test config,
- `Makefile`, `justfile`, `Taskfile.yml`, `scripts/*`,
- test directories,
- docs directories,
- tracker references in README, CONTRIBUTING, or issue templates,
- `.gitignore` for local state and secret patterns.

The agent should not read every source file. The goal is harness fit, not full
codebase comprehension.

### 2. Identify Existing Signals

Classify what already exists.

```text
Agent entrypoint:
  present / absent / stale / unclear

Work source:
  Jira / GitHub Issues / Linear / chat / docs / unknown

Verification:
  documented / inferred from CI / inferred from config / missing

Project docs:
  none / small / useful but unrouted / large enough to route

Sensitive files:
  obvious / not obvious / existing policy

Agent tools:
  Codex / Claude / Cursor / mixed / unknown

CI:
  present / absent / not inspected
```

### 3. Decide Current And Target Maturity

The agent should explicitly state both the current observed maturity and the
target maturity for the installation.

Template:

```md
## Target Harness Maturity

Current observed maturity:
- Level:
- Evidence:
- Gaps:

Recommended target for this installation:
- Target level:
- Selected pull-ins from higher levels:
- Components intentionally not added:

Why this target:
-

Signal to expand later:
-
```

Example:

```md
## Target Harness Maturity

Current observed maturity:
- Level: partial Level 0
- Evidence: README documents `pytest`, CI runs tests, but there is no agent
  entrypoint or work brief.
- Gaps: no canonical verification script; no acceptance evidence standard.

Recommended target for this installation:
- Target level: Level 1
- Selected pull-ins from higher levels: none
- Components intentionally not added: SPEC-MAP.md, .harness.yml, hooks

Why this target:
- The repo already has basic test evidence, but work handoff is vague.
- The highest-value improvement is a small agent entrypoint, a work brief, and
  a canonical verify command.
- Context routing is premature because project docs are small.

Signal to expand later:
- Agents repeatedly ask where domain context lives or miss existing docs.
```

### 4. Prepare A Harness Fit Proposal

Before editing, present this proposal.

```md
# Harness Fit Proposal

## Repo Signals
-

## Current Maturity
-

## Target Maturity
-

## Recommended Starter
-

## Defaults Inferred From Repo
-

## Gaps Surfaced
Affects harness now:
-

Future improvement:
-

## Trade-Offs
-

## Human Decisions Needed
-

## Persisted Plan
- Path:
- Update rule:

## Intentionally Deferred
-

## Files Proposed
Create:
-

Edit:
-

## Acceptance Criteria
-
```

Persist the Harness Fit Proposal to disk as the installation plan before
editing. Ask for a preferred path only if the target repo already has a clear
planning location or the human is likely to care. Otherwise use a temp path such
as:

```text
/tmp/<target-repo-name>-harness-fit-proposal.md
```

The plan should survive a session handoff. If the proposal changes after human
questions are answered, update the persisted plan before editing files.

Use recommendations instead of open-ended questions where possible.

Poor:

```text
What should the harness do?
```

Better:

```text
I found pytest in CI and no lint command. I recommend scripts/verify.sh run
pytest only for now and record linting as a future improvement. Do you want
linting added now despite it not already existing?
```

### 5. Ask Focused Human Questions

Ask only questions that affect the implementation.

Useful questions:

- Where should Agent Work Briefs live for the first trial?
- Which work tracker is authoritative?
- Which agent tools will the team actually use?
- Which agent platforms need first-class support now, if any?
- Do you want the Harness Fit Proposal plan somewhere other than `/tmp`?
- Should verification run automatically, or only be documented for now?
- Are any files, directories, services, or data sources off limits to agents?
- What acceptance evidence matters most for this repo?
- How much ceremony will the team tolerate right now?

Avoid asking:

- questions answered by README or CI,
- broad philosophical questions,
- decisions that can safely use the guide's default.

For each question, provide:

```text
Recommended default:
Why:
Trade-off:
When to revisit:
```

### 6. Implement The Agreed Starter

Create or edit only the agreed files.

Keep content short. The starter harness should make the next agent more
effective without making the repo feel process-heavy.

### 7. Validate The Harness

After implementation, check that a fresh agent could:

- find the repo entrypoint,
- find the persisted Harness Fit Proposal plan or its recorded path,
- understand where work comes from,
- create or read an Agent Work Brief,
- find relevant context or know that no context router exists yet,
- run `scripts/verify.sh`,
- produce mechanical and acceptance evidence,
- know what review should check,
- know what was intentionally deferred.

## Starter Acceptance Checklist

A Level 0 or Level 1 starter harness is acceptable when:

- `AGENTS.md` tells agents where to start without becoming an encyclopedia,
- the work brief template can turn a Jira ticket, GitHub issue, or chat request
  into executable work,
- `scripts/verify.sh` exists and either runs real repo commands or clearly
  fails with an honest placeholder,
- verification commands are derived from repo evidence or clearly marked as
  placeholders,
- `docs/harness/README.md` records harness provenance, target maturity,
  installed files, and intentional deferrals,
- acceptance evidence is required for externally visible or boundary-changing
  behavior,
- review guidance checks bugs, scope, tests, maintainability, and
  over-engineering,
- optional components are explicitly deferred with signals for later adoption,
- the human can explain why the chosen maturity target fits the repo.

## Work Brief Lifecycle

The Agent Work Brief is the central work artifact. The implementation guide
should choose where it lives for the project rather than leaving that implicit.

### Placement Options

#### Jira Ticket Or Comment

Best when Jira is the team source of truth.

Pros:

- visible to the team,
- keeps planning near the tracked work,
- easier for humans to review and discuss.

Cons:

- less convenient for local agent tooling,
- may require copy/paste if Jira tooling is weak,
- harder to version alongside code.

Recommended default for Jira-centered teams:

```text
Keep the canonical brief in Jira as a ticket section or comment.
Agents may create a temporary local draft, but the durable brief lives in Jira.
If the temporary draft gains progress, evidence, blockers, or plan changes,
post those updates back to Jira before removing the local draft.
```

#### Repo File

Possible locations:

```text
docs/work/<ticket-id>.md
.agent/work/<ticket-id>.md
```

Pros:

- easy for agents to read and edit,
- versioned if stored under docs,
- works without tracker integration.

Cons:

- can drift from the tracker,
- may clutter the repo,
- may expose planning material that belongs in the tracker.

Recommended default:

```text
Use repo files only when the team wants durable in-repo planning artifacts or
does not have a reliable tracker workflow.
```

#### PR Description

Pros:

- useful for review,
- close to the diff.

Cons:

- too late for implementation planning,
- not ideal as the source brief.

Recommended default:

```text
Use the PR description to summarize the brief and evidence, not as the
canonical planning surface.
```

#### Chat Artifact

Pros:

- lightest possible process,
- useful for very small work.

Cons:

- not durable,
- hard for fresh agents to resume,
- invisible to teammates.

Recommended default:

```text
Use chat-only briefs only for tiny work where loss of continuity is acceptable.
```

### Status

A simple lifecycle is enough:

```text
Draft -> Ready For Implementation -> Implemented -> Verified -> Reviewed
```

Do not add more states until the team needs them.

For work that spans sessions, the current brief should also capture enough
resume state for the next agent or reviewer:

- current status,
- plan changes,
- divergences from the expected approach and why they were accepted,
- blockers,
- latest evidence,
- next action.

This resume state belongs wherever the canonical brief lives. A local draft can
be convenient during implementation, but it should not become the durable source
of truth unless the team chose repo-local planning artifacts.

### Ownership

The human owns product intent and trade-offs.

The planning agent owns converting that intent into an executable brief.

The implementation agent owns carrying out the brief and producing evidence.

The reviewer owns checking whether the change satisfies the brief and whether
the implementation introduces unacceptable risk or debt.

## Verification Discovery Recipe

`scripts/verify.sh` should encode the repo's current verification contract.
The agent should derive that contract from evidence.

### Discovery Order

1. Inspect CI workflows.
2. Inspect documented setup and test commands in README or CONTRIBUTING.
3. Inspect project config.
4. Inspect existing scripts such as `Makefile`, `justfile`, `tox`, `nox`, or
   `package.json`.
5. Inspect test directories and naming conventions.
6. Prefer commands the repo already uses over commands the agent happens to
   prefer.
7. If commands conflict, surface the conflict in the Harness Fit Proposal.

### Python Signals

Common signals:

```text
pytest:
  pyproject.toml, pytest.ini, tests/, CI command uses pytest

ruff:
  pyproject.toml [tool.ruff], CI uses ruff

mypy:
  mypy.ini, pyproject.toml [tool.mypy], CI uses mypy

pyright:
  pyrightconfig.json, CI uses pyright

tox:
  tox.ini

nox:
  noxfile.py

uv:
  uv.lock, pyproject.toml, CI uses uv run

poetry:
  poetry.lock, pyproject.toml [tool.poetry]
```

### Command Selection Rules

Prefer the highest-level command the repo already uses.

Examples:

```text
If CI runs `make test`, use `make test`.
If CI runs `tox`, use `tox`.
If README says `uv run pytest`, use `uv run pytest`.
If only pytest config exists, use `pytest` or the repo's environment manager.
```

Do not add a new tool during harness installation unless the human agrees.

### Generic `verify.sh` Template

```sh
#!/usr/bin/env sh
set -eu

# Canonical local verification for this repo.
# Keep this aligned with CI where practical.

run() {
  echo "+ $*"
  "$@"
}

# Replace these commands with the repo's existing verification commands.
# Prefer commands already documented in README, CI, Makefile, tox, nox, or
# project config.
# If no command can be confirmed, leave this explicit failure in place instead
# of guessing.

echo "No canonical verification command has been configured for this repo." >&2
echo "Replace this placeholder with commands derived from README, CI, Makefile, tox, nox, or project config." >&2
exit 1
```

### Python Examples

Existing pytest only:

```sh
#!/usr/bin/env sh
set -eu

run() {
  echo "+ $*"
  "$@"
}

run pytest
```

Existing ruff and pytest:

```sh
#!/usr/bin/env sh
set -eu

run() {
  echo "+ $*"
  "$@"
}

run ruff check .
run pytest
```

Existing uv workflow:

```sh
#!/usr/bin/env sh
set -eu

run() {
  echo "+ $*"
  "$@"
}

run uv run ruff check .
run uv run pytest
```

Existing make workflow:

```sh
#!/usr/bin/env sh
set -eu

run() {
  echo "+ $*"
  "$@"
}

run make test
```

### If Verification Is Missing

If no reliable command can be inferred:

1. do not invent a full verification stack,
2. create `scripts/verify.sh` with an explicit placeholder,
3. record the missing verification command as a gap,
4. recommend the smallest next action.

Example placeholder:

```sh
#!/usr/bin/env sh
set -eu

echo "No canonical verification command has been configured for this repo." >&2
echo "Add the repo's test/lint/typecheck commands here once agreed." >&2
exit 1
```

This makes the absence explicit instead of letting agents pretend verification
exists.

## Portability Model

The harness should separate concepts from adapters.

### Concepts

Portable concepts:

- repo entrypoint,
- work brief,
- verification command,
- review guidance,
- acceptance evidence,
- maturity model,
- maintainability feedback.

### Adapters

Adapters depend on the team's tools:

- Codex hooks,
- Claude Code settings,
- Cursor rules,
- GitHub Actions,
- tracker APIs, CLIs, or MCP tools,
- GitHub CLI,
- pre-commit,
- repowise,
- unattended runners.

The implementation guide should not require an adapter unless the repo already
uses that environment or the human explicitly wants it.

### Cross-Tool Uniformity

When a repo uses multiple agentic coding tools, the harness should preserve the
same behavior across them wherever practical. Claude Code, Codex, Cursor, CI,
and pre-commit adapters should not each define their own version of the
harness.

Default:

```text
Keep shared policy in AGENTS.md, scripts/verify.sh, work brief templates, and
portable skill guidance. Make adapters thin wrappers around those shared
contracts.
```

For hooks, this means:

- prefer one shared script for verification, secret checks, or destructive
  action checks,
- have Codex, Claude Code, pre-commit, and CI call that shared script where
  possible,
- keep output shape and failure meaning consistent across tools,
- document any unavoidable divergence in the adapter README.

Uniformity matters more than feature parity. A simple check that behaves the
same in Claude Code and Codex is usually better than two clever tool-specific
checks that drift.

If platform-specific support is in scope, read `docs/platform-support.md`, then
the specific platform note for the adapter being installed. Do not load those
docs for ordinary product work or for a basic Level 0 install that does not add
platform-specific settings, hooks, or skill adapters.

### Skills

Keep shared skill source portable. This framework defaults to
`.agents/skills`, which Codex supports natively. Other platforms may need a
thin adapter, mirror, symlink, or install step to expose the same skill content
through their native discovery path.

Default:

```text
Install skill source files to .agents/skills/<skill-name>/SKILL.md.

Keep shared skill guidance portable. Use adapters only for tool-specific
loading behavior or limitations.
```

### Hooks

Hooks are optional in the starter installation.

Default:

```text
Start with scripts/verify.sh as the contract. Add hooks only if the team wants
automatic enforcement or repeated failures show that agents forget the command.
```

## Starter Assets

The source-of-truth asset selections live in the manifests. Do not maintain
second copies inside this guide.

Use the manifests to decide what to copy or adapt:

- `manifests/bootstrap.yml`
- `manifests/level-0.yml`
- `manifests/level-1.yml`
- `manifests/optional-assets.yml`

The embedded examples elsewhere in this guide explain how to adapt these
assets. The files above are the templates to copy.

## Level Decision Worksheet

Use this worksheet during the Harness Fit Proposal.

```md
# Harness Level Decision

## Level 0: Table Stakes

Already present:
-

Missing:
-

Needed now?
- yes/no

Why:
-

## Level 1: Bounded Work Execution

Signals present:
-

Needed now?
- yes/no

Why:
-

## Level 2: Context Routing

Signals present:
-

Needed now?
- yes/no

Why:
-

## Level 3: Deterministic Controls

Signals present:
-

Needed now?
- yes/no

Why:
-

## Level 4: Maintainability Sensors

Signals present:
-

Needed now?
- yes/no

Why:
-

## Level 5: Orchestration And Automation

Signals present:
-

Needed now?
- usually no for starter install

Why:
-

## Recommended Target

Target level:

Selective pull-ins from higher levels:

Intentionally deferred:

Smallest useful installation:
-
```

## Common Installation Shapes

### Tiny Repo With No Agent Harness

Recommended target:

```text
Level 0
```

Create:

- the Level 0 assets from `manifests/level-0.yml`

Defer:

- context routing,
- platform pointer files for unused tools,
- hooks,
- `.harness.yml`,
- maintainability tooling.

### Jira-Centered Team With Vague Tickets

Recommended target:

```text
Level 1
```

Create:

- the Level 0 assets from `manifests/level-0.yml`
- the additive Level 1 assets and behaviors from `manifests/level-1.yml`.

Decision:

- canonical work brief lives in Jira ticket/comment or repo file.

Add:

- acceptance evidence standard,
- non-goals and interface sections for boundary-changing work,
- implementation guidance for agents working from briefs,
- work-brief guidance if agents will shape tickets or chat requests into
  executable briefs.

Defer:

- tracker automation unless it clearly helps seed the brief.

### Repo With Useful But Scattered Docs

Recommended target:

```text
Level 1 plus selected Level 2
```

Add:

- short project-doc routing note,
- maybe `SPEC-MAP.md` if there are multiple areas.

Defer:

- `CONTEXT.md` unless vocabulary confusion is recurring.

### Repo With Repeated Mechanical Failures

Recommended target:

```text
Level 1 plus selected Level 3
```

Add:

- `scripts/verify.sh`,
- pre-commit or Stop hook only if the team wants automatic enforcement,
- CI parity if CI already exists or is in scope.

Defer:

- broader maintainability automation.

## Done Criteria For Harness Installation

The implementation is done when:

- the chosen maturity target, provenance, and deferrals are recorded in
  `docs/harness/README.md`,
- the Harness Fit Proposal plan was persisted to disk and the path is recorded,
- the human has agreed to the starter shape or explicitly delegated the choice,
- all agreed starter files exist,
- `scripts/verify.sh` either runs real repo commands or clearly fails with an
  honest placeholder,
- the Agent Work Brief has a chosen placement and lifecycle,
- the final report separates mechanical verification from acceptance evidence,
- optional components are deferred with reasons and future signals,
- a fresh agent can read `AGENTS.md` and know how to proceed,
- the final report lists files changed, commands run, acceptance evidence,
  gaps surfaced, and deferred work.

## Final Report Format

After implementation, report:

```md
## Harness Installed

Target maturity:

Harness Fit Proposal plan:
- Path:

Files changed:
-

Work brief:
- Canonical location:
- Allowed temporary draft location:
- Lifecycle/status updates:

Mechanical verification:
-

Acceptance evidence:
- <evidence or "not applicable; behavior did not change">

Gaps surfaced:
-

Deferred:
-

How to expand later:
-
```

## Summary

The implementation guide should make the agent behave like a careful senior
engineer introducing leverage:

- inspect before prescribing,
- infer defaults from repo evidence,
- ask focused questions,
- state the target maturity,
- keep the first install small,
- separate hygiene gaps from harness scope,
- argue for complexity,
- record deferrals,
- leave the repo with a harness humans can understand and maintain.

The goal is not to maximize harness maturity. The goal is to install the
smallest harness that makes agents and humans more effective now, while making
the next useful layer obvious when the project earns it.
