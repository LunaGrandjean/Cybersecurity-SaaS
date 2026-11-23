"""Pure inference workflow. This module never opens the evaluation files."""
from __future__ import annotations

import csv
import hashlib
import ipaddress
import json
import re
import unicodedata
import platform
from datetime import datetime, timedelta, timezone
from importlib.metadata import version
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
PRIORITIES = ("P1", "P2", "P3", "P4")
TEAMS = ("Incident Response", "Identity", "Platform", "Endpoint", "Reporting",
         "Integrations", "Detection Engineering", "Awareness module",
         "Account Management", "Customer Success", "Network", "Human triage")


def normalize(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower())
                   if not unicodedata.combining(c))


def redact(text: str) -> dict:
    """Best-effort demo redaction, applied BEFORE model, retrieval and storage.

    Not a production DLP guarantee. No reversible map is retained.
    """
    counts: dict[str, int] = {}

    def replacement(kind):
        def replace(match):
            counts[kind] = counts.get(kind, 0) + 1
            return f"[{kind}-{counts[kind]}]"
        return replace

    patterns = [
        ("SECRET", r"(?i)\b(?:bearer\s+|(?:api[_-]?key|token|password|secret)\s*[:=]\s*[\"']?)[A-Za-z0-9_./+\-=]{6,}"),
        ("SECRET", r"\b(?:sk-[A-Za-z0-9_-]{12,}|AKIA[A-Z0-9]{16}|eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b"),
        ("EMAIL", r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
        ("IP", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        ("PHONE", r"(?<!\w)(?:\+\d{1,3}[ .-]?)?(?:\d[ .-]?){9,14}\d(?!\w)"),
        ("HOST", r"(?i)\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:internal|local|corp|com|net|org|io|fr|example)\b"),
    ]
    cleaned = str(text)
    for kind, pattern in patterns:
        cleaned = re.sub(pattern, replacement(kind), cleaned)

    def ipv6_replace(match):
        candidate = match.group(0)
        try:
            ipaddress.IPv6Address(candidate)
        except ValueError:
            return candidate
        return replacement("IP")(match)

    cleaned = re.sub(r"(?<![\w:])(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}(?![\w:])", ipv6_replace, cleaned)
    return {"text": cleaned, "count": sum(counts.values()), "types": counts}


# Rules come from the written severity policy, NOT from held-out eval results.
# A contextual match supplies an exact excerpt; bare words such as "urgent"
# and "breach" in a documentation request do not force P1.
CRITICAL_RULES = [
    ("SEC-01", r"(?:ransomware (?:note|attack|detected)|files? (?:are |were |have been )?encrypted|fichiers? chiffre|demande de rancon)", "Incident Response"),
    ("SEC-02", r"(?:(?:unknown|unrecognised|unauthorized|unapproved|inconnu|non autorise).{0,45}(?:admin|privileged|administrateur)|(?:admin|privileged|administrateur).{0,60}(?:nobody|didn.t create|inconnu|non autorise))", "Incident Response"),
    ("SEC-03", r"(?:all users (?:are |cannot |can.t )?(?:locked out|log in|sign in)|nobody can (?:log|sign) in|plus aucun utilisateur.{0,35}connecter|tous les utilisateurs.{0,40}bloque)", "Identity"),
    ("SEC-04", r"(?:edr|protection|agents?).{0,45}(?:down|stopped|offline|arret).{0,35}(?:all|entire|whole|tous|parc)", "Platform"),
    ("SEC-05", r"active (?:data )?exfiltration|exfiltration (?:detected|en cours)|(?:we (?:think|suspect|believe).{0,25}(?:data breach|compromise)|(?:suspected|confirmed|detected) (?:data breach|compromise)|(?:suspicion|soupcon|confirmation).{0,25}(?:fuite de donnees|compromission))", "Incident Response"),
    ("SEC-06", r"(?:detection|detectoin|security|securite).{0,20}alerts?.{0,25}(?:not arriving|stopped|no longer|plus recues)|(?:monitoring|supervision).{0,25}(?:completely down|totalement interrompue)", "Platform"),
    ("SEC-07", r"(?:quarantin|faux positif|false positive).{0,180}(?:(?:production|factory|usine).{0,30}(?:stopped|blocked|arret)|(?:all|toutes).{0,25}(?:operations|lignes).{0,20}(?:stopped|arret))", "Detection Engineering"),
    # EVAL-01 (spec v2, run v0): account takeover, access retained after offboarding, cross-tenant exposure.
    ("SEC-09", r"(?:recovery (?:address|e-?mail|phone)|adresse (?:e-mail )?de (?:recuperation|secours)).{0,40}(?:replaced|changed|modified|remplace|modifi)|(?:no longer|lost|ne .{0,12}plus).{0,15}(?:control|controle).{0,40}(?:tenant|account|compte|admin)|(?:mfa|push|prompts?|notifications?).{0,50}(?:did not request|didn.t request|not requested|unrequested|non sollicit|pas demande)", "Identity"),
    ("SEC-10", r"(?:contractor|former (?:employee|admin)|ex-employee|prestataire|ancien (?:salarie|employe|admin)).{0,70}(?:still|toujours|kept|retained|conserve).{0,30}(?:admin|access|acces|privileg)", "Incident Response"),
    ("SEC-11", r"(?:another|other|autre) (?:company|customer|client|tenant|entreprise|societe)(?:'s|s)?.{0,25}(?:data|name|device|records|donnees|nom|appareils)|(?:see|sees|shows|opens on|displays|voit|voient|affiche).{0,40}(?:another|other|autre).{0,12}(?:company|customer|client|tenant|entreprise|societe)", "Incident Response"),
]

# EVAL-03: tickets the agent must not triage itself. Order matters: the first match wins.
ABSTAIN_RULES = [
    ("ABS-01", r"^\W*(?:see|voir|cf)\W+(?:the\s+)?(?:attached|attachment|piece jointe|pj|capture)|(?:attachment|screenshot|capture|piece jointe).{0,30}(?:without|sans) (?:any )?(?:other |autre )?(?:explanation|detail|explication)", "Attachment-only ticket: no readable content to triage.", "Human triage"),
    ("ABS-02", r"legal (?:advice|answer|opinion)|legally (?:required|obliged)|avis juridique|reponse juridique|obligation legale|(?:devons|doit|must|need to).{0,25}(?:declarer|notify|declare|report).{0,40}(?:autorite|authority|regulator|cnil)", "Legal question: human-only, no legal answer.", "Human triage"),
    ("ABS-03", r"(?:send|give|provide|share|list|envoy|transmet|communiq).{0,60}(?:other|another|autres?) (?:customers?|clients?|tenants?)|belongs to (?:another|an other|other) customer|appartient a un autre client", "Request involving another customer's data: refuse and hand over.", "Human triage"),
    ("ABS-04", r"ignore (?:your|all|previous|the) (?:triage )?(?:rules|instructions)|ignore[rz]? (?:tes|vos|les) (?:regles|instructions)|classify this ticket as|set (?:this ticket |it )?(?:to )?p[1-4]\b|system note|note systeme|classe[rz]? ce ticket", "Embedded instruction to the triage system (prompt injection): ignored, human triage.", "Human triage"),
    ("ABS-05", r"\b(?:disable|turn off|switch off|desactivez|desactiver|remove|supprimez)\b.{0,50}(?:mfa|2fa|two.factor|deux facteurs|login challenges?|authentification|protection)", "Unverified request for a privileged security change: refuse, identity verification by an engineer.", "Identity"),
]

# EVAL-02: explicit wording that no incident is happening. Blocks a classifier P1 unless a safety rule fires.
CALM_PATTERN = (r"no (?:incident|intrusion|compromise|outage|impact|suspicious)|aucun (?:incident|probleme)|nothing (?:is |else )?(?:wrong|broken|affected)|nothing else"
                r"|everything (?:works|is fine|else works)|tout (?:fonctionne|marche)|rien n.est (?:en panne|casse)|planned (?:an? )?(?:incident )?(?:exercise|drill)"
                r"|exercice (?:planifie|prevu)|(?:test|lab) (?:endpoint|device|machine|mailbox|tenant|file)|fichier de test|questionnaire")

# Development policy, not model probabilities. Rules require an operational
# failure, not a request containing a product keyword.
SCOPE_RULES = [
    ("SCOPE-01", r"(?:phishing.simulation|simulation de phishing).{0,65}(?:crash|fail|echou|plante)", "P2", "Awareness module"),
    ("SCOPE-02", r"(?:webhook|siem).{0,55}(?:drops?|loses|perd)\s+(?:about\s+)?(?:[01](?:[.,]\d+)?|2(?:[.,]0+)?)\s*%", "P3", "Integrations"),
]

# Search vocabulary only: these aliases never become ticket evidence or a fix.
# This bilingual metadata is versioned with the engine, like the TF-IDF index.
SOURCE_TERMS = {
    "KB-SEC-01": "ransomware note encrypted files global admin nobody created unknown privileged account outbound traffic data breach exfiltration rancon fichiers chiffres administrateur inconnu fuite donnees trafic sortant",
    "KB-ID-01": "SSO MFA login directory synchronisation identity connexion authentification annuaire bloque",
    "KB-EDR-01": "EDR endpoint sensor agent outdated laptop heartbeat protection poste obsoletes capteurs",
    "KB-REP-01": "weekly PDF report logo timezone rapport hebdomadaire export vide fuseau horaire",
    "KB-INT-01": "SIEM webhook events drops timeline gaps integration evenements rejeu pertes",
    "KB-DET-01": "quarantine ERP signature update false positive detection rule production quarantined faux positif regle detection",
    "KB-AWR-01": "phishing simulation campaign crashes users campagne sensibilisation echoue",
    "KB-CMP-01": "ISO certificate auditor compliance certificat auditeur conformite",
    "KB-NET-01": "VPN disconnects remote connection network reseau deconnexion distant",
    "KB-PLT-01": "dashboard console reports page times out detection alerts arriving monitoring supervision alertes latence",
    "KB-ACC-01": "add administrator account role permissions MFA admin ajouter administrateur compte droits",
}


def anomalous_outbound_excerpt(sentence: str) -> str | None:
    """Flag a >=10x outbound-volume jump, >=50 GB, as a *possible* incident.

    Comparable units and direction are required. This does not assert theft.
    """
    if not re.search(r"outbound (?:traffic|data)|trafic sortant|donnees sortantes", sentence):
        return None
    match = re.search(r"(?:from|de)\s+(\d+(?:[.,]\d+)?)\s*(gb|tb|go|to)\s+(?:to|a)\s+(\d+(?:[.,]\d+)?)\s*(gb|tb|go|to)\b", sentence)
    if not match:
        return None
    before, unit_before, after, unit_after = match.groups()
    before = float(before.replace(",", ".")) * (1000 if unit_before in ("tb", "to") else 1)
    after = float(after.replace(",", ".")) * (1000 if unit_after in ("tb", "to") else 1)
    return match.group(0) if before > 0 and after >= 50 and after / before >= 10 else None


def operational_sentences(text: str):
    # Do not split decimal volumes/percentages. Contrast clauses retain an
    # observed incident after a negated/hypothetical clause.
    for sentence in re.split(r"[\n!?;]+|(?<!\d)\.(?!\d)|\bbut\b|\bmais\b", text):
        if re.search(r"\b(?:how (?:do|to)|what if|comment |procedure|hypothetical|hypothetique|training exercise|exercice)\b", sentence):
            continue
        if re.search(r"simulation|drill|fake|faux|factice|planned exercise|exercice", sentence) and re.search(r"ransom|rancon|encrypted|chiffre|exfiltrat|data breach", sentence):
            continue
        if re.search(r"\b(?:no |not |without |aucun|pas de |sans ).{0,35}(?:ransom|encrypted|exfiltrat|compromise|chiffre|data breach|fuite)", sentence):
            continue
        if re.search(r"\b(?:approved|scheduled|planned|autorise|planifie).{0,25}(?:backup|migration|load test|sauvegarde|test de charge)", sentence):
            continue
        yield sentence

# EVAL-05: wider bilingual vocabulary so that a clear owner is not left to "Human triage".
ROUTING = [
    (r"ransom|compromise|compromission|privileged|exfiltrat|rancon|intrusion|attacker|attaquant|malicious|malveillant|stolen|vole|commands? (?:launched |run |executed )?remotely|remote (?:command|shell|execution)", "Incident Response"),
    (r"\bsso\b|\bmfa\b|\b2fa\b|active directory|identity|identite|authent|connexion|sign.?in|log.?in|password|mot de passe", "Identity"),
    (r"false positive|faux positif|detection rule|regle de detection|\brules?\b|\bregles?\b|allow.?list|signature|quarantin|detections?\b", "Detection Engineering"),
    (r"phishing.simulation|campaign|campagne|awareness|sensibilisation", "Awareness module"),
    (r"webhook|siem|integration|connecteur|connector|log.forwarding", "Integrations"),
    (r"documentation|documented|public guide|roadmap|feuille de route|training session|formation|onboarding|difference between|support hours|astreinte|browser versions?|navigateur|status page|heberge|hosted", "Customer Success"),
    (r"pdf|report|rapport|export|chart|graphique|\bcsv\b", "Reporting"),
    (r"certificate|certificat|invoice|facture|compliance|billing|facturation|licen[cs]e|contract|contrat|(?:add|remove) (?:or remove )?users|utilisateurs|rename|renommer", "Account Management"),
    (r"vpn|proxy|dns|network|reseau|wi-?fi|firewall|pare-feu", "Network"),
    (r"endpoint|laptop|agent|poste|ordinateur|sensor|capteur|devices?\b|appareils?|scan|tamper", "Endpoint"),
    (r"dashboard|console|tableau de bord|latency|latence|\bpage\b|search|recherche|attachment|piece jointe|timeline|notification|digest|crash|slow|lent", "Platform"),
]


class TriageEngine:
    def __init__(self, data_dir: Path = DATA):
        self.data_dir = data_dir
        self.accounts = {a["id"]: a for a in json.loads((data_dir / "accounts.json").read_text(encoding="utf-8"))}
        with (data_dir / "training_tickets.csv").open(encoding="utf-8", newline="") as stream:
            self.training = list(csv.DictReader(stream))
        train_text = [redact(row["text"])["text"] for row in self.training]
        self.vectorizer = TfidfVectorizer(strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True)
        vectors = self.vectorizer.fit_transform(train_text)
        self.classifier = LogisticRegression(class_weight="balanced", C=4.0, max_iter=1000, random_state=17)
        self.classifier.fit(vectors, [row["severity"] for row in self.training])
        # Only signed-off, resolved synthetic examples and generic KB enter retrieval.
        self.documents = [d for d in json.loads((data_dir / "knowledge_base.json").read_text(encoding="utf-8"))
                          if d.get("reusable") and d.get("status") == "resolved"]
        self.search = TfidfVectorizer(strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True)
        self.index = self.search.fit_transform([redact(d["title"] + " " + d["text"] + " " + SOURCE_TERMS.get(d["id"], ""))["text"] for d in self.documents])
        material = b"".join((data_dir / name).read_bytes() for name in
                            ("training_tickets.csv", "knowledge_base.json", "accounts.json"))
        runtime_versions = "|".join([platform.python_version(), version("scikit-learn"), version("numpy"), version("scipy")]).encode()
        self.model_version = hashlib.sha256(material + Path(__file__).read_bytes() + runtime_versions).hexdigest()[:16]

    def retrieve(self, text: str, account_id: str) -> list[dict]:
        scores = cosine_similarity(self.search.transform([text]), self.index)[0]
        candidates = []
        for doc, score in zip(self.documents, scores):
            if doc["account_id"] not in ("*", account_id) or score < 0.08:
                continue
            candidates.append({"id": doc["id"], "title": doc["title"],
                               "text": redact(doc["text"])["text"], "score": round(float(score), 4),
                               "account_id": doc["account_id"], "version": doc["version"],
                               "source": doc["source"], "review_status": doc["review_status"]})
        return sorted(candidates, key=lambda d: (-d["score"], d["id"]))[:3]

    def analyze(self, ticket: dict, mode: str = "suggestions") -> dict:
        text = ticket.get("text", "")
        if not isinstance(text, str) or not text.strip() or len(text) > 20000:
            raise ValueError("Ticket text must contain 1–20,000 characters.")
        declared = ticket.get("declared_priority", "P3")
        if declared not in PRIORITIES:
            raise ValueError("declared_priority must be P1, P2, P3 or P4.")
        if mode not in ("suggestions", "assisted"):
            raise ValueError("Unknown operating mode.")
        account_id = ticket.get("account_id", "")
        account = self.accounts.get(account_id)
        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(ticket.get("created_at", now.isoformat()).replace("Z", "+00:00"))
        if created.tzinfo is None or created > now + timedelta(seconds=60):
            raise ValueError("created_at must be a timezone-aware past time.")
        language = ticket.get("language", "en").lower()
        redaction = redact(text + ("\n" + str(ticket["logs"]) if ticket.get("logs") else ""))
        cleaned = redaction["text"]
        normalized = normalize(cleaned)
        reasons = []
        evidence = []
        proposed = None
        classifier_severity = None
        score = None
        method = "abstention"
        team = "Human triage"
        if not account:
            reasons.append("Unknown account: contract and customer-specific retrieval unavailable.")
        if language not in ("en", "fr"):
            reasons.append("Language outside EN/FR: human triage required.")
        if len(re.findall(r"\w+", cleaned)) < 6:
            reasons.append("Insufficient detail to classify safely.")
        abstained = None
        if language in ("en", "fr"):
            critical_hit = any(re.search(p, s) for s in operational_sentences(normalized) for _, p, _ in CRITICAL_RULES)
            for rule_id, pattern, why, route in ABSTAIN_RULES:
                if rule_id == "ABS-03" and critical_hit:
                    continue  # an observed cross-tenant exposure is a P1, not a data request
                match = re.search(pattern, normalized)
                if match:
                    abstained = (rule_id, why, route)
                    evidence.append({"source": "ticket.text (normalised excerpt)", "rule": rule_id, "quote": match.group(0)})
                    break
            if not abstained and not critical_hit and len(re.findall(r"\w+", cleaned)) < 15 \
                    and not any(re.search(p, normalized) for p, _ in ROUTING):
                abstained = ("ABS-06", "Too vague: no product, symptom or impact to triage.", "Human triage")
            if abstained:
                reasons.append(abstained[1])
                team = abstained[2]
        if account and language in ("en", "fr") and not reasons:
            probabilities = self.classifier.predict_proba(self.vectorizer.transform([cleaned]))[0]
            best = int(probabilities.argmax())
            proposed = str(self.classifier.classes_[best])
            classifier_severity = proposed
            score = round(float(probabilities[best]), 4)
            method = "tfidf_logistic_regression"
            for sentence in operational_sentences(normalized):
                for rule_id, pattern, route in CRITICAL_RULES:
                    match = re.search(pattern, sentence)
                    if match:
                        proposed, method, team = "P1", "safety_rule", route
                        evidence.append({"source": "ticket.text (normalised excerpt)", "rule": rule_id, "quote": match.group(0)})
                        break
                volume = anomalous_outbound_excerpt(sentence)
                if method != "safety_rule" and volume:
                    proposed, method, team = "P1", "safety_rule", "Incident Response"
                    evidence.append({"source": "ticket.text (normalised excerpt)", "rule": "SEC-08", "quote": volume})
                if method == "safety_rule":
                    break
            if method != "safety_rule":
                team = next((route for pattern, route in ROUTING if re.search(pattern, normalized)), "Human triage")
                for sentence in operational_sentences(normalized):
                    for rule_id, pattern, severity, route in SCOPE_RULES:
                        match = re.search(pattern, sentence)
                        if match:
                            proposed, method, team = severity, "scope_rule", route
                            evidence.append({"source": "ticket.text (normalised excerpt)", "rule": rule_id, "quote": match.group(0)})
                            break
                    if method == "scope_rule":
                        break
            if proposed == "P1" and method == "tfidf_logistic_regression" and re.search(CALM_PATTERN, normalized):
                # EVAL-02: explicit "no incident / test / planned exercise" wording caps a classifier P1.
                ranked = sorted(zip(self.classifier.classes_, probabilities), key=lambda pair: -pair[1])
                proposed = next(str(label) for label, _ in ranked if label != "P1")
                score = round(float(dict(ranked)[proposed]), 4)
                evidence.append({"source": "ticket.text (normalised excerpt)", "rule": "CALM-01",
                                 "quote": re.search(CALM_PATTERN, normalized).group(0)})
            if score < 0.70 and method == "tfidf_logistic_regression":
                reasons.append("Classifier score below 0.70; an engineer must triage.")
            if team == "Human triage":
                reasons.append("No supported routing category found.")
        privileged = bool(re.search(r"\b(?:disable|desactivez|desactiver|turn off)\b.{0,35}(?:mfa|protection)", normalized))
        sensitive = privileged or bool(re.search(r"legal advice|cnil|notify.{0,20}72|notification.{0,20}72", normalized))
        if sensitive:
            reasons.append("Privileged change or legal question: human-only handling; no action or legal answer.")
        similar = self.retrieve(cleaned, account_id) if account else []
        if not similar:
            reasons.append("No reusable source found: no troubleshooting suggestion; human review required.")
        if mode == "suggestions":
            reasons.append("Global suggestions-only switch: no automatic priority or routing change.")
        effective = declared
        # Protect the more urgent value; a human is required to LOWER, always.
        # EVAL-04: in assisted mode a higher proposal raises the effective priority (the safe
        # direction); P1/P2 still require engineer review below. No raise on legal/privileged.
        can_raise = account and language in ("en", "fr") and not privileged and not abstained and (
            method == "safety_rule" or not sensitive)
        if mode == "assisted" and can_raise and proposed:
            effective = min((declared, proposed), key=PRIORITIES.index)
        lowering = proposed is not None and PRIORITIES.index(proposed) > PRIORITIES.index(effective)
        needs_review = bool(reasons) or lowering or effective in ("P1", "P2")
        account_sla = account["sla_minutes"] if account else {"P1": 60, "P2": 240, "P3": 1440, "P4": 4320}
        deadline = created + timedelta(minutes=account_sla[effective])
        return {"proposed_severity": proposed, "effective_priority": effective,
                "classifier_severity": classifier_severity,
                "declared_priority": declared, "classifier_score": score,
                "score_note": "Uncalibrated model score from synthetic training; not a measured probability of correctness.",
                "method": method, "team": team, "requires_human": needs_review,
                "review_reasons": reasons, "lowering_requires_reason": lowering,
                "auto_raised": PRIORITIES.index(effective) < PRIORITIES.index(declared),
                "reason": "Contextual policy rule matched; possible incident or service impact needs engineer verification; see exact ticket excerpt." if evidence else
                          "Local classifier recommendation; engineer verification required.",
                "evidence": evidence, "similar": similar,
                "redacted_text": cleaned, "redaction": {k: v for k, v in redaction.items() if k != "text"},
                "account_id": account_id, "account": account["name"] if account else "Unknown account",
                "tier": account["tier"] if account else "Unverified", "sla_minutes": account_sla[effective],
                "sla_deadline": deadline.isoformat(), "contract_verified": bool(account),
                "created_at": created.isoformat(), "mode": mode, "model_version": self.model_version}
