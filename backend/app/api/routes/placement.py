from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import StudentProfile
from app.models.schemas import (
    PlacementEligibilityRequest, PlacementEligibilityResponse,
    CompanyComparisonRequest, CompanyComparisonResponse, StudentProfileBase
)
from app.api.routes.companies import get_companies
from app.services.placement_engine import PlacementEligibilityEngine

router = APIRouter(prefix="/placement", tags=["Placement"])

@router.post("/check-eligibility", response_model=PlacementEligibilityResponse)
def check_eligibility(request: PlacementEligibilityRequest, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).first()
    profile_dict = {
        "branch": profile.branch if profile else "Computer Engineering",
        "cgpa": profile.cgpa if profile else 7.2,
        "backlogs": profile.backlogs if profile else 1
    }
    
    companies = get_companies(db)
    if request.company_name:
        companies = [c for c in companies if c.name.lower() == request.company_name.lower()]

    results = []
    for c in companies:
        criteria = {
            "company_name": c.name,
            "min_cgpa": c.min_cgpa,
            "max_backlogs": c.max_backlogs,
            "branches": c.eligible_branches
        }
        sources = [{"document_name": c.doc_source, "page_number": 1}] if c.doc_source else []
        res = PlacementEligibilityEngine.evaluate_eligibility(profile_dict, criteria, sources)
        results.append(res)

    return PlacementEligibilityResponse(
        profile=StudentProfileBase(
            branch=profile_dict["branch"],
            cgpa=profile_dict["cgpa"],
            backlogs=profile_dict["backlogs"],
            graduation_year=profile.graduation_year if profile else 2027,
            skills=profile.skills if profile else "",
            preferred_role=profile.preferred_role if profile else ""
        ),
        results=results
    )

@router.post("/compare", response_model=CompanyComparisonResponse)
def compare_companies(request: CompanyComparisonRequest, db: Session = Depends(get_db)):
    all_companies = get_companies(db)
    selected = [c for c in all_companies if c.name in request.company_names]
    if not selected:
        selected = all_companies[:3]

    profile = db.query(StudentProfile).first()
    profile_dict = {
        "branch": profile.branch if profile else "Computer Engineering",
        "cgpa": profile.cgpa if profile else 7.2,
        "backlogs": profile.backlogs if profile else 1
    }

    matrix = {
        "headers": ["Requirement"] + [c.name for c in selected],
        "rows": []
    }

    # CGPA Row
    matrix["rows"].append({
        "feature": "Minimum CGPA",
        "values": [str(c.min_cgpa) if c.min_cgpa is not None else "N/A" for c in selected]
    })

    # Backlogs Row
    matrix["rows"].append({
        "feature": "Max Backlogs Allowed",
        "values": [str(c.max_backlogs) if c.max_backlogs is not None else "N/A" for c in selected]
    })

    # Branches Row
    matrix["rows"].append({
        "feature": "Eligible Branches",
        "values": [", ".join(c.eligible_branches) if c.eligible_branches else "All Branches" for c in selected]
    })

    # CTC Row
    matrix["rows"].append({
        "feature": "Offered CTC",
        "values": [c.ctc or "N/A" for c in selected]
    })

    # Status Row
    statuses = []
    for c in selected:
        crit = {"company_name": c.name, "min_cgpa": c.min_cgpa, "max_backlogs": c.max_backlogs, "branches": c.eligible_branches}
        res = PlacementEligibilityEngine.evaluate_eligibility(profile_dict, crit)
        statuses.append(res["status"])

    matrix["rows"].append({
        "feature": "Your Eligibility Status",
        "values": statuses
    })

    return CompanyComparisonResponse(
        companies=selected,
        matrix=matrix
    )
