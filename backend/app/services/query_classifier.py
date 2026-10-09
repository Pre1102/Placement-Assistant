import re

class QueryClassifier:
    @staticmethod
    def classify(query: str) -> dict:
        """
        Classifies user query into one of standardized placement/career categories.
        Returns a dictionary: {"category": "CATEGORY_NAME", "reason": "Explanation"}
        """
        q = query.lower().strip()

        # 1. Internship Guidelines (High Priority)
        if any(kw in q for kw in ["internship", "intern", "stipend", "ppo", "semester viii", "semester 8", "monthly report"]):
            return {
                "category": "INTERNSHIP",
                "reason": "Query specifically concerns internship guidelines, stipends, or PPOs."
            }

        # 2. Company Specific Requirements (CTC, packages, company requirements)
        if any(kw in q for kw in [
            "ctc", "package", "salary", "selection procedure", "job roles offered",
            "minimum cgpa required for demo company", "branches are eligible for demo company",
            "active backlog policy for demo company", "package for demo company"
        ]):
            return {
                "category": "COMPANY_REQUIREMENTS",
                "reason": "Query asks about company recruitment requirements, CGPA criteria, or packages."
            }
        
        # 3. Eligibility Check Queries
        if any(kw in q for kw in [
            "can i apply", "can a student", "eligible", "eligibility", "am i eligible",
            "am i allowed", "can i participate", "with 1 backlog", "with 2 backlogs", "with 3 backlogs"
        ]):
            return {
                "category": "PLACEMENT_ELIGIBILITY",
                "reason": "Query contains student eligibility checks or backlog rules."
            }

        # 4. Placement Procedure & Rules
        if any(kw in q for kw in [
            "register", "registration", "policy", "rule", "procedure", "process",
            "document", "documents required", "shortlist", "ppt", "pre-placement",
            "one student one job", "dream option", "miss an interview", "stages of campus recruitment"
        ]):
            return {
                "category": "PLACEMENT_PROCEDURE",
                "reason": "Query inquires about placement registration, policies, rules, or required documents."
            }

        # 5. Career Guidance & Roadmaps
        if any(kw in q for kw in [
            "roadmap", "career", "how should i prepare for", "skills are needed for", "learning roadmap",
            "key learning phases", "data analyst role", "software developer position",
            "ai/ml engineer", "cybersecurity", "web developer", "cloud engineer"
        ]):
            return {
                "category": "CAREER_GUIDANCE",
                "reason": "Query seeks career roadmaps, learning paths, or role skill recommendations."
            }

        # 6. Interview Preparation
        if any(kw in q for kw in ["interview", "questions", "technical questions", "hr questions", "behavioral", "mock interview", "interview prep"]):
            return {
                "category": "INTERVIEW_PREPARATION",
                "reason": "Query asks for interview preparation questions or practice material."
            }

        # 7. Resume Guidance
        if any(kw in q for kw in ["resume", "cv", "ats", "bullet points", "highlight skills", "projects on resume"]):
            return {
                "category": "RESUME_GUIDANCE",
                "reason": "Query requests resume formatting, project highlights, or skill recommendations."
            }

        # Fallback to General
        return {
            "category": "GENERAL",
            "reason": "Query classified under general campus placement assistance."
        }
