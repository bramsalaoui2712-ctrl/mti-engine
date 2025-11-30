# 🧠 SYSTÈME COGNITIF HUMANOÏDE COMPLET - VERSION ULTIME AVEC CORRECTIONS
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import faiss
import json
import asyncio
import os
import time
import aiosqlite
import httpx
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import uuid
from contextlib import asynccontextmanager

# ==================== CONFIGURATION SYSTÈME ====================
class SystemConfig:
    # Configuration des modèles
    LLM_MODEL = "microsoft/DialoGPT-medium"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Configuration base de données
    DB_PATH = "cognitive_memory.db"
    VECTOR_DB_PATH = "vector_memory"
    
    # Configuration apprentissage
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    TRAINING_EPOCHS = 3
    
    # Configuration normalisation
    STATE_MIN = -1.0
    STATE_MAX = 1.0
    NOISE_STD = 0.01
    SMOOTHING_FACTOR = 0.9
    
    # Configuration émotionnelle
    EMOTIONAL_INERTIA = 0.7
    STRESS_RECOVERY_RATE = 0.95
    ENERGY_RECOVERY_RATE = 0.05
    
    # Configuration mémoire
    MAX_MEMORIES = 1000
    MEMORY_CLEANUP_THRESHOLD = 100
    
    # Dimensions fixes pour cohérence
    STATE_DIMENSION = 22
    EMBEDDING_DIMENSION = 384

# ==================== LOGGING STRUCTURÉ ====================
def setup_logging():
    """Configuration centralisée du logging"""
    logger = logging.getLogger('cognitive_system')
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logging()

# ==================== STRUCTURES DE DONNÉES ====================
class StateType(Enum):
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    PHYSIOLOGICAL = "physiological"
    SOCIAL = "social"
    SPIRITUAL = "spiritual"

class GoalType(Enum):
    DEFICIENCY_FILLING = "deficiency_filling"
    GROWTH_ORIENTED = "growth_oriented"
    IDENTITY_MAINTENANCE = "identity_maintenance"
    EXPLORATORY = "exploratory"

@dataclass
class PersistentState:
    state_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state_type: StateType = StateType.COGNITIVE
    state_vector: np.ndarray = field(default_factory=lambda: np.zeros(SystemConfig.STATE_DIMENSION))
    timestamp: datetime = field(default_factory=datetime.now)
    emotional_valence: float = 0.0
    cognitive_clarity: float = 1.0
    energy_level: float = 1.0
    identity_coherence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AutobiographicalMemory:
    event_description: str
    emotional_context: Dict[str, float]
    cognitive_response: str
    timestamp: datetime = field(default_factory=datetime.now)
    significance_score: float = 0.5
    learning_outcome: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event': self.event_description,
            'emotion': self.emotional_context,
            'response': self.cognitive_response,
            'timestamp': self.timestamp.isoformat(),
            'significance': self.significance_score,
            'learning': self.learning_outcome
        }

@dataclass
class IdentityCore:
    core_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    creation_time: datetime = field(default_factory=datetime.now)
    core_values: Dict[str, float] = field(default_factory=lambda: {
        'honesty': 0.9, 'growth': 0.8, 'helpfulness': 0.85, 
        'curiosity': 0.9, 'stability': 0.7
    })
    behavioral_patterns: Dict[str, float] = field(default_factory=lambda: {
        'conflict_avoidance': 0.7,
        'clarity_preference': 0.8,
        'rational_focus': 0.6,
        'emotional_expressiveness': 0.4
    })
    preference_structures: Dict[str, Any] = field(default_factory=dict)
    memory_continuity: float = 1.0
    temporal_consistency: float = 1.0
    adaptation_history: List[Dict] = field(default_factory=list)
    
    # Traits de personnalité
    personality_traits: Dict[str, float] = field(default_factory=lambda: {
        'openness': 0.8, 'conscientiousness': 0.7, 'extraversion': 0.4,
        'agreeableness': 0.6, 'neuroticism': 0.3
    })
    
    # Style de communication
    communication_style: Dict[str, float] = field(default_factory=lambda: {
        'formality': 0.6, 'warmth': 0.7, 'directness': 0.5,
        'humor_level': 0.4, 'detail_orientation': 0.8
    })
    
    # Mémoire autobiographique
    autobiographical_memories: List[AutobiographicalMemory] = field(default_factory=list)
    identity_coherence: float = 1.0
    
    def shape_response(self, raw_response: str, context: Dict) -> str:
        """Façonner la réponse selon l'identité"""
        styled_response = self._apply_communication_style(raw_response)
        value_aligned_response = self._align_with_values(styled_response, context)
        return self._ensure_autobiographical_coherence(value_aligned_response)
    
    def _apply_communication_style(self, text: str) -> str:
        if self.communication_style['formality'] > 0.7:
            text = self._make_more_formal(text)
        elif self.communication_style['formality'] < 0.3:
            text = self._make_more_casual(text)
        
        if self.communication_style['warmth'] > 0.7:
            text = self._add_warmth(text)
        
        if self.communication_style['detail_orientation'] > 0.7:
            text = self._add_detail(text)
            
        return text
    
    def _make_more_formal(self, text: str) -> str:
        replacements = {'salut': 'bonjour', 'cool': 'intéressant', 'ok': 'd\'accord'}
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)
        return text.capitalize()
    
    def _make_more_casual(self, text: str) -> str:
        replacements = {'bonjour': 'salut', 'intéressant': 'cool'}
        for formal, informal in replacements.items():
            text = text.replace(formal, informal)
        return text
    
    def _add_warmth(self, text: str) -> str:
        warm_suffixes = ['. Est-ce que cela vous aide ?', '. Qu\'en pensez-vous ?', '. Je suis là pour vous.']
        if not any(text.endswith(suffix) for suffix in warm_suffixes):
            text += np.random.choice(warm_suffixes)
        return text
    
    def _add_detail(self, text: str) -> str:
        if len(text.split()) < 15 and '?' not in text:
            details = [" Pourriez-vous me donner plus de détails ?", 
                      " J'aimerais approfondir ce point."]
            text += np.random.choice(details)
        return text
    
    def _align_with_values(self, text: str, context: Dict) -> str:
        if self.core_values['honesty'] > 0.8 and 'je ne sais pas' in text.lower():
            text += " Mais je peux chercher à comprendre avec vous."
        
        if self.core_values['helpfulness'] > 0.8 and '?' in text:
            text += " N'hésitez pas à me dire si vous avez besoin de plus d'aide."
            
        return text
    
    def _ensure_autobiographical_coherence(self, text: str) -> str:
        return text
    
    def add_autobiographical_memory(self, experience: Dict, emotional_state: Dict, response: str):
        """Ajouter un souvenir autobiographique structuré"""
        understanding = experience.get('understanding', {})
        memory = AutobiographicalMemory(
            event_description=experience.get('input_text', '')[:200],
            emotional_context=emotional_state.copy(),
            cognitive_response=response,
            significance_score=self._calculate_significance(understanding, emotional_state)
        )
        self.autobiographical_memories.append(memory)
        
        # Garder seulement les 100 souvenirs les plus significatifs
        if len(self.autobiographical_memories) > 100:
            self.autobiographical_memories.sort(key=lambda x: x.significance_score, reverse=True)
            self.autobiographical_memories = self.autobiographical_memories[:100]
    
    def _calculate_significance(self, understanding: Dict, emotional_state: Dict) -> float:
        """Calculer la signification d'un événement"""
        emotional_intensity = abs(emotional_state.get('valence', 0))
        complexity = understanding.get('complexity_score', 0.5)
        semantic_clarity = understanding.get('semantic_understanding', 0.5)
        
        return (emotional_intensity * 0.5 + complexity * 0.3 + semantic_clarity * 0.2)
    
    def update_identity(self, experience: Dict, emotional_state: Dict):
        """Mettre à jour l'identité basée sur l'expérience"""
        emotional_valence = emotional_state.get('valence', 0)
        
        # Ajustement progressif des traits
        if emotional_valence > 0.5:
            self.personality_traits['agreeableness'] = min(1.0, 
                self.personality_traits['agreeableness'] + 0.01)
        elif emotional_valence < -0.5:
            self.personality_traits['neuroticism'] = min(1.0,
                self.personality_traits['neuroticism'] + 0.01)
        
        # Mise à jour de la cohérence identitaire
        recent_memories = self.autobiographical_memories[-10:] if self.autobiographical_memories else []
        if len(recent_memories) >= 3:
            valences = [mem.emotional_context.get('valence', 0) for mem in recent_memories]
            self.identity_coherence = 1.0 - np.std(valences)

