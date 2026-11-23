# Team 8 SLA triage copilot

**P7 Cybersecurity SaaS | Finalisation 23 November 2026 | Evaluated engine v0.5**

The prototype helps an internal support engineer propose severity, preserve the original SLA clock, retrieve customer-scoped knowledge and record a human decision. It never lowers a priority automatically, contacts a customer or executes remediation.

**Decision: no live assisted launch.** Keep the current release as a local synthetic-data demonstration in suggestions-only mode. The latest recorded run misses 5 of 14 expected P1 incidents. The [launch memo](08_launch_memo.md) states the evidence, risks and conditions for reconsideration.

## Team

Jane Galthie, Malek Saoudi and Luna Grandjean. Each person uses their own Git account for genuine contributions. Operational owners in the documents are proposed roles, not real production appointments.

## Run and verify

Run these commands from this repository root:

```powershell
uv run --frozen --python 3.12 python -m prototype.server
```

Open http://127.0.0.1:8765 and use invented data only. Dependencies are locked; the first installation needs network access, inference does not. The default is suggestions-only. Assisted mode is available for synthetic workflow demonstrations, not approved for live tickets.

```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_review prototype.test_evaluation prototype.test_workflow -v
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --run-dir evals/runs/v0 --cases evals/eval_set_v0.csv --check-only
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --run-dir evals/runs/v1_fresh --cases evals/eval_set_v1_fresh.csv --check-only
uv run --frozen --python 3.12 python -m prototype.audit_submission
```

The summary commands recompute results without changing recorded metrics. Legacy Windows/Git LF/CRLF conversion is accepted; other changes to frozen cases or predictions still fail validation. The submission audit distinguishes integrity checks, failed product gates and remaining human work.

## Recorded results

| Measure | Initial run, E001-E050 | Latest run, E051-E100 | Gate |
|---|---|---|---|
| P3/P4 accepted by both recorded graders | 2/17 = 11.8% | 9/22 = 40.9% | At least 62%: not met |
| P1 detected | 11/14 = 78.6% | 9/14 = 64.3% | 100%: not met |
| False P1 on labelled P2/P3/P4 | 7/28 = 25.0% | 3/28 = 10.7% | At most 15%: met on latest run |
| Automatic lowering | 0/50 | 0/50 | Zero: met |

See [report_v0.md](evals/report_v0.md) for methods, original evidence and limitations. The batches differ, the second batch's inputs had been visible to the developer, and main human grading used LLM-prefilled sheets. Luna confirmed actual review of sheets bearing her name on 23 November. No actual handling-time saving or annual financial benefit has been measured.

## Deliverables

| File | Purpose and current state |
|---|---|
| `01_problem_statement.md` | Scenario facts, unknown baseline and problem hypotheses |
| `02_sizing_CyberSaas.xlsx`, `02_investment_memo.md` | Historical conditional investment hypotheses; final decision is in S8 |
| `03_product_brief.md`, `03_ai_lean_canvas.md`, `03_user_research.md` | S3 design history; interviews remain explicitly simulated |
| `03_prototype_link.md` | Original Jane prototype and functional local console |
| `04_architecture.md` | Actual v0.5 workflow, checkpoints, switch, data and limits |
| `05_metrics.md` | Current metrics, segment counts, business hypotheses and evaluation limits |
| `06_07_experiments_operations.md` | Proposed experiment and operations plan; not a deployed pilot |
| `08_launch_memo.md` | No live assisted launch; conditions for reconsideration |
| `product_brief.md` | Final consolidated product scope and evidence |
| `spec.md` | Implemented behaviour and remaining EVAL-06 to EVAL-09 requirements |
| `governance.md` | Sessions 1-8, checkpoints, owners and final scope |
| `evals/report_v0.md`, `evals/runs/` | Two preserved evaluations and original grades |
| `evals/finalisation_2026_11_23/` | Separate finalisation evidence, grading confirmation and browser checks |

## Evaluation coverage and remaining human work

There are **100 recorded human-reviewed cases** and **100 additional input candidates** in `evals/eval_set_v2_candidates.csv`. The latter have no expected answers or grades and have not been passed to the model. The target of 200 human-reviewed cases is **not yet met**. Exact text and unique ids cannot establish semantic independence.

Draft expected answers are available in `evals/ai_review/proposed_labels_v2.csv`; all human decisions/names/dates remain blank. They are review aids, not model outputs or ground truth.

Follow [VALIDATION_EQUIPE.md](evals/VALIDATION_EQUIPE.md) to review those candidates before any new inference. Production also requires training-label/source review, real user observations, approved data access/retention and operational sign-off. None is substituted with fabricated evidence.

The lecturer's requirements concerning four commit authors for a three-person team and any missing classroom starter remain to be reconciled. Team members must review and commit their changes, then create the final `v1.0` tag before the oral deadline specified by the course. No final tag, push, deployment or real operational approval is claimed by these files.

[Current handoff](S4_CHECKLIST.md) | [Prototype instructions](prototype/README.md) | [Finalisation checklist](FINALISATION.md)
