import os
import faiss
import numpy as np

class VectorStoreManager:
    def __init__(self, index_dir: str, dimension: int = 384):
        self.index_dir = index_dir
        self.index_path = os.path.join(index_dir, "faiss.index")
        self.dimension = dimension
        self.index = None
        self._initialize_index()

    def _initialize_index(self):
        os.makedirs(self.index_dir, exist_ok=True)
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print(f"[FAISS] Loaded existing index with {self.index.ntotal} vectors.")
            except Exception as e:
                print(f"[FAISS] Failed to load index: {e}. Creating new index.")
                self.create_new_index()
        else:
            self.create_new_index()

    def create_new_index(self):
        # IndexFlatIP (Inner Product) with normalized vectors for Cosine Similarity
        self.index = faiss.IndexFlatIP(self.dimension)
        self.save_index()
        print(f"[FAISS] Created new empty FAISS index (dim={self.dimension}).")

    def save_index(self):
        os.makedirs(self.index_dir, exist_ok=True)
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)

    def add_vectors(self, embeddings: np.ndarray) -> list[int]:
        """
        Adds normalized vector embeddings to FAISS index.
        Returns assigned vector IDs (start_id .. start_id + count - 1).
        """
        if embeddings is None or len(embeddings) == 0:
            return []
        
        # Ensure float32 and L2 normalized for cosine similarity
        vectors = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(vectors)
        
        start_id = self.index.ntotal
        self.index.add(vectors)
        self.save_index()
        
        assigned_ids = list(range(start_id, self.index.ntotal))
        return assigned_ids

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[tuple[int, float]]:
        """
        Searches FAISS for top_k nearest vectors.
        Returns list of (vector_id, similarity_score).
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        q_vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(q_vec)

        scores, indices = self.index.search(q_vec, min(top_k, self.index.ntotal))
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1:
                results.append((int(idx), float(score)))
        return results

    def reset_index(self):
        self.create_new_index()

    def get_total_vectors(self) -> int:
        return self.index.ntotal if self.index else 0
