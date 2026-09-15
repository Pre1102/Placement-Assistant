import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import engine, Base, SessionLocal
from app.services.vector_store import VectorStoreManager
from app.services.retriever import HybridRetriever
from app.services.rag_engine import RAGEngine

# Import Routes
from app.api.routes import (
    chat, profile, placement, companies, career,
    interview, resume, documents, knowledge_base, retrieval
)

# Initialize Core Services
vector_store = VectorStoreManager(index_dir=settings.VECTORSTORE_DIR, dimension=384)
retriever = HybridRetriever(vector_store=vector_store)
rag_engine = RAGEngine(retriever=retriever)

# Wire services into routers
chat.set_rag_engine(rag_engine)
documents.set_vector_store(vector_store)
knowledge_base.set_vector_store(vector_store)
retrieval.set_retriever(retriever)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("[CareerCampusAI] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Auto-seed default student profile if empty
    db = SessionLocal()
    try:
        from app.models.database_models import User, StudentProfile
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
            print("[CareerCampusAI] Created default Demo Student profile.")
    except Exception as e:
        print(f"[CareerCampusAI] Startup seed error: {e}")
    finally:
        db.close()
        
    yield
    print("[CareerCampusAI] Shutting down application.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for React frontend (Vite default port 5173 / localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chat.router, prefix=settings.API_PREFIX)
app.include_router(profile.router, prefix=settings.API_PREFIX)
app.include_router(placement.router, prefix=settings.API_PREFIX)
app.include_router(companies.router, prefix=settings.API_PREFIX)
app.include_router(career.router, prefix=settings.API_PREFIX)
app.include_router(interview.router, prefix=settings.API_PREFIX)
app.include_router(resume.router, prefix=settings.API_PREFIX)
app.include_router(documents.router, prefix=settings.API_PREFIX)
app.include_router(knowledge_base.router, prefix=settings.API_PREFIX)
app.include_router(retrieval.router, prefix=settings.API_PREFIX)

@app.get(f"{settings.API_PREFIX}/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "vector_count": vector_store.get_total_vectors()
    }
