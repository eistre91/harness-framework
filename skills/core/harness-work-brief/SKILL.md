---
name: harness-work-brief
description: Converts external work from a tracker, issue, chat, or planning notes into an Agent Work Brief that agents can execute. Use when turning user intent or a work item into implementation-ready scope.
---

# Harness Work Brief

Use when turning an external work item into an Agent Work Brief. Use
`work-brief-template.md` from this skill directory as the default template.

## Goal

Create an implementation-ready brief that contains the information an
implementation agent needs to do the work without reading the planning
discussion.

The planning agent may build up more context than the implementer needs.
Distill that context into the relevant outcome, constraints, accepted decisions,
source-of-truth references, and acceptance evidence. Do not copy the full
discussion into the brief. Do not list rejected options for provenance; include
only the accepted decision or constraint when it affects implementation or
review.

The planning goal is to identify the smallest valuable outcome that satisfies
the user's intent. Apply KISS and YAGNI before implementation starts: avoid
speculative abstractions, broad cleanup, new dependencies, or extra process
unless they are necessary to deliver the requested value or prevent a concrete
failure.

## Process

1. Inspect the canonical work source named in the repo entrypoint.
2. Infer obvious defaults from existing repo docs and code.
3. Surface ambiguities and trade-offs.
4. Ask focused human questions only when the answer materially affects scope,
   interface, verification, or acceptance evidence.
5. Decide whether the work is agent-runnable. If acceptance, ownership,
   interface, access, or product judgment is unclear, split runnable work from
   decision work.
6. Record tier, goal, value target, non-goals, context, implementation
   guidance, verification, docs impact, and done criteria.
7. Record only accepted decisions and constraints that affect implementation or
   review.
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

## Work Source

If the canonical source is external, such as Jira, GitHub Issues, or Linear, use
it when the current agent session has working read/write access through an MCP
server, API, CLI, or browser workflow. If that source is unavailable, use the
repo's gitignored local fallback only as temporary draft state.

Do not commit local fallback brief instances. Before handoff, copy durable
progress, evidence, blockers, and accepted plan changes back to the canonical
source when access is available. If the team wants versioned in-repo briefs,
they should choose an explicit durable path such as `docs/work/` as the
canonical location instead of treating local fallback drafts as source of truth.

For tiny work, do not force every template section. Capture the source, goal,
context, verification, and done criteria, then add richer sections only when
they reduce real risk.

## Collaboration

Use this while planning with the human. The final brief should keep only the
accepted decisions and constraints the implementer or reviewer needs.

For each meaningful choice, provide:

- recommended default,
- why it fits the repo,
- trade-off,
- when to revisit.

The human owns product intent and trade-offs. The planning agent owns making
the intent executable.
