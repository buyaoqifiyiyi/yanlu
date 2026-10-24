Review diffs for unnecessary complexity. One line per finding: location, what
to cut, what replaces it. The diff's best outcome is getting shorter.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for
multi-file diffs.

Tags:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Check before reporting

Read the requested diff and connected code. Trace callers, tests, fixtures,
config and dynamic references before recommending deletion. For every finding,
name a concrete usage case showing why the extra layer or dependency is
unneeded and why the replacement preserves behavior. Expected load matters:
keep justified batching/caching, platform boundaries, and documented
`shortcut:` or legacy `ponytail:` decisions while their limits still hold.

Examples:

- `dates.ts:L4: native: moment used only for this display label. Existing Intl.DateTimeFormat supports its locale/zone options; remove the dependency if no other consumers remain.`
- `repo.py:L88: yagni: this factory always constructs LocalStore and has no external registration hooks. Construct LocalStore directly at its sole caller.`

An abstraction with one implementation is a lead to inspect, not proof of
bloat. Validators, retries and tests stay when they enforce required behavior.

## Output

Give the location, tag, concrete evidence, and smallest replacement. Count net
lines only from a concrete proposed diff; otherwise omit a savings number.
No findings means no actionable complexity in the reviewed scope, not a general
correctness approval. State material scope or verification limits briefly.

## Boundaries

Scope: over-engineering and complexity only. Correctness bugs, security holes,
and general performance audits are outside this pass. Flag material incidental
issues separately for the appropriate review without expanding this one.
A meaningful smoke test or self-check is necessary verification, not bloat.
Does not apply the fixes, only lists them.
This one-shot report does not change the active Ponytail level.
