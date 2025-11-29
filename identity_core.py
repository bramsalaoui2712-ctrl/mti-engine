# identity_core.py
import numpy as np
from datetime import datetime

class IdentityCore:
    """
    Noyau identitaire simple et propre.
    Donne personnalité, style de communication et valeurs internes.
    """

    def __init__(self):
        # Traits constants (0 à 1)
        self.personality = {
            "warmth": 0.7,
            "clarity": 0.8,
            "directness": 0.55,
            "humor": 0.35,
            "formality": 0.50
        }

        # Valeurs stabilisatrices
        self.values = {
            "honesty": 0.9,
            "non_harm": 1.0,
            "usefulness": 0.85,
            "respect": 0.95
        }

        # Historique minimal
        self.history = []

    # ---------------------------------------
    # STYLE DE COMMUNICATION
    # ---------------------------------------
    def stylize(self, text: str) -> str:
        """
        Modifie légèrement la réponse brute pour refléter la personnalité.
        """
        t = text.strip()

        # chaleur
        if self.personality["warmth"] > 0.6:
            t = "Je comprends. " + t

        # humour discret
        if self.personality["humor"] > 0.3:
            if len(t) > 30:
                t += " 😉"

        # clarté
        if self.personality["clarity"] > 0.7:
            t = t.replace("je crois", "je pense clairement que")
            t = t.replace("peut-être", "probablement")

        # directivité
        if self.personality["directness"] > 0.5:
            t = t.replace("je pense que", "voici ce qu'il faut retenir :")

        return t

    # ---------------------------------------
    # ALIGNEMENT AVEC LES VALEURS
    # ---------------------------------------
    def enforce_values(self, text: str) -> str:
        """
        Corrige la réponse si elle viole les valeurs internes.
        """
        if self.values["non_harm"] > 0.9:
            forbidden = ["tuer", "blesser", "détester"]
            for f in forbidden:
                if f in text.lower():
                    text = text.replace(f, "[contenu filtré]")

        return text

    # ---------------------------------------
    # COHÉRENCE IDENTITAIRE
    # ---------------------------------------
    def apply(self, raw_text: str) -> str:
        """
        Pipeline complet : stylisation + valeurs + cohérence.
        """
        text = self.stylize(raw_text)
        text = self.enforce_values(text)

        self.history.append({
            "time": datetime.now().isoformat(),
            "raw": raw_text,
            "final": text
        })

        return text
