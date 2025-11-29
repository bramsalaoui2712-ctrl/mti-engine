# emotional_engine.py
import numpy as np
from datetime import datetime

class EmotionalEngine:
    """
    Moteur émotionnel simple et stable.
    Gère un état émotionnel interne et son évolution.
    Compatible API / microservice.
    """

    def __init__(self):
        self.state = {
            "valence": 0.0,        # humeur (-1 à +1)
            "arousal": 0.4,        # activation émotionnelle
            "stress": 0.1,         # stress interne
            "energy": 0.7          # énergie dispo
        }

        self.history = []

        # paramètres physiologiques simulés
        self.inertia = 0.7
        self.recovery = 0.04

    # ------------------------------------------
    # Mise à jour émotionnelle
    # ------------------------------------------
    def process(self, sentiment: float, complexity: float):
        """
        sentiment : -1 à +1
        complexity : 0 à 1
        """

        # Mise à jour progressive
        self.state["valence"] = (
            self.state["valence"] * self.inertia +
            sentiment * (1 - self.inertia)
        )

        # Complexité = charge cognitive
        self.state["stress"] += complexity * 0.15
        self.state["stress"] = min(1.0, self.state["stress"])

        # Energie diminue avec la charge, remonte naturellement
        self.state["energy"] += -complexity * 0.1 + self.recovery
        self.state["energy"] = max(0.0, min(1.0, self.state["energy"]))

        # Enregistrer
        self.history.append({
            "time": datetime.now().isoformat(),
            "state": self.state.copy()
        })

        return self.state.copy()

    # ------------------------------------------
    # Extraction simple de l'état émotionnel
    # ------------------------------------------
    def export_vector(self):
        """
        Retourne un petit vecteur émotionnel utilisable partout.
        """
        return np.array([
            self.state["valence"],
            self.state["arousal"],
            self.state["stress"],
            self.state["energy"]
        ], dtype=float)
