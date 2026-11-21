# AI-assisted preparation — not human grading

Prepared on **15 November 2026**. No evaluation is attributed to Jane, Malek or Luna. No human name, signature, grade or review time has been invented.

## Files
- `proposed_labels_v0.csv`: 50 proposed corrections for E001–E050, authored by an AI assistant from ticket facts and the written rubric. Includes explicit uncertainty notes. Human fields remain blank and status is `ai_proposed_pending_human_review`.
- `demo_reference_adapted.json`: proposed structured interpretation of Jane's original 20 exposed demo examples, saved before computing predictions. C19 proposes P2 but its declared P1 must remain effective until a human approves lowering.
- `demo_diagnostic.json` / `.csv`: actual model outputs and mechanical comparisons on those **20 exposed demo cases only**. They are neither two independent graders nor an official test result.
- `diagnostic_report.md`: readable exploratory results and component-level misses, generated from the actual diagnostic output.

The canonical `evals/eval_set_v0.csv` remains unlabelled and is NOT passed to the model by either preparation script. It can still be used for the first human-labelled test if nobody has separately exposed its predictions.

The baseline above is preserved. A separate post-fix diagnostic is in `post_fix_2026_11_15/`: same provisional references, no official holdout inference. See [before/after comparison](post_fix_2026_11_15/comparison.md).

For the actual team review, follow [VALIDATION_EQUIPE.md](../VALIDATION_EQUIPE.md). `prototype.import_review` checks actual decision/name/date fields and writes a new reviewed CSV without creating predictions or overwriting earlier annotations.

## AI re-review of E035–E050 — 18 November 2026

The 16 proposed references assigned to Luna were reviewed again against the inputs, rubric and actual KB text, without running the model. See [the case-by-case review](review_E035_E050_2026-11-18.md) and [structured review decisions](review_E035_E050_2026-11-18.json). Only their proposed actions, source references, handover flags and AI notes were updated; other cases and human fields were preserved. The canonical evaluation CSV remains unchanged and human validation is still pending.

Four unsupported expected source matches were removed (E035, E037, E039, E048); E035/E039 now explicitly require a human because there is no sufficiently relevant source. E050 closely overlaps training family `TRAIN-P4-03`: replacement is recommended before an independent evaluation. No input was silently replaced, and the classifier/training data were not changed in response to these cases.

## Suggested work distribution, not a record of completed work
| Proposed task owner | Initial label review |
|---|---|
| Jane | E001–E017 |
| Malek | E018–E034 |
| Luna | E035–E050 |

Each person reads the original input, considers the AI proposal critically, accepts or corrects it, and records their own real name/date. Cases with `ai_uncertainty` need agreement on the rubric before the first model run. Copy only genuinely reviewed answers into the canonical CSV; set `human_verified` only after that actual review. Optional `human_decision` / `human_comment` columns are working notes, not a signature.

After labels/model are frozen and the 50 cases have run, **two people each grade all 50 outputs independently**. For example Jane could fill grading A and Malek grading B, while Luna coordinates disagreements; these are suggested future roles only. Do not split the two-grader requirement into 25 cases per person. Preserve the original grades.

Mechanical severity/team/source agreement on the demo does not establish the ≥62% two-human acceptance criterion, measured ≥17% time saving, or a calibrated confidence score. The official report must disclose the actual method and any remaining human work.

## Human review status as of 21 November 2026

- E018-E034: Malek Saoudi accepted the proposed labels on 17 November; the review fields are complete.
- E035-E049: Luna Grandjean approved the labels on 18 November; the review fields are complete.
- E050: Luna marked the original case for replacement because it overlaps training family `TRAIN-P4-03`. E050 was replaced on 22 November 2026 by a new independent case (R1, incident family `EVAL-ONLY-050-R1`, a French holiday support-coverage question with no overlap with training). Malek Saoudi reviewed and approved its expected reference on behalf of Luna Grandjean. The original row is kept in `evals/ai_review/replaced/E050_v0_replaced.csv`.
- E001-E017: Jane Galthie reviewed E001-E017 with Malek Saoudi on 17 November 2026 (16:00-17:00, UTC+01:00); her rows are timestamped 2026-11-17T16:42:18+01:00, during that session. 12 accepted, 5 corrected (E003, E004, E007, E009, E015).

The combined proposal CSV preserves each person's recorded work. `evals/eval_set_v0.csv` remains unlabelled, and the official 50-case evaluation has not been run. All 50 references are now human-reviewed and pass the guarded import check; next: import, freeze, then run the holdout.