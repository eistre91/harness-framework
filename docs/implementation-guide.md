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

Before fitting a harness, read `docs/principles.md` and `docs/framework.md`.
The principles are the shared decision lens for deciding what to install,
adapt, defer, or reject.

The first implementation should normally aim for Level 0 or Level 1 maturity,
possibly with a small number of selected pieces from higher levels when the
repo already has clear evidence for them.

Do not use this guide as permission to install every harness component. The
default posture is to keep the harness small, useful, and easy for the team to
understand.

## Installation Modes

Every Harness Fit Proposal must state the installation mode. The mode controls
what a maturity claim means.

Use `docs/maturity-model.md` as the canonical prose source for maturity levels,
installation modes, asset completeness, and behavioral completeness. This guide
uses those definitions operationally while fitting a specific target repo.

Also state:

- target maturity: the behavior the repo is being fitted toward,
- asset completeness: full / partial / mostly existing,
- behavioral completeness: whether the resulting workflow is actually usable,
- deferred manifest assets and why they are not installed now.

When the install is partial, use precise wording:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
Deferred manifest assets are listed below with reasons and revisit signals.
```

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

After writing the proposal file, present the exact proposal text to the human.
Then present a short "Decisions I need from you" list. Do not edit the repo
until the human explicitly approves the harness shape or corrects the proposal.
If unresolved trade-offs remain in the proposal, do not treat silence, branch
creation, or a broad "carry it out" as approval of those decisions.

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

Tests, linting, and type checking are especially important for agent
performance. The proposal should actively look for them and either include
existing commands in `scripts/repo-checks.sh` or explicitly opt out of missing
ones for this install.

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
  Opt out of adding linting during this install unless the team explicitly
  wants it. Use the existing repo checks command in scripts/repo-checks.sh and
  record the linting opt-out in the proposal.
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
- platform skills or commands such as `.claude/skills/`,
  `.claude/commands/`, `.agents/skills/`, Cursor rules, or local team
  command directories,
- CI workflows such as `.github/workflows/*`,
- package, build, or project config files,
- existing task runners and scripts,
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

Existing harness components:
  none / agent entrypoint / skills / repo checks script / hooks / work docs / other

Skill or command conflicts:
  none / review-like / implement-like / work-brief-like / diagnose-debug-like / run-checks-like / unknown

CI:
  present / absent / not inspected
```

Existing components should be treated as evidence first, not as obstacles. For
each one that overlaps with the harness, record:

```text
Component:
  <path or platform feature>

Appears to do:
  <summary>

Harness principle it already satisfies:
  <entrypoint / verification / brief / review / context routing / safety / other>

Recommended handling:
  thread through / adapt / supersede / leave alone / defer

Human decision needed:
  <none or concrete decision>
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
- Installation mode: canonical / starter / overlay
- Asset completeness claim:
- Behavioral completeness claim:
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
- Evidence: README documents a test command, CI runs tests, but there is no
  agent entrypoint or work brief.
- Gaps: no canonical deterministic repo checks script; no acceptance evidence
  standard.

Recommended target for this installation:
- Target level: Level 1 bounded work execution
- Installation mode: starter
- Asset completeness claim: partial, not full canonical Level 1
- Behavioral completeness claim: intended to support bounded work briefs,
  verification, acceptance evidence, and review with the installed surfaces
- Selected pull-ins from higher levels: none
- Components intentionally not added: SPEC-MAP.md, .harness.yml, hooks

Why this target:
- The repo already has basic test evidence, but work handoff is vague.
- The highest-value improvement is a small agent entrypoint, a work brief, and
  a canonical repo checks command.
- Context routing is premature because project docs are small.

Signal to expand later:
- Agents repeatedly ask where domain context lives or miss existing docs.
```

### 4. Prepare A Harness Fit Proposal

Before editing, prepare a Harness Fit Proposal using the canonical schema in
`templates/core/docs/harness/fit-proposal.md`. Do not maintain a second full
proposal schema in this guide.

The proposal must include decisions for:

- repo signals and existing harness components,
- skill and command conflicts,
- current and target maturity,
- installation mode and completeness,
- manifest inclusion or deferral,
- work brief storage, local fallback, commit policy, and sync rule,
- verification, focused validation, CI-only checks, and manual evidence,
- tests, lint/format, and type checking,
- gaps, trade-offs, human decisions, deferred items, proposed files,
  acceptance criteria, and communication audit.

Persist the Harness Fit Proposal to disk as the installation plan before
editing. Ask for a preferred path only if the target repo already has a clear
planning location or the human is likely to care. Otherwise use a temp path such
as:

```text
/tmp/<target-repo-name>-harness-fit-proposal.md
```

After writing the temporary proposal, present the exact proposal text to the
human before editing. A short summary is fine, but it must not substitute for
the full proposal.

The temporary plan should survive a session handoff during installation, but
`/tmp` is not durable repo documentation. After installation, record only the
final proposal or equivalent decision log under `docs/harness/`, either by
creating a file such as `docs/harness/fit-proposal.md` or by embedding the
final decisions in `docs/harness/README.md`. Do not copy temporary proposal
paths into durable harness docs.

If the proposal changes after human questions are answered, update the
persisted plan before editing files.

Use recommendations instead of open-ended questions where possible.

Poor:

```text
What should the harness do?
```

Better:

```text
I found a test command in CI and no lint command. I recommend scripts/repo-checks.sh
run the existing test command only for now and record linting as a future
improvement. Do you want linting added now despite it not already existing?
```

### 5. Ask Focused Human Questions

Ask only questions that affect the implementation.

For harness installation, ask this minimum decision set unless the answer is
both obvious from repo evidence and low-risk:

- Should this install mode be `canonical`, `starter`, or `overlay`?
- Where should canonical Agent Work Briefs live?
- What local fallback should agents use when the canonical brief store is
  unavailable?
- Should brief instances live only in the external tracker, in a durable repo
  path, or as gitignored local fallback drafts?
- Should missing test, lint/format, or type-check tools be added now or
  explicitly deferred?
- How should existing platform skills, commands, or review flows be merged,
  namespaced, documented, or deferred?
- Should the final fit proposal be committed under `docs/harness/`, or should
  equivalent decisions be embedded in `docs/harness/README.md`?

Useful questions:

- Where should Agent Work Briefs live for the first trial?
- Which work tracker is authoritative?
- Which agent tools will the team actually use?
- Which agent platforms need first-class support now, if any?
- Should the final proposal be copied to `docs/harness/fit-proposal.md` or
  embedded in `docs/harness/README.md`?
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

Before editing, use a final checkpoint shaped like this:

```md
I have written the fit proposal and will not edit the repo until you confirm
the harness shape. Please review:

- target maturity and installation mode,
- included and excluded assets,
- work brief storage and fallback,
- repo checks command,
- existing component merge/defer decisions,
- skill or command conflict decisions,
- durable location for the final fit proposal.

Reply with corrections, or say "approved to install" and I will make only the
listed changes.
```

### 6. Implement The Agreed Starter

Create or edit only the agreed files.

Keep content short. The starter harness should make the next agent more
effective without making the repo feel process-heavy.

### 7. Validate The Harness

After implementation, check that a fresh agent could:

- find the repo entrypoint,
- find the durable Harness Fit Proposal or equivalent decision log under
  `docs/harness/`,
- understand where work comes from,
- create or read an Agent Work Brief,
- find relevant context or know that no context router exists yet,
- run `scripts/repo-checks.sh`,
- produce mechanical and acceptance evidence,
- know what review should check,
- know what was intentionally deferred,
- understand whether the repo has a canonical install, starter install, or
  overlay,
- avoid mistaking deferred manifest assets for completed maturity.

## Starter Acceptance Checklist

A Level 0 or Level 1 starter harness is acceptable when:

- `AGENTS.md` tells agents where to start without becoming an encyclopedia,
- the work-brief skill bundle can turn a tracker item, issue, or chat request
  into executable work,
- `scripts/repo-checks.sh` exists and either runs real repo checks or clearly
  fails with an honest placeholder,
- repo checks commands are derived from repo evidence or clearly marked as
  placeholders,
- `docs/harness/README.md` records portable harness provenance, target
  maturity, installation mode, completeness, installed files, and intentional
  deferrals,
- the final proposal or equivalent decision log is durable under
  `docs/harness/`,
- acceptance evidence is required for externally visible or boundary-changing
  behavior,
- side-effect evidence uses "secrets management" wording and does not imply
  agents should print, reveal, inspect, or directly handle secret values,
- review guidance checks bugs, scope, tests, maintainability, and
  over-engineering,
- existing platform skills or commands that could overlap with the harness are
  recorded with a merge, adapt, leave-alone, or defer decision,
- tests, linting, and type checking are either included or explicitly opted out
  with a future default where useful,
- a post-install communication audit records what fresh agents can understand
  and what they may still misunderstand,
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
Agents may create a temporary local draft in a gitignored location such as
.agent/work/, but the durable brief lives in Jira.
If the temporary draft gains progress, evidence, blockers, or plan changes,
post those updates back to Jira before removing the local draft.
```

#### Repo File

Possible locations:

```text
docs/work/<ticket-id>.md
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

### Local Fallback

When the canonical brief location is external, choose a local fallback for
agents that cannot access the external store.

Recommended default:

```text
Canonical work brief location: <tracker>.
Local fallback: .agent/work/ or another gitignored directory.
Commit policy: do not commit local fallback brief instances. If the team wants
versioned in-repo briefs, choose a durable repo path such as docs/work/ as the
canonical location.
Sync rule: if local fallback state changes, copy the durable summary back to
the tracker before considering the work handed off.
```

Add the fallback directory to `.gitignore` when it is introduced.

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

## Repo Checks Discovery Recipe

`scripts/repo-checks.sh` should encode the repo's current deterministic checks
contract.
The agent should derive that contract from evidence.

The proposal should distinguish:

- canonical full-repo deterministic checks,
- focused validation for a subsystem, package, agent, or component,
- CI-only verification that is not practical locally,
- manual acceptance evidence for behavior, external systems, schedules,
  integrations, runtime boundaries, or secrets management.

Prefer reusing or wrapping existing commands over replacing them. A new
`scripts/repo-checks.sh` can be valuable when it gives agents one stable command,
but it should call the repo's existing test, lint, type-check, or validation
entrypoints where practical.

### Discovery Order

1. Inspect CI workflows.
2. Inspect documented setup and test commands in README or CONTRIBUTING.
3. Inspect project config.
4. Inspect existing task runners, scripts, and package/build entrypoints.
5. Inspect test directories and naming conventions.
6. Prefer commands the repo already uses over commands the agent happens to
   prefer.
7. If commands conflict, surface the conflict in the Harness Fit Proposal.
8. If tests, linting, or type checking are missing, record an explicit opt-out
   or human-approved addition rather than silently deferring it.

### Command Selection Rules

Prefer the highest-level command the repo already uses.

Examples without naming target-specific tools:

```text
If CI runs a single project checks command, use that command.
If README documents a local test command, use that command.
If an existing script wraps tests, linting, and type checking, use that wrapper.
If only lower-level tool config exists, propose the smallest command derived
from that config and record the evidence.
```

Do not add a new tool during harness installation unless the human agrees.

### Generic `repo-checks.sh` Template

```sh
#!/usr/bin/env sh
set -eu

# Canonical deterministic checks for this repo.
# Installed by the minimal agent harness as the repo checks entrypoint.
# Scope: lint/typecheck/tests/build checks for product code, not harness validation.
#
# Keep this aligned with CI where practical.

run() {
  echo "+ $*"
  "$@"
}

# Replace these commands with the repo's existing deterministic checks.
# Prefer commands already documented in README, CI, existing scripts, or
# package/project config.
# If no command can be confirmed, leave this explicit failure in place instead
# of guessing.

echo "No canonical repo checks command has been configured for this repo." >&2
echo "Replace this placeholder with commands derived from repo evidence." >&2
exit 1
```

### Existing Wrapper Example

```sh
#!/usr/bin/env sh
set -eu

run() {
  echo "+ $*"
  "$@"
}

run <existing-project-verification-command>
```

### If Verification Is Missing

If no reliable command can be inferred:

1. do not invent a full verification stack,
2. create `scripts/repo-checks.sh` with an explicit placeholder,
3. record the missing repo checks command as a gap,
4. recommend the smallest next action.

Example placeholder:

```sh
#!/usr/bin/env sh
set -eu

echo "No canonical repo checks command has been configured for this repo." >&2
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
- repo checks command,
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
Keep shared policy in AGENTS.md, scripts/repo-checks.sh, work-brief skill bundles,
and portable skill guidance. Make adapters thin wrappers around those shared
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
Install harness-provided skill source files to
.agents/skills/harness-<skill-name>/SKILL.md unless adapting to an existing
repo convention.

Keep shared skill guidance portable. Use adapters only for tool-specific
loading behavior or limitations. If the target repo already has review,
implementation, work-brief, run, verify, debug, or diagnose skills or
commands, record whether the harness skill is added, adapted, merged,
supersedes the existing skill, or is deferred.
```

If Claude Code native skills are installed, create `.claude/skills/<skill>/`
as a platform adapter rather than a second canonical skill body. The Claude
`SKILL.md` wrapper should keep Claude Code frontmatter, including fields such
as model or tool declarations when the target repo uses them, and its body may
delegate to the shared `.agents/skills/<skill>/SKILL.md` with an `@` import.
Record the wrapper path, shared source path, and preserved Claude frontmatter
fields in the fit proposal.

When Claude Code is in scope, mention bundled Claude Code skills and workflows
such as `/code-review`, `/debug`, `/run`, and `/verify`. Ask whether they
should stay enabled and documented, be treated as secondary to repo-specific
guidance, or be disabled through Claude Code settings such as
`disableBundledSkills` or the `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` environment
variable.

### Hooks

Hooks are optional in the starter installation.

Default:

```text
Start with scripts/repo-checks.sh as the contract. Add hooks only if the team wants
automatic enforcement or repeated failures show that agents forget the command.
```

A narrow Stop hook that runs `scripts/repo-checks.sh` is a common Level 1 starter
pull-in when the checks are real, reasonably fast, and actionable. Treat
broader hook systems, secret guards, destructive-action policy, cross-platform
hook runners, and CI/pre-commit parity as selected Level 3 deterministic
controls.

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

Installation mode:

Installation completeness:

Behavioral completeness:

Selective pull-ins from higher levels:

Intentionally deferred:

Smallest useful installation:
-
```

## Common Installation Shapes

### Tiny Repo With No Agent Harness

Recommended target:

```text
Target maturity: Level 0 table stakes
Installation mode: canonical or starter depending on existing repo surfaces
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
Target maturity: Level 1 bounded work execution
Installation mode: canonical when all Level 0 and Level 1 manifest assets are
installed or already satisfied; starter when only selected Level 1 behavior is
installed.
```

Create:

- the Level 0 assets from `manifests/level-0.yml`
- the additive Level 1 assets and behaviors from `manifests/level-1.yml`.

Decision:

- canonical work brief lives in Jira ticket/comment or repo file.
- local fallback and commit policy are explicit.
- missing lint, format, and type-check commands are included or explicitly
  opted out.

Add:

- acceptance evidence standard,
- non-goals and interface sections for boundary-changing work,
- implementation guidance for agents working from briefs.

Defer:

- tracker automation unless it clearly helps seed the brief.

### Repo With Useful But Scattered Docs

Recommended target:

```text
Target maturity: Level 1 plus selected Level 2 context routing
Installation mode: starter unless the proposal includes all required assets
and behaviors for the claimed levels.
```

Add:

- short project-doc routing note,
- maybe `SPEC-MAP.md` if there are multiple areas.

Defer:

- `CONTEXT.md` unless vocabulary confusion is recurring.

### Repo With Repeated Mechanical Failures

Recommended target:

```text
Target maturity: Level 1 plus selected Level 3 deterministic controls
Installation mode: starter unless the proposal includes all required assets
and behaviors for the claimed levels.
```

Add:

- `scripts/repo-checks.sh`,
- early Stop hook running `scripts/repo-checks.sh` when the command is real,
  reasonably fast, and actionable,
- pre-commit or broader hooks only if the team wants stronger automatic
  enforcement,
- CI parity if CI already exists or is in scope.

Defer:

- broader maintainability automation.

## Done Criteria For Harness Installation

The implementation is done when:

- the chosen maturity target, provenance, and deferrals are recorded in
  `docs/harness/README.md`,
- the chosen installation mode, installation completeness, and behavioral
  completeness claims are recorded,
- the final Harness Fit Proposal or equivalent decision log is durable under
  `docs/harness/`,
- temporary proposal paths are not copied into durable harness docs,
- the human has agreed to the starter shape or explicitly delegated the choice,
- all agreed starter files exist,
- `scripts/repo-checks.sh` either runs real repo checks or clearly fails with an
  honest placeholder,
- the Agent Work Brief has a chosen placement and lifecycle,
- any local work-brief fallback is gitignored, and any durable in-repo briefs
  use an explicit canonical repo path,
- the final report separates mechanical verification from acceptance evidence,
- side-effect evidence covers external systems, secrets management, schedules,
  deployment behavior, integrations, and runtime boundaries when relevant,
  without exposing sensitive values,
- existing harness-like components and platform skills have recorded handling
  decisions,
- tests, linting, and type checking are either included or explicitly opted out,
- optional components are deferred with reasons and future signals,
- the post-install communication audit is recorded,
- a fresh agent can read `AGENTS.md` and know how to proceed,
- the final report lists files changed, commands run, acceptance evidence,
  gaps surfaced, and deferred work.

## Final Report Format

After implementation, report:

```md
## Harness Installed

Target maturity:

Installation mode:

Installation completeness:

Behavioral completeness:

Harness Fit Proposal / decision log:
- Durable post-install path:

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

Existing component decisions:
-

Skill or command conflict decisions:
-

Tests / lint / type check:
-

Communication audit:
-

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

Before finishing installed docs, run this wording check:

- Does any phrase claim a maturity level that is only a target?
- Does any phrase imply agents should access, print, inspect, or directly
  handle sensitive values instead of validating secrets management wiring?
- Does durable documentation point to a machine-local path such as
  `../harness-framework` instead of the portable source name
  `harness-framework`?
- Does any durable doc record `/tmp` state or another machine-local path?
- Does the doc distinguish required behavior from optional guidance?
- Does the doc tell ordinary implementers to read `docs/harness/` when they
  only need the work brief, project docs, and code?

The goal is not to maximize harness maturity. The goal is to install the
smallest harness that makes agents and humans more effective now, while making
the next useful layer obvious when the project earns it.
