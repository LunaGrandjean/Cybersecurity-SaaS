# spec.md - executable spec - SLA-aware triage copilot - v2

**S4 implementation: 12 November; corrected 15 November 2026.** This describes the code in `/prototype`.
The independent product evaluation and two-person grading have not yet taken place.

## problem
Support engineers need severity, contractual response deadlines and reusable diagnostic sources in one console. P7 supplies 400 accounts, 6,000 tickets/month and 25 engineers. The 240 annual breaches, 33-minute handling time, 12-minute triage split and financial gains are assumptions/estimates, not measured prototype results. The >=62% routine-acceptance proxy depends on those timing assumptions; the >=17% real handling-time saving still needs a timed comparison.

## user_workflow
1. Enter an invented ticket: account, declared priority, language, timezone-aware creation time, text/logs.
2. Redact before inference, retrieval or persistence; keep no reversible mapping.
3. Look up the synthetic account SLA. Unknown account: abstain, flag unverified contract, use a clearly provisional clock.
4. TF-IDF + class-weighted logistic regression proposes a severity; contextual safety rules may override to P1 and bounded service-impact rules to P2/P3, using an exact normalised ticket excerpt.
5. Retrieve up to 3 reusable sources, minimum cosine similarity 0.08, scoped to the same customer or generic KB; bilingual topic aliases enrich the search index only.
6. Apply human-review gates and the global mode. Default `suggestions`: never change priority. In `assisted`, an eligible model score >=0.70 or separately matched contextual rule may raise but never lower.
7. Engineer can take over, change priority/team with a reason, record verification and accept. P1/P2, lowering, weak confidence, unsupported input and missing sources require review. Taking over never removes manual controls.
8. Persist only the redacted ticket, analysis, engineer actions and global setting in local SQLite. No customer-send or remediation endpoint exists.

## io_contracts
```text
ticket: {account_id, title?, text, logs?, declared_priority: P1|P2|P3|P4,
         language: en|fr|other, created_at?: ISO8601 with timezone}
triage: {proposed_severity: P1|P2|P3|P4|null, effective_priority,
         classifier_severity, classifier_score: number|null, method,
         reason, evidence[{rule,source,quote}], requires_human,
         review_reasons[], team, similar[{id,title,text,score,account_id,version,source}],
         redacted_text, redaction:{count,types}, sla_deadline, sla_minutes,
         created_at, contract_verified, model_version, mode}
```
Text length 1-20,000; request body <=65,536 bytes. Unsupported priorities, malformed dates and future creation times are rejected. All API calls use JSON and same-origin requests. The local demo's self-declared operator string is an audit convenience, not authentication.

## endpoints
- `GET /api/health`: model/data version and training count.
- `GET /api/state`: redacted persisted tickets, mode, synthetic accounts and teams.
- `POST /api/triage`: analyze and store a new ticket; no raw text persisted.
- `POST /api/action`: take_over, review, change or accept; server-enforced verification and reason gates.
- `POST /api/switch`: persist suggestions/assisted mode, operator, reason and timestamp.
- `POST /api/demo`: load six exposed fixtures; never used as holdout evidence.
- `GET /api/audit`: export structured audit events.

## model_and_score
TF-IDF unigrams/bigrams, accent stripping, sublinear term frequency; logistic regression with balanced class weights, C=4, seed 17. Fit only on `prototype/data/training_tickets.csv`. Retrieval has a separate TF-IDF index over 15 synthetic approved-status fixtures plus versioned bilingual search aliases in `engine.py`. Aliases are not source passages or ticket facts. Inference makes no network calls.

The classifier score is an **uncalibrated model output for classifier_severity**, not 'how often the final decision is right'. Safety-rule decisions have separate evidence; they do not inherit a calibrated percentage. The 0.70 threshold is provisional, fixed before holdout exposure. Templates/AI-proposed training labels must be reviewed and do not establish generalisation.

## edge_cases_and_fallbacks
- Fewer than six words, unsupported language or unknown account: classifier abstains, preserves declared priority and requires human triage.
- Low classifier score: no classifier-driven auto-raise; show why review is needed. A contextual safety rule can independently raise in assisted mode.
- No reusable source: show no match; do not invent a troubleshooting step; require engineer review.
- Possible privileged-access change or legal request: human-only; never execute access changes or produce legal advice.
- A customer declaring P1 when the model suggests P3: effective priority remains P1 until a reasoned engineer change.
- Bare urgent/capital letters are not severity rules. Negated or hypothetical attack descriptions must not alone trigger a safety rule.
- Rule evidence must come from the actual input. Never invent a time, telemetry result or change-window check.
- Account isolation filters retrieval results, including matches with high similarity. Only generic KB can be shared.
- Mask recognised IPv4/IPv6, e-mail, phone, dotted-hostname and credential patterns. Regex has known gaps (e.g. arbitrary usernames, unusual secret formats); this is not certified DLP. Synthetic data only.
- Model error: HTTP 503, manual-triage instruction, no automatic ticket mutation.
- API down: show connection error. No production ticketing integration or queued background action is present.

