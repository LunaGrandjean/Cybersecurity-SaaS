# Investment memo — SLA-aware triage agent (P7, cybersecurity SaaS)

**Recommendation: conditional go. Expected value ≈ €133k a year, above both the do-nothing (€112k) and the next-best project (€100k), on one condition: the S4 prototype must show ≥ 17 % handling time saved on routine tickets. Below that, no-go. Because the pessimistic case (−€187k) does not clear the hurdle, we commit the integration budget only after the test, not before.**

## 1. What is it worth?

The agent reads every incoming ticket and proposes a priority (P1 to P4) using the ticket content, client telemetry and the client's contract tier. It creates value in two ways.

| Year 1, base case | € / year |
|---|---|
| Engineer time saved on triage (≈ 2.6 FTE in year 1, ≈ 4.6 at full adoption) | 234,520 |
| SLA penalties avoided (240 breaches × 30 % avoided × €2,000 × year-1 ramp) | 81,000 |
| Cost of agent errors (mainly false escalations) | −25,920 |
| AI handling cost (tokens, retries) | −4,503 |
| Fixed costs (integration amortised, evaluation, 0.5 FTE supervision, monitoring, re-evaluation) | −133,333 |
| **Net annual value** | **151,764** |

Across scenarios, year-1 net value is −€187k (pessimistic), +€152k (base) and +€565k (optimistic). Weighted 30 / 50 / 20 %, the expected value is ≈ €133k. The weighting leans pessimistic on purpose: we do not yet know how many breaches come from misprioritisation rather than lack of capacity.

## 2. Compared to what?

Doing nothing is worth ≈ €112k a year: the current process keeps improving by about 5 % on its own. The next-best project for the same team is rule-based SLA routing in our existing ticketing tool, worth ≈ €100k. The agent clears both in expectation, but only by €20–33k. This conditional go does not rely on lowering the do-nothing bar, the hurdle, or the penalty assumptions, which all come from the course brief or stay deliberately conservative.

## 3. What has to be true?

The decision flips at ≈ 17 % handling time saved on routine tickets (base: 20 %, taken from the course's copilot benchmark). That is the number the S4 prototype must measure on 200 routine tickets. Two further assumptions matter. First, 30 % of SLA breaches must be avoidable by better prioritisation; we will check this with a root-cause audit of last year's breaches. Second, the time saved is only cash if it absorbs ticket growth without the hires planned for next year. If volume stays flat, it frees engineers but does not reduce cost, and the case rests on penalties alone.

## 4. What could go wrong?

A missed P1 means an SLA penalty and a reputational risk with enterprise clients. Guardrail: the agent may raise a priority on its own but never lowers one without an engineer. Its errors are therefore mainly false escalations, priced at ≈ €26k a year, plus a residual risk that engineers trust the agent too much. Two further caveats. We assume the 25 engineers are fully dedicated to support and cost €90k loaded each, which is the top of the Paris range; a lower figure would reduce the value of time saved. Not included: revenue retained from enterprise accounts that churn after repeated breaches, a real upside that we have not measured.

**Build / buy / orchestrate:** we orchestrate (weighted score 3.80, against build 3.60 and buy 2.40), because client security telemetry must stay in our perimeter and our engineers have no capacity to run a full build. We would build only if two engineers could be freed for evaluation and on-call. Buying looks ≈ €41k a year cheaper on paper, but that comparison ignores the integration a bought tool still needs and would send client telemetry to a third party.

**Next steps:** (1) S4 prototype on 200 routine tickets to measure time saved against the 17 % threshold; (2) root-cause audit of last year's SLA breaches; (3) integration budget released only if both come back positive.
