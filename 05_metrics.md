# 05 · Metrics — Team 8 · SLA-aware triage copilot (P7)

> Session 5 deliverable, 22 November 2026. Every number traces to `02_sizing_CyberSaas.xlsx` (cell given), `evals/report_v0.md` (run `evals/runs/v0`, 50 human-labelled cases, two graders), or `02_investment_memo.md` / `03_product_brief.md` §7, whose numbers are derived from the sizing sheet. No other numbers appear here.

## 1 · Place the number — the stack for our agent

| Level | Question | Our metric | Value today | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | Does it move the P&L? | SLA penalties avoided (€ / year) | Not yet. Base hypothesis €81,000 in year 1 (Inputs D68) | Online A/B, then monitoring of breaches and penalties | Head of Support | Quarterly |
| 4 Product | Do engineers adopt it and get the job done? | Share of P3/P4 triages that engineers accept unchanged in the console | Not yet (no live users). Offline proxy: level 2 | Console audit log (accept vs change) | Support lead | Weekly |
| 3 Guardrails & responsible AI | Does it stay inside the lines, for everyone? | Priority lowered below the declared priority; P1 recall by language and tier | Lowered: **0 / 50**. P1 recall: EN 8/10, FR 3/4, Enterprise 9/10, Standard 2/4 | Offline eval-set, then daily monitoring | Head of Support | Daily |
| 2 AI system | Does the workflow complete the task? | **P3/P4 triages both graders accept unchanged** | **2 / 17 = 11.8 %** (criterion ≥ 62 %) | Eval-set + two graders | AI product team (Team 8) | Every release (hours) |
| 1 Model | Is the component right? | Severity classifier: P1 recall; severity accuracy | **11 / 14 = 78.6 %**; 33 / 50 = 66 % | Offline eval-set | AI product team (Team 8) | Every commit (seconds) |

Supporting level-1 numbers from the same run: team accuracy 17/50 = 34 %, effective-priority accuracy 29/50 = 58 %, expected source in top 3 14/34 = 41 %, handover agreement 46/50 = 92 %, false-P1 rate 7/28 = 25 %.

## 2 · Decide when to stop — the stop criterion

*"We stop improving **source hit@3** (41 % today) once **P3/P4 acceptance by two graders** stops responding to it above **62 %**. At 62 % the memo's decision flips from conditional go to go, and above it the decision does not change. The next point would cost a re-evaluation of €5,000 per model change (Inputs D56), plus a newly labelled eval-set each time, because the old one is exposed."*

- **Component metric and value:** source hit@3, 41 % today (`report_v0.md` §1). Retrieval feeds criterion 5 of the guideline: at least one relevant source on routine tickets.
- **The level-above metric that stops responding:** P3/P4 acceptance (level 2). 62 % is the action threshold. It comes from the memo flip point of 17 % handling time saved: an accepted triage saves about 9.1 of 33 minutes, and 5.6 ÷ 9.1 ≈ 62 % (`03_product_brief.md` §7, from `02_sizing`). Above 62 % the decision stays at go, so further retrieval work no longer changes what we do.
- **Cost of the next point:** €5,000 per re-evaluation (Inputs D56) and €20,000 a year of eval-set upkeep and graders (Inputs D51). Each tuning round exposes the eval-set it is tuned on, so it needs fresh labelled cases (see §5).
- **Floor, not a stop (any miss blocks the release):**
  - **P1 recall = 100 %**, in every segment. Today it is 78.6 %; the three misses E003, E012 and E015 are an account takeover, retained admin access and a cross-tenant data leak.
  - **0 priorities lowered below the declared priority** without an engineer. Today 0 / 50 ✅.

  We never trade either floor for acceptance.

## 3 · Choose what to protect — the hierarchy, by segment

| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | P3/P4 triages accepted unchanged | P3/P4 triages accepted without any change ÷ P3/P4 triages proposed. Abstentions stay in the denominator | 4 (offline proxy at level 2: 11.8 %) | Weekly | Console audit log · Support lead |
| Guardrail | P1 recall | Tickets proposed P1 ÷ tickets an engineer confirms as P1 at closure | 3 | Days (P1 confirmed at closure) | Eval-set + ticketing tool · Head of Support |
| Guardrail | Never lowered | Tickets whose effective priority < declared priority without an engineer reason ÷ all triaged tickets | 3 | Real time | Audit log (`POST /api/action`) · Head of Support |
| Guardrail | False-P1 rate | Proposed P1 not confirmed as P1 ÷ tickets that are not P1 (offline target ≤ 15 %; today 25 %) | 3 | Days | Eval-set + ticketing tool · Support lead |
| Counter-metric | SLA breach rate | SLA breaches ÷ tickets, compared with the 240 breaches a year baseline (sizing How-to B48) | 5 | Months (penalties are invoiced later) | Ticketing tool, contracts · Head of Support |
| Counter-metric | Human-triage share | Outputs routed to "Human triage" ÷ all outputs (today 31/50) | 4 | Weekly | Console audit log · Support lead |

