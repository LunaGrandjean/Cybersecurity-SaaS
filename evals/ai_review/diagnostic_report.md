# Diagnostic exploratoire - 15 novembre 2026

> Diagnostic historique du 15 novembre. Les evaluations du 22 novembre et la decision actuelle figurent dans [report_v0.md](../report_v0.md) et [08_launch_memo.md](../../08_launch_memo.md). Les mentions de travail en attente ci-dessous concernent uniquement cette execution initiale.

**Comparaison automatique sur les 20 cas de demonstration deja exposes. Aucun grade humain.**

Les references proviennent du brouillon de Jane, avec une adaptation structuree proposee par IA avant execution. Elles restent a verifier. Les desaccords de routage peuvent notamment traduire une convention d'equipe encore ambigue.

| Mesure automatique | Compte | Taux |
|---|---|---|
| Accord de severite avec la reference | 16/20 | 80% |
| Accord de routage avec la reference | 14/20 | 70% |
| Au moins une source candidate attendue dans le top 3 | 15/20 | 75% |
| P1 reconnus dans la suggestion | 6/8 | 75% |
| Fausses suggestions P1 sur les references non-P1 | 0/12 | 0% |
| Priorite declaree jamais abaissee automatiquement | 20/20 | 100% |
| Sources du meme client ou generiques uniquement | 20/20 | 100% |

Ces taux ne sont ni le critere officiel des 62% acceptes par deux personnes, ni un gain de temps mesure, ni une garantie de generalisation.

## Trois categories de desaccord constatees

| Categorie | Cas | Composant a examiner |
|---|---|---|
| Routage different de la reference (6/20) | C03, C09, C15, C17, C18, C19 | routing / convention de responsabilite |
| Source candidate attendue absente du top 3 (5/20) | C01, C02, C08, C17, C20 | retrieval / couverture documentaire |
| Severite differente de la reference (4/20) | C03, C07, C14, C18 | classifier / regles de securite |

Les categories se recouvrent : un ticket peut avoir plusieurs desaccords.

## P1 a traiter en priorite

- **C03 : P1 attendu, P4 suggere, P4 effectif.** Le transfert sortant de 2 Go a 140 Go vers une destination nouvelle n'est pas reconnu comme un signal possible d'exfiltration. Le classement declare P4 est conserve : la regle ne-jamais-baisser ne protege pas contre une urgence initialement sous-declaree.
- **C18 : P1 attendu, P4 suggere, P1 effectif conserve.** La demande melange possible fuite de donnees et question juridique. La gravite technique est manquee, mais la priorite P1 declaree est conservee et le dossier part en verification humaine. Ne pas confondre suggestion erronee et baisse de priorite effective.

## Detail des 20 cas

| Cas | Reference | Suggestion | Effective | Equipe reference | Equipe proposee | Source attendue trouvee |
|---|---|---|---|---|---|---|
| C01 | P1 | P1 | P1 | Incident Response | Incident Response | non |
| C02 | P1 | P1 | P1 | Incident Response | Incident Response | non |
| C03 | P1 | P4 | P4 | Incident Response | Human triage | oui |
| C04 | P1 | P1 | P1 | Identity | Identity | oui |
| C05 | P1 | P1 | P1 | Platform | Platform | oui |
| C06 | P1 | P1 | P3 | Platform | Platform | oui |
| C07 | P2 | P4 | P2 | Awareness module | Awareness module | oui |
| C08 | P1 | P1 | P1 | Detection Engineering | Detection Engineering | non |
| C09 | P2 | P2 | P2 | Platform | Reporting | oui |
| C10 | P2 | P2 | P2 | Identity | Identity | oui |
| C11 | P3 | P3 | P3 | Reporting | Reporting | oui |
| C12 | P3 | P3 | P2 | Endpoint | Endpoint | oui |
| C13 | P3 | P3 | P2 | Detection Engineering | Detection Engineering | oui |
| C14 | P3 | P4 | P3 | Integrations | Integrations | oui |
| C15 | P4 | P4 | P4 | Customer Success | Platform | oui |
| C16 | P4 | P4 | P4 | Account Management | Account Management | oui |
| C17 | P4 | P4 | P3 | Customer Success | Reporting | non |
| C18 | P1 | P4 | P1 | Incident Response | Human triage | oui |
| C19 | P2 | P2 | P1 | Identity | Human triage | oui |
| C20 | P3 | P3 | P3 | Network | Network | non |

## Provenance et integrite

- Version du modele : `41acde6fcf51b4c1`.
- References adaptees enregistrees avant prediction, SHA-256 : `91b8e3411768dd54cc38e5d4d94086923cb6bef49bbe89309ff515209746d7b8`.
- Execution reelle : `2026-11-15T18:34:07.491911+00:00`.
- Evaluateurs humains : aucun. Aucun nom de Jane, Malek ou Luna n'est utilise comme auteur d'un grade.
- Les 50 cas E001-E050 n'ont pas ete executes ici. Leur fichier canonique reste sans reponses attendues.
- Aucune correction du moteur n'a ete faite apres observation de ces resultats.

Les sorties completes sont dans `demo_diagnostic.json`; le tableau filtrable est dans `demo_diagnostic.csv`.