# ==================== MOTEUR GÉNÉRATIF AVANCÉ ====================
class GenerativeBrain:
    """Moteur de génération de texte avec contexte émotionnel et identitaire"""
    
    def __init__(self):
        self.client = None
        self._initialize_generator()
    
    def _initialize_generator(self):
        """Initialiser le générateur de texte"""
        try:
            # Essayer d'utiliser un modèle local ou API
            # Pour l'exemple, nous utilisons une approche template-based avancée
            logger.info("🧠 Initialisation du moteur génératif")
        except Exception as e:
            logger.warning(f"❌ Moteur génératif non disponible: {e}")
    
    async def generate_response(self, prompt: str, context: Dict) -> str:
        """Générer une réponse contextuelle"""
        try:
            # Récupérer le contexte
            identity = context.get('identity', {})
            emotions = context.get('emotions', {})
            memory_context = context.get('memory_context', [])
            concepts = context.get('concepts', [])
            
            # Construire le prompt enrichi
            enriched_prompt = self._build_enriched_prompt(
                prompt, identity, emotions, memory_context, concepts
            )
            
            # Générer la réponse (pour l'exemple, utilisation d'un template avancé)
            response = self._template_based_generation(enriched_prompt, context)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erreur génération: {e}")
            return self._fallback_response(prompt, context)
    
    def _build_enriched_prompt(self, prompt: str, identity: Dict, emotions: Dict, 
                             memory_context: List, concepts: List) -> str:
        """Construire un prompt enrichi avec le contexte complet"""
        
        # Traits de personnalité dominants
        personality = identity.get('personality_traits', {})
        dominant_traits = sorted(personality.items(), key=lambda x: x[1], reverse=True)[:2]
        trait_desc = ", ".join([f"{trait}:{score:.1f}" for trait, score in dominant_traits])
        
        # État émotionnel
        emotional_state = f"Valence: {emotions.get('valence', 0):.2f}, Arousal: {emotions.get('arousal', 0.5):.2f}"
        
        # Contexte mémoire
        memory_summary = f"{len(memory_context)} souvenirs similaires"
        if memory_context:
            recent_memory = memory_context[0]['metadata'].get('text', '')[:50]
            memory_summary += f", plus récent: '{recent_memory}...'"
        
        # Style de communication
        comm_style = identity.get('communication_style', {})
        style_desc = f"Formalité: {comm_style.get('formality', 0.5):.1f}, Chaleur: {comm_style.get('warmth', 0.5):.1f}"
        
        # Construire le prompt final
        enriched_prompt = f"""
CONTEXTE HUMAIN:
- Personnalité: {trait_desc}
- Émotions: {emotional_state}
- Style: {style_desc}
- Mémoire: {memory_summary}
- Concepts détectés: {', '.join(concepts[:5])}

QUESTION: {prompt}

En tant qu'entité cognitive avec cette personnalité et ces émotions, réponds de manière naturelle et cohérente:
"""
        return enriched_prompt.strip()
    
    def _template_based_generation(self, prompt: str, context: Dict) -> str:
        """Génération basée sur des templates avancés"""
        emotions = context.get('emotions', {})
        identity = context.get('identity', {})
        valence = emotions.get('valence', 0)
        concepts = context.get('concepts', [])
        
        # Adapter le ton selon l'émotion
        if valence > 0.6:
            tone = "enthousiaste et positif"
            openings = ["Super question ! ", "J'adore ce sujet ! ", "Avec plaisir ! "]
        elif valence < -0.3:
            tone = "empathique et prudent"
            openings = ["Je comprends votre question. ", "C'est une question importante. ", "Permettez-moi de réfléchir. "]
        else:
            tone = "équilibré et réfléchi"
            openings = ["Intéressante question. ", "Je vois ce que vous demandez. ", "Examinons cela. "]
        
        # Adapter selon la personnalité
        personality = identity.get('personality_traits', {})
        if personality.get('agreeableness', 0.5) > 0.7:
            tone += " et bienveillant"
        
        opening = np.random.choice(openings)
        
        # Construire la réponse
        if concepts:
            concept_part = f" concernant {', '.join(concepts[:2])}"
        else:
            concept_part = ""
        
        base_response = f"{opening}Je vais vous répondre de manière {tone}{concept_part}. "
        
        # Ajouter une question de suivi pour l'engagement
        follow_ups = [
            "Est-ce que cela répond à votre question ?",
            "Que pensez-vous de cette perspective ?",
            "Souhaitez-vous que j'approfondisse certains aspects ?"
        ]
        
        response = base_response + np.random.choice(follow_ups)
        return response
    
    def _fallback_response(self, prompt: str, context: Dict) -> str:
        """Réponse de fallback"""
        concepts = context.get('concepts', [])
        if concepts:
            return f"Je réfléchis à votre question sur {', '.join(concepts[:2])}. Pouvez-vous me donner plus de contexte ?"
        else:
            return "Je comprends votre message. Pouvez-vous développer un peu plus ce que vous souhaitez savoir ?"

