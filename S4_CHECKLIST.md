# Assignment 4 handoff — 15 November 2026, 23:59

## Built in this working tree
- Functional local console derived from Jane's v0.2; new-ticket API, classifier, rules, retrieval, manual correction, SQLite audit and global suggestions-only switch.
- 300 synthetic training rows: P1 70 / P2 75 / P3 90 / P4 65; AI-proposed labels clearly identified.
- 50 separate evaluation candidate inputs, with expected labels intentionally blank.
- Evaluation validation/freeze/run/two-grader/summarise commands.
- Guarded import of actual reviewed corrections, preserving original inputs and refusing incomplete reviewer decision/name/date fields.
- Architecture, spec v2, S4 governance and reproducible engineering checks.

## Team actions still required for the graded submission
1. Review the proposed training labels and resolve ambiguous severity definitions. Freeze model/data before holdout exposure.
2. Read and annotate all 50 evaluation cases yourselves. Review near-duplicates and remove any demo overlap. The AI cannot certify these answers for you.
3. Run the frozen evaluation; two actual people independently grade every output. Fill report v0 with exact metrics and the three frequent misses, then turn each miss into a spec requirement. Keep the original run when tuning a later version.
4. Run the global switch yourselves and record the responsible person's name/date. Current engineering evidence does not substitute for team sign-off.
5. Make commits with your own Git accounts. Suggested reviewable slices: classifier/data; rules/redaction/SLA; retrieval/UI; evaluation/spec/governance. The assignment says four authors while this repository lists three team members: ask the lecturer how that applies; never invent an author.
6. The consigne also asks to run `support-copilot-starter.zip` once. It is not present among the downloaded materials, so no Paylio-starter execution is claimed here. Obtain/run it if required; the project workflow itself is implemented independently.
7. S3 research remains explicitly simulated; replace it with actual conversations/role-play observations as required by the course, without inventing quotations.

`report_v0.md` must remain pending until the human steps are actually done. A passing engineering test suite is not proof of the 62% product criterion or 17% measured handling-time savings. Target 200 reviewed holdout cases for S5 after the S4 run.

## Update — 15 November 2026
- 50 **AI-proposed** corrections are ready in `evals/ai_review/proposed_labels_v0.csv`; they are not human verified and contain no human signatures.
- The initial diagnostic (severity 16/20, proposed-P1 recall 6/8) is preserved. Technical corrections now give severity 20/20, proposed P1 8/8, route 17/20 and source-id hit 20/20 on the SAME exposed development cases; this is not independent test evidence.
- Corrected large outbound anomalies, suspected breach plus legal handling, service-impact rules and bilingual retrieval. Three routing conventions remain C09/C15/C17; settle ownership before freeze. See `spec.md` DEV-01–06.
- 29 code/API/protocol/import tests and 16 real Edge checks passed on 15 November. The official 50 cases have not been predicted.
- Suggested label review only (not completed work): Jane E001–E017, Malek E018–E034, Luna E035–E050. Afterwards two actual people each grade all 50 outputs independently.
- Follow [the French team guide](evals/VALIDATION_EQUIPE.md) for reviewed-label import, freeze/run, grading, switch sign-off and submission.
- Read [BILAN_S4_15_NOV.md](BILAN_S4_15_NOV.md) for the current completed/pending status. Files are still local working-tree changes; commit and push the submission with your own accounts before the course deadline.
