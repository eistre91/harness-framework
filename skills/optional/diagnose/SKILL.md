---
name: diagnose
description: "Runs a disciplined diagnosis loop for bugs, failing tests, regressions, and unclear behavior: reproduce, minimize, hypothesize, instrument, fix, regression-test. Use when something is broken, flaky, slow, throwing, or behaving unexpectedly."
maturity: level-1
install_when: Agents will debug bugs, failing tests, flaky behavior, regressions, or production-like incidents.
repo_specific_adaptation: Reproduction commands, logs, runtime services, test command, observability tools, and rollback or safety rules.
---

# Diagnose

Use when something is broken, failing, slow, flaky, or behaving unexpectedly.

## Loop

1. Reproduce the problem or state clearly why reproduction is blocked.
2. Minimize the failing case.
3. Form one or two concrete hypotheses.
4. Inspect or instrument the narrowest relevant code path.
5. Make the smallest fix that explains the evidence.
6. Add or update a regression test where practical.
7. Run mechanical verification.
8. Report the cause, fix, evidence, and residual risk.

## Guardrails

- Do not shotgun unrelated fixes.
- Do not rewrite broad areas to avoid understanding the failure.
- Do not claim a fix without reproduction or a clear explanation of why
  reproduction was impossible.
- Prefer evidence over speculation.
