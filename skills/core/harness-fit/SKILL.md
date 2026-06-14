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
3. State current observed maturity.
4. Recommend a target maturity and any selective higher-level pull-ins.
5. Present a Harness Fit Proposal before editing.
6. Persist the proposal to disk as the installation plan, using a temp path by
   default unless the human specifies another location.
7. Ask focused human questions with recommended defaults.
8. Update the persisted plan if decisions change the starter shape.
9. Install only agreed assets.
10. Record deferrals and future expansion signals.

## Rule

Harness installation is repo diagnosis plus collaborative workflow design, not
blind template installation.
