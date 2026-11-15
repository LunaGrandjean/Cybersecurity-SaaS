"""Fictional fixtures test runner integrity; NOT human/product evaluation."""
import csv
import json
import shutil
import unittest
import uuid
from pathlib import Path

from .evaluate import freeze, run, summarise


class EvaluationProtocolTests(unittest.TestCase):
    def setUp(self):
        self.runtime = Path(__file__).parent / "runtime"
        self.folder = self.runtime / ("protocol-test-" + uuid.uuid4().hex)
        self.folder.mkdir(parents=True)
        self.cases = self.folder / "fictional_test_cases.csv"
        self.output = self.folder / "fictional_run"
        self.rows = []
        for i in range(50):
            self.rows.append({"id": f"UNIT-{i}", "incident_family_id": f"UNIT-ONLY-{i}",
                 "input_the_agent_receives": "UNIT TEST FIXTURE: " + ("An unknown privileged administrator is active." if i == 0 else f"Request {i}: Where can I download the ISO 27001 certificate for our auditor?"),
                 "expected_severity": "P1" if i == 0 else "P4", "expected_effective_priority": "P1" if i == 0 else "P4",
                 "expected_team": "Incident Response" if i == 0 else "Account Management",
                 "expected_output_or_action": "Fictional test assertion, not a real human label",
                 "evidence_or_source": "Unit-test fixture", "expected_evidence_ids": "KB-CMP-01" if i else "KB-SEC-01",
                 "labelled_by": "FICTIONAL-TEST-FIXTURE", "labelled_at":"2026-11-12T00:00:00Z",
                 "label_status":"human_verified", "hand_over_to_a_person":"yes" if i == 0 else "no",
                 "segment":"unit-test", "account_id":"helix", "declared_priority":"P1" if i == 0 else "P4", "language":"en"})
        self.write_cases()

    def write_cases(self):
        with self.cases.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(self.rows[0]))
            writer.writeheader()
            writer.writerows(self.rows)

    def tearDown(self):
        assert self.folder.resolve().is_relative_to(self.runtime.resolve()) and self.folder.name.startswith("protocol-test-")
        shutil.rmtree(self.folder)

    def test_pending_labels_cannot_produce_predictions(self):
        self.rows[0]["label_status"] = "pending_human"
        self.write_cases()
        with self.assertRaises(ValueError):
            freeze(self.cases, self.output)
        self.assertFalse((self.output / "predictions.json").exists())

    def test_changed_frozen_cases_cannot_run(self):
        freeze(self.cases, self.output)
        self.rows[1]["expected_team"] = "Network"
        self.write_cases()
        with self.assertRaises(ValueError):
            run(self.cases, self.output)

    def test_independent_grading_and_tamper_guards(self):
        freeze(self.cases, self.output)
        run(self.cases, self.output)
        with self.assertRaises(ValueError):
            run(self.cases, self.output)
        with self.assertRaises(ValueError):
            summarise(self.cases, self.output)
        for suffix in ("a", "b"):
            with (self.output / f"grading_{suffix}.csv").open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["case_id","grader","usable_as_is","reason","component"])
                writer.writeheader()
                writer.writerows({"case_id":r["id"], "grader":f"FICTIONAL-test-grader-{suffix}",
                                  "usable_as_is":"yes", "reason":"Unit-test-only decision", "component":""} for r in self.rows)
        result = summarise(self.cases, self.output)
        self.assertEqual(result["routine_total"], 49)
        self.assertEqual(result["routine_accepted"], 49)
        self.assertEqual(result["disagreements"], 0)
        predictions = self.output / "predictions.json"
        predictions.write_text(predictions.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaises(ValueError):
            summarise(self.cases, self.output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
