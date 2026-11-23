# spec.md - executable spec - SLA-aware triage copilot - v2

**Updated 23 November 2026.** This describes evaluated engine v0.5 and the final console. Two recorded evaluations exist; both fail the launch criterion. [Final decision](08_launch_memo.md): no live assisted launch. EVAL-01 to EVAL-05 are implemented; EVAL-06 to EVAL-09 remain future requirements, not evaluated fixes.

## problem
Support engineers need severity, contractual response deadlines and reusable diagnostic sources in one console. P7 supplies 400 accounts, 6,000 tickets/month and 25 engineers. The 240 annual breaches, 33-minute handling time, 12-minute triage split and financial gains are assumptions/estimates, not measured prototype results. The >=62% routine-acceptance proxy depends on those timing assumptions; the >=17% real handling-time saving still needs a timed comparison.

## user_workflow
1. Enter an invented ticket: account, declared priority, language, timezone-aware creation time, text/logs.
2. Redact before inference, retrieval or persistence; keep no reversible mapping.
3. Look up the synthetic account SLA. Unknown account: abstain, flag unverified contract, use a clearly provisional clock.
4. TF-IDF + class-weighted logistic regression proposes a severity; contextual safety rules may override to P1 and bounded service-impact rules to P2/P3, using an exact normalised ticket excerpt.
5. Retrieve up to 3 reusable sources, minimum cosine similarity 0.08, scoped to the same customer or generic KB; bilingual topic aliases enrich the search index only.
6. Apply human-review gates and the global mode. Default `suggestions`: never change priority. In the v0.5 synthetic `assisted` demonstration, an eligible higher proposal raises even below score 0.70; review is still required. Never lower. Live assisted use is not approved.
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

The classifier score is an **uncalibrated model output for classifier_severity**, not 'how often the final decision is right'. Safety-rule decisions have separate evidence; they do not inherit a calibrated percentage. The 0.70 review threshold is provisional; in v0.5 it adds a review reason but no longer blocks an eligible assisted raise. Templates/AI-proposed training labels must be reviewed and do not establish generalisation.

## edge_cases_and_fallbacks
- Fewer than six words, unsupported language or unknown account: classifier abstains, preserves declared priority and requires human triage.
- Low classifier score: show why review is needed. In v0.5 a higher proposal can still raise in assisted mode; this is a synthetic demonstration policy, not permission for live use.
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
- Training: 300 synthetic rows, 70/75/90/65, 40 families; human label review is still pending.
- Exposed development material: six UI tickets, Jane's original 20 examples, regression inputs and the 100 cases already evaluated.
- Recorded runs: 50 reviewed cases in `eval_set_v0.csv` and 50 additional cases in `eval_set_v1_fresh.csv`; original manifests, predictions and grades are preserved.
- The second batch's inputs were visible to the developer, and main grading used LLM-prefilled sheets. Do not claim a fully blind independent study. Luna confirmed her actual review of grading sheets bearing her name on 23 November.
- E101-E200 in `eval_set_v2_candidates.csv` are additional INPUT candidates only. Semantic overlap review and expected answers are required before prediction; no human signatures are generated.
- Freeze labels and model before a new run. A later tuned version requires fresh cases. The engine never reads evaluation files during training or interactive inference.
- Hash checks allow only LF/CRLF conversion for historical Windows/Git files. Changes to labels, JSON content, whitespace beyond line-ending conversion or the model still fail the appropriate checks.
- `summarise --check-only` recomputes existing results without modifying recorded metrics. The final audit additionally checks counts, source/customer isolation and preservation of original evidence.
- Passing engineering checks does not satisfy the product criterion or measure time saving. Latest routine acceptance is 9/22 and P1 recall 9/14; both fail their gates.

## done_criteria
- >=62% of human-labelled P3/P4 cases accepted unchanged by BOTH human graders, including correct severity/team and >=1 relevant source. Abstentions stay in the denominator.
- P1 recall =100% on the finite human-labelled holdout; abstention is not a successful detection. This is not a guarantee for production.
- False-P1 rate <=15% of human-labelled non-P1 cases, reported with numerator/denominator.
- Redaction, customer isolation, never-lower, original SLA timestamps, takeover and global-switch engineering checks pass.
- Product verdict is not_met on both recorded runs. A new launch decision requires a genuinely independent human-reviewed evaluation that meets the first three criteria; engineering tests cannot substitute.

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
| EVAL-05 | The team is left to "Human triage" while the expected team is clear (9 cases graded on routing; 31/50 outputs are Human triage, 24 of them where a named team was expected) | routing | The routing table covers Platform, Detection Engineering, Integrations, Reporting and Customer Success topics; "Human triage" only when the expected action requires a person to choose; team accuracy ≥ 70 % |

