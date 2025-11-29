# emotional_engine.py
from datetime import datetime

class EmotionalEngine:
    """
    Moteur émotionnel simplifié pour MTI.
    Gère un état émotionnel interne stable et évolutif.
    """

    def __init__(self):
        self.state = {
            "valence": 0.0,
            "arousal": 0.5,
            "stress": 0.1,
            "energy": 0.8,
            "last_update": datetime.now()
        }

    def update(self, sentiment: float = 0.0, complexity: float = 0.5):
        """Met à jour l'état émotionnel avec un mini-modèle."""
        self.state["valence"] = max(-1, min(1, self.state["valence"] * 0.7 + sentiment * 0.3))
        self.state["arousal"] = max(0, min(1, self.state["arousal"] * 0.6 + complexity * 0.4))
        self.state["stress"] = max(0, min(1, self.state["stress"] * 0.9 + abs(sentiment) * 0.2))
        self.state["energy"] = max(0, min(1, self.state["energy"] * 0.95 + (0.5 - complexity) * 0.1))
        self.state["last_update"] = datetime.now()
        return self.state

    def get_state(self):
        return self.state
