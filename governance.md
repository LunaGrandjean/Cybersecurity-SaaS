# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | **Minimal risk.** An internal tool that proposes a priority to our own support engineers; it is not in the Annex III high-risk list and never talks to a customer. Engineers know every proposal comes from the agent (it is labelled in the console). If it ever wrote to customers, it would become limited risk (art. 50: tell the user it is an AI). | Legal |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | Ticket text, the client's contract and SLA tier, and logs that contain personal data of the client's employees (IPs, e-mails, usernames). Legal basis: the support contract with the B2B client (art. 6(1)(b)); for the logs we act as processor under the client's DPA. Training a model on client tickets is a different purpose and needs an explicit contract clause. | DPO · client contract template |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | The agent only proposes. The engineer who accepts, corrects or lowers a priority is accountable for that ticket; the head of support is accountable for the agent and its rules. A person sees every ticket before any action, and only a person can lower a priority. | Head of support |
| 4 | **Never:** what must it never do? (our first guardrail) | Lower a ticket's priority on its own · contact a customer · send raw logs outside our perimeter (redaction before any model call). | Security team |
| 5 | **Explainability:** explainable to whom — the customer, the support agent, the auditor? | **To the engineer:** a one-line reason, the evidence and the closest resolved tickets for every proposal. **To the auditor or the client in a penalty dispute:** a log of every proposal, acceptance and change of priority, with the reason given. Not to the customer directly: the customer only talks to engineers. | Head of support · DPO |
| 6 | **The people it cannot serve:** what happens to them? | Tickets in languages other than English and French, tickets with too little information, and new attack types with no past case. The agent does not guess: it keeps the customer's priority or higher and flags "needs human triage". These cases are reported separately in the evaluation. | Support team (volume of such tickets) |

## Session 2 — the cost of error
- Which cost-of-error line is a **legal or reputational** risk, not just money? **A missed P1.** The SLA penalty (~€2,000 per breach) is only the visible part: an enterprise security client whose incident was triaged as routine may leave, and that churn is not in our sizing. Second line: a **redaction failure**, where client logs containing personal data reach a third party, is a GDPR breach, not just a cost.
- Who in the company **owns** that risk? The **head of support** owns missed P1s and SLA penalties (and the switch that puts the agent back to suggestions only); the **DPO** owns the redaction and logs risk.

## Session 3 — data and trust level
> Paste this section into governance.md, then delete this file.

### The six-question data audit
| # | Question | Our answer | Source type | To check with |
|---|---|---|---|---|
| 1 | **Provenance** | No real client tickets. Inputs are AI-generated from public material (public status pages, public CVE descriptions, vendor documentation), then labelled by hand by the team. The origin is written in every row of `evals/eval_set_v0.csv`. In production: tickets and telemetry from our ticketing tool and our own platform. | measured (we built it) | — |
| 2 | **Volume & labels** | 20 eval cases now, 50 with Assignment 4, 200 by Session 5. ~300 synthetic tickets to train the classifier, ~5 % P1, a third of them disguised (calm tone). Labels: severity P1–P4, team, hand-over yes/no, set by two team members against our severity guideline (P1 = service down or active compromise; P2 = major degradation; P3 = issue with a workaround; P4 = question or request). Disagreements settled by a third member. | measured | severity guideline reviewed by a security engineer |
| 3 | **Coverage** | English and French; Enterprise and Standard tiers; all four severities with P1 oversampled. Not covered: other languages, non-English logs, tickets with attachments only. | measured (eval-set) | the 400 accounts' language and tier mix |
| 4 | **Rights** | Production legal basis: the customer contract (GDPR art. 6(1)(b)) and our DPA as processor for triage. IPs, e-mails and usernames in logs are personal data. Training on client tickets is a different purpose: it needs an explicit clause, otherwise only the synthetic set is used. Retention: aligned with the ticket retention in the contract; the model provider keeps nothing (redaction before any call, zero-retention terms). | guess | DPO · legal (DPA template) |
| 5 | **Leakage** | Eval and training split **by incident**, not by ticket, so near-duplicates of the same incident never sit on both sides. The similar-ticket index is filtered by customer: a client's resolved tickets are shown to our engineer, never quoted in another client's message. | guess → tested in S4 | — |
| 6 | **Freshness** | The threat landscape changes monthly (fails test 7 of the eight): new CVEs, new attack patterns. The eval-set is refreshed every month with new cases; the classifier is retrained when P1 recall drops on the new cases. | analogy | security team |

