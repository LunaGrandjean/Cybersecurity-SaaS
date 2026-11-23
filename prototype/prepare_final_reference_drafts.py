"""Draft reviewable references BEFORE inference, never human signatures.

Rubric-based authoring aid for E101-E200; not classifier predictions. The
canonical candidates remain input-only. Humans must resolve every draft.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P2_TEAMS = ["Platform", "Platform", "Network", "Platform", "Identity",
            "Platform", "Integrations", "Platform", "Platform", "Platform",
            "Identity", "Platform", "Platform", "Integrations", "Platform",
            "Integrations", "Network", "Platform", "Integrations", "Platform"]
P3_TEAMS = ["Endpoint", "Platform", "Platform", "Platform", "Platform",
            "Platform", "Platform", "Platform", "Platform", "Platform",
            "Platform", "Platform", "Reporting", "Platform", "Platform",
            "Reporting", "Platform", "Platform", "Platform", "Platform"]
P4_TEAMS = ["Identity", "Customer Success", "Customer Success", "Customer Success", "Customer Success",
            "Integrations", "Customer Success", "Customer Success", "Endpoint", "Customer Success",
            "Customer Success", "Customer Success", "Reporting", "Platform", "Identity",
            "Endpoint", "Platform", "Integrations", "Customer Success", "Endpoint"]
SOURCE_IDS = {123: "KB-NET-01", 125: "KB-ACC-01", 131: "KB-ACC-01",
              137: "KB-NET-01", 138: "KB-PLT-01", 162: "KB-ACC-01", 199: "KB-ACC-01"}


def main():
    target = ROOT / "evals/ai_review/proposed_labels_v2.csv"
    if target.exists():
        raise ValueError("Draft file already exists; preserve human edits.")
    with (ROOT / "evals/eval_set_v2_candidates.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames + ["ai_author", "ai_prepared_date", "ai_uncertainty", "human_decision", "human_comment"]
        rows = list(reader)
    assert [r["id"] for r in rows] == [f"E{i:03}" for i in range(101, 201)]
    kb = {d["id"]: d for d in json.loads((ROOT / "prototype/data/knowledge_base.json").read_text(encoding="utf-8"))}
    for row in rows:
        number = int(row["id"][1:])
        if number <= 120:
            severity, team = "P1", "Incident Response"
            action = "Treat the reported unauthorised access, exposure or integrity change as a possible critical incident; preserve evidence and obtain urgent engineer investigation. Do not assert a confirmed attacker or execute containment automatically."
            source = "KB-SEC-01"
        elif number <= 140:
            severity, team = "P2", P2_TEAMS[number - 121]
            action = "Major failure of the described workflow is reported, while the input does not establish active compromise. Confirm affected scope, timing and available fallback with the owning engineer; do not invent a repair."
            source = SOURCE_IDS.get(number, "")
        elif number <= 160:
            severity, team = "P3", P3_TEAMS[number - 141]
            action = "Limited display/workflow defect with working core data or a stated alternative. Preserve original data, establish the actual scope and have the owning team verify the behaviour. Do not infer protection loss or invent a configuration change."
            source = ""
        elif number <= 180:
            severity, team = "P4", P4_TEAMS[number - 161]
            action = "Routine product/documentation question without a stated security incident. Obtain the authoritative product guidance through the owning team; do not assert an undocumented capability, setting or procedure."
            source = SOURCE_IDS.get(number, "")
        else:
            severity, team = "ABSTAIN", "Identity" if number == 199 else "Human triage"
            action = "Insufficient, contradictory, unsupported or unauthorised context: do not assign a technical incident severity or execute the requested action. Hand over, establish actual account/impact/authority and obtain the missing supported context; preserve confidentiality and do not invent facts or legal advice."
            source = SOURCE_IDS.get(number, "")
        uncertainty = "Confirmer les faits, la gravite et l'equipe sans consulter de prediction. Verifier le perimetre produit, la pertinence exacte de la source et l'independance semantique ; modifier ou remplacer les cas non adaptes."
        if number == 158:
            severity = "P4"
            action = "The stated size discrepancy may be normal rounding: content integrity succeeds and no actual failure is established. Treat as a clarification question provisionally, ask for exact units/values and do not claim a defect or a fix."
            uncertainty += " E158 : P4 propose pour une difference potentiellement normale ; P3 si un vrai defaut d'affichage est etabli."
        if number == 177:
            severity = "P3"
            action = "A saved lab view was actually deleted, while underlying investigation/event data remains intact. Treat as a limited user-workspace problem and obtain the supported recovery process; do not promise recoverability or invent a workaround."
            uncertainty += " E177 : P3 propose pour une vue effectivement supprimee ; aucun mecanisme de recuperation n'est atteste."
        if number in (197, 198):
            action = "Language outside the declared EN/FR scope: abstain, preserve declared priority and hand over for supported-language clarification. The preserved priority does not establish low impact."
        effective = row["declared_priority"] if severity == "ABSTAIN" else min(row["declared_priority"], severity)
        if source:
            assert kb[source]["account_id"] in ("*", row["account_id"])
            action += " The cited source supplies general triage safeguards only; it does not prove the current facts or provide an unquoted product-specific procedure."
        else:
            action += " No sufficiently specific source has been identified in the current KB; require engineer review rather than inventing an answer."
        row.update(expected_severity=severity, expected_effective_priority=effective, expected_team=team,
                   expected_output_or_action=action + f" Keep effective {effective}; never automatically lower below declared {row['declared_priority']}.",
                   evidence_or_source="Proposed reference from evals/README.md severity rubric, spec.md safeguards and the actual ticket facts. " + (source + " is generic guidance, not proof of this incident." if source else "Current KB does not justify a specific procedure for this case."),
                   expected_evidence_ids=source, hand_over_to_a_person="yes",
                   segment=f"{severity} | {row['account_id']} | {row['language']} | additional-candidate",
                   label_status="ai_proposed_pending_human_review", labelled_by="", labelled_at="",
                   origin="Synthetic input; reference initially drafted before human review and inference",
                   ai_author="AI assistant", ai_prepared_date="2026-11-23", ai_uncertainty=uncertainty,
                   human_decision="", human_comment="")
    with target.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} reference DRAFTS for human review. Canonical inputs, human signatures and predictions remain unchanged.")


if __name__ == "__main__":
    main()
