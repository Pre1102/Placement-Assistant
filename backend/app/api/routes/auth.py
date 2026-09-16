from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.database_models import User, StudentProfile
from app.models.schemas import UserSignup, UserLogin, TokenResponse, UserResponse, StudentProfileBase

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Helper to extract User from Authorization Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    user_id = int(payload["sub"])
    return db.query(User).filter(User.id == user_id).first()

@router.post("/signup", response_model=TokenResponse)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    """Register a new user (Student or Admin) and create initial profile."""
    existing_user = db.query(User).filter(User.email == data.email.strip().lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    
    # Create user
    user = User(
        name=data.name.strip(),
        email=data.email.strip().lower(),
        hashed_password=hash_password(data.password),
        role=data.role.strip().lower() if data.role in ["student", "admin"] else "student"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create profile for student
    profile_data = None
    if user.role == "student":
        profile = StudentProfile(
            user_id=user.id,
            branch=data.branch or "Computer Engineering",
            cgpa=data.cgpa if data.cgpa is not None else 7.2,
            graduation_year=data.graduation_year or 2027,
            backlogs=data.backlogs if data.backlogs is not None else 1,
            skills=data.skills or "Python, SQL, HTML, CSS",
            preferred_role=data.preferred_role or "Data Analyst"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        profile_data = StudentProfileBase(
            branch=profile.branch,
            cgpa=profile.cgpa,
            graduation_year=profile.graduation_year,
            backlogs=profile.backlogs,
            skills=profile.skills,
            preferred_role=profile.preferred_role
        )

    # Token
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(id=user.id, name=user.name, email=user.email, role=user.role),
        profile=profile_data
    )

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate existing user and return access token."""
    user = db.query(User).filter(User.email == data.email.strip().lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    profile_data = None
    if user.profile:
        profile_data = StudentProfileBase(
            branch=user.profile.branch,
            cgpa=user.profile.cgpa,
            graduation_year=user.profile.graduation_year,
            backlogs=user.profile.backlogs,
            skills=user.profile.skills,
            preferred_role=user.profile.preferred_role
        )

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(id=user.id, name=user.name, email=user.email, role=user.role),
        profile=profile_data
    )

@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Fetch current logged-in user profile details."""
    user = get_current_user_from_token(authorization, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated."
        )

    profile_data = None
    if user.profile:
        profile_data = {
            "branch": user.profile.branch,
            "cgpa": user.profile.cgpa,
            "graduation_year": user.profile.graduation_year,
            "backlogs": user.profile.backlogs,
            "skills": user.profile.skills,
            "preferred_role": user.profile.preferred_role
        }

    return {
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role},
        "profile": profile_data
    }
