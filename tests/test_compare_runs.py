"""Synthetic fixtures test record comparison, not actual skill performance."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "compare_runs.py"
SPEC = importlib.util.spec_from_file_location("compare_runs", SCRIPT)
COMPARATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPARATOR)


class CompareRunsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="synthetic-comparator-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan_path = self.root / "plan.json"
        self.baseline_path = self.root / "baseline" / "run.json"
        self.candidate_path = self.root / "candidate" / "run.json"
        self.plan = {"schema_version": 1, "target_metric": "errors", "cases": [
            {"id": "development", "split": "development", "critical": False},
            {"id": "holdout", "split": "holdout", "critical": True}]}
        self.write(self.plan_path, self.plan)
        self.baseline = {"suite_sha256": self.fingerprint(), "version": "synthetic-baseline",
                         "conditions": {"model": "synthetic-model", "toolset": "stdlib", "inputs": "synthetic-v1", "budget": "synthetic-fixed"},
                         "results": [self.row("development", 10), self.row("holdout", 10)]}
        self.candidate = copy.deepcopy(self.baseline)
        self.candidate["version"] = "synthetic-candidate"
        self.candidate["results"][0]["metrics"]["errors"] = 5
        for run_path in (self.baseline_path, self.candidate_path):
            run_path.parent.mkdir()
            (run_path.parent / "evidence.txt").write_text("SYNTHETIC fixture; no real execution occurred.\n", encoding="utf-8")

    @staticmethod
    def row(case_id, value):
        return {"case_id": case_id, "status": "pass", "evidence_level": "executed", "artifact": "evidence.txt", "metrics": {"errors": value}}

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def fingerprint(self):
        return hashlib.sha256(self.plan_path.read_bytes()).hexdigest()

    def save(self):
        self.write(self.baseline_path, self.baseline)
        self.write(self.candidate_path, self.candidate)

    def compare(self):
        self.save()
        return COMPARATOR.compare(self.plan_path, self.baseline_path, self.candidate_path)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], text=True, capture_output=True)

    def test_strict_improvement_and_cli(self):
        result = self.compare()
        self.assertEqual(result["status"], "evidence_supports_candidate")
        self.assertEqual(result["target_metric_totals"], {"paired_cases": 2, "baseline": 20, "candidate": 15})
        proc = self.cli(self.plan_path, self.baseline_path, self.candidate_path)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), result)

    def test_tie(self):
        self.candidate["results"][0]["metrics"]["errors"] = 10
        self.assertEqual(self.compare()["status"], "no_gain")

    def test_aggregate_overflow_is_clear_cli_error(self):
        for run in (self.baseline, self.candidate):
            run["results"][0]["metrics"]["errors"] = 1e308
            run["results"][1]["metrics"]["errors"] = 1e308
        self.save()
        proc = self.cli(self.plan_path, self.baseline_path, self.candidate_path)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("metric total exceeds supported numeric range", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_float_total_rounding_does_not_hide_small_improvement(self):
        self.baseline["results"][0]["metrics"]["errors"] = 1e308
        self.candidate["results"][0]["metrics"]["errors"] = 1e308
        self.baseline["results"][1]["metrics"]["errors"] = 2
        self.candidate["results"][1]["metrics"]["errors"] = 1
        self.assertEqual(self.compare()["status"], "evidence_supports_candidate")

    def test_critical_failure_without_metric_regression(self):
        self.candidate["results"][1]["status"] = "fail"
        result = self.compare()
        self.assertEqual(result["status"], "regression")
        self.assertIn("critical candidate failed", [r["reason"] for r in result["regressions"]])

    def test_pass_to_fail_noncritical(self):
        self.candidate["results"][0]["status"] = "fail"
        self.assertEqual(self.compare()["status"], "regression")

    def test_total_gain_does_not_hide_individual_regression(self):
        self.candidate["results"][1]["metrics"]["errors"] = 11
        result = self.compare()
        self.assertLess(result["target_metric_totals"]["candidate"], result["target_metric_totals"]["baseline"])
        self.assertEqual(result["status"], "regression")
        self.assertEqual(result["regressions"][0]["case_id"], "holdout")

    def test_missing_stays_in_denominator(self):
        self.candidate["results"].pop()
        result = self.compare()
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["candidate"]["planned"], 2)
        self.assertEqual(result["candidate"]["missing"], 1)
        self.assertEqual(result["target_metric_totals"]["paired_cases"], 1)

    def test_unknown_tokens_not_zero(self):
        self.plan["target_metric"] = "tokens"
        self.write(self.plan_path, self.plan)
        for run in (self.baseline, self.candidate):
            run["suite_sha256"] = self.fingerprint()
            run["results"][0]["metrics"]["tokens"] = None
        result = self.compare()
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["target_metric_totals"]["paired_cases"], 0)
        self.assertIsNone(result["target_metric_totals"]["baseline"])
        self.assertIsNone(result["target_metric_totals"]["candidate"])
        self.assertTrue(any("unknown target metric tokens" in r for r in result["reasons"]))

    def test_incomplete_evidence_is_unverified(self):
        pristine = copy.deepcopy(self.candidate)
        for field, value in (("evidence_level", "static"), ("evidence_level", "dry_run"), ("status", "blocked"), ("artifact", "missing.txt"), ("artifact", "")):
            with self.subTest(field=field, value=value):
                self.candidate = copy.deepcopy(pristine)
                self.candidate["results"][1][field] = value
                self.assertEqual(self.compare()["status"], "unverified")
        self.candidate = pristine
        del self.candidate["results"][0]["artifact"]
        self.assertEqual(self.compare()["status"], "unverified")
        (self.candidate_path.parent / "evidence.txt").write_text("", encoding="utf-8")
        self.assertEqual(self.compare()["status"], "unverified")

    def test_executed_regression_retains_other_gaps(self):
        self.candidate["results"][0]["metrics"]["errors"] = 11
        self.candidate["results"].pop()
        result = self.compare()
        self.assertEqual(result["status"], "regression")
        self.assertTrue(any("missing case" in r for r in result["reasons"]))

    def test_conditions(self):
        self.candidate["conditions"]["model"] = "different-model"
        self.assertEqual(self.compare()["status"], "incomparable")
        for value in ("unknown-model", "N/A", "TBD", "未知"):
            with self.subTest(value=value):
                self.candidate["conditions"]["model"] = value
                self.assertEqual(self.compare()["status"], "unverified")

    def test_no_holdout(self):
        self.plan["cases"][1]["split"] = "development"
        self.write(self.plan_path, self.plan)
        for run in (self.baseline, self.candidate):
            run["suite_sha256"] = self.fingerprint()
        self.assertEqual(self.compare()["status"], "unverified")

    def test_fingerprint_detects_raw_byte_tampering(self):
        proc = self.cli("--fingerprint", self.plan_path)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), self.fingerprint())
        self.plan_path.write_bytes(self.plan_path.read_bytes() + b"\n")
        self.assertEqual(self.compare()["status"], "incomparable")

    def test_invalid_metric_values_and_extra_metrics(self):
        for value in (True, -1, float("nan"), float("inf"), "3"):
            with self.subTest(value=value):
                self.candidate["results"][0]["metrics"]["extra"] = value
                with self.assertRaises(ValueError):
                    self.compare()
        self.candidate["results"][0]["metrics"]["extra"] = None
        self.assertEqual(self.compare()["status"], "evidence_supports_candidate")

    def test_duplicate_unknown_result_and_invalid_artifact_field(self):
        pristine = copy.deepcopy(self.candidate)
        for mutation in ("duplicate", "unknown", "invalid_artifact", "bad_status", "bad_level"):
            with self.subTest(mutation=mutation):
                self.candidate = copy.deepcopy(pristine)
                if mutation == "duplicate":
                    self.candidate["results"].append(copy.deepcopy(self.candidate["results"][0]))
                elif mutation == "unknown":
                    self.candidate["results"][0]["case_id"] = "not-planned"
                elif mutation == "invalid_artifact":
                    self.candidate["results"][0]["artifact"] = True
                elif mutation == "bad_status":
                    self.candidate["results"][0]["status"] = "success"
                else:
                    self.candidate["results"][0]["evidence_level"] = "mock"
                with self.assertRaises(ValueError):
                    self.compare()

    def test_plan_schema_duplicate_and_direction_rejection(self):
        pristine = copy.deepcopy(self.plan)
        for mutation in ("schema", "duplicate", "direction"):
            with self.subTest(mutation=mutation):
                self.plan = copy.deepcopy(pristine)
                if mutation == "schema":
                    self.plan["schema_version"] = True
                elif mutation == "duplicate":
                    self.plan["cases"].append(copy.deepcopy(self.plan["cases"][0]))
                else:
                    self.plan["direction"] = "maximize"
                self.write(self.plan_path, self.plan)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_cli_errors_have_no_traceback(self):
        self.save()
        self.candidate_path.write_text('{"results": [], "results": []}', encoding="utf-8")
        for args in ((self.plan_path, self.baseline_path, self.candidate_path), (self.root / "absent.json", self.baseline_path, self.candidate_path), (self.plan_path,)):
            with self.subTest(args=args):
                proc = self.cli(*args)
                self.assertEqual(proc.returncode, 2)
                self.assertEqual(proc.stdout, "")
                self.assertIn("error:", proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
