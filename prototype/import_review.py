"""Import actual human decisions, without running inference or inventing grades."""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from .evaluate import DEFAULT_CASES, ROOT, read_csv, validate

IDENTITY_FIELDS = ("id", "incident_family_id", "project", "account_id",
                   "declared_priority", "language", "input_the_agent_receives")


def import_review(review_path, cases_path, output_path):
    output_path = Path(output_path)
    if output_path.exists():
        raise ValueError("Output already exists; preserve the earlier annotations.")
    original = read_csv(cases_path)
    reviews = read_csv(review_path)
    by_id = {row["id"]: row for row in reviews}
    if len(by_id) != len(reviews) or set(by_id) != {row["id"] for row in original}:
        raise ValueError("Review must contain each original case exactly once.")
    verified = []
    for case in original:
        review = by_id[case["id"]]
        if any(review.get(key) != case[key] for key in IDENTITY_FIELDS):
            raise ValueError(case["id"] + ": original input/identity changed; review a new version explicitly.")
        if review.get("human_decision") not in ("accept", "correct"):
            raise ValueError(case["id"] + ": a real reviewer must enter human_decision=accept|correct.")
        if not review.get("labelled_by", "").strip():
            raise ValueError(case["id"] + ": actual reviewer name is missing.")
        try:
            stamp = datetime.fromisoformat(review.get("labelled_at", "").replace("Z", "+00:00"))
            if stamp.tzinfo is None or stamp > datetime.now(timezone.utc):
                raise ValueError("Missing timezone or future date")
        except ValueError as error:
            raise ValueError(case["id"] + ": enter the actual review date/time with timezone.") from error
        if review["human_decision"] == "correct" and not review.get("human_comment", "").strip():
            raise ValueError(case["id"] + ": explain the correction in human_comment.")
        merged = {key: review.get(key, case[key]) for key in case}
        merged["label_status"] = "human_verified"
        # Preserve AI provenance; a human review does not turn synthetic inputs
        # into real incidents or retrospectively sign off the training set.
        for key in ("ai_author", "ai_prepared_date", "ai_uncertainty", "human_decision", "human_comment"):
            merged[key] = review.get(key, "")
        verified.append(merged)
    errors = validate(verified)
    if errors:
        raise ValueError("Review incomplete/invalid:\n" + "\n".join(errors))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create: never replace a file edited during validation.
    with output_path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(verified[0]))
        writer.writeheader()
        writer.writerows(verified)
    return {"reviewed_cases": len(verified), "output": str(output_path),
            "predictions_exposed": False, "next": "validate, freeze, run; then two independent human graders"}


def main():
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, default=ROOT / "evals/ai_review/proposed_labels_v0.csv")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--out", type=Path, default=ROOT / "evals/eval_set_reviewed_v0.csv")
    args = parser.parse_args()
    try:
        print(json.dumps(import_review(args.review, args.cases, args.out), indent=2))
        return 0
    except (ValueError, FileNotFoundError) as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
