# Eval report v0 — SLA-aware triage copilot

**Prepared:** 12 November 2026 · **Verdict: PENDING HUMAN EVALUATION**
Prototype: v0.4. No measured product performance is claimed.

## 1. Number against the criterion
| Measure | Result |
|---|---|
| Candidate cases | 50 AI-generated inputs in `eval_set_v0.csv` |
| Human-verified expected outputs | Pending; expected columns deliberately blank |
| Frozen independent run | Not yet performed |
| P3/P4 triages both graders accept unchanged (criterion ≥62%) | Not measured |
| P1 recall (criterion 100% on this finite holdout) | Not measured |
| False-P1 rate (offline target ≤15% of non-P1 cases) | Not measured |
| Actual handling time saved (memo threshold ≥17%) | Not measured; ≥62% acceptance is an assumption-based proxy |
| Engineering regression / browser checks | See `engineering_checks.md`; these are not independent product evaluation |

After real human labels and two independent grading files, run `python -m prototype.evaluate summarise` and copy the exact run id, case/model hashes, counts, segment results and disagreements here. An unsupported/uncertain routine case remains in the P3/P4 denominator, rather than being excluded to improve the score.

## 2. Three most frequent misses
**Pending the independent run.** Do not invent misses or replace this table with unit-test results.

| Frequency | Failure and case ids | Component | New spec requirement |
|---|---|---|---|
| Pending | Pending | Pending | Pending |
| Pending | Pending | Pending | Pending |
| Pending | Pending | Pending | Pending |

Known engineering issues found before holdout execution are recorded separately in `spec.md` v2: hard-coded decisions, unsupported assertions, weak-confidence acceptance, takeover controls, source isolation, original SLA timestamp and persistent global override. They are not the three statistically most frequent product misses.

## 3. Graders
Two actual people must independently grade every output. Names, dates, disagreements and any later adjudication: **pending**. Neither AI-proposed training labels nor generated inputs are human judgments. No signed-off research interview or grading session is fabricated.

## 4. Demo versus evaluation
Jane's original 20 examples, six interactive demo tickets and all engineering regression cases were exposed during development and are excluded from the new holdout. The old CSV is preserved unchanged as `demo_reference_v0.csv`; C19's declared P1 / expected P2 inconsistency must not become an automatic downgrade rule. The new 50 inputs were prepared independently of training families and have not been run through the model. They require a final human near-duplicate review and expected answers **before** freeze. If anyone tunes while viewing a case's output, reclassify that case as demo data and replace it in the independent holdout.

## 5. Next step
Review synthetic training labels, human-annotate the holdout, freeze labels/model, run once, collect two independent grades, then add every observed miss to the next spec. Do not release an integration budget based on this pending report.

## 6. Preserved initial exploratory diagnostic — 15 November 2026
An automatic diagnostic was executed on the **20 exposed demo references only**, not on E001–E050. No human grades were created or attributed. Reference interpretations were prepared before predictions but are not independently certified.

| Mechanical comparison with provisional demo reference | Result |
|---|---|
| Severity agreement | 16/20 = 80% |
| Team agreement | 14/20 = 70% |
| Candidate expected source found in top 3 | 15/20 = 75% |
| P1 detected in the proposed severity | 6/8 = 75% |
| False P1 suggestions among reference non-P1s | 0/12 |
| Declared priority never automatically lowered | 20/20 |
| Same-customer or generic sources only | 20/20 |

Frequent disagreement categories overlap: routing 6 cases, source retrieval 5 cases, severity 4 cases. These are exploratory comparisons, **not** the official two-human acceptance result. Routing references in particular need human agreement on team ownership.

Critical examples in this initial run: C03 suggested P4 for a possible exfiltration and retained declared P4; C18 suggested P4 for a possible breach mixed with a legal question, but correctly retained declared P1 and required human review. Preserving declared priority cannot by itself detect a customer's under-declared emergency. Subsequent corrections are in section 7.

Full initial evidence: [diagnostic report](ai_review/diagnostic_report.md), [raw outputs](ai_review/demo_diagnostic.json). Baseline model fingerprint: `41acde6fcf51b4c1`. The code was subsequently corrected using these exposed development cases; see section 7. These cases are excluded from the independent holdout.

The [50 proposed corrections](ai_review/proposed_labels_v0.csv) are explicitly AI-authored drafts, with human names/dates left blank. Canonical E001–E050 labels remain pending and their predictions have not been exposed by either diagnostic. **Official verdict stays pending human evaluation.** The initial demo P1 recall failed its target; subsequent development correction is recorded separately below.

## 7. Post-fix development diagnostic — 15 November 2026

Actual new run: model `e472b6a6d01222de`, same 20 exposed demo cases and **byte-identical provisional expected references**. Original outputs were preserved. The code was tuned using these cases, so this result cannot establish generalisation or satisfy the two-grader criterion.

| Mechanical comparison | Initial | Post-fix |
|---|---|---|
| Proposed severity agreement | 16/20 | 20/20 |
| Team agreement | 14/20 | 17/20 |
| Candidate source hit in top 3 | 15/20 | 20/20 |
| Proposed P1 detected | 6/8 | 8/8 |
| False P1 among provisional non-P1s | 0/12 | 0/12 |
| Never lower / customer isolation | 20/20 each | 20/20 each |

C03 now surfaces a possible incident and raises P4 to P1 in assisted mode. C18 proposes P1 while preserving human-only legal handling. Contextual service-impact rules and bilingual search aliases address the other exposed severity/source misses. Three route disagreements remain: C09 (reports-page outage), C15 (mixed administrator/dashboard help), C17 (cosmetic report-logo request). Team ownership needs agreement; these are not three independently established model failures. Each development miss led to a marked requirement in `spec.md` DEV-01–06.

[Raw post-fix outputs and comparison](ai_review/post_fix_2026_11_15/comparison.md). Perfect source-id overlap is not proof of relevant troubleshooting. No human acceptance result or measured time saving is claimed. The official top-three-misses section remains pending the real independent run.

Next: [team validation instructions](VALIDATION_EQUIPE.md), then freeze/run, two independent grades and exact reporting. The import helper refuses incomplete review, never generates grades and never invokes inference.
