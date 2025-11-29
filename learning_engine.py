import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class LearningEngine(nn.Module):
    """
    Moteur d’apprentissage MTI.
    Version simple, stable et suffisante pour un moteur modulaire.
    """

    def __init__(self, input_dim=22, hidden_dim=64, output_dim=6):
        super().__init__()

        # Réseau pour produire des préférences internes
        self.pref_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Tanh()
        )

        # Réseau pour produire une décision
        self.decider = nn.Sequential(
            nn.Linear(input_dim + output_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=-1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def forward(self, state_vec):
        prefs = self.pref_net(state_vec)
        combined = torch.cat([state_vec, prefs], dim=-1)
        decision = self.decider(combined)
        return prefs, decision

    def learn(self, state_vec, reward):
        """
        Apprentissage simplifié : pousse le réseau vers état = reward.
        """
        state_vec = torch.FloatTensor(state_vec).unsqueeze(0)
        reward_tensor = torch.FloatTensor([reward])

        # Forward
        prefs, decisions = self.forward(state_vec)

        # Objectif : que la sortie colle avec le reward
        target = torch.ones_like(decisions) * reward_tensor

        loss = self.loss_fn(decisions, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
