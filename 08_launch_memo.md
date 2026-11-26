# Launch memo — SLA-aware triage copilot (Team 8, P7) — 26 November 2026

> One page. Evaluated engine v0.5. Full evidence: `evals/report_v0.md`; plan: `06_07_experiments_operations.md`.

## 1 · Decision
**No-go** for assisted mode on live tickets. We keep the local demonstration on invented data, in suggestions-only mode by default, and we do not release the integration budget. The next decision is read once a fresh, reviewed batch has been frozen and run once (E101–E200), by the Head of Support and the AI product team (Team 8).

**Budget we ask for:** **€20,000** for the next validation step only, which is the base evaluation line of `02_sizing.xlsx` (Inputs D51). It pays for labelling, freezing and grading a fresh batch with two human graders. The full fixed-cost envelope of **€133,333 a year** (Decision D14: integration €33.3k amortised, supervision €45k, evaluation and re-evaluation €35k, monitoring €20k) is requested only if that batch passes every gate.

## 2 · Evidence
- **Eval** (50 fresh cases E051–E100, two graders, the judge checked on a golden set of 30: human–human agreement 29/30 = 96.7 %, human–judge 29/29 = 100 %): **9/22 = 40.9 %** of P3/P4 triages accepted unchanged by both graders, against the criterion **"≥ 62 % of P3/P4 triages accepted unchanged by two graders, and no P1 proposed below P1"**. **Not met.**
- **Guardrails:** P1 detected **9/14** (100 % required, **not met**). False P1 **3/28 = 10.7 %** (≤ 15 %, met). Priority lowered below the declaration **0/50** on each run (met). Customer messages sent **0**: no such endpoint exists. Checked on every frozen run.
- **What the A/B will prove:** routine handling time from **33 to ≤ 27.4 min** (−17 %, the investment flip point). Units per arm for handling time are not computed yet, because its variance is unmeasured and will be measured in shadow mode. Detecting the −30 % effect on SLA breaches would need ≈ 44,000 tickets per arm. Duration: **2 weeks of shadow + 13 weeks of alternating days**, set by P1 recall, the slowest guardrail.
- **Sizing:** base **€152k** net in year 1 against a hurdle of **€100k** (rule-based SLA routing in the ticketing tool). Expected value **≈ €133k**. Do-nothing trajectory **≈ €112k**. These are modelled values, not realised ones: the 40.9 % acceptance implies only ≈ 11 % of handling time saved, below the 17 % flip.

## 3 · Rollout steps
| Step | Scope | Duration | Gate (metric · threshold · read date) | Signs the next step |
|---|---|---|---|---|
| 0 | Fresh offline batch, then shadow mode on live tickets | Batch: 2 weeks · shadow: 2 weeks | P1 recall 100 %, P3/P4 acceptance ≥ 62 %, false P1 ≤ 15 % on a frozen batch · **not met on 26 Nov** | Head of Support, with the DPO reading |
| 1 | Suggestions-only for all engineers | 2 weeks | 0 lowered priorities · P1 recall 100 % on the weekly sample | Support lead |
| 2 | Assisted mode on alternating days (the A/B) | 13 weeks | Handling time −17 % on "on" days · guardrails green · ship / iterate / kill at the end of the quarter | Head of Support + AI product team |
| 3 | Assisted every day, with "off" days kept as a holdout | 6 months | Monthly: four monitoring layers green, drift review | Head of Support |

## 4 · Rollback & the switch
**Trigger:** one confirmed P1 proposed below P1, one priority lowered without an engineer, a 5-minute API outage, or a P1-recall alert from the weekly re-run. **Who decides:** the Head of Support by day, the on-call support engineer by night, and either one is enough. **Action:** suggestions-only (`POST /api/switch`, from the console header), then engine off and manual triage, then redeploy of the previous tagged version. **Time to execute:** the switch itself takes 0.003 s, with a target of under 15 min from alert to switch. **What people see:** engineers see a "suggestions only" banner and no automatic raises, and priorities already raised are kept. Customers see nothing, because the agent never contacts them. **Last tested: 22 November 2026, on the local prototype, by Malek Saoudi (7/7 checks).**

## 5 · Owners — and who signs
| Decision | Owner | Written where |
|---|---|---|
| Run an experiment on real users | Head of Support signs; the DPO reads | 06_07 §1–§2 · governance.md |
| Read the weekly numbers and act | Support lead (product and guardrails); AI product team (model quality) | 06_07 §3 |
| Press the switch | Head of Support; at night, the on-call support engineer | 06_07 §4 · governance.md |
| Approve a release (rules, classifier, sources, routing) | AI product team, with the eval re-run; the Head of Support co-signs any change of mode | evals/README.md |
| Keep the trace, answer a customer or a regulator | AI product team keeps it; the Head of Support answers, with the DPO for personal data | governance.md |

**This no-go is signed by Team 8: Luna Grandjean, Malek Saoudi and Jane Galthie.**

## 6 · What we do not know yet
- **P1 recall on attack types never seen.** It fell from 78.6 % to 64.3 % on the fresh cases. Next experiment: freeze and run once on E101–E200 (100 references reviewed by Jane and Luna on 23 November; 7 cases flagged as close to earlier ones, to be settled before the freeze).
- **Whether engineers use it the way we designed it.** The S3 interviews were simulated within the team. Next experiment: three real support engineers, with a usability test on the agent-is-wrong case.
- **Real handling time.** The 33 min, the 12 min of triage and the −17 % are assumptions. How we will measure it: time engineers' tickets with and without the copilot during the two weeks of shadow mode.
