import os
import fitz  # PyMuPDF

DISCLAIMER = "DEMO DATA — For academic prototype/testing only. Not an official college/company policy."

DOCUMENTS = [
    {
        "filename": "DEMO_Placement_Policy.pdf",
        "title": "Institutional Placement Policy 2026-2027",
        "category": "Placement Rules",
        "pages": [
            [
                "Institutional Placement Policy 2026-2027",
                DISCLAIMER,
                "Section 1: General Eligibility",
                "1. Students must maintain a minimum overall CGPA of 6.0 to participate in the campus placement drive.",
                "2. Students with more than 2 active backlogs at the time of registration are not eligible for Tier-1 company drives.",
                "3. Eligible branches for general drives include Computer Engineering (CE), Computer Science & Engineering (CSE), Information Technology (IT), Electronics & Communication (ECE), and Electrical Engineering (EE).",
                "Section 2: Code of Conduct & Offer Rules",
                "1. One Student, One Job Policy: Once a student receives a confirmed placement offer with a CTC above 6 LPA, they are considered placed and cannot apply for lower or equivalent tier companies.",
                "2. Dream Option: Placed students with a package under 8 LPA may apply for one 'Dream Company' offering a CTC greater than 12 LPA.",
                "3. Students absenting from an interview after being shortlisted will be barred from the next 2 campus recruitment drives."
            ]
        ]
    },
    {
        "filename": "DEMO_Placement_Registration.pdf",
        "title": "Placement Registration & Verification Procedure",
        "category": "Placement Procedures",
        "pages": [
            [
                "Placement Registration & Verification Procedure",
                DISCLAIMER,
                "Section 1: Registration Timeline",
                "Placement registration opens on July 1st and closes on August 15th for final year (Semester VII) students.",
                "Section 2: Mandatory Required Documents",
                "Students must submit the following verified documents to the Placement Cell prior to registration:",
                "1. Updated One-Page Professional Resume (PDF format).",
                "2. All semester marksheets (Semester I to Semester VI) verified by the academic section.",
                "3. Official Identity Card and Aadhar Card copy.",
                "4. No-Objection Certificate (NOC) signed by the Head of Department (HOD) if applying for semester-long internships.",
                "5. Passport size photographs (4 copies)."
            ]
        ]
    },
    {
        "filename": "DEMO_Placement_FAQ.pdf",
        "title": "Campus Placement Frequently Asked Questions (FAQ)",
        "category": "Placement FAQs",
        "pages": [
            [
                "Campus Placement Frequently Asked Questions (FAQ)",
                DISCLAIMER,
                "Q1: What happens if I clear my active backlog before the company onboarding date?",
                "A: Company eligibility is verified at the time of shortlisting/application. If a company allows 0 active backlogs, you cannot apply even if you clear it later. If a company allows 1 active backlog on the condition of clearing before onboarding, official proof must be submitted to the Placement Cell.",
                "Q2: Can I apply to a company if my branch is not explicitly listed in the notice?",
                "A: No. Shortlisting filters strictly adhere to the eligible branches specified in the recruitment notice issued by the Training & Placement Cell.",
                "Q3: Are online certifications accepted as proof of skills?",
                "A: Certifications from recognized platforms (Coursera, NPTEL, edX) strengthen your resume but do not override CGPA or backlog eligibility rules."
            ]
        ]
    },
    {
        "filename": "DEMO_Company_A_Requirements.pdf",
        "title": "Recruitment Notice: Demo Company A (Tech Solutions)",
        "category": "Company Notices",
        "pages": [
            [
                "Recruitment Notice: Demo Company A (Tech Solutions)",
                DISCLAIMER,
                "Company Profile: Demo Company A is a premier software product firm.",
                "Eligible Branches: Computer Engineering (CE), Computer Science & Engineering (CSE).",
                "Minimum CGPA Criterion: 7.0 / 10.0 (No rounding allowed).",
                "Active Backlog Policy: Maximum 0 active backlogs allowed. All previous backlogs must be cleared.",
                "Offered CTC: 8.5 LPA.",
                "Job Roles: Software Engineer, Backend Developer.",
                "Selection Procedure:",
                "Step 1: Online Technical Assessment (Data Structures, Algorithms, SQL, Quantitative Aptitude).",
                "Step 2: Technical Interview Round 1 (Coding & System Concepts).",
                "Step 3: Technical Interview Round 2 (Project Architecture & Problem Solving).",
                "Step 4: HR & Cultural Fit Interview."
            ]
        ]
    },
    {
        "filename": "DEMO_Company_B_Requirements.pdf",
        "title": "Recruitment Notice: Demo Company B (Global Data Corp)",
        "category": "Company Notices",
        "pages": [
            [
                "Recruitment Notice: Demo Company B (Global Data Corp)",
                DISCLAIMER,
                "Company Profile: Demo Company B specializes in enterprise analytics and cloud insights.",
                "Eligible Branches: Computer Engineering (CE), CSE, Information Technology (IT), Electronics & Communication (ECE).",
                "Minimum CGPA Criterion: 6.5 / 10.0.",
                "Active Backlog Policy: Maximum 1 active backlog allowed at the time of application.",
                "Offered CTC: 6.8 LPA.",
                "Job Roles: Data Analyst, Cloud Operations Engineer.",
                "Selection Procedure:",
                "Step 1: Online Aptitude & Coding Assessment (SQL, Data Interpretation, Python basics).",
                "Step 2: Technical Interview (SQL queries, Case Study analysis, Python/Pandas).",
                "Step 3: HR Round."
            ]
        ]
    },
    {
        "filename": "DEMO_Company_C_Requirements.pdf",
        "title": "Recruitment Notice: Demo Company C (Apex AI Labs)",
        "category": "Company Notices",
        "pages": [
            [
                "Recruitment Notice: Demo Company C (Apex AI Labs)",
                DISCLAIMER,
                "Company Profile: Apex AI Labs works on generative AI products and deep learning infrastructure.",
                "Eligible Branches: Computer Engineering (CE), CSE.",
                "Minimum CGPA Criterion: 7.5 / 10.0.",
                "Active Backlog Policy: Strictly 0 active backlogs (No dead/active backlogs permitted).",
                "Offered CTC: 14.0 LPA.",
                "Job Roles: AI/ML Engineer, Machine Learning Research Associate.",
                "Selection Procedure:",
                "Step 1: Resume Screening & Github Portfolio Evaluation.",
                "Step 2: Advanced Machine Learning & Math Assessment.",
                "Step 3: Live Coding & Deep Learning Architecture Interview.",
                "Step 4: Founder / Technical Leadership Round."
            ]
        ]
    },
    {
        "filename": "DEMO_Company_D_Requirements.pdf",
        "title": "Recruitment Notice: Demo Company D (SecureNet Systems)",
        "category": "Company Notices",
        "pages": [
            [
                "Recruitment Notice: Demo Company D (SecureNet Systems)",
                DISCLAIMER,
                "Company Profile: SecureNet Systems provides cybersecurity consulting and cloud security solutions.",
                "Eligible Branches: CE, CSE, IT, ECE, Electrical Engineering (EE).",
                "Minimum CGPA Criterion: 6.0 / 10.0.",
                "Active Backlog Policy: Maximum 2 active backlogs permitted.",
                "Offered CTC: 5.5 LPA.",
                "Job Roles: Associate Security Analyst, Network Engineer.",
                "Selection Procedure:",
                "Step 1: Cybersecurity & Networking Fundamentals Test.",
                "Step 2: Technical Interview (Linux commands, OSI Model, Firewalls, Python scripting).",
                "Step 3: HR Interview."
            ]
        ]
    },
    {
        "filename": "DEMO_Internship_Guidelines.pdf",
        "title": "Semester VIII Full-Time Internship Guidelines",
        "category": "Internship",
        "pages": [
            [
                "Semester VIII Full-Time Internship Guidelines",
                DISCLAIMER,
                "Guideline 1: Internship Eligibility",
                "Final year students undergoing 8th semester full-time internship must complete all core course credits by Semester VII.",
                "Guideline 2: Monthly Progress Reports",
                "Interns are required to submit monthly evaluation reports countersigned by their Industry Mentor and Internal Academic Guide.",
                "Guideline 3: Stipend & Pre-Placement Offer (PPO)",
                "Minimum recommended stipend for full-time technical internships is INR 15,000 per month. If offered a PPO, students must inform the Placement Cell within 7 business days."
            ]
        ]
    },
    {
        "filename": "DEMO_Recruitment_Process.pdf",
        "title": "Standard Campus Recruitment Process & Stages",
        "category": "Placement Procedures",
        "pages": [
            [
                "Standard Campus Recruitment Process & Stages",
                DISCLAIMER,
                "Stage 1: Pre-Placement Talk (PPT)",
                "Companies introduce their culture, career progression, bond terms, and salary breakdown.",
                "Stage 2: Shortlisting & Online Screening",
                "Includes aptitude tests, domain coding tests, psychometric assessments, and resume screening based on CGPA.",
                "Stage 3: Group Discussion (GD) / Case Study (Optional)",
                "Evaluates communication skills, logical reasoning, teamwork, and domain knowledge.",
                "Stage 4: Technical & HR Interviews",
                "Depth evaluation of projects, core fundamentals, data structures, database management, and behavioral fitment."
            ]
        ]
    },
    {
        "filename": "DEMO_Data_Analyst_Roadmap.pdf",
        "title": "Career Roadmap: Data Analyst Role",
        "category": "Career Guidance",
        "pages": [
            [
                "Career Roadmap: Data Analyst Role",
                DISCLAIMER,
                "Phase 1 (Month 1): Spreadsheet & Database Fundamentals",
                "Master Advanced Excel (Pivot tables, VLOOKUP, XLOOKUP, Index-Match) and SQL (JOINs, Group By, Subqueries, Window Functions).",
                "Phase 2 (Month 2): Data Manipulation with Python",
                "Learn Python core syntax, NumPy, Pandas dataframes, and data cleaning techniques.",
                "Phase 3 (Month 3): Visualization & Dashboarding",
                "Build interactive dashboards using Power BI or Tableau. Master Matplotlib and Seaborn.",
                "Phase 4 (Month 4): Statistics & Business Analytics",
                "Understand descriptive statistics, hypothesis testing, probability, and exploratory data analysis (EDA). Build 2 end-to-end portfolio projects."
            ]
        ]
    },
    {
        "filename": "DEMO_Software_Developer_Roadmap.pdf",
        "title": "Career Roadmap: Software Developer Role",
        "category": "Career Guidance",
        "pages": [
            [
                "Career Roadmap: Software Developer Role",
                DISCLAIMER,
                "Phase 1: Computer Science Core & Data Structures",
                "Master Array, String, Linked List, Stack, Queue, Binary Tree, Graph algorithms in Python/C++/Java.",
                "Phase 2: Database & System Fundamentals",
                "Study Relational Databases (PostgreSQL/MySQL), Normalization, Indexing, and Operating System / Networking basics.",
                "Phase 3: Web Application Architecture",
                "Build RESTful APIs with FastAPI or Express.js. Frontend integration using React and responsive CSS.",
                "Phase 4: Software Engineering & Git Workflow",
                "Practice Git, GitHub Actions, Docker basics, unit testing, and design patterns. Build a full-stack capstone project."
            ]
        ]
    },
    {
        "filename": "DEMO_AI_ML_Roadmap.pdf",
        "title": "Career Roadmap: AI / Machine Learning Engineer",
        "category": "Career Guidance",
        "pages": [
            [
                "Career Roadmap: AI / Machine Learning Engineer",
                DISCLAIMER,
                "Phase 1: Mathematics & Python Foundations",
                "Linear Algebra, Multivariable Calculus, Probability, NumPy, and Scikit-Learn.",
                "Phase 2: Supervised & Unsupervised Machine Learning",
                "Regression, Classification, Decision Trees, Random Forests, XGBoost, K-Means clustering, and Model Evaluation metrics.",
                "Phase 3: Deep Learning & Neural Networks",
                "PyTorch / TensorFlow, Convolutional Neural Networks (CNN), Recurrent Networks (RNN/LSTM), and Transformers.",
                "Phase 4: Generative AI & RAG Engineering",
                "LLM fine-tuning, Prompt Engineering, Vector Databases (FAISS), Embedding Models, and LangChain/LlamaIndex paradigms."
            ]
        ]
    },
    {
        "filename": "DEMO_Cybersecurity_Roadmap.pdf",
        "title": "Career Roadmap: Cybersecurity Analyst",
        "category": "Career Guidance",
        "pages": [
            [
                "Career Roadmap: Cybersecurity Analyst",
                DISCLAIMER,
                "Phase 1: Networking & Linux Mastery",
                "OSI Model, TCP/IP, Linux command line, Wireshark packet capture, Subnetting.",
                "Phase 2: Security Concepts & Vulnerability Assessment",
                "OWASP Top 10 web vulnerabilities, cryptography, public key infrastructure (PKI), Nmap scanning.",
                "Phase 3: Defense & Incident Response",
                "SIEM tools (Splunk, Elastic), Log analysis, Malware analysis basics, Security Operations Center (SOC) workflows.",
                "Phase 4: Certifications & Hands-on Labs",
                "Practice on TryHackMe, HackTheBox. Prepare for CompTIA Security+ or Certified Ethical Hacker (CEH)."
            ]
        ]
    }
]

