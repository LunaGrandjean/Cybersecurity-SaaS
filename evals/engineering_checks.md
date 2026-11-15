# S4 engineering verification — updated 15 November 2026

These checks validate implementation behaviour. **They are not the independent product evaluation, human research, or measured handling-time savings.** No holdout predictions were produced.

## Current verification — 15 November

Command from the repository root:
```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_workflow prototype.test_evaluation prototype.test_review -v
```
Observed in the locked Python 3.12 environment: **29 tests passed, 0 failures/errors, 7.283 seconds**. This adds EN/FR traffic-volume anomaly boundaries, planned-backup/hypothetical controls, incident/legal separation, bounded service-impact rules, bilingual source matching and guarded review import to the earlier checks. Import on the untouched actual draft was also refused at E001 for missing real human decision; it did not create a reviewed output or predictions.

Real Edge / Playwright 1.65.1 check on a separate local server/database: **16 checks passed**, no JavaScript errors and no page requests outside the local service. [New JSON evidence](engineering_2026_11_15_retry/browser_checks.json), timestamp `2026-11-15T20:18:11.791295+00:00`; model `e472b6a6d01222de`; [new screenshot](engineering_2026_11_15_retry/prototype.png). Prior evidence remains preserved below.

The first browser attempt failed because the test used a JavaScript string predicate incompatible with the page's Content Security Policy. The check now waits on the actual locator; the application CSP was kept. The full retry passed. The check exercises the actual browser → API → engine → SQLite → UI flow, plus reloads and switch audit, using only invented demo inputs.

The [post-fix exploratory comparison](ai_review/post_fix_2026_11_15/comparison.md) preserves the old run and expected references. No official E001–E050 inference was executed. Human labels, two independent grades and team-operated switch sign-off remain pending.

## Historical verification — 12 November

## Python workflow / API / evaluation-protocol checks
Command, from the repository root:
```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_workflow prototype.test_evaluation -v
```
Observed on the locked Python 3.12 environment: **21 tests passed; 0 failures; 0 errors** (final run: 21 tests in 14.514 seconds).

Covered: synthetic training counts/provenance; recognised redaction patterns; actual matched rule evidence; never-lower; suggestions switch preventing raises; original SLA timestamp after escalation; customer-specific retrieval isolation; unsupported language/account abstention; insufficient input/no source; hypothetical/negated attack terms; privileged-action handover; invalid input; API health and static console; reason/review acceptance gates; persisted ticket state; audited/persisted switch; cross-origin rejection; absence of customer-send endpoint; model-failure fallback; unlabelled/frozen/changed evaluation guards; two-grader protocol and prediction-tampering detection.

The evaluation-protocol tests use explicitly fictional unit fixtures in Git-ignored runtime directories. Their generated grades/results are not product evidence and are removed after testing.

## Real browser: UI → API → inference → storage → UI
Installed Microsoft Edge, Playwright 1.65.1. Historical evidence is [browser_checks.json](browser_checks.json), recorded at `2026-11-12T14:36:20Z`. Inference fingerprint: `41acde6fcf51b4c1`; 300 training rows. Current 15 November evidence is linked at the top.

**16 browser checks passed; no JavaScript errors; no page requests outside the local service.**

Verified: console startup in suggestions mode; demo loading; new synthetic ticket submission and redacted rendering; no automatic raise in suggestions mode; acceptance blocked until review; takeover retaining manual controls; engineer priority/team correction; acceptance after verification; tickets surviving reload; global assisted/suggestions switch; persisted switch; audit download; desktop panels scrolling inside the viewport; 390px viewport without horizontal overflow.

During repeatable browser QA, a new-ticket modal could close before the refreshed ticket was rendered. The UI now waits for refreshed state before closing; the check uses a unique ticket title so it cannot accidentally inspect an older demo ticket. The final browser run passed after that change.

Screenshot: [prototype v0.4](../prototype/prototype_v0.4.png).

## Data and provenance verification
- Original Jane v0.2 HTML preserved byte-for-byte in `prototype_triage_copilot_v0.2.html`.
- Original 20-case CSV preserved byte-for-byte in `demo_reference_v0.csv`.
- Current training: 300 rows, AI-proposed training labels; not certified as human reviewed.
- New holdout: 50 inputs; all expected-severity fields blank and `label_status=pending_human`.
- No `evals/runs/v0/predictions.json` exists. No 62% acceptance, P1 recall or time saving is claimed.
- Git whitespace check completed without errors after line-ending normalisation.

## Still required from the team
Training-label review, semantic leakage review, human expected answers, a frozen independent run, two independent human graders, observed top misses and actual team operator sign-off of the switch. See [S4_CHECKLIST.md](../S4_CHECKLIST.md).
