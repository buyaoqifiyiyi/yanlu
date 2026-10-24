Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

Use the issue tracker configuration if the repo has one. Otherwise use a spec supplied in this conversation or a local file. Reviewing code does not require installing or running a setup skill. Report any missing spec as a limit on the Spec axis.

## Process

### 1. Pin the fixed point

Use the fixed point or scope the user supplied. For a PR or branch, infer its base from verified PR metadata or upstream configuration when unambiguous. For work in progress, review the requested working-tree scope without demanding a branch base. Ask only when the intended scope is materially ambiguous.

Capture commands matching that scope:

- Committed branch changes: verify the base with `git rev-parse <fixed-point>`, then use `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`.
- Staged changes: `git diff --cached`.
- Unstaged changes: `git diff`.
- All tracked uncommitted changes: `git diff HEAD`.
- New files: enumerate with `git ls-files --others --exclude-standard` and read relevant files separately; normal git diffs omit them.

For an implementation review before commit, include its actual uncommitted changes and relevant new files. For a clean branch review, use the committed range. State the reviewed scope and any exclusions. An empty committed diff does not mean there is no work to review: inspect `git status --short` before that conclusion. Do not commit or change files merely to create a reviewable diff.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Use the user's task and agreed requirements from the current conversation, when available. If no source exists, report "no spec available" and continue Standards review. Ask only when a missing requirement blocks a meaningful assessment of the requested change.

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 按需检查跨文件语义

当前变更涉及单位/表示、默认值或异步状态，或用户明确要求一致性审查时，读取[跨文件语义一致性](references/semantic-consistency.md)。只追踪相关生产/消费两端，先确认共同职责及实际保证，区分已证实问题、疑点和有意差异。交给审查者时附相关定义与适用检查；结果仍进入原 Standards / Spec 所属轴，不新增强制报告、代理或全仓考古。

### 4. Spawn both sub-agents in parallel

When delegation is authorized and slots are available, issue both sub-agent calls together and aggregate their reports. Otherwise inspect Standards and Spec sequentially in the current session, preserving the two axes and reporting that independent reviewers were unavailable. Do not create separate user chats as a substitute.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
