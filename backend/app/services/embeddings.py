import numpy as np

class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print("[EmbeddingService] Loading SentenceTransformer 'all-MiniLM-L6-v2'...")
                cls._model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"[EmbeddingService] Error loading SentenceTransformer: {e}")
                cls._model = None
        return cls._model

    @classmethod
    def encode_text(cls, text: str) -> np.ndarray:
        model = cls.get_model()
        if model:
            emb = model.encode(text, convert_to_numpy=True)
            return emb.astype(np.float32)
        else:
            # Fallback deterministic pseudo-embedding (384 dim) if model fails
            np.random.seed(abs(hash(text)) % (2**32))
            emb = np.random.randn(384).astype(np.float32)
            return emb / np.linalg.norm(emb)

    @classmethod
    def encode_batch(cls, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        model = cls.get_model()
        if model:
            embs = model.encode(texts, convert_to_numpy=True)
            return embs.astype(np.float32)
        else:
            res = [cls.encode_text(t) for t in texts]
            return np.array(res, dtype=np.float32)
