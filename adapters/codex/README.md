# Codex Adapter

This adapter is intentionally a guidance placeholder, not a complete install
package.

Use when the target repo wants Codex-specific hooks or local configuration.

Before implementing Codex-specific hooks, project config, skill loading, or
other Codex adapter behavior, read:

- `docs/platform-support.md`
- `docs/platforms/codex.md`

Those files are the canonical source for Codex guidance. Keep this adapter
directory limited to Codex-specific assets that cannot live in shared
templates, such as config examples, hook adapters, or skill-loading wrappers.

Unclear until a target repo needs it:

- which hooks are worth adding,
- whether project-local `.codex/` config should be committed,
- how hook output should be shaped against current Codex docs.

Potential future assets:

- Stop hook wrapper for `scripts/verify.sh`,
- secret or sensitive-file guard,
- destructive shell warning rules,
- bounded hook output formatting.
