# Wizard

A **wizard** is a bash script that walks a human, step by step, through a manual procedure that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at every stage, and shows how many stages are left. It might configure third-party services, run a one-off migration, or move the project from one state to another.

The UX in [template.sh](template.sh) provides stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, `.env` upserts, `gh secret`/`gh variable` writes, and a closing summary. Scope the procedure and author its stages. Keep the shared library unchanged unless a demonstrated defect or the target project's actual parser requires an authorized adjustment; verify that adjustment in isolation.

The bundled `write_env` is verified for single-line values with Node.js `util.parseEnv`, using an absent single, double or backtick quote as the delimiter. This is a specific parser contract. Before generating a runnable wizard, check the target project's real `.env` parser; another parser may interpret backticks or escapes differently. Reuse the project's existing writer or give a manual step when this encoding is unsupported. No new runtime dependency is required by the Bash helper. Multiline values and values containing all three delimiters are rejected without writing. `_existing` can read this writer's values and the old writer's shell-style single-quote encoding; unrelated existing lines are retained, not migrated. A read failure leaves the original file intact; a write failure is reported and requires checking the file before retrying.

A wizard is ephemeral by default: built for one run, saved to a scratch or `scripts/` path, deleted when the job's done. Commit it only when the user wants a repeatable setup path that should live in the repo.

On Windows, verify a usable Git Bash or WSL environment before choosing the Bash template. Give the exact executable and script path to run; PowerShell does not execute this template directly. If Bash is unavailable, use the current shell's native workflow for the authorized task and report the template limitation rather than installing a shell without a request. Preserve prior approval for steps already authorized; pause at an irreversible step only when approval is still missing.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value that gets captured along the way. Read the repo first, don't ask cold:

- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and `.github/workflows/*` (every `secrets.*` / `vars.*` reference is a value the wizard must produce).
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

Show the ordered stages and the values each produces. Ask only about unresolved scope or missing authorization; prior approval remains valid.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, a GitHub secret, both, or nowhere; some stages are pure actions), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills: e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs: never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Set `TOTAL_STAGES` to the number of stages you wrote.

Open the URL before asking for its value, use `ask_secret` for secrets, use the verified target-project writer for persisted values, and use `set_secret` only for values CI needs. Use `confirm` before an irreversible action only when authorization is still missing. Each `stage` clears the screen, so keep it focused. Preserve the shared library except for the verified adjustments described above.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Don't run it end-to-end yourself: it opens browsers and blocks on human input. Trace it statically instead: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name exactly matches a `secrets.*` reference in CI.
- Tell the user how to run it. For a requested repeatable setup path, link it from the README; commit only when current authorization includes committing.