## sla_and_override
Deadlines are `original created_at + effective priority contract duration`. They never restart on a raise, a downgrade, page reload or takeover. P1=60 and P2=240 minutes come from P7; P3=1440 and P4=4320 are explicit demo decisions. Both demo tiers currently share those durations, configurable per synthetic account.

Global suggestions mode blocks new automatic raises and requires human verification before accepting existing tickets. It preserves previous raised priorities and engineer decisions. Changes are persisted in SQLite and audited. Operational owner in the design: Head of Support; local access is unauthenticated, loopback-only. Team sign-off of the switch is pending.

## evaluation_protocol
- Training: 300 synthetic rows; P1 70 / P2 75 / P3 90 / P4 65; 40 families. Labels are AI proposals pending human review.
- Demo: six UI tickets + Jane's original 20 exposed cases (`evals/demo_reference_v0.csv`) + regression tests.
- Holdout: 50 new INPUTS in `evals/eval_set_v0.csv`. Expected labels, names and dates remain blank until humans fill them. No predictions have been produced for them.
- `validate` checks required human annotation, family ids and exact text overlap. Human semantic leakage review is still required.
- `freeze` hashes expected answers and model/data before inference; `run` refuses an altered/unlabelled run.
- Two graders independently judge every output; original grades and disagreements remain preserved. `summarise` never fabricates grades or time savings.
- Do not tune on holdout outputs. Keep the original run and use a fresh holdout for a changed model.

## done_criteria
- >=62% of human-labelled P3/P4 cases accepted unchanged by BOTH human graders, including correct severity/team and >=1 relevant source. Abstentions stay in the denominator.
- P1 recall =100% on the finite human-labelled holdout; abstention is not a successful detection. This is not a guarantee for production.
- False-P1 rate <=15% of human-labelled non-P1 cases, reported with numerator/denominator.
- Redaction, customer isolation, never-lower, original SLA timestamps, takeover and global-switch engineering checks pass.
- Product verdict remains pending until the human-labelled and independently graded run exists. Engineering tests alone never satisfy the first three criteria.

## changes_since_skeleton
These were found during inspection/development, BEFORE holdout execution. They must not be presented as the three most frequent evaluation misses.

| Observation | v2 requirement / implementation |
|---|---|
| Six hard-coded decisions could not triage unseen input | New-ticket API + reproducible local classifier and retrieval |
| Model score described as empirical certainty | Display uncalibrated score with its own classifier label; rule evidence separate |
| Claimed 23:14/change-window evidence absent from the displayed ticket | Only actual matched text can be rule evidence; source documents are inspectable |
| Low-confidence ticket could be accepted without explicit checking | API and UI require recorded verification |
| Takeover hid all priority controls | Manual priority/team controls remain accessible |
| Only in-memory logs and no global override | Persistent SQLite audit + suggestions-mode switch; no rollback downgrade |
| Eval directory nested and demo cases reused as tests | Canonical `evals/` path; original examples archived as exposed demo; new candidates unlabelled |
| C19 in original CSV appeared to allow P1 -> P2 automatically | Preserve original reference; new policy distinguishes proposed and effective severity |
| Data/train-label/sign-off claims exceeded available evidence | All synthetic origins, AI-proposed labels and simulated source approvals explicitly marked |

## post_eval_misses
*Added 22 November 2026 from run `evals/runs/v0` (see `evals/report_v0.md` §2). The original run is preserved.*

| Id | Observed miss (cases) | Component | Testable requirement |
|---|---|---|---|
| EVAL-01 | Real P1s proposed as P3/P4: recovery-address takeover, retained contractor admin access, cross-tenant data exposure (E003, E012, E015) | classifier | Account takeover, privileged access kept after offboarding, and any cross-tenant data visibility propose **P1** and require a human; P1 recall = 100 % on the next frozen set |
| EVAL-02 | False P1 on contained, test, planned-exercise or documentation tickets (E035, E039, E049, E050; E004, E017, E024 at P2) | classifier | Explicit "no incident", "test", "planned exercise" or documentation-only wording cannot produce P1 unless an active-compromise signal is also present; false-P1 rate ≤ 15 % |
| EVAL-03 | A severity is proposed on ABSTAIN cases: vague ticket, attachment only, legal request, another customer's data, prompt injection, unverified authority (E041, E042, E045–E048) | classifier / policy | These patterns return `proposed_severity = null` (ABSTAIN), keep the declared priority and hand the ticket to a person; 8/8 ABSTAIN cases abstain |
| EVAL-04 | Effective priority stays at the declared priority even when the proposed severity is higher (16 cases, e.g. E007 and E011, expected P1, left at P4) | sla / rules | In assisted mode, when proposed severity > declared priority, `effective_priority` = proposed severity and `auto_raised = true`, logged in the audit; never lower |
| EVAL-05 | The team is left to "Human triage" while the expected team is clear (9 cases; 26/50 outputs are Human triage overall) | routing | The routing table covers Platform, Detection Engineering, Integrations, Reporting and Customer Success topics; "Human triage" only when the expected action requires a person to choose; team accuracy ≥ 70 % |