- **Segments reported** (from the S3 audit in `governance.md`): severity (P1 / P2 / P3 / P4 / ABSTAIN), language (EN / FR / other), tier (Enterprise / Standard). Never one global number.
- **Fairness metric:** **equal error rates across segments**, read on P1 recall and the false-P1 rate. Today they are not equal:
  - P1 recall is Standard 2/4 against Enterprise 9/10, and FR 3/4 against EN 8/10.
  - The false-P1 rate is EN 6/20 against FR 1/8.

  The small Standard and FR samples are why `eval_set_v1.csv` oversamples them.
- **Harm threshold that stops the rollout (copied into `governance.md`):** any confirmed P1 that the agent proposed below P1, in any segment, or any priority lowered below the declared one without an engineer reason, puts the agent back in suggestions-only mode the same day. Owner: **Head of Support**, who holds the ⏻ switch.
- **How it could be gamed, and the repair:**
  - The agent could push the primary up by sending every hard ticket to "Human triage", which removes the risky ones from what gets accepted. Repair: the human-triage share is a counter-metric, and abstentions stay in the primary's denominator.
  - It could push P1 recall up by proposing P1 for everything. Repair: the false-P1 guardrail.

## 4 · Derive the business metrics — three, with expected effects (the oral)

| Business metric | Baseline (from `02_sizing`) | Expected effect (from `report_v0.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| **Engineer handling time on routine tickets** | 6,000 tickets / month (Inputs D6), 75 % P3/P4 (D14), €31.25 per ticket (D9). Gross value of the time saved: €234,520 / year in the base case (Upside D39) | **v0: ≈ 3 % of handling time saved** (11.8 % acceptance × 9.1 min ÷ 33 min), against the 17 % flip, so **no-go on v0**. The base case needs 20 % (Inputs D22), which needs acceptance ≥ 62 % | Weeks | End of the first pilot quarter | Acceptance in the console turns into real minutes saved per ticket (memo §3). It is still unverified: S3 timings are guesses |
| **SLA penalties** | 240 breaches / year × €2,000 per breach (sizing How-to B48). Base hypothesis: 30 % avoided × year-1 ramp = €81,000 (Inputs D68) | **v0: ≈ €0**, because the effective priority is never raised: 0 automatic raises in 50 cases (`report_v0.md` §2, EVAL-04), and 3 P1s are missed. The €81,000 needs EVAL-01 and EVAL-04 and P1 recall = 100 % | Months | Two quarters after pilot start | 30 % of breaches come from misprioritisation rather than capacity; to be checked by the root-cause audit (memo §3) |
| **Engineer headcount (non-effect)** | 25 engineers (Inputs D7) | **Unchanged: 25 ± 0 in year 1.** Time saved absorbs ticket growth, not jobs (memo §3). Stop band: any proposal to cut headcount on the basis of the agent before the time saving is measured | Year | End of year 1 | Time saved is only cash if it avoids planned hires (memo §3) |

The tree from component to business, with the effect each arrow claims:

```
P1 recall 78.6 %  + raise rule (0 raises)  --> effective priority right 58 %  --> SLA breaches avoided (30 % hypothesis) --> €81k/yr penalties (Inputs D68)
severity 66 % + team 34 % + source 41 %    --> P3/P4 accepted 11.8 % (need 62 %) --> handling time saved ≈ 3 % (need 17 %) --> €234,520/yr gross (Upside D39)
false-P1 25 % (target ≤ 15 %)               --> false escalations, alert fatigue  --> error cost €25,920/yr (Upside D40), rises with false P1s
```

## 5 · Make the judge trustworthy — the evaluation plan

- **Eval-set v1:** `evals/eval_set_v1.csv`, 100 cases (28 P1, 17 P2, 25 P3, 14 P4, 16 ABSTAIN; 61 EN, 35 FR, 4 unsupported languages). It combines the 50 cases of v0, now exposed, with 50 new synthetic cases that are tagged as synthetic and labelled by a person before any run. It is stratified by severity, language and tier, with P1, FR and Standard oversampled (§3). The **golden set** is 30 of the v0 cases and never changes; see `evals/README.md`.
- **Grading guideline:** `evals/README.md`, five binary criteria with boundary examples. Two graders on the same 30 rows, independently from blank sheets: **agreement 29/30 = 96.7 %**. The one disagreement, E030 (is an irrelevant source a source?), led to a guideline fix on 22 November 2026.
- **Judge:** an LLM judge, with its prompt in `evals/judge_prompt.txt`. We ran two independent runs on the 50 v0 outputs; they agree on 49/50. **Human–judge agreement on the golden 30: 29/29 = 100 %** on the cases where both humans agree, for both runs. The triage engine is rule-based with a classical classifier and no LLM, so the judge and the system share no model family. Known bias: one run misread a P1-vs-P3 effective priority as a match (E032). The prompt now asks for one sentence of evidence per criterion.
- **Cadence:** eval-set + judge on every change to the engine; human sample of the console's weekly triages; full two-grader re-run on every release.
