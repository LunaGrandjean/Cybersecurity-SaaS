# 06_07 — Experiments & operations · Team 8 · SLA-aware triage copilot (P7)

> Sessions 6 + 7 deliverable, 23 November 2026. Every number traces to `02_sizing_CyberSaas.xlsx` (cell given), `05_metrics.md` or `evals/report_v0.md`. A value that is our own decision is marked *(decision)*. Every owner is a role from our proposal. Every threshold has a clock.
>
> **Current gate, updated 23 November:** latest v0.5 acceptance is 9/22 = 40.9% and P1 recall 9/14 = 64.3%; live assisted launch is not approved. [The final memo](08_launch_memo.md) governs release. This is a proposed future experiment/operations plan. No live experiment, production monitoring service or operational trace pipeline is implemented.

## §1 Prove the effect — hypothesis, unit, design

**Hypotheses**, one per business metric of `05_metrics.md` §4:

1. **Handling time.** If engineers use the copilot in assisted mode on P3/P4 tickets, **handling time per routine ticket moves from 33 min to ≤ 27.4 min (−17 %, the memo flip point)** by the end of the first pilot quarter, without P1 recall leaving 100 % and without the false-P1 rate exceeding 15 %. (Baseline: `03_product_brief.md` §2, derived from 25 engineers × ~1,600 h ÷ 72,000 tickets; flip: `02_investment_memo.md` §3.)
2. **SLA penalties.** If the copilot proposes and raises priorities on all new tickets, **SLA breaches move from 240 a year (20 a month) to ≤ 168 a year (−30 %, Inputs D68 hypothesis)** two quarters after the start, without the human-triage share rising above the initial 31/50 baseline (latest 9/50) (`05_metrics.md` §3).
3. **Headcount (non-effect).** **Engineer headcount stays at 25 ± 0** in year 1 (Inputs D7). Time saved absorbs growth instead of replacing people (memo §3).

**Proposed unit of randomisation: the day, not the ticket.** Raising one ticket's priority moves every other ticket down the queue, so a ticket-level A/B leaks the treatment into the control group through the shared queue (interference). Engineers also work a rotation, so a team-level split would mix the same people across arms. Randomly assign whole days to on/off conditions, blocked by weekday, after measuring baseline variability. Existing backlog, long SLAs and engineer learning can carry effects across days, so this does not isolate queues perfectly. Pre-register carryover handling and assess whether genuinely separate queues are needed before the experiment.

**Design, in two steps:**
1. **Shadow mode, 2 weeks *(decision)*.** The copilot runs on every live ticket, but its proposals are logged and not shown. This measures live P1 recall and the false-P1 rate on real tickets before anyone sees a suggestion. Shadow mode limits decision influence but still needs approved access, retention and privacy controls; it is not risk-free.
2. **A/B on randomly assigned days, provisionally one pilot quarter (13 weeks).** It reads hypothesis 1 (handling time) and the guardrails.

**What it cannot see:**
- **The learning effect.** Engineers who see suggestions on "on" days may triage better on "off" days, which shrinks the measured effect.
- **Weekday mix.** Weekday and incident-spike mix differ between days (volume range 5,000–7,500 a month, Inputs C6:E6); weekday blocking helps balance this; residual mix and carryover must be analysed.
- **SLA breaches cannot be proven by this A/B within a year.** Breaches are rare: 240 / 72,000 = 0.33 % of tickets. Detecting −30 % needs ≈ 44,000 tickets per group, about 64 weeks of total volume (two-proportion test, risks of 1 in 20 and 1 in 5). We therefore read hypothesis 2 as **before/after with a control**: last year's monthly breaches against the pilot months, adjusted by the root-cause audit of the memo (§3). We say this openly; we do not stretch the A/B.

## §2 Decide before — duration and decision rule

**Smallest improvement that still justifies the agent:** **−17 % handling time on routine tickets.** Below it, the memo's decision flips to no-go: the time saved no longer covers the €133,333 / year of fixed costs (Decision D14).

**Slowest guardrail to read, and how long we run:** P1 recall. Each P1 must be confirmed by an engineer at closure. At ≈ 69 P1 tickets a week (6,000 / month × 5 %, Inputs D6 × D16), 13 weeks give ≈ 900 P1s, half of them on "on" days. Those are projected counts, not a power calculation or proof of safety. Confirm the duration using measured variability, day-level allocation and carryover; a quarter is a planning assumption, not a statistically justified duration yet.

