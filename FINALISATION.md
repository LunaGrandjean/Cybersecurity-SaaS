# Finalisation du projet au 23 novembre 2026

Le prototype local et les livrables ecrits sont consolides. La decision actuelle est **pas de lancement en mode assiste sur des tickets reels** : dernier rappel P1 9/14, acceptation courante 9/22. Le rendu peut expliquer ce non-lancement sans presenter les objectifs comme atteints.

## Travail termine dans le depot

| Element | Etat |
|---|---|
| Brief final | `product_brief.md`, perimetre reel, resultats et limites |
| Memo S8 | `08_launch_memo.md`, decision et conditions de reexamen |
| Architecture et spec | Comportement v0.5, checkpoints, mode de demonstration et exigences futures distingues |
| S5 et S6-S7 | Metriques actualisees ; experience et outils de production presentes comme projets |
| Gouvernance S8 | Non-lancement, roles proposes, donnees et limites de preuve |
| Anciennes pages | Conservees comme historique avec renvoi vers les resultats actuels |
| Integrite | Runs, notes, references, moteur et donnees d'origine conserves ; tolerance uniquement LF/CRLF pour les empreintes historiques |
| Verification | Suite de regression, recalcul sans ecriture des deux runs, controle du parcours dans Edge ; preuves dans `evals/finalisation_2026_11_23/` |
| Grilles de Luna | Confirmation personnelle recueillie le 23 novembre, avec empreintes des fichiers concernes |
| Objectif de volume | 100 cas supplementaires E101-E200 prepares sans etiquettes ni predictions |
| Oral et demo | Parcours et points a expliquer dans `ORAL_DEMO.md` |

Les corrections proposees des 100 nouveaux cas sont preparees dans `evals/ai_review/proposed_labels_v2.csv`. Les champs humains y restent vides ; la relecture porte aussi sur la validite de chaque proposition.

## Travail humain encore necessaire

1. Relire, dedoublonner semantiquement et annoter E101-E200 avant toute prediction. Il y a 200 entrees candidates au total, mais seulement 100 references renseignees. Ne pas annoncer 200 cas valides/evalues.
2. Pour une nouvelle conclusion independante, geler ces nouvelles references et le modele, executer une fois puis faire noter chaque sortie par deux personnes. Les cas deja exposes servent au developpement/regression, pas a une nouvelle preuve de generalisation.
3. La recherche S3 reste du role-play prepare. De vraies observations, une mesure de temps et la revue des etiquettes d'entrainement/sources sont necessaires avant de pretendre a un pilote valide.
4. Faire la revue finale en equipe et les commits sous les vrais comptes. Verifier avec l'enseignant la demande de quatre auteurs pour une equipe de trois, le starter absent et les attentes de volume. Aucun auteur ou exercice n'est invente.
5. Pousser apres revue et creer le tag `v1.0` sur le commit final approuve, avant l'oral selon la consigne. Aucun tag ni depot externe n'a ete publie par cette finalisation.

Les approbations du Head of Support et du DPO, la collecte de donnees reelles, l'authentification, la supervision et le deploiement ne sont pas fournis par un document de projet. Leurs roles sont definis pour un futur fonctionnement, pas attribues a de vrais responsables de production.

## Controle reproductible

Depuis la racine du projet :

```powershell
uv run --frozen --python 3.12 python -m unittest prototype.test_review prototype.test_evaluation prototype.test_workflow -v
uv run --frozen --python 3.12 python -m prototype.audit_submission
```

L'audit recompute les deux evaluations sans nouvelles predictions et sans remplacer les metriques conservees. Un succes d'integrite ne signifie pas que le produit atteint ses seuils ni que les 100 nouveaux cas sont relus.

[Decision finale](08_launch_memo.md) | [Brief final](product_brief.md) | [Resultats](evals/report_v0.md) | [Relecture restante](evals/VALIDATION_EQUIPE.md)
