# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | | |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | | |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | | |
| 4 | **Never:** what must it never do? (our first guardrail) | | |
| 5 | **Explainability:** explainable to whom — the customer, the support agent, the auditor? | | |
| 6 | **The people it cannot serve:** what happens to them? | | |

## Session 2 — the cost of error
- Which cost-of-error line is a **legal or reputational** risk, not just money? …
- Who in the company **owns** that risk? …

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

## Session 4 — human-in-the-loop points and the override switch (to come)
## Session 5 — counter-metrics and the segments we report (to come)
## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
## Session 7 — accountable owner, rollback authority, incident path (to come)
