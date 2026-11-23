# Relecture et evaluation restantes

**Etat au 23 novembre 2026 :** E001-E100 ont des references renseignees et deux evaluations sont archivees. Luna a confirme avoir relu et approuve toutes les grilles existantes a son nom. Les resultats echouent encore aux seuils de lancement ; le [memo final](../08_launch_memo.md) retient un non-lancement en mode assiste.

**Mise a jour des nouvelles references :** Luna a aussi approuve E151-E200 et le remplacement propose pour E174 ; ses 50 decisions et son prenom sont enregistres dans `ai_review/proposed_labels_v2.csv` ([confirmation](ai_review/luna_confirmation_E151_E200_2026-11-23.json)). E101-E150 attendent encore la revue de Jane. Les fichiers canoniques de reference importes et les evaluations historiques restent inchanges. Les similitudes de familles restent a arbitrer avant de presenter le nouveau lot comme independant ; aucune prediction ni notation des nouvelles sorties n'a ete produite.

## Les 100 cas supplementaires

`eval_set_v2_candidates.csv` contient E101-E200 : uniquement des entrees, sans bonne reponse, nom de validateur ni prediction. Ils completent un vivier de 200 scenarios, mais **il n'y a encore que 100 references humaines renseignees**.

Repartition possible, a realiser effectivement : Jane E101-E150 et Luna E151-E200. Chacune peut demander un arbitrage sur un cas ambigu ; ne pas remplir une signature a la place de l'autre. Malek peut aider selon sa disponibilite, avec son propre nom sur ses vraies contributions.

Les corrections sont preparees dans `ai_review/proposed_labels_v2.csv` pour faciliter la relecture : E151-E200 portent maintenant l'accord reel de Luna ; E101-E150 restent des brouillons a relire par Jane. Chaque relectrice accepte ou corrige les reponses puis renseigne son nom, sa vraie date et `human_decision=accept|correct` ; une correction doit etre expliquee dans `human_comment`. Les choix ambigus et le perimetre produit restent a verifier cas par cas.

## Avant de remplir les reponses

Comparer chaque scenario aux 300 lignes d'entrainement, aux familles, aux anciens exemples, a la KB et aux E001-E100 deja exposes. Un simple changement d'appareil, de nom ou de langue ne produit pas un incident independant. Retirer ou remplacer les cas trop proches avant de geler le nouveau jeu. Des ids uniques ne suffisent pas.

Ne pas entrer E101-E200 dans la console pour essayer le classement pendant cette phase : cela exposerait les sorties avant fixation des references. Le moteur n'a pas ete modifie pour ces nouveaux cas.

## Renseigner chaque ligne apres une vraie relecture

- Gravite : `expected_severity` = P1/P2/P3/P4/ABSTAIN. Expliquer les faits et les limites, sans inventer de telemetrie.
- Priorite appliquee : `expected_effective_priority`, selon le mode assiste documente ; aucune baisse automatique sous la declaration.
- Equipe, action acceptable, source reelle ou absence de source : `expected_team`, `expected_output_or_action`, `evidence_or_source`, `expected_evidence_ids` si pertinent.
- Reprise humaine : `hand_over_to_a_person` = yes/no. Une source simplement proche par ses mots n'est pas une procedure valide.
- Segment : severite, langue, tier et type de scenario.
- Signature : nom reel dans `labelled_by`, vraie date ISO dans `labelled_at`, puis `label_status=human_verified` apres accord reel. Utiliser une date/heure avec fuseau pour les nouvelles relectures, sans inventer une heure historique.

Les decisions d'organisation, les faits manquants et les desaccords doivent etre resolus avant le premier run. Ne jamais modifier les references d'un run expose pour ameliorer son score.

## Importer les vraies relectures puis executer

Depuis `Cybersecurity-SaaS`, seulement apres les 100 decisions humaines :

```powershell
uv run --frozen --python 3.12 python -m prototype.import_review --review evals/ai_review/proposed_labels_v2.csv --cases evals/eval_set_v2_candidates.csv --out evals/eval_set_v2_reviewed.csv
```

Cette commande conserve les entrees originales et refuse des signatures/decisions manquantes. Les etapes suivantes utilisent le nouveau fichier relu :

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate validate --cases evals/eval_set_v2_reviewed.csv
uv run --frozen --python 3.12 python -m prototype.evaluate freeze --cases evals/eval_set_v2_reviewed.csv --run-dir evals/runs/v2
uv run --frozen --python 3.12 python -m prototype.evaluate run --cases evals/eval_set_v2_reviewed.csv --run-dir evals/runs/v2
```

Avant relecture complete, validate/freeze refusent le fichier : c'est attendu. Si `v2` existe deja, le conserver et choisir un autre dossier. Une modification du modele apres consultation d'un cas demande de nouveaux cas pour une conclusion independante.

Deux personnes notent ensuite **chacune tous les nouveaux resultats**, dans leurs propres `grading_a.csv` et `grading_b.csv`, sans se consulter avant de remettre leurs decisions. Suivre [le bareme](README.md). Une relecture des references ne remplace pas cette notation des sorties.

```powershell
uv run --frozen --python 3.12 python -m prototype.evaluate summarise --cases evals/eval_set_v2_reviewed.csv --run-dir evals/runs/v2
```

Reporter les vrais resultats avec les echecs et leurs composants dans un nouveau rapport. Conserver les anciens resultats. Le temps economise, les utilisateurs reels et le lancement ne sont pas valides par la creation de ce fichier.

## Dernier controle de rendu

Relire le brief final, le memo de lancement et [FINALISATION.md](../FINALISATION.md). Verifier la consigne des 200 cas, les exigences d'auteurs et le starter avec l'enseignant. Faire les commits sous vos comptes, pousser apres revue et creer le tag final uniquement sur le commit relu. Les entretiens S3 restent explicitement simules tant que de vraies observations n'ont pas ete ajoutees.
