import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.config import settings
from app.models.database_models import Document, DocumentChunk
from app.models.schemas import DocumentResponse
from app.services.document_processor import DocumentProcessor
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingService

router = APIRouter(prefix="/documents", tags=["Documents"])

# References to global vector store initialized in main
vector_store_instance = None

def set_vector_store(store):
    global vector_store_instance
    vector_store_instance = store

@router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.upload_date.desc()).all()
    return docs

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("Placement Rules"),
    company: str = Form(""),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    os.makedirs(settings.DATA_DIR, exist_ok=True)
    save_path = os.path.join(settings.DATA_DIR, file.filename)
    
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Database document record
    doc_record = Document(
        filename=file.filename,
        category=category,
        company=company if company else None,
        status="processing"
    )
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)

    # Ingestion pipeline: Extract -> Chunk -> Embed -> FAISS -> SQLite
    pages = DocumentProcessor.extract_text_from_pdf(save_path)
    chunks_data = TextChunker.chunk_document(
        pages=pages,
        document_id=doc_record.id,
        document_name=doc_record.filename,
        category=category,
        company=company if company else None
    )

    if chunks_data and vector_store_instance:
        texts = [c["text"] for c in chunks_data]
        embeddings = EmbeddingService.encode_batch(texts)
        vector_ids = vector_store_instance.add_vectors(embeddings)

        for chunk_info, vec_id in zip(chunks_data, vector_ids):
            chunk_obj = DocumentChunk(
                document_id=doc_record.id,
                chunk_id=chunk_info["chunk_id"],
                vector_id=vec_id,
                page_number=chunk_info["page_number"],
                category=category,
                company=company if company else None,
                text=chunk_info["text"]
            )
            db.add(chunk_obj)

        doc_record.chunk_count = len(chunks_data)
        doc_record.status = "indexed"
    else:
        doc_record.status = "indexed" if not chunks_data else "failed"

    db.commit()
    db.refresh(doc_record)
    return doc_record

@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Remove physical file if present
    file_path = os.path.join(settings.DATA_DIR, doc.filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"[Documents] Failed to delete file {file_path}: {e}")

    # Remove chunks and document record from SQLite
    db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).delete()
    db.delete(doc)
    db.commit()

    return {"message": f"Document '{doc.filename}' deleted successfully."}

@router.post("/{doc_id}/reprocess", response_model=DocumentResponse)
def reprocess_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = os.path.join(settings.DATA_DIR, doc.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Physical document file missing on server.")

    # Remove existing chunks
    db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_id).delete()

    pages = DocumentProcessor.extract_text_from_pdf(file_path)
    chunks_data = TextChunker.chunk_document(
        pages=pages,
        document_id=doc.id,
        document_name=doc.filename,
        category=doc.category,
        company=doc.company
    )

    if chunks_data and vector_store_instance:
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
    db.refresh(doc)
    return doc
