# 03 — User research · SLA-aware triage copilot

> Three conversations + one usability test of the prototype.
> **Important: these are simulated interviews.** No real user was reached in time. Members of our project team played each role from a prepared role brief, with answers prepared in advance. We therefore treat everything below as **hypotheses to verify with real users**, not as evidence. Quotes are translated from French.

## Who we talked to
| # | Who (role played) | Real user or classmate in role? | Date | Interviewer · note-taker |
|---|---|---|---|---|
| 1 | "Thomas" — L2 support engineer at a cybersecurity SaaS (3 years, ~40 tickets a day) | Team member in role (simulated) | 5 Nov 2026 | project team |
| 2 | "Sarah" — SOC analyst at a consulting firm | Team member in role (simulated) | 6 Nov 2026 | project team |
| 3 | "Marc" — IT manager of a 300-person SME, opens tickets with vendors | Team member in role (simulated) | 8 Nov 2026 | project team |

## Interview guide used (past behaviour only)
1. Tell me about the last urgent ticket you handled. What did you look at first?
2. How long did it take you to decide how urgent it was?
3. A time a ticket turned out worse than it looked: how did you find out?
4. The last time a ticket's priority was lowered: who decided, and what did they check?
5. When a tool suggests a priority, what do you do with it?

## What we heard (in their words, simulated)
| # | Quote or behaviour | Which part of our brief it confirms or contradicts |
|---|---|---|
| 1 | Looked at the client's name and tier first, then the logs: "It's an Enterprise account, so it hurts." | **Confirms** step 1 (tier lookup) comes first → MUST is right |
| 1 | Deciding urgency: "maybe 5 minutes, tops." | **Consistent** with our steps 1–2 (2 + 3 = 5 min). Says nothing about step 3 (search, 6 min), which stays **unverified** |
| 2 | Deciding urgency: "4 or 5 minutes" (logs + IP reputation). | Same as above |
| 1 | A "dashboard loads slowly" ticket sat 2 h in the normal queue until 4 other clients reported the same thing. | **New:** the strongest signal of a disguised P1 can be several clients with the same symptom — our agent triages each ticket alone |
| 2 | An adware block filed as "Low" became a ransomware precursor 6 h later when threat intel was updated. | **New:** a ticket's severity can change after triage when new information arrives — our agent only triages once |
| 3 | Low-priority Wi-Fi drops turned into a full office outage the next day. | Confirms disguised P1s exist on the client side too |
| 1 | Lowers priorities "every day" (a P1 for a PDF export), using the SLA matrix: "otherwise everything is urgent and nothing is." | **Confirms** lowering is frequent and a human call — but **warns** that our "reason required" rule adds friction to a daily action |
| 2 | Downgraded a "critical mass file deletion" alert after seeing it was a scheduled IT script. | Confirms lowering needs a human who checks the evidence |
| 3 | "They checked their procedure instead of listening to my need" (backup line down, lowered to medium by tier-1). | **Confirms** the "never lower without a person" rule, and that lowering on the contract alone frustrates clients |
| 1 | Distrusts suggestions: the tool raises priority because "Urgent" is typed three times in caps; always checks by hand. | **Contradicts** using customer words as P1 triggers → the agent must raise on facts, not on tone |
| 2 | Treats a high-confidence score "as a hint, not a truth" and redoes the analysis. | Confirms the risk that a bare score is ignored → show the evidence, not just a number |
| 3 | Closes suggested-article pop-ups immediately; overrides auto-categorisation to reach a senior engineer. | Confirms the customer-facing chatbot stays out of scope |

## Usability test — one task, think aloud, don't help
**Prototype link:** see `03_prototype_link.md` (tester 1 on v0.1, tester 2 on v0.2)
**Task given:** "Three new tickets have arrived. Decide which one you'd handle first, and set the right priority on the Helix Logistics ticket. If you disagree with the tool, change it. Think out loud."

| Tester | Finished without help? | Where they hesitated | What they expected instead |
|---|---|---|---|
| Team member (simulated user) | yes | no hesitation observed | — |
| Second tester — team member (simulated user), on v0.2 | yes | no hesitation on the task; asked two questions | (1) "What does the confidence percentage mean?" (2) "What does the tool do with a ticket that has too little information to classify?" — neither answer was visible on screen |

**What the test does not show:** the agent was right on every ticket, so the task only checked that the screen is usable, not that a tester catches a wrong triage. v0.2 adds a ticket where the agent misses a disguised P1.

## Desirability gate — do they want it?
- [x] 2 of 2 finished the task without help
- [ ] They told us what they did last time — **yes, but in simulated interviews**
- [ ] At least one said "I want this before…" — **no**
- [x] Our out-of-scope list grew; our success criterion did not move

**Decision:** go to the build, because both testers used the screen without help and nothing contradicted the design. The second tester's two questions (confidence percentage, vague tickets) are answered in the brief and the spec. **Condition:** replace at least one simulated interview with a real support engineer before Session 5. Until then, the changes in brief v2 are hypotheses.
