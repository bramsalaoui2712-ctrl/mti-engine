from mti_engine import (
    RobustCognitiveEngine,
    AdvancedEmotionalEngine,
    IdentityCore,
    RobustVectorMemory,
    ConsistentStateIntegrator,
    AdvancedEthicalFirewall,
    FunctionalLearningEngine,
    GenerationPipeline,
    AsyncCognitiveDatabase,
    AsyncActionModule
)

class CognitiveOrchestrator:
    """
    Orchestrateur central du MTI-Engine.
    Coordonne mémoire, compréhension, émotions, génération, apprentissage et sécurité.
    """

    def __init__(self):
        self.cognitive_engine = RobustCognitiveEngine()
        self.emotional_engine = AdvancedEmotionalEngine()
        self.identity_core = IdentityCore()
        self.vector_memory = RobustVectorMemory()
        self.state_integrator = ConsistentStateIntegrator()
        self.ethical_firewall = AdvancedEthicalFirewall()
        self.learning_engine = FunctionalLearningEngine()
        self.generation_pipeline = GenerationPipeline()
        self.db = AsyncCognitiveDatabase()
        self.action_module = AsyncActionModule()

    async def process_user_input(self, text: str) -> dict:
        """Pipeline complet pour un input utilisateur."""

        # 1 — Compréhension
        understanding = self.cognitive_engine.understand_text(text)

        # 2 — Recherche mémoire
        similar_memories = await self.vector_memory.search_similar(
            understanding['embedding'], k=5
        )

        # 3 — Traitement émotionnel
        emotional_state = self.emotional_engine.process_experience_emotionally(
            understanding,
            similar_memories
        )

        # 4 — Intégration état unifié
        state = self.state_integrator.integrate_complete_state(
            understanding,
            emotional_state,
            similar_memories,
            self.identity_core.__dict__,
            {"time_since_start": 10, "recent_activity_level": 0.5, "fatigue_factor": 0.1}
        )

        # 5 — Génération réponse
        response = await self.generation_pipeline.generate_response(
            text,
            {
                "identity": self.identity_core.__dict__,
                "emotions": emotional_state,
                "memory_context": similar_memories,
                "concepts": understanding.get("concepts", []),
                "understanding": understanding
            }
        )

        # 6 — Passer par le firewall
        safety = self.ethical_firewall.validate_action(
            "text_response",
            {"text": response},
            {"understanding": understanding, "identity_context": self.identity_core.__dict__}
        )

        if not safety["is_safe"]:
            response = safety["required_modifications"].get(
                "text", "Je ne peux pas répondre à cette demande."
            )

        # 7 — Ajouter en mémoire vectorielle
        await self.vector_memory.add_memory(
            understanding["embedding"],
            {"text": text, "emotional_valence": emotional_state["valence"]}
        )

        return {
            "response": response,
            "emotions": emotional_state,
            "memories_used": len(similar_memories),
            "safety": safety
        }
