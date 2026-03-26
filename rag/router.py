class DomainRouter:
    def __init__(self):
        self.domain_keywords = {
            "auto": [
                "voiture", "auto", "automobile", "accident", "constat",
                "conducteur", "franchise auto", "bris de glace", "tous risques",
                "responsabilité civile auto", "véhicule"
            ],
            "sante": [
                "santé", "maladie", "arrêt maladie", "médecin", "hospitalisation",
                "mutuelle", "remboursement santé", "consultation", "optique",
                "dentaire", "indemnités journalières", "prévoyance"
            ],
            "habitation": [
                "habitation", "maison", "appartement", "locataire", "propriétaire",
                "incendie", "dégât des eaux", "vol", "multirisque habitation",
                "logement", "sinistre habitation"
            ],
            "banque_immobilier": [
                "banque", "immobilier", "prêt", "crédit", "emprunteur",
                "assurance emprunteur", "carte bancaire", "paiement", "fraude",
                "achat immobilier", "hypothèque", "mensualité", "taux"
            ],
        }

    def detect_domain(self, query: str) -> str:
        q = query.lower()
        scores = {domain: 0 for domain in self.domain_keywords}

        for domain, keywords in self.domain_keywords.items():
            for kw in keywords:
                if kw in q:
                    scores[domain] += 1

        best_domain = max(scores, key=scores.get)
        if scores[best_domain] == 0:
            return "general"

        return best_domain