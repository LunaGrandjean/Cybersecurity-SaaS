# 01 — Problem statement

**Team:** 8 — Jane Galthié, Malek Saoudi, Luna Grandjean · **Agent:** P7 — SLA-aware prioritisation · **Last updated:** 2026-10-16

## 1. The problem in one sentence
Support engineers at an enterprise cybersecurity SaaS misprioritise incoming tickets, contributing to contractual SLA breaches and repeated troubleshooting work; the P7 scenario specifies 400 enterprise accounts, 6,000 tickets per month and 25 support engineers, but gives no measured breach rate, penalty amount or time-cost baseline. Without intervention, the described misprioritisation and repeated work are expected to continue; success means reducing the measured SLA breach rate without increasing incorrect triage or unsafe actions.

| Number | Value | Evidence status | Source or next test |
|---|---|---|---|
| Enterprise accounts | 400 | Scenario input; not independently measured | P7 project proposal |
| P1 response SLA | 1 hour | Scenario input; contractual target in the brief | P7 project proposal; verify against account records |
| P2 response SLA | 4 hours | Scenario input; contractual target in the brief | P7 project proposal; verify against account records |
| Tickets | 6,000 per month | Scenario input; not independently measured | P7 project proposal; validate with ticket-system export |
| Support engineers | 25 on rotation | Scenario input; not independently measured | P7 project proposal; verify with support team |
| SLA breach rate, penalties and repeated-work cost | Not provided | Unknown | Establish a historical baseline before setting a target |

## 2. Problem tree — from symptom to cause
- **Symptom:** Tickets are misprioritised, which the brief says causes SLA breaches; engineers also rewrite the same troubleshooting steps.
- **Problem:** The support workflow does not reliably connect ticket severity with the account's contractual SLA, and troubleshooting work is repeated. The current workflow and scale of each issue have not been measured.
- **Root cause (5 Whys):**
  1. Why are SLAs breached? The brief attributes breaches in part to misprioritised tickets.
  2. Why are tickets misprioritised? Unknown; inspect ticket content, account-SLA lookup, severity labels and queue routing.
  3. Why might those steps fail? Not established; compare the ticket record with the account contract and the engineer's decision.
  4. Why is troubleshooting repeated? The brief reports repeated steps, but does not explain whether knowledge is hard to find, incomplete or not reusable.
  5. Root cause is not yet established; validate it through ticket-history analysis and interviews before choosing a process fix.
- **What could address the described issues:** Apply deterministic SLA rules to ticket/account context, then retrieve relevant resolved tickets to suggest troubleshooting steps. Keep an engineer in control and never contact the customer directly. This is a candidate mix of rules, retrieval/AI and workflow changes; the actual root cause still needs validation.

## 3. Is AI the right tool?
| Question | Our answer |
|---|---|
| Is there a rule that solves 80% of it? | SLA lookup and deadline calculation should be deterministic. The brief does not say how much of prioritisation can be handled by rules; compare a rule-only baseline with engineer decisions. |
| Is it a prediction / generation problem, or an organisational decision? | Severity classification from ticket text and retrieval of troubleshooting suggestions may benefit from language models. Priority is still an operational decision, so the system should recommend and an engineer should approve. |
| Do we have the data — which, how much, who owns it? | The proposal assumes ticket text, account SLA data and resolved tickets. It gives a monthly ticket volume, but actual access, history, labels, quality, ownership and permissions are unconfirmed. |
| What does one error cost — and who pays it? | The brief names SLA breaches/penalties and repeated engineering work. The amount per breach, time per repeated task and error distribution are unknown; the company bears penalties and the support team bears rework. |

**Level chosen:** Provisional human-in-the-loop assistant combining deterministic SLA rules with text classification and retrieval. An agent is justified only if it must look up account SLAs and past cases across tools; otherwise a simpler classifier/search workflow may be enough. Autonomous customer contact is explicitly out of scope.

## 4. Why this agent — the four selection questions
| Criterion | Our answer |
|---|---|
| High frequency — is the work done every day or every hour? | 6,000 tickets per month in the proposal scenario indicates frequent work; the actual arrival pattern is unknown. |
| Bounded decision space — can we list its tools and outcomes on one slide? | Candidate inputs: ticket and account SLA. Candidate outputs: severity/priority recommendation and troubleshooting steps from resolved tickets. The brief forbids direct customer contact; ticket-system permissions and other actions remain to be defined. |
| Measurable success — can we say in one sentence whether it succeeded on one ticket? | Compare the suggested severity with an engineer-reviewed decision and whether the ticket met its SLA; measure overall SLA breach rate against a historical baseline. Neither baseline nor target is provided yet. |
| Recoverable failure — if it is wrong, is the damage limited and reversible? | P7 is described as borderline. A wrong priority can still cause a breach. Require engineer approval, an audit trail and a way to restore the previous priority; define rollback thresholds before any live pilot. Suggestions remain internal and the agent must never contact customers. |

## 5. Press release (Working Backwards)
*Hypothetical pilot announcement — not a customer claim:* For support teams at an enterprise cybersecurity SaaS, an internal SLA-aware assistant brings ticket severity, account response targets and relevant troubleshooting from resolved cases together for engineer review. The P7 scenario covers 400 enterprise accounts and 6,000 tickets per month. The pilot will measure SLA breach rate against the historical baseline; engineers retain approval and the assistant never contacts customers. **Customer quote:** to be collected; none was provided in the brief.

## 6. What would have to be true?
| # | Hypothesis | Evidence status | How we will test it | Session |
|---|---|---|---|---|
| 1 | Using account SLA context improves priority decisions and reduces SLA breaches versus the current workflow. | Guess to test | Audit historical tickets; compare an SLA-rule baseline, engineer decisions and a controlled pilot. | S4 prototype / S5 metrics / S6 A/B |
| 2 | Suggestions retrieved from resolved tickets reduce repeated troubleshooting without reducing answer quality. | Guess to test | Measure handling time and suggestion use; have engineers review a sample for relevance and correctness. | S4 prototype / S5 metrics |
| 3 | Engineer approval and a no-customer-contact boundary keep errors recoverable. | Proposed guardrail; effectiveness untested | Test overrides, incorrect-priority cases, auditability and rollback in a sandbox before any live pilot. | S4 prototype / S6 A/B |

## 7. Do-nothing baseline
The proposal describes 6,000 tickets per month, misprioritisation linked to SLA breaches and repeated troubleshooting steps. If nothing is built, those issues may continue, but the 12-month direction and cost cannot be estimated from the brief: no current breach rate, penalty data, handling-time baseline, volume trend or planned process changes are provided. First measure these against historical ticket and SLA records; do not treat the scenario figures as operational measurements.
