# Investment memo — SLA-aware triage agent (P7, cybersecurity SaaS)

**Recommendation: no-go for a year-1 build at today's assumptions. Conditional go
if the S4 prototype shows ≥ 27 % handling time saved on routine tickets and a
breach audit shows ≥ 30 % of SLA breaches are caused by misprioritisation.**

## 1. [CFO question 1 — e.g. what is it worth?]
Year-1 net value: −€309k / +€5k / +€448k (pessimistic / base / optimistic),
weighted 30 / 50 / 20 % → expected value ≈ €0. Value comes from engineer time
saved on triage (€176k base, ≈ 2 FTE) and SLA penalties avoided (€81k base).
Fixed costs are €193k a year, half of it human supervision.

## 2. [CFO question 2 — e.g. compared to what?]
Doing nothing is worth €112k a year (the current process improving by 5 %).
The next-best project — rule-based SLA routing in our existing ticketing tool —
is worth ~€100k. The agent beats neither in expectation.

## 3. [CFO question 3 — e.g. what has to be true?]
The decision flips if time saved on routine tickets reaches ≈ 27 % (base: 15 %).
The second untested assumption: 30 % of breaches are avoidable by better
prioritisation, not caused by lack of capacity. Time saved is only cash if it
absorbs ticket growth without new hires.

## 4. [CFO question 4 — e.g. what can go wrong?]
A missed P1 means a penalty and a reputational risk. Guardrail: the agent may
raise a priority, never lower one without a human. Errors are priced at €54k a
year in the base case. Not included: revenue retained from accounts that churn
after repeated breaches — a real upside, unmeasured.

**Build / buy / orchestrate:** we would orchestrate (score 3.80 vs build 3.65,
buy 2.30) because client security telemetry must stay in our perimeter and our
engineers have no capacity to run a full build; we would build if [condition].

**Next step:** S4 prototype on 200 routine tickets to measure time saved, and a
root-cause audit of last year's SLA breaches.
