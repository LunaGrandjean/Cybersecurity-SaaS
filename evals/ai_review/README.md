# Reference preparation and historical diagnostics

**Current state on 23 November 2026.** The draft references were reviewed and recorded evaluations now exist. This folder contains preparation/history; [the current report](../report_v0.md) and [launch decision](../../08_launch_memo.md) govern the product status.

## Files

- `proposed_labels_v0.csv`: the reviewed working references for the original 50 cases. Actual reviewer fields record the subsequent human decisions; initial preparation is not itself a human validation.
- `proposed_labels_v1.csv`: reviewed working references for the 50 additional cases. Canonical snapshots and frozen runs are preserved under the main evals directory.
- `replaced/E050_v0_replaced.csv`: the old E050 retained when its overlap with training was identified. The replacement was made before the first freeze.
- `demo_reference_adapted.json`, `demo_diagnostic.json`, `demo_diagnostic.csv`, `diagnostic_report.md`: initial 15 November exploratory comparisons on 20 exposed examples only.
- `post_fix_2026_11_15/`: separate post-fix development run with the same provisional references, [comparison](post_fix_2026_11_15/comparison.md). This is tuning evidence, not the official evaluation.

The diagnostic scripts did not predict the official cases. The later 22 November runs are recorded elsewhere; do not use historical pending-label descriptions as the current status.

`proposed_labels_v2.csv` contains expected answers for E101-E200, before any model output. Luna approved E151-E200 on 23 November 2026; her first name, actual registration time and decisions are recorded. E101-E150 still await Jane's actual review. Semantic family similarities remain disclosed and require resolution before an independent holdout; no model output has been graded by this reference approval.

The [E151-E200 preparatory review](review_E151_E200_2026-11-23.md) explains each of Luna's 50 references and the routing corrections for E162, E170 and E172. Luna subsequently approved them and the proposed E174 replacement: a coordinated-vulnerability-disclosure documentation question replaces the browser-support question that repeated E092. The [confirmation record](luna_confirmation_E151_E200_2026-11-23.json) preserves that explicit agreement and the former E174. The preparatory JSON remains a historical snapshot; other family similarities still need arbitration, and this is not a model evaluation.

## Human review and next batch

Luna confirmed actual review of all existing grading sheets bearing her name on 23 November 2026; [dated confirmation and file hashes](../finalisation_2026_11_23/luna_grading_confirmation.json). This does not authorise signatures for a new scenario or establish an independent blind study. The main recorded sheets used judge-prefilled answers, as disclosed in the report.

E101-E200 in `../eval_set_v2_candidates.csv` remain input-only candidates; approved expected answers are recorded separately in `proposed_labels_v2.csv`. E174's approved replacement is aligned in both files. Predictions have not been exposed and semantic independence still requires review. Follow [VALIDATION_EQUIPE.md](../VALIDATION_EQUIPE.md) before a new freeze/run. Never turn a preparation script or a judge output into a human signature.
