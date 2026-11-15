# Validation S4 par l'équipe

Le code et les documents sont préparés. Les décisions ci-dessous doivent encore être prises par de vraies personnes. Aucun résultat n'a été attribué à Jane, Malek ou Luna.

## 1. Relire les 50 corrections avant de lancer les prédictions

Ouvrir [proposed_labels_v0.csv](ai_review/proposed_labels_v0.csv), en CSV UTF-8. Répartition proposée :

| Personne | Cas |
|---|---|
| Jane | E001–E017 |
| Malek | E018–E034 |
| Luna | E035–E050 |

Pour chaque ligne : lire le ticket, puis accepter ou corriger les champs `expected_*`, `hand_over_to_a_person`, `evidence_or_source` et `segment`. Une proposition IA n'est pas forcément juste. Discuter les cas ambigus signalés dans `ai_uncertainty`, sans consulter une prédiction du modèle.

Renseigner soi-même :

- `human_decision` : `accept` ou `correct` ;
- `human_comment` : expliquer une correction et les ambiguïtés résolues ;
- `labelled_by` : le nom de la personne qui a réellement relu ;
- `labelled_at` : la date et l'heure réelles avec fuseau, par exemple au format `AAAA-MM-JJTHH:MM:SS+01:00`.

Conserver les colonnes et les entrées originales. Ne pas faire tourner le modèle sur ces cas pendant la relecture. Vérifier aussi l'absence de variantes d'un même incident entre entraînement, démo et évaluation. Les contrôles automatiques de texte/famille ne suffisent pas à vérifier cela.

## 2. Importer uniquement une fois les 50 lignes réellement relues

Commandes PowerShell depuis `Cybersecurity-SaaS` :

```powershell
uv run --frozen --python 3.12 python -m prototype.import_review
```

La commande refuse une relecture incomplète et crée `evals/eval_set_reviewed_v0.csv`. Elle ne fait aucune prédiction et ne remplace aucun fichier existant. Elle vérifie la présence des décisions, noms et dates ; elle ne peut pas prouver que la personne a réellement lu le ticket.

Après vérification du fichier créé, mettre les réponses validées dans le fichier attendu pour le rendu, **avant tout gel** :

```powershell
Copy-Item -LiteralPath evals/eval_set_reviewed_v0.csv -Destination evals/eval_set_v0.csv
uv run --frozen --python 3.12 python -m prototype.evaluate validate
```

Les corrections restent traçables dans le CSV de relecture. Si un premier run a déjà été gelé ou exécuté, conserver ce run : ne pas remplacer ses références pour améliorer son résultat.

## 3. Geler, puis exécuter une seule fois

Relire aussi les étiquettes d'entraînement proposées par IA et approuver les conventions de gravité/routage avant de figer le modèle. Ensuite :

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate freeze
uv run --frozen --python 3.12 python -m prototype.evaluate run
```

Les sorties sont dans `evals/runs/v0/predictions.json`. Si `v0` existe déjà, ne pas l'écraser. Toute modification après consultation d'une sortie transforme ces cas en données de développement ; une nouvelle évaluation indépendante nécessite alors de nouveaux cas.

## 4. Deux personnes notent chacune les 50 sorties

Proposition : Jane remplit `grading_a.csv`, Malek `grading_b.csv`, Luna coordonne ensuite les désaccords. C'est un rôle proposé, pas une action déjà effectuée. Les deux personnes travaillent indépendamment et notent **tous les 50 cas**, pas 25 chacune.

Chaque fichier se trouve dans `evals/runs/v0/`. Remplir `grader`, `usable_as_is` (`yes` ou `no`), `reason` pour chaque cas et `component` pour un échec. Suivre [le guide de notation](README.md). Conserver les deux jugements initiaux même après discussion.

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate summarise
```

Reporter les vrais résultats de `metrics.json` dans [report_v0.md](report_v0.md), identifier les trois échecs les plus fréquents avec leurs composants et ajouter les exigences correspondantes à [spec.md](../spec.md). Un résultat insuffisant doit rester visible. Le temps économisé reste non mesuré sans comparaison chronométrée.

## 5. Vérifier le bouton d'arrêt et rendre sur Git

Sur des tickets inventés, passer en mode assisté, créer un cas critique puis repasser en mode suggestions et créer un nouveau cas critique. Le second garde sa priorité déclarée ; le premier n'est pas rétrogradé. Tester aussi la reprise en main et exporter le journal. Dans `governance.md`, renseigner la personne, la date réelle et le résultat après votre essai.

Faire les commits avec vos propres comptes, puis pousser le rendu. La consigne demande quatre auteurs pour quatre commits alors que l'équipe compte trois personnes : faire préciser cette modalité par l'enseignant. Le starter Paylio absent des supports locaux et les entretiens S3 encore simulés restent des éléments à régulariser selon les attentes du cours.
