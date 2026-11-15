# Local triage prototype — Assignment 4

Run commands from the **Cybersecurity-SaaS repository root**, not from `prototype/`.
Requires Python 3.11–3.13 and scikit-learn 1.7.2. No API key, database service or Node installation.

```powershell
uv run --python 3.12 python -m prototype.server
```

Open **http://127.0.0.1:8765**. The server is loopback-only. `uv` installs the pinned dependency automatically; the first install needs internet, inference itself does not. Alternatively create a Python 3.12 venv, run `python -m pip install scikit-learn==1.7.2`, then `python -m prototype.server`.

Startup prints `[1/3]` while loading ML libraries, `[2/3]` while preparing the classifier, and `[3/3] Ready` when the address can be opened. The first launch can be slower on a OneDrive folder. Keep that terminal open while using the console. The project uses uv copy mode to avoid unsupported hardlink warnings across the cache and OneDrive.

1. Load demo tickets or enter a new **invented** ticket.
2. Inspect the effective priority, model/rule suggestion, source evidence and original SLA timestamp.
3. Verify/change priority or team; give an engineer reason. Acceptance becomes available after required review.
4. Take over: the proposal is hidden and manual controls remain available.
5. Change mode: suggestions-only is the default; assisted mode permits eligible raises on new tickets. Never lowers automatically.
6. Export audit to inspect recorded events. Reloading the page or restarting the server preserves local state.

The UI derives from Jane's console; its original v0.2 is preserved in `prototype_triage_copilot_v0.2.html`. The functional page must be served by Python, not opened directly as `file://`.

```powershell
# Engineering regression checks (not product evaluation)
uv run --python 3.12 python -m unittest prototype.test_workflow prototype.test_evaluation prototype.test_review -v

# Candidate validation: intentionally fails until the TEAM fills the labels
uv run --python 3.12 python -m prototype.evaluate validate

# After human labels and semantic leakage review; freeze BEFORE prediction
uv run --python 3.12 python -m prototype.evaluate freeze
uv run --python 3.12 python -m prototype.evaluate run

# Two people independently complete evals/runs/v0/grading_a.csv and grading_b.csv
uv run --python 3.12 python -m prototype.evaluate summarise
```

Fixture generation is reproducible with `python -m prototype.prepare_data`; existing data and human annotations are never overwritten. Keep evaluation data out of training and do not tune on exposed holdout outputs.

Team review: [step-by-step instructions in French](../evals/VALIDATION_EQUIPE.md), including Jane E001–E017 / Malek E018–E034 / Luna E035–E050 and the guarded `prototype.import_review` command. Labels are not automatically accepted on behalf of a team member.

To repeat the exploratory **exposed-demo** diagnostic, preserve the earlier run:
```powershell
uv run --frozen --python 3.12 python -m prototype.diagnose_demo --out-dir evals/ai_review/NEW_UNIQUE_RUN
```
The 15 November correction detects large outbound-volume anomalies and suspected breaches, distinguishes legal handling from incident urgency, adds bounded service-impact rules and bilingual source aliases. These rules are provisional development policy; source aliases improve search and are never ticket evidence. The original classifier score remains uncalibrated. A traffic-volume anomaly is a reason to investigate, not proof of theft.

Dependencies are recorded in `uv.lock`; use `uv run --frozen --python 3.12 ...` to refuse unexpected dependency changes. The model fingerprint includes code, fixture bytes and Python/scikit-learn/NumPy/SciPy versions.

Optional browser QA (installed Microsoft Edge required; start the server first):
```powershell
uv run --frozen --extra qa --python 3.12 python -m prototype.verify_browser --out-dir evals/NEW_UNIQUE_QA_RUN
```
This creates additional synthetic demo tickets, exports engineering audit evidence and captures `prototype_v0.4.png`. It never opens the holdout. Evidence: `evals/browser_checks.json`.

Local demo limits: no authentication, synthetic contracts, approximate regex redaction, uncalibrated classifier score, small template-based training set and synthetic KB with simulated sign-off. No production integration or customer action exists. Stop with Ctrl+C. To reset the demo, stop the server and remove only `prototype/runtime/triage.sqlite3`.
