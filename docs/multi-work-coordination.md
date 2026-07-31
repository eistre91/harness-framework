# Multi-Work Coordination Sketch

Audience: maintainers exploring how the emerging Multi-Work Coordination
capability could support larger outcomes composed of multiple bounded work
units.

Status: future-facing and non-authoritative. The Capability Map owns the
domain's outcome, boundary, prerequisites, selection guidance, and validation.
This sketch explores a possible operating model and implies no installable
package.

## Purpose

Use the Capability Map for the outcome, boundary, and selection guidance. This
sketch starts from that definition and explores candidate phase artifacts,
checkpoints, context boundaries, mechanisms, and open operating questions.

## Candidate Work Model

`docs/framework.md` owns shared work-model terminology. The Capability Map owns
the capability definition and its use of Initiative. This sketch uses those
terms without redefining them. The formal Session and Attempt model remains an
open decision in `TODO.md`.

The storage system is deliberately unspecified. Jira, GitHub Issues, Linear,
repo files, PRs, or a dedicated coordination store can satisfy the contract if
future agents and humans can recover intent, status, dependencies, evidence,
decisions, and next action.

## Candidate Phase Artifacts

Complex work often separates the primitive verbs into distinct contexts:

```text
research -> plan -> implement -> validate
```

Possible artifacts include:

- Research notes: relevant code, docs, prior decisions, external references,
  repo conventions, risks, and open questions.
- Plan or Agent Work Brief: intended outcome, non-goals, interface, accepted
  decisions, human checkpoints, verification, acceptance evidence, and split
  work units when needed.
- Implementation artifact: code, docs, generated output, configuration, or
  other produced work, plus recorded divergences from the plan.
- Validation report: verification results, review findings, acceptance
  evidence, residual risks, and recommended next action.
- State update: durable status, blockers, dependencies, evidence, decisions,
  divergences, and next action copied back to the canonical work source.

Keep these artifacts as small as possible while still allowing a fresh agent or
human to continue without relying on chat history.

## Validation Result Needs

A future validation contract must distinguish successful completion, retained
risk requiring human judgment, and work that cannot close. Exact result and
state names remain open in `TODO.md`.

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

Separate research, planning, implementation, or validation contexts when one or
more are true:

- work spans multiple sessions, agents, issues, work units, or owners,
- the research set is large enough to bias or overload implementation,
- the plan contains material product, interface, architecture, or sequencing
  decisions,
- implementation is likely to need multiple attempts,
- validation should be independent from implementation,
- residual risk may require human approval,
- state or evidence would otherwise be lost between contexts.

Tiny work may collapse all phases into one context. Standard work often
combines research and planning, and may combine planning and implementation when
scope is clear. Context separation alone does not imply Multi-Work
Coordination; multiple contributing work units do.

## Candidate Mechanisms

No mechanism is required merely because it appears here. Evidence may
eventually justify:

- PRD or technical-design lifecycle guidance,
- tracker adapters and durable work-state stores,
- structured final-output and validation protocols,
- coordinator, worker, integrator, and verifier roles,
- explicit ownership boundaries across work units,
- unattended or semi-unattended runners inside bounded human-approved intent,
- eval suites for harness behavior,
- operating modes for different coordination shapes,
- stricter file-access or execution controls when separately justified.

Adopt only the smallest mechanism that addresses a demonstrated coordination
cost. Keep a component brief for each new harness part, and simplify or remove
mechanisms that stop earning their maintenance cost.

## Open Questions

- What exact schema should validation reports use?
- Should `blocked` and `needs human decision` be validation results, work-unit
  states, or both?
- When should a target repo install a research skill instead of adapting the
  work-brief workflow?
- How should attempts relate to PR history, issue comments, review findings,
  and long-horizon initiative state?
- Which continuity and phase-separation practices belong to Bounded Work, and
  which dependency, ownership, integration, or closeout practices belong to
  Multi-Work Coordination?
- What evidence would justify an installable package rather than continued
  project-specific adaptation?
