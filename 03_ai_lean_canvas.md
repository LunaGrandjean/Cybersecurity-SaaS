# 03 — AI Lean Canvas · SLA-aware triage copilot

> One screen. Nine classic blocks (Ash Maurya) + five blocks an AI product cannot skip.

## The nine classic blocks
| Block | Our answer | Comes from |
|---|---|---|
| 1. Problem — top 3 pains | ~12 of 33 min per ticket spent on triage · ~240 SLA breaches a year at ~€2,000 · disguised P1s (calm tone) get the wrong priority | 01 · 02 |
| 2. Users / customer segments | 25 L2 support engineers · 400 enterprise client accounts with 1 h (P1) and 4 h (P2) SLAs | 01 (persona) |
| 3. Unique value proposition | Every ticket arrives already triaged — severity, SLA clock and the closest past fixes — and the agent can raise the alarm, never lower it | 01 (press release) |
| 4. Solution — the MUST features | SLA and tier lookup · severity proposal with "never lower" rule · log redaction · top-3 similar resolved tickets | 03 brief §3 |
| 5. Channels — where it lives | A side panel in the ticketing console the engineers already use | 03 brief §6 |
| 6. Value — per year | Internal product: base €152k net in year 1 · expected value ≈ €133k vs €112k do-nothing and €100k hurdle → conditional go | 02 |
| 7. Cost structure | Tokens (~€4.5k) · integration (€100k, amortised over 3 years) · evaluation (€20k) · supervision (0.5 FTE, €45k) · monitoring (€20k) · re-evaluation (3 × €5k) · error cost (~€26k) | 02 |
| 8. Key metric | ≥ 62 % of P3/P4 triages accepted unchanged by two graders, and no P1 proposed below P1 | 03 brief §7 |
| 9. Unfair advantage | Our own resolved-ticket history and client contract/SLA data — no vendor has them | 02 (build / buy: orchestrate) |

## The five AI blocks
| Block | Our answer | Comes from |
|---|---|---|
| 10. Data | Synthetic tickets from public material, labelled by hand · production: our tickets under the client DPA · gaps: languages beyond EN/FR, new attack types | governance.md · S3 |
| 11. Model | Rules (SLA lookup, redaction, P1 keywords) + classical ML (severity classifier, TF-IDF retrieval) → hybrid; no LLM in v0 | 03 brief §5 |
| 12. Evaluation | `evals/eval_set_v0.csv`: 20 cases now → 200 by Session 5, P1s oversampled, two graders | evals/ |
| 13. Human in the loop | L4 to raise a severity · person only to lower · L1 suggestions · nothing reaches the client without an engineer · "Take over" on every decision | 03 brief §2 |
| 14. Risks & governance | Never lower a severity, never send raw logs outside · rollback: any P1 proposed below P1, or false P1 > 20 % in a week → back to L1 within the hour | governance.md |
