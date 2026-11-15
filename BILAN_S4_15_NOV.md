# Bilan S4 — 15 novembre 2026

**Etat : prototype fonctionnel et documents prepares ; validation humaine et rendu Git a terminer.** Aucun grade ni entretien n'a ete attribue fictivement a Jane, Malek ou Luna.

## Ce qui est fait
| Element | Etat reel |
|---|---|
| Maquette de Jane | Version v0.2 conservee, HTML et image d'origine preserves |
| Prototype S4 local | Nouveaux tickets, classification, regles de priorite, SLA, recherche de sources, correction humaine, reprise en main, mode suggestions uniquement et journal SQLite |
| Donnees d'entrainement | 300 tickets synthetiques, repartition P1 70 / P2 75 / P3 90 / P4 65 ; etiquettes proposees par IA, a relire |
| Cas de test officiels | 50 entrees preparees, distinctes de l'entrainement ; pas de predictions executees dessus par le diagnostic |
| Aide a la correction | 50 propositions remplies dans [le CSV IA](evals/ai_review/proposed_labels_v0.csv), avec justifications et incertitudes. Champs humains vides |
| Verification technique | 29 tests de code/API/protocole/import et 16 controles dans Edge passes le 15 novembre ; ce ne sont pas des notes produit |
| Diagnostic exploratoire | Diagnostic initial conserve et nouvelle execution apres correction sur les 20 exemples exposes, avec les memes references provisoires |
| Import de relecture | Commande qui exige les decisions, noms et dates reels, refuse les entrees modifiees et produit un nouveau CSV sans lancer de prediction |
| Documents | Architecture, spec v2, gouvernance S4, guide de lancement, protocole et rapport avec statut honnete |

## Ce que montre le diagnostic de demo
| Comparaison automatique avec une reference provisoire | Initial | Apres correction |
|---|---|---|
| Accord de priorite proposee | 16/20 | 20/20 |
| Accord d'equipe | 14/20 | 17/20 |
| Source candidate attendue dans le top 3 | 15/20 | 20/20 |
| P1 reconnus dans la suggestion | 6/8 | 8/8 |
| Fausses suggestions P1 sur les non-P1 de reference | 0/12 | 0/12 |
| Priorite declaree jamais abaissee automatiquement | 20/20 | 20/20 |
| Sources limitees au client ou a la KB generique | 20/20 | 20/20 |

Ces taux portent sur des cas deja exposes et des references non certifiees. Ils ne prouvent pas les 62% de triages acceptables par deux personnes, ni les 17% de temps reellement gagne.

**Corrections techniques faites :** C03 signale maintenant un possible incident et passe de P4 a P1 en mode assiste ; C18 propose P1 tout en laissant le traitement juridique a un humain. Les interruptions d'alertes, quarantaines bloquant la production et incidents de module sont mieux pris en compte. Les alias de recherche EN/FR ameliorent les sources retrouvees. Ces corrections ont utilise les exemples exposes : leur reussite ne prouve pas une performance sur de nouveaux cas. Trois desaccords de routage restent a arbitrer : C09 (Platform/Reporting), C15 (aide admin et fuseau horaire), C17 (logo de rapport).

Voir [la comparaison avant/apres et les limites](evals/ai_review/post_fix_2026_11_15/comparison.md). Les attentes du diagnostic initial n'ont pas ete modifiees.

## Ce qu'il reste a faire, dans l'ordre
1. **Relire les references et les donnees d'entrainement.** Les propositions IA sont une aide, pas une validation automatique. Traiter les notes `ai_uncertainty` et fixer les conventions de gravite/equipe.
2. **Valider humainement les 50 corrections avant le premier test.** Repartition proposee : Jane E001–E017, Malek E018–E034, Luna E035–E050. Suivre [le guide equipe](evals/VALIDATION_EQUIPE.md) : decision accept/correct, nom et date reels, puis import controle sans prediction.
3. **Geler puis executer les 50 cas**, avec `prototype.evaluate freeze` puis `run`, apres validation des references et du modele. Les 50 cas officiels n'ont pas servi aux corrections techniques.
4. **Deux personnes notent independamment les memes 50 sorties.** Par exemple Jane remplit `grading_a.csv`, Malek `grading_b.csv`, Luna coordonne les desaccords. Ce sont des roles proposes, pas des actions deja effectuees. Chacun des deux evaluateurs note les 50 cas.
5. **Calculer et reporter les vrais resultats**, via `summarise`, puis remplir le rapport et les lignes de spec correspondant aux echecs observes. Un resultat insuffisant doit rester visible.
6. **Tester vous-memes le bouton d'arret**, renseigner qui l'a teste et quand. Les controles techniques automatiques ne remplacent pas votre verification.
7. **Faire vos commits et pousser sur Git** pour le rendu du 15 novembre a 23 h 59. Les fichiers ajoutes/modifies sont encore dans le dossier de travail local.

Autres points du cours : les entretiens S3 restent declares simules dans le depot ; le starter Paylio n'est pas present parmi les supports locaux et son execution n'est pas attestee. La consigne mentionne quatre auteurs pour une equipe de trois : demander la modalite applicable sans inventer un auteur.

## Fichiers utiles
- [50 corrections proposees par IA](evals/ai_review/proposed_labels_v0.csv)
- [Instructions equipe et commandes](evals/VALIDATION_EQUIPE.md)
- [Repartition proposee et mode d'emploi](evals/ai_review/README.md)
- [50 cas officiels a valider](evals/eval_set_v0.csv)
- [Guide d'evaluation](evals/README.md)
- [Rapport S4](evals/report_v0.md)
- [Architecture](04_architecture.md)
