class CareerEngine:
    ROADMAPP_DATA = {
        "Data Analyst": {
            "skills": ["Excel", "SQL", "Python", "Pandas", "Power BI", "Statistics", "EDA"],
            "sequence": [
                {"month": "Month 1", "focus": "Excel & SQL Fundamentals", "topics": ["Pivot Tables", "VLOOKUP", "JOINs", "Group By", "Subqueries", "Window Functions"]},
                {"month": "Month 2", "focus": "Python & Data Wrangling", "topics": ["Python Basics", "NumPy Arrays", "Pandas DataFrames", "Data Cleaning", "Handling Missing Values"]},
                {"month": "Month 3", "focus": "Visualization & Power BI", "topics": ["Power BI Dashboards", "DAX Expressions", "Matplotlib", "Seaborn", "Storytelling with Data"]},
                {"month": "Month 4", "focus": "Statistics & Portfolio Project", "topics": ["Descriptive Statistics", "Hypothesis Testing", "Correlation Analysis", "2 End-to-End Projects"]}
            ],
            "projects": [
                {"title": "E-Commerce Sales Analytics Dashboard", "description": "Interactive Power BI dashboard summarizing revenue trends, region performance, and product category churn."},
                {"title": "Customer Churn Prediction Dataset Analysis", "description": "Python EDA project identifying key risk factors using Pandas and SQL queries."}
            ],
            "topics": ["SQL Queries & Window Functions", "Data Cleaning Techniques", "Business Case Studies", "Statistics & Probability"],
            "resume_focus": ["Quantify impact (e.g. 'Improved query efficiency by 30%')", "Highlight SQL JOINs and Power BI dashboards", "Include Github repo link to Jupyter Notebooks"]
        },
        "Software Developer": {
            "skills": ["Data Structures & Algorithms", "Python/C++/Java", "SQL", "Git", "REST APIs", "System Design Basics"],
            "sequence": [
                {"month": "Month 1", "focus": "DSA Fundamentals", "topics": ["Arrays", "Strings", "Hash Tables", "Two Pointers", "Sliding Window"]},
                {"month": "Month 2", "focus": "Advanced DSA & OOP", "topics": ["Recursion", "Trees", "Graphs", "Dynamic Programming", "Object-Oriented Design"]},
                {"month": "Month 3", "focus": "Backend API & Database", "topics": ["FastAPI / Express.js", "Relational Database Design", "SQL Indexing", "REST Principles"]},
                {"month": "Month 4", "focus": "Full-Stack Project & Git", "topics": ["Frontend Integration", "Git & GitHub Workflow", "Unit Testing", "Deployment"]}
            ],
            "projects": [
                {"title": "Placement Intelligence Web App", "description": "Full-stack application with REST API backend, SQLite storage, and responsive React frontend."},
                {"title": "Distributed File Synchronizer", "description": "Multi-threaded client-server tool built using Python socket programming."}
            ],
            "topics": ["Time & Space Complexity", "Data Structure Selection", "SQL Normalization & Indexes", "REST API Error Handling"],
            "resume_focus": ["Demonstrate problem-solving (e.g., 'Solved 250+ LeetCode problems')", "Highlight tech stack explicitly", "Provide live project demo links"]
        },
        "AI/ML Engineer": {
            "skills": ["Linear Algebra", "Python", "NumPy", "Scikit-Learn", "PyTorch", "Generative AI", "RAG & Vector DBs"],
            "sequence": [
                {"month": "Month 1", "focus": "Math & Data Foundations", "topics": ["Linear Algebra", "Calculus", "Probability", "NumPy & Pandas"]},
                {"month": "Month 2", "focus": "Classical Machine Learning", "topics": ["Supervised Learning", "Random Forests", "XGBoost", "Model Evaluation Metrics"]},
                {"month": "Month 3", "focus": "Deep Learning & PyTorch", "topics": ["Neural Networks", "CNNs", "Optimization Algorithms", "PyTorch Basics"]},
                {"month": "Month 4", "focus": "Generative AI & RAG", "topics": ["Embeddings", "FAISS Vector Database", "LLM Prompting & API Integration"]}
            ],
            "projects": [
                {"title": "Source-Grounded Document QA System", "description": "RAG pipeline using Sentence Transformers, FAISS vector search, and Gemini LLM synthesis."},
                {"title": "Medical Image Classification", "description": "Convolutional Neural Network built with PyTorch achieving 92% evaluation accuracy."}
            ],
            "topics": ["Precision, Recall & F1-Score", "Overfitting & Regularization", "Vector Similarity Metrics", "LLM Fine-Tuning vs RAG"],
            "resume_focus": ["Focus on model accuracy & performance metrics", "Detail datasets used", "Include ML architecture diagrams"]
        },
        "Cybersecurity": {
            "skills": ["Linux", "Networking (TCP/IP)", "Wireshark", "Nmap", "Vulnerability Scanning", "Cryptography"],
            "sequence": [
                {"month": "Month 1", "focus": "Networking & Linux Fundamentals", "topics": ["OSI Layer", "TCP/UDP Protocols", "Linux Command Line", "Shell Scripting"]},
                {"month": "Month 2", "focus": "Security Fundamentals", "topics": ["Encryption (AES/RSA)", "Hashing", "Firewalls", "Nmap Port Scanning"]},
                {"month": "Month 3", "focus": "Web Security & OWASP", "topics": ["SQL Injection", "XSS", "CSRF", "Wireshark Packet Analysis"]},
                {"month": "Month 4", "focus": "Labs & Security Operations", "topics": ["TryHackMe Rooms", "SIEM Log Analysis", "CompTIA Security+ Prep"]}
            ],
            "projects": [
                {"title": "Automated Network Vulnerability Scanner", "description": "Python CLI tool integrating Nmap to identify open ports and weak SSL configurations."},
                {"title": "SOC Log Monitoring Dashboard", "description": "Log parser detecting anomalous authentication spikes."}
            ],
            "topics": ["OSI Model & Port Numbers", "Symmetric vs Asymmetric Encryption", "OWASP Top 10", "Incident Response Steps"],
            "resume_focus": ["List hands-on lab badges (TryHackMe / HTB)", "Highlight Linux & Wireshark mastery", "Mention relevant certifications"]
        }
    }

    @classmethod
    def get_roadmap(cls, target_role: str, current_level: str = "Beginner", prep_time: str = "3 Months") -> dict:
        data = cls.ROADMAPP_DATA.get(target_role, cls.ROADMAPP_DATA["Software Developer"])
        return {
            "target_role": target_role,
            "skills_to_learn": data["skills"],
            "learning_sequence": data["sequence"],
            "projects_to_build": data["projects"],
            "interview_topics": data["topics"],
            "resume_focus": data["resume_focus"],
            "is_general_guidance": True
        }

    @classmethod
    def generate_interview_questions(cls, target_role: str, topic: str = "All", difficulty: str = "Intermediate") -> dict:
        questions = [
            {"category": "Technical", "question": f"Explain the core data structures or primary tools used in {target_role}.", "tip": "State trade-offs, time complexity, and real-world application scenarios."},
            {"category": "Technical", "question": f"How do you handle performance bottlenecks or unexpected data errors in a {target_role} workflow?", "tip": "Structure answer using Problem -> Investigation -> Resolution -> Prevention."},
            {"category": "Behavioral", "question": "Describe a technical project where you faced a tight deadline or conflicting requirements.", "tip": "Use STAR method (Situation, Task, Action, Result)."},
            {"category": "HR", "question": "Why do you want to join our organization and how does this role align with your 3-year plan?", "tip": "Demonstrate knowledge of company domain and express enthusiasm for continuous learning."}
        ]
        
        checklist = [
            "Review your listed resume projects thoroughly.",
            "Practice writing clean code or SQL queries on a whiteboard / paper.",
            "Prepare 2-3 thoughtful questions to ask the interviewer.",
            "Ensure stable internet connection and professional background for virtual interviews."
        ]
        
        return {
            "target_role": target_role,
            "questions": questions,
            "preparation_checklist": checklist
        }

    @classmethod
    def generate_resume_guidance(cls, target_role: str, student_skills: str, projects: str = "") -> dict:
        data = cls.ROADMAPP_DATA.get(target_role, cls.ROADMAPP_DATA["Software Developer"])
        
        student_skill_list = [s.strip().lower() for s in student_skills.split(",")]
        missing = [s for s in data["skills"] if s.lower() not in student_skill_list]
        
        bullets = [
            f"Designed and implemented a full-featured project using {student_skills.split(',')[0] if student_skills else 'Python'} targeting {target_role} requirements.",
            f"Optimized database queries and data processing pipelines to improve application efficiency by 25%.",
            f"Collaborated on technical documentation, version control, and system testing."
        ]
        
        return {
            "target_role": target_role,
            "highlight_skills": [s for s in data["skills"] if s.lower() in student_skill_list] or data["skills"][:3],
            "suggested_bullet_points": bullets,
            "missing_skill_areas": missing if missing else ["Advanced System Architecture"],
            "disclaimer": "These changes may improve alignment with the target role."
        }
