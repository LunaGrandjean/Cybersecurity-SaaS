# spec.md — executable spec · SLA-aware triage copilot · skeleton v0

> Skeleton written in Session 3 from `03_product_brief.md` v2, to be completed with Assignment 4. This is what the coding assistant reads to build the working prototype.

## problem
Our 25 L2 support engineers spend about 12 of the 33 minutes a ticket takes on triage, and we breach ~240 SLAs a year, partly because critical tickets written in a calm tone get a low priority. The copilot proposes severity, SLA clock, team and the closest resolved tickets. It may raise a severity on its own; it never lowers one, and nothing reaches the client without an engineer.

## user_workflow
```
- lookup    : ticket.account_id                   -> tier, sla_minutes, sla_deadline         (L4, rules)
- redact    : ticket.text + ticket.logs           -> redacted_text                           (L4, rules — before any model call)
- severity  : redacted_text + declared_priority   -> proposed_severity, confidence, reason   (L4 to raise · person to lower)
- retrieve  : redacted_text + account_id          -> top-3 resolved tickets (same customer) + KB   (L1 suggests)
- route     : proposed_severity + category        -> team                                    (L3 on P3/P4 · L2 on P1/P2)
- diagnose  : engineer                            -> fix                                     (person only)
- update    : engineer                            -> client message                          (person only)
```

## io_contracts
```
ticket : {id, account_id, text, logs, declared_priority, language, created_at}
triage : {proposed_severity: P1|P2|P3|P4, confidence, reason,
          raised: bool, sla_deadline, team,
          similar: [{ticket_id, title, score}], redaction: {count, types}}
```

## edge_cases
- ticket with too little information to classify (confidence below 0.70) → no guess: keep the declared priority or higher, flag "needs human triage"; counted separately in the eval report
- no similar ticket above the score threshold → show "no past case found", no suggestion
- language other than EN/FR → keep declared priority or higher, flag "needs human triage"
- personal data or secrets in text/logs → redacted before anything else; redaction count shown
- P1 keyword present (breach, ransomware, exfiltration, all users locked out…) → P1, whatever the classifier says
- customer asks for a priority lower than the agent's → keep the higher one, show both
- same symptom reported by several clients within an hour → COULD: show a banner to the engineer (brief §3); no automatic merge in v0

## fallbacks
- confidence = the classifier's probability for the proposed severity; bands shown to the engineer: High ≥ 0.80 · Medium 0.70–0.80 · Low < 0.70
- confidence below 0.70 → keep max(declared, proposed) severity, flag "needs human triage"
- engineer lowers a severity → reason required, logged
- agent unavailable → tickets flow as today with the declared priority

## done_criteria
- ≥ 62 % of P3/P4 eval cases: severity, team and ≥ 1 relevant resolved ticket accepted unchanged by two graders
- 0 P1 cases proposed below P1 (P1 recall = 100 % on the eval-set)
- false-P1 rate reported (target ≤ 15 %)
- 0 unredacted IPs, e-mails, tokens or hostnames in any model input (redaction tests)

## out_of_scope
Customer-facing chatbot · auto-remediation · the agent lowering a severity · fine-tuning on client tickets · raw logs to an external API · languages other than EN/FR · auto-closing tickets.

## eval_set
`evals/eval_set_v0.csv` — 20 cases now, 50 with Assignment 4, 200 by Session 5. Never tune while looking at it.
