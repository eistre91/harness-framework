# Minimal Agent Harness Implementation Guide

Audience: agents and maintainers fitting this framework to a target repo.

Use when: inspecting a repo, proposing the smallest useful harness shape, and
installing only the approved assets.

This guide turns the framework into an installation process. The central rule
is:

```text
Harness implementation is repo diagnosis plus collaborative workflow design,
not blind template installation.
```

The framework explains what the harness is and why it is shaped that way:
`docs/framework.md`.

The principles are the decision lens for installing, adapting, deferring, or
rejecting components: `docs/principles.md`.

## Source Of Truth Map

- Maturity levels, installation modes, asset completeness, behavioral
  completeness, and level-specific signals: `docs/maturity-model.md`
- Bootstrap, Level 0, Level 1, and optional asset lists:
  `manifests/bootstrap.yml`, `manifests/level-0.yml`,
  `manifests/level-1.yml`, and `manifests/optional-assets.yml`
- Portable asset boundaries: `docs/portable-assets.md`
- Platform support: `docs/platform-support.md`, then the relevant platform note
- Harness Fit Proposal template:
  `templates/core/docs/harness/fit-proposal.md`
- Installed harness docs template: `templates/core/docs/harness/README.md`
- Target-repo checks template: `templates/core/scripts/repo-checks.sh`
- Work brief skill and template: `skills/core/harness-work-brief/`

Do not maintain second copies of those assets or schemas in this guide.

## Installation Modes

Every Harness Fit Proposal must state:

- target maturity: the behavior the repo is being fitted toward,
- installation mode: `canonical`, `starter`, or `overlay`,
- asset completeness: full / partial / mostly existing,
- behavioral completeness: whether the workflow is usable,
- deferred manifest assets and why they are not installed now.

When installation is partial, use precise wording:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
Deferred manifest assets are listed below with reasons and revisit signals.
```

Do not describe a repo as having completed a level unless the manifest assets
and intended behavior for that claim are actually complete or already
satisfied.

## Operating Rules

### Collaborate Before Editing

Before creating or changing target-repo files, write a Harness Fit Proposal and
present the exact proposal text to the human. Do not edit the repo until the
human explicitly approves the harness shape or corrects the proposal.

The proposal should explain:

- repo signals,
- current observed maturity,
- recommended target maturity,
- installation mode and completeness,
- files to create or edit,
- defaults inferred from repo evidence,
- gaps found,
- intentional deferrals,
- questions that require human judgment.

Do not ask questions whose answers can be discovered from the repo. Inspect
first, infer defaults, and ask only questions that materially affect the
harness shape.

If unresolved trade-offs remain, do not treat silence, branch creation, or a
broad "carry it out" as approval of those decisions.

### Start Lower Than Feels Ambitious

Most repos should start with Level 0 or Level 1. Adding a large harness too
early creates harness debt: too many docs, instructions, hooks, artifacts, and
process surfaces that nobody maintains.

A small harness that is used is more valuable than a complete harness that
people work around.

### Surface Gaps Without Owning Every Gap

Harness installation may reveal missing engineering hygiene, such as no test
command, no CI, no linting, no clear work tracker, stale README instructions,
or no sensitive-file policy.

Surface those gaps, but do not turn harness installation into a broad
modernization project unless the human explicitly chooses that scope.

Tests, linting, and type checking are important for agent performance. The
proposal should either include existing commands in `scripts/repo-checks.sh` or
explicitly opt out of missing ones for this install.

Separate gaps into:

```text
Affects harness now:
  must be resolved or explicitly defaulted to install the starter harness

Future improvement:
  worth recording, but not part of this installation
