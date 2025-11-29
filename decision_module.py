import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class DecisionModule(nn.Module):
    """
    Module de décision simple pour MTI.
    Prend un état vectorisé (22 dim) + émotions -> renvoie un score d'action
    """

    def __init__(self, input_dim=22, hidden_dim=48, output_dim=4):
        """
        output_dim = 4 actions possibles :
        0 : répondre texto
        1 : enregistrer en mémoire
        2 : renforcer apprentissage
        3 : analyser émotionnellement
        """
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=-1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def forward(self, state_vector):
        """
        state_vector : torch.tensor shape (1,22)
        """
        return self.model(state_vector)

    def select_action(self, state_vector):
        """
        Retourne l’action avec probabilité max
        """
        with torch.no_grad():
            probs = self.forward(state_vector)
        return int(torch.argmax(probs, dim=-1).item())

    def train_from_reward(self, state_vector, action, reward):
        """
        Renforcement simple : 
        reward ∈ [0,1]
        action = index à renforcer
        """
        target = torch.zeros(1, self.model[-1].out_features)
        target[0, action] = reward

        preds = self.forward(state_vector)

        loss = self.loss_fn(preds, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