| Input | Value | Source |
|---|---|---|
| Baseline p₀, an outcome that exists with and without the agent | Handling time 33 min per ticket; SLA breaches 0.33 % of tickets (240 / 72,000) | `03_product_brief.md` §2; sizing How-to B48, Inputs D6 |
| Smallest rise worth acting on | −17 % handling time; −30 % breaches | memo §3; Inputs D68 |
| Two risks accepted (false win · missed win) | 1 in 20 · 1 in 5 | preset in the calculator |
| **Units per group** | Handling time: not computed yet, because the variance of handling time is unmeasured (S3 timings are guesses), so we measure it during shadow mode. Breaches: ≈ 44,000 tickets | ticket-level two-proportion approximation; day-level clustering and carryover are not included |
| Volume per week | ≈ 1,385 tickets (72,000 / 52), ≈ 69 P1 | Inputs D6, D16 |
| **Proposed duration** | Proposed 2 weeks shadow + provisional 13 weeks A/B; final duration after baseline measurement | the read date of the slowest guardrail |

**Pre-registered segments** (from `05_metrics.md` §3): severity (P1–P4, ABSTAIN), language (EN / FR / other), tier (Enterprise / Standard).

**Decision rule, written on 23 November 2026, before the first unit:**
- **Ship** (assisted mode for all teams) if handling time on P3/P4 falls by ≥ 17 % on "on" days, P1 recall = 100 % in every segment, the false-P1 rate is ≤ 15 %, and no priority was lowered.
- **Iterate** (stay in suggestions-only, fix, re-run on fresh cases) if handling time falls by less than 17 %, or the false-P1 rate is above 15 %, with both floors intact.
- **Kill** if handling time does not fall at all, or if the guardrails fail again after one iteration.
- **Stop early only on the harm threshold of `governance.md`:** one confirmed P1 proposed below P1, or one priority lowered without an engineer. We never stop early on a good number, and we read the result once, at the end.

## §3 Watch the four layers — monitoring and drift

| Layer | Metric (from `05_metrics.md`) | Threshold that pages someone | Clock | Owner | Tool — startup | Tool — large company |
|---|---|---|---|---|---|---|
| Infrastructure | Triage API up, latency, error rate | API unreachable for 5 min *(decision: well inside the 1 h P1 SLA)* → automatic fallback to manual triage | Real time | On-call support engineer (rotation) | Container health checks + Grafana Cloud | Cloud Monitoring / Azure Monitor + Datadog |
| Model quality | P1 recall and false-P1 rate on the frozen `eval_set_v1.csv`; judge score on a weekly sample | P1 recall < 100 % or false-P1 > 15 % on any re-run | Weekly and on every release | AI product team (Team 8) | Phoenix (self-hosted) | Langfuse self-hosted |
| Product & guardrails | Priority lowered below declared; P3/P4 accepted unchanged; human-triage share | **Any** lowered priority → page now; human-triage share above the pre-pilot baseline for a week (baseline to measure) | Daily (lowered: real time) | Support lead | SQLite / Postgres table + Metabase | Warehouse + Power BI |
| Business | SLA breaches per month against 20 a month (240 / 12); penalties € | Breaches above last year's same month | Monthly | Head of Support | Weekly query + sheet | BI dashboard |
| Paging | — | — | — | Head of Support by day,on-call support engineer (rotation) by night | Slack / Teams webhook | PagerDuty / Opsgenie |

The table names planned options, not installed or approved services. Any selected service must respect the agreed data perimeter; a third-party cloud dashboard is not automatically compatible with that requirement. Current implementation uses only local SQLite and audit export.

**Where the Python standard-library HTTP service runs:** today, on our laptop (loopback only, synthetic data). For a pilot: a container in **our own cloud tenant or on-premises**, next to the ticketing tool. Inference stays local: the engine is a rule set plus a classical classifier, with no third-party model API. Secrets live in `.env` or the tenant's secret manager, never in Git.

**Release path and gates:**
- **dev**, on every commit: the current regression suite plus the switch drill (`python -m prototype.switch_drill`).
- **staging**, on every change of rules, classifier, sources or routing table: a fresh reviewed batch plus the judge, with exposed cases used only for regression, both floors checked, 2 weeks of shadow mode, rollback re-tested.
- **production, by steps:** suggestions-only for all teams → assisted on alternating days (the A/B) → assisted every day. Each step is guarded by the thresholds above; any page sends it back one step.

**First drift expected: concept drift from new attack types.** A new CVE or campaign produces tickets that look like nothing in the training families, and the volume spikes towards the high case (7,500 tickets a month, Inputs E6). **Signal:** abstentions and the human-triage share rise, the false-P1 rate moves, and engineers change more proposals. Knowledge drift (outdated KB articles) comes second; its signal is a falling source hit@3. **What we re-run:** fresh reviewed cases for release-quality claims, plus exposed cases for regression on every release, every classifier retrain and every rule change, plus a fresh labelled batch after every major incident wave.

