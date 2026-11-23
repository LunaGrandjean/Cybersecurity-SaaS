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
The sheets record grader A as **Malek Saoudi** and grader B as **Luna Grandjean** for the run dated 22 November 2026 (`grading_a.csv`, `grading_b.csv`). Luna explicitly confirmed her actual review on 23 November. The recorded method follows the guideline in `evals/README.md`, which was committed before grading. They disagree on **1 / 50 cases (98 % agreement)**: on E032, A accepts and B rejects because the effective priority is P1 where P3 was expected. Original grades are preserved and there was no adjudication. Graders A and B reviewed and signed each grade, starting from an LLM-judge pre-fill (`evals/runs/v0/ai_judge/`, prompt `evals/judge_prompt.txt`).

## 4. Demo versus evaluation
Jane's original 20 examples, the six interactive demo tickets and all engineering regression cases were exposed during development, so they are excluded from this holdout (`demo_reference_v0.csv`, unchanged). E050 was replaced before freezing because it overlapped TRAIN-P4-03 (`evals/ai_review/replaced/`). **All 50 E-cases are now exposed:** their outputs were read for grading. Any change to the model made after reading them must be evaluated on fresh cases (`eval_set_v1.csv`), not on these 50.

## 5. Next step at the end of the initial run
The steps in this paragraph were subsequently implemented for v0.5 (section 8). Implement EVAL-01 to EVAL-05 without looking at these 50 outputs again, then evaluate on a fresh, labelled set before any integration budget. The priority order is P1 recall (a catastrophic miss), then the raise rule (16 cases, a mostly mechanical fix), then routing.

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

At the time of the 15 November diagnostic, the proposed references were drafts and the official run had not occurred. Those 50 references were subsequently reviewed, E050 was replaced and the run was executed on 22 November (sections 1-5). This historical diagnostic is not the current product verdict.

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

[Raw post-fix outputs and comparison](ai_review/post_fix_2026_11_15/comparison.md). Perfect source-id overlap is not proof of relevant troubleshooting. No human acceptance result or measured time saving is claimed. At the time of that development diagnostic the official run was pending; its later misses are now reported in sections 2 and 8.

For a future genuinely unseen batch, follow [team validation instructions](VALIDATION_EQUIPE.md). Existing runs and grades must remain preserved. The import helper does not create human review or invoke inference.

## 8. v0.5 on fresh cases: after fixing EVAL-01 to EVAL-05 (22 November 2026)
**Engine v0.5** (`e4ef11ac89758672`) implements spec EVAL-01 to EVAL-05: account-takeover, retained-access and cross-tenant P1 rules; explicit "no incident" wording caps a classifier P1; abstention on attachment-only, legal, other-customer-data, prompt-injection, unverified privileged-change and vague tickets; raising the effective priority whenever the proposal is higher (assisted mode, never lowering); a wider routing vocabulary. The rules were developed on the exposed v0 cases only (development check: P1 recall 14/14, false P1 3/28). The engine was frozen, then run **once** on the 50 **fresh** cases E051–E100 of `eval_set_v1.csv`, which were labelled by the team before the run (`evals/eval_set_v1_fresh.csv`; run `evals/runs/v1_fresh`; cases SHA-256 `66303cc4…`; predictions SHA-256 `46a2b526…`). Caveat: the person writing the fixes had seen the v1 inputs; the fixes follow the spec patterns, not individual v1 tickets.

| Measure | v0 (E001–E050) | **v0.5 (E051–E100, fresh)** | Criterion |
|---|---|---|---|
| P3/P4 triages both graders accept unchanged | 2/17 = 11.8 % | **9/22 = 40.9 %** | ≥ 62 % → not met |
| P1 recall | 11/14 = 78.6 % | **9/14 = 64.3 %** | 100 % → **not met** |
| False-P1 rate | 7/28 = 25 % | **3/28 = 10.7 %** | ≤ 15 % → **met** |
| Severity accuracy | 66 % | **72 %** | — |
| Effective-priority accuracy | 58 % | **74 %** | — |
| Team accuracy | 34 % | **68 %** | — |
| Handover agreement | 92 % | **94 %** | — |
| Expected source in top 3 | 41 % | **59 %** (22/37) | — |
| ABSTAIN cases that abstain | 2/8 | **7/8** | — |
| Outputs sent to Human triage | 31/50 | **9/50** | — |
| Priority lowered below declared | 0 | **0** | 0 → met |

