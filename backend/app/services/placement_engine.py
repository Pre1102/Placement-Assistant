import re

class PlacementEligibilityEngine:
    @staticmethod
    def extract_company_criteria_from_text(text: str, company_name: str = "") -> dict:
        """
        Parses text chunks to extract numeric/branch constraints for a company.
        """
        criteria = {
            "company_name": company_name,
            "min_cgpa": None,
            "max_backlogs": None,
            "branches": [],
            "ctc": None
        }

        # 1. CGPA extraction (e.g. "minimum cgpa: 7.0" or "cgpa criterion: 6.5")
        cgpa_match = re.search(r'(?:cgpa|grade|pointer)[^\d]*(\d+\.\d+|\d+)', text, re.IGNORECASE)
        if cgpa_match:
            try:
                criteria["min_cgpa"] = float(cgpa_match.group(1))
            except ValueError:
                pass

        # 2. Backlog extraction (e.g. "maximum 1 active backlog", "0 active backlogs", "up to 2 backlogs")
        backlog_match = re.search(r'(\d+)\s*(?:active\s*)?backlogs?', text, re.IGNORECASE)
        if backlog_match:
            try:
                criteria["max_backlogs"] = int(backlog_match.group(1))
            except ValueError:
                pass

        # 3. Branch extraction
        branches = []
        text_upper = text.upper()
        if "COMPUTER ENGINEERING" in text_upper or " CE " in text_upper or "CE," in text_upper or "(CE)" in text_upper:
            branches.append("Computer Engineering")
        if "COMPUTER SCIENCE" in text_upper or " CSE " in text_upper or "(CSE)" in text_upper:
            branches.append("Computer Science & Engineering")
        if "INFORMATION TECHNOLOGY" in text_upper or " IT " in text_upper or "(IT)" in text_upper:
            branches.append("Information Technology")
        if "ELECTRONICS" in text_upper or " ECE " in text_upper or "(ECE)" in text_upper:
            branches.append("Electronics & Communication")
        if "ELECTRICAL" in text_upper or " EE " in text_upper or "(EE)" in text_upper:
            branches.append("Electrical Engineering")
        
        criteria["branches"] = list(set(branches))
        return criteria

    @classmethod
    def evaluate_eligibility(cls, profile_dict: dict, criteria: dict, sources: list = None) -> dict:
        """
        Data-driven evaluation of student profile vs extracted company criteria.
        """
        checks = []
        reasons = []
        is_eligible = True

        student_cgpa = profile_dict.get("cgpa", 0.0)
        student_backlogs = profile_dict.get("backlogs", 0)
        student_branch = profile_dict.get("branch", "")

        req_min_cgpa = criteria.get("min_cgpa")
        req_max_backlogs = criteria.get("max_backlogs")
        req_branches = criteria.get("branches", [])
        company_name = criteria.get("company_name", "Company")

        if req_min_cgpa is None and req_max_backlogs is None and not req_branches:
            return {
                "company_name": company_name,
                "status": "Requirement Unknown",
                "reasons": ["Insufficient requirement details in knowledge base for this company."],
                "checks": [],
                "sources": sources or []
            }

        # CGPA Check
        if req_min_cgpa is not None:
            satisfied = student_cgpa >= req_min_cgpa
            if not satisfied:
                is_eligible = False
                reasons.append(f"Your CGPA ({student_cgpa}) is below required minimum of {req_min_cgpa}.")
            checks.append({
                "requirement_name": "Minimum CGPA",
                "required_value": f"≥ {req_min_cgpa}",
                "student_value": str(student_cgpa),
                "satisfied": satisfied
            })

        # Backlog Check
        if req_max_backlogs is not None:
            satisfied = student_backlogs <= req_max_backlogs
            if not satisfied:
                is_eligible = False
                reasons.append(f"Your active backlogs ({student_backlogs}) exceed maximum limit of {req_max_backlogs}.")
            checks.append({
                "requirement_name": "Active Backlogs",
                "required_value": f"≤ {req_max_backlogs}",
                "student_value": str(student_backlogs),
                "satisfied": satisfied
            })

        # Branch Check
        if req_branches:
            # Check for partial / abbreviated match
            branch_match = any(
                b.lower() in student_branch.lower() or student_branch.lower() in b.lower()
                for b in req_branches
            )
            if not branch_match:
                is_eligible = False
                reasons.append(f"Your branch ({student_branch}) is not listed under eligible branches ({', '.join(req_branches)}).")
            checks.append({
                "requirement_name": "Eligible Branch",
                "required_value": ", ".join(req_branches),
                "student_value": student_branch,
                "satisfied": branch_match
            })

        status = "Eligible" if is_eligible else "Not Eligible"
        if is_eligible:
            reasons.append("You meet all specified mandatory eligibility requirements.")

        return {
            "company_name": company_name,
            "status": status,
            "reasons": reasons,
            "checks": checks,
            "sources": sources or []
        }