## §4 Contain the incident — trace, classes, rollback

**Trace: one OpenTelemetry trace per ticket, one span per step of `04_architecture.md`:**
- `request`: ticket id, timestamp, account, tier, language, declared priority, engine version, latency.
- `redact`: number of redactions; no raw text stored.
- `account_sla`: SLA minutes, deadline, contract verified yes/no.
- `classify`: proposed severity, classifier score, method (rule / model).
- `rules`: raised yes/no, lowering blocked yes/no.
- `retrieve`: top-3 source ids with scores, or a no-hit flag.
- `route`: team, or Human triage with its reason.
- `policy`: requires_human, review reasons, mode (suggestions / assisted).
- `human_decision`: accepted / changed / taken over, engineer, reason, and the judge score or human grade when sampled.

A future operational trace would be stored in an approved self-hosted service inside the agreed perimeter, linked to the audit. The prototype currently stores SQLite audit events; it does not emit OpenTelemetry spans or deploy Phoenix/Langfuse.

**Our one-page dashboard, five panels:**
1. **Stat tiles with thresholds:** lowered priorities today, P1 recall this week, false-P1 rate, API status. *Am I paged?*
2. **Line over time:** P3/P4 acceptance and handling time per day, "on" vs "off" days. *Is the effect there, and is it stable?*
3. **Histogram, this week vs last:** classifier score and human-triage share. *Is it drifting?*
4. **Bars by segment:** P1 recall and false-P1 rate by language and tier. *Is it fair, or is there a Simpson's paradox?*
5. **Worst-cases table:** missed or late P1s, lowered priorities, the biggest engineer changes. *What do we fix on Monday?*

Proposed dashboard using an approved internal BI/monitoring tool. No such dashboard is deployed in this prototype.

| Class | Example on our agent | Action |
|---|---|---|
| Caught | False P1 on a planned exercise (E049 type); the engineer corrects it before acceptance | Count it; weekly review; spec line if it repeats |
| Sent wrong | The team is left to "Human triage" while the owner is clear (E008 type); the ticket waits for a manual hand-off and loses SLA minutes | Weekly review of routing misses; fix the routing table (EVAL-05); re-run the eval-set |
| Harmful (above the harm threshold) | A real P1, such as an account-recovery takeover (E003 type), proposed P4 and accepted, or any priority lowered without an engineer | **Rollback now** to suggestions-only; incident report within the day; DPO informed if customer data is involved |
| Outage | Triage API down, or a classifier load failure | Automatic fallback: the console shows manual triage only, and declared priorities and SLA clocks keep running unchanged |

**Rollback plan**

| Field | Ours |
|---|---|
| 1 · Trigger | The harm threshold of `governance.md` (one confirmed P1 proposed below P1, or one lowered priority), **or** an API outage of 5 min, **or** a P1-recall page from the weekly re-run |
| 2 · Who decides (day / night) | Head of Support by day; on-call support engineer (rotation) by night. Either one is enough; nobody needs a second approval to switch off |
| 3 · The action | Step 1: **suggestions-only** (`POST /api/switch`, from the console header). Step 2 if needed: engine off, manual triage only. Step 3: redeploy the previous engine version from the release tag |
| 4 · Time to execute | The switch itself: 0.003 s measured. Target from page to switched: under 15 min |
| 5 · What people see | Engineers see a "suggestions only" banner and no automatic raises; acceptance needs a recorded review. Priorities already raised are kept, nothing is downgraded. Customers see nothing, because the agent never contacts them |
| 6 · Last tested | **22 November 2026, 01:20 (UTC+01:00), on the local prototype, by Malek Saoudi:** `evals/switch_drills/drill_2026-11-22_012010.json`, 7/7 checks passed. Next test: before the pilot starts, then monthly |

## §5 Own the system — the five owners

| Decision | Owner (role) | Written where |
|---|---|---|
| Run an experiment on real users | **Head of Support** signs; the **DPO** reads the protocol before the first unit | This file §1–§2 · `governance.md` S6–7 |
| Read the weekly numbers and act | **Support lead** (product and guardrails); **AI product team (Team 8)** (model quality) | §3 |
| Press the switch (day / night) | **Head of Support** by day · **on-call support engineer (rotation)** by night | §4 · `governance.md` S4 and S6–7 · `04_architecture.md` §6 |
| Approve a release (rules, classifier, sources, routing) | **AI product team (Team 8)**, after the staging gates; **Head of Support** co-signs any change of mode | `evals/README.md` · §3 release path |
| Keep the trace; answer a customer or a regulator | **Head of Support** answers; the **DPO** handles any personal-data request. The company answers for what the system proposes (Moffatt v. Air Canada, 2024) | `governance.md` S6–7 |
