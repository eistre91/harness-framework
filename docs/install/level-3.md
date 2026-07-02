# Level 3 Installer Checklist

Audience: agents and maintainers installing selected deterministic controls in
a target repo.

Use when: Level 1 has been installed and validated, the human has chosen to
inspect selected deterministic controls, and the current approved installation
stage is Level 3. Start from `docs/installer.md` first.

## Read For This Stage

Always read:

- `docs/principles.md`
- `docs/installer.md`
- this checklist
- `manifests/level-3.yml`
- the Level 3 section of `docs/maturity-model.md`
- the target repo's durable Level 1 handoff under `docs/harness/`
- the target repo's installed `AGENTS.md`
- the target repo's existing `scripts/repo-checks.sh`
- only the target-repo mechanisms and evidence relevant to the selected control
  families in current scope, such as hook configuration, Git hooks, pre-commit
  config, secret scanning config, generated-artifact tooling, or protected
  paths

Read only if needed for this Level 3 stage:

- `docs/platform-support.md`, then only the relevant platform note, when a
  selected control uses agent-runtime hooks or platform config
- `docs/hook-pattern.md`, when designing hooks beyond an existing standard
  adapter
- `adapters/pre-commit/README.md`, when a selected control uses pre-commit
- `docs/portable-assets.md`, when adaptation boundaries are unclear
- `docs/implementation-guide.md`, only for deeper installation background that
  this checklist does not answer

Do not read by default:

- Level 4 or later guidance
- `docs/level-5-orchestration.md`
- the full `manifests/optional-assets.yml`
- broad CI/CD, deployment, or enterprise-tooling docs unless the selected
  control's approved scope requires them
- broad historical, plan, discussion, or provenance docs in the target repo

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope

Level 3 installs selected deterministic controls around agent action bounds.
It narrows risky or repeatedly-missed agent outcomes with checks, guidance,
blocks, or verification at useful lifecycle points.

Use `manifests/level-3.yml` as the canonical selected-control family list. Do
not maintain a second full family list here.

Level 3 is a menu, not a required bundle. A Level 3 pass may install one
approved control, several approved controls, or none if inspection shows the
friction would not earn its cost. The operator owns the trade-off: every new
control adds friction, and that friction must be worth the value or risk
reduction.

Level 1 remains the owner of `scripts/repo-checks.sh` and the narrow
`repo-checks-on-stop` behavior. Level 3 begins when controls become selected
agent-action bounds, broader lifecycle gates, or deterministic steering beyond
the Level 1 lint, type-check, test, and Stop-hook contract.

Do not treat Level 3 as general CI/CD maturity. CI, pre-commit, static
analysis, format, build, or repo-quality tools may be selected mechanisms only
when they help the harness constrain agent behavior at the right lifecycle
point. Broad maintainability sensors usually belong to Level 4 unless they are
used to constrain a specific Level 3 agent action.

## Discovery

Inspect only the control families in current approved scope. Use these
questions to discover whether a selected control is worth proposing:

- What agent actions could cause expensive cleanup, data loss, credential
  exposure, broken history, or confusing state?
- What instructions do humans repeatedly give agents at the same lifecycle
  moment?
- What repo conventions are important enough that review should not be the
  first line of defense?
- What files, paths, commands, or generated artifacts require extra trust
  before mutation?
- What stale state causes agents to continue work from the wrong premise?
- What checks are cheap, fast, and clear enough to run at the moment of risk?
- What should be blocked, what should guide, what should verify, and what
  should only be observed?
- What control would humans and agents actually respect rather than bypass?

Use these enforcement modes:

- `observe`: record or report signal only.
- `guide`: inject just-in-time guidance and allow continuation.
- `block`: prevent the action or transition until the condition changes.
- `verify`: run a deterministic check and use pass/fail as evidence.

Do not use `ask` as a portable mode. When human approval is required, use a
`block` result that tells the agent to get human approval, or use a
platform-native approval flow only when the selected adapter explicitly
supports one. Do not use `warn` as a separate mode; it is a tone or severity
inside `guide`.

Choose the cheapest useful mechanism for the risk. A staged-file secret scan
may be better than an agent-runtime hook for preventing committed secrets. A
runtime command hook may be better for destructive shell commands. A Git hook
may be better for commit standards. A Stop hook or handoff verifier may be
better for final evidence.

Secret controls must be honest about coverage. It is useful to block common
direct reads of sensitive paths and to block committed secret values, but do
not claim complete prevention. Agents can bypass simple read guards through
unanticipated shell tools or local filesystem paths. Validate secret wiring by
names, declarations, aliases, and permissions without reading, printing, or
persisting secret values.

