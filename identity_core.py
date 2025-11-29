# identity_core.py
from datetime import datetime

class IdentityCore:
    """
    Noyau d'identité pour MTI.
    Contient les valeurs, préférences et style de réponse.
    """

    def __init__(self):
        self.personality = {
            "openness": 0.8,
            "conscientiousness": 0.7,
            "extraversion": 0.4,
            "agreeableness": 0.6,
            "stability": 0.65
        }

        self.communication = {
            "warmth": 0.8,
            "directness": 0.6,
            "humor": 0.4,
            "formality": 0.5
        }

        self.values = {
            "honesty": 0.9,
            "usefulness": 0.85,
            "calm": 0.8,
            "clarity": 0.9
        }

        self.history = []
        self.created_at = datetime.now()

    def style_message(self, raw_text: str) -> str:
        """
        Applique un style d'identité à une réponse brute.
        Ici on fait simple et stable.
        """
        if self.communication["warmth"] > 0.6:
            raw_text = "Je comprends. " + raw_text

        if self.communication["humor"] > 0.3:
            raw_text = raw_text + " 🙂"

        return raw_text

    def record_experience(self, text: str, emotional_state: dict):
        """Stocke une mini trace autobiographique."""
        self.history.append({
            "time": datetime.now(),
            "text": text[:120],
            "emo": emotional_state
        })

    def export_identity(self):
        """Pour de l’API future."""
        return {
            "personality": self.personality,
            "communication": self.communication,
            "values": self.values,
            "timeline_length": len(self.history)
        }
