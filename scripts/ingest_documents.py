import os
import sys

# Ensure backend app path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.config import settings
from app.core.database import SessionLocal, Base, engine
from app.models.database_models import Document, DocumentChunk, User, StudentProfile
from app.services.document_processor import DocumentProcessor
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreManager

def determine_category_and_company(filename: str) -> tuple[str, str]:
    fn = filename.upper()
    if "POLICY" in fn:
        return ("Placement Rules", None)
    if "REGISTRATION" in fn or "PROCEDURE" in fn or "PROCESS" in fn:
        return ("Placement Procedures", None)
    if "FAQ" in fn:
        return ("Placement FAQs", None)
    if "INTERNSHIP" in fn:
        return ("Internship", None)
    if "ROADMAP" in fn or "CAREER" in fn:
        return ("Career Guidance", None)
    if "COMPANY_A" in fn:
        return ("Company Notices", "Demo Company A")
    if "COMPANY_B" in fn:
        return ("Company Notices", "Demo Company B")
    if "COMPANY_C" in fn:
        return ("Company Notices", "Demo Company C")
    if "COMPANY_D" in fn:
        return ("Company Notices", "Demo Company D")
    return ("General", None)

def run_ingestion():
    print("=" * 60)
    print("CareerCampusAI — Document Ingestion Pipeline")
    print("=" * 60)

    # 1. Ensure DB & FAISS storage
    Base.metadata.create_all(bind=engine)
    vector_store = VectorStoreManager(index_dir=settings.VECTORSTORE_DIR, dimension=384)
    db = SessionLocal()

    # 2. Scan demo data directory
    data_dir = settings.DATA_DIR
    if not os.path.exists(data_dir):
        print(f"[!] Data directory '{data_dir}' not found. Please run scripts/generate_demo_pdfs.py first.")
        return

    pdf_files = [f for f in os.listdir(data_dir) if f.endswith(".pdf")]
    print(f"[*] Found {len(pdf_files)} PDF files in {data_dir}")

    total_chunks_added = 0
    docs_processed = 0

    for filename in pdf_files:
        file_path = os.path.join(data_dir, filename)
        category, company = determine_category_and_company(filename)

        # Check if doc already in DB
        doc_record = db.query(Document).filter(Document.filename == filename).first()
        if not doc_record:
            doc_record = Document(
                filename=filename,
                category=category,
                company=company,
                status="processing"
            )
            db.add(doc_record)
            db.commit()
            db.refresh(doc_record)
        else:
            # Clear old chunks for re-ingestion
            db.query(DocumentChunk).filter(DocumentChunk.document_id == doc_record.id).delete()
            db.commit()

        # Extract text & chunk
        pages = DocumentProcessor.extract_text_from_pdf(file_path)
        chunks_data = TextChunker.chunk_document(
            pages=pages,
            document_id=doc_record.id,
            document_name=doc_record.filename,
            category=category,
            company=company
        )

        if chunks_data:
            texts = [c["text"] for c in chunks_data]
            embeddings = EmbeddingService.encode_batch(texts)
            vector_ids = vector_store.add_vectors(embeddings)

            for chunk_info, vec_id in zip(chunks_data, vector_ids):
                chunk_obj = DocumentChunk(
                    document_id=doc_record.id,
                    chunk_id=chunk_info["chunk_id"],
                    vector_id=vec_id,
                    page_number=chunk_info["page_number"],
                    category=category,
                    company=company,
                    text=chunk_info["text"]
                )
                db.add(chunk_obj)

            doc_record.chunk_count = len(chunks_data)
            doc_record.status = "indexed"
            total_chunks_added += len(chunks_data)
            docs_processed += 1
            print(f"[+] Indexed: '{filename}' ({len(chunks_data)} chunks) -> Vector IDs {vector_ids[0]}..{vector_ids[-1]}")

    # Seed demo profile if missing
    if not db.query(User).first():
        user = User(name="Demo Student", email="student@careercampus.ai", role="student")
        db.add(user)
        db.commit()
        db.refresh(user)

        prof = StudentProfile(
            user_id=user.id,
            branch="Computer Engineering",
            cgpa=7.2,
            graduation_year=2027,
            backlogs=1,
            skills="Python, C++, SQL, HTML, CSS",
            preferred_role="Data Analyst"
        )
        db.add(prof)

    db.commit()
    db.close()

    print("=" * 60)
    print(f"SUCCESS: Indexed {docs_processed} documents with {total_chunks_added} chunks into FAISS & SQLite.")
    print("=" * 60)

if __name__ == "__main__":
    run_ingestion()
