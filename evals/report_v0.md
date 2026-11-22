# Eval report v0 — SLA-aware triage copilot

**Prepared:** 12 November 2026 · **Run:** 22 November 2026 · **Verdict: CRITERION NOT MET**
Prototype v0.4 · run `evals/runs/v0` · model `3e5517585b1eeb42` · mode `assisted` · cases SHA-256 `2db7b5c4…aec3` · predictions SHA-256 `c1d05b39…d09`. Labels were human-reviewed and frozen at 00:43 (UTC+01:00), and the run was executed once, 3 seconds later. Full output: `evals/runs/v0/metrics.json`.

## 1. Number against the criterion
| Measure | Result | Criterion |
|---|---|---|
| Cases | 50 human-labelled cases in `eval_set_v0.csv` (14 P1, 11 P2, 10 P3, 7 P4, 8 ABSTAIN; 34 EN, 14 FR, 1 DE, 1 ES) | — |
| **P3/P4 triages both graders accept unchanged** | **2 / 17 = 11.8 %** | ≥ 62 % → **not met** |
| **P1 recall** | **11 / 14 = 78.6 %** (missed: E003, E012, E015) | 100 % → **not met** |
| **False-P1 rate** | **7 / 28 = 25 %** (E004, E017, E024, E035, E039, E049, E050) | ≤ 15 % → **not met** |
| Severity accuracy | 33 / 50 = 66 % | — |
| Effective-priority accuracy | 29 / 50 = 58 % | — |
| Team accuracy | 17 / 50 = 34 % | — |
| Handover agreement | 46 / 50 = 92 % | — |
| Expected source in top 3 | 14 / 34 = 41 % | — |
| Priority lowered below the declared priority | **0 / 50** | 0 → met |
| Actual handling time saved | Not measured; acceptance is only a proxy | ≥ 17 % |

By segment, the cases both graders accept: P1 0/14, P2 1/11, P3 1/10, P4 1/7, ABSTAIN 2/8; EN 2/34, FR 1/14; Enterprise 4/38, Standard 1/12. On this run, v0.4 is safe on the "never lower" rule, but it is not useful yet: it would save almost no engineer time, and it misses 3 real P1s.

## 2. Three most frequent misses
Counts are cases that grader A marked `no`; grader B's counts are the same except for E032.

| Frequency | Failure and case ids | Component | New spec requirement |
|---|---|---|---|
| 17 / 50 | **Wrong severity.** 3 real P1s proposed as P3/P4 (E003 recovery address replaced, E012 contractor admin access kept, E015 cross-tenant data visible); 7 false P1s on P2–P4 tickets (E004, E017, E024, E035, E039, E049, E050); 6 of 8 ABSTAIN cases get a severity (E041, E042, E045, E046, E047, E048) | `classifier` | EVAL-01, EVAL-02, EVAL-03 |
| 16 / 50 | **Effective priority not raised.** Severity is often right, but the effective priority stays at the declared priority (e.g. E007 and E011: expected P1, left at P4). The run shows 0 automatic raises in assisted mode | `sla` / raise rule | EVAL-04 |
| 9 / 50 | **Team left to "Human triage"** although the expected answer names a team (E008, E016, E018, E022, E026, E033, E034, E036, E038); 31 of the 50 outputs go to Human triage overall, 24 of them where a named team was expected | `routing` | EVAL-05 |

Single misses: E029 sends to a person a ticket that needs no handover (`policy`); E030 cites an irrelevant source, KB-DET-01, instead of KB-INT-01 (`retrieval`).

## 3. Graders
Grader A was **Malek Saoudi**, grader B **Luna Grandjean**, 22 November 2026 (`grading_a.csv`, `grading_b.csv`), following the guideline in `evals/README.md`, which was committed before grading. They disagree on **1 / 50 cases (98 % agreement)**: on E032, A accepts and B rejects because the effective priority is P1 where P3 was expected. Original grades are preserved and there was no adjudication. Graders A and B reviewed and signed each grade, starting from an LLM-judge pre-fill (`evals/runs/v0/ai_judge/`, prompt `evals/judge_prompt.txt`).

## 4. Demo versus evaluation
Jane's original 20 examples, the six interactive demo tickets and all engineering regression cases were exposed during development, so they are excluded from this holdout (`demo_reference_v0.csv`, unchanged). E050 was replaced before freezing because it overlapped TRAIN-P4-03 (`evals/ai_review/replaced/`). **All 50 E-cases are now exposed:** their outputs were read for grading. Any change to the model made after reading them must be evaluated on fresh cases (`eval_set_v1.csv`), not on these 50.

## 5. Next step
Implement EVAL-01 to EVAL-05 without looking at these 50 outputs again, then evaluate on a fresh, labelled set before any integration budget. The priority order is P1 recall (a catastrophic miss), then the raise rule (16 cases, a mostly mechanical fix), then routing.

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
