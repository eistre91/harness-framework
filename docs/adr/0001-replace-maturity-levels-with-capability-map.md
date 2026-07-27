---
status: accepted
---

# Replace maturity levels with a capability map

The framework replaced its numbered maturity taxonomy with the Harness
Capability Map defined in `docs/capability-map.md`. Numbered levels implied
cumulative progression and certification, while the implemented framework has
one Bounded Work foundation and independently selected capability domains. A
target repo has a dependency-closed Harness Profile that records selected
scope, current realizations, evidence, and known limits without a universal
maturity or completeness claim.

We rejected preserving corrected level prose because the ordinal repeatedly
recreates the wrong intuition, and we rejected parallel level and capability
taxonomies because they would duplicate the source of truth. The retired
numbered model remains only as an explicitly historical record.
`docs/capability-map-transition.md` records the completed bounded cutover.

## Consequences

Manifests, installer workflow, target-repo fit records, validation tooling,
tests, templates, and conceptual docs must migrate together. Existing target
repos must be re-profiled from installed behavior and evidence rather than
assuming that a historical level number certifies capabilities that were not
required by that level.