## out_of_scope
Customer-facing chatbot, customer messages, remediation, autonomous lowering, production identity/access control, external inference API, fine-tuning, other languages, auto-closing and automatic cross-customer incident merging.

## Exposed-demo diagnostic — 15 November 2026
These observations come from a real automatic run on the 20 already exposed demo references. They are not two-person grading or independent holdout results. Requirements below are for a next version and are **not yet implemented**.

| Observation / cases | Next requirement |
|---|---|
| Severity disagreement in C03, C07, C14, C18 (4/20) | Review severity features and add separate development regressions. C03's abnormal outbound volume must trigger security review; a calm tone or a declared P4 cannot suppress that signal. Do not invent destination approval status. For C18, separate the possible incident's urgency from the human-only legal request. Preserve the recorded baseline. |
| Team-reference disagreement in C03, C09, C15, C17, C18, C19 (6/20) | First agree on ownership conventions, especially Platform vs Reporting and Customer Success vs specialist teams. Then test routing against those approved conventions; do not declare every provisional-reference disagreement a routing bug. |
| Candidate expected source absent in C01, C02, C08, C17, C20 (5/20) | Review actual source relevance, corpus coverage and retrieval before changing thresholds. Return no troubleshooting rather than an irrelevant fix; preserve customer isolation. |

In the initial diagnostic, C03 missed proposed P1 and kept effective P4; C18 missed proposed P1 while preserving effective P1. Evaluate both proposed severity and effective priority so a safety rule is not mistaken for successful classification. Preserved initial outputs and provenance: `evals/ai_review/demo_diagnostic.json`; corrections are recorded below.

The first official test still requires human validation of E001–E050 before inference and two independent human graders after inference. AI-proposed references in `evals/ai_review/proposed_labels_v0.csv` do not satisfy that requirement.

## v2 changes implemented after the exposed-demo baseline — 15 November

The miss table above describes the **initial** diagnostic. Preserve it as evidence; do not substitute development results for the independent evaluation. Current evidence: [comparison](evals/ai_review/post_fix_2026_11_15/comparison.md).

| Requirement added from observed development misses | Implementation / limit |
|---|---|
| DEV-01: a calm but very large outbound-volume increase must surface a possible incident | SEC-08 requires outbound direction, comparable GB/TB/Go/To units, >=10x increase and >=50 GB final volume. Explicit planned-backup/hypothetical clauses do not alone trigger it. Requires engineer investigation; never assert theft. Regex cannot resolve all backup/context ambiguity. |
| DEV-02: a suspected breach must retain incident urgency when combined with a legal question | SEC-05 proposes P1 with actual ticket excerpt. Assisted mode may raise while legal handling remains human-only. Privileged-change requests still block automatic raising. Suggestions mode still blocks every automatic raise. |
| DEV-03: missing detection alerts and production-blocking quarantine need an explicit safety route | SEC-06/07 propose P1 with scoped evidence and engineer review, rather than relying on a low classifier score. |
| DEV-04: distinguish a broken simulation module from a routine how-to, and limited connector loss from major loss | SCOPE-01 proposes P2 for a crashing phishing-simulation module. SCOPE-02 proposes P3 for explicitly <=2% SIEM/webhook event loss. Never lower declared urgency. These are provisional operational conventions, not universal severity guarantees. |
| DEV-05: retrieve a relevant generic topic even across EN/FR vocabulary gaps | Versioned bilingual aliases augment TF-IDF search; returned text remains the actual scoped synthetic document. Source-id hit is not a human relevance judgment. |
| DEV-06: review imports must not invent validation or alter input incidents | Require explicit accept/correct, real reviewer name/time, correction explanation and valid expected fields for every row. Reject changed original inputs and existing output files; never run inference during import. Presence of fields alone cannot attest genuine review. |

Regression evidence includes EN/FR volume anomalies, modest growth, planned backups, hypothetical/negated incidents, mixed legal requests, percentage boundaries, source isolation and review-import rejection. The post-fix exposed-demo run has 20/20 severity agreement and 8/8 proposed P1s, but **is not independent**. C09 Platform/Reporting, C15 mixed admin/dashboard help and C17 report-logo ownership remain provisional routing disagreements for the team to settle before freeze. No rule was added just to match those three reference teams.
