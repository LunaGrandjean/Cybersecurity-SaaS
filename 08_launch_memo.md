# 08 Launch decision for the SLA triage copilot

**Team 8 · 23 November 2026 · evaluated engine v0.5.**

## Decision

**Do not launch assisted mode on live customer tickets.** Keep the current release as a local demonstration with synthetic data and suggestions-only as its default. Do not release the production integration budget on the strength of these results.

The latest recorded run detects 9 of 14 expected P1 incidents and has 9 of 22 routine triages accepted unchanged by both recorded graders. Both fall below the agreed gates. Passing engineering tests and never automatically lowering a priority do not compensate for an emergency that the customer originally declared too low.

## Evidence behind the decision

| Gate | Initial run, 50 cases | Latest run, 50 additional cases | Decision threshold |
|---|---|---|---|
| P3/P4 accepted unchanged by both recorded graders | 2/17 = 11.8% | 9/22 = 40.9% | At least 62%: not met |
| Expected P1 incidents proposed P1 | 11/14 = 78.6% | 9/14 = 64.3% | 100% on the finite holdout: not met |
| False P1 among cases labelled P2/P3/P4 | 7/28 = 25.0% | 3/28 = 10.7% | At most 15%: met on latest run |
| Priority automatically lowered below declaration | 0/50 | 0/50 | Zero: met on both runs |
| Relevant candidate source id in top 3 | 14/34 = 41.2% | 22/37 = 59.5% | Diagnostic; source usefulness still needs human judgement |

The frozen cases, outputs and original grades remain in `evals/runs/v0` and `evals/runs/v1_fresh`. The full interpretation is in [the evaluation report](evals/report_v0.md). The two batches use different cases: their percentages describe the two runs, not a controlled estimate of improvement on the same population.

The development author had seen the second batch's inputs before the fixes. That batch contains new incidents but is not a fully blind holdout. The main grading files started from an LLM-judge prefill, creating a possible anchoring effect. Luna confirmed her actual review and approval of the grading files bearing her name on 23 November 2026. These limitations remain attached to the results; neither model agreement nor a named CSV alone establishes independent human judgement.

## Business case

The [investment memo](02_investment_memo.md) models a conditional expected annual value of about EUR133k, based on assumptions about handling time, avoided SLA breaches, adoption and costs. Those assumptions are not realised savings. The prototype has no production users, measured handling-time comparison or observed avoided penalties.

Under the historical timing assumption, 40.9% acceptance multiplied by 9.1 minutes per accepted triage and divided by 33 minutes is approximately **11.3% potential handling-time reduction**. This calculation is an illustrative proxy, not a measurement, and is below the assumed 17% investment flip point. Even a better proxy would not override the missed-P1 gate.

## Permitted scope and human control

The current console may be demonstrated locally with invented tickets. Engineers can inspect sources, verify or change priority/team with a reason, take over and export the audit. It sends no customer message and executes no remediation. Assisted mode remains available for synthetic demonstrations of the workflow; its availability is not an approval for live use.

In the proposed operating model, the Head of Support owns the stop switch by day and the on-call support engineer by night. Switching to suggestions-only prevents raises on new tickets, retains earlier raised priorities and requires review before acceptance. The team recorded a seven-check local switch drill on 22 November; current engineering evidence is in [engineering_checks.md](evals/engineering_checks.md). Real operational appointments and production authorisations are outside this classroom prototype.

## Conditions before reconsidering launch

1. Review the 300 synthetic training labels and their 40 template families, and establish authoritative, customer-scoped reusable sources. Simulated KB sign-off is insufficient for live operations.
2. Complete semantic overlap review and human expected answers for a genuinely unseen evaluation batch. The repository has 100 reviewed cases and 100 additional input candidates; **200 candidates are not 200 reviewed or evaluated cases**. Freeze references and model before prediction, then obtain the required human grading.
3. Meet the P1, routine-acceptance and false-P1 gates on that batch, reporting counts by language, tier and severity. Any later tuning requires another independent batch. A perfect finite test does not guarantee production recall.
4. Replace simulated research with observed user behaviour, measure the actual manual baseline and assisted handling time, and derive an experiment duration using observed variance and the chosen day-level randomisation unit.
5. Obtain the Head of Support and DPO review, real authentication and access controls, appropriate retention, an operational audit/monitoring setup and a tested rollback before a live shadow study. Production tooling described in the [operations plan](06_07_experiments_operations.md) is planned, not deployed.

## Release and submission status

The final brief, architecture, metrics, experiment/operations plan, spec and this decision form the written handoff. Original evidence is preserved; the finalisation audit records verification separately. New input candidates and a human-review guide are prepared for the remaining evaluation work.

Human review of those additional cases, real-user research and operational approval cannot be replaced by generated signatures or simulated results. Commit authorship, the course's team-size/four-author requirement and any required classroom starter exercise must be reconciled with the lecturer. Create the final Git tag only after the team has reviewed the final commit; no external release, push or operational approval is implied by this memo.
