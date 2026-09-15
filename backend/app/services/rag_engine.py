import re
from sqlalchemy.orm import Session
from app.services.query_classifier import QueryClassifier
from app.services.retriever import HybridRetriever
from app.services.llm_service import LLMService
from app.services.placement_engine import PlacementEligibilityEngine
from app.models.database_models import StudentProfile

class RAGEngine:
    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever

    def process_query(self, db: Session, query: str, user_id: int = 1) -> dict:
        """
        Processes student query through Query Classification, RAG Retrieval,
        Eligibility Engine, LLM Grounded Answer, and Source Attribution.
        """
        # 1. Query Classification
        classification = QueryClassifier.classify(query)
        category = classification["category"]

        # 2. Retrieve Relevant Chunks
        chunks = self.retriever.retrieve_chunks(db, query, top_k=4, score_threshold=0.20)

        # 3. Handle Unknown Information (If no context retrieved for institutional placement queries)
        is_unknown = False
        if not chunks and category in ["PLACEMENT_ELIGIBILITY", "COMPANY_REQUIREMENTS", "PLACEMENT_PROCEDURE", "INTERNSHIP"]:
            is_unknown = True

        # Extract Sources
        sources = []
        seen_sources = set()
        for c in chunks:
            key = f"{c['document_name']}_p{c['page_number']}"
            if key not in seen_sources:
                seen_sources.add(key)
                sources.append({
                    "document_name": c["document_name"],
                    "page_number": c["page_number"],
                    "category": c.get("category"),
                    "company": c.get("company"),
                    "snippet": c["text"][:120] + "..."
                })

        # 4. Data-driven Eligibility Evaluation if applicable
        eligibility_result = None
        if category in ["PLACEMENT_ELIGIBILITY", "COMPANY_REQUIREMENTS"]:
            # Retrieve student profile
            profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
            profile_dict = {
                "branch": profile.branch if profile else "Computer Engineering",
                "cgpa": profile.cgpa if profile else 7.2,
                "backlogs": profile.backlogs if profile else 1
            }

            # Identify target company name from query or retrieved chunks
            target_company = self._detect_company_name(query, chunks)
            
            # Combine retrieved text for criteria extraction
            context_text = " ".join([c["text"] for c in chunks])
            criteria = PlacementEligibilityEngine.extract_company_criteria_from_text(context_text, target_company)

            if criteria["min_cgpa"] is not None or criteria["max_backlogs"] is not None or criteria["branches"]:
                eligibility_result = PlacementEligibilityEngine.evaluate_eligibility(profile_dict, criteria, sources)

        # 5. Generate Grounded LLM Response
        answer = LLMService.generate_grounded_answer(query, category, chunks, unknown_flag=is_unknown)

        return {
            "category": category,
            "answer": answer,
            "eligibility_result": eligibility_result,
            "sources": sources,
            "unknown_query": is_unknown
        }

    def _detect_company_name(self, query: str, chunks: list[dict]) -> str:
        q_upper = query.upper()
        if "COMPANY A" in q_upper or "TECH SOLUTIONS" in q_upper:
            return "Demo Company A"
        if "COMPANY B" in q_upper or "GLOBAL DATA" in q_upper:
            return "Demo Company B"
        if "COMPANY C" in q_upper or "APEX AI" in q_upper:
            return "Demo Company C"
        if "COMPANY D" in q_upper or "SECURENET" in q_upper:
            return "Demo Company D"

        for c in chunks:
            if c.get("company"):
                return c["company"]
        return "Target Company"
