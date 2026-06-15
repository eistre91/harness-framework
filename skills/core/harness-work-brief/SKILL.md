---
name: harness-work-brief
description: Converts external work from a tracker, issue, chat, or planning notes into an Agent Work Brief that agents can execute. Use when turning user intent or a work item into implementation-ready scope.
maturity: level-1
install_when: Work arrives in a tracker or chat format that is not directly executable by agents.
repo_specific_adaptation: Canonical brief location, tracker conventions, required acceptance evidence, and project context paths.
---

# Harness Work Brief

Use when turning an external work item into an Agent Work Brief.

## Goal

Create an implementation-ready brief that contains the information an
implementation agent needs to do the work without reading the planning
discussion.

The planning agent may build up more context than the implementer needs.
Distill that context into the relevant outcome, constraints, decisions,
source-of-truth references, and acceptance evidence. Do not copy the full
discussion into the brief. Include considered trade-offs only when the accepted
decision affects implementation or review.

The planning goal is to identify the smallest valuable outcome that satisfies
the user's intent. Apply KISS and YAGNI before implementation starts: avoid
speculative abstractions, broad cleanup, new dependencies, or extra process
unless they are necessary to deliver the requested value or prevent a concrete
failure.

## Process

1. Inspect the source work item.
2. Infer obvious defaults from existing repo docs and code.
3. Surface ambiguities and trade-offs.
4. Ask focused human questions only when the answer materially affects scope,
   interface, verification, or acceptance evidence.
5. Decide whether the work is agent-runnable. If acceptance, ownership,
   interface, access, or product judgment is unclear, split runnable work from
   decision work.
6. Record tier, goal, value target, non-goals, context, implementation
   guidance, verification, docs impact, and done criteria.
7. Record only decisions and trade-offs that affect implementation or review.
8. Add the boundary/interface section only when the work changes a boundary.
9. If the source work is too large, propose independently verifiable vertical
   slices instead of layer-by-layer tasks. Each slice should have a clear
   outcome, boundary or interface, test surface, and dependency relationship.
10. For each proposed slice, make it thin but complete. A completed slice should
    be demoable or verifiable on its own.
11. Prefer more thin slices over a few thick slices when that reduces ambiguity
    and dependency risk.
12. If the owning behavior, interface, test surface, or acceptance evidence
    cannot be named without guessing, split the work further or mark the
    decision as human-blocked.
13. Record lightweight design guardrails when they reduce implementation risk:
    owning module or boundary, public interface callers/tests should use, what
    complexity should stay hidden, test surface, dependency or blocker state,
    and any obvious gravity-well risk.
14. Present proposed slices before finalizing them when the split changes scope,
    dependency ordering, or human/agent ownership.
15. Challenge any plan that adds structure, generality, dependencies, or cleanup
    outside the requested value. Keep it only when the trade-off is explicit.
16. Write durable briefs around behavior, interfaces, acceptance evidence, and
    source-of-truth files. Avoid brittle line numbers in long-lived briefs.

## Collaboration

Use this while planning with the human. The final brief should keep only the
decisions and constraints the implementer or reviewer needs.

For each meaningful choice, provide:

- recommended default,
- why it fits the repo,
- trade-off,
- when to revisit.

The human owns product intent and trade-offs. The planning agent owns making
the intent executable.