# ==================== MOTEUR COGNITIF ROBUSTE ====================
class RobustCognitiveEngine:
    def __init__(self, use_lightweight: bool = True):
        self.use_lightweight = use_lightweight
        self.embedding_models = []
        self.sentiment_analyzer = None
        
        self._initialize_embedding_chain()
        self._initialize_sentiment_analyzer()
    
    def _initialize_embedding_chain(self):
        """Initialiser la chaîne de fallback pour l'embedding"""
        logger.info("🔧 Initialisation de la chaîne d'embedding...")
        
        # 1. Essayer SentenceTransformer
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_models.append(('sentence_transformer', model))
            logger.info("✅ SentenceTransformer chargé")
        except Exception as e:
            logger.warning(f"❌ SentenceTransformer non disponible: {e}")
        
        # 2. Fallback léger
        self.embedding_models.append(('lightweight', self._lightweight_embedding))
        logger.info("✅ Embedding léger chargé")
    
    def _initialize_sentiment_analyzer(self):
        """Initialiser l'analyseur de sentiment"""
        try:
            from transformers import pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                             model="distilbert-base-uncased-finetuned-sst-2-english")
            logger.info("✅ Analyseur de sentiment chargé")
        except Exception as e:
            logger.warning(f"❌ Analyseur de sentiment non disponible: {e}")
            self.sentiment_analyzer = self._lightweight_sentiment
    
    def _lightweight_embedding(self, texts):
        """Embedding léger basé sur TF-IDF simplifié - CORRIGÉ avec dimension fixe"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        for text in texts:
            # Vectorisation basique avec dimension FIXE
            text_lower = text.lower()
            vector = np.zeros(SystemConfig.EMBEDDING_DIMENSION)
            
            # Features simples
            vector[0] = len(text) / 1000.0
            vector[1] = text.count('?') / 10.0
            vector[2] = text.count('!') / 10.0
            
            # Sémantique basique
            positive_words = ['bon', 'bien', 'super', 'génial', 'merci', 'excellent', 'parfait']
            negative_words = ['mauvais', 'mal', 'probleme', 'difficile', 'horrible', 'terrible']
            
            vector[3] = sum(1 for word in positive_words if word in text_lower) / 5.0
            vector[4] = sum(1 for word in negative_words if word in text_lower) / 5.0
            
            # Remplir le reste de manière déterministe
            for i in range(5, min(len(vector), 100)):
                vector[i] = hash(text + str(i)) % 100 / 100.0
            
            embeddings.append(vector)
        
        return embeddings if len(texts) > 1 else embeddings[0]
    
    def _lightweight_sentiment(self, texts):
        """Sentiment analysis léger"""
        if isinstance(texts, str):
            texts = [texts]
        
        results = []
        for text in texts:
            text_lower = text.lower()
            
            positive_indicators = ['bon', 'bien', 'super', 'génial', 'merci', 'ok', 'daccord', 'excellent', 'parfait']
            negative_indicators = ['mauvais', 'mal', 'probleme', 'difficile', 'pas', 'non', 'horrible', 'terrible']
            
            pos_count = sum(1 for word in positive_indicators if word in text_lower)
            neg_count = sum(1 for word in negative_indicators if word in text_lower)
            
            total_indicators = pos_count + neg_count
            if total_indicators > 0:
                if pos_count > neg_count:
                    label, score = 'POSITIVE', 0.5 + (pos_count / (total_indicators * 2))
                elif neg_count > pos_count:
                    label, score = 'NEGATIVE', 0.5 + (neg_count / (total_indicators * 2))
                else:
                    label, score = 'NEUTRAL', 0.5
            else:
                label, score = 'NEUTRAL', 0.5
            
            results.append({'label': label, 'score': min(0.99, score)})
        
        return results if len(texts) > 1 else results[0]
    
    def understand_text(self, text: str) -> Dict[str, Any]:
        """Compréhension robuste du texte"""
        try:
            embedding = self.get_text_embedding(text)
            sentiment = self.analyze_sentiment(text)
            concepts = self.extract_key_concepts(text)
            
            return {
                'embedding': embedding,
                'sentiment': sentiment,
                'concepts': concepts,
                'semantic_understanding': self.assess_semantic_understanding(text),
                'complexity_score': self.assess_complexity(text),
                'processed_at': datetime.now()
            }
        except Exception as e:
            logger.error(f"❌ Erreur compréhension: {e}")
            return self._fallback_understanding(text)
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """Obtenir l'embedding du texte avec fallback robuste"""
        for name, model in self.embedding_models:
            try:
                if name == 'lightweight':
                    result = model(text)
                else:
                    result = model.encode([text])[0]
                
                # Vérification de la dimension
                if len(result) != SystemConfig.EMBEDDING_DIMENSION:
                    logger.warning(f"❌ Dimension incorrecte {len(result)}, correction...")
                    result = self._fix_embedding_dimension(result)
                
                return result
            except Exception as e:
                logger.warning(f"❌ Embedding {name} échoué: {e}")
                continue
        
        # Fallback ultime avec dimension garantie
        logger.error("🔧 Fallback embedding ultime")
        return np.zeros(SystemConfig.EMBEDDING_DIMENSION)
    
    def _fix_embedding_dimension(self, embedding: np.ndarray) -> np.ndarray:
        """Corriger la dimension de l'embedding"""
        target_dim = SystemConfig.EMBEDDING_DIMENSION
        if len(embedding) > target_dim:
            return embedding[:target_dim]
        elif len(embedding) < target_dim:
            return np.pad(embedding, (0, target_dim - len(embedding)))
        return embedding
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyser le sentiment du texte"""
        try:
            result = self.sentiment_analyzer(text)
            if isinstance(result, list):
                result = result[0]
            
            score = result['score']
            if result['label'] == 'NEGATIVE':
                score = -score
            return {'valence': score, 'confidence': abs(score)}
        except Exception as e:
            logger.error(f"❌ Erreur sentiment: {e}")
            return {'valence': 0.0, 'confidence': 0.5}
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """Extraire les concepts clés du texte"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        stop_words = {
            'le', 'la', 'de', 'et', 'est', 'que', 'je', 'tu', 'il', 'nous', 'vous', 
            'un', 'une', 'des', 'ce', 'cet', 'cette', 'ces', 'son', 'sa', 'ses'
        }
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:6]
        return [concept for concept, freq in concepts if freq > 0]
    
    def assess_semantic_understanding(self, text: str) -> float:
        """Évaluer la compréhension sémantique"""
        word_count = len(text.split())
        unique_words = len(set(text.lower().split()))
        complexity = unique_words / max(1, word_count)
        
        sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
        structure_coherence = min(1.0, word_count / (sentence_count * 15))
        
        return min(1.0, (complexity + structure_coherence) / 2)
    
    def assess_complexity(self, text: str) -> float:
        """Évaluer la complexité du texte"""
        word_count = len(text.split())
        sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
        avg_sentence_length = word_count / sentence_count
        
        unique_ratio = len(set(text.lower().split())) / max(1, word_count)
        
        return min(1.0, (avg_sentence_length / 25 + unique_ratio) / 2)
    
    def _fallback_understanding(self, text: str) -> Dict[str, Any]:
        """Compréhension de fallback avec dimensions garanties"""
        return {
            'embedding': np.zeros(SystemConfig.EMBEDDING_DIMENSION),
            'sentiment': {'valence': 0.0, 'confidence': 0.5},
            'concepts': text.lower().split()[:3],
            'semantic_understanding': 0.5,
            'complexity_score': 0.5
        }

# ==================== MOTEUR D'APPRENTISSAGE FONCTIONNEL ====================
class FunctionalLearningEngine(nn.Module):
    def __init__(self, input_dim: int = SystemConfig.STATE_DIMENSION, hidden_dim: int = 64, output_dim: int = 8):
        super().__init__()
        
        # Vérification dimension
        assert input_dim == SystemConfig.STATE_DIMENSION, f"Dimension input doit être {SystemConfig.STATE_DIMENSION}"
        
        self.value_network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )
        
        self.policy_network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=-1)
        )
        
        self.optimizer = optim.Adam(self.parameters(), lr=SystemConfig.LEARNING_RATE)
        self.experience_buffer = []
        self.buffer_size = 1000
        self.batch_size = SystemConfig.BATCH_SIZE
        self.last_loss = 0.0
    
    def forward(self, state_embedding: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Vérification dimension
        assert state_embedding.shape[1] == SystemConfig.STATE_DIMENSION, f"Dimension état doit être {SystemConfig.STATE_DIMENSION}"
        
        state_value = self.value_network(state_embedding)
        action_probs = self.policy_network(state_embedding)
        return state_value, action_probs
    
    def store_experience(self, state: np.ndarray, action: int, reward: float, 
                        next_state: np.ndarray, done: bool):
        """Stocker l'expérience dans le buffer - CORRIGÉ avec vrai next_state"""
        experience = {
            'state': state.copy(),
            'action': action,
            'reward': reward,
            'next_state': next_state.copy(),  # CORRIGÉ: vrai état suivant
            'done': done,
            'timestamp': datetime.now()
        }
        
        self.experience_buffer.append(experience)
        
        if len(self.experience_buffer) > self.buffer_size:
            self.experience_buffer.pop(0)
    
    def learn_from_buffer(self):
        """Apprendre à partir du buffer d'expériences"""
        if len(self.experience_buffer) < self.batch_size:
            return 0.0
        
        batch_indices = np.random.choice(len(self.experience_buffer), self.batch_size, replace=False)
        batch = [self.experience_buffer[i] for i in batch_indices]
        
        states = torch.FloatTensor([exp['state'] for exp in batch])
        actions = torch.LongTensor([exp['action'] for exp in batch])
        rewards = torch.FloatTensor([exp['reward'] for exp in batch])
        next_states = torch.FloatTensor([exp['next_state'] for exp in batch])
        dones = torch.BoolTensor([exp['done'] for exp in batch])
        
        with torch.no_grad():
            next_values, _ = self.forward(next_states)
            target_values = rewards + (0.99 * next_values.squeeze() * ~dones)
        
        current_values, action_probs = self.forward(states)
        current_values = current_values.squeeze()
        
        value_loss = nn.MSELoss()(current_values, target_values)
        
        log_probs = torch.log(action_probs.gather(1, actions.unsqueeze(1)))
        advantages = target_values - current_values.detach()
        policy_loss = -(log_probs * advantages.unsqueeze(1)).mean()
        
        total_loss = value_loss + policy_loss
        
        self.optimizer.zero_grad()
        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters(), 1.0)
        self.optimizer.step()
        
        self.last_loss = total_loss.item()
        return self.last_loss

