from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.schemas import StudentProfileResponse, StudentProfileCreate
from app.models.database_models import User, StudentProfile
from app.api.routes.auth import get_current_user_from_token

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=StudentProfileResponse)
def get_profile(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user_from_token(authorization, db)
    if not user:
        # Fallback to first user in database or create default demo user
        user = db.query(User).first()
        if not user:
            user = User(name="Demo Student", email="student@careercampus.ai", role="student")
            db.add(user)
            db.commit()
            db.refresh(user)

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        profile = StudentProfile(
            user_id=user.id,
            branch="Computer Engineering",
            cgpa=7.2,
            graduation_year=2027,
            backlogs=1,
            skills="Python, C++, SQL, HTML, CSS",
            preferred_role="Data Analyst"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return StudentProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        branch=profile.branch,
        cgpa=profile.cgpa,
        graduation_year=profile.graduation_year,
        backlogs=profile.backlogs,
        skills=profile.skills,
        preferred_role=profile.preferred_role,
        name=user.name,
        email=user.email
    )

@router.put("", response_model=StudentProfileResponse)
def update_profile(data: StudentProfileCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    user = get_current_user_from_token(authorization, db)
    if not user:
        user = db.query(User).first()

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        profile = StudentProfile(user_id=user.id)
        db.add(profile)

    profile.branch = data.branch
    profile.cgpa = data.cgpa
    profile.graduation_year = data.graduation_year
    profile.backlogs = data.backlogs
    profile.skills = data.skills
    profile.preferred_role = data.preferred_role

    db.commit()
    db.refresh(profile)

    return StudentProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        branch=profile.branch,
        cgpa=profile.cgpa,
        graduation_year=profile.graduation_year,
        backlogs=profile.backlogs,
        skills=profile.skills,
        preferred_role=profile.preferred_role,
        name=user.name,
        email=user.email
    )
