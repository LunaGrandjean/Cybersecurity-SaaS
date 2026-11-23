# Local SLA triage prototype

Run from the **Cybersecurity-SaaS repository root**. Python 3.11-3.13 is supported; the checked environment is Python 3.12. No API key, external database service or Node installation is needed.

```powershell
uv run --frozen --python 3.12 python -m prototype.server
```

Open http://127.0.0.1:8765. The first dependency installation requires network access; inference and assets are local. Startup reports model preparation and the ready address. Keep the terminal running. Use invented data only. Default mode is suggestions-only. The evaluated engine is v0.5, while the console originated as v0.4 from Jane's preserved v0.2.

## Engineer workflow

1. Load demo tickets or enter an invented ticket.
2. Inspect effective versus suggested priority, the original SLA time, actual matched excerpts and scoped sources.
3. Verify/change priority or team with a reason; acceptance is enabled after required review.
4. Take over to hide the suggestion while keeping manual controls.
5. Demonstrate the assisted/suggestions switch on synthetic tickets only. It does not lower existing raised priorities. Live assisted launch is not approved.
6. Export the audit and reload to verify persistence. Local operator names are self-declared, not authenticated identities.

The service uses Python's standard-library ThreadingHTTPServer and SQLite, not FastAPI. There is no customer-send, remediation or automatic-lowering endpoint. Model scores are uncalibrated; the UI labels the scored class correctly when CALM-01 caps a P1 classifier suggestion.

## Verification

```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_review prototype.test_evaluation prototype.test_workflow -v
uv run --frozen --python 3.12 python -m prototype.audit_submission
```

The audit verifies existing evidence and leaves historical metrics untouched. It does not perform a new evaluation or create signatures. [Current checks](../evals/engineering_checks.md).

Optional browser QA requires installed Edge; start a separate local server/database if you want to preserve your normal demo state:

```powershell
uv run --frozen --python 3.12 python -m prototype.server --port 8767 --db prototype/runtime/browser-qa.sqlite3
# In another terminal, with a new evidence directory:
uv run --frozen --extra qa --python 3.12 python -m prototype.verify_browser --url http://127.0.0.1:8767 --out-dir evals/NEW_UNIQUE_QA_DIRECTORY
```

The browser check adds invented demo tickets and saves browser_checks.json and prototype.png in the requested directory. It never opens candidate holdout files. The server must be in suggestions mode at the start of this check.

## Evaluation

The old v0/v1_fresh runs already have predictions: do not run or freeze over them. To check their results without rewriting them:

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --cases evals/eval_set_v0.csv --run-dir evals/runs/v0 --check-only
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --cases evals/eval_set_v1_fresh.csv --run-dir evals/runs/v1_fresh --check-only
```

For the additional E101-E200 candidates, follow [the team review guide](../evals/VALIDATION_EQUIPE.md): human annotation and semantic overlap review, then freeze, run once, two actual graders and summarise. References remain blank until those decisions are made. Fixture/preparation scripts refuse existing files so they do not overwrite edits. Never use case ids alone as proof of independence.

Dependencies are locked in uv.lock. Historical file hashes accept only LF/CRLF conversion, not other changes. Model fingerprints still include source/data bytes and runtime versions; new manifests record those details. A different local fingerprint cannot be passed off as a reproduction of archived inference.

## Limits and stopping

Synthetic contracts, unreviewed synthetic training labels, simulated KB approval, regex redaction gaps and no authentication limit this to a local demonstration. Current P1/usefulness gates fail: [launch decision](../08_launch_memo.md). No time saving or production effect has been measured.

Stop with Ctrl+C. To reset a local demo, stop its server first and remove only its chosen SQLite file under prototype/runtime. Original Jane HTML and screenshots remain preserved.
