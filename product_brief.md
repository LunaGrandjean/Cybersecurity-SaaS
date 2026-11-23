# Final product brief for the SLA triage copilot

**Team 8 · P7 Cybersecurity SaaS · 23 November 2026 · evaluated engine v0.5.**

## User and problem

An L2 support engineer needs to assess a new ticket, identify the account's response deadline, find useful prior knowledge and choose an owning team. The course scenario supplies 400 enterprise accounts, 6,000 tickets per month, 25 engineers, a one-hour P1 SLA and a four-hour P2 SLA. The actual breach rate, root causes and handling-time baseline have not been observed.

The proposed assistant brings those decisions into one internal console. The current decision is **no launch of assisted mode on live tickets**: the evaluated prototype misses critical incidents and does not meet routine-acceptance criteria. See [the launch memo](08_launch_memo.md).

## Delivered workflow

The engineer enters an invented ticket with account, language, declared priority, creation time and text/logs. The local Python service masks recognised sensitive patterns, looks up the synthetic contract, computes a classifier suggestion, applies contextual rules and retrieves up to three same-customer or generic KB sources.

Suggestions-only is the default: the declared priority is kept. In the synthetic assisted demonstration, an eligible higher recommendation may raise priority; no recommendation automatically lowers it. In v0.5, a low classifier score triggers review but does not itself prevent such a raise. P1/P2, a proposed lowering, unsupported or uncertain inputs, sensitive requests and absent sources require appropriate engineer review. The SLA starts at the original creation time.

The engineer can inspect evidence, take over, change priority/team with a reason and record acceptance. Redacted tickets, decisions and the global mode persist in local SQLite. No customer message, remediation or ticket-system integration is executed.

## Scope and architecture

| Delivered | Boundary |
|---|---|
| Account/SLA lookup | Four synthetic account contracts; P3/P4 deadlines are explicit demo choices |
| Severity suggestion | TF-IDF plus balanced logistic regression trained on 300 synthetic rows; contextual rules and abstention gates |
| Source suggestions | Separate TF-IDF index over 15 synthetic documents, with bilingual search vocabulary and customer isolation |
| Human control | Verification, reasoned corrections, takeover, persistent suggestions/assisted switch and audit export |
| Local console and API | HTML/JavaScript, Python standard-library HTTP server and SQLite; loopback only, no external inference |

Customer communication, remediation, automatic lowering, live authentication/authorisation, production monitoring and automatic incident correlation are outside the delivered prototype. EN/FR are supported; other languages require a person. Redaction is a best-effort regex implementation, not certified DLP. Model scores are uncalibrated and must not be presented as measured correctness probabilities. The [architecture](04_architecture.md) and [spec](spec.md) describe the executable behaviour.

## Evaluation and value

The latest recorded batch contains 50 cases additional to the original 50. It yields 9/22 routine triages accepted by both recorded graders (40.9%, target at least 62%), P1 recall 9/14 (64.3%, target 100%) and false-P1 rate 3/28 on labelled P2/P3/P4 cases (10.7%, target at most 15%). No automatic lowering occurred in either recorded run.

The five latest missed P1s concern sensor removal, misuse of an API key, disabled detection, an uncontrolled remote session and credential dumping. These failures motivate spec EVAL-06 to EVAL-09; they have not been repaired and independently re-evaluated in this finalisation. Case/source ids being present do not prove the suggested troubleshooting is useful.

The second batch is not fully blind: its inputs had been visible to the developer. Main human grading used LLM-prefilled sheets, with associated anchoring risk. Luna confirmed her review of the grading sheets bearing her name on 23 November. Original outputs and grades remain available in the [report](evals/report_v0.md); results are not substituted with engineering tests or with demonstration performance.

The historical investment case assumes 33 minutes per ticket and 9.1 minutes saved on an accepted routine triage. It predicts value only if adoption, actual time saving and avoided breaches follow. Neither annual savings nor actual time saved have been measured. Those forecasts do not justify production integration while the safety gate fails.

## Data and research

All tickets and KB records are synthetic. Training contains 70 P1, 75 P2, 90 P3 and 65 P4 examples across 40 template families; its labels still require human review. The first 100 evaluation references are recorded as human-reviewed. A further 100 input candidates are prepared for review and must not be counted as evaluated or signed off.

The three S3 interviews are explicitly simulated role-play, with prepared answers. They provide design hypotheses, not evidence of real customer behaviour. The final product therefore retains human control and makes no validated adoption or time-saving claim. Semantic train/test independence, real research and operational source approval remain release conditions.

## Next decision

Keep the prototype local with invented data. Before reconsidering live use, complete genuinely independent evaluation and human review, resolve the training/source gaps, obtain real user observations and pass the safety and usefulness gates. The experiment and operational controls are specified in [06_07_experiments_operations.md](06_07_experiments_operations.md); no live pilot has been conducted.
