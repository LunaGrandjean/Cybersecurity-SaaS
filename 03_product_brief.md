# 03 — Product brief · SLA-aware triage copilot · v2

**Team:** Luna, Malek, Jane · **Starting point:** P7 · Cybersecurity SaaS · **Version:** v2 

> **Historical S3 design brief. Current implementation and results, updated 23 November 2026:** see [product_brief.md](product_brief.md), [04_architecture.md](04_architecture.md) and [08_launch_memo.md](08_launch_memo.md). The evaluated engine is v0.5; 100 references are reviewed and 100 additional input candidates await review. Latest acceptance is 9/22 and P1 recall 9/14, so no live assisted launch is approved. Timings, financial gains and role-play interview answers below remain hypotheses. The original S3 feature prioritisation is retained as design history.

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem in one sentence:** engineers need to connect ticket severity, the account SLA and reusable knowledge reliably. The scenario supplies 25 engineers; the 12/33-minute triage split and 240 annual breaches at about EUR2,000 each are sizing hypotheses, not measured customer facts.
- **User (persona):** L2 support engineer — goal: put each of ~240 tickets a month in the right queue at the right severity before the SLA clock runs out — pain: has to read raw logs and search old tickets by hand before even knowing how urgent a ticket is.
- **Do-nothing baseline:** the team keeps triaging by hand and improves by about 5 % a year (≈ €112k, `02_sizing.xlsx`). The competing project is rule-based SLA routing in the ticketing tool (≈ €100k).

## 2. The process — as-is and to-be
Minutes: 33 min per ticket on average = 25 engineers × ~1,600 h ÷ 72,000 tickets a year. Step split and error rates are **guesses**, to be measured by watching two engineers triage 10 tickets each. *(v2)* The simulated interviews put deciding urgency at 4–5 min, consistent with steps 1–2 (5 min); step 3 (6 min) is still unverified and is the number the flip depends on.

| # | Step | Who today | Minutes | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level | Minutes after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Identify the account, contract tier and SLA clock | engineer | 2 | 3 % (guess) | SLA clock wrong → breach risk on P1/P2 | automate — passes all eight (a lookup) | L4 | 0.2 | tier lookup accuracy |
| 2 | **Assess severity P1–P4** | engineer | 3 | 6 % (guess) | missed P1 → €2,000 penalty + churn risk; false P1 → ~€30 of wasted time | augment — fails test 6 (errors are not cheap) and 7 (attack types change) | **L4 to raise · person to lower** | 0.5 | **P1 recall** (and false-P1 rate) |
| 3 | **Search logs and similar resolved tickets** | engineer | 6 | 15 % known fix not found (guess) | +9 min, wrong fix tried | augment — fails test 5 (the engineer must judge relevance) | L1 suggests | 2 | hit@3 (a relevant resolved ticket in the top 3) |
| 4 | Route to the right team | engineer | 1 | 8 % (guess) | ~30 min reassignment delay | automate on P3/P4 · augment on P1/P2 | L3 on P3/P4 (lead samples 5 %) · L2 on P1/P2 | 0.2 | reassignment rate |
| 5 | Diagnose and fix | engineer | 17 | — | — | keep human — fails 4 (long reasoning), 6, 8 | person only | 17 | time to resolution (watched, not targeted) |
| 6 | Update the customer and log | engineer | 4 | 2 % (guess) | wrong statement to an enterprise client | keep human in the MVP (draft is a COULD) | person only | 4 | SLA first response met |

**Total:** 33 min → ≈ 24 min when the agent's triage is accepted (−9 min, ≈ 28 % of handling time).
**Where the pain sits (the two steps):** step 2 (where the expensive errors are) and step 3 (where most triage minutes go).
**The way back to a person (designed first):** every ticket stays in the engineers' queue; "Take over" on every agent decision; below 0.70 confidence the ticket is flagged "needs human triage" and keeps the customer-declared priority or higher.
**Where the governance line sits:** the agent may raise a severity on its own but never lower one; nothing reaches the customer without an engineer; raw logs never leave our perimeter (redaction before any model call).

