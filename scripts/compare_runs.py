"""Compare recorded evidence; never run cases or automatically adopt a skill."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

METRICS = {"errors", "retries", "manual_interventions", "false_completions", "elapsed_seconds", "tokens"}
CONDITIONS = ("model", "toolset", "inputs", "budget")
UNKNOWN = re.compile(r"\b(unknown|n/?a|tbd|todo|unset|unspecified|none|null)\b|not[ _-]specified|未知|待定|未提供|未记录|不详|待确认", re.I)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def read_json(path):
    raw = Path(path).read_bytes()
    obj = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
    require(isinstance(obj, dict), f"{path}: expected JSON object")
    return obj, hashlib.sha256(raw).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def read_plan(path):
    plan, fingerprint = read_json(path)
    require(type(plan.get("schema_version")) is int and plan["schema_version"] == 1, "plan schema_version must be 1")
    require(plan.get("target_metric") in METRICS, "invalid target_metric")
    require(plan.get("direction", "minimize") == "minimize", "direction must be minimize")
    require(isinstance(plan.get("cases"), list) and plan["cases"], "cases must be a nonempty list")
    cases = {}
    for case in plan["cases"]:
        require(isinstance(case, dict), "case must be an object")
        key = case.get("id")
        require(nonempty(key) and key not in cases, "case id must be nonempty and unique")
        require(case.get("split") in ("development", "holdout"), f"{key}: invalid split")
        require(type(case.get("critical")) is bool, f"{key}: critical must be boolean")
        cases[key] = case
    return plan, cases, fingerprint


def read_run(path, cases):
    run, _ = read_json(path)
    require("schema_version" not in run or (type(run["schema_version"]) is int and run["schema_version"] == 1), "run schema_version must be 1 when present")
    require(isinstance(run.get("suite_sha256"), str) and re.fullmatch("[0-9a-f]{64}", run["suite_sha256"]), "suite_sha256 must be a lowercase SHA256")
    require(nonempty(run.get("version")), "version must be nonempty text")
    conditions = run.get("conditions")
    require(isinstance(conditions, dict) and set(conditions) == set(CONDITIONS), "conditions must contain model, toolset, inputs, budget")
    require(all(nonempty(conditions[k]) for k in CONDITIONS), "condition values must be nonempty text")
    require(isinstance(run.get("results"), list), "results must be a list")
    results = {}
    for row in run["results"]:
        require(isinstance(row, dict), "result must be an object")
        key = row.get("case_id")
        require(isinstance(key, str) and key in cases and key not in results, "unknown or duplicate case_id")
        require(row.get("status") in ("pass", "fail", "blocked"), f"{key}: invalid status")
        require(row.get("evidence_level") in ("executed", "static", "dry_run"), f"{key}: invalid evidence_level")
        row.setdefault("artifact", "")
        require(isinstance(row["artifact"], str), f"{key}: artifact must be text")
        require(not Path(row["artifact"]).anchor, f"{key}: artifact must be relative to run JSON")
        metrics = row.get("metrics")
        require(isinstance(metrics, dict), f"{key}: metrics must be an object")
        for metric, value in metrics.items():
            require(value is None or (type(value) is int and value >= 0) or (type(value) is float and value >= 0 and math.isfinite(value)), f"{key}: invalid metric {metric}")
        artifact = Path(path).parent / row["artifact"]
        try:
            row["_has_artifact"] = bool(row["artifact"].strip()) and artifact.is_file() and artifact.stat().st_size > 0
        except OSError:
            row["_has_artifact"] = False
        results[key] = row
    return run, results


def usable(row):
    return row is not None and row["status"] != "blocked" and row["evidence_level"] == "executed" and row["_has_artifact"]


def counts(cases, results):
    return {"planned": len(cases), "executed": sum(r["evidence_level"] == "executed" for r in results.values()),
            **{s: sum(r["status"] == s for r in results.values()) for s in ("pass", "fail", "blocked")},
            "missing": len(cases) - len(results)}


def total(values):
    try:
        value = sum(values)
    except OverflowError as exc:
        raise ValueError("metric total exceeds supported numeric range") from exc
    require(type(value) is int or math.isfinite(value), "metric total exceeds supported numeric range")
    return value


def compare(plan_path, baseline_path, candidate_path):
    plan, cases, fingerprint = read_plan(plan_path)
    baseline, before = read_run(baseline_path, cases)
    candidate, after = read_run(candidate_path, cases)
    metric, gaps, mismatches, regressions, pairs = plan["target_metric"], [], [], [], []
    if baseline["suite_sha256"] != fingerprint or candidate["suite_sha256"] != fingerprint:
        mismatches.append("suite_sha256 does not match raw plan bytes")
    for field in CONDITIONS:
        a, b = baseline["conditions"][field], candidate["conditions"][field]
        if UNKNOWN.search(a) or UNKNOWN.search(b):
            gaps.append(f"unknown condition: {field}")
        elif a != b:
            mismatches.append(f"condition mismatch: {field}")
    if not any(case["split"] == "holdout" for case in cases.values()):
        gaps.append("plan has no holdout case")
    for key, case in cases.items():
        a, b = before.get(key), after.get(key)
        for label, row in (("baseline", a), ("candidate", b)):
            if row is None:
                gaps.append(f"{label}/{key}: missing case")
                continue
            if not usable(row):
                gaps.append(f"{label}/{key}: requires nonblocked executed result and nonempty artifact")
            if row["metrics"].get(metric) is None:
                gaps.append(f"{label}/{key}: unknown target metric {metric}")
        if usable(b) and case["critical"] and b["status"] == "fail":
            regressions.append({"case_id": key, "reason": "critical candidate failed"})
        if not (usable(a) and usable(b)):
            continue
        if a["status"] == "pass" and b["status"] == "fail":
            regressions.append({"case_id": key, "reason": "pass became fail"})
        av, bv = a["metrics"].get(metric), b["metrics"].get(metric)
        if av is not None and bv is not None:
            pairs.append((av, bv))
            if bv > av:
                regressions.append({"case_id": key, "reason": f"{metric} increased", "baseline": av, "candidate": bv})
    totals = {"paired_cases": len(pairs), "baseline": total(a for a, _ in pairs) if pairs else None, "candidate": total(b for _, b in pairs) if pairs else None}
    if mismatches:
        status, reasons = "incomparable", mismatches + gaps
    elif regressions:
        status, reasons = "regression", ["observed executed regression"] + gaps
    elif gaps:
        status, reasons = "unverified", gaps
    elif any(b < a for a, b in pairs):
        status, reasons = "evidence_supports_candidate", ["complete comparable records; target metric strictly improved without observed regression"]
    else:
        status, reasons = "no_gain", ["complete comparable records; target metric tied"]
    return {"status": status, "reasons": reasons, "suite_sha256": fingerprint, "target_metric": metric,
            "baseline": counts(cases, before), "candidate": counts(cases, after), "target_metric_totals": totals,
            "regressions": regressions}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", metavar="JSON")
    parser.add_argument("--fingerprint", metavar="PLAN")
    args = parser.parse_args(argv)
    try:
        if args.fingerprint:
            require(not args.paths, "--fingerprint accepts only PLAN")
            print(hashlib.sha256(Path(args.fingerprint).read_bytes()).hexdigest())
        else:
            require(len(args.paths) == 3, "expected PLAN BASELINE CANDIDATE")
            print(json.dumps(compare(*args.paths), ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
