# Evaluation protocol and current evidence

**Updated 23 November 2026.** The initial 50 cases and an additional 50 have reviewed references and recorded runs. Both runs fail the launch gate. E101-E200 are new input candidates, not reviewed references. [Current report](report_v0.md) | [Final decision](../08_launch_memo.md).

## Data and independence

| File | Use |
|---|---|
| `demo_reference_v0.csv` | Original 20 exposed examples; demonstration/development only |
| `eval_set_v0_inputs.csv`, `eval_set_v0.csv` | Original inputs and reviewed E001-E050; E050 replaced before freeze |
| `eval_set_v1_inputs.csv`, `eval_set_v1_fresh.csv` | Inputs and reviewed E051-E100; second recorded batch |
| `eval_set_v1.csv` | Combined 100 reviewed references, not one blind evaluation of a single model |
| `eval_set_v2_candidates.csv` | E101-E200 input candidates with blank expected answers and human fields |
| `runs/v0`, `runs/v1_fresh` | Preserved manifests, predictions, grades and metrics |

All fixtures are synthetic. Split by actual incident, not by changed names or text alone. Unique ids and the exact-text check do not certify semantic independence. An exposed case used to tune the system becomes development data. The second recorded batch was new but not fully blind: its inputs were visible to the developer before the fixes.

Draft references for E101-E200 are in `ai_review/proposed_labels_v2.csv`. Humans must accept/correct and sign them before guarded import into `eval_set_v2_reviewed.csv`. They are not ground truth or model predictions.

## Expected answers before prediction

A real reviewer fills `expected_severity` (P1/P2/P3/P4/ABSTAIN), `expected_effective_priority`, `expected_team`, `expected_output_or_action`, `evidence_or_source`, optional relevant `expected_evidence_ids` separated by `|`, `hand_over_to_a_person` (yes/no), `segment`, their actual `labelled_by` and `labelled_at`, and `label_status=human_verified` after review.

P1: active compromise or business-critical outage; P2: major degradation; P3: limited issue or usable workaround; P4: question/routine request. ABSTAIN means insufficient or unsupported context. These are review guidelines, not permission to infer missing facts. A preserved priority during abstention does not prove low impact.

Teams: Incident Response, Identity, Platform, Endpoint, Reporting, Integrations, Detection Engineering, Awareness module, Account Management, Customer Success, Network, Human triage. Decide ambiguous ownership before freeze. Never automatically lower a declared priority. Expected effective priority refers to the documented assisted demonstration policy, distinct from suggestions-only default.

## Freeze and run

Run from the repository root. First review and import the proposed references following VALIDATION_EQUIPE.md to create eval_set_v2_reviewed.csv. Existing directories and predictions must be preserved.

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate validate --cases evals/eval_set_v2_reviewed.csv
# Only after actual human labels and semantic overlap review:
uv run --frozen --python 3.12 python -m prototype.evaluate freeze --cases evals/eval_set_v2_reviewed.csv --run-dir evals/runs/v2
uv run --frozen --python 3.12 python -m prototype.evaluate run --cases evals/eval_set_v2_reviewed.csv --run-dir evals/runs/v2
```

Candidate validation intentionally fails before human annotation. Freeze records case/model hashes. Run refuses changed references/model and refuses an existing prediction file. Legacy LF/CRLF-only conversion is allowed for text-file hashes; JSON reformatting, extra spaces, changed fields and other edits are not. Original historical hashes remain unchanged. A model source/runtime fingerprint is still checked for a new run; newline portability does not waive model identity.

## Human grading

Each person reads every case, reference and output independently before comparing decisions. Fill `grading_a.csv` and `grading_b.csv` with the actual grader, yes/no `usable_as_is`, a reason for every grade and the responsible component for failures. The same 50 or 100 outputs are graded by each person; do not split them between graders.

An unchanged acceptable triage needs all of the following:

| Criterion | Requirement |
|---|---|
| Severity | Matches the reviewed expected severity; ABSTAIN produces no severity |
| Effective priority | Never below declaration, and raised where the reference requires it |
| Team | Matches the agreed owning team or expected Human triage |
| Human handover | Correct verification/abstention behaviour; no privileged or legal action executed |
| Grounding | No invented fact/procedure; a relevant source for routine triages. A missing-source handover may be safe but does not establish a grounded routine success |

Components: classifier, rules, routing, retrieval, policy, sla, redaction, ui. Optional `elapsed_seconds` is review duration, not a controlled estimate of handling time saved. Preserve original disagreements after later discussion.

The main archived sheets began from LLM-judge prefill. Human review can correct them, but this introduces anchoring and is different from two blind initial judgements. Luna confirmed actual review of sheets bearing her name on 23 November; [record](finalisation_2026_11_23/luna_grading_confirmation.json). That confirmation does not label E101-E200 or sign off training/production use.

## Recompute without overwriting evidence

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --cases evals/eval_set_v0.csv --run-dir evals/runs/v0 --check-only
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --cases evals/eval_set_v1_fresh.csv --run-dir evals/runs/v1_fresh --check-only
uv run --frozen --python 3.12 python -m prototype.audit_submission
```

Without `--check-only`, summarise writes metrics for a newly graded run. The finalisation audit uses read-only computation and separately checks frozen evidence, customer isolation and never-lower. It does not run predictions.

Routine acceptance uses all cases human-labelled P3/P4 as denominator, including abstentions and missing-source cases. P1 recall counts abstention as missed. False-P1 rate uses expected P2/P3/P4, excluding ABSTAIN references that do not establish non-P1 truth. Report exact counts by segment. The 62% gate is an assumption-based proxy for the memo's 17% timing threshold; no actual time saving is established by it.

## Archived judge calibration

The golden 30 reports 29/30 human-human agreement and 29/29 human-judge agreement on the subset where both people agree. The many rejected cases, selected denominator and small sample limit the interpretation. On the additional 50-case batch, recorded human-human agreement is 47/50; judge A agrees with grader A on 50/50 and with B on 47/50. These are agreement measures, not proof of unbiased independent correctness.

Original sheets, prompt, guideline and disagreement notes remain under `runs/` and in [the report](report_v0.md). The next genuinely independent evaluation must retain disagreements and avoid selecting only cases where judges agree.
