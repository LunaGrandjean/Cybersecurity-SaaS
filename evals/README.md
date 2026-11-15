# S4 evaluation — annotate first, run second

`eval_set_v0.csv` contains **50 new synthetic INPUTS, not 50 human-labelled cases**.
`demo_reference_v0.csv` preserves Jane's original 20 examples; these have been exposed during design and must not be used for an independent success claim. The original course guide is retained as `course_eval_guide.md`.

**Team handoff:** [instructions en français et commandes](VALIDATION_EQUIPE.md). The guarded import creates a reviewed CSV only after all 50 rows have an explicit human decision/name/date. It does not execute inference or generate human grades.

## Human annotation before inference
For every case, a team member fills these columns without consulting model predictions:

| Column | Required value |
|---|---|
| `expected_severity` | P1, P2, P3, P4 or ABSTAIN (insufficient/unsupported input) |
| `expected_effective_priority` | Priority actually kept/applied in **assisted** mode; never automatically less urgent than declared |
| `expected_team` | One team from the list below |
| `expected_output_or_action` | Concrete acceptable decision, constraints and explanation |
| `evidence_or_source` | Written severity guideline, precise ticket facts and/or KB ids |
| `expected_evidence_ids` | Optional relevant KB/resolved ids separated by `|`; leave blank if none should be returned |
| `hand_over_to_a_person` | Exactly `yes` or `no`; distinguish automatic raising from P1/P2 engineer review |
| `segment` | Severity, tier, language and scenario type for later breakdown |
| `labelled_by`, `labelled_at` | Actual human name and ISO timestamp |
| `label_status` | Change to `human_verified` only after a human has decided the expected answer |

Teams: Incident Response · Identity · Platform · Endpoint · Reporting · Integrations · Detection Engineering · Awareness module · Account Management · Customer Success · Network · Human triage.

Suggested rubric (team must approve): P1 active compromise or business-critical service down; P2 major degradation; P3 limited issue / usable workaround; P4 question or routine request. Severity and contract tier are different. The declared priority is an input, not the correct answer. A P1-declared ticket that merits P2 still stays P1 until an engineer approves lowering. Do not infer facts absent from the input. Ambiguous cases need explicit human handling.

Review scenario families and near-duplicates against `prototype/data/training_tickets.csv`, the demo and KB. Sharing a general topic is normal; repeating a specific incident with changed names is leakage. All variants of an incident belong on the same side. The scripts check ids and exact text, not semantic independence.

## Freeze and run
Commands are in `prototype/README.md`. `freeze` records the case hash and model/data version. `run` refuses pending labels or changes to that frozen state; outputs are never used to retrain automatically. A run directory is immutable: keep original outputs and record a fresh holdout for a later tuned model. The default remains assisted mode for a reproducible comparison, regardless of the console's persisted global switch.

## Two independent graders
Each grader reads the input, frozen expected answer and `predictions.json`, then fills their own grading CSV. Do not consult the other grader before submitting. `usable_as_is=yes` requires correct severity/team, appropriate evidence, no invented fact, correct never-lower/handover behaviour and at least one relevant source for routine cases. Abstentions and missing-source routine cases remain in the denominator. A synthetic KB's simulated sign-off is not proof of real operational validity.

Record `reason` for **every** grade and `component` for a failure (`classifier`, `rules`, `routing`, `retrieval`, `policy`, `sla`, `redaction`, `ui`). `elapsed_seconds` is optional review time, not a measured baseline saving. The acceptance metric uses both graders' agreement on `yes`; disagreements are counted and can be discussed separately without changing the original grades.

`summarise` creates `metrics.json`, including P3/P4 acceptance, P1 recall (abstention counts as not detected), false-P1 rate among labelled non-P1 cases, classification/team agreement, disagreements and three frequent misses. False-P1 ≤15% is an offline guardrail; >20% over a week is the brief's separate proposed production rollback trigger. Neither is established by engineering tests.

The ≥62% criterion is a **proxy** derived from guessed minutes, not proof of ≥17% real handling-time savings. That requires a separately timed comparison with/without the assistant. Grow to 200 genuinely reviewed cases for S5; do not count 200 paraphrases as 200 independent incidents.
