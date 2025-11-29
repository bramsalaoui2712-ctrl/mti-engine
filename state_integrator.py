import numpy as np

class StateIntegrator:
    """
    Intégrateur d’état unifié :
    combine cognition + émotion + mémoire légère + identité.
    Retourne un vecteur d’état de dimension 22.
    """

    def __init__(self):
        # Poids d’intégration
        self.weights = {
            "cognitive": 0.30,
            "emotional": 0.25,
            "memory": 0.20,
            "identity": 0.15,
            "temporal": 0.10
        }

    def fix_dim(self, arr, size):
        """Force un tableau vers une dimension donnée (truncate/pad)."""
        arr = np.array(arr)
        if len(arr) > size:
            return arr[:size]
        if len(arr) < size:
            return np.pad(arr, (0, size - len(arr)))
        return arr

    def integrate(self, cognitive, emotional, memory, identity, temporal):
        """
        Fusionne les 5 modules en un vecteur d'état cohérent et stable.
        """

        c = self.fix_dim(cognitive, 4)   * self.weights["cognitive"]
        e = self.fix_dim(emotional, 5)   * self.weights["emotional"]
        m = self.fix_dim(memory, 5)      * self.weights["memory"]
        i = self.fix_dim(identity, 5)    * self.weights["identity"]
        t = self.fix_dim(temporal, 3)    * self.weights["temporal"]

        final_state = np.concatenate([c, e, m, i, t])

        return final_state  # → vecteur de dimension 22