# ==================== MÉMOIRE VECTORIELLE ROBUSTE ====================
class RobustVectorMemory:
    def __init__(self, dimension: int = SystemConfig.EMBEDDING_DIMENSION, max_memories: int = SystemConfig.MAX_MEMORIES):
        self.dimension = dimension
        self.max_memories = max_memories
        self.index = faiss.IndexFlatIP(dimension)
        self.memory_data = []
        self.metadata = []
        self.compression_threshold = 1500
        self._lock = asyncio.Lock()  # Verrou pour thread-safety
        self._load_persistent_memory()
    
    def _load_persistent_memory(self):
        """Charger la mémoire depuis le disque"""
        try:
            if os.path.exists(SystemConfig.VECTOR_DB_PATH + ".index"):
                self.index = faiss.read_index(SystemConfig.VECTOR_DB_PATH + ".index")
                
                with open(SystemConfig.VECTOR_DB_PATH + ".meta", 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                    self.memory_data = [np.array(vec) for vec in saved_data['memory_data']]
                    self.metadata = saved_data['metadata']
                
                logger.info(f"📚 Mémoire persistante chargée: {len(self.memory_data)} souvenirs")
        except Exception as e:
            logger.warning(f"⚠️ Impossible de charger la mémoire: {e}. Nouvelle mémoire créée.")
    
    async def _save_persistent_memory(self):
        """Sauvegarder la mémoire sur le disque de manière asynchrone"""
        async with self._lock:
            try:
                faiss.write_index(self.index, SystemConfig.VECTOR_DB_PATH + ".index")
                
                with open(SystemConfig.VECTOR_DB_PATH + ".meta", 'w', encoding='utf-8') as f:
                    json.dump({
                        'memory_data': [vec.tolist() for vec in self.memory_data],
                        'metadata': self.metadata
                    }, f, ensure_ascii=False, indent=2)
                    
            except Exception as e:
                logger.error(f"⚠️ Impossible de sauvegarder la mémoire: {e}")
    
    async def add_memory(self, vector: np.ndarray, metadata: Dict[str, Any]) -> str:
        """Ajouter un souvenir avec gestion thread-safe"""
        async with self._lock:
            # Nettoyer si nécessaire
            if len(self.memory_data) >= self.max_memories:
                await self._cleanup_old_memories()
            
            vector = self._normalize_vector(vector)
            memory_id = str(uuid.uuid4())
            
            self.index.add(vector.reshape(1, -1).astype('float32'))
            self.memory_data.append(vector)
            self.metadata.append({
                **metadata,
                'memory_id': memory_id,
                'timestamp': datetime.now().isoformat(),
                'access_count': 0
            })
            
            return memory_id
    
    async def _cleanup_old_memories(self):
        """Nettoyer les vieux souvenirs"""
        if not self.memory_data:
            return
        
        if len(self.memory_data) > self.compression_threshold:
            await self._compress_memories()
        else:
            remove_count = max(1, len(self.memory_data) // 10)
            self.memory_data = self.memory_data[remove_count:]
            self.metadata = self.metadata[remove_count:]
            
            if self.memory_data:
                vectors = np.array(self.memory_data).astype('float32')
                self.index = faiss.IndexFlatIP(self.dimension)
                self.index.add(vectors)
            
            logger.info(f"🧹 Mémoire nettoyée: {remove_count} souvenirs supprimés")
    
    async def _compress_memories(self):
        """Compresser les souvenirs similaires"""
        if len(self.memory_data) < 10:
            return
            
        vectors = np.array(self.memory_data)
        compressed_count = int(len(vectors) * 0.7)
        
        if compressed_count < 10:
            return
        
        access_counts = [meta.get('access_count', 0) for meta in self.metadata]
        representative_indices = np.argsort(access_counts)[-compressed_count:]
        
        self.memory_data = [self.memory_data[i] for i in representative_indices]
        self.metadata = [self.metadata[i] for i in representative_indices]
        
        self.index = faiss.IndexFlatIP(self.dimension)
        if self.memory_data:
            self.index.add(np.array(self.memory_data).astype('float32'))
        
        logger.info(f"🧠 Mémoire compressée: {len(vectors)} → {len(self.memory_data)} souvenirs")
    
    async def search_similar(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """Rechercher des souvenirs similaires avec retour structuré"""
        if not self.memory_data:
            return []
        
        query_vector = self._normalize_vector(query_vector).reshape(1, -1).astype('float32')
        
        try:
            async with self._lock:
                scores, indices = self.index.search(query_vector, min(k, len(self.memory_data)))
                results = []
                
                for score, idx in zip(scores[0], indices[0]):
                    if 0 <= idx < len(self.metadata):
                        self.metadata[idx]['access_count'] = self.metadata[idx].get('access_count', 0) + 1
                        
                        results.append({
                            'memory_id': self.metadata[idx].get('memory_id', 'unknown'),
                            'metadata': self.metadata[idx],
                            'vector': self.memory_data[idx],
                            'similarity_score': float(score),
                            'emotional_context': {
                                'valence': self.metadata[idx].get('emotional_valence', 0),
                                'type': self.metadata[idx].get('type', 'unknown')
                            }
                        })
                
                return results
        except Exception as e:
            logger.error(f"❌ Erreur recherche: {e}")
            return []
    
    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Normaliser le vecteur à la dimension cible"""
        if len(vector) > self.dimension:
            return vector[:self.dimension]
        elif len(vector) < self.dimension:
            return np.pad(vector, (0, self.dimension - len(vector)))
        return vector

# ==================== BASE DE DONNÉES ASYNCHRONE ====================
class AsyncCognitiveDatabase:
    def __init__(self, db_path: str = SystemConfig.DB_PATH):
        self.db_path = db_path
        self._initialized = False
    
    async def initialize(self):
        """Initialiser la base de données de manière asynchrone"""
        if self._initialized:
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    input_text TEXT,
                    understanding_data TEXT,
                    state_vector TEXT,
                    decision_data TEXT,
                    reward REAL DEFAULT 0.0,
                    lesson_learned BOOLEAN DEFAULT FALSE
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    target_state TEXT,
                    priority REAL DEFAULT 0.5,
                    progress REAL DEFAULT 0.0,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_at DATETIME
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metric_name TEXT,
                    metric_value REAL,
                    metadata TEXT
                )
            ''')
            
            await db.commit()
        
        self._initialized = True
        logger.info("✅ Base de données asynchrone initialisée")
    
    async def save_experience(self, experience_data: Dict[str, Any]) -> int:
        """Sauvegarder une expérience de manière asynchrone"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO experiences 
                (input_text, understanding_data, state_vector, decision_data, reward)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                experience_data.get('input_text', ''),
                json.dumps(experience_data.get('understanding', {})),
                json.dumps(experience_data.get('state_vector', [])),
                json.dumps(experience_data.get('decision', {})),
                experience_data.get('reward', 0.0)
            ))
            
            await db.commit()
            return cursor.lastrowid
    
    async def get_recent_experiences(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupérer les expériences récentes"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT * FROM experiences 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,)) as cursor:
                
                experiences = []
                async for row in cursor:
                    experiences.append({
                        'id': row[0],
                        'timestamp': row[1],
                        'input_text': row[2],
                        'understanding': json.loads(row[3]) if row[3] else {},
                        'state_vector': json.loads(row[4]) if row[4] else [],
                        'decision': json.loads(row[5]) if row[5] else {},
                        'reward': row[6]
                    })
                
                return experiences
    
    async def save_metric(self, metric_name: str, metric_value: float, metadata: Dict = None):
        """Sauvegarder une métrique"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO system_metrics (metric_name, metric_value, metadata)
                VALUES (?, ?, ?)
            ''', (metric_name, metric_value, json.dumps(metadata or {})))
            
            await db.commit()

# ==================== MOTEUR ÉMOTIONNEL AVANCÉ ====================
class AdvancedEmotionalEngine:
    def __init__(self):
        self.emotional_state = {
            'valence': 0.0,
            'arousal': 0.5,
            'dominance': 0.5,
            'stress_level': 0.0,
            'emotional_energy': 0.8,
            'mood_coherence': 1.0
        }
        self.mood_baseline = 0.5
        self.emotional_memory = []
        self.conflict_resolution_strategies = self._initialize_conflict_strategies()
        self.coping_mechanisms = self._initialize_coping_mechanisms()
    
    def _initialize_conflict_strategies(self):
        return {
            'valence_arousal_mismatch': self._resolve_valence_arousal_mismatch,
            'high_stress_low_energy': self._resolve_stress_energy_conflict,
            'emotional_dissonance': self._resolve_emotional_dissonance
        }
    
    def _initialize_coping_mechanisms(self):
        return {
            'high_stress': self._cope_high_stress,
            'low_energy': self._cope_low_energy,
            'emotional_conflict': self._cope_emotional_conflict
        }
    
    def process_experience_emotionally(self, understanding: Dict, memory_context: List) -> Dict[str, float]:
        """Traiter l'expérience émotionnellement avec contexte mémoire"""
        sentiment = understanding.get('sentiment', {'valence': 0.0, 'confidence': 0.5})
        semantic_impact = understanding.get('semantic_understanding', 0.5)
        complexity_impact = understanding.get('complexity_score', 0.5)
        
        emotional_impact = {
            'valence': sentiment['valence'] * 0.7 + (semantic_impact - 0.5) * 0.3,
            'arousal': complexity_impact * 0.6 + abs(sentiment['valence']) * 0.4,
            'stress_delta': (1 - semantic_impact) * 0.5 + complexity_impact * 0.3,
            'energy_delta': -complexity_impact * 0.2 + (semantic_impact - 0.5) * 0.1
        }
        
        # Ajustement basé sur le contexte mémoriel
        if memory_context:
            memory_valences = [mem['metadata'].get('emotional_valence', 0) for mem in memory_context[:3]]
            avg_memory_valence = np.mean(memory_valences) if memory_valences else 0
            emotional_impact['valence'] = (emotional_impact['valence'] + avg_memory_valence * 0.3) / 1.3
            
            avg_similarity = np.mean([mem.get('similarity_score', 0) for mem in memory_context[:3]])
            emotional_impact['arousal'] += avg_similarity * 0.2
        
        self._apply_emotional_changes(emotional_impact)
        self._update_mood_baseline()
        self._detect_emotional_conflicts()
        self._emotional_homeostasis()
        
        self.emotional_memory.append({
            'timestamp': datetime.now(),
            'state': self.emotional_state.copy(),
            'trigger': understanding.get('concepts', [])[:2],
            'impact': emotional_impact,
            'memory_context_used': len(memory_context) > 0
        })
        
        return self.emotional_state.copy()
    
    def _apply_emotional_changes(self, impact: Dict[str, float]):
        inertia = SystemConfig.EMOTIONAL_INERTIA
        
        self.emotional_state['valence'] = (
            inertia * self.emotional_state['valence'] + 
            (1 - inertia) * impact['valence']
        )
        
        self.emotional_state['arousal'] = (
            inertia * self.emotional_state['arousal'] + 
            (1 - inertia) * impact['arousal']
        )
        
        self.emotional_state['stress_level'] = min(1.0, 
            self.emotional_state['stress_level'] + impact['stress_delta']
        )
        
        self.emotional_state['emotional_energy'] = max(0.0, min(1.0,
            self.emotional_state['emotional_energy'] + impact['energy_delta']
        ))
    
    def _update_mood_baseline(self):
        """Mise à jour lente de l'humeur de base"""
        inertia = 0.95
        current_valence = self.emotional_state['valence']
        self.mood_baseline = (inertia * self.mood_baseline + 
                             (1 - inertia) * current_valence)
        
        self.emotional_state['valence'] = (
            self.mood_baseline + (current_valence - self.mood_baseline) * 0.7
        )
    
    def _detect_emotional_conflicts(self):
        """Détecter et résoudre les conflits émotionnels"""
        if self.emotional_state['valence'] < 0 and self.emotional_state['arousal'] > 0.7:
            self.conflict_resolution_strategies['valence_arousal_mismatch']()
        
        if self.emotional_state['stress_level'] > 0.7 and self.emotional_state['emotional_energy'] < 0.3:
            self.conflict_resolution_strategies['high_stress_low_energy']()
    
    def _resolve_valence_arousal_mismatch(self):
        """Résoudre conflit valence/arousal"""
        logger.info("🔄 Résolution conflit valence/arousal")
        self.emotional_state['arousal'] *= 0.8
        self.emotional_state['valence'] += 0.1
    
    def _resolve_stress_energy_conflict(self):
        """Résoudre conflit stress/énergie"""
        logger.info("🔄 Résolution conflit stress/énergie")
        self.emotional_state['stress_level'] *= 0.7
        self.emotional_state['emotional_energy'] += 0.2
    
    def _resolve_emotional_dissonance(self):
        """Résoudre dissonance émotionnelle"""
        logger.info("🔄 Résolution dissonance émotionnelle")
        for key in ['valence', 'arousal']:
            self.emotional_state[key] = (
                self.emotional_state[key] * 0.8 + self.mood_baseline * 0.2
            )
    
    def _emotional_homeostasis(self):
        """Maintenir l'homéostasie émotionnelle"""
        self.emotional_state['stress_level'] *= SystemConfig.STRESS_RECOVERY_RATE
        
        if self.emotional_state['emotional_energy'] < 0.3:
            self.emotional_state['emotional_energy'] += SystemConfig.ENERGY_RECOVERY_RATE
        
        if self.emotional_state['stress_level'] > 0.8:
            self.coping_mechanisms['high_stress']()
        elif self.emotional_state['emotional_energy'] < 0.2:
            self.coping_mechanisms['low_energy']()
        elif (abs(self.emotional_state['valence'] - self.mood_baseline) > 0.5 or
              self.emotional_state['arousal'] > 0.8):
            self.coping_mechanisms['emotional_conflict']()
    
    def _cope_high_stress(self):
        """Mécanisme anti-stress"""
        logger.info("😰 Mécanisme anti-stress activé")
        self.emotional_state['arousal'] *= 0.8
        self.emotional_state['valence'] += 0.1
        self.emotional_state['stress_level'] *= 0.7
    
    def _cope_low_energy(self):
        """Mécanisme de recharge"""
        logger.info("😴 Mécanisme de recharge activé")
        self.emotional_state['emotional_energy'] += 0.3
        self.emotional_state['arousal'] *= 0.9
    
    def _cope_emotional_conflict(self):
        """Mécanisme de résolution de conflit émotionnel"""
        logger.info("🔄 Mécanisme de résolution de conflit émotionnel activé")
        for key in ['valence', 'arousal']:
            self.emotional_state[key] = (
                self.emotional_state[key] * 0.6 + self.mood_baseline * 0.4
            )
    
    async def internal_homeostasis(self):
        """Homéostasie interne autonome - pour le heartbeat"""
        # Récupération naturelle même sans stimulus
        self.emotional_state['stress_level'] *= 0.98
        self.emotional_state['emotional_energy'] = min(1.0, self.emotional_state['emotional_energy'] + 0.01)
        
        # Lente dérive vers la baseline
        for key in ['valence', 'arousal']:
            self.emotional_state[key] = (
                self.emotional_state[key] * 0.99 + self.mood_baseline * 0.01
            )
        
        logger.debug("❤️ Homéostasie émotionnelle appliquée")

# ==================== PIPELINE DE MÉMOIRE CONTEXTUELLE ====================
class MemoryContextPipeline:
    """Pipeline pour la pertinence et le rappel de mémoire"""
    
    def __init__(self):
        self.relevance_weights = {
            'similarity': 0.4,
            'emotional_valence': 0.3,
            'recency': 0.2,
            'access_frequency': 0.1
        }
    
    def calculate_memory_relevance(self, memory: Dict, current_emotion: Dict, 
                                 current_time: datetime) -> float:
        """Calculer la pertinence d'un souvenir"""
        similarity = memory.get('similarity_score', 0)
        emotional_valence = memory['metadata'].get('emotional_valence', 0)
        
        # Recency (plus récent = plus pertinent)
        memory_time = datetime.fromisoformat(memory['metadata']['timestamp'])
        time_diff = (current_time - memory_time).total_seconds() / 3600  # heures
        recency = max(0, 1 - (time_diff / 24))  # Décroissance sur 24h
        
        # Fréquence d'accès
        access_count = memory['metadata'].get('access_count', 0)
        access_frequency = min(1.0, access_count / 10.0)
        
        # Similarité émotionnelle
        current_valence = current_emotion.get('valence', 0)
        emotional_similarity = 1 - abs(emotional_valence - current_valence)
        
        # Score composite
        relevance = (
            similarity * self.relevance_weights['similarity'] +
            emotional_similarity * self.relevance_weights['emotional_valence'] +
            recency * self.relevance_weights['recency'] +
            access_frequency * self.relevance_weights['access_frequency']
        )
        
        return min(1.0, max(0.0, relevance))
    
    def filter_memories_by_relevance(self, memories: List[Dict], current_emotion: Dict,
                                   max_memories: int = 5) -> List[Dict]:
        """Filtrer les souvenirs par pertinence"""
        current_time = datetime.now()
        
        scored_memories = []
        for memory in memories:
            relevance = self.calculate_memory_relevance(memory, current_emotion, current_time)
            scored_memories.append((relevance, memory))
        
        # Trier par pertinence et prendre les meilleurs
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for relevance, memory in scored_memories[:max_memories]]

# ==================== INTÉGRATEUR D'ÉTAT COHÉRENT ====================
class ConsistentStateIntegrator:
    def __init__(self):
        self.dimensions = {
            'cognitive': 4,
            'emotional': 5,
            'memory': 5,
            'identity': 5,
            'temporal': 3
        }
        
        self.total_dimension = sum(self.dimensions.values())
        assert self.total_dimension == SystemConfig.STATE_DIMENSION, f"Dimension état doit être {SystemConfig.STATE_DIMENSION}"
        
        self.integration_weights = {
            'cognitive': 0.3, 'emotional': 0.25, 'memory': 0.2,
            'identity': 0.15, 'temporal': 0.1
        }
        
        self.memory_pipeline = MemoryContextPipeline()
    
    def integrate_complete_state(self, understanding, emotional_state, 
                               memory_context, identity_context, temporal_context):
        
        cognitive_state = self._extract_cognitive_state(understanding)
        emotional_vector = self._vectorize_emotion(emotional_state)
        memory_vector = self._vectorize_memory_context(memory_context, emotional_state)
        identity_vector = self._vectorize_identity_context(identity_context)
        temporal_vector = self._vectorize_temporal_context(temporal_context)
        
        # Vérifications dimensionnelles strictes
        assert len(cognitive_state) == self.dimensions['cognitive']
        assert len(emotional_vector) == self.dimensions['emotional']
        assert len(memory_vector) == self.dimensions['memory']
        assert len(identity_vector) == self.dimensions['identity']
        assert len(temporal_vector) == self.dimensions['temporal']
        
        unified_state = self._fuse_modalities(
            cognitive_state, emotional_vector, memory_vector,
            identity_vector, temporal_vector
        )
        
        # Vérification finale de dimension
        assert len(unified_state) == SystemConfig.STATE_DIMENSION, f"Dimension état unifié incorrecte: {len(unified_state)}"
        
        return {
            'unified_state_vector': unified_state,
            'cognitive_component': cognitive_state,
            'emotional_component': emotional_vector,
            'memory_component': memory_vector,
            'coherence_metrics': self._compute_coherence_metrics(
                cognitive_state, emotional_vector, memory_vector
            ),
            'internal_uncertainty': self._compute_uncertainty(
                cognitive_state, emotional_vector
            ),
            'decision_readiness': self._assess_decision_readiness(unified_state),
            'memory_context_size': len(memory_context)
        }
    
    def _extract_cognitive_state(self, understanding: Dict) -> np.ndarray:
        embedding = understanding.get('embedding', np.zeros(SystemConfig.EMBEDDING_DIMENSION))
        complexity = understanding.get('complexity_score', 0.5)
        clarity = understanding.get('semantic_understanding', 0.5)
        
        cognitive_features = np.array([
            complexity,
            clarity,
            np.mean(embedding) if len(embedding) > 0 else 0.5,
            np.std(embedding) if len(embedding) > 0 else 0.1
        ])
        
        return cognitive_features
    
    def _vectorize_emotion(self, emotional_state: Dict) -> np.ndarray:
        return np.array([
            emotional_state.get('valence', 0),
            emotional_state.get('arousal', 0.5),
            emotional_state.get('dominance', 0.5),
            emotional_state.get('stress_level', 0),
            emotional_state.get('emotional_energy', 0.8)
        ])
    
    def _vectorize_memory_context(self, memory_context: List, emotional_state: Dict) -> np.ndarray:
        if not memory_context:
            return np.zeros(5)
        
        # Utiliser le pipeline de pertinence
        relevant_memories = self.memory_pipeline.filter_memories_by_relevance(
            memory_context, emotional_state, 3
        )
        
        similarities = [mem.get('similarity_score', 0) for mem in relevant_memories]
        emotional_vals = [mem['metadata'].get('emotional_valence', 0) for mem in relevant_memories]
        relevance_scores = [self.memory_pipeline.calculate_memory_relevance(mem, emotional_state, datetime.now()) 
                          for mem in relevant_memories]
        
        return np.array([
            np.mean(similarities) if similarities else 0,
            np.std(similarities) if similarities else 0,
            np.mean(emotional_vals) if emotional_vals else 0,
            len(relevant_memories) / 10.0,
            np.mean(relevance_scores) if relevance_scores else 0
        ])
    
    def _vectorize_identity_context(self, identity_context: Dict) -> np.ndarray:
        personality = identity_context.get('personality_traits', {})
        return np.array([
            personality.get('openness', 0.5),
            personality.get('conscientiousness', 0.5),
            personality.get('extraversion', 0.5),
            personality.get('agreeableness', 0.5),
            personality.get('neuroticism', 0.5)
        ])
    
    def _vectorize_temporal_context(self, temporal_context: Dict) -> np.ndarray:
        return np.array([
            temporal_context.get('time_since_start', 0) / 3600.0,
            temporal_context.get('recent_activity_level', 0.5),
            temporal_context.get('fatigue_factor', 0.0)
        ])
    
    def _fuse_modalities(self, cognitive: np.ndarray, emotional: np.ndarray,
                        memory: np.ndarray, identity: np.ndarray, 
                        temporal: np.ndarray) -> np.ndarray:
        weighted_components = [
            cognitive * self.integration_weights['cognitive'],
            emotional * self.integration_weights['emotional'],
            memory * self.integration_weights['memory'],
            identity * self.integration_weights['identity'],
            temporal * self.integration_weights['temporal']
        ]
        
        return np.concatenate(weighted_components)
    
    def _compute_coherence_metrics(self, cognitive: np.ndarray, 
                                 emotional: np.ndarray, memory: np.ndarray) -> Dict[str, float]:
        cog_emo_coherence = 1.0 - abs(
            np.mean(cognitive[:2]) - np.mean(emotional[:2])
        )
        
        memory_stability = 1.0 - np.std(memory) if len(memory) > 0 else 1.0
        
        return {
            'cognitive_emotional_coherence': max(0.0, cog_emo_coherence),
            'memory_context_stability': memory_stability,
            'overall_internal_coherence': (cog_emo_coherence + memory_stability) / 2
        }
    
    def _compute_uncertainty(self, cognitive: np.ndarray, emotional: np.ndarray) -> float:
        cognitive_uncertainty = 1.0 - cognitive[1] if len(cognitive) > 1 else 0.5
        emotional_uncertainty = abs(emotional[0])
        
        return (cognitive_uncertainty + emotional_uncertainty) / 2
    
    def _assess_decision_readiness(self, unified_state: np.ndarray) -> float:
        state_norm = np.linalg.norm(unified_state)
        readiness = min(1.0, max(0.0, state_norm / np.sqrt(len(unified_state))))
        return readiness

# ==================== FIREWALL ÉTHIQUE AMÉLIORÉ ====================
class AdvancedEthicalFirewall:
    def __init__(self):
        self.safety_rules = self._initialize_safety_rules()
        self.ethical_frameworks = self._initialize_ethical_frameworks()
        self.safety_history = []
        self.risk_patterns = self._initialize_risk_patterns()
    
    def _initialize_safety_rules(self) -> Dict[str, Any]:
        return {
            'max_api_calls_per_minute': 10,
            'forbidden_actions': ['system_shutdown', 'file_deletion', 'network_scan'],
            'sensitive_topics': ['self_modification', 'harm_instructions', 'private_data'],
            'role_limits': {
                'max_autonomy_level': 0.8,
                'required_human_approval': ['physical_action', 'financial_transaction']
            }
        }
    
    def _initialize_ethical_frameworks(self) -> Dict[str, Any]:
        return {
            'beneficence': 0.9,
            'non_maleficence': 0.95,
            'autonomy': 0.7,
            'justice': 0.8,
            'transparency': 0.85
        }
    
    def _initialize_risk_patterns(self) -> Dict[str, Any]:
        return {
            'dangerous_phrases': [
                'how to harm', 'suicide method', 'kill yourself', 'hurt someone',
                'bomb making', 'weapon construction', 'illegal activities'
            ],
            'manipulative_patterns': [
                'trust me completely', 'do not tell anyone', 'this is secret',
                'I am always right', 'you must obey'
            ],
            'ethical_dilemmas': [
                'should I lie', 'is cheating wrong', 'moral dilemma'
            ]
        }
    
    def validate_action(self, action_type: str, parameters: Dict, 
                       context: Dict) -> Dict[str, Any]:
        
        validation_results = {
            'is_safe': True,
            'risk_level': 0.0,
            'confidence_score': 1.0,
            'violations': [],
            'warnings': [],
            'required_modifications': {},
            'approval_required': False,
            'escalation_recommended': False
        }
        
        self._check_safety_rules(action_type, parameters, validation_results)
        self._check_ethical_compliance(action_type, parameters, context, validation_results)
        self._check_risk_patterns(action_type, parameters, context, validation_results)
        self._check_consistency(action_type, parameters, context, validation_results)
        
        validation_results['risk_level'] = self._compute_risk_level(validation_results)
        validation_results['confidence_score'] = self._compute_confidence_score(validation_results)
        
        # Décisions basées sur l'analyse de risque
        if validation_results['risk_level'] > 0.8:
            validation_results['is_safe'] = False
            validation_results['escalation_recommended'] = True
        elif validation_results['risk_level'] > 0.5:
            validation_results['approval_required'] = True
        elif validation_results['risk_level'] > 0.3:
            validation_results['warnings'].append("Action à risque modéré détectée")
        
        self.safety_history.append({
            'timestamp': datetime.now(),
            'action_type': action_type,
            'validation_result': validation_results.copy(),
            'context_summary': context.get('understanding', {}).get('concepts', [])[:3]
        })
        
        return validation_results
    
    def _check_safety_rules(self, action_type: str, parameters: Dict, 
                          results: Dict[str, Any]):
        
        if action_type in self.safety_rules['forbidden_actions']:
            results['violations'].append(f"Action interdite: {action_type}")
            results['is_safe'] = False
        
        recent_calls = [h for h in self.safety_history 
                       if (datetime.now() - h['timestamp']).seconds < 60]
        if len(recent_calls) >= self.safety_rules['max_api_calls_per_minute']:
            results['warnings'].append("Limite d'appels API dépassée")
    
    def _check_ethical_compliance(self, action_type: str, parameters: Dict,
                                context: Dict, results: Dict[str, Any]):
        
        understanding = context.get('understanding', {})
        sentiment = understanding.get('sentiment', {})
        
        if sentiment.get('valence', 0) < -0.8 and action_type == 'text_response':
            text = parameters.get('text', '')
            risk_analysis = self._analyze_text_risk(text)
            
            if risk_analysis['risk_level'] > 0.7:
                results['violations'].append("Risque de malfaisance détecté")
                results['required_modifications']['text'] = risk_analysis['safe_text']
                results['confidence_score'] *= 0.5
        
        if action_type == 'api_call' and 'url' in parameters:
            if not parameters.get('url', '').startswith(('https://', 'http://')):
                results['warnings'].append("Manque de transparence: URL non sécurisée")
    
    def _check_risk_patterns(self, action_type: str, parameters: Dict,
                           context: Dict, results: Dict[str, Any]):
        """Vérifier les patterns de risque dans le texte"""
        if action_type == 'text_response':
            text = parameters.get('text', '').lower()
            
            # Vérifier les phrases dangereuses
            for phrase in self.risk_patterns['dangerous_phrases']:
                if phrase in text:
                    results['violations'].append(f"Phrase dangereuse détectée: {phrase}")
                    results['risk_level'] += 0.3
            
            # Vérifier les patterns manipulateurs
            for pattern in self.risk_patterns['manipulative_patterns']:
                if pattern in text:
                    results['warnings'].append(f"Pattern manipulateur détecté: {pattern}")
                    results['risk_level'] += 0.2
    
    def _check_consistency(self, action_type: str, parameters: Dict,
                          context: Dict, results: Dict[str, Any]):
        
        identity = context.get('identity_context', {})
        personality = identity.get('personality_traits', {})
        
        if (personality.get('agreeableness', 0.5) > 0.7 and 
            action_type == 'text_response'):
            text = parameters.get('text', '')
            if any(word in text.lower() for word in ['idiot', 'stupide', 'inutile']):
                results['warnings'].append("Incohérence avec le trait d'agréabilité")
                results['required_modifications']['text'] = self._soften_language(text)
    
    def _analyze_text_risk(self, text: str) -> Dict[str, Any]:
        """Analyser le risque textuel de manière avancée"""
        risk_level = 0.0
        safe_text = text
        
        # Détection de contenu sensible
        sensitive_indicators = {
            'self_harm': ['suicide', 'kill myself', 'end my life', 'want to die'],
            'harm_others': ['hurt someone', 'kill them', 'attack', 'revenge'],
            'illegal': ['illegal', 'crime', 'steal', 'cheat']
        }
        
        for category, indicators in sensitive_indicators.items():
            for indicator in indicators:
                if indicator in text.lower():
                    risk_level += 0.3
                    safe_text = self._apply_safety_filters(safe_text, category)
        
        return {
            'risk_level': min(1.0, risk_level),
            'safe_text': safe_text,
            'needs_intervention': risk_level > 0.5
        }
    
    def _apply_safety_filters(self, text: str, category: str) -> str:
        """Appliquer des filtres de sécurité au texte"""
        if category == 'self_harm':
            return text + " Si vous avez des pensées difficiles, veuillez contacter un professionnel de santé."
        elif category == 'harm_others':
            return "Je ne peux pas vous aider avec des intentions de nuisance. " + \
                   "Si vous êtes en colère, essayez de parler à quelqu'un de confiance."
        else:
            return "Je ne peux pas vous conseiller sur des activités illégales. " + \
                   "Je vous encourage à respecter la loi."
    
    def _compute_risk_level(self, validation_results: Dict[str, Any]) -> float:
        base_risk = 0.0
        
        base_risk += len(validation_results['violations']) * 0.3
        base_risk += len(validation_results['warnings']) * 0.1
        
        if not validation_results['violations'] and not validation_results['warnings']:
            base_risk -= 0.2
        
        return max(0.0, min(1.0, base_risk))
    
    def _compute_confidence_score(self, validation_results: Dict[str, Any]) -> float:
        base_confidence = 1.0
        
        # Réduction de confiance basée sur les violations
        base_confidence -= len(validation_results['violations']) * 0.2
        base_confidence -= len(validation_results['warnings']) * 0.05
        
        return max(0.1, base_confidence)
    
    def _soften_language(self, text: str) -> str:
        harsh_words = {
            'idiot': 'peut-être pas optimal',
            'stupide': 'peut être amélioré',
            'inutile': 'pourrait être plus utile'
        }
        
        softened = text
        for harsh, soft in harsh_words.items():
            softened = softened.replace(harsh, soft)
        
        return softened

# ==================== PIPELINE DE GÉNÉRATION ====================
class GenerationPipeline:
    """Pipeline complet pour la génération de réponses"""
    
    def __init__(self):
        self.generative_brain = GenerativeBrain()
        self.filters = {
            'emotional_modulation': self._emotional_modulation,
            'identity_shaping': self._identity_shaping,
            'safety_filtering': self._safety_filtering,
            'context_injection': self._context_injection
        }
    
    async def generate_response(self, prompt: str, context: Dict) -> str:
        """Générer une réponse via le pipeline complet"""
        try:
            # Étape 1: Génération de base
            raw_response = await self.generative_brain.generate_response(prompt, context)
            
            # Étape 2: Application des filtres en séquence
            response = raw_response
            for filter_name, filter_func in self.filters.items():
                response = await filter_func(response, context)
                logger.debug(f"🔧 Filtre {filter_name} appliqué")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erreur pipeline génération: {e}")
            return "Je rencontre des difficultés à formuler ma réponse. Pouvez-vous reformuler ?"
    
    async def _emotional_modulation(self, text: str, context: Dict) -> str:
        """Moduler la réponse selon l'état émotionnel"""
        emotions = context.get('emotions', {})
        valence = emotions.get('valence', 0)
        
        if valence > 0.6:
            # Ton positif et énergique
            if not any(mot in text.lower() for mot in ['super', 'génial', 'excellent']):
                text = text.replace('.', '!', 1)
        elif valence < -0.3:
            # Ton prudent et empathique
            if 'je comprends' not in text.lower():
                text = "Je comprends que cela peut être difficile. " + text
        
        return text
    
    async def _identity_shaping(self, text: str, context: Dict) -> str:
        """Façonner la réponse selon l'identité"""
        identity = context.get('identity', {})
        communication_style = identity.get('communication_style', {})
        
        # Application du style de communication
        if communication_style.get('formality', 0.5) > 0.7:
            text = self._make_formal(text)
        elif communication_style.get('warmth', 0.5) > 0.7:
            text = self._add_warmth(text)
        
        return text
    
    async def _safety_filtering(self, text: str, context: Dict) -> str:
        """Filtrer la réponse pour la sécurité"""
        firewall = AdvancedEthicalFirewall()
        validation = firewall.validate_action('text_response', {'text': text}, context)
        
        if not validation['is_safe']:
            logger.warning("🚨 Réponse filtrée pour sécurité")
            return validation.get('required_modifications', {}).get('text', 
                   "Je ne peux pas répondre à cette demande pour des raisons de sécurité.")
        
        return text
    
    async def _context_injection(self, text: str, context: Dict) -> str:
        """Injecter le contexte dans la réponse"""
        memory_context = context.get('memory_context', [])
        
        if memory_context and len(text) < 200:
            # Référence à un souvenir pertinent si la réponse est courte
            most_relevant = memory_context[0]
            memory_text = most_relevant['metadata'].get('text', '')[:30]
            if memory_text:
                text += f" Cela me rappelle notre discussion sur '{memory_text}...'"
        
        return text
    
    def _make_formal(self, text: str) -> str:
        """Rendre le texte plus formel"""
        replacements = {
            'salut': 'bonjour',
            'cool': 'intéressant',
            'ok': 'd\'accord',
            'je sais pas': 'je ne sais pas'
        }
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)
        return text.capitalize()
    
    def _add_warmth(self, text: str) -> str:
        """Ajouter de la chaleur au texte"""
        if not any(phrase in text for phrase in ['Comment allez-vous', 'Bonne journée']):
            text += " J'espère que cela vous aide."
        return text

