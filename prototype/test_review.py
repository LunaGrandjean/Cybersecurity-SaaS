"""Review import safeguards using FICTIONAL unit rows, not the 50 holdout cases."""
import csv
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from .import_review import import_review
from .evaluate import read_csv


class ReviewImportTests(unittest.TestCase):
    def setUp(self):
        self.runtime = Path(__file__).parent / "runtime"
        self.folder = self.runtime / ("review-test-" + uuid.uuid4().hex)
        self.folder.mkdir(parents=True)
        self.original = self.folder / "input.csv"
        self.review = self.folder / "review.csv"
        self.output = self.folder / "verified.csv"
        self.row = {"id":"UNIT-ONLY", "incident_family_id":"UNIT-ONLY-FAMILY", "project":"UNIT",
                    "account_id":"helix", "declared_priority":"P3", "language":"en",
                    "input_the_agent_receives":"Fictional review-import unit fixture; never product evidence.",
                    "label_status":"pending_human", "labelled_by":"", "labelled_at":""}
        self.write(self.original, self.row)
        self.proposal = {**self.row, "human_decision":"accept", "human_comment":"",
                         "labelled_by":"FICTIONAL-UNIT-REVIEWER", "labelled_at":"2026-11-12T10:00:00Z"}

    def write(self, path, row):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(row))
            writer.writeheader()
            writer.writerow(row)

    def tearDown(self):
        assert self.folder.resolve().is_relative_to(self.runtime.resolve()) and self.folder.name.startswith("review-test-")
        shutil.rmtree(self.folder)

    def test_missing_decision_name_date_and_correction_reason_are_rejected(self):
        for changes in ({"human_decision":""}, {"labelled_by":""}, {"labelled_at":"2026-11-12"},
                        {"labelled_at":"2999-01-01T00:00:00Z"}, {"human_decision":"correct"}):
            self.write(self.review, {**self.proposal, **changes})
            with self.assertRaises(ValueError):
                import_review(self.review, self.original, self.output)
            self.assertFalse(self.output.exists())

    def test_input_changes_and_invalid_labels_are_rejected(self):
        self.write(self.review, {**self.proposal, "input_the_agent_receives":"Changed incident"})
        with self.assertRaises(ValueError):
            import_review(self.review, self.original, self.output)
        self.write(self.review, self.proposal)
        # The unmocked validator rejects incomplete / fewer-than-50 unit labels.
        with self.assertRaises(ValueError):
            import_review(self.review, self.original, self.output)
        self.assertFalse(self.output.exists())

    def test_import_preserves_original_and_never_predicts_or_overwrites(self):
        self.write(self.review, self.proposal)
        before = self.original.read_bytes()
        with patch("prototype.import_review.validate", return_value=[]), patch("prototype.engine.TriageEngine") as engine:
            result = import_review(self.review, self.original, self.output)
            engine.assert_not_called()
        self.assertFalse(result["predictions_exposed"])
        self.assertEqual(read_csv(self.output)[0]["label_status"], "human_verified")
        self.assertEqual(self.original.read_bytes(), before)
        with self.assertRaises(ValueError):
            import_review(self.review, self.original, self.output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