```

### Argue For Complexity

When proposing a component beyond Level 0, state:

- what failure it prevents,
- what signal proves the repo needs it,
- what maintenance cost it adds,
- what simpler option was considered,
- what would justify removing or simplifying it later.

Deferring a component is a design decision, not neglect. Record the reason and
the signal that should trigger reconsideration.

## Implementation Flow

Follow this sequence.

### 1. Inspect The Repo

Read enough to understand workflow and verification without consuming
unnecessary context.

Suggested inspection targets:

- repo root listing,
- `README*`,
- existing `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.codex/`, `.agents/`,
- platform skills or commands such as `.claude/skills/`,
  `.claude/commands/`, `.agents/skills/`, Cursor rules, or local team command
  directories,
- CI workflows such as `.github/workflows/*`,
- package, build, or project config files,
- existing task runners and scripts,
- test directories,
- docs directories,
- tracker references in README, CONTRIBUTING, or issue templates,
- `.gitignore` for local state and secret patterns.

Do not read every source file. The goal is harness fit, not full codebase
comprehension.

### 2. Identify Existing Signals

Classify what already exists:

- agent entrypoint: present / absent / stale / unclear,
- entrypoint fit: universal and concise / too broad / too long / over-routed,
- work source: Jira / GitHub Issues / Linear / chat / docs / unknown,
- verification: documented / inferred from CI / inferred from config / missing,
- project docs: none / small / useful but unrouted / large enough to route,
- sensitive files: obvious / not obvious / existing policy,
- agent tools: Codex / Claude / Cursor / mixed / unknown,
- existing harness components: none / entrypoint / skills / repo checks /
  hooks / work docs / other,
- skill or command conflicts: review-like / implement-like / work-brief-like /
  diagnose-debug-like / run-checks-like / unknown,
- CI: present / absent / not inspected.

Treat existing components as evidence first. For each overlapping component,
record:

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

Use `docs/maturity-model.md` to decide the smallest useful target. The proposal
must explicitly state current observed maturity and recommended target
maturity.

Include:

- current observed level, evidence, and gaps,
- recommended target level,
- installation mode,
- asset completeness claim,
- behavioral completeness claim,
- selected pull-ins from higher levels,
- components intentionally not added,
- why this target fits,
- signal to expand later.

### 4. Prepare A Harness Fit Proposal

Before editing, prepare a Harness Fit Proposal using the canonical schema in
`templates/core/docs/harness/fit-proposal.md`.

The proposal must include decisions for:

- repo signals and existing harness components,
- entrypoint fit, including any recommendation to split non-universal
  `AGENTS.md` content into skills, scripts, project docs, hooks, or review
  guidance,
- skill and command conflicts,
- current and target maturity,
- installation mode and completeness,
- manifest inclusion or deferral,
- work brief storage, durability rationale, local fallback, commit policy,
  stale brief mitigation, and sync rule,
- verification, focused validation, CI-only checks, and manual evidence,
- tests, lint/format, and type checking,
- gaps, trade-offs, human decisions, deferred items, proposed files,
  acceptance criteria, and communication audit.

Persist the proposal to disk before editing. Ask for a preferred path only if
the target repo already has a clear planning location or the human is likely to
care. Otherwise use a temp path such as:

```text
/tmp/<target-repo-name>-harness-fit-proposal.md
```

After writing the temporary proposal, present the exact proposal text to the
human. A short summary is fine, but it must not replace the full proposal.

`/tmp` is not durable repo documentation. After installation, record only the
final proposal or equivalent decision log under `docs/harness/`, either as
`docs/harness/fit-proposal.md` or embedded in `docs/harness/README.md`. Do not
copy temporary proposal paths into durable harness docs.

If the proposal changes after human questions are answered, update the
persisted plan before editing files.

Use recommendations instead of open-ended questions where possible:

```text
I found a test command in CI and no lint command. I recommend
scripts/repo-checks.sh run the existing test command only for now and record
linting as a future improvement. Do you want linting added now despite it not
already existing?
```

### 5. Ask Focused Human Questions

Ask only questions that affect implementation.

Ask this minimum decision set unless the answer is both obvious from repo
evidence and low-risk:

- Should this install mode be `canonical`, `starter`, or `overlay`?
- Where should canonical Agent Work Briefs live?
- Why is that durability choice the right trade-off for this repo now?
- What local fallback should agents use when the canonical brief store is
  unavailable?
- Should brief instances live only in the external tracker, in a durable repo
  path, or as gitignored local fallback drafts?
- If briefs are committed, how should stale or completed briefs be audited,
  archived, or removed?
- Should missing test, lint/format, or type-check tools be added now or
  explicitly deferred?
- Are any files, directories, services, or data sources off limits to agents?
- How should existing platform skills, commands, or review flows be merged,
  namespaced, documented, or deferred?
- Should the final fit proposal be committed under `docs/harness/`, or should
  equivalent decisions be embedded in `docs/harness/README.md`?

For each question, provide:

```text
Recommended default:
Why:
Trade-off:
When to revisit:
```

Before editing, use a final checkpoint:

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

Create or edit only the agreed files. Use the manifests to select assets and
the templates as starting points.

Keep installed content short. The starter harness should make the next agent
more effective without making the repo feel process-heavy.

Do not add a new tool, dependency, hook system, tracker adapter, or platform
adapter unless the proposal records human approval or clear repo evidence.

### 7. Validate The Harness

After implementation, check that a fresh agent could:

- find the repo entrypoint,
- find the durable Harness Fit Proposal or equivalent decision log under
  `docs/harness/`,
- understand where work comes from,
- create or read an Agent Work Brief,
- understand that harness skills are used by phase and not as one combined
  reading list,
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
- `AGENTS.md` contains only instructions every agent needs for ordinary work,
  with phase-specific, product/domain, or rare-task guidance routed elsewhere,
- the work-brief skill bundle can turn a tracker item, issue, or chat request
  into executable work,
- `scripts/repo-checks.sh` exists and either runs real repo checks or clearly
  fails with an honest placeholder,
- repo checks commands are derived from repo evidence or clearly marked as
  placeholders,
- `docs/harness/README.md` records provenance, target maturity, installation
  mode, completeness, installed files, and intentional deferrals,
- the final proposal or equivalent decision log is durable under
  `docs/harness/`,
- acceptance evidence is required for externally visible or boundary-changing
  behavior,
- `AGENTS.md` tells agents to use work-brief, implementation, and review skills
  by phase,
- non-trivial work can get independent review in a separate context when
  practical,
- secrets management evidence does not imply agents should print, reveal,
  inspect, or directly handle secret values,
- review guidance checks bugs, scope, tests, maintainability, and
  over-engineering,
- existing platform skills or commands that overlap with the harness are
  recorded with a merge, adapt, leave-alone, or defer decision,
- tests, linting, and type checking are either included or explicitly opted out
  with a future default where useful,
- a post-install communication audit records what fresh agents can understand
  and what they may still misunderstand,
- optional components are explicitly deferred with signals for later adoption,
- the human can explain why the chosen maturity target fits the repo.

## Work Brief Lifecycle

The Agent Work Brief is the central work artifact. Do not leave its location or
durability implicit.

Supported patterns:

- External durable store: the brief lives in Jira, GitHub Issues, Linear, or
  another team source of truth.
- Repo durable store: the brief lives in a committed repo path such as
  `docs/work/<ticket-id>.md`.
- Local temporary store: the brief lives in a gitignored local path such as
  `.agent/work/`.

Recommended default: use an external durable store when the team already has a
reliable tracker workflow and agents can read and update it. This keeps work
context visible to the team without turning the code repo into a planning
archive.

Repo durable storage is reasonable when the team wants shared agent-readable
work records, tracker access is weak, or a small repo benefits more from
visible collaboration than from minimizing documentation surface. The cost is
long-term maintenance: committed briefs can go stale, duplicate tracker truth,
and confuse future agents. If committed briefs are used, record status, source,
owner, and supersession/archive state.

Local temporary storage is convenient for drafting and for sessions that
cannot access the canonical store. It is not shared provenance. Use it only as
a fallback or for tiny work where losing continuity is acceptable. Copy durable
progress, evidence, blockers, and accepted plan changes back to the canonical
location before handoff.

When the canonical brief location is external, choose a local fallback:

```text
Canonical work brief location: <tracker>.
Local fallback: .agent/work/ or another gitignored directory.
Commit policy: do not commit local fallback brief instances.
Sync rule: if local fallback state changes, copy the durable summary back to
the tracker before considering the work handed off.
```

Add the fallback directory to `.gitignore` when it is introduced.

Use PR descriptions to summarize the brief and evidence, not as the canonical
planning surface. Use chat-only briefs only for tiny work where loss of
continuity is acceptable.

A simple lifecycle is enough:

```text
Draft -> Ready For Implementation -> Implemented -> Verified -> Reviewed
```

Do not add more states until the team needs them.

For work that spans sessions, the canonical brief should capture:

- current status,
- plan changes,
- divergences from the expected approach and why they were accepted,
- blockers,
- latest evidence,
- next action.

Ownership:

- the human owns product intent, trade-offs, and the risk of delegated choices,
- the planning agent owns converting intent into an executable brief,
- the implementation agent owns carrying out the brief and producing evidence,
- the reviewer owns checking whether the change satisfies the brief and whether
  the implementation introduces unacceptable risk or debt, including latent
  decisions that should return to human ownership.

## Repo Checks Discovery

`scripts/repo-checks.sh` should encode the repo's current deterministic checks
contract. Derive that contract from evidence.

The proposal should distinguish:

- canonical full-repo deterministic checks,
- focused validation for a subsystem, package, agent, or component,
- CI-only verification that is not practical locally,
- manual acceptance evidence for behavior, external systems, schedules,
  integrations, runtime boundaries, or secrets management.

Prefer reusing or wrapping existing commands over replacing them.

Discovery order:

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

Selection rules:

- prefer the highest-level command the repo already uses,
- use a single CI or project checks command when one exists,
- use README-documented local test commands when CI is absent or unsuitable,
- propose the smallest command derived from config when no wrapper exists,
- do not add a new tool during harness installation unless the human agrees.

Use `templates/core/scripts/repo-checks.sh` as the target-repo template. Do not
copy this framework repo's own `scripts/repo-checks.sh` into target repos.

If no reliable command can be inferred:

1. do not invent a full verification stack,
2. create `scripts/repo-checks.sh` with an explicit placeholder,
3. record the missing repo checks command as a gap,
4. recommend the smallest next action.

When the Claude Code generated skill mirror adapter is installed, add this
adapter health check to the target repo's adapted `scripts/repo-checks.sh`
unless the fit proposal records a deliberate reason not to:

```sh
python3 -m scripts.sync_claude_skills --check
```

Do not add that Claude mirror check to the base template by default. It applies
only when `scripts/sync_claude_skills.py` and `.claude/skills` mirrors are
installed in the target repo.

Keep command details in `scripts/repo-checks.sh`; do not maintain a second
command list in docs.

## Portability And Adapters

The harness should separate concepts from adapters.

Portable concepts:

- repo entrypoint,
- work brief,
- repo checks command,
- review guidance,
- acceptance evidence,
- maturity model,
- maintainability feedback.

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

Do not require an adapter unless the repo already uses that environment or the
human explicitly wants it.

When a repo uses multiple agentic coding tools, preserve the same behavior
where practical:

```text
Keep universal operating guidance in AGENTS.md, deterministic checks in
scripts/repo-checks.sh, and phase-specific workflow in work-brief bundles and
portable skill guidance. Make adapters thin mirrors, wrappers, or callers
around those shared contracts.
```

For hooks:

- prefer one shared script for verification, secret checks, or destructive
  action checks,
- have Codex, Claude Code, pre-commit, and CI call that shared script where
  possible,
- keep output shape and failure meaning consistent across tools,
- document unavoidable divergence in the adapter README.

If platform-specific support is in scope, read `docs/platform-support.md`, then
the specific platform note for the adapter being installed. Do not load those
docs for ordinary product work or for a basic Level 0 install that does not add
platform-specific settings, hooks, or skill adapters.

## Skills

Install harness-provided skill source files to:

```text
.agents/skills/harness-<skill-name>/SKILL.md
```

Adapt that path only when the target repo has a stronger convention.

Keep shared skill guidance portable. Use adapters only for tool-specific
loading behavior or limitations. If the target repo already has review,
implementation, work-brief, run, verify, debug, or diagnose skills or
commands, record whether the harness skill is added, adapted, merged,
supersedes the existing skill, or is deferred.

If Claude Code native skills are installed, follow
`docs/platforms/claude-code.md` and the `claude-skill-mirrors` optional asset
manifest entry. Record the mirror path, shared source path, sync command,
preserved Claude frontmatter fields, and any deliberate wrapper-import
exception in the fit proposal.

When Claude Code is in scope, mention bundled Claude Code skills and workflows
such as `/code-review`, `/debug`, `/run`, and `/verify`. Ask whether they
should stay enabled and documented, be treated as secondary to repo-specific
guidance, or be disabled through user or project Claude Code settings such as
`disableBundledSkills` or `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`.

## Hooks

Hooks are optional in the starter installation.

Default:

```text
Start with scripts/repo-checks.sh as the contract. Add hooks only if the team
wants automatic enforcement or repeated failures show that agents forget the
command.
```

A narrow Stop hook that runs `scripts/repo-checks.sh` is a common Level 1
starter pull-in when checks are real, reasonably fast, and actionable. Treat
broader hook systems, secret guards, destructive-action policy, cross-platform
hook runners, and CI/pre-commit parity as selected Level 3 deterministic
controls. Level 3 safety policy should also cover protected paths, protected
command families, ask/warn/block behavior, and whether an operation is safe for
the specific tool call, including whether a command can run concurrently in the
current context.

## Starter Assets

The source-of-truth asset selections live in manifests:

- `manifests/bootstrap.yml`
- `manifests/level-0.yml`
- `manifests/level-1.yml`
- `manifests/optional-assets.yml`

Use those files to decide what to copy or adapt. The examples in this guide
explain how to adapt assets; they are not separate asset lists.

Common install shapes:

- Tiny repo with no agent harness: usually Level 0 canonical or starter.
- Jira-centered team with vague tickets: usually Level 1 bounded work
  execution, with canonical briefs in Jira ticket/comment or a repo file.
- Repo with useful but scattered docs: Level 1 plus selected Level 2 context
  routing; maybe `SPEC-MAP.md` if there are multiple areas.
- Repo with repeated mechanical failures: Level 1 plus selected Level 3
  deterministic controls; maybe a Stop hook running `scripts/repo-checks.sh`.

In all cases, defer assets that lack evidence or human preference, and record
the revisit signal.

## Done Criteria

The installation is done when:

- the chosen maturity target, provenance, and deferrals are recorded in
  `docs/harness/README.md`,
- installation mode, installation completeness, and behavioral completeness
  claims are recorded,
- the final Harness Fit Proposal or equivalent decision log is durable under
  `docs/harness/`,
- temporary proposal paths are not copied into durable harness docs,
- the human has agreed to the starter shape or explicitly delegated the choice,
- all agreed starter files exist,
- `scripts/repo-checks.sh` either runs real repo checks or clearly fails with
  an honest placeholder,
- the Agent Work Brief has a chosen placement and lifecycle,
- any local work-brief fallback is gitignored,
- any durable in-repo briefs use an explicit canonical repo path,
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

## Final Report

After installation, report:

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

## Wording Check

Before finishing installed docs, check:

- Does any phrase claim a maturity level that is only a target?
- Does any phrase imply agents should access, print, inspect, or directly
  handle sensitive values instead of validating secrets management wiring?
- Does durable documentation point to a machine-local path such as
  `../harness-framework` instead of the portable source name
  `harness-framework`?
- Does any durable doc record `/tmp` state or another machine-local path?
- Does the doc distinguish required behavior from optional guidance?
- Does `AGENTS.md` include only guidance that is broadly applicable to ordinary
  repo work, rather than product strategy, one-off standards, historical notes,
  or phase-specific instructions better owned by skills or focused docs?
- Does the doc tell ordinary implementers to read `docs/harness/` when they
  only need the work brief, project docs, and code?

The goal is not to maximize harness maturity. The goal is to install the
smallest harness that makes agents and humans more effective now, while making
the next useful layer obvious when the project earns it.
