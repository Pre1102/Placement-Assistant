from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Document, DocumentChunk
from app.models.schemas import CompanyDetail
from app.services.placement_engine import PlacementEligibilityEngine

router = APIRouter(prefix="/companies", tags=["Companies"])

DEMO_COMPANIES = [
    {
        "id": 1,
        "name": "Demo Company A",
        "min_cgpa": 7.0,
        "max_backlogs": 0,
        "eligible_branches": ["Computer Engineering", "Computer Science & Engineering"],
        "ctc": "8.5 LPA",
        "roles": ["Software Engineer", "Backend Developer"],
        "selection_process": ["Online Technical Assessment", "Technical Interview Round 1", "Technical Interview Round 2", "HR Round"],
        "doc_source": "DEMO_Company_A_Requirements.pdf"
    },
    {
        "id": 2,
        "name": "Demo Company B",
        "min_cgpa": 6.5,
        "max_backlogs": 1,
        "eligible_branches": ["Computer Engineering", "Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
        "ctc": "6.8 LPA",
        "roles": ["Data Analyst", "Cloud Operations Engineer"],
        "selection_process": ["Aptitude & Coding Test", "Technical Interview (SQL/Python)", "HR Round"],
        "doc_source": "DEMO_Company_B_Requirements.pdf"
    },
    {
        "id": 3,
        "name": "Demo Company C",
        "min_cgpa": 7.5,
        "max_backlogs": 0,
        "eligible_branches": ["Computer Engineering", "Computer Science & Engineering"],
        "ctc": "14.0 LPA",
        "roles": ["AI/ML Engineer", "Machine Learning Research Associate"],
        "selection_process": ["Resume & Portfolio Screening", "Advanced Math & ML Test", "Live Coding Interview", "Founder Round"],
        "doc_source": "DEMO_Company_C_Requirements.pdf"
    },
    {
        "id": 4,
        "name": "Demo Company D",
        "min_cgpa": 6.0,
        "max_backlogs": 2,
        "eligible_branches": ["Computer Engineering", "Computer Science & Engineering", "Information Technology", "Electronics & Communication", "Electrical Engineering"],
        "ctc": "5.5 LPA",
        "roles": ["Associate Security Analyst", "Network Engineer"],
        "selection_process": ["Networking Fundamentals Test", "Technical Interview", "HR Interview"],
        "doc_source": "DEMO_Company_D_Requirements.pdf"
    }
]

@router.get("", response_model=list[CompanyDetail])
def get_companies(db: Session = Depends(get_db)):
    # Dynamically supplement demo companies from indexed documents in SQLite
    companies_map = {c["name"]: CompanyDetail(**c) for c in DEMO_COMPANIES}

    company_docs = db.query(Document).filter(Document.category == "Company Notices").all()
    for doc in company_docs:
        c_name = doc.company or doc.filename.replace(".pdf", "").replace("DEMO_", "").replace("_Requirements", "").replace("_", " ")
        if c_name not in companies_map:
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).all()
            full_text = " ".join([ch.text for ch in chunks])
            parsed = PlacementEligibilityEngine.extract_company_criteria_from_text(full_text, c_name)
            
            companies_map[c_name] = CompanyDetail(
                id=doc.id + 100,
                name=c_name,
                min_cgpa=parsed["min_cgpa"],
                max_backlogs=parsed["max_backlogs"],
                eligible_branches=parsed["branches"],
                ctc="Negotiable / See Notice",
                roles=["Software Engineer"],
                selection_process=["Aptitude Test", "Technical Interview", "HR Round"],
                doc_source=doc.filename
            )

    return list(companies_map.values())

@router.get("/{company_id}", response_model=CompanyDetail)
def get_company(company_id: int, db: Session = Depends(get_db)):
    all_companies = get_companies(db)
    for c in all_companies:
        if c.id == company_id:
            return c
    raise HTTPException(status_code=404, detail="Company not found")
