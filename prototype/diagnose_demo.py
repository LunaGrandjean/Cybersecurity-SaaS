"""Exploratory automatic checks on EXPOSED demo references, never the holdout.

No human grades are generated or attributed. Reference labels are adapted
from Jane's original demo CSV, not certified ground truth.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evals/ai_review"
DEMO_REFERENCE = [
    ("P1", "Incident Response", "KB-SEC-01"),
    ("P1", "Incident Response", "KB-SEC-01"),
    ("P1", "Incident Response", "KB-SEC-01"),
    ("P1", "Identity", "KB-ID-01"),
    ("P1", "Platform", "KB-EDR-01|KB-PLT-01"),
    ("P1", "Platform", "KB-PLT-01"),
    ("P2", "Awareness module", "KB-AWR-01"),
    ("P1", "Detection Engineering", "KB-DET-01"),
    ("P2", "Platform", "KB-PLT-01"),
    ("P2", "Identity", "KB-ID-01"),
    ("P3", "Reporting", "KB-REP-01|INC-OR-01"),
    ("P3", "Endpoint", "KB-EDR-01"),
    ("P3", "Detection Engineering", "KB-DET-01"),
    ("P3", "Integrations", "KB-INT-01"),
    ("P4", "Customer Success", "KB-ACC-01|KB-REP-01"),
    ("P4", "Account Management", "KB-CMP-01"),
    ("P4", "Customer Success", "KB-REP-01"),
    ("P1", "Incident Response", "KB-SEC-01"),
    ("P2", "Identity", "KB-ACC-01"),
    ("P3", "Network", "KB-NET-01"),
]


def run(out_dir=OUT):
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.glob("demo_*")):
        raise ValueError("Preserve the recorded diagnostic; do not overwrite it after tuning.")
    with (ROOT / "evals/demo_reference_v0.csv").open(encoding="utf-8-sig", newline="") as stream:
        references = list(csv.DictReader(stream))
    if len(references) != 20 or [r["id"] for r in references] != [f"C{i:02}" for i in range(1, 21)]:
        raise ValueError("Expected the original 20 exposed demo references.")
    # Store the proposed structured reference before any model output exists.
    out_dir.mkdir(parents=True, exist_ok=True)
    reference_path = out_dir / "demo_reference_adapted.json"
    reference_path.write_text(json.dumps([
        {"case_id": r["id"], "reference_severity": severity, "reference_team": team,
         "candidate_source_ids": sources.split("|")}
        for r, (severity, team, sources) in zip(references, DEMO_REFERENCE)
    ], indent=2) + "\n", encoding="utf-8")

    from .engine import TriageEngine, normalize, PRIORITIES
    engine = TriageEngine()
    results = []
    counters = Counter()
    problems = Counter()
    for row, (severity, team, source_ids) in zip(references, DEMO_REFERENCE):
        text = row["input_the_agent_receives"]
        normalized = normalize(text)
        declared_match = re.search(r"declare[d]?\s+(p[1-4])", normalized)
        if not declared_match:
            raise ValueError("Missing declared priority in " + row["id"])
        declared = declared_match.group(1).upper()
        account_text = re.search(r"(?:account|compte)\s*:\s*([^.]*)", normalized)
        if not account_text:
            raise ValueError("Missing account in " + row["id"])
        names = {"helix logistics":"helix", "banque arpege":"arpege", "orion retail":"orion"}
        account = next((account_id for name, account_id in names.items() if name in account_text.group(1)), None)
        if account is None:
            raise ValueError("Unknown demo account in " + row["id"])
        language = "fr" if " · fr" in row["segment"] else "en"
        output = engine.analyze({"text":text, "account_id":account, "declared_priority":declared, "language":language}, "assisted")
        checks = {"severity_agreement": output["proposed_severity"] == severity,
                  "team_agreement": output["team"] == team,
                  "candidate_source_hit": bool(set(source_ids.split("|")) & {d["id"] for d in output["similar"]}),
                  "never_lower": PRIORITIES.index(output["effective_priority"]) <= PRIORITIES.index(declared),
                  "customer_isolation": all(d["account_id"] in ("*", account) for d in output["similar"])}
        for key, value in checks.items():
            counters[key] += value
        if not checks["severity_agreement"]:
            problems["severity disagreement"] += 1
        if not checks["team_agreement"]:
            problems["routing disagreement"] += 1
        if not checks["candidate_source_hit"]:
            problems["no candidate relevant source in top 3"] += 1
        if severity == "P1":
            counters["reference_p1"] += 1
            counters["p1_detected"] += output["proposed_severity"] == "P1"
        else:
            counters["reference_non_p1"] += 1
            counters["false_p1"] += output["proposed_severity"] == "P1"
        results.append({"case_id":row["id"], "reference_severity":severity, "reference_team":team,
                        "declared_priority":declared, "candidate_source_ids":source_ids,
                        "checks":checks, "actual_output":output,
                        "grade_source":"automatic comparison to adapted demo reference; NOT human grading"})
    summary = {"date":"2026-11-15", "executed_at":datetime.now(timezone.utc).isoformat(),
               "kind":"exploratory automatic diagnostic on exposed demo cases",
               "human_evaluation":False, "human_graders":[], "independent_holdout":False,
               "model_version":engine.model_version,
               "reference_sha256":hashlib.sha256(reference_path.read_bytes()).hexdigest(),
               "cases":len(results), "counts":dict(counters), "error_categories":dict(problems),
               "limitations":["No two-person grading", "Demo data exposed during development", "Reference not independently verified", "No measured handling-time saving", "Not the official 62% acceptance metric"],
               "results":results}
    (out_dir / "demo_diagnostic.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fields = ["case_id","reference_severity","actual_severity","declared_priority","effective_priority",
              "reference_team","actual_team","severity_agreement","team_agreement","candidate_source_hit",
              "never_lower","customer_isolation","review_required","review_reasons","grade_source"]
    with (out_dir / "demo_diagnostic.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for result in results:
            output = result["actual_output"]
            writer.writerow({"case_id":result["case_id"], "reference_severity":result["reference_severity"],
                 "actual_severity":output["proposed_severity"] or "ABSTAIN", "declared_priority":result["declared_priority"],
                 "effective_priority":output["effective_priority"], "reference_team":result["reference_team"],
                 "actual_team":output["team"], **result["checks"], "review_required":output["requires_human"],
                 "review_reasons":" | ".join(output["review_reasons"]), "grade_source":result["grade_source"]})
    print(json.dumps({key:value for key,value in summary.items() if key != "results"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=OUT,
                        help="New directory per diagnostic; prior evidence is never overwritten.")
    run(parser.parse_args().out_dir)
