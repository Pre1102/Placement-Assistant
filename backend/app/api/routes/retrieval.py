from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import RetrievalTestRequest, RetrievalTestResponse, RetrievalChunkResult
from app.services.retriever import HybridRetriever

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])

retriever_instance = None

def set_retriever(retriever: HybridRetriever):
    global retriever_instance
    retriever_instance = retriever

@router.post("/test", response_model=RetrievalTestResponse)
def test_retrieval(request: RetrievalTestRequest, db: Session = Depends(get_db)):
    if not retriever_instance:
        raise HTTPException(status_code=500, detail="Retriever service not initialized.")

    chunks = retriever_instance.retrieve_chunks(
        db=db,
        query=request.query,
        top_k=request.top_k or 5,
        score_threshold=0.0
    )

    results = []
    for c in chunks:
        results.append(RetrievalChunkResult(
            chunk_id=c["chunk_id"],
            document_name=c["document_name"],
            page_number=c["page_number"],
            category=c.get("category"),
            company=c.get("company"),
            similarity_score=c["similarity_score"],
            text=c["text"]
        ))

    return RetrievalTestResponse(
        query=request.query,
        results=results
    )
