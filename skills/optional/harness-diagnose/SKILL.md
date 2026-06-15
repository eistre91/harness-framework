---
name: harness-diagnose
description: "Runs a disciplined diagnosis loop for bugs, failing tests, regressions, and unclear behavior: reproduce, minimize, hypothesize, instrument, fix, regression-test. Use when something is broken, flaky, slow, throwing, or behaving unexpectedly."
maturity: level-1
install_when: Agents will debug bugs, failing tests, flaky behavior, regressions, or production-like incidents.
repo_specific_adaptation: Reproduction commands, logs, runtime services, test command, observability tools, and rollback or safety rules.
support_files:
  - scripts/hitl-loop.template.sh
---

# Harness Diagnose

Use when something is broken, failing, slow, flaky, or behaving unexpectedly.

Skip phases only when explicitly justified.

## Phase 1: Build A Feedback Loop

This is the core of diagnosis. If you have a fast, deterministic,
agent-runnable pass/fail signal for the bug, bisection, hypothesis testing, and
instrumentation can all consume that signal. If you do not have one, stop
staring at code and build a better loop.

Spend disproportionate effort here.

Ways to construct a loop, roughly in preferred order:

1. Failing test at the narrowest seam that reaches the bug: unit, integration,
   or end-to-end.
2. HTTP script such as curl against a running local service.
3. CLI invocation with fixture input, diffing stdout or output files against
   known-good output.
4. Headless browser script such as Playwright or Puppeteer, asserting on DOM,
   console, or network behavior.
5. Replayed captured trace: network request, payload, event log, job input, or
   other artifact replayed through the code path.
6. Throwaway harness that spins up the smallest useful subset of the system and
   exercises the bug path with a direct call.
7. Property or fuzz loop for sometimes-wrong output.
8. Bisection harness when the bug appeared between two known commits, datasets,
   versions, or configurations.
9. Differential loop that runs the same input through old and new versions, or
   two relevant configurations, and diffs the result.
10. Human-in-the-loop script as a last resort. If a person must click or inspect
    something manually, copy and edit `scripts/hitl-loop.template.sh` so the
    manual loop still produces structured captured output.

Once a loop exists, improve it:

- Make it faster by caching setup, skipping unrelated initialization, or
  narrowing the test scope.
- Make it sharper by asserting on the specific symptom, not just "did not
  crash."
- Make it more deterministic by pinning time, seeding randomness, isolating the
  filesystem, and freezing or replacing network dependencies where appropriate.

For nondeterministic bugs, the first goal is a higher reproduction rate, not a
perfect repro. Loop the trigger many times, run in parallel, add stress, narrow
timing windows, or inject sleeps until the failure rate is high enough to debug.

If you genuinely cannot build a loop, stop and say so explicitly. List what you
tried. Ask for one of:

- access to an environment that reproduces it,
- a captured artifact such as logs, HAR, payload, core dump, trace, or screen
  recording with timestamps,
- permission to add temporary targeted instrumentation.

Do not proceed to hypothesis-driven changes without a loop you trust or a clear
explanation of why reproduction is blocked.

## Phase 2: Reproduce

Run the loop and watch the bug appear.

Confirm:

- the loop produces the failure mode the user described, not a nearby but
  different failure,
- the failure is reproducible across multiple runs, or for flaky bugs appears
  often enough to debug,
- the exact symptom is captured: error message, wrong output, missing side
  effect, slow timing, or other observable failure.

Do not proceed until you have reproduced the bug or explicitly documented why
reproduction is blocked.

## Phase 3: Hypothesize

Generate three to five ranked hypotheses before testing any one of them.
Single-hypothesis debugging anchors too early.

Each hypothesis must be falsifiable:

```text
If <cause> is true, then <probe or change> will make <observable symptom>
change in <specific way>.
```

If you cannot state the prediction, sharpen or discard the hypothesis.

Share the ranked list with the user when their domain knowledge could re-rank
it cheaply. Do not block indefinitely if the user is unavailable and the next
probe is low risk.

## Phase 4: Instrument

Each probe should map to a specific prediction from the hypothesis list. Change
one variable at a time.

Preferred probes:

1. Debugger, REPL, profiler, or inspectable test failure when available.
2. Targeted logs at boundaries that distinguish hypotheses.
3. Minimal code probes that can be removed cleanly.

Do not "log everything and grep." Tag every temporary debug log or probe with a
unique prefix such as `[DEBUG-a4f2]` so cleanup is mechanical.

For performance regressions, establish a baseline measurement before changing
code. Use a timing harness, profiler, query plan, browser performance trace, or
other measurement appropriate to the stack. Measure first, fix second.

## Phase 5: Fix And Regression-Test

Make the smallest fix that explains the evidence.

Write the regression test before the fix when there is a correct seam for it.
A correct seam exercises the real bug pattern as it occurs at the call site. A
too-shallow seam gives false confidence.

If no correct seam exists, record that as a finding. It may mean the code has no
good test boundary for this failure. Still fix the bug, but be explicit about
the residual risk.

When a correct seam exists:

1. Turn the minimized reproduction into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the original reproduction loop against the unminimized scenario.

## Phase 6: Cleanup And Postmortem

Before declaring done:

- re-run the original reproduction loop and confirm it no longer reproduces,
- run the regression test, or document why no correct regression seam exists,
- remove all tagged debug instrumentation,
- remove throwaway prototypes or move them to a clearly marked debug location
  only if the repo wants to keep them,
- run mechanical verification,
- state the cause, fix, evidence, and residual risk.

Then ask what would have prevented the bug. If the answer is architectural, such
as no good test seam, tangled callers, or hidden coupling, recommend follow-up
work after the fix is understood rather than turning the bug fix into a broad
refactor.

## Guardrails

- Do not shotgun unrelated fixes.
- Do not rewrite broad areas to avoid understanding the failure.
- Do not claim a fix without reproduction or a clear explanation of why
  reproduction was impossible.
- Prefer evidence over speculation.
- Do not keep temporary instrumentation unless the user or repo explicitly wants
  it.
