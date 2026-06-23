# Level 5 Orchestration Sketch

Audience: agents and maintainers evolving Level 5 orchestration and automation
guidance.

Status: exploratory. `docs/maturity-model.md` remains the source of truth for
the Level 5 maturity definition. This document captures emerging operating
language that should be refined before it becomes installable guidance.

## Purpose

Level 5 is for larger or more agent-heavy projects where execution,
coordination, validation, or harness improvement needs explicit orchestration.
That can include work that cannot reliably fit inside one agent context, one
brief, one implementation pass, or one reviewer pass, as well as unattended
runners, structured protocols, eval suites, tracker adapters, and multi-agent
coordination rules. It introduces more explicit orchestration while preserving
human ownership of strategy, product meaning, architecture direction, priority,
trade-offs, and acceptable risk.

The goal is not to maximize autonomy. The goal is to let larger work survive
fresh contexts, repeated attempts, independent validation, and human-required
checkpoints without losing intent or state.

## Work Hierarchy

Use these terms as current working language:

- Initiative: a larger feature, PRD, design, or body of work that decomposes
  into multiple agent-executable work units.
- Work item: the external source of requested work, such as a tracker ticket,
  issue, PRD section, or human request.
- Work unit: the agent-executable slice, usually represented by an Agent Work
  Brief or equivalent executable scope.
- Attempt: one bounded execution pass against a work unit, with actor, status,
  files touched, decisions, divergences, evidence, blockers, and next action.

The storage system is deliberately unspecified. Jira, GitHub Issues, Linear,
repo files, PRs, or a dedicated coordination store can satisfy the contract if
future agents and humans can recover intent, status, evidence, and next action.

## Phase Artifacts

Complex work often separates the primitive verbs into distinct contexts:

```text
research -> plan -> implement -> validate
```

Candidate phase artifacts:

- Research notes: relevant code, docs, prior decisions, external references,
  repo conventions, risks, and open questions.
- Plan or Agent Work Brief: intended outcome, non-goals, boundary, accepted
  decisions, human checkpoints, verification, acceptance evidence, and split
  work units when needed.
- Implementation artifact: code, docs, generated output, configuration, or
  other produced work, plus recorded divergences from the plan.
- Validation report: verification results, review findings, acceptance
  evidence, residual risks, and recommended next action.
- State update: durable status, blockers, evidence, decisions, divergences, and
  next action copied back to the canonical work source.

These artifacts should be as small as possible while still allowing a fresh
agent or human to continue without relying on chat history.

## Validation Result Sketch

For orchestrated work, validation may eventually report one of:

- Pass: the work satisfies the brief and no material residual risk is known.
- Pass with risks: the work may be acceptable, but residual risk, incomplete
  scope, uncertain acceptance, or trade-off debt requires explicit human
  approval before closeout.
- Fail: the work does not satisfy the brief, verification failed, review found
  material issues, or acceptance evidence is insufficient.

This schema is provisional. Future guidance may need separate states for
blocked work, missing human decisions, unavailable environments, or validation
that cannot be completed.

## Human-Required Checkpoints

Human-required checkpoints mark places where the harness cannot own the next
decision. They may require:

- clarification of missing intent,
- approval of a plan,
- approval of an interface or long-living decision,
- acceptance of residual risk,
- evaluation of acceptance by seeing, using, or judging the result.

Move human decisions left when practical: planning should surface ambiguity,
trade-offs, and approval needs before implementation. Implementation should halt
only on material unexpected issues. Validation should surface residual risk,
incomplete intent satisfaction, and human acceptance needs before closeout.

Use checkpoints deliberately. Too many gates create decision fatigue and reduce
human leverage. Too few gates allow semantic drift, hidden risk, and software
that mechanically passes while drifting from product intent.

## Context Separation Signals

Split phases into separate contexts when one or more are true:

- the work spans multiple sessions, agents, issues, or owners,
- the research set is large enough to bias or overload implementation,
- the plan contains material product, interface, architecture, or sequencing
  decisions,
- implementation is likely to need multiple attempts,
- validation should be independent from implementation,
- residual risk may require human approval,
- state or evidence would otherwise be lost between contexts.

Tiny work may collapse all phases into one context. Standard work often
combines research and planning, and may combine planning and implementation when
scope is clear. Complex work usually benefits from separate research, planning,
implementation, and validation contexts with explicit artifacts.

## Open Questions

- What exact schema should validation reports use?
- Should "blocked" and "needs human decision" be validation results, work-unit
  states, or both?
- When should a target repo install a `harness-research` skill instead of
  adapting `harness-work-brief`?
- How should attempts relate to PR history, issue comments, review findings,
  and long-horizon initiative state?
- Which parts of this model are Level 5 only, and which should remain as
  explanatory language for Levels 0 through 4?
