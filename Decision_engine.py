import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class DecisionEngine(nn.Module):
    """
    Module décisionnel de MTI :
    - combine état cognitif/emotionnel/mémoire
    - calcule une intention
    - produit un type d'action + paramètres
    """

    def __init__(self, input_dim=22, hidden_dim=64, output_dim=4):
        super().__init__()

        # 1. Préférences internes
        self.pref_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Tanh()
        )

        # 2. Décision à partir de l'état + préférences
        self.decision_net = nn.Sequential(
            nn.Linear(input_dim + output_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=-1)
        )

        self.actions = ["text", "memory_update", "reflect", "noop"]

    def forward(self, state_vector):
        """
        Produit :
        - préférences internes
        - distribution de décision
        """

        if isinstance(state_vector, np.ndarray):
            state_vector = torch.FloatTensor(state_vector)

        state_vector = state_vector.unsqueeze(0)

        prefs = self.pref_net(state_vector)
        x = torch.cat([state_vector, prefs], dim=-1)
        decisions = self.decision_net(x)

        action_idx = torch.argmax(decisions).item()
        action_type = self.actions[action_idx]

        return {
            "preferences": prefs.detach().numpy().tolist(),
            "decision_map": decisions.detach().numpy().tolist(),
            "action": action_type
        }
