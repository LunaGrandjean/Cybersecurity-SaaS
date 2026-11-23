"""Human-labelled holdout protocol. No predictions until labels are frozen.

validate -> freeze -> run -> two independent grading CSVs -> summarise.
Never import this module into training or the interactive demo.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "eval_set_v0.csv"


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def runtime_provenance():
    """Record enough source/data/runtime detail for future reproduction."""
    prototype = Path(__file__).parent
    versions = {"python": platform.python_version(),
                **{name: version(name) for name in ("scikit-learn", "numpy", "scipy")}}
    files = [prototype / "data" / name for name in ("training_tickets.csv", "knowledge_base.json", "accounts.json")]
    files.append(prototype / "engine.py")
    material = b"".join(p.read_bytes() for p in files)
    runtime_bytes = "|".join(versions[name] for name in ("python", "scikit-learn", "numpy", "scipy")).encode()
    return {"versions": versions,
            "file_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p) for p in files},
            "model_version": hashlib.sha256(material + runtime_bytes).hexdigest()[:16]}


def digest_match(path, expected):
    """Accept exact bytes or LF/CRLF conversion only, never other edits.

    Historical manifests used Windows text-mode bytes before Git converted
    line endings. Keep those manifests unchanged and compare only equivalent
    newline encodings; no JSON reformatting or whitespace stripping is allowed.
    """
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() == expected:
        return "exact"
    lf = raw.replace(b"\r\n", b"\n")
    if any(hashlib.sha256(candidate).hexdigest() == expected
           for candidate in (lf, lf.replace(b"\n", b"\r\n"))):
        return "line_endings_only"
    return None


def validate(cases):
    from .engine import DATA, PRIORITIES, TEAMS, normalize
    training = read_csv(DATA / "training_tickets.csv")
    families = {row["incident_family_id"] for row in training}
    text_seen = {normalize(row["text"]).strip() for row in training}
    errors = []
    if len(cases) < 50:
        errors.append("Assignment 4 needs at least 50 cases.")
    ids = [row["id"] for row in cases]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate case ids.")
    groups = [row["incident_family_id"] for row in cases]
    if len(groups) != len(set(groups)):
        errors.append("Several evaluation rows share an incident family; report/de-duplicate first.")
    for row in cases:
        missing = []
        for field in ("labelled_by", "labelled_at", "expected_severity", "expected_effective_priority",
                      "expected_team", "expected_output_or_action", "evidence_or_source", "segment"):
            if not row.get(field, "").strip():
                missing.append(field)
        if row.get("label_status") != "human_verified":
            missing.append("label_status=human_verified")
        if row.get("expected_severity") not in (*PRIORITIES, "ABSTAIN"):
            missing.append("valid expected_severity")
        if row.get("expected_effective_priority") not in PRIORITIES:
            missing.append("valid expected_effective_priority")
        if row.get("expected_team") not in TEAMS:
            missing.append("valid expected_team")
        if row.get("hand_over_to_a_person") not in ("yes", "no"):
            missing.append("hand_over_to_a_person=yes|no")
        if row["incident_family_id"] in families or normalize(row["input_the_agent_receives"]).strip() in text_seen:
            missing.append("training/eval overlap: remove this incident from holdout")
        if missing:
            errors.append(row["id"] + ": " + ", ".join(missing))
    if not any(row.get("expected_severity") == "P1" for row in cases):
        errors.append("No human-labelled P1 cases: critical coverage is missing.")
    return errors


def freeze(cases_path, run_dir):
    cases = read_csv(cases_path)
    errors = validate(cases)
    if errors:
        raise ValueError("Cannot freeze:\n" + "\n".join(errors))
    from .engine import TriageEngine
    engine = TriageEngine()
    run_dir.mkdir(parents=True, exist_ok=True)
    target = run_dir / "manifest.json"
    if target.exists():
        raise ValueError("Manifest already exists. Keep this run immutable; use a new run directory.")
    manifest = {"frozen_at": datetime.now(timezone.utc).isoformat(), "cases_sha256": digest(cases_path),
                "cases": len(cases), "model_version": engine.model_version,
                "mode": "assisted", "human_labels_required": True, "predictions_exposed": False,
                "runtime_provenance": runtime_provenance()}
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def run(cases_path, run_dir):
    cases = read_csv(cases_path)
    errors = validate(cases)
    if errors:
        raise ValueError("Cannot run before human annotation:\n" + "\n".join(errors))
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError("Freeze labels and model before running.")
    manifest = json.loads(manifest_path.read_text())
    from .engine import TriageEngine
    engine = TriageEngine()
    if not digest_match(cases_path, manifest["cases_sha256"]) or manifest["model_version"] != engine.model_version:
        raise ValueError("Frozen cases or model changed. Do not tune on this holdout; create a fresh run and fresh cases.")
    if (run_dir / "predictions.json").exists():
        raise ValueError("This run already has predictions. Preserve it; do not silently overwrite.")
    predictions = []
    for row in cases:
        output = engine.analyze({"text": row["input_the_agent_receives"], "account_id": row["account_id"],
                                 "language": row["language"], "declared_priority": row["declared_priority"]}, "assisted")
        predictions.append({"case_id": row["id"], "output": output})
    (run_dir / "predictions.json").write_text(json.dumps(predictions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for grader in ("a", "b"):
        with (run_dir / f"grading_{grader}.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["case_id", "grader", "usable_as_is", "reason", "component", "elapsed_seconds"])
            writer.writeheader()
            writer.writerows({"case_id": row["id"], "grader": "", "usable_as_is": "", "reason": "", "component": "", "elapsed_seconds": ""} for row in cases)
    manifest.update(predictions_exposed=True, executed_at=datetime.now(timezone.utc).isoformat(),
                    predictions_sha256=digest(run_dir / "predictions.json"))
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"predictions": len(predictions), "status": "Awaiting two independent human graders"}


def summarise(cases_path, run_dir, write=True):
    cases = read_csv(cases_path)
    manifest = json.loads((run_dir / "manifest.json").read_text())
    if not digest_match(cases_path, manifest["cases_sha256"]) or not digest_match(run_dir / "predictions.json", manifest["predictions_sha256"]):
        raise ValueError("Frozen labels/predictions were modified; do not publish this run.")
    outputs = {p["case_id"]: p["output"] for p in json.loads((run_dir / "predictions.json").read_text(encoding="utf-8"))}
    grades = [read_csv(run_dir / f"grading_{g}.csv") for g in ("a", "b")]
    indexed = []
    names = []
    for rows in grades:
        if len(rows) != len(cases) or {r["case_id"] for r in rows} != {r["id"] for r in cases}:
            raise ValueError("Each grader must grade every case exactly once.")
        if any(r["usable_as_is"] not in ("yes", "no") or not r["grader"].strip() or not r["reason"].strip() for r in rows):
            raise ValueError("Human grades, names and reasons are incomplete.")
        identities = {r["grader"].strip().casefold() for r in rows}
        if len(identities) != 1:
            raise ValueError("One named person per grading file.")
        names.append(next(iter(identities)))
        indexed.append({r["case_id"]: r for r in rows})
    if names[0] == names[1]:
        raise ValueError("Two different graders are required.")
    routine = [r for r in cases if r["expected_severity"] in ("P3", "P4")]
    critical = [r for r in cases if r["expected_severity"] == "P1"]
    noncritical = [r for r in cases if r["expected_severity"] in ("P2", "P3", "P4")]
    accepted = lambda r: all(g[r["id"]]["usable_as_is"] == "yes" for g in indexed)
    p1_found = sum(outputs[r["id"]]["proposed_severity"] == "P1" for r in critical)
    false_p1 = sum(outputs[r["id"]]["proposed_severity"] == "P1" for r in noncritical)
    accepted_routine = sum(accepted(r) for r in routine)
    rate = lambda count, total: count / total if total else None
    misses = Counter()
    for row in cases:
        for grade in indexed:
            decision = grade[row["id"]]
            if decision["usable_as_is"] == "no":
                misses[(decision.get("component", "unspecified"), decision["reason"])] += 1
    metrics = {"cases": len(cases), "graders": names,
               "routine_accepted": accepted_routine, "routine_total": len(routine),
               "routine_acceptance": rate(accepted_routine, len(routine)),
               "p1_detected": p1_found, "p1_total": len(critical), "p1_recall": rate(p1_found, len(critical)),
               "false_p1": false_p1, "non_p1_total": len(noncritical), "false_p1_rate": rate(false_p1, len(noncritical)),
               "severity_accuracy": rate(sum((outputs[r["id"]]["proposed_severity"] or "ABSTAIN") == r["expected_severity"] for r in cases), len(cases)),
               "team_accuracy": rate(sum(outputs[r["id"]]["team"] == r["expected_team"] for r in cases), len(cases)),
               "effective_priority_accuracy": rate(sum(outputs[r["id"]]["effective_priority"] == r["expected_effective_priority"] for r in cases), len(cases)),
               "handover_agreement": rate(sum(outputs[r["id"]]["requires_human"] == (r["hand_over_to_a_person"] == "yes") for r in cases), len(cases)),
               "disagreements": sum(indexed[0][r["id"]]["usable_as_is"] != indexed[1][r["id"]]["usable_as_is"] for r in cases),
               "top_misses": [{"component": component, "reason": reason, "grader_mentions": count} for (component, reason), count in misses.most_common(3)],
               "segments": {}}
    for severity in ("P1", "P2", "P3", "P4", "ABSTAIN"):
        group = [r for r in cases if r["expected_severity"] == severity]
        metrics["segments"][severity] = {"cases": len(group), "both_accept": sum(accepted(r) for r in group)}
    for language in sorted({r["language"] for r in cases}):
        group = [r for r in cases if r["language"] == language]
        metrics["segments"]["language:" + language] = {"cases": len(group), "both_accept": sum(accepted(r) for r in group)}
    from .engine import DATA
    tiers = {a["id"]: a["tier"] for a in json.loads((DATA / "accounts.json").read_text(encoding="utf-8"))}
    for tier in sorted({tiers.get(r["account_id"], "Unknown") for r in cases}):
        group = [r for r in cases if tiers.get(r["account_id"], "Unknown") == tier]
        metrics["segments"]["tier:" + tier] = {"cases": len(group), "both_accept": sum(accepted(r) for r in group)}
    source_cases = [r for r in cases if r.get("expected_evidence_ids", "").strip()]
    source_hits = sum(bool(set(r["expected_evidence_ids"].split("|")) & {d["id"] for d in outputs[r["id"]]["similar"]}) for r in source_cases)
    metrics["source_hit_at_3"] = {"hits": source_hits, "eligible": len(source_cases), "rate": rate(source_hits, len(source_cases))}
    metrics["verdict"] = "met" if (routine and accepted_routine / len(routine) >= .62 and critical and p1_found == len(critical) and (not noncritical or false_p1 / len(noncritical) <= .15)) else "not_met"
    metrics["handling_time_saved"] = "NOT MEASURED; acceptance is only a proxy based on unverified timing assumptions."
    if write:
        (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("validate", "freeze", "run", "summarise"))
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--run-dir", type=Path, default=ROOT / "evals" / "runs" / "v0")
    parser.add_argument("--check-only", action="store_true", help="Recompute a summary without changing the recorded metrics.")
    args = parser.parse_args()
    try:
        if args.action == "validate":
            errors = validate(read_csv(args.cases))
            result = {"ready": not errors, "issues": errors}
            print(json.dumps(result, indent=2))
            return 1 if errors else 0
        if args.check_only and args.action != "summarise":
            raise ValueError("--check-only is available for summarise only.")
        result = summarise(args.cases, args.run_dir, write=not args.check_only) if args.action == "summarise" else {"freeze": freeze, "run": run}[args.action](args.cases, args.run_dir)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, FileNotFoundError) as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
