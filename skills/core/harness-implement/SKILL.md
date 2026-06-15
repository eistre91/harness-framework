---
name: harness-implement
description: Implements an Agent Work Brief with narrow scope, boundary-level tests where practical, and explicit mechanical and acceptance evidence. Use when coding from a brief, ticket, or agreed implementation scope.
maturity: level-1
install_when: Agents will implement work from briefs or tickets.
repo_specific_adaptation: Verification command, project context paths, test conventions, and project-specific implementation risks.
---

# Harness Implement

Use when implementing an Agent Work Brief.

## Principles

- Implement the smallest valuable change that satisfies the brief.
- Respect non-goals and avoid speculative abstractions.
- Prefer existing project patterns over new dependencies or new architecture.
- When behavior changes, tests should verify observable behavior through a
  public interface or boundary, not private implementation details.
- Test names should use the repo's domain language and read like behavior
  specifications.
- Mock only at system boundaries such as external APIs, time, randomness,
  filesystem, or databases when needed.
- For selection, routing, snapshot, fallback, or ordering logic, include a
  competing or stale candidate case when practical.
- Focus test effort on critical paths and complex logic, not every possible
  edge case.

## Process

1. Read the brief and only the context needed for the task.
2. Confirm the tier and stop on ambiguities that materially affect scope,
   interface, verification, or acceptance.
3. Identify the behavior boundary: API, CLI, function, component, job, file
   format, integration, or user-visible workflow.
4. For behavior changes, use a vertical red-green loop where practical:
   - write one failing test for one observable behavior,
   - add only enough code to pass it,
   - repeat for the next behavior.
5. Avoid horizontal slicing: do not write a large batch of imagined tests and
   then a large batch of implementation.
6. Keep each cycle narrow:
   - one test at a time,
   - no speculative behavior for future tests,
   - no refactor while the suite is red.
7. Refactor only after tests are green; keep tests on public behavior so
   internal refactors do not break them.
8. Run the repo's canonical verification command before claiming done.
9. Provide mechanical evidence and acceptance evidence.
10. Prepare a handoff for an independent reviewer.
11. Call out any scope, design, or verification gaps.

## Guardrails

- Do not broaden the task without human approval.
- Do not add dependencies unless the brief or human approves the trade-off.
- Do not continue coding from a brief that lacks a necessary interface,
  behavior, or acceptance decision.
- If no meaningful test surface exists, say so and explain the residual risk.

## Final Evidence

Report:

- files changed,
- mechanical verification commands and results,
- acceptance evidence or "not applicable; behavior did not change",
- docs impact: none / maybe / required,
- negative proof for removals, moves, cleanup, or narrowed interfaces, when
  relevant,
- review handoff: brief/source, tier, changed files, behavior boundaries,
  test surfaces, and known risks,
- any remaining risks or follow-up work.