- **Purpose limitation (GDPR art. 5):** ticket data is used to triage that ticket (severity, team, similar past fixes). It is not used to train a model unless the client contract allows it. Redacted logs are processed in memory and not stored by the agent beyond the ticket's own retention period.
- **Isolation between customers:** the retrieval index is partitioned by customer ID; generic knowledge-base articles are shared, client tickets are not. A test case in the eval-set checks that customer A's incident never appears in a suggestion for customer B.
- **Known gaps by segment:** languages other than EN/FR; smaller Standard-tier accounts (fewer resolved tickets to retrieve from); brand-new attack types with no past ticket; disguised P1s, which are rare by construction. Results are reported by severity, tier and language, never as one global number.

### Trust level per step (same scale as Session 1)
| Step | Trust level | Why (cost of an error) |
|---|---|---|
| 1. Account, tier and SLA clock | L4 | deterministic lookup; an error is visible immediately |
| 2. Severity — raise | L4 | a false P1 costs ~€30 of engineer time |
| 2. Severity — lower | person only | a missed P1 costs a ~€2,000 penalty and puts the account at risk |
| 3. Logs and similar resolved tickets | L1 suggests | the engineer judges relevance; a bad suggestion costs minutes |
| 4. Routing | L3 on P3/P4 (lead samples 5 %) · L2 on P1/P2 | a misroute on a P1 eats the 1 h SLA |
| 5. Diagnose and fix | person only | long reasoning, physical consequences on the client's systems |
| 6. Customer update | person only (draft is a COULD) | a wrong statement to an enterprise client during an incident |

## Session 4 — human checkpoints and override switch
**Implemented 12 November 2026, local synthetic-data demo; team acceptance sign-off pending.** This section records actual S4 behaviour and supersedes earlier S3 implementation assumptions where they differ.

| Checkpoint | Kind | Who / local behaviour |
|---|---|---|
| Unknown account/language, weak model score, insufficient context | Abstention/review | Engineer keeps manual triage; no classifier-driven auto-raise |
| No reusable source | Abstention | No troubleshooting is invented; engineer checks the case |
| P1/P2 and any priority reduction | Approval | Engineer records verification/reason before acceptance; API enforces this |
| Privileged-access or legal request | Human-only handling | No access change or legal answer is executed |
| Take over | Manual override | Proposal hidden; manual priority/team controls stay available |
| P3/P4 | Assisted recommendation | Human acceptance logged. Production 5% sampling remains a future policy |

- **Override owner in the proposed operating model:** Head of Support. Local operator names are self-declared and do not establish real identity or approval authority.
- **How:** header → Change mode → reason. `POST /api/switch` persists and audits the mode. Default is `suggestions`; assisted mode deliberately permits eligible automatic raises for new tickets only.
- **Scope:** all new tickets. Suggestions mode also requires recorded verification before accepting existing tickets. Previous raised priorities and engineer decisions remain unchanged so disabling cannot downgrade a ticket.
- **Test:** automated API/browser evidence is recorded in `evals/engineering_checks.md`. Team test: **22 November 2026, 01:20 (UTC+01:00), operated by Malek Saoudi** on the local prototype (`python -m prototype.switch_drill --operator "Malek Saoudi"`); 7/7 checks passed. Switching assisted → suggestions took 0.003 s, new tickets were no longer raised, the earlier raised ticket stayed at P1, acceptance was blocked until a human review, both switch actions were audited with the operator, and the mode persisted after restart. Evidence: `evals/switch_drills/drill_2026-11-22_012010.json`. Next test: before every release, and at least monthly.
- **Evaluation data:** `evals/eval_set_v0.csv` contains 50 synthetic inputs with expected answers reviewed by named team members (Jane Galthie, Malek Saoudi, Luna Grandjean); the inputs-only original is `evals/eval_set_v0_inputs.csv`. The frozen run and both grading files are in `evals/runs/v0`. Freeze/run manifests and two independent grading files go under `evals/runs/`. Repository collaborators can see synthetic files; no real customer data is allowed.
- **Training data:** 300 synthetic rows (70/75/90/65), 40 template families. Labels are AI proposals pending human review. Earlier S3 5%-P1 and human-label claims do not describe this current generated set.
- **Knowledge base:** synthetic versioned fixtures; reuse sign-off is simulated, not a real security engineer approval.
- **Persistence:** redacted text, decisions, timestamps and reasons are stored in Git-ignored `prototype/runtime/triage.sqlite3` until the team resets it. This corrects the earlier memory-only assumption. Inference and assets are local; no external model/provider is called.
- **Redaction:** best-effort regex before inference/storage. Passing fixtures do not establish universal coverage or a legal determination. Real-data permissions, retention and classification remain production questions for the designated S1/S3 reviewers.
- **Isolation:** retrieval returns only same-customer sources or generic KB. Regression checks verify another customer's exact source is excluded. Semantic relevance is judged by humans.
- **Evaluation integrity:** the 20 original examples and all dev/test fixtures are exposed demo data. Humans must annotate new inputs before prediction and review semantic near-duplicates. The runner blocks pending labels and altered frozen runs.

