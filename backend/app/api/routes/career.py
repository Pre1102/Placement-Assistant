from fastapi import APIRouter
from app.models.schemas import CareerRoadmapRequest, CareerRoadmapResponse
from app.services.career_engine import CareerEngine

router = APIRouter(prefix="/career", tags=["Career"])

@router.post("/roadmap", response_model=CareerRoadmapResponse)
def get_career_roadmap(request: CareerRoadmapRequest):
    return CareerEngine.get_roadmap(
        target_role=request.target_role,
        current_level=request.current_skill_level or "Beginner",
        prep_time=request.preparation_time or "3 Months"
    )
