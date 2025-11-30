# cognitive_orchestrator.py
import asyncio
from datetime import datetime
from typing import Dict, Any

from mti_engine import (
    RobustCognitiveEngine,
    AdvancedEmotionalEngine,
    IdentityCore,
    RobustVectorMemory,
    ConsistentStateIntegrator,
    FunctionalLearningEngine,
    AdvancedEthicalFirewall,
    AsyncCognitiveDatabase,
    GenerationPipeline,
    AsyncActionModule,
)

class CognitiveOrchestrator:
    """Orchestrateur central du moteur MTI."""

    def __init__(self):
        self.creation_time = datetime.now()

        # Sous-systèmes
        self.cognitive_engine = RobustCognitiveEngine()
        self.emotional_engine = AdvancedEmotionalEngine()
        self.identity_core = IdentityCore()
        self.vector_memory = RobustVectorMemory()
        self.state_integrator = ConsistentStateIntegrator()
        self.learning_engine = FunctionalLearningEngine()
        self.ethical_firewall = AdvancedEthicalFirewall()
        self.db = AsyncCognitiveDatabase()
        self.generator = GenerationPipeline()
        self.actions = AsyncActionModule()

    async def process(self, user_text: str) -> Dict[str, Any]:
        """Pipeline complet pour traiter une entrée utilisateur."""

        # 1. Compréhension
        understanding = self.cognitive_engine.understand_text(user_text)

        # 2. Rappel mémoire
        similar_memories = await self.vector_memory.search_similar(
            understanding["embedding"],
            k=5
        )

        # 3. Traitement émotionnel
        emotional_state = self.emotional_engine.process_experience_emotionally(
            understanding,
            similar_memories
        )

        # 4. État unifié
        unified_state = self.state_integrator.integrate_complete_state(
            understanding,
            emotional_state,
            similar_memories,
            {
                "personality_traits": self.identity_core.personality_traits,
                "communication_style": self.identity_core.communication_style
            },
            {
                "time_since_start": (datetime.now() - self.creation_time).seconds,
                "recent_activity_level": 0.5,
                "fatigue_factor": 1 - emotional_state.get("emotional_energy", 1)
            }
        )

        # 5. Décision = choisir une action parmi le policy network
        state_tensor = unified_state["unified_state_vector"]
        state_tensor_t = (
            state_tensor.reshape(1, -1)
            if hasattr(state_tensor, "reshape")
            else state_tensor
        )

        state_tensor_t = state_tensor_t.astype("float32")
        import torch
        state_tensor_t = torch.tensor(state_tensor_t)

        _, action_probs = self.learning_engine(state_tensor_t)
        action_index = int(torch.argmax(action_probs, dim=-1).item())

        # Action choisie
        action_type = "text_response"  # pour le moment, la seule action
        text_to_generate = user_text

        # 6. Génération
        response_text = await self.generator.generate_response(
            user_text,
            {
                "identity": self.identity_core.export_identity(),
                "emotions": emotional_state,
                "memory_context": similar_memories,
                "concepts": understanding["concepts"]
            }
        )

        # 7. Firewall
        safety = self.ethical_firewall.validate_action(
            "text_response",
            {"text": response_text},
            {"understanding": understanding}
        )

        if not safety["is_safe"]:
            response_text = safety.get("required_modifications", {}).get(
                "text",
                "Je ne peux pas répondre à cela."
            )

        # 8. Mémoire
        await self.vector_memory.add_memory(
            understanding["embedding"],
            {
                "text": user_text,
                "emotional_valence": emotional_state.get("valence", 0.0)
            }
        )

        # 9. Stockage BDD
        await self.db.save_experience({
            "input_text": user_text,
            "understanding": understanding,
            "state_vector": unified_state["unified_state_vector"].tolist(),
            "decision": {"action": action_type},
            "reward": emotional_state.get("valence", 0)
        })

        return {
            "response": response_text,
            "emotions": emotional_state,
            "concepts": understanding["concepts"],
            "memory_used": len(similar_memories)
        }
