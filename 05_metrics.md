# 05 Metrics for the SLA triage copilot

**Updated 23 November 2026 | Latest evidence: engine v0.5 on E051-E100 | Decision: no live assisted launch**

## Measurement stack

| Level | Metric | Current result | Owner and proposed cadence |
|---|---|---|---|
| Business | Observed handling-time reduction and avoided SLA penalties | Not measured; investment values remain hypotheses | Head of Support, after an approved pilot |
| Product | Routine triages engineers accept unchanged | No live usage; offline proxy 9/22 = 40.9% | Support lead, weekly in a future pilot |
| Safety | Expected P1s proposed P1; no automatic lowering | 9/14 = 64.3%; 0/50 lowerings | Head of Support, each release and daily live monitoring if approved |
| AI system | Human-labelled P3/P4 accepted by both recorded graders | 9/22 = 40.9%, below 62% | Team 8, each frozen evaluation |
| Components | Severity, routing, source coverage and handover agreement | 36/50 = 72%; 34/50 = 68%; 22/37 = 59.5%; 47/50 = 94% | Team 8, development diagnostics |

All current counts are offline synthetic evaluations. The [report](evals/report_v0.md) records both runs and their methods. Neither a passing unit test nor an LLM-judge agreement rate measures business value.

## Definitions and release gates

- **Routine acceptance:** human-labelled P3/P4 cases accepted unchanged by both recorded graders divided by all human-labelled P3/P4 cases. Use the expected severity fixed before prediction, not the model's proposed label. Abstentions, missing sources and handovers stay in the denominator.
- **P1 recall:** expected P1 cases proposed P1 divided by all expected P1 cases. Abstention counts as not detected. Latest 9/14; required 14/14 on this finite batch. This is not a production guarantee.
- **False-P1 rate:** P1 proposals on expected P2/P3/P4 divided by expected P2/P3/P4 cases: 3/28 = 10.7%. ABSTAIN references are excluded because they do not establish a true non-P1 severity; report their behaviour separately. Target at most 15%.
- **Never lower:** automatic effective priority must never be less urgent than the declaration. Latest 0/50 violations. Later reasoned human corrections are different actions.
- **Source hit@3:** cases returning at least one expected candidate source id divided by cases with such ids: 22/37. A matching id does not prove the passage supports a correct fix.

**Stop decision:** do not ship because one component score improves. Routine acceptance must reach 62%, P1 recall must meet its floor, false-P1 must remain at most 15%, and never-lower must hold. Further retrieval work is useful only if it improves the end-to-end task while the safety floors hold. The latest run fails the P1 and usefulness gates.

## Segments and counter-metrics

Report severity, language and contract tier with numerators and denominators. The latest run contains 14 P1, 6 P2, 15 P3, 7 P4 and 8 ABSTAIN cases; 27 EN, 21 FR and two unsupported-language cases; 30 Enterprise and 20 Standard cases.

| Segment | Cases both recorded graders accept | Denominator |
|---|---|---|
| P1 | 2 | 14 |
| P2 | 4 | 6 |
| P3 | 4 | 15 |
| P4 | 5 | 7 |
| ABSTAIN | 7 | 8 |
| EN | 13 | 27 |
| FR | 7 | 21 |
| Enterprise | 13 | 30 |
| Standard | 9 | 20 |

Critical metrics from the latest preserved outputs, with actual denominators:

| Segment | P1 detected / expected P1 | False P1 / labelled P2-P4 |
|---|---|---|
| EN | 6/8 | 2/16 |
| FR | 3/6 | 1/12 |
| Enterprise | 6/8 | 2/17 |
| Standard | 3/6 | 1/11 |

These are acceptance counts, not segment-specific P1 recall. The finalisation audit separately derives critical recall and false-P1 counts by language/tier. Small strata cannot establish equal error rates or fairness. Unsupported languages require a person; preserving the declared priority does not establish low impact.

Counter-metrics are human-triage share (9/50 latest, 31/50 initially), engineer corrections, false-P1 rate and eventual real SLA breaches. Keep difficult cases in the routine-acceptance denominator so that abstaining cannot artificially improve the primary score. Do not maximise P1 recall by labelling every ticket P1.

Proposed live harm threshold: one confirmed P1 proposed below P1, or one unauthorised automatic lowering, triggers suggestions-only and incident review. Owner: Head of Support by day, on-call engineer by night. This is a future operating policy; no live rollout has occurred.

## Business metrics and assumptions

| Business metric | Historical hypothesis | Current interpretation |
|---|---|---|
| Routine handling time | 33 minutes per ticket, 9.1 minutes saved per accepted triage; investment flip near 17% | 40.9% x 9.1 / 33 is about 11.3% potential reduction under those assumptions, not observed saving |
| SLA penalties | 240 breaches/year x EUR2,000; 30% potentially avoided, yielding EUR81k year-one upside with ramp | Neither the baseline nor avoided penalties has been observed; no monetary benefit can be inferred from zero automatic lowerings |
| Staffing | Scenario has 25 engineers; freed capacity absorbs growth rather than reducing jobs | No actual headcount or avoided-hire effect measured |

Source: [historical sizing and investment memo](02_investment_memo.md), including the referenced spreadsheet. The modeled EUR133k expected annual value is conditional; current results do not authorise the integration budget. The [launch memo](08_launch_memo.md) supersedes the earlier conditional-go recommendation.

## Evaluation quality and coverage

The repository holds two recorded evaluations of 50 cases, not one independent 100-case evaluation of a single model. The second batch's inputs had been visible during development. Main grading began with LLM-prefilled sheets; reported agreement may reflect anchoring as well as task clarity. Luna confirmed her actual review of all grading sheets bearing her name on 23 November 2026; [confirmation record](evals/finalisation_2026_11_23/luna_grading_confirmation.json).

The archived golden 30 reports human-human agreement 29/30 and judge agreement 29/29 on the subset where both humans agreed. Conditioning on that subset and the predominance of rejected cases make the 100% figure insufficient as a general judge-accuracy claim. Keep the original sheets and disagreement notes.

There are 100 reviewed references plus 100 additional E101-E200 input candidates. The target of 200 reviewed cases is still pending human annotation and semantic overlap screening. Do not count changed names or duplicate incidents as additional independent cases. [Next review and evaluation steps](evals/VALIDATION_EQUIPE.md).
