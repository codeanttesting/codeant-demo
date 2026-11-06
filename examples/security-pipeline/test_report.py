"""Checks for deployment bypasses and report export safety. Run with unittest."""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("report", Path(__file__).with_name("report.py"))
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class PipelinePolicyTests(unittest.TestCase):
    def run_gate(self, result, mode="enforce", scanner="sast"):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                if result is not None:
                    Path("results.json").write_text(json.dumps(result))
                with patch("sys.argv", ["report.py", "gate", "--scanner", scanner, "--mode", mode]):
                    with contextlib.redirect_stdout(io.StringIO()):
                        return report.main()
            finally:
                os.chdir(previous)

    def completed(self, findings):
        return {"status": "COMPLETED", "metrics": {"sast_rating_full_code": "S", "sca_rating_full_code": "S"},
                "findings": findings}

    def test_clean_completed_scan_passes_enforcement(self):
        self.assertEqual(self.run_gate(self.completed([])), 0)

    def test_high_sast_blocks_only_in_enforcement(self):
        result = self.completed([{"engine": "sast", "severity": "HIGH"}])
        self.assertEqual(self.run_gate(result, "warn"), 0)
        self.assertEqual(self.run_gate(result), 1)

    def test_missing_or_incomplete_results_fail_even_in_warning_mode(self):
        for result in [None, {"status": "done"}, {"status": "PENDING"}, {"status": "COMPLETED"}]:
            with self.subTest(result=result):
                self.assertEqual(self.run_gate(result, "warn"), 1)

    def test_scanner_jobs_do_not_block_on_other_engines(self):
        self.assertEqual(self.run_gate(self.completed([{"engine": "sca", "severity": "CRITICAL"}])), 0)

    def test_secrets_block_regardless_of_severity(self):
        self.assertEqual(self.run_gate(self.completed([{"engine": "secrets", "severity": "LOW"}]), scanner="secrets"), 1)

    def test_unknown_severity_is_not_silently_allowed(self):
        self.assertEqual(self.run_gate(self.completed([{"engine": "sast", "severity": ""}])), 1)

    def test_csv_does_not_execute_formulas(self):
        for value in ["=HYPERLINK(1)", " +1", "-1", "@SUM(A1)"]:
            self.assertTrue(report.csv_cell(value).startswith("'"))


if __name__ == "__main__":
    unittest.main()
