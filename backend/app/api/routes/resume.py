from fastapi import APIRouter
from app.models.schemas import ResumeGuidanceRequest, ResumeGuidanceResponse
from app.services.career_engine import CareerEngine

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/guidance", response_model=ResumeGuidanceResponse)
def get_resume_guidance(request: ResumeGuidanceRequest):
    return CareerEngine.generate_resume_guidance(
        target_role=request.target_role,
        student_skills=request.skills,
        projects=request.projects or ""
    )
