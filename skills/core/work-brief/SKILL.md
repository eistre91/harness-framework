---
name: work-brief
description: Converts external work from a tracker, issue, chat, or planning notes into an Agent Work Brief that agents can execute. Use when turning user intent or a work item into implementation-ready scope.
maturity: level-1
install_when: Work arrives in a tracker or chat format that is not directly executable by agents.
repo_specific_adaptation: Canonical brief location, tracker conventions, required acceptance evidence, and project context paths.
---

# Work Brief

Use when turning an external work item into an Agent Work Brief.

## Goal

Create enough shared understanding that an implementation agent can proceed
without relying on hidden chat context.

## Process

1. Inspect the source work item.
2. Infer obvious defaults from existing repo docs and code.
3. Surface ambiguities and trade-offs.
4. Ask focused human questions only when the answer materially affects scope,
   interface, verification, or acceptance evidence.
5. Decide whether the work is agent-runnable. If acceptance, ownership,
   interface, access, or product judgment is unclear, split runnable work from
   decision work.
6. Record tier, goal, non-goals, context, implementation guidance,
   verification, docs impact, and done criteria.
7. Add the boundary/interface section only when the work changes a boundary.
8. If the source work is too large, propose independently verifiable vertical
   slices instead of layer-by-layer tasks. Each slice should have a clear
   outcome, boundary or interface, test surface, and dependency relationship.
9. Write durable briefs around behavior, interfaces, acceptance evidence, and
   source-of-truth files. Avoid brittle line numbers in long-lived briefs.

## Collaboration

For each meaningful choice, provide:

- recommended default,
- why it fits the repo,
- trade-off,
- when to revisit.

The human owns product intent and trade-offs. The planning agent owns making
the intent executable.