def create_demo_pdfs():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "demo")
    os.makedirs(out_dir, exist_ok=True)
    
    generated = 0
    for doc_info in DOCUMENTS:
        file_path = os.path.join(out_dir, doc_info["filename"])
        pdf_doc = fitz.open()
        
        for page_lines in doc_info["pages"]:
            page = pdf_doc.new_page(width=595, height=842) # A4 size
            
            y = 50
            # Header title
            page.insert_text((40, y), page_lines[0], fontsize=16, fontname="helv", color=(0.02, 0.58, 0.41)) # Emerald green header
            y += 25
            
            # Disclaimer
            page.insert_text((40, y), page_lines[1], fontsize=9, fontname="helv", color=(0.8, 0.1, 0.1))
            y += 30
            
            # Content lines
            for line in page_lines[2:]:
                if line.startswith("Section") or line.startswith("Q") or line.startswith("Phase") or line.startswith("Stage") or line.startswith("Step"):
                    y += 10
                    page.insert_text((40, y), line, fontsize=12, fontname="helv", color=(0.1, 0.1, 0.1))
                    y += 20
                else:
                    # Wrap long text manually if needed
                    words = line.split(" ")
                    current_line = ""
                    for w in words:
                        if len(current_line + " " + w) > 75:
                            page.insert_text((50, y), current_line, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                            y += 16
                            current_line = w
                        else:
                            current_line = (current_line + " " + w).strip()
                    if current_line:
                        page.insert_text((50, y), current_line, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                        y += 16
                
                if y > 780:
                    page = pdf_doc.new_page(width=595, height=842)
                    y = 50

        pdf_doc.save(file_path)
        pdf_doc.close()
        generated += 1
        print(f"[+] Created synthetic PDF: {doc_info['filename']}")
        
    print(f"\nSuccessfully generated {generated} synthetic placement & career PDFs in {out_dir}")

if __name__ == "__main__":
    create_demo_pdfs()