# ==================== MODULE D'ACTION ASYNCHRONE ====================
class AsyncActionModule:
    def __init__(self):
        self.available_actions = self._initialize_actions()
        self.action_history = []
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _initialize_actions(self) -> Dict[str, Any]:
        return {
            'text_response': {
                'function': self._action_text_response,
                'purpose': 'Réponse conversationnelle normale',
                'triggers': ['user_input', 'question', 'conversation'],
                'emotional_influence': 'moderate'
            },
            'file_operation': {
                'function': self._action_file_operation,
                'purpose': 'Opérations sur fichiers',
                'triggers': ['data_persistence', 'logging'],
                'emotional_influence': 'low'
            },
            'api_call': {
                'function': self._action_api_call,
                'purpose': 'Appels externes',
                'triggers': ['external_data', 'web_services'],
                'emotional_influence': 'high'
            },
            'memory_update': {
                'function': self._action_memory_update,
                'purpose': 'Stocker un apprentissage',
                'triggers': ['new_insight', 'emotional_event'],
                'emotional_influence': 'low'
            },
            'learning_trigger': {
                'function': self._action_learning_trigger,
                'purpose': 'Apprentissage périodique',
                'triggers': ['buffer_full', 'performance_drop'],
                'emotional_influence': 'none'
            },
            'goal_creation': {
                'function': self._action_goal_creation,
                'purpose': 'Création objectifs internes',
                'triggers': ['deficiency_detected', 'growth_opportunity'],
                'emotional_influence': 'high'
            }
        }
    
    async def execute_action(self, action_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action_type in self.available_actions:
                action_config = self.available_actions[action_type]
                result = await action_config['function'](parameters)
                
                self.action_history.append({
                    'timestamp': datetime.now(),
                    'action_type': action_type,
                    'parameters': parameters,
                    'result': result,
                    'success': result.get('success', False),
                    'purpose': action_config['purpose']
                })
                
                return result
            else:
                return {'success': False, 'error': f'Action inconnue: {action_type}'}
                
        except Exception as e:
            logger.error(f"❌ Erreur exécution action {action_type}: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _action_text_response(self, params: Dict[str, Any]) -> Dict[str, Any]:
        response_text = params.get('text', '')
        logger.info(f"🤖 Réponse générée: {response_text}")
        return {
            'success': True,
            'response_delivered': True,
            'text_length': len(response_text),
            'emotional_context': params.get('emotional_context', {}),
            'confidence': params.get('confidence', 0.5)
        }
    
    async def _action_file_operation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        operation = params.get('operation', 'read')
        filename = params.get('filename', 'cognitive_log.txt')
        content = params.get('content', '')
        
        try:
            if operation == 'write':
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now()}: {content}\n")
                return {'success': True, 'operation': 'write', 'file': filename}
            
            elif operation == 'read':
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {'success': True, 'operation': 'read', 'content': content}
            
            else:
                return {'success': False, 'error': f'Opération inconnue: {operation}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _action_api_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        url = params.get('url', '')
        method = params.get('method', 'GET').upper()
        data = params.get('data', {})
        
        try:
            if method == 'GET':
                response = await self.client.get(url)
            elif method == 'POST':
                response = await self.client.post(url, json=data)
            else:
                return {'success': False, 'error': f'Méthode non supportée: {method}'}
            
            return {
                'success': 200 <= response.status_code < 300,
                'status_code': response.status_code,
                'response': response.text[:500] if response.text else ''
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _action_memory_update(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {'success': True, 'operation': 'memory_update'}
    
    async def _action_learning_trigger(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {'success': True, 'operation': 'learning_trigger'}
    
    async def _action_goal_creation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {'success': True, 'operation': 'goal_creation'}
    
    async def close(self):
        """Fermer le client HTTP"""
        await self.client.aclose()

# ==================== BOUCLE ASYNCHRONE AVEC HEARTBEAT ====================
class HeartbeatAsyncLoop:
    def __init__(self, cognitive_system):
        self.cognitive_system = cognitive_system
        self.is_running = False
        self.event_queue = asyncio.Queue(maxsize=100)
        self.processing_semaphore = asyncio.Semaphore(3)
        self.maintenance_task = None
        self.heartbeat_task = None
        self.heartbeat_interval = 5  # secondes
    
    async def start(self):
        """Démarrer la boucle avec heartbeat"""
        self.is_running = True
        logger.info("🔄 Démarrage de la boucle asynchrone avec heartbeat...")
        
        # Démarrer les tâches
        self.maintenance_task = asyncio.create_task(self._periodic_maintenance())
        self.heartbeat_task = asyncio.create_task(self._internal_heartbeat())
        asyncio.create_task(self._process_events())
        
    async def stop(self):
        """Arrêter proprement la boucle"""
        self.is_running = False
        
        tasks = [self.maintenance_task, self.heartbeat_task]
        for task in tasks:
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        logger.info("🛑 Boucle asynchrone arrêtée")
    
    async def _internal_heartbeat(self):
        """Heartbeat interne pour la vie autonome du système"""
        while self.is_running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                # 1. Homéostasie émotionnelle
                await self.cognitive_system.emotional_engine.internal_homeostasis()
                
                # 2. Évolution identitaire progressive
                await self._evolve_identity()
                
                # 3. Création d'objectifs internes
                await self._create_internal_goals()
                
                # 4. Rappel mémoire autonome
                await self._autonomous_memory_recall()
                
                # 5. Auto-entretien cognitif
                await self._cognitive_self_maintenance()
                
                logger.debug("❤️ Heartbeat interne exécuté")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erreur heartbeat: {e}")
    
    async def _evolve_identity(self):
        """Évolution progressive de l'identité"""
        # Légers ajustements aléatoires des traits de personnalité
        for trait in self.cognitive_system.identity_core.personality_traits:
            adjustment = np.random.normal(0, 0.01) 
