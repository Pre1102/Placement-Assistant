from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import StudentProfileResponse, StudentProfileCreate
from app.models.database_models import User, StudentProfile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=StudentProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).first()
    if not profile:
        # Create default demo profile
        user = db.query(User).first()
        if not user:
            user = User(name="Demo Student", email="student@careercampus.ai", role="student")
            db.add(user)
            db.commit()
            db.refresh(user)
        
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
        
    user = db.query(User).filter(User.id == profile.user_id).first()
    return StudentProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        branch=profile.branch,
        cgpa=profile.cgpa,
        graduation_year=profile.graduation_year,
        backlogs=profile.backlogs,
        skills=profile.skills,
        preferred_role=profile.preferred_role,
        name=user.name if user else "Demo Student",
        email=user.email if user else "student@careercampus.ai"
    )

@router.put("", response_model=StudentProfileResponse)
def update_profile(data: StudentProfileCreate, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).first()
    if not profile:
        user = db.query(User).first()
        if not user:
            user = User(name="Demo Student", email="student@careercampus.ai", role="student")
            db.add(user)
            db.commit()
            db.refresh(user)
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

    user = db.query(User).filter(User.id == profile.user_id).first()
    return StudentProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        branch=profile.branch,
        cgpa=profile.cgpa,
        graduation_year=profile.graduation_year,
        backlogs=profile.backlogs,
        skills=profile.skills,
        preferred_role=profile.preferred_role,
        name=user.name if user else "Demo Student",
        email=user.email if user else "student@careercampus.ai"
    )
