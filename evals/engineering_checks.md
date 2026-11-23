# Final engineering verification on 23 November 2026

These checks verify the local synthetic-data workflow. They do not turn a failed product gate into a pass, validate new references or measure business benefit.

## Current checks

- **36 regression tests passed** in the locked Python 3.12 environment. Added coverage proves LF/CRLF-only portability while changed labels, content or extra whitespace remain rejected; new freezes record runtime/source/data provenance; check-only summaries do not overwrite recorded metrics.
- **16 checks passed in Microsoft Edge**, covering browser -> API -> model/retrieval -> SQLite -> UI, redaction, review/acceptance gates, takeover, switch, reload persistence, audit export and mobile overflow. No JavaScript errors or page requests outside the local service. [Evidence](finalisation_2026_11_23/browser/browser_checks.json) and [screenshot](finalisation_2026_11_23/browser/prototype.png).
- **Both stored metrics files recompute identically** from their original references, outputs and grades. v0 predictions match the historical hash under CRLF-only reconstruction; v1_fresh matches exact bytes. No run, grade, source engine or training data was changed. [Final audit](finalisation_2026_11_23/submission_audit_final.json), [original evidence snapshot](finalisation_2026_11_23/original_evidence_sha256.json).
- The 100 additional input candidates have unique ids and no exact normalised text overlap with existing training/evaluation inputs. This does not certify semantic independence; all expected answers and human fields remain blank. No predictions were run on them.
- The console now labels the score returned after CALM-01 with its scored class, rather than incorrectly pairing that score with the original P1 label. The evaluated engine and archived predictions remain unchanged.

## Runtime reproduction limit

The current browser build has fingerprint `1ce52f110ca7f043`; the archived v0.5 run records `e4ef11ac89758672`. A fingerprint includes source/data bytes and Python/scikit-learn/NumPy/SciPy versions. The old manifests did not store all those details, so exact reconstruction of their inference environment is not certified. Recomputing metrics from preserved predictions is different from reproducing inference. The audit records current versions and this mismatch; new freezes include the detailed provenance. No model-identity check was weakened to hide the difference.

## Commands

```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_review prototype.test_evaluation prototype.test_workflow -v
uv run --frozen --python 3.12 python -m prototype.audit_submission
```

Browser QA used a separate local server/database on port 8767 and invented demo tickets. The normal user's database was not used. The only evaluation-protocol grades produced by regression tests belong to clearly fictional temporary unit fixtures, not to project evidence.

## Historical verification

The material below is preserved as dated development history. Its pending-label statements describe November 12-15, before the recorded November 22 runs. Current product status is [no live assisted launch](../08_launch_memo.md); 100 additional references and actual user research remain human work.

# S4 engineering verification — updated 15 November 2026

These checks validate implementation behaviour. **They are not the independent product evaluation, human research, or measured handling-time savings.** No holdout predictions were produced.

## Historical verification — 15 November

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
