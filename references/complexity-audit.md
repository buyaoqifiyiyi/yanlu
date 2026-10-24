ponytail-review, repo-wide. Scan the whole tree instead of a diff. Rank
findings biggest cut first.

## Tags

Same as ponytail-review:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Hunt

Deps the stdlib or platform already ships, single-implementation interfaces,
factories with one product, wrappers that only delegate, files exporting one
thing, dead flags and config, hand-rolled stdlib.

## Evidence before a finding

Read the requested scope's entry points, dependency list and relevant callers.
Before calling something unused, search tests, fixtures, config, string and
dynamic references. An interface with one implementation can still serve a
real boundary; identify a concrete simplification and explain which behavior
it preserves. Check expected load before removing a cache, batch or deliberate
shortcut. A documented `shortcut:` or legacy `ponytail:` limit is a decision,
not a finding while actual use remains within it. State unverified assumptions.

## Output

Rank the largest justified simplifications first. For each, give the location,
what to cut, its replacement, and a concrete caller or usage case supporting
the finding. Add a second sentence only when needed to explain preserved behavior.
Report line/dependency savings only when counted from a concrete proposed diff;
otherwise omit numbers. No findings: say no actionable complexity was found
within the checked scope. State any material coverage limits.

## Boundaries

Scope: over-engineering and complexity only. Correctness bugs, security holes,
and general performance audits are outside this pass. If a material issue is
noticed incidentally, flag it separately for the appropriate review without
expanding this audit. Lists findings, applies nothing. One-shot.
This one-shot report does not change the active Ponytail level.
