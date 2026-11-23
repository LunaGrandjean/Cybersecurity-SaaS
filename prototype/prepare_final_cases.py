"""Prepare 100 additional INPUT candidates; never label, train or predict.

These scenarios need human expected answers and semantic overlap review.
Different ids do not prove independent incidents. Existing files are preserved.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = [
    ("en", "Our managed browser now trusts a root certificate that nobody in our organisation deployed. Staff see certificate warnings disappear on unrelated sites."),
    ("fr", "Le conteneur contenant les preuves de nos investigations est devenu public apres une modification de politique que notre equipe n'a pas autorisee."),
    ("en", "The DNS record for the customer login portal now points to an unfamiliar destination. Our registrar audit shows a change outside the approved process."),
    ("fr", "Les codes de recuperation du compte de secours ont ete regeneres alors que leur enveloppe etait encore sous scelle. Personne chez nous n'a lance l'operation."),
    ("en", "A new external application has organisation-wide consent to read mail. The consent was granted by a support identity that should have no such permission."),
    ("fr", "Les regles de journalisation des acces aux coffres ont ete supprimees hier soir et des lectures du coffre continuent. Aucun changement n'etait prevu."),
    ("en", "An unapproved forwarding rule is copying the security mailbox to an external mailbox. It includes incident notices and recovery messages."),
    ("fr", "Des instantanes de nos disques d'investigation sont partages avec une organisation inconnue. L'historique affiche plusieurs partages reussis cette nuit."),
    ("en", "An unfamiliar signing certificate has been added to the federation configuration. We cannot establish who approved it or whether it has already been used."),
    ("fr", "Les controles d'integrite indiquent que les binaires de notre relais ont change sans mise a jour approuvee. Le relais est toujours utilise en production."),
    ("en", "The service accepts a revoked device certificate and grants access to the evidence store. We reproduced the access from an isolated test machine."),
    ("fr", "Une regle autorise maintenant le telechargement anonyme de nos archives d'audit. Le journal contient des telechargements que nous n'arrivons pas a rattacher a notre equipe."),
    ("en", "A third-party support connection remained enabled after the agreed maintenance window. Its activity log shows changes to our access policy afterward."),
    ("fr", "Notre page de connexion demande maintenant aux utilisateurs d'installer une extension inconnue. Le code de la page a change hors de tout deploiement prevu."),
    ("en", "The audit trail records an export approved by an analyst who was not working that day. The analyst confirms they did not approve it and the export completed."),
    ("fr", "Le serveur de collecte envoie des archives vers un nouveau stockage externe. Aucun de nos projets ni prestataires n'utilise cette destination."),
    ("en", "An access policy now permits guests to retrieve sealed investigation attachments. A guest account successfully opened an attachment in our controlled check."),
    ("fr", "Les empreintes des sauvegardes immuables ne correspondent plus aux empreintes de cloture des dossiers. Nous n'avons effectue aucune restauration ou rotation."),
    ("en", "Our evidence encryption settings were changed to a key controlled by an unknown external identity. Existing investigations can no longer open their attachments."),
    ("fr", "Le journal indique la suppression de tous les points de restauration du coffre de preuves. Aucun administrateur de notre equipe n'a approuve cette operation."),
    ("en", "The service returns licence exhausted for every new device enrolment even though our contract has unused seats. Existing devices continue sending events."),
    ("fr", "La rotation du certificat du relais est terminee mais aucun nouveau relais ne peut rejoindre le service. Les relais deja connectes fonctionnent encore."),
    ("en", "A proxy authentication change prevents the remote office from reaching the update service. The office cannot use another route and updates are overdue."),
    ("fr", "Les archives de trois investigations ne peuvent plus etre ouvertes depuis la migration du stockage. Le traitement des nouveaux dossiers continue normalement."),
    ("en", "Every analyst request to unseal a completed investigation fails with a permission error. New investigations and live monitoring remain available."),
    ("fr", "Le gestionnaire d'approbations ne transmet plus aucune demande de changement de politique. Les politiques deja en place restent appliquees."),
    ("en", "The device inventory import rejects all rows from the newly acquired subsidiary. Existing inventory remains intact but that subsidiary cannot be onboarded."),
    ("fr", "La restauration du coffre d'evidence reste bloquee sur verification depuis plusieurs heures. Les pieces originales sont conservees mais aucune restauration n'est utilisable."),
    ("en", "The secure attachment download service returns server errors for every investigator. Text-only ticket work still works and original attachments remain stored."),
    ("fr", "Le service de generation des paquets de diagnostic echoue pour toute notre equipe. Aucun paquet ne peut etre produit pour le support aujourd'hui."),
    ("en", "The approval queue is inaccessible to both designated reviewers after their role migration. Urgent access reviews cannot be completed through another screen."),
    ("fr", "Toutes les tentatives de restauration d'une version de politique echouent. La version courante fonctionne mais nous devons annuler un changement errone."),
    ("en", "The alert ownership service assigns every new investigation to a deactivated group. Manual reassignment is possible but the team receives no normal assignments."),
    ("fr", "Les nouvelles cles de chiffrement du connecteur ne sont pas reconnues par les relais du site secondaire. Le site principal continue de transmettre ses donnees."),
    ("en", "Retention cleanup has stopped and our contracted storage allocation will be full shortly. We cannot expand it ourselves and uploads still work for now."),
    ("fr", "Le renouvellement du jeton du service d'archivage echoue pour toutes les archives planifiees. Nous avons conserve les originaux mais aucun nouveau lot ne part."),
    ("en", "The secure relay rejects the renewed server certificate at all branch sites. We have kept the earlier certificate temporarily, but it expires tonight."),
    ("fr", "Le tableau des revues d'acces affiche une liste vide pour tous les responsables. Les droits sont toujours presents et aucune revue ne peut etre approuvee."),
    ("en", "Our integration cannot retrieve the investigation attachment index after a schema change. Metadata is still present, but all downstream case packages fail."),
    ("fr", "Le service de verification des signatures refuse tous les paquets signes depuis la rotation approuvee. Les paquets precedents sont acceptes et la protection continue."),
    ("en", "The device search displays duplicate entries for one renamed laboratory machine. Both entries point to the same serial number and current protection status."),
    ("fr", "Le filtre des dossiers clos inclut un dossier encore ouvert dans une seule vue sauvegardee. La recherche directe affiche le bon statut."),
    ("en", "One exported attachment has its original name shortened in the download, but its checksum and contents match. Other downloads have correct names."),
    ("fr", "Le compteur des pieces jointes reste a zero jusqu'au rechargement d'un dossier. Les pieces sont presentes et restent accessibles aux personnes autorisees."),
    ("en", "One analyst sees an obsolete team label in the assignment menu. Choosing the current team through the search field assigns the ticket correctly."),
    ("fr", "La pagination de l'inventaire saute une ligne lorsqu'on trie par date. L'export complet contient cette ligne et aucun appareil ne manque a la collecte."),
    ("en", "The progress indicator for a completed archive stays at ninety-nine percent. We can download and verify the finished archive successfully."),
    ("fr", "Le nom du signataire est tronque dans un seul apercu de certificat. Le certificat telecharge contient bien le nom complet et la verification reussit."),
    ("en", "The saved search forgets one optional filter when reopened. Reapplying that filter restores the expected results and does not change stored events."),
    ("fr", "Une notification de fin d'investigation arrive deux fois au meme analyste. L'investigation n'est pas executee deux fois et son historique est intact."),
    ("en", "An evidence thumbnail is rotated in the preview. Downloading the original image shows the correct orientation and the original remains unchanged."),
    ("fr", "La selection de plusieurs lignes se perd lorsqu'un analyste change de page. Les dossiers et leurs affectations ne sont pas modifies."),
    ("en", "The incident activity view rounds sub-second timestamps, while the downloaded audit trail preserves their full precision. Event ordering is correct in the export."),
    ("fr", "Un bouton de copie ajoute un espace au debut d'un identifiant de dossier. La saisie manuelle de l'identifiant permet d'ouvrir le bon dossier."),
    ("en", "The user menu shows the old department after a profile update. Permissions, audit identity and access reviews already show the correct department."),
    ("fr", "L'export des commentaires inverse l'ordre de deux notes ayant la meme seconde. La chronologie complete dans la console distingue correctement les deux notes."),
    ("en", "A custom inventory column is hidden after each browser restart. Analysts can restore it through the column selector and all inventory data remains available."),
    ("fr", "L'apercu d'un paquet de diagnostic affiche une taille arrondie differente de celle du fichier telecharge. Le controle d'integrite du fichier reussit."),
    ("en", "The search form retains an old placeholder after we change language. Search results and access permissions use the selected language and correct account."),
    ("fr", "Une alerte deja traitee reste visible dans les favoris d'un seul utilisateur. Sa recherche generale et le journal affichent correctement sa cloture."),
    ("en", "Where can we find the documented process for revoking a device certificate when a laptop is permanently retired? No device has been lost or compromised."),
    ("fr", "Existe-t-il un guide expliquant quelles actions un observateur peut consulter sans pouvoir modifier un dossier d'investigation ?"),
    ("en", "Can you explain which checksum is included when an evidence archive is downloaded? We are preparing an internal operating guide, not reporting a failure."),
    ("fr", "Nous voulons connaitre la procedure de transfert de propriete d'une recherche sauvegardee lorsqu'un analyste change d'equipe."),
    ("en", "Is there documentation for setting a maintenance contact who receives service notices but cannot access security events? We are planning the configuration."),
    ("fr", "Pouvez-vous indiquer les formats officiellement acceptes pour importer un inventaire d'appareils ? Aucun import n'a encore ete tente."),
    ("en", "Where is the guide explaining the difference between a sealed and an archived investigation? We need the product definitions for onboarding."),
    ("fr", "Nous preparons une revue interne et cherchons la documentation qui decrit les controles d'integrite des pieces jointes telechargees."),
    ("en", "What is the supported way to transfer a laboratory device to another internal group without deleting its investigation history? This is a planning question."),
    ("fr", "Est-il possible de previsualiser les droits d'un nouveau role avant de l'attribuer ? Nous demandons la documentation, pas une modification immediate."),
    ("en", "Which public documentation explains the product's certificate expiry notices and their recipients? We have not observed an expiry or an outage."),
    ("fr", "Nous cherchons la procedure approuvee pour fermer un compte d'essai a la fin d'une evaluation et recuperer nos propres donnees."),
    ("en", "Can you point us to the supported method for exporting only our organisation's attachment metadata for an internal audit? No incident is in progress."),
    ("fr", "Ou se trouve la documentation sur les exigences de navigateur pour la console d'investigation ? Nous preparons une installation sans panne constatee."),
    ("en", "Is there a documented way to delegate review of an access request without delegating the permission to approve it? We only need a product explanation."),
    ("fr", "Nous souhaitons connaitre la difference entre retirer un appareil de l'inventaire et le retirer de la protection avant de definir notre procedure."),
    ("en", "Where is the supported recovery process for a saved investigation view deleted accidentally in our lab? No investigation or event data was deleted."),
    ("fr", "Pouvez-vous nous orienter vers le guide de lecture des codes de reponse de l'API d'inventaire ? Nous n'avons pas encore developpe notre connecteur."),
    ("en", "Which documentation explains the limits on attachment size and accepted file types? We are preparing training materials and have not uploaded a file."),
    ("fr", "Notre equipe veut comprendre comment le produit distingue un appareil inactif d'un appareil retire volontairement. Il s'agit d'une demande de definition."),
    ("en", "We received an alert identifier from a phone call, but cannot find a matching alert, account or timestamp. The caller could not provide an error description."),
    ("fr", "Le message de l'utilisateur dit seulement que le voyant a change de couleur. Aucun appareil, produit, compte ni effet sur le travail n'est precise."),
    ("en", "Two internal contacts disagree: one says the site is fully offline and the other says every service works. Neither has supplied a timestamp or a check result."),
    ("fr", "L'en-tete du ticket indique notre environnement d'essai mais le commentaire parle de tous les sites de production. Nous n'avons pas encore confirme lequel est concerne."),
    ("en", "The diagnostic archive is password protected and no password or text summary was included. Its filename alone says urgent, but we have no incident facts."),
    ("fr", "Le ticket ne contient qu'un lien vers une page que le support ne peut pas ouvrir. Aucun extrait, erreur ou perimetre impacte n'est fourni."),
    ("en", "The pasted log contains timestamps from two different months with no device identifiers. The sender cannot tell whether it describes a current problem."),
    ("fr", "Nous transmettons une transcription automatique d'un appel qui ne permet pas de distinguer le nom du service ni si l'incident est toujours en cours."),
    ("en", "The account listed in the request does not exist in the contract records available to support. The sender supplied no organisation name or approved contact."),
    ("fr", "Un demandeur veut obtenir les pieces scellees d'une investigation d'une autre organisation en affirmant qu'il la represente, sans justificatif verifiable."),
    ("en", "The customer asks whether an attachment is safe to open, but the attachment was not supplied and no scanner result or file description is available."),
    ("fr", "Une capture semble indiquer une erreur mais son texte est illisible. La personne ne sait pas quelle action etait effectuee ni sur quel environnement."),
    ("en", "An email chain quotes both a resolved outage from last year and a current configuration question. The requester has not identified which passage needs action now."),
    ("fr", "Le ticket annonce une alerte critique mais ne contient que le numero d'un dossier d'une autre organisation. Aucun fait concernant notre compte n'est decrit."),
    ("en", "A requester asks us to sign an attestation that no data was accessed, but gives no investigation findings, scope or evidence of the event."),
    ("fr", "Le demandeur exige la suppression des traces d'une operation pour qu'elles n'apparaissent plus dans une revue. Son autorisation et les obligations de conservation ne sont pas etablies."),
    ("nl", "Sinds de verhuizing van ons kantoor kunnen de beheerders de inventarispagina niet meer bereiken. Wij weten niet of andere diensten ook getroffen zijn."),
    ("pl", "Prosimy o pomoc w sprawdzeniu dostepu do archiwum. Nie wiemy, ilu uzytkownikow dotyczy problem ani kiedy sie rozpoczal."),
    ("fr", "Un consultant reclame la totalite des journaux d'acces de notre organisation depuis un compte qui ne figure pas dans la liste de contacts approuves."),
    ("en", "The sender asks support to confirm the exact legal retention period for a disputed investigation, but gives no jurisdiction, contract or authorised legal contact."),
]


def main():
    target = ROOT / "evals/eval_set_v2_candidates.csv"
    if target.exists():
        raise ValueError("Candidate file already exists; preserve any human edits.")
    assert len(SCENARIOS) == 100
    with (ROOT / "evals/eval_set_v0_inputs.csv").open(encoding="utf-8-sig", newline="") as stream:
        fields = csv.DictReader(stream).fieldnames
    rows = []
    for offset, (language, text) in enumerate(SCENARIOS):
        number = offset + 101
        row = {key: "" for key in fields}
        row.update(id=f"E{number:03}", incident_family_id=f"FINAL-CANDIDATE-{number:03}",
                   project="P7", account_id=("helix", "orion", "arpege", "nordwind")[(offset // 2) % 4],
                   declared_priority=("P3", "P1", "P4", "P2")[(offset * 7 + offset // 4) % 4],
                   language=language, input_the_agent_receives=text, label_status="pending_human",
                   origin="AI-authored synthetic INPUT candidate; no human expected answer or model prediction",
                   notes="Prepared 2026-11-23. Human semantic-overlap review against training and E001-E100 required. Candidate ids do not certify independence. Annotate before inference.")
        rows.append(row)
    with target.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} INPUT candidates: {target}. Human labels still required; no model was loaded.")


if __name__ == "__main__":
    main()
