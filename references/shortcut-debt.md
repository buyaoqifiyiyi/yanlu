# Ponytail Debt

Collect deliberate limits and their upgrade triggers from comments. Both
`shortcut: <limit>, <when to upgrade>` and older `ponytail:` comments count.

## Scan

Run from the requested repository root. Prefer this Git command, which also
includes untracked files while respecting standard ignore rules:

```sh
git grep --no-index --exclude-standard -nE -e '(#|//|/[*])[[:space:]]*(shortcut|ponytail):'
```

Exit code 0 means candidate matches, 1 means no matches, and 2 or greater is a
scan failure to report. This command also works as an external program in
PowerShell. It does not need Bash. It skips `.git` and ignored dependency,
build and cache paths. Do not override ignore rules without user scope.
If Git is unavailable, use `rg -n --hidden -g '!.git/**' -e '<expression>' .` from the scope
root, substituting the same expression as one quoted argument. The explicit
`.` keeps piped invocations from searching stdin; retain default ignore handling.
Report inaccessible files or a tool failure as incomplete coverage.

These are candidate hits, not automatic ledger rows. Read the source context:
keep actual deferrals in comments (including inline/block comments), and skip
keyboard shortcut notes, string literals and documentation examples that only
mention the convention. Add language-specific comment prefixes only for stacks
in the requested scope. If the user supplies another marker, search it as a
literal with `git grep --no-index --exclude-standard -nF -e '<marker>:'`, then
apply the same comment/deferral check. Never interpolate user text as a regex
or shell command; pass it as one quoted argument.

## Output

Group rows by file:

`<file>:<line>, <what was simplified>. ceiling: <stated limit>. upgrade: <stated trigger>.`

Use the text in the comment; do not invent missing limits or triggers. A real
deferral with no stated trigger gets `no-trigger`. Optionally inspect
`git blame -L<line>,<line>` when ownership is requested; untracked files have
no blame history.

End with `<N> markers, <M> with no trigger.` If no real deferrals remain after
filtering: `No shortcut debt in the checked scope.` Distinguish candidate hits
from accepted rows and report material scan exclusions.

## Boundaries

Reads and reports only. Save a ledger file when requested or already authorized;
otherwise return it inline. Does not edit source comments or change Ponytail mode.