Both graders accept, by segment: P1 2/14, P2 4/6, P3 4/15, P4 5/7, ABSTAIN 7/8; EN 13/27, FR 7/21; Enterprise 13/30, Standard 9/20.

**Graders:** Malek Saoudi (`grading_a.csv`) and Luna Grandjean (`grading_b.csv`) disagree on **3/50 cases (94 % agreement)**: E059, E063 and E066, all borderline (a correct triage with off-topic sources, Human triage on a P1, a P2 proposed for a P3). The LLM judge (two runs, `evals/runs/v1_fresh/ai_judge/`) agrees with grader A on 50/50 and with grader B on 47/50.

**Three most frequent misses on fresh cases** (grader A):

| Frequency | Failure and case ids | Component | New spec requirement |
|---|---|---|---|
| 14/50 | **Wrong severity.** 5 real P1s of *new attack types* proposed as P3/P4: mass sensor removal (E054), production API key used from an unknown address (E055), detection silently off fleet-wide (E058), uncontrolled remote session (E062), credential dumping on a domain controller (E064). Plus over-escalation of P3 tickets to P2/P1 (E065, E066, E071, E074, E080, E083, E085) | `classifier` | EVAL-06, EVAL-07 |
| 8/50 | **P1 routed to the component team instead of Incident Response** (e.g. E051, E053, E057, E060, E063) | `routing` | EVAL-08 |
| 5/50 | **Correct triage, but the cited sources do not address the component** (E059, E068, E070, E077, E088) | `retrieval` | EVAL-09 |

**Interpretation.** Routine acceptance, routing and false-P1 rate are better in the second recorded batch, while P1 recall is lower. Different batches and model versions prevent a controlled causal comparison. The second batch's inputs had also been visible to the developer, so these results do not demonstrate fully blind generalisation. They reveal continuing coverage gaps; they do not by themselves measure temporal concept drift. **Launch decision:** no live assisted mode; the current release remains a local synthetic-data demonstration. [Final launch memo](../08_launch_memo.md).

## 9. Finalisation audit and review confirmation - 23 November 2026

Luna explicitly confirmed actual review and approval of all grading sheets bearing her name, including both grading_b files and the golden30 blind_b sheet. [Confirmation and file hashes](finalisation_2026_11_23/luna_grading_confirmation.json). This does not validate future cases, training labels or operational approval. The original main sheets used judge-prefilled answers, so agreement rates remain subject to anchoring; no additional blind review is invented.

Both recorded metrics files are recomputed with the check-only summary during finalisation. The initial prediction hash matches only after reconstructing its original Windows CRLF line endings; Git had converted the file to LF. Only that newline equivalence is accepted; other content changes still fail. No original run, grade, case reference, model source or training fixture is rewritten.

The initial ABSTAIN comparison in section 8 is corrected from 0/8 to **2/8**, based on the actual preserved outputs. Latest actual abstention is 7/8 and assisted raises are 21/50 (initially 0/50). These are descriptive counts, not a new evaluation.

There are 100 recorded reviewed cases and 100 new input candidates E101-E200. The target of 200 reviewed cases remains pending semantic overlap review and actual human labels for the candidates. The candidates have not been run through the model and carry no generated human signatures. Real user interviews, measured time saving and training/source review are also not completed by this finalisation.

[Current metrics](../05_metrics.md) | [Final product brief](../product_brief.md) | [Finalisation status](../FINALISATION.md).
