---
name: harness-fit
description: Collaboratively applies the minimal harness framework to an unfamiliar repository by inspecting repo evidence, proposing a maturity target, and installing only justified assets. Use when fitting this harness framework to a target repository.
maturity: bootstrap
install_when: Applying this harness framework to a new repository.
repo_specific_adaptation: All installed files, verification commands, tracker location, agent runtime, and adapters.
---

# Harness Fit

Use with `docs/implementation-guide.md` when applying the harness to a target
repo.

## Process

1. Inspect the repo without reading every source file.
2. Identify existing signals: work source, verification, docs, CI, sensitive
   files, and agent tools.
3. Inventory existing harness-like components and platform skills or commands.
   Record whether each should be threaded through, adapted, superseded, left
   alone, or deferred.
4. State current observed maturity.
5. Recommend a target maturity, installation mode (`canonical`, `starter`, or
   `overlay`), asset completeness claim, behavioral completeness claim, and any
   selective higher-level pull-ins.
6. Present a Harness Fit Proposal before editing. Include a manifest inclusion
   table, work-brief storage decision, tests/lint-format/type-check decisions,
   verification and validation matrix, skill or command conflict audit, durable
   proposal location, and communication audit. Use
   `templates/core/docs/harness/fit-proposal.md` as the canonical schema.
7. Persist the proposal to disk as the temporary installation plan, using a
   temp path by default unless the human specifies another location.
8. Present the exact persisted proposal text to the human.
9. Ask focused human questions with recommended defaults. At minimum, confirm
   target mode (`canonical`, `starter`, or `overlay`), completeness, work brief
   storage and fallback, missing test/lint-format/type-check decisions,
   existing skill or command handling, and whether the final proposal should be
   recorded under `docs/harness/`.
10. Wait for explicit approval or corrections before editing repository files.
11. Update the persisted plan if decisions change the starter shape.
12. Install only agreed assets.
13. Record deferrals and future expansion signals.
14. Record the final proposal or equivalent decision log durably under
    `docs/harness/`.

## Rule

Harness installation is repo diagnosis plus collaborative workflow design, not
blind template installation.

Do not describe a repo as simply "Level 1" when the install is a partial
starter or overlay. Use wording such as:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
```

When Claude Code is in scope, mention bundled Claude Code skills such as
`/code-review`, `/debug`, `/run`, and `/verify`. Ask whether they should stay
enabled and documented, be treated as secondary to repo-specific skills, or be
disabled through Claude Code settings such as `disableBundledSkills` or the
`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` environment variable.
