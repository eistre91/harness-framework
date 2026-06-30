# Harness Fit Proposal

This file records the final approved harness installation proposal or equivalent
decision log. It is durable repo documentation. Do not record machine-local
paths or temporary installation-session proposal paths here.

Use this template for the current approved stage. Fill or keep only the
sections that apply to that stage. Do not use a Level 0 proposal to approve
later-stage assets.

## Repo Signals

-

## Existing Harness Components

| Component | Appears to do | Harness principle satisfied | Handling | Human decision |
| --- | --- | --- | --- | --- |
|  |  |  | thread through / adapt / supersede / leave alone / defer |  |

## Skill And Command Conflict Audit

| Platform or path | Existing skill/command | Overlap | Handling | Human decision |
| --- | --- | --- | --- | --- |
|  |  | review / implement / work brief / diagnose-debug / run-checks / other |  |  |

Claude Code note, when relevant:

- bundled skills such as `/code-review`, `/debug`, `/run`, and `/verify`
  remain enabled / are secondary / are disabled by user or project settings,
- disable mechanism, if chosen: `disableBundledSkills` or
  `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`,
- native skill adapter decision: none / generated mirror with
  `scripts/sync_claude_skills.py` / symlink / thin wrapper with Claude
  frontmatter and `@` import,
- Claude mirror or wrapper frontmatter to preserve or add, such as `model`,
  `allowed-tools`, `effort`, `context`, `hooks`, or `paths`:
- sync/check command, when using generated mirrors:
- reason:

## Current Stage Assessment

-

## Stage Target

- Current stage:
- Target maturity:
- Installation mode: canonical / starter / overlay
- Stage asset completeness:
- Stage behavioral completeness:
- Maturity wording to use in installed docs:

## Manifest Inclusion Table

Use the current stage manifest as the source of truth. Do not use this table to
preselect future-stage or optional assets during a Level 0 stage.

| Stage | Asset or behavior | Status | Reason | Revisit signal |
| --- | --- | --- | --- | --- |
| current |  | include / adapt / already satisfied / defer / exclude |  |  |

## Project Context And Intent

Use when project context or intent is in the current approved stage.

- Existing project context docs:
- Existing project intent source:
- `docs/project/intent.md` decision: include / adapt existing / defer / exclude
- Reason:
- Revisit signal:
- Routing note:
  planning and value-sensitive review only / explicitly routed implementation
  context / other:

## Work Brief Storage

- Canonical location:
- Local fallback when canonical store is unavailable:
- Commit policy for brief instances:
- Sync rule back to canonical location:
- Durability rationale:
- Stale brief mitigation when briefs are committed:

## Tests, Lint, And Type Checking

| Capability | Existing command | Decision | Reason / future default |
| --- | --- | --- | --- |
| Tests |  | include / add / omit with reason / waiver |  |
| Lint |  | include / add / omit with reason / waiver |  |
| Type check |  | include / add / omit with reason / waiver |  |

## Acceptance Evidence

| Kind | Command or evidence | Status | Notes |
| --- | --- | --- | --- |
| Manual acceptance evidence |  | include / not applicable |  |

## Later Deterministic Controls

Use only when the current approved stage includes Level 3 deterministic
controls or an explicit selected pull-in. Do not use this section to approve
future-stage assets during Level 0.

| Candidate | Existing command or evidence | Status | Notes |
| --- | --- | --- | --- |
| Focused subsystem validation |  | observation / include now / defer |  |
| CI-only verification |  | observation / include now / defer |  |
| Format checks |  | observation / include now / defer |  |
| Build/package checks |  | observation / include now / defer |  |
| Static analysis |  | observation / include now / defer |  |

## Gaps Surfaced

Affects harness now:

-

Future improvement:

-

## Trade-Offs

-

## Human Decisions

-

## Intentionally Deferred

| Component | Why deferred | Revisit signal |
| --- | --- | --- |
|  |  |  |

## Out-Of-Stage Observations

Record plain observations found during the current stage. Do not classify them
by future maturity level or preselect future assets unless the human has
approved that stage.

-

## Context Used

Framework sources:

-

Target repo sources:

-

Out-of-stage sources used and justification:

-

## Files Proposed Or Installed

Create:

-

Edit:

-

## Acceptance Criteria

-

## Communication Audit

- A fresh agent can now understand:
- A fresh agent may still misunderstand:
- Terms that need clearer wording:
- Deferred decisions that must not be mistaken for completed maturity:
