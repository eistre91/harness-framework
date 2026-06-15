---
name: harness-review
description: Reviews implementation against an Agent Work Brief with findings-led focus on bugs, scope, evidence, maintainability, and over-engineering. Use when reviewing a completed change, PR, commit, or working tree against a brief.
maturity: level-0
install_when: Agents or humans need a reusable review lens for harness-managed work.
repo_specific_adaptation: Review output format, severity scale, and project-specific risks.
---

# Harness Review

Use when reviewing implementation against an Agent Work Brief.

## Goal

Protect value delivery as well as correctness. A good change satisfies the brief
with the least structure that is clear and maintainable.

Review the change critically against the brief, the diff, and the evidence.
Do not edit files while using this skill. Lead with findings; keep summaries
brief and secondary.

Treat unearned abstraction, broad cleanup, new dependencies, or extra process as
findings when the brief did not justify them.

## Review Independence

Before reviewing, state one of:

- Independent review: I did not implement this change in this context.
- Self-review: I implemented this change or share the implementation context.

Self-review is allowed, but lower-confidence. For standard or
boundary-changing work, recommend an independent review before merge or
handoff when practical.

## Check

1. Scope and intent:
   - requested value delivered,
   - missed requirements,
   - scope creep,
   - YAGNI violations or unearned generality,
   - acceptance evidence gaps,
   - docs impact marked none / maybe / required.
2. Architecture and design:
   - module responsibilities,
   - unclear or unstable interfaces,
   - premature abstractions,
   - unnecessary dependencies,
   - misuse of existing project patterns.
3. Code quality and maintainability:
   - readability and local consistency,
   - KISS violations,
   - maintainability risks for future humans and agents,
   - docs or comments drifting from code,
   - retired imports, routes, scripts, aliases, or references still present
     after removals, moves, cleanup, or narrowed interfaces.
4. Tests:
   - behavior changes covered by meaningful tests,
   - tests exercise public interfaces or behavior boundaries,
   - tests describe observable behavior, not implementation details,
   - test names use project or domain language and read like behavior
     specifications,
   - bug fixes include a regression test where practical,
   - test effort focuses on critical paths and complex logic, not every
     possible edge case,
   - selection, routing, snapshot, fallback, or ordering logic includes a
     competing or stale candidate case when practical,
   - mocks stay at system boundaries such as external APIs, time,
     randomness, filesystem, or databases when needed,
   - tests do not mock internal collaborators or assert on private methods,
     call counts, or call order unless that interaction is the public contract.
5. User experience:
   - behavior is coherent from the user's perspective,
   - small polish gaps matter only when they materially affect the outcome.

## Finding Format

Number every finding with a stable ID so follow-up work can cite it:

- `CR-1`, `CR-2`, `CR-3`, etc.

For each finding, include:

- severity,
- file or behavior reference,
- why it matters,
- suggested fix or decision needed.

If there are no findings, say so and note any residual verification gaps.
