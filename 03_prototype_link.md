# 03 — Prototype link · SLA-aware triage copilot

> One clickable prototype of where the agent lives (the surface). Fake data only.

- **Link:** https://claude.ai/artifact/6xNp4g6SWZi9wq2CwhkiVq
- **Tool:** Claude artifact
- **Version:** v0.1 — first version from the prompt below; tested with one team member (finished the task, no hesitation) · v0.2 — after the user research: evidence line under every raise, confidence shown as a word with its basis, one-click preset reasons to lower a priority, and a fourth ticket where the copilot is wrong (a disguised incident left at P3 with low confidence)
- **Task for the v0.2 test:** "Four tickets have arrived. Check the copilot's triage on each one and correct anything you disagree with. Think out loud." *(We watch whether the tester accepts the Nordwind Energy ticket at P3 without checking.)*
- **The prompt we used (the brief in three paragraphs):**

```
Paragraph 1 — who uses it and for what job:
A support console for the 25 L2 support engineers of a cybersecurity SaaS with 400 enterprise
clients. Their job: put each new ticket at the right priority (P1–P4) and in the right team
before the SLA clock runs out (P1 = 1 h, P2 = 4 h). The copilot lives in a side panel of the
console they already use, not in a new tool.

Paragraph 2 — what is on the screen:
Left: the open tickets sorted by time left on the SLA, each with its priority, a live countdown
and a bar. Centre: the customer's message, with IPs and e-mails shown as masked tokens and a
line saying how many items were masked. Right: the copilot — proposed priority, confidence,
one-line reason, SLA clock, team, the closest resolved tickets — and three actions: Accept
triage, Take over, Change priority. It must never send anything to the customer.

Paragraph 3 — the rules:
The copilot can raise a priority on its own and must say why ("Raised from P3 to P1 because…").
It can never lower one: if it thinks a ticket is less urgent, the ticket keeps the higher
priority until an engineer confirms, and lowering always asks for a reason that goes into the
ticket log. "Take over" hides the proposal. Trust level: L4 to raise, person only to lower,
L1 for the similar-ticket suggestions.
```

- **Screenshot:** add one image in the repo (e.g. `prototype_v0.2.png`) and link it here.
