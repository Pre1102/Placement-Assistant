import re

class QueryClassifier:
    @staticmethod
    def classify(query: str) -> dict:
        """
        Classifies user query into one of 8 standardized placement/career categories.
        Returns a dictionary: {"category": "CATEGORY_NAME", "reason": "Explanation"}
        """
        q = query.lower().strip()
        
        # 1. Eligibility Check Queries
        if any(kw in q for kw in ["eligible", "eligibility", "can i apply", "can i participate", "am i allowed", "eligible for", "with 1 backlog", "with 2 backlogs", "backlog policy"]):
            return {
                "category": "PLACEMENT_ELIGIBILITY",
                "reason": "Query contains eligibility, application rules, or student criteria checks."
            }
            
        # 2. Company Specific Requirements
        if any(kw in q for kw in ["company", "company a", "company b", "company c", "company d", "ctc", "package", "salary", "criteria for company", "requirements for company", "apex ai", "global data", "tech solutions"]):
            return {
                "category": "COMPANY_REQUIREMENTS",
                "reason": "Query asks about company recruitment requirements, CGPA criteria, or packages."
            }
            
        # 3. Placement Procedure & Rules
        if any(kw in q for kw in ["register", "registration", "policy", "rule", "procedure", "process", "document", "documents required", "shortlist", "ppt", "pre-placement", "marksheet", "noc"]):
            return {
                "category": "PLACEMENT_PROCEDURE",
                "reason": "Query inquires about placement registration, policies, rules, or required documents."
            }

        # 4. Internship Guidelines
        if any(kw in q for kw in ["internship", "intern", "stipend", "ppo", "semester viii", "semester 8", "monthly report"]):
            return {
                "category": "INTERNSHIP",
                "reason": "Query specifically concerns internship guidelines, stipends, or PPOs."
            }

        # 5. Career Guidance & Roadmaps
        if any(kw in q for kw in ["roadmap", "career", "how to prepare for", "prepare for role", "data analyst role", "software developer role", "ai/ml", "cybersecurity", "cloud engineer", "learning sequence", "skills to learn"]):
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

        # Default fallback
        return {
            "category": "GENERAL",
            "reason": "Query classified under general campus placement assistance."
        }
