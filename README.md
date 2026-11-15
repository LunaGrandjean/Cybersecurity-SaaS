# Team 8 — SLA-aware prioritisation for cybersecurity SaaS

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School · shared project with Agentic Workflows
**Cohort:** M2-INTER-1 / M2-INTER-2 (keep one)
**Project:** P7 — SLA-aware prioritisation
**Repository:** [Cybersecurity-SaaS](https://github.com/LunaGrandjean/Cybersecurity-SaaS)

## Team
| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Jane Galthié | | |
| Malek Saoudi | | |
| Luna Grandjean | LunaGrandjean | |

## Our agent
- **Starting point:** P7 — SLA-aware prioritisation
- **The company:** Cybersecurity SaaS — 400 enterprise accounts, 6,000 tickets a month, 25 support engineers, SLA P1 = 1 h, P2 = 4 h
- **The job, in one sentence:** When a new support ticket arrives, the agent looks up the client's SLA, proposes a severity with its reason and the closest resolved tickets, producing a triage that an engineer accepts or corrects before the SLA clock runs out.
- **Trust level per step:** L4 to raise a severity · person only to lower one · L1 for similar-ticket suggestions · L3 for routing P3/P4 tickets (lead samples 5 %) · person only for diagnosis and any customer message
- **One thing it must never do:** lower a ticket's priority on its own — and never contact a customer.

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | — not applicable (official proposal P7) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | done |
| `governance.md` | created for Assignment 1, one line added every session | Sessions 1–4; team sign-off pending |
| `02_sizing_CyberSaas.xlsx` | S2 — Assignment 2 | done — conditional go |
| `02_investment_memo.md` | S2 — Assignment 2 | done |
| `03_product_brief.md` | S3 | done - v2 — with `03_ai_lean_canvas.md`, `03_user_research.md`, `03_prototype_link.md` |
| `04_architecture.md` | S4 | implemented v0.4; independent evaluation pending |
| `05_metrics.md` | S5 | Assignment 5 — due 22 Nov |
| `06_ab_protocol.md` | S6 | to do |
| `07_operations.md` | S7 | to do |
| `08_launch_memo.md` | S8 | to do |
| `spec.md`, `product_brief.md` | final | `spec.md` v2 (S4), post-eval misses pending; `product_brief.md` at S8 |
| `/prototype`, `/evals` | from S4 | 300 synthetic training rows, 50 unlabelled eval inputs, functional local console |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

## Run the S4 prototype
From this repository root:
```powershell
uv run --python 3.12 python -m prototype.server
```
Open http://127.0.0.1:8765. Default: suggestions-only, synthetic data, no external inference or customer action.
See [run and evaluation instructions](prototype/README.md), [architecture](04_architecture.md), [pending eval report](evals/report_v0.md) and [team handoff checklist](S4_CHECKLIST.md).

15 November technical correction: 29 engineering tests and 16 real-browser checks passed. Exposed-demo misses were corrected with the original diagnostic preserved; this is not an independent performance result. [Instructions pour Jane, Malek et Luna](evals/VALIDATION_EQUIPE.md) cover the actual 50-label review, guarded import and subsequent two-person grading.

Training labels are AI-proposed pending review. Holdout labels and two independent human grades must be completed before a product-performance claim. No measured handling-time saving is available yet.
