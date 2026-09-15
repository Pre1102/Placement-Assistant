from sqlalchemy.orm import Session
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreManager
from app.models.database_models import DocumentChunk, Document

class HybridRetriever:
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store

    def retrieve_chunks(self, db: Session, query: str, top_k: int = 5, score_threshold: float = 0.25) -> list[dict]:
        """
        Retrieves top-K relevant chunks matching query embedding.
        Returns list of dicts with chunk text, page_number, doc_name, company, score.
        """
        query_emb = EmbeddingService.encode_text(query)
        faiss_results = self.vector_store.search(query_emb, top_k=top_k * 2)

        if not faiss_results:
            return []

        retrieved_chunks = []
        for vector_id, score in faiss_results:
            if score < score_threshold and len(retrieved_chunks) > 0:
                continue

            chunk_record = db.query(DocumentChunk).filter(DocumentChunk.vector_id == vector_id).first()
            if chunk_record:
                doc_record = db.query(Document).filter(Document.id == chunk_record.document_id).first()
                doc_name = doc_record.filename if doc_record else "Unknown Document"
                
                retrieved_chunks.append({
                    "chunk_id": chunk_record.chunk_id,
                    "document_id": chunk_record.document_id,
                    "document_name": doc_name,
                    "page_number": chunk_record.page_number,
                    "category": chunk_record.category or (doc_record.category if doc_record else None),
                    "company": chunk_record.company or (doc_record.company if doc_record else None),
                    "text": chunk_record.text,
                    "similarity_score": round(float(score), 4)
                })

                if len(retrieved_chunks) >= top_k:
                    break

        return retrieved_chunks
