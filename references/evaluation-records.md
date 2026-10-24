# 离线运行记录比较

该工具只检查同一冻结套件的已有记录；不执行目标业务、不调用模型、不判断产物语义，也不自动修改技能。数据真实性和独立判据仍由实际执行与评审负责。Python 3.11+，仅标准库。

```text
PYTHON SKILL_ROOT/scripts/compare_runs.py --fingerprint RUN_ROOT/plan.json
PYTHON SKILL_ROOT/scripts/compare_runs.py RUN_ROOT/plan.json RUN_ROOT/baseline/run.json RUN_ROOT/candidate/run.json
```

`plan.json`应在执行前固定。原字节SHA256写入两侧的suite_sha256，版本身份分别记录；路径相对各自run.json解析，证据放同一任务目录。开发数据参与选优后不再叫最终holdout，比较器无法靠split标签验证未泄露。

关注errors、retries、manual_interventions、false_completions等实际稳定性指标，耗时和tokens只有真实记录时才填；未知用null，不能从字符数推算。所有指标均越小越好。同条件、有holdout、执行与证据完整且无逐项退步之后，严格改善只得到evidence_supports_candidate的记录层建议；不是发布许可或普遍有效结论。正常业务任务无需为调用Ponytail新建这些记录。

## 重复试验与成功率口径

仅在用户要测可靠性或已有间歇失败时增加重复试验；次数和预算事先固定，不为凑连续成功反复运行。每次保留 case_id、版本、组/尝试序号、模型/工具/输入/预算、结果及产物证据；有反馈、人工介入或条件变化也记录。

- 冻结版本和判据下的重复执行，才可讨论该条件下的重复成功表现；还要说明随机性和独立性是否成立。首次失败后修改提示词、代码或工具，再成功，属于修复重试，分别保留版本、失败与介入成本，不当作原版本独立采样。
- 经验性 `pass@1` 看每组第一次；`pass@k` 看预先划定的每组 k 次中至少一次成功；`pass^k` 看该组 k 次是否全部成功。一次恰好连续成功不是总体概率；单次成功比例也不能直接取 k 次幂冒充实测。需要概率估计时另行说明估计方法和假设。
- 报告分子、分母、k、计划/完整/未完成组数及 fail/blocked/未执行数。不完整组保留为不完整，明确每个指标可判定的部分；不能丢掉受阻项后把完整组的比例称为全套成功率。小样本只报告观察结果，不宣称普遍可靠性或统计显著改善。
- 例如三组 `[pass,fail,pass]`、`[fail,fail,fail]`、`[pass,pass,pass]` 的首次、三次内至少一次、三次全部成功分别为 `2/3`、`2/3`、`1/3`。若还有未完成组，必须同时报告，以上仅是这三个完整组的结果。

`compare_runs.py` 不计算这些成功率，也不调度重复执行；保持其六个 minimize 指标和单次配对契约。成功率不能作为其 target_metric，不能靠额外 JSON 字段使比较器完成语义或可靠性评估。可在既有计划/结果中附加 capability/regression、trial_group、attempt 等元数据；当前比较器忽略额外元数据，不据此分组或形成采用结论。分别运行的配对记录及补充统计均不授权发布。

以下是保持不变的精确数据契约，供需要运行比较时读取：

# Deterministic recorded-run comparison

Python 3.11+, standard library only. Run `python scripts/compare_runs.py PLAN BASELINE CANDIDATE`; print a raw-file SHA256 with `python scripts/compare_runs.py --fingerprint PLAN`. JSON output uses `incomparable`, `regression`, `unverified`, `evidence_supports_candidate`, or `no_gain`. Valid comparisons exit 0 for every status; malformed input / unreadable JSON exits 2 with a short stderr error and no traceback.

Plan schema: `schema_version: 1`, nonempty `cases` with unique nonempty `id`, `split` (`development` or `holdout`) and boolean `critical`; `target_metric` is one of `errors`, `retries`, `manual_interventions`, `false_completions`, `elapsed_seconds`, `tokens`. All six minimize. `direction` may be omitted or `minimize`; maximize is rejected.

Each run has a lowercase `suite_sha256` of the **original raw plan bytes**, nonempty `version`, exactly four nonempty string `conditions` (`model`, `toolset`, `inputs`, `budget`), and `results`. Optional run `schema_version` must be integer 1. Each result has a planned unique `case_id`, `status` (`pass`, `fail`, `blocked`), `evidence_level` (`executed`, `static`, `dry_run`), string `artifact` relative to that run JSON's directory, and `metrics` object. Metric values, including extra metric keys, are null or finite nonnegative numbers; booleans, negatives, NaN and Infinity are rejected. Duplicate JSON object keys are rejected. Extra plan/run/result metadata is ignored.

Missing artifact field / empty / nonexistent artifact or artifact directory means unverified evidence, not an input error. An explicitly non-string artifact is an input error. Artifact path must be relative; its file must exist and contain at least one byte. This checks file presence only, not correctness, authenticity, freshness, or whether a mock was mislabeled as executed. Artifact content is never interpreted. Correctly labeled static/dry_run evidence never supports adoption.

Priority: known condition or plan-hash mismatch → incomparable; observed executed regression → regression; any remaining evidence/coverage/metric/unknown-condition gap or absence of holdout → unverified; strict paired-total decrease → evidence_supports_candidate; otherwise no_gain. Unknown condition markers include unknown, n/a, na, tbd, todo, unset, unspecified, none, null, not specified, 未知, 待定, 未提供, 未记录, 不详, 待确认. Other differing condition strings compare exactly. Unknown values do not establish equality. Comparable executed regressions can be reported even while other cases have gaps. A critical candidate **fail** with executed nonempty evidence is regression; critical blocked/missing/nonexecuted evidence is only unverified. Pass→fail requires executed nonempty evidence on both sides. Any such valid pair with a larger target metric is regression even if its overall total improves. All gaps remain in reasons. No numerical tolerance or significance inference is applied.

Each side's planned count is the whole plan denominator. Missing is planned minus result rows. pass/fail/blocked counts reflect declared statuses, executed reflects declared evidence_level; these counts alone do not certify evidence. `target_metric_totals` sums only nonblocked executed pairs with nonempty artifacts and known target values. `paired_cases` must therefore accompany the totals; partial totals cannot establish improvement. With zero valid pairs, both totals are null. Unknown/missing tokens never become zero. Strict improvement uses at least one per-case decrease after all per-case increases are excluded, avoiding floating-total cancellation. Candidate critical cases must pass to support adoption; other failures may remain unchanged, so a supported result is a recorded comparison, not a quality guarantee or automatic skill update.

Tests generate explicitly synthetic plans, results and plain-text evidence files inside temporary directories. They validate comparator behavior only; they are not real skill trials, business outcomes, model usage, token savings or quality evidence. Run: `python -m unittest discover -s tests -v`.

Totals are JSON numbers (or null for zero pairs). A total beyond the supported numeric range is rejected with exit 2 and a clear error. Decisions compare original individual metric numbers, not rounded display totals.