### S4 technical update — 15 November 2026
- Corrected missed development emergencies and source matching using only the exposed C01–C20 examples; preserved the initial diagnostic and reference bytes. [Comparison and limits](evals/ai_review/post_fix_2026_11_15/comparison.md). Three routing-ownership conventions still need agreement before freeze.
- An explicitly suspected incident can raise in assisted mode even when the ticket also asks a legal question; the legal answer remains human-only. Privileged-change requests still block automatic raising. Every P1/P2 needs engineer review before acceptance. The default suggestions switch still blocks every automatic raise.
- Automated verification: 29 code/API/protocol/import tests and 16 real-browser checks passed on 15 November; [evidence](evals/engineering_checks.md). Real team operator, date and switch acceptance sign-off remain **pending**; no operator identity is fabricated.
- [Review instructions](evals/VALIDATION_EQUIPE.md): proposed split Jane E001–E017, Malek E018–E034, Luna E035–E050. `prototype.import_review` requires explicit decisions/names/dates, rejects changed original inputs and writes a separate reviewed CSV without inference. These fields record the reviewers' assertions; the script cannot establish that a real review occurred.
- The official 50 inputs remain unpredicted by these technical checks. Two people must independently grade all 50 outputs after the actual label review and freeze; the review split is not a substitute for two graders.

## Session 5 — counter-metrics and the segments we report
*22 November 2026 · details in `05_metrics.md` §3.*
- **Counter-metrics:** SLA breach rate (baseline 240 breaches a year) and the share of outputs routed to "Human triage" (31/50 on run v0).
- **Segments reported, never one global number:** severity (P1–P4, ABSTAIN), language (EN / FR / other), tier (Enterprise / Standard). Fairness metric: equal error rates (P1 recall and false-P1 rate) across language and tier.
- **Harm threshold that stops the rollout:** any confirmed P1 that the agent proposed below P1, in any segment, or any priority lowered below the declared one without an engineer reason. Consequence: the agent goes back to suggestions-only mode the same day. **Owner: Head of Support**, who holds the ⏻ switch.
## Sessions 6 + 7 — experiments, switch and trace
*23 November 2026 · details in `06_07_experiments_operations.md`.*
- **Experiments on real users:** any experiment on real support engineers and live tickets is signed by the **Head of Support** and read by the **DPO** before it starts. The decision rule (ship / iterate / kill) and the harm threshold (Session 5) were written on 23 November 2026, before the first unit (06_07 §2). Pre-registered segments: severity, language, tier.
- **The switch:** the **Head of Support** can move the system to suggestions-only or off by day, the **on-call support engineer (rotation)** by night; either one is enough. Last tested 22 November 2026 by Malek Saoudi on the local prototype (7/7 checks); next test before the pilot starts, then monthly.
- **The trace:** one trace per ticket (spans: request → redact → account_sla → classify → rules → retrieve → route → policy → human_decision), kept for 12 months *(decision: one contract year, so that any SLA penalty dispute can be answered)* in a self-hosted store inside our tenant. The **Head of Support** answers a customer or a regulator from it, with the **DPO** for personal data. The company answers for what the system proposes (Moffatt v. Air Canada, 2024).
