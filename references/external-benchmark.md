# Ponytail Gain

Present the following author-reported results, sourced from the fixed
[2026-10-07 agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md).
This is a published external experiment, not a benchmark run on this machine.
The locally adapted skill is not the exact configuration tested by the author.

## Conditions

The report compares Ponytail 5 against the same agent without the skill:
Claude Code CLI 2.1.288, Opus 5.5, default effort, headless sessions, 39 tasks
and 5 runs per task/arm. Bash was disabled; the benchmark ran delivered code
and tests afterwards. It measures code produced under those conditions, not
the agent's interactive debugging ability. Results use the geometric mean of
per-task median ratios, not a typical savings guarantee. The report includes
a third v4.13 arm; the following table uses only Ponytail 5 vs no skill.

## Scoreboard

| Metric | Ponytail 5 vs no skill, author-reported |
|---|---:|
| Lines of code | -53% (95% interval -63% to -41%) |
| Output tokens | -45% (95% interval -54% to -35%) |
| Cost | -26% (95% interval -36% to -16%) |
| Time | -41% (95% interval -49% to -32%) |
| Hidden checks, 18 tasks x 5 runs | 87/90 vs 86/90 |
| Test present on tasks classified as needing one | 98% vs 68% |

Keep the condition summary and source next to the numbers. The 21 remaining
tasks do not have the same hidden correctness/safety checks. Similar hidden
pass rates in this experiment do not establish a quality improvement.

## Honesty boundary

These figures have not been independently reproduced here and are not savings
for the user's repository, this local adaptation, Codex, or another model.
Do not calculate a per-repository savings percentage from code never written.
For current local facts use `ponytail-debt` to count deferrals or
`ponytail-audit` to identify concrete simplifications; neither measures an
unobserved no-skill baseline. One-shot display; edits nothing and changes no mode.
