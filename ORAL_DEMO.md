# Oral et demonstration du copilot de triage

## Message a porter

Nous avons construit un assistant interne pour aider un ingenieur support a proposer une gravite, retrouver le bon SLA et des sources utiles. Le scenario compte 400 comptes, 6000 tickets par mois et 25 ingenieurs. Le prototype est un workflow fixe : regles, classifieur classique, recherche et verification humaine. Il ne contacte jamais le client et ne baisse jamais automatiquement une priorite.

Le modele utilise TF-IDF et une regression logistique sur 300 exemples synthetiques. Ses scores ne sont pas des probabilites de justesse mesurees. Les regles donnent des extraits du ticket, pas des heures ou des preuves inventees. Les donnees d'entrainement et la KB ont encore des limites de validation.

Le point decisif est l'evaluation : derniere version 9/22 triages courants acceptes par les deux grilles et 9/14 urgences P1 reconnues. Les fausses alertes P1 sont 3/28 et aucune priorite n'a ete abaissee. Les seuils de securite et d'utilite echouent, donc nous ne recommandons pas le lancement assiste. Nous avons conserve les echecs, traduit leurs causes en exigences et defini les conditions d'un nouvel essai.

## Parcours de demo

1. Depuis la racine, lancer `uv run --frozen --python 3.12 python -m prototype.server`, puis ouvrir http://127.0.0.1:8765. Utiliser seulement des donnees inventees et les exemples de demonstration.
2. Montrer le mode suggestions par defaut. Creer un ticket P3 sur un administrateur privilegie inconnu : lire la suggestion P1, l'extrait reel et la priorite effective qui reste P3 dans ce mode.
3. Montrer le SLA ancre a l'heure de creation, les sources de meme client ou generiques et les limites du score. Verifier/changer avec un motif, puis accepter. Montrer que Take over conserve les controles manuels.
4. Sur des tickets de demonstration uniquement, activer le mode assiste avec un motif. Creer un nouveau cas critique : il peut monter en P1. Repasser en suggestions et creer un nouveau ticket : il reste a sa priorite declaree. Le ticket precedemment monte n'est pas retrograde.
5. Exporter le journal, recharger la page et montrer la persistance. Revenir en suggestions-only avant de fermer la demo.
6. Ouvrir le rapport pour montrer un echec reel deja expose et les chiffres du non-lancement. Ne pas utiliser E101-E200 pour essayer le modele avant fixation de leurs references.

## Questions a savoir expliquer

- Pourquoi pas un agent autonome ou un LLM ? La tache est bornee, le workflow fixe est inspectable et l'inference reste locale. Un modele plus complexe devrait apporter un gain mesure.
- Pourquoi le mode ne-jamais-baisser ne suffit-il pas ? Un client peut declarer P4 pour une vraie urgence ; conserver P4 ne detecte pas le P1.
- Pourquoi ne pas annoncer un gain financier ? Les minutes et penalites du sizing sont des hypotheses. Ni le temps reel ni les penalites evitees n'ont ete mesures.
- Les deux lots sont-ils une preuve aveugle ? Non : le second lot etait nouveau mais ses entrees avaient ete vues par l'auteur des corrections. Les principales grilles ont utilise un pre-remplissage ; le rapport garde ces limites.
- Les entretiens sont-ils reels ? Non, la recherche S3 est explicitement simulee. Elle donne des hypotheses, pas une validation utilisateur.
- Qu'est-ce qui manque ? Les 100 nouveaux cas doivent etre relus et labels avant execution, les sources/etiquettes revues et les conditions de securite/utilite remplies avant un pilote approuve.

Chaque membre presente une contribution qu'il a reellement relue et un commit de son propre compte. Adapter la duree de cette trame a la consigne de l'oral ; aucune duree officielle n'est supposee ici.
