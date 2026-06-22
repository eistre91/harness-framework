---
name: harness-review
description: Reviews implementation against an Agent Work Brief with findings-led focus on bugs, scope, evidence, maintainability, and over-engineering. Use when reviewing a completed change, PR, commit, or working tree against a brief.
---

# Harness Review

Use when reviewing implementation against an Agent Work Brief, tracker item, or
human-approved scope. In this skill, "Agent Work Brief" means the canonical work
source or equivalent executable scope the implementer was expected to satisfy.

## Goal

Protect value delivery as well as correctness. A good change satisfies the brief
with the least structure that is clear and maintainable.

Review the change critically against the brief, the diff, and the evidence.
Do not edit files while using this skill. Lead with findings; keep summaries
brief and secondary.

Treat unearned abstraction, broad cleanup, new dependencies, or extra process as
findings when the brief did not justify them.

Surface latent product, architecture, domain, priority, or risk decisions that
the implementation exposed but the brief did not settle. Review can identify
those decisions and recommend options; ownership returns to the human unless a
prior policy explicitly delegated the choice.

If `docs/project/intent.md` exists, consult it only for value-sensitive review,
such as when a change may satisfy the brief mechanically while drifting from the
project's stated problem, audience, direction, or value proposition.

## Review Independence

Before reviewing, state one of:

- Independent review: I did not implement this change in this context.
- Self-review: I implemented this change or share the implementation context.

Self-review is allowed, but lower-confidence. For standard or complex work,
recommend an independent review before merge or handoff when practical.

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
6. Security and operational risk:
   - secrets, credentials, tokens, sensitive URLs, and private state are not
     hardcoded, read unnecessarily, printed, copied, logged, serialized,
     committed, or exposed in tests,
   - auth, authorization, permissions, and data exposure boundaries still match
     the intended behavior,
   - inputs that cross trust boundaries are validated, escaped, constrained, or
     otherwise handled according to existing project patterns,
   - shell, subprocess, query, template, and file-path construction do not
     introduce injection or traversal risk,
   - external side effects, migrations, scheduled work, deployment behavior, and
     integrations are scoped and reversible enough for the brief,
   - logs, errors, screenshots, fixtures, and test output do not reveal sensitive
     values.
7. Project-specific risks:
   - check the repo entrypoint, local agent docs, work brief, or review request
     for named invariants the change must preserve,
   - examples include dependency direction, runtime or framework isolation,
     configuration/schema contracts, secret-management rules, generated
     artifacts, compatibility promises, deployment constraints, and validation
     commands,
   - treat violations of those local invariants as review findings even when the
     generic checklist would not catch them.

## Finding Format

Number every finding with a stable ID so follow-up work can cite it:

- `CR-1`, `CR-2`, `CR-3`, etc.

For each finding, include:

- severity,
- file or behavior reference,
- why it matters,
- suggested fix or decision needed.

If there are no findings, say so and note any residual verification gaps.