*Trust levels — L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold.*

## 3. Features — RICE and MoSCoW
Reach = 6,000 tickets a month (`02_sizing.xlsx`, Inputs D6); auto-remediation reaches P1/P2 only (~600).

| Feature | Reach / month | Impact (0.25–3) | Confidence | Effort (person-weeks) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| SLA clock and contract-tier lookup | 6,000 | 2 | 100 % | 0.5 | 24,000 | MUST |
| Severity proposal with confidence + "never lower" rule | 6,000 | 3 | 80 % | 2 | 7,200 | MUST |
| Log redaction before any model call | 6,000 | 1 | 100 % | 1 | 6,000 | MUST |
| Team routing suggestion | 6,000 | 1 | 80 % | 1 | 4,800 | SHOULD |
| Top-3 similar resolved tickets | 6,000 | 2 | 50 % | 2 | 3,000 | MUST |
| Customer update draft (L2) | 6,000 | 1 | 50 % | 3 | 1,000 | COULD |
| Customer-facing chatbot | 6,000 | 1 | 50 % | 6 | 500 | WON'T |
| Auto-remediation (lock account, block IP) | 600 | 3 | 50 % | 6 | 150 | WON'T |

- **MUST (4):** SLA lookup · severity proposal with the "never lower" rule · log redaction · top-3 similar resolved tickets
- **SHOULD:** team routing suggestion · override capture (engineer's correction + reason, feeds the eval-set) · *(v2)* evidence line under every raise · change the team without rejecting the rest of the triage
- **COULD:** customer update draft · *(v2)* banner when several clients report the same symptom · mandatory impact question ("how many users are affected?") before a P1 or P2 can be submitted, so vague tickets carry enough information to triage
- **WON'T this time (dated 8 November 2026) — out-of-scope list:** customer-facing chatbot · auto-remediation · the agent lowering a severity · fine-tuning on client tickets · raw logs sent to an external API · languages other than English and French · auto-closing tickets · *(v2)* re-triaging tickets automatically when threat intel changes · raising a priority because of the customer's tone or capital letters
- **The feature that tests our flip assumption, and why it is a MUST:** top-3 similar resolved tickets. The memo flips at 17 % of handling time saved, and step 3 holds half the triage minutes. Its RICE is only 5th because its confidence is the lowest (50 %): that is exactly why we build it first, to learn.
- **The cut that hurt the most:** the customer update draft. On a P1, the first message to the client is what the client remembers, but it is a higher trust level than this MVP and does not test the flip.

## 4. Data  *(details in governance.md)*
No real tickets are used. Current fixtures are internally authored synthetic scenarios, not an imported public dataset. Training contains 300 rows across 40 template families (P1 70 / P2 75 / P3 90 / P4 65), with human review pending. Two 50-case evaluations have recorded reviewed references and grades; a further 100 input candidates are not yet labelled or evaluated. The target of 200 reviewed cases remains pending. Customer isolation and exact-text/family checks are implemented, while semantic independence still needs review. Source reuse approvals are simulated; live data rights and retention require the designated operational reviewers.


## 5. Model — one rung per part
| Part | Rung | Why the rung below fails |
|---|---|---|
| SLA clock and tier lookup | 1 · rules (contract database) | — nothing below rules |
| Log redaction (IPs, hostnames, tokens, e-mails) | 1 · rules (regex + allow-list), tested | — a redaction rule must be auditable |
| Severity proposal | 4 · hybrid: rung 2 (TF-IDF + class-weighted logistic regression, gives a confidence) + rung 1 overlay (P1 keywords force P1; "never lower" rule) | rules alone miss disguised P1s written calmly; we climb to rung 3 only if P1 recall fails on the eval-set |
| Similar resolved tickets | 2 · TF-IDF cosine retrieval over resolved tickets of the same customer + generic KB | keyword rules do not match paraphrases ("SSO loop" vs "can't sign in") |
| The MVP | 4 · hybrid | each part on its own rung; no LLM needed in v0, so no log leaves our perimeter |

## 6. Where it lives (integration surface)
A side panel inside the ticketing console the engineers already use — no new tool. Speed: triage shown under 30 s after the ticket arrives (P1 SLA = 1 h). Format: severity badge + confidence + one-line reason + SLA countdown + top-3 similar tickets. **Confidence** = the severity classifier's probability for the proposed priority, an uncalibrated model output, not a measured probability of correctness: High ≥ 80 %, Medium 70–80 %, Low < 70 % (below 70% engineer review is required). In the functional prototype the score is calculated, but it remains uncalibrated; a rule override is a separate decision. In v0.5 a low score requires review but can still accompany an assisted-mode raise in a synthetic demonstration. Fallback: if the agent is down, tickets flow as today with the customer-declared priority. Log: every agent decision with its reason, visible to the support lead and auditable in a penalty dispute.

## 7. Success criterion — one sentence
> On our eval-set (20 cases now, 200 by then), at least **62 % of P3/P4 tickets** get a triage — severity, team and at least one relevant resolved ticket — that two graders would accept without changing anything, **and no P1 is proposed below P1**.

*Why 62 %: an accepted triage saves ~9 of 33 minutes; the memo's flip is 17 % of handling time = 5.6 min; 5.6 ÷ 9.1 ≈ 62 %. Same move as Paylio's 65 % → 45 %.*

## 8. Risks and rollback trigger
- **Top risks:** vague tickets with too little information: the agent sends them back to a person, so less time is saved and the 62 % threshold gets harder to reach (share of vague tickets to measure on the eval-set) · a disguised P1 missed · alert fatigue from too many false P1s · a redaction gap leaking client logs · engineers trusting the agent and skipping their own check · new attack types the model has never seen.
- **Rollback trigger:** any P1 proposed below P1 in production, or a false-P1 rate above 20 % over a week → the agent drops to L1 (suggestions only) within the hour.

---
*v2 only — after the users*

## 9. What the users changed
*Source: three simulated interviews role-played within our team and one usability test (see `03_user_research.md`). These changes are hypotheses until confirmed by real users.*

| Change | Evidence |
|---|---|
| Every raise shows the fact behind it (event, time), not only a pattern name | 2 of 3 personas said they always re-check a tool's priority by hand; one treats a high-confidence score "as a hint, not a truth" |
| The agent never raises a priority because of tone, capital letters or the word "urgent" | Persona 1 ignores tools that raise priority because "Urgent" is typed three times |
| Lowering stays human, but takes one click: preset reasons (e.g. "core security flow working", "scheduled job", "single user affected") plus free text | Persona 1 lowers priorities "every day"; a typed reason on each one would slow a daily action |
| Confidence shown as a word with the basis behind it, not a bare percentage | Persona 2 redoes the analysis whatever the score says |
| New COULD: banner when several clients report the same symptom within an hour | Persona 1's disguised P1 was only spotted when 4 other clients sent the same ticket |
| New WON'T: automatic re-triage when threat intel changes | Persona 2's adware became a ransomware precursor 6 h later; real need, but outside a triage MVP |
| The usability task now includes a ticket where the agent is wrong | Tester finished v0.1 with no hesitation, but every triage was correct, so the test could not show over-trust |

## 10. What they could not decide
- **The 62 % threshold** — it comes from the memo's flip point (`02_sizing.xlsx`), not from users. *Unchanged.*
- **"No P1 below P1"** — a governance choice, set by the cost of a missed P1, even though every persona lowers priorities themselves.
- **The model family** — decided by the eval-set, not by the personas' distrust of AI scores.
- **The legal basis for using client tickets** — decided by the customer contract and the DPO.
- **Whether the 6 minutes of searching (step 3) are real** — no persona was asked; only observing real engineers can settle it.
