# vector_memory.py
import numpy as np
from datetime import datetime

class VectorMemory:
    """
    Mémoire vectorielle simple et robuste pour MTI.
    Fonctionne sans FAISS, sans GPU, totalement portable.
    """
    def __init__(self, dim: int = 384):
        self.dim = dim
        self.vectors = []
        self.metadata = []

    def _norm(self, v: np.ndarray):
        """Normalise la dimension du vecteur."""
        v = np.array(v, dtype=float)

        if len(v) > self.dim:
            return v[:self.dim]

        if len(v) < self.dim:
            pad = np.zeros(self.dim - len(v))
            return np.concatenate([v, pad])

        return v

    def add(self, vector: np.ndarray, meta: dict):
        """Ajoute un vecteur + metadata."""
        v = self._norm(vector)

        self.vectors.append(v)
        self.metadata.append({
            **meta,
            "timestamp": datetime.now().isoformat()
        })

    def search(self, query: np.ndarray, top_k: int = 5):
        """Recherche les vecteurs les plus similaires (cosine)."""
        if not self.vectors:
            return []

        q = self._norm(query)

        similarities = []

        for idx, vec in enumerate(self.vectors):
            score = self._cosine(q, vec)
            similarities.append((score, idx))

        similarities.sort(reverse=True, key=lambda x: x[0])

        results = []
        for score, idx in similarities[:top_k]:
            results.append({
                "score": float(score),
                "vector": self.vectors[idx].tolist(),
                "meta": self.metadata[idx]
            })

        return results

    def _cosine(self, a, b):
        """Cosine similarity."""
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
