"""Recompute recorded evidence without predictions, training or fake grades."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .evaluate import ROOT, digest_match, read_csv, runtime_provenance, summarise, validate

REQUIRED = ("README.md", "01_problem_statement.md", "02_investment_memo.md",
            "03_product_brief.md", "03_user_research.md", "04_architecture.md",
            "05_metrics.md", "06_07_experiments_operations.md", "08_launch_memo.md",
            "product_brief.md", "spec.md", "governance.md", "evals/report_v0.md",
            "FINALISATION.md", "ORAL_DEMO.md")


def audit():
    result = {"checked_at": datetime.now(timezone.utc).isoformat(), "predictions_executed": False,
              "required_documents": {name: (ROOT / name).is_file() for name in REQUIRED}, "runs": {}}
    result["current_runtime"] = runtime_provenance()
    accounts = {r["id"]: r for r in json.loads((ROOT / "prototype/data/accounts.json").read_text(encoding="utf-8"))}
    total_reviewed = 0
    for run_name, case_file in (("v0", "eval_set_v0.csv"), ("v1_fresh", "eval_set_v1_fresh.csv")):
        folder = ROOT / "evals/runs" / run_name
        cases_path = ROOT / "evals" / case_file
        cases = read_csv(cases_path)
        validation_errors = validate(cases)
        metrics = summarise(cases_path, folder, write=False)
        recorded = json.loads((folder / "metrics.json").read_text(encoding="utf-8"))
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        outputs = {p["case_id"]: p["output"] for p in json.loads((folder / "predictions.json").read_text(encoding="utf-8"))}
        total_reviewed += len(cases)
        invariants = {
            "case_ids_match": len(outputs) == len(cases) and set(outputs) == {r["id"] for r in cases},
            "never_lower": all(int(outputs[r["id"]]["effective_priority"][1]) <= int(r["declared_priority"][1]) for r in cases),
            "customer_isolation": all(d["account_id"] in ("*", r["account_id"]) for r in cases for d in outputs[r["id"]]["similar"]),
        }
        segments = {}
        for key, value in [("language", x) for x in sorted({r["language"] for r in cases})] + [("tier", x) for x in ("Enterprise", "Standard")]:
            group = [r for r in cases if (r["language"] if key == "language" else accounts[r["account_id"]]["tier"]) == value]
            critical = [r for r in group if r["expected_severity"] == "P1"]
            noncritical = [r for r in group if r["expected_severity"] in ("P2", "P3", "P4")]
            segments[key + ":" + value] = {
                "cases": len(group), "p1_detected": sum(outputs[r["id"]]["proposed_severity"] == "P1" for r in critical),
                "p1_total": len(critical), "false_p1": sum(outputs[r["id"]]["proposed_severity"] == "P1" for r in noncritical),
                "non_p1_total": len(noncritical),
            }
        result["runs"][run_name] = {"validation_errors": validation_errors,
            "case_hash_match": digest_match(cases_path, manifest["cases_sha256"]),
            "prediction_hash_match": digest_match(folder / "predictions.json", manifest["predictions_sha256"]),
            "recorded_metrics_match": metrics == recorded, "invariants": invariants,
            "metrics": metrics, "segments_detailed": segments}
        result["runs"][run_name]["model_reproduction"] = {
            "recorded_model_version": manifest["model_version"],
            "matches_current_runtime": result["current_runtime"]["model_version"] == manifest["model_version"],
            "original_runtime_details_recorded": "runtime_provenance" in manifest,
            "note": "Historical metrics can be recomputed from preserved outputs; a different runtime fingerprint does not reproduce historical inference. Future freezes record runtime and source/data details."}
    candidates = read_csv(ROOT / "evals/eval_set_v2_candidates.csv")
    reviewed_path = ROOT / "evals/eval_set_v2_reviewed.csv"
    additional_reviewed = read_csv(reviewed_path) if reviewed_path.exists() else candidates
    prior = read_csv(ROOT / "evals/eval_set_v1.csv")
    training = read_csv(ROOT / "prototype/data/training_tickets.csv")
    normalise = lambda text: re.sub(r"\s+", " ", text.casefold()).strip()
    existing = {normalise(r["input_the_agent_receives"]) for r in prior} | {normalise(r["text"]) for r in training}
    result["coverage"] = {"recorded_human_reviewed_cases": total_reviewed,
        "additional_candidates": len(candidates), "additional_human_verified": sum(r["label_status"] == "human_verified" for r in additional_reviewed),
        "candidate_ids_unique": len({r["id"] for r in candidates}) == len(candidates),
        "exact_overlap_with_training_or_prior": [r["id"] for r in candidates if normalise(r["input_the_agent_receives"]) in existing],
        "target_200_human_reviewed_met": total_reviewed + sum(r["label_status"] == "human_verified" for r in additional_reviewed) >= 200,
        "semantic_independence": "Human review required; ids and exact-text checks are insufficient."}
    snapshot = json.loads((ROOT / "evals/finalisation_2026_11_23/original_evidence_sha256.json").read_text(encoding="utf-8"))
    result["original_evidence_unchanged"] = all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == sha for p, sha in snapshot.items())
    result["integrity_checks_passed"] = all(result["required_documents"].values()) and result["original_evidence_unchanged"] and all(
        not r["validation_errors"] and r["recorded_metrics_match"] and all(r["invariants"].values())
        for r in result["runs"].values())
    result["live_assisted_launch"] = "NO-GO: latest recorded P1 and routine-acceptance gates fail."
    result["remaining_human_work"] = ["Review/replace overlaps and label E101-E200 before inference.",
        "Conduct real user research and training/source review before a live pilot.",
        "Team final review, genuine commit authorship, course-specific requirements and final Git tag."]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional new audit JSON; existing evidence is never overwritten.")
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["integrity_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
