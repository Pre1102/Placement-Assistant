from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

# Profile
class StudentProfileBase(BaseModel):
    branch: str = "Computer Engineering"
    cgpa: float = Field(7.2, ge=0.0, le=10.0)
    graduation_year: int = 2027
    backlogs: int = Field(1, ge=0)
    skills: str = "Python, C++, SQL, HTML, CSS"
    preferred_role: str = "Data Analyst"

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileResponse(StudentProfileBase):
    id: int
    user_id: int
    name: Optional[str] = "Demo Student"
    email: Optional[str] = "student@careercampus.ai"

    class Config:
        from_attributes = True

# User Authentication Schemas
class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    role: str = "student" # "student" or "admin"
    branch: Optional[str] = "Computer Engineering"
    cgpa: Optional[float] = 7.2
    graduation_year: Optional[int] = 2027
    backlogs: Optional[int] = 1
    skills: Optional[str] = "Python, C++, SQL, HTML, CSS"
    preferred_role: Optional[str] = "Data Analyst"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    profile: Optional[StudentProfileBase] = None

# Sources
class SourceCitation(BaseModel):
    document_name: str
    page_number: int
    category: Optional[str] = None
    company: Optional[str] = None
    snippet: Optional[str] = None

# Eligibility Detail Card
class RequirementCheck(BaseModel):
    requirement_name: str
    required_value: str
    student_value: str
    satisfied: bool

class EligibilityResult(BaseModel):
    company_name: str
    status: str # "Eligible", "Not Eligible", "Requirement Unknown"
    reasons: List[str]
    checks: List[RequirementCheck]
    sources: List[SourceCitation] = []

# Chat
class ChatRequest(BaseModel):
    query: str
    user_id: Optional[int] = 1

class ChatResponse(BaseModel):
    category: str
    answer: str
    eligibility_result: Optional[EligibilityResult] = None
    sources: List[SourceCitation] = []
    unknown_query: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Company
class CompanyDetail(BaseModel):
    id: Optional[int] = None
    name: str
    min_cgpa: Optional[float] = None
    max_backlogs: Optional[int] = None
    eligible_branches: List[str] = []
    ctc: Optional[str] = None
    roles: List[str] = []
    selection_process: List[str] = []
    doc_source: str = ""

class CompanyComparisonRequest(BaseModel):
    company_names: List[str]

class CompanyComparisonResponse(BaseModel):
    companies: List[CompanyDetail]
    matrix: Dict[str, Any]

# Placement Eligibility Check
class PlacementEligibilityRequest(BaseModel):
    company_name: Optional[str] = None # If None, check all available companies

class PlacementEligibilityResponse(BaseModel):
    profile: StudentProfileBase
    results: List[EligibilityResult]

# Career Roadmap
class CareerRoadmapRequest(BaseModel):
    target_role: str
    current_skill_level: Optional[str] = "Beginner"
    preparation_time: Optional[str] = "3 Months"

class CareerRoadmapResponse(BaseModel):
    target_role: str
    timeline_duration: str
    skills_to_learn: List[str]
    learning_sequence: List[Dict[str, Any]]
    projects_to_build: List[Dict[str, str]]
    interview_topics: List[str]
    resume_focus: List[str]
    placement_officer_tips: List[str]
    is_general_guidance: bool = True

# Interview Prep
class InterviewPrepRequest(BaseModel):
    target_role: str
    topic: Optional[str] = "All Topics"
    difficulty: Optional[str] = "Intermediate"

class InterviewQuestion(BaseModel):
    category: str # "Technical", "SQL", "System Design", "HR", "Behavioral"
    question: str
    model_answer: str
    tip: str
    difficulty: str = "Intermediate" 

class InterviewPrepResponse(BaseModel):
    target_role: str
    questions: List[InterviewQuestion]
    preparation_checklist: List[str]

# Resume Guidance
class ResumeGuidanceRequest(BaseModel):
    target_role: str
    skills: str
    projects: Optional[str] = ""

class ResumeGuidanceResponse(BaseModel):
    target_role: str
    ats_score: int
    score_breakdown: Dict[str, int]
    highlight_skills: List[str]
    suggested_bullet_points: List[str]
    missing_skill_areas: List[str]
    disclaimer: str = "These suggestions may improve alignment with the target role."

# Document & KB Management
class DocumentResponse(BaseModel):
    id: int
    filename: str
    category: str
    company: Optional[str] = None
    upload_date: datetime
    chunk_count: int
    status: str

    class Config:
        from_attributes = True

class KBStatusResponse(BaseModel):
    status: str
    total_documents: int
    total_chunks: int
    vector_count: int
    last_updated: str

class RetrievalTestRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class RetrievalChunkResult(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    category: Optional[str] = None
    company: Optional[str] = None
    similarity_score: float
    text: str

class RetrievalTestResponse(BaseModel):
    query: str
    results: List[RetrievalChunkResult]
