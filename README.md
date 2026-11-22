# Team 8 — SLA-aware prioritisation for cybersecurity SaaS

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School · shared project with Agentic Workflows
**Cohort:** M2-INTER-1 / M2-INTER-2 (keep one)
**Project:** P7 — SLA-aware prioritisation
**Repository:** [Cybersecurity-SaaS](https://github.com/LunaGrandjean/Cybersecurity-SaaS)

## Team
| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Jane Galthié | jgalthie-sketch | |
| Malek Saoudi | Msaoudi115 | |
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
| `00_pitch.md` | before S3, only if you bring your own idea | not applicable (official proposal P7) |
| `01_problem_statement.md` | S1–S2, Assignment 1 | done |
| `governance.md` | created for Assignment 1, one section added every session | Sessions 1 to 7 done; Session 8 at launch |
| `02_sizing_CyberSaas.xlsx` | S2, Assignment 2 | done: conditional go |
| `02_investment_memo.md` | S2, Assignment 2 | done |
| `03_product_brief.md` | S3 | done, v2, with `03_ai_lean_canvas.md`, `03_user_research.md`, `03_prototype_link.md`; final version at S8 |
| `04_architecture.md` | S4 | done: prototype v0.4 → v0.5, switch tested 22 Nov 2026 |
| `05_metrics.md` | S5 | done: metric stack, stop criterion, hierarchy by segment, three business metrics |
| `06_07_experiments_operations.md` | S6 + S7 (the course merges `06_ab_protocol.md` and `07_operations.md` into one file) | done: A/B protocol, monitoring, incidents, rollback, owners |
| `08_launch_memo.md` | S8 | to do (due 26 Nov) |
| `spec.md` | S4 → final | v2 with post-evaluation requirements EVAL-01 to EVAL-09; final version at S8 |
| `/prototype` | from S4 | local console and engine v0.5, switch test script, 35 regression tests |
| `/evals` | from S4 | `eval_set_v0.csv` (50) and `eval_set_v1.csv` (100) labelled by the team; frozen runs `runs/v0` and `runs/v1_fresh`; grading guideline and agreement rates in `evals/README.md`; results in `evals/report_v0.md` |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

## Run the prototype
From this repository root:
```powershell
uv run --python 3.12 python -m prototype.server
```
Open http://127.0.0.1:8765. Default: suggestions-only, synthetic data, no external inference, no customer action. More in [run and evaluation instructions](prototype/README.md) and [architecture](04_architecture.md).

Tests and the stop-switch drill:
```powershell
uv run --python 3.12 python -m unittest prototype.test_review prototype.test_evaluation prototype.test_workflow
uv run --python 3.12 python -m prototype.switch_drill --operator "Your Name"
```

## Results so far
Full detail in [`evals/report_v0.md`](evals/report_v0.md). Every case was labelled by the team before the run, and every run was graded by two people.

| | v0 (E001–E050) | v0.5 (E051–E100, fresh cases) | Criterion |
|---|---|---|---|
| P3/P4 triages both graders accept unchanged | 11.8 % | 40.9 % | ≥ 62 % |
| P1 recall | 78.6 % | 64.3 % | 100 % |
| False-P1 rate | 25 % | 10.7 % | ≤ 15 % |
| Priority lowered below declared | 0 | 0 | 0 |

The criterion is not met yet. The agent never lowered a priority, but it still misses P1s of attack types it has never seen. Next requirements: `spec.md` EVAL-06 to EVAL-09. The training labels are synthetic and not yet reviewed by the team, and no handling-time saving has been measured.
