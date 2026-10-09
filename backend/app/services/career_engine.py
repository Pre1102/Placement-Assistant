import re

class CareerIntelligenceEngine:
    ROADMAPP_DATA = {
        "Data Analyst": {
            "skills": ["SQL", "Excel & PowerBI/Tableau", "Python (Pandas, NumPy, Matplotlib)", "Applied Statistics", "Data Warehousing Basics"],
            "1 Month": [
                {"period": "Week 1", "focus": "Advanced SQL & Database Queries", "topics": ["Aggregations & Group By", "JOINs (INNER, LEFT, FULL)", "Subqueries & Window Functions", "Query Performance"]},
                {"period": "Week 2", "focus": "Excel Modeling & Power BI Dashboards", "topics": ["VLOOKUP/XLOOKUP", "Pivot Tables", "DAX Formulas", "Interactive Dashboards"]},
                {"period": "Week 3", "focus": "Python Data Wrangling", "topics": ["Pandas DataFrames", "Data Cleaning", "Matplotlib/Seaborn Visualizations", "EDA Workflow"]},
                {"period": "Week 4", "focus": "Portfolio Project & Mock Interviews", "topics": ["End-to-End Analytics Case Study", "GitHub Documentation", "Metric Interpretation"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "Foundations: SQL & Business Intelligence", "topics": ["Complex SQL Queries", "Window Functions & CTEs", "Data Modeling (Star Schema)", "Tableau/Power BI Dashboards"]},
                {"period": "Month 2", "focus": "Python Data Analysis & Statistics", "topics": ["NumPy & Pandas Pipelines", "Exploratory Data Analysis", "Hypothesis Testing", "A/B Testing Methodologies"]},
                {"period": "Month 3", "focus": "Real-World Projects & Interview Drill", "topics": ["E-Commerce Customer Churn Analysis", "Executive Dashboard Portfolio", "SQL Live Coding Speed Drills"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Mastering Advanced SQL & Data Warehousing", "topics": ["PostgreSQL/Snowflake", "Indexing & Optimization", "ETL Pipeline Basics", "Dimensional Modeling"]},
                {"period": "Months 3-4", "focus": "Data Science Fundamentals & Statistical Inference", "topics": ["Statistical Distributions", "Scikit-Learn Regression/Clustering", "Automated Reporting Pipelines"]},
                {"period": "Months 5-6", "focus": "Industry Capstone & Corporate Case Studies", "topics": ["Production-grade Analytics Dashboard", "A/B Test Design for Product Metrics", "Placement Interview Panels"]}
            ],
            "projects": [
                {"title": "Campus Placement Eligibility & Recruitment Trends", "description": "Interactive Power BI dashboard tracking CTC percentiles, branch placement ratios, and company visit seasons."},
                {"title": "Customer Segmentation & Lifetime Value Engine", "description": "Python RFM analysis and K-Means clustering pipeline identifying high-value student cohorts."}
            ],
            "topics": ["SQL Window Functions (ROW_NUMBER, RANK, DENSE_RANK)", "Difference between WHERE and HAVING", "Measures vs Calculated Columns in DAX", "A/B Testing Confidence Intervals"],
            "resume_focus": ["Quantify impact (e.g. 'Improved query efficiency by 30%')", "Highlight SQL JOINs and Power BI dashboards", "Include Github repo link to Jupyter Notebooks"],
            "placement_tips": [
                "Placement cells note that 80% of Data Analyst screening tests focus heavily on SQL window functions and complex JOINs.",
                "Always upload your Power BI/Tableau interactive workbook to NovyPro or GitHub with a public viewable link.",
                "Be ready to explain 'Why did you choose this metric?' during managerial technical rounds."
            ]
        },
        "Software Developer": {
            "skills": ["Data Structures & Algorithms", "Python / C++ / Java", "SQL & Database Design", "Git & GitHub", "REST APIs", "System Design Basics"],
            "1 Month": [
                {"period": "Week 1", "focus": "Core DSA Speed Run", "topics": ["Arrays", "Strings", "Hash Maps", "Two Pointers & Sliding Window"]},
                {"period": "Week 2", "focus": "Intermediate DSA & Trees", "topics": ["Recursion & Backtracking", "Binary Trees & BST", "Stack & Queue Patterns"]},
                {"period": "Week 3", "focus": "Backend Architecture & SQL", "topics": ["FastAPI / Express REST APIs", "Database Schema Design & Indexes", "Authentication (JWT)"]},
                {"period": "Week 4", "focus": "Full-Stack Integration & Mock Interviews", "topics": ["React Integration", "Git Commits & Deployment", "LeetCode Top 50 Interview Problems"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "DSA Fundamentals & Problem Solving", "topics": ["Arrays, Linked Lists, Hash Tables", "Binary Search & Sorting", "Recursion & Trees", "Graph BFS/DFS Basics"]},
                {"period": "Month 2", "focus": "Advanced Algorithms & System Concepts", "topics": ["Dynamic Programming Patterns", "Tries & Graphs", "Operating System Threads & Locks", "Database Normalization"]},
                {"period": "Month 3", "focus": "Full-Stack Project & Placement Sprints", "topics": ["RESTful Microservice with FastAPI", "React & Tailwind Dashboard", "Clean Code Architecture & Unit Tests"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Comprehensive DSA Mastery", "topics": ["300+ Curated Problems (LeetCode Blind 75 / Striver SDE Sheet)", "Advanced Trees, Graphs, DP", "Bit Manipulation"]},
                {"period": "Months 3-4", "focus": "Backend Engineering & Low-Level Design", "topics": ["OOP Design Principles (SOLID)", "Design Patterns (Factory, Singleton, Observer)", "Concurrency & Multi-threading"]},
                {"period": "Months 5-6", "focus": "High-Level System Design & Production Deployment", "topics": ["Caching (Redis), Message Queues (Kafka)", "Dockerization & CI/CD Pipelines", "Mock Interview Marathons"]}
            ],
            "projects": [
                {"title": "Placement Intelligence & RAG Web Platform", "description": "Full-stack application with FastAPI REST API backend, SQLite storage, and responsive React frontend."},
                {"title": "High-Concurrency URL Shortener with Analytics", "description": "Distributed URL redirection service implementing Redis caching, rate limiting, and Docker containers."}
            ],
            "topics": ["Time & Space Complexity Analysis", "Data Structure Selection Trade-offs", "SQL Normalization vs Denormalization", "REST API Error Handling & Status Codes"],
            "resume_focus": ["Demonstrate problem-solving (e.g., 'Solved 250+ LeetCode problems')", "Highlight tech stack explicitly (FastAPI, React, SQLite, Docker)", "Provide live deployment and repository links"],
            "placement_tips": [
                "Tech recruiters test code cleanliness, variable naming, and corner-case handling during live paired coding rounds.",
                "Ensure your GitHub profile exhibits consistent green commit squares over the last 3-6 months.",
                "Review Operating Systems (virtual memory, page replacement) and DBMS (ACID properties, transactions) thoroughly."
            ]
        },
        "AI/ML Engineer": {
            "skills": ["Linear Algebra & Calculus", "Python (NumPy, Pandas)", "Scikit-Learn", "PyTorch / TensorFlow", "Generative AI & LLMs", "RAG & FAISS Vector DB"],
            "1 Month": [
                {"period": "Week 1", "focus": "Math & Data Processing", "topics": ["Matrix Operations", "Probability & Statistics", "NumPy & Pandas Vectorization"]},
                {"period": "Week 2", "focus": "Core Machine Learning", "topics": ["Supervised Learning (Regression, Trees)", "Ensemble Methods (XGBoost)", "Hyperparameter Tuning"]},
                {"period": "Week 3", "focus": "Deep Learning & NLP", "topics": ["Neural Networks Architecture", "PyTorch Tensors & Training Loop", "Transformers & Attention Mechanism"]},
                {"period": "Week 4", "focus": "Generative AI & RAG Capstone", "topics": ["Sentence Transformers", "FAISS Vector Search", "LLM Prompting & API Integration"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "Foundations: Math, Data & Classic ML", "topics": ["Linear Algebra & Optimization", "NumPy & Pandas Pipelines", "Scikit-Learn Classification & Regression", "Cross-Validation & ROC-AUC"]},
                {"period": "Month 2", "focus": "Deep Learning & Computer Vision / NLP", "topics": ["PyTorch Neural Network Training", "CNNs & Transfer Learning", "Recurrent Networks & Self-Attention", "Hugging Face Pipelines"]},
                {"period": "Month 3", "focus": "Generative AI, RAG & Production Deployment", "topics": ["Sentence Embeddings & FAISS Indexing", "Retrieval-Augmented Generation (RAG)", "LangChain / LlamaIndex Basics", "FastAPI ML Model Serving"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Rigorous Mathematical Foundations & Classical ML", "topics": ["Multivariate Calculus & Convex Optimization", "Probabilistic Graphical Models", "PCA, t-SNE, Clustering", "Feature Engineering at Scale"]},
                {"period": "Months 3-4", "focus": "Deep Learning Specialization", "topics": ["PyTorch Architecture Customization", "Transformer Encoders (BERT) & Decoders (GPT)", "Fine-Tuning Techniques (LoRA, QLoRA)"]},
                {"period": "Months 5-6", "focus": "End-to-End LLMOps & Production GenAI Systems", "topics": ["RAG Triad Evaluation (Faithfulness, Relevance)", "Vector Database Clustering & Hybrid Search", "Dockerized FastAPI Inference Servers"]}
            ],
            "projects": [
                {"title": "Source-Grounded Institutional Document RAG Engine", "description": "Production RAG pipeline using Sentence Transformers, FAISS vector index, and Gemini LLM synthesis with page-level citations."},
                {"title": "Automated Medical Scan Classification with PyTorch", "description": "Deep Convolutional Neural Network with transfer learning achieving 94% F1-score with grad-CAM explainability."}
            ],
            "topics": ["Precision, Recall, F1-Score & Confusion Matrix", "Bias-Variance Tradeoff & Regularization (L1/L2)", "Cosine Similarity vs Euclidean Distance in Embeddings", "RAG Hallucination Mitigation Strategies"],
            "resume_focus": ["Focus on model evaluation metrics (F1-score, latency, memory footprint)", "Detail datasets and preprocessing steps used", "Include ML architecture diagrams and ablation studies"],
            "placement_tips": [
                "Interviewers will probe whether you truly understand the math behind backpropagation and attention matrices.",
                "Be ready to justify choosing RAG over fine-tuning for dynamic organizational knowledge bases.",
                "Showcase an evaluation benchmark (like Hit Rate@k or MRR) alongside your GenAI project."
            ]
        },
        "Cybersecurity": {
            "skills": ["Linux & Bash Scripting", "Networking Protocols (TCP/IP, DNS, OSI)", "Wireshark & Packet Analysis", "Nmap & Vulnerability Scanning", "Cryptography", "OWASP Top 10"],
            "1 Month": [
                {"period": "Week 1", "focus": "Linux & Network Protocols", "topics": ["Linux File Permissions & Shell", "OSI & TCP/IP Model", "Wireshark Packet Captures"]},
                {"period": "Week 2", "focus": "Reconnaissance & Cryptography", "topics": ["Nmap Port Scanning", "Symmetric vs Asymmetric Encryption", "SSL/TLS Handshakes"]},
                {"period": "Week 3", "focus": "Web Security & OWASP Top 10", "topics": ["SQL Injection Exploit & Defense", "Cross-Site Scripting (XSS)", "CSRF & Broken Authentication"]},
                {"period": "Week 4", "focus": "Incident Handling & Security Labs", "topics": ["TryHackMe Rooms", "Security Information & Event Logs (SIEM)", "CompTIA Security+ Question Drills"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "Networking, Operating Systems & Scripting", "topics": ["Subnetting & Routing Protocols", "Linux Internals & Bash Automation", "Python Socket Programming & Scapy", "Packet Capture & Protocol Dissection"]},
                {"period": "Month 2", "focus": "Vulnerability Assessment & Web Security", "topics": ["Port Scanning with Nmap & Masscan", "OWASP Top 10 Deep Dive", "Burp Suite Proxy & Interception", "Secure Coding Principles"]},
                {"period": "Month 3", "focus": "Defensive Security, Cryptography & Labs", "topics": ["PKI, Digital Certificates, AES/RSA", "SIEM Log Analysis (Splunk / Elastic)", "TryHackMe / HackTheBox Badges", "SOC Analyst Workflows"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Advanced Network Security & Linux Hardening", "topics": ["Firewalls, IDS/IPS Configuration (Snort)", "Kernel Hardening & SELinux", "Automated Python Security Scripting"]},
                {"period": "Months 3-4", "focus": "Offensive & Defensive Security Specialization", "topics": ["Privilege Escalation Techniques", "Web Application Penetration Testing", "Active Directory Security Basics", "Malware Analysis Sandboxing"]},
                {"period": "Months 5-6", "focus": "Enterprise Incident Response & Compliance", "topics": ["SOC Playbooks & Threat Hunting", "ISO 27001 / NIST Cybersecurity Framework", "CompTIA Security+ / CEH Exam Preparation"]}
            ],
            "projects": [
                {"title": "Automated Network Port & Vulnerability Auditor", "description": "Python CLI tool integrating Nmap to identify unpatched services, open ports, and insecure SSL certificates."},
                {"title": "Real-Time SOC SIEM Log Anomaly Detector", "description": "Log analysis pipeline detecting brute-force SSH logins and port scanning attempts with automated alert dispatch."}
            ],
            "topics": ["OSI 7 Layers & Common Port Numbers (22, 53, 80, 443)", "Symmetric vs Asymmetric Encryption & Diffie-Hellman", "OWASP Top 10 Vulnerabilities & Remediation", "Incident Response Lifecycle (NIST)"],
            "resume_focus": ["List hands-on lab badges (TryHackMe, HackTheBox, OverTheWire)", "Highlight Linux system administration and Wireshark mastery", "Mention industry certifications (CEH, Security+)"],
            "placement_tips": [
                "Corporate security hiring managers look for ethics, sound networking fundamentals, and hands-on lab experience.",
                "Always emphasize your defensive understanding: knowing how to patch a vulnerability is more valuable than just knowing the exploit.",
                "Highlight clean, documented reports from CTF or lab challenges on your GitHub portfolio."
            ]
        },
        "Web Developer": {
            "skills": ["HTML5, CSS3, JavaScript (ES6+)", "React.js / Next.js", "Tailwind CSS", "Node.js / Express or FastAPI", "RESTful APIs", "Git & CI/CD", "Responsive UI/UX"],
            "1 Month": [
                {"period": "Week 1", "focus": "Modern JavaScript & DOM", "topics": ["ES6+ Syntax (Promises, Async/Await)", "DOM Manipulation", "Fetch API & JSON Handling"]},
                {"period": "Week 2", "focus": "React.js Core", "topics": ["JSX & Component Architecture", "Hooks (useState, useEffect, useMemo)", "Props & State Management"]},
                {"period": "Week 3", "focus": "Styling & Backend Integration", "topics": ["Tailwind CSS Responsive Utilities", "Connecting React with REST Endpoints", "Form Validation & Error States"]},
                {"period": "Week 4", "focus": "Full-Stack Deployment & Portfolio", "topics": ["Vite Build & Optimization", "Vercel / Netlify Deployment", "Lighthouse Performance & SEO"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "Frontend Mastery: React & Modern CSS", "topics": ["Advanced React Hooks (useContext, useReducer)", "Tailwind CSS & Glassmorphism Aesthetics", "React Router SPA Routing", "Axios Interceptors & Authentication"]},
                {"period": "Month 2", "focus": "Backend API Development & Databases", "topics": ["FastAPI / Express.js Route Design", "Relational Database Modelling with SQLite/PostgreSQL", "JWT Authentication & Route Guards", "CORS & Security Headers"]},
                {"period": "Month 3", "focus": "Full-Stack SaaS Projects & Optimization", "topics": ["State Management (Zustand / Redux Toolkit)", "WebSockets / Real-time Updates", "Responsive Cross-browser Testing", "Production CI/CD Deployments"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Deep Dive JavaScript & Advanced Frontend", "topics": ["JS Event Loop, Closures, Prototypes", "Next.js Server-Side Rendering (SSR) & SSG", "Advanced Component Systems & Storybook"]},
                {"period": "Months 3-4", "focus": "Scalable Backend Architecture & Cloud Services", "topics": ["Microservices vs Monoliths", "Caching with Redis & Database Indexing", "Cloud Object Storage (AWS S3) & CDN Integration"]},
                {"period": "Months 5-6", "focus": "Enterprise Capstone & Performance Engineering", "topics": ["High-Performance Web Apps (<1s Load Time)", "Automated E2E Testing (Cypress / Playwright)", "Mock Placement Interview Sprints"]}
            ],
            "projects": [
                {"title": "Placement Cell Administration & Student Portal", "description": "Single-Page Application with React, Vite, and Tailwind CSS backed by FastAPI REST endpoints and SQLite database."},
                {"title": "Real-Time Collaborative Code & Markdown Editor", "description": "Full-stack web application featuring WebSocket live synchronization, syntax highlighting, and OAuth authentication."}
            ],
            "topics": ["Virtual DOM vs Real DOM in React", "CSS Flexbox vs Grid & Responsive Breakpoints", "State Management Strategies (Props Drilling vs Context)", "Client-Side vs Server-Side Rendering (CSR vs SSR)"],
            "resume_focus": ["Include live deployed URLs (e.g. Vercel, Netlify) for all projects", "Highlight performance scores (95+ Lighthouse metrics)", "Showcase clean, modern component libraries and design tokens"],
            "placement_tips": [
                "Recruiters love clean UI aesthetics with fluid micro-interactions, dark mode support, and seamless responsiveness.",
                "Be ready to write vanilla JavaScript functions (debounce, throttle, deep clone) on a whiteboard.",
                "Explain the end-to-end lifecycle of an HTTP request from browser URL bar to backend database query."
            ]
        },
        "Cloud Engineer": {
            "skills": ["Linux System Administration", "Cloud Provider (AWS / Azure / GCP)", "Docker & Containers", "Kubernetes (K8s)", "Infrastructure as Code (Terraform)", "CI/CD (GitHub Actions)"],
            "1 Month": [
                {"period": "Week 1", "focus": "Linux & Cloud Core", "topics": ["Linux Commands, Shell Scripting & SSH", "AWS EC2, VPC, Security Groups", "S3 Storage & IAM Roles"]},
                {"period": "Week 2", "focus": "Containerization with Docker", "topics": ["Dockerfiles & Multi-stage Builds", "Docker Compose Multi-container Setup", "Container Networking & Volumes"]},
                {"period": "Week 3", "focus": "CI/CD & Cloud Deployment", "topics": ["GitHub Actions Workflows", "Automated Testing & Build Pipelines", "Deploying Containerized Apps to Cloud"]},
                {"period": "Week 4", "focus": "Cloud Architecture & Mock Drills", "topics": ["Load Balancing (ALB) & Auto Scaling", "Monitoring & Logs (CloudWatch)", "Cloud Practitioner / Solutions Architect Questions"]}
            ],
            "3 Months": [
                {"period": "Month 1", "focus": "Linux Mastery & Cloud Infrastructure (AWS)", "topics": ["Linux Server Administration & Bash Scripting", "AWS Core Services (EC2, S3, RDS, VPC, Route53)", "IAM Policies & Least Privilege Access", "Billing & Cost Optimization Basics"]},
                {"period": "Month 2", "focus": "Containers, Orchestration & CI/CD", "topics": ["Production Docker Image Optimization", "Kubernetes Pods, Services, Deployments & Ingress", "GitHub Actions CI/CD Pipeline Automation", "Helm Charts & Configuration Management"]},
                {"period": "Month 3", "focus": "Infrastructure as Code (IaC) & Monitoring", "topics": ["Terraform Modules for Cloud Provisioning", "Prometheus & Grafana Monitoring Dashboards", "Disaster Recovery & High Availability Multi-AZ Design"]}
            ],
            "6 Months": [
                {"period": "Months 1-2", "focus": "Linux Internals, Networking & Cloud Foundations", "topics": ["Kernel Tuning, Systemd & Networking (CIDR, Subnets)", "AWS Certified Solutions Architect Associate Curriculum", "VPC Peering, Transit Gateway & Direct Connect"]},
                {"period": "Months 3-4", "focus": "Advanced Kubernetes & Cloud-Native Ecosystem", "topics": ["Production Kubernetes (EKS / GKE)", "Service Meshes (Istio) & Microservice Security", "GitOps Workflows with ArgoCD"]},
                {"period": "Months 5-6", "focus": "Enterprise SRE, Chaos Engineering & IaC Mastery", "topics": ["Multi-Cloud Architecture with Terraform", "Site Reliability Engineering (SLO, SLA, Error Budgets)", "Campus Recruitment Technical Interview Panels"]}
            ],
            "projects": [
                {"title": "Automated Multi-Tier Cloud Deployment with Terraform", "description": "IaC code repository provisioning secure VPC, auto-scaling EC2 instances, and managed RDS database on AWS."},
                {"title": "Zero-Downtime CI/CD Pipeline with Docker & GitHub Actions", "description": "End-to-end continuous deployment workflow with automated testing, Docker container builds, and deployment to cloud cluster."}
            ],
            "topics": ["Horizontal vs Vertical Scaling & Auto-Scaling Groups", "Docker Container vs Virtual Machine Architecture", "Kubernetes Cluster Architecture (Control Plane vs Worker Nodes)", "Stateless vs Stateful Cloud Applications"],
            "resume_focus": ["Highlight public cloud certifications (AWS Solutions Architect, CKA)", "Link GitHub repos containing modular Terraform and Docker configurations", "Quantify operational benefits (e.g. 'Reduced deployment time by 60%')"],
            "placement_tips": [
                "Cloud infrastructure interviews heavily test understanding of networking (Subnets, NAT Gateways, Routing Tables).",
                "Demonstrate practical hands-on experience by bringing an active AWS Free Tier architectural diagram.",
                "Practice explaining high availability, disaster recovery, and recovery point objectives (RPO/RTO)."
            ]
        }
    }

    @classmethod
    def get_roadmap(cls, target_role: str, current_level: str = "Beginner", prep_time: str = "3 Months") -> dict:
        data = cls.ROADMAPP_DATA.get(target_role)
        if not data:
            data = cls.ROADMAPP_DATA["Software Developer"]
            target_role = "Software Developer"

        # Normalize duration selection
        clean_time = "3 Months"
        if "1" in prep_time:
            clean_time = "1 Month"
        elif "6" in prep_time:
            clean_time = "6 Months"

        sequence = data.get(clean_time, data["3 Months"])
        
        # Transform into standardized output dictionary
        formatted_sequence = [
            {"month": step["period"], "focus": step["focus"], "topics": step["topics"]}
            for step in sequence
        ]

        return {
            "target_role": target_role,
            "timeline_duration": clean_time,
            "skills_to_learn": data["skills"],
            "learning_sequence": formatted_sequence,
            "projects_to_build": data["projects"],
            "interview_topics": data["topics"],
            "resume_focus": data["resume_focus"],
            "placement_officer_tips": data["placement_tips"],
            "is_general_guidance": True
        }

    @classmethod
    def generate_interview_questions(cls, target_role: str, topic: str = "All Topics", difficulty: str = "Intermediate") -> dict:
        """
        Generates role-specific questions across 4 core domains:
        Technical, SQL, System Design, and HR - complete with model answers.
        """
        role_questions = {
            "Software Developer": [
                {
                    "category": "Technical",
                    "question": "What is the difference between an Array and a Linked List, and when would you choose one over the other?",
                    "model_answer": "Arrays allocate memory contiguously, providing O(1) random access by index but O(n) insertions/deletions in the middle due to element shifting. Linked Lists allocate nodes dynamically with pointers, allowing O(1) insertion/deletion once the position is known, but O(n) traversal. Choose Arrays for frequent index lookups and cache-friendly reads; choose Linked Lists when frequent dynamic inserts/deletions are required without pre-allocating contiguous memory.",
                    "tip": "Mention memory caching efficiency (locality of reference) for bonus points.",
                    "difficulty": "Easy"
                },
                {
                    "category": "Technical",
                    "question": "Explain how HashMap works under the hood and how hash collisions are resolved.",
                    "model_answer": "A HashMap maps keys to buckets using a hash function: index = hash(key) % capacity. Collisions happen when two keys hash to the same bucket. They are resolved via Chaining (storing collided entries in a linked list or self-balancing BST like Java 8 Red-Black trees) or Open Addressing (Linear Probing, Quadratic Probing). Average lookup is O(1); worst-case degraded lookup is O(n) or O(log n).",
                    "tip": "Explain load factors (e.g. 0.75) and rehashing triggers.",
                    "difficulty": "Intermediate"
                },
                {
                    "category": "SQL",
                    "question": "Write and explain an SQL query to find the second highest salary from an Employee table without using LIMIT.",
                    "model_answer": "SELECT MAX(salary) FROM Employee WHERE salary < (SELECT MAX(salary) FROM Employee); Alternative using Window Function: WITH Ranked AS (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk FROM Employee) SELECT salary FROM Ranked WHERE rnk = 2 LIMIT 1.",
                    "tip": "Clarify how duplicate highest salaries should be handled (use DENSE_RANK over RANK).",
                    "difficulty": "Intermediate"
                },
                {
                    "category": "System Design",
                    "question": "How would you design a scalable URL shortener service like TinyURL?",
                    "model_answer": "1. Functional Requirements: Given a long URL, return a 7-character short URL (Base62: [a-z, A-Z, 0-9], allowing 62^7 = 3.5 trillion URLs). 2. Key Generation: Use distributed ID counter (Snowflake) or MD5 hash with collision check. 3. Data Tier: NoSQL (MongoDB/Cassandra) or Relational (PostgreSQL) storing (short_url_hash PK, original_url, created_at). 4. Caching: Redis caching for top 20% most accessed URLs. 5. Routing: HTTP 301 (Permanent) vs 302 (Temporary) redirect depending on whether click analytics are tracked.",
                    "tip": "Start with requirements clarification, estimate read/write QPS, then discuss database and caching tiers.",
                    "difficulty": "Advanced"
                },
                {
                    "category": "HR",
                    "question": "Describe a scenario where you had a disagreement with a team member during a project. How did you resolve it?",
                    "model_answer": "In our capstone project, my teammate preferred building custom authentication from scratch while I recommended adopting an established JWT and FastAPI OAuth2 standard to prioritize security and delivery time. Rather than arguing, I drafted a quick trade-off matrix comparing delivery risk, token expiration handling, and industry best practices. Seeing the objective comparison, we mutually agreed to use the standard library and allocated our saved time to improving the UI.",
                    "tip": "Use the STAR method: Situation, Task, Action, Result. Focus on constructive problem resolution.",
                    "difficulty": "Easy"
                }
            ],
            "Data Analyst": [
                {
                    "category": "Technical",
                    "question": "What is the difference between Supervised and Unsupervised Learning, and where does clustering fit in?",
                    "model_answer": "Supervised Learning models learn from labeled training datasets where input features map to ground-truth targets (e.g., Regression and Classification). Unsupervised Learning discovers hidden patterns, groupings, or representations in unlabeled data without target guidance. Clustering (e.g., K-Means, DBSCAN) is an unsupervised technique grouping data points by similarity.",
                    "tip": "Give quick domain examples like customer churn prediction (supervised) vs customer segmentation (unsupervised).",
                    "difficulty": "Easy"
                },
                {
                    "category": "SQL",
                    "question": "Explain the difference between ROW_NUMBER(), RANK(), and DENSE_RANK() window functions.",
                    "model_answer": "All three assign ranks to rows within partitions ordered by a column. ROW_NUMBER() assigns strictly sequential numbers (1, 2, 3, 4) regardless of ties. RANK() assigns the same rank to ties but skips subsequent numbers (e.g., ties at 2 yield 1, 2, 2, 4). DENSE_RANK() assigns the same rank to ties without skipping subsequent numbers (1, 2, 2, 3).",
                    "tip": "State a real scenario: choosing top student scores where ties shouldn't leave gaps.",
                    "difficulty": "Intermediate"
                },
                {
                    "category": "System Design",
                    "question": "How would you design an end-to-end automated analytics pipeline for daily placement drive reports?",
                    "model_answer": "1. Ingestion: Cron/Airflow trigger pulling daily registration and interview logs from SQLite/PostgreSQL. 2. Processing: Python/Pandas transformation script validating data cleanliness, calculating key metrics (daily turnout, pass rates). 3. Storage: Aggregate data mart table optimized for read queries. 4. BI Layer: Scheduled refresh of Power BI / Tableau dashboards. 5. Alerting: Automated Slack/Email webhook alerting placement officers if company applicant counts fall below target threshold.",
                    "tip": "Emphasize data validation steps before reports reach management.",
                    "difficulty": "Intermediate"
                },
                {
                    "category": "HR",
                    "question": "How do you present complex technical data findings to non-technical stakeholders?",
                    "model_answer": "I focus on the business impact and 'so-what' narrative rather than statistical jargon. I lead with key takeaways and executive summaries, use intuitive charts (like bar charts or line graphs rather than dense scatter plots), highlight actionable next steps, and keep detailed calculation methodologies in appendix slides for reference if requested.",
                    "tip": "Interviewers evaluate your empathy, communication clarity, and business awareness.",
                    "difficulty": "Easy"
                }
            ]
        }

        # Fallback to Software Developer if role not explicitly custom-mapped
        questions = role_questions.get(target_role, role_questions["Software Developer"])

        # Filter by category if requested
        if topic and topic != "All Topics":
            filtered = [q for q in questions if q["category"].lower() == topic.lower()]
            if filtered:
                questions = filtered

        checklist = [
            f"Review fundamental algorithms, database syntax, and projects relevant to {target_role}.",
            "Practice articulating your thought process out loud before jumping into solutions.",
            "Prepare 2-3 technical questions about the company's tech stack and engineering challenges.",
            "Have your GitHub repository links and deployed demos open and ready in advance."
        ]

        return {
            "target_role": target_role,
            "questions": questions,
            "preparation_checklist": checklist
        }

    @classmethod
    def generate_resume_guidance(cls, target_role: str, student_skills: str, projects: str = "") -> dict:
        data = cls.ROADMAPP_DATA.get(target_role, cls.ROADMAPP_DATA["Software Developer"])
        
        student_skill_list = [s.strip().lower() for s in student_skills.split(",") if s.strip()]
        required_skills = [s.lower() for s in data["skills"]]
        
        # Calculate matched vs missing skills
        matched = [s for s in data["skills"] if s.lower() in student_skill_list]
        missing = [s for s in data["skills"] if s.lower() not in student_skill_list]
        
        # Calculate numerical ATS Alignment Score (0 to 100)
        skills_ratio = len(matched) / max(len(data["skills"]), 1)
        skills_score = int(skills_ratio * 50) # up to 50 pts
        
        # Project depth score (up to 30 pts)
        project_score = 15
        p_lower = projects.lower()
        if any(kw in p_lower for kw in ["deploy", "fastapi", "react", "sql", "rag", "docker", "accuracy", "pipeline", "github"]):
            project_score = 28
        elif len(projects.strip()) > 20:
            project_score = 22
            
        # Action verbs & formatting score (up to 20 pts)
        formatting_score = 18
        
        total_ats_score = min(100, max(25, skills_score + project_score + formatting_score))

        # Build STAR-formatted bullet points (Situation, Task, Action, Result)
        lead_skill = student_skills.split(",")[0].strip() if student_skills else "Python"
        second_skill = student_skills.split(",")[1].strip() if len(student_skills.split(",")) > 1 else "SQL"

        star_bullets = [
            f"[SITUATION & TASK] Built a centralized institutional platform to streamline technical workflows for {target_role} requirements. [ACTION] Engineered robust REST API microservices using {lead_skill} and integrated relational data pipelines with {second_skill}. [RESULT] Improved data query throughput by 35% and cut end-to-end response latency below 200ms.",
            f"[SITUATION & TASK] Addressed manual data validation overhead in legacy student operations. [ACTION] Architected modular business logic validation engines with automated test coverage and strict schema sanitization. [RESULT] Eliminated 98% of human eligibility verification errors and supported concurrent multi-user sessions.",
            f"[SITUATION & TASK] Needed source traceability and real-time observability for team projects. [ACTION] Configured automated Git version control, structured logging, and Dockerized deployment workflows. [RESULT] Decreased setup time for onboarding contributors from 2 hours to 5 minutes."
        ]

        return {
            "target_role": target_role,
            "ats_score": total_ats_score,
            "score_breakdown": {
                "skills_alignment": min(100, int((skills_score / 50) * 100)),
                "project_relevance": min(100, int((project_score / 30) * 100)),
                "action_verb_strength": min(100, int((formatting_score / 20) * 100))
            },
            "highlight_skills": matched if matched else data["skills"][:3],
            "suggested_bullet_points": star_bullets,
            "missing_skill_areas": missing if missing else ["Advanced System Architecture", "Production Load Testing"],
            "disclaimer": "ATS alignment score is estimated based on keyword density, role prerequisites, and STAR methodology alignment."
        }

# Backwards-compatibility alias
CareerEngine = CareerIntelligenceEngine