## Proposal

Prepare a Level 3 proposal before editing. The proposal authorizes only the
selected deterministic controls listed for this Level 3 pass.

Include:

- current stage: Level 3,
- target maturity behavior: selected deterministic controls,
- installation mode: usually `starter` or `overlay`; use `canonical` only when
  the proposal explains what full canonical completeness means for the
  approved selected-control scope,
- Level 1 bounded-work foundation status and any Level 1 gaps that affect the
  selected controls,
- repo signals or operator decisions that justify Level 3 now,
- Level 3 asset completeness for the approved selected-control scope,
- expected Level 3 behavioral completeness for the approved selected-control
  scope,
- selected-control rows,
- files to create or edit,
- current-stage deferrals,
- human decisions needed before editing,
- context used.

Use this compact shape for each selected-control row:

| Control | Why now | Event | Mode | Mechanism | Files | Validation | Friction risk | Known limits | Revisit / removal signal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | observe / guide / block / verify |  |  |  |  |  |  |

For controls that block, touch shared hooks, or have unusual risk, add any
extra details needed to make the trade-off reviewable, such as expected output,
human-approval wording, or rollback path.

Out-of-stage observations may be recorded as plain observations. Do not map
them to future levels, propose later-stage assets, or ask for approval to
install them during the Level 3 stage.

## Human Checkpoint Before Editing

After writing and persisting the proposal, present the exact proposal text to
the human and wait for approval or corrections.

The approval should cover only:

- Level 3 installation mode,
- each selected-control row,
- files to create or edit,
- lifecycle event or mechanism for each selected control,
- enforcement mode for each selected control,
- validation method for each selected control,
- known limits, friction risks, and revisit or removal signals,
- durable location for the Level 3 decision log or stage handoff.

Do not edit target-repo files before this checkpoint is resolved. Do not
install unapproved controls just because they share a hook, script, or platform
adapter with an approved control.

## Level 3 Gate

Level 3 passes when the approved controls are installed, validated, and honest
about their scope.

Check:

- The durable Level 1 handoff exists and either remains accurate or is updated
  by this stage.
- Every installed control matches an approved selected-control row.
- No unapproved control families were installed.
- Each selected control has an event, mode, mechanism, validation method,
  friction risk, known limits, and revisit or removal signal.
- Each selected control has validation evidence from a deterministic command,
  wrapper smoke test, hook smoke test, or documented reason why only static
  inspection was possible.
- Hook outputs are quiet when passing and actionable when they guide, block, or
  report failure.
- Shared policy is not duplicated across platform adapters, Git hooks, docs,
  and scripts without a clear owner.
- Platform-specific files are thin adapters when shared policy is practical.
- Secret controls do not tell agents to read, print, inspect, or persist secret
  values.
- Secret read guards record known bypass limits rather than claiming complete
  prevention.
- Destructive-command controls are narrow enough that humans and agents are not
  likely to bypass them routinely.
- `scripts/repo-checks.sh` remains focused and does not become a dumping ground
  for unrelated CI/CD maturity.
- The durable harness record states that Level 3 completeness is
  selected-control completeness for this pass, not exhaustive deterministic
  control maturity.
- The stage report lists context used.

Missing useful controls do not fail a Level 3 pass when they are honestly
deferred with a revisit signal. Installed controls fail when they are hidden,
unvalidated, noisy enough to be bypassed, or overclaim coverage.

## Stage Handoff

After installation and validation, report the Level 3 result and copy durable
stage state under `docs/harness/`. Use the canonical stage handoff fields in
`docs/installer.md`.

For Level 3, make sure the handoff also makes these details explicit:

- selected-control rows installed or already satisfied,
- Level 3 asset completeness for the approved selected-control scope,
- Level 3 behavioral completeness for the approved selected-control scope,
- validation result for each selected control,
- hook, script, Git hook, adapter, or repo-checks mechanism used,
- known limits for each selected control,
- friction risks and any expected operator cost,
- control families intentionally deferred or excluded,
- broad CI/CD, static analysis, maintainability, or orchestration ideas
  deferred out of Level 3,
- recommended next action: stop, revise selected controls, inspect another
  selected Level 3 control family, or ask the human whether to inspect the next
  maturity stage.

Do not inspect Level 4 maintainability sensors or future orchestration guidance
beyond this stage until the human chooses to begin that next stage or
explicitly changes the current approved scope.
