# Exposed-demo diagnostic: preserved baseline and post-fix run

**15 November 2026. Development evidence only; not independent evaluation or human grades.**

The model was deliberately corrected after viewing C01-C20. These cases are excluded from the official E001-E050 holdout. The reference bytes are identical in both runs; no expected answer was changed to improve agreement.

| Mechanical check | Baseline | After correction |
|---|---|---|
| Proposed severity agreement | 16/20 | 20/20 |
| Team agreement | 14/20 | 17/20 |
| Candidate source hit@3 | 15/20 | 20/20 |
| P1 detected | 6/8 | 8/8 |
| False P1 | 0/12 | 0/12 |
| Never lower | 20/20 | 20/20 |
| Customer isolation | 20/20 | 20/20 |

Baseline fingerprint: `41acde6fcf51b4c1`; post-fix: `e472b6a6d01222de`.
Post-fix execution: `2026-11-15T20:11:31.263838+00:00`. Both use the same provisional reference hash `91b8e3411768dd54cc38e5d4d94086923cb6bef49bbe89309ff515209746d7b8`.

## Changes tied to observed misses

- C03: flag a large outbound-volume anomaly as a possible incident. Require comparable units, a >=10x increase and >=50 GB final volume; skip explicit scheduled-backup/hypothetical context. This is not proof of exfiltration.
- C18: detect an explicitly suspected breach and keep the legal question for a human; in assisted mode a critical incident can raise severity without answering the legal question. Privileged-change requests remain blocked from automatic raising.
- C06/C08: capture interrupted detection alerts and production-blocking quarantine with exact ticket excerpts.
- C07/C14: bounded service-impact rules for a crashing awareness module and <=2% webhook event loss. These are provisional conventions to review, not calibrated statistical decisions.
- C01/C02/C08/C17/C20: bilingual topic aliases improve TF-IDF matching. The returned evidence stays the original scoped, versioned synthetic document, not the alias text.

## Remaining ownership disagreements

| Case | Provisional reference | Current suggestion |
|---|---|---|
| C09 | Platform | Reporting |
| C15 | Customer Success | Platform |
| C17 | Customer Success | Reporting |

C09 is a reports-page outage (Platform versus Reporting); C15 mixes administrator help and dashboard time zone; C17 is a cosmetic report-logo request. The team must agree ownership before freezing the model/references. No arbitrary routing rule was added solely to match these three provisional labels.

The perfect severity agreement and source-id hit rate on exposed examples do not establish generalisation, source usefulness, two-human acceptance, calibrated confidence or measured time savings. A source-id hit is a mechanical overlap, not proof of a correct fix. E001-E050 remain unlabelled/unpredicted by this diagnostic.

Evidence: [post-fix outputs](demo_diagnostic.json), [CSV](demo_diagnostic.csv), [original baseline](../demo_diagnostic.json).
