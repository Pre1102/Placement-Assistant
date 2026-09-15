from fastapi import APIRouter
from app.models.schemas import InterviewPrepRequest, InterviewPrepResponse
from app.services.career_engine import CareerEngine

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.post("/generate", response_model=InterviewPrepResponse)
def generate_interview_prep(request: InterviewPrepRequest):
    return CareerEngine.generate_interview_questions(
        target_role=request.target_role,
        topic=request.topic or "All",
        difficulty=request.difficulty or "Intermediate"
    )
