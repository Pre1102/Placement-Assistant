from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.models.database_models import ChatHistory
from app.services.rag_engine import RAGEngine

router = APIRouter(prefix="/chat", tags=["Chat"])

# Single shared instance for RAG Engine initialized in main
rag_engine_instance = None

def set_rag_engine(engine: RAGEngine):
    global rag_engine_instance
    rag_engine_instance = engine

@router.post("", response_model=ChatResponse)
def ask_chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not rag_engine_instance:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized.")
    
    result = rag_engine_instance.process_query(db, request.query, user_id=request.user_id or 1)
    
    # Save chat history
    try:
        history_entry = ChatHistory(
            user_id=request.user_id or 1,
            query=request.query,
            response=result["answer"],
            category=result["category"]
        )
        db.add(history_entry)
        db.commit()
    except Exception as e:
        print(f"[ChatRoute] Failed to save chat history: {e}")
        
    return ChatResponse(
        category=result["category"],
        answer=result["answer"],
        eligibility_result=result["eligibility_result"],
        sources=result["sources"],
        unknown_query=result["unknown_query"]
    )
