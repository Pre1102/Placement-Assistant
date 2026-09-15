import os
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.config import settings
from app.models.database_models import Document, DocumentChunk
from app.models.schemas import KBStatusResponse
from app.services.document_processor import DocumentProcessor
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingService

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])

vector_store_instance = None

def set_vector_store(store):
    global vector_store_instance
    vector_store_instance = store

@router.get("/status", response_model=KBStatusResponse)
def get_kb_status(db: Session = Depends(get_db)):
    total_docs = db.query(Document).count()
    total_chunks = db.query(DocumentChunk).count()
    vector_count = vector_store_instance.get_total_vectors() if vector_store_instance else 0
    
    last_doc = db.query(Document).order_by(Document.upload_date.desc()).first()
    last_updated = last_doc.upload_date.strftime("%Y-%m-%d %H:%M:%S") if last_doc else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    return KBStatusResponse(
        status="Active",
        total_documents=total_docs,
        total_chunks=total_chunks,
        vector_count=vector_count,
        last_updated=last_updated
    )

@router.post("/rebuild", response_model=KBStatusResponse)
def rebuild_kb_index(db: Session = Depends(get_db)):
    """
    Clears FAISS index and rebuilds all document vectors from SQLite database or demo PDFs.
    """
    if not vector_store_instance:
        return get_kb_status(db)

    # 1. Reset FAISS index
    vector_store_instance.reset_index()

    # 2. Clear existing document chunk records in DB
    db.query(DocumentChunk).delete()
    db.commit()

    # 3. Iterate over documents in data/demo or DB and re-ingest
    docs = db.query(Document).all()
    for doc in docs:
        file_path = os.path.join(settings.DATA_DIR, doc.filename)
        if os.path.exists(file_path):
            pages = DocumentProcessor.extract_text_from_pdf(file_path)
            chunks_data = TextChunker.chunk_document(
                pages=pages,
                document_id=doc.id,
                document_name=doc.filename,
                category=doc.category,
                company=doc.company
            )

            if chunks_data:
                texts = [c["text"] for c in chunks_data]
                embeddings = EmbeddingService.encode_batch(texts)
                vector_ids = vector_store_instance.add_vectors(embeddings)

                for chunk_info, vec_id in zip(chunks_data, vector_ids):
                    chunk_obj = DocumentChunk(
                        document_id=doc.id,
                        chunk_id=chunk_info["chunk_id"],
                        vector_id=vec_id,
                        page_number=chunk_info["page_number"],
                        category=doc.category,
                        company=doc.company,
                        text=chunk_info["text"]
                    )
                    db.add(chunk_obj)

                doc.chunk_count = len(chunks_data)
                doc.status = "indexed"

    db.commit()
    return get_kb_status(db)