### After the fresh run v0.5 (`evals/runs/v1_fresh`, 22 November 2026)

| Id | Observed miss (cases) | Component | Testable requirement |
|---|---|---|---|
| EVAL-06 | Real P1s of attack types absent from training and rules: sensor tampering, API-key misuse, detection disabled fleet-wide, uncontrolled remote session, credential dumping (E054, E055, E058, E062, E064) | classifier | Any ticket mentioning a security control being removed or disabled, a credential or key used from an unknown origin, or an attacker tool or remote access the customer does not control, proposes **P1** and hands over; P1 recall = 100 % on the **next fresh** labelled set, not on these cases |
| EVAL-07 | P3 tickets over-escalated to P2/P1 when a workaround or mitigation is stated (E065, E066, E071, E075, E080, E083, E085) | classifier | Stated workaround or mitigation ("still protected", "workaround", "other sites work") caps a classifier proposal at P3 unless a safety rule fires |
| EVAL-08 | P1 incidents routed to the component team instead of Incident Response (E051, E053, E057, E060, E063) | routing | A P1 from a compromise rule always routes to Incident Response; component teams only for P1 outages without compromise |
| EVAL-09 | Correct triage, but no cited source addresses the ticket's component (E059, E068, E070, E077, E088) | retrieval | Sources are filtered to the routed team's KB articles first; source hit@3 ≥ 80 % on the next fresh set |

## out_of_scope
Customer-facing chatbot, customer messages, remediation, autonomous lowering, production identity/access control, external inference API, fine-tuning, other languages, auto-closing and automatic cross-customer incident merging.

## Exposed-demo diagnostic — 15 November 2026
These observations come from a real automatic run on the 20 already exposed demo references. They are not two-person grading or independent holdout results. This is the historical pre-fix observation table; the implemented corrections are listed under DEV-01 to DEV-06 below. It does not describe current run status.

| Observation / cases | Next requirement |
|---|---|
| Severity disagreement in C03, C07, C14, C18 (4/20) | Review severity features and add separate development regressions. C03's abnormal outbound volume must trigger security review; a calm tone or a declared P4 cannot suppress that signal. Do not invent destination approval status. For C18, separate the possible incident's urgency from the human-only legal request. Preserve the recorded baseline. |
| Team-reference disagreement in C03, C09, C15, C17, C18, C19 (6/20) | First agree on ownership conventions, especially Platform vs Reporting and Customer Success vs specialist teams. Then test routing against those approved conventions; do not declare every provisional-reference disagreement a routing bug. |
| Candidate expected source absent in C01, C02, C08, C17, C20 (5/20) | Review actual source relevance, corpus coverage and retrieval before changing thresholds. Return no troubleshooting rather than an irrelevant fix; preserve customer isolation. |

In the initial diagnostic, C03 missed proposed P1 and kept effective P4; C18 missed proposed P1 while preserving effective P1. Evaluate both proposed severity and effective priority so a safety rule is not mistaken for successful classification. Preserved initial outputs and provenance: `evals/ai_review/demo_diagnostic.json`; corrections are recorded below.

The first official run was completed on reviewed references on 22 November. Its original evidence is preserved. New cases must be human-reviewed before inference and graded according to the documented protocol; generated references alone do not satisfy that requirement.

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

## Finalisation requirements implemented 23 November
- PORT-01: legacy frozen files may differ only by Windows/Git LF/CRLF conversion; all other content changes are rejected. Preserve old manifests and outputs.
- AUDIT-01: a check-only summary and submission audit recompute recorded results without predictions or overwriting evidence. Product failure remains visible.
- UI-01: when CALM-01 selects a non-P1 class, label the displayed score with the scored class, not the original P1 class. This corrects display semantics without changing the evaluated engine or its predictions.
- DOC-01: final brief, launch decision and current governance distinguish delivered synthetic functionality, proposed production tooling and remaining human work.
