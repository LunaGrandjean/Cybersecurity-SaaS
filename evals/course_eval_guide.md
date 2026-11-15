# The eval-set — what a "case" is for your project

The eval-set is the list of situations your agent must handle, each with the answer a good system would give. It is the judge of your prototype (Session 4), the seed of your metrics (Session 5) and the thing you replay after every change (Session 7).

For a support agent a case is a **ticket**. For another agent it is whatever the agent receives: a document to summarise, a record to score, an incident to detect, a hotel's reviews to explain. `eval_set_v0.csv` has one example row per proposal (P1–P8) and one for a project of your own — delete the examples and write yours.

## One row = one case

| Column | What to write |
|---|---|
| `input_the_agent_receives` | the message, document, record or event, as the agent will see it — with the context it gets (account, history, data) |
| `expected_output_or_action` | what a good answer or action looks like, specific enough that two graders can say *yes / no* without arguing |
| `evidence_or_source` | where the right answer comes from (article, policy clause, data row, past case) |
| `hand_over_to_a_person` | yes / no — and the trust level if it matters (L2 draft, L4 under a threshold…) |
| `segment` | language, plan, region, severity, amount band… — whatever you will later check results *by* |
| `origin` | invented · anonymised · real-public. Never real customer data |
| `notes` | why this case is in the set (easy · hard · out of scope · the trap of your proposal) |

## Rules
- **20 cases for 6 November, 50 with Assignment 4, 200 by Session 5.**
- Label them **before** you run the prototype on them, and never change a label because of the prototype's output.
- Mix: easy cases, hard cases, out-of-scope cases that must be handed over, and every segment you serve. Oversample the rare catastrophic case of your proposal (a P1 ticket, a refund over the threshold, a grade request, a merged incident).
- Never tune the prompt or the rules while looking at these rows. If you did, that row is demo data now: say so in `evals/report_v0.md`.
- "Sendable / usable as is" is judged by **two people** on each output, independently. The script counts outputs; the people decide.

For the Session 4 workshop everyone uses the Paylio starter (`support-copilot-starter.zip`, `evals/tickets_v0.csv`): that is the class example. Your team's file is `evals/eval_set_v0.csv`.

## No data for your project? Generate the inputs, label them yourselves

Most teams have no real tickets, documents or records — that is expected. The Paylio starter's `data/tickets_synthetic.csv` is generated too. The rule is simple: **the inputs can be synthetic; the labels must be human.**

1. **Start from what exists.** P8 has `reviews.csv` (real, public). Every proposal has public material you can use as inputs: a product's public documentation or help centre (the knowledge base), a public status page, a refund policy, a published SLA. Public datasets of support conversations exist on Hugging Face and Kaggle — check the licence and the language before you use one.
2. **Write the first five cases by hand**, one per situation type: an easy one, a hard one, an out-of-scope one, one in another segment (language, plan, severity), and the trap of your proposal (a P1, a refund above the threshold, a grade request, two incidents at once).
3. **Generate variety with an AI, from those five** — paste the prompt below. Ask for 30, keep 20. Make it produce messy inputs: typos, two questions in one, missing context, the wrong channel, a customer who is angry or who writes in another language.
4. **Label by hand, before any run.** The expected output, the evidence, hand-over yes/no, the segment. Not the AI: if the model that writes your cases also writes your labels, your eval-set agrees with itself and measures nothing.
5. **Someone who did not write the case grades it** when the prototype runs. Two graders, independently.
6. **Write the origin in every row** (`invented`, `AI-generated · human-labelled`, `anonymised`, `real-public`) and say so in `04_architecture.md` §7. An eval-set with a documented origin is a credible eval-set; one presented as "real" without a source is a flaw — the Session 4 drill, in reverse.

What not to do: real customer data from an internship or a job (never, whatever the anonymisation); generating the cases with the same prompt your drafter uses (it will pass by construction); fifty variants of one easy case.

### Prompt to generate cases (paste, then edit the brackets)

```
You write test cases for an AI agent. The agent: [one sentence from your brief — who uses it, what it does, what it must never do].
Here are five cases I wrote, in CSV with these columns: input_the_agent_receives, segment, notes.
[paste your five rows]
Generate 30 more inputs in the same format, realistic and varied:
- cover these segments: [languages / plans / severities / amount bands you serve]
- at least 6 must be out of scope or must be handed over to a person: [list the sensitive situations]
- at least 5 must be messy: typos, two questions in one, missing information, an angry tone
- no two inputs about the same situation
Leave expected_output_or_action, evidence_or_source and hand_over_to_a_person EMPTY — I will fill them in by hand.
```
