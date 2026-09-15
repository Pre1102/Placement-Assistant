# CareerCampusAI — Placement Intelligence & Career Guidance System

> **Semester VII Multidisciplinary Generative AI Capstone Project**  
> *A source-grounded, explainable placement intelligence engine and career companion for college students and placement cells.*

---

## 🌟 Overview & Product Identity

**CareerCampusAI** is designed to solve the critical information gap faced by college students during campus placement seasons. Instead of behaving like a generic PDF chatbot, CareerCampusAI delivers **structured placement intelligence, data-driven eligibility verification, and personalized career roadmaps**.

Every response is strictly grounded in official institutional notices, placement policy documents, and company eligibility criteria—complete with explicit document name and page-number citations to eliminate AI hallucinations.

---

## ✨ Key Features

### 🎓 Student Placement Workspace
1. **Source-Grounded AI Assistant (`/ai-assistant`)**:
   - Natural language query interface with automatic intent classification (*PLACEMENT_ELIGIBILITY*, *COMPANY_REQUIREMENTS*, *PLACEMENT_PROCEDURE*, *INTERNSHIP*, *CAREER_GUIDANCE*, *INTERVIEW_PREPARATION*, *RESUME_GUIDANCE*).
   - Grounded context synthesis with explicit document & page citations.
   - Safe fallback for unknown institutional queries not documented in the knowledge base.

2. **Data-Driven Eligibility Analyzer (`/placement`)**:
   - Evaluates student profile metrics (**CGPA, Academic Branch, Active Backlogs**) against target company criteria.
   - Displays pass/fail breakdown matrix with exact requirements vs student profile values.

3. **Company Drives Directory & Side-by-Side Comparison Matrix (`/companies`)**:
   - View active campus recruiters (CTC, Min CGPA, Max Backlogs, Eligible Branches, Selection Rounds).
   - Select up to 4 companies for a side-by-side comparison matrix with real-time student eligibility status.

4. **Career Guidance & Step-by-Step Roadmaps (`/career`)**:
   - Customized learning timelines (1, 3, or 6 months) for target technical roles (*Data Analyst, Software Developer, AI/ML Engineer, Cybersecurity, Web Developer, Cloud Engineer*).
   - Recommended portfolio projects and placement officer pro-tips.

5. **AI Interview Question Generator (`/interview-prep`)**:
   - Technical, SQL, System Design, and HR interview questions with model answer solutions.

6. **Resume & ATS Alignment Analyzer (`/resume-guidance`)**:
   - Role alignment scoring, missing skill recommendations, and STAR-formatted bullet point suggestions.

7. **Editable Student Profile (`/profile`)**:
   - Update CGPA, Branch, Backlogs, Skills, and Preferred Role.

---

### 🛡️ Placement Cell Admin Workspace
1. **Admin Dashboard (`/admin`)**: Overview of indexed PDF documents, text chunks, and FAISS vector count.
2. **Document Management (`/admin/documents`)**: Upload new PDF policy notices, assign category tags and company metadata, re-process, or delete documents.
3. **Knowledge Base Health (`/admin/knowledge-base`)**: Monitor vector store health and trigger full FAISS index rebuilds.
4. **FAISS Vector Retrieval Inspector (`/admin/retrieval-test`)**: Interactive tool for viva evaluation to test vector similarity scores, page numbers, and exact text chunks.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+) |
| **Database** | SQLite + [SQLAlchemy ORM](https://www.sqlalchemy.org/) |
| **Vector Indexing** | [FAISS](https://github.com/facebookresearch/faiss) (`IndexFlatIP` cosine similarity) |
| **Embeddings** | [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`, 384 dimensions) |
| **PDF Extraction & Chunking** | PyMuPDF (`fitz`) + Metadata-aware sliding window chunker |
| **LLM Provider** | Google Gemini API (`gemini-1.5-flash`) with Grounded Fallback Synthesizer |
| **Frontend Framework** | React 18 + [Vite](https://vitejs.dev/) |
| **Styling & UI** | Tailwind CSS (Emerald Green Theme, strictly non-blue) + [Lucide Icons](https://lucide.dev/) |
| **Routing & HTTP** | React Router DOM v6 + Axios |

---

## 📁 Repository Directory Structure

```
c:\Projects\Gen Ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # REST API Endpoints (chat, profile, placement, companies, career, etc.)
│   │   ├── core/                # Database engine & base configuration
│   │   ├── models/              # SQLAlchemy DB models & Pydantic schemas
│   │   ├── services/            # RAG Engine, Retriever, Vector Store, Embeddings, Placement Engine, LLM
│   │   ├── config.py            # Environment settings
│   │   └── main.py              # FastAPI main entrypoint & CORS configuration
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components (Navbar, Sidebar, Card, Badge, EligibilityCard, etc.)
│   │   ├── pages/               # Student & Admin page views
│   │   ├── services/            # Axios API client
│   │   ├── App.jsx              # Main React Router shell
│   │   ├── index.css            # Tailwind CSS directives
│   │   └── main.jsx             # React DOM root
│   ├── package.json
│   ├── tailwind.config.js       # Emerald green palette configuration
│   └── vite.config.js
├── data/
│   └── demo/                    # Synthetic institutional PDF policy notices
├── scripts/
│   ├── generate_demo_pdfs.py    # Synthetic PDF generator script
│   ├── ingest_documents.py      # Automated PDF ingestion pipeline
│   └── evaluate.py              # 35-question benchmark evaluation suite
├── vectorstore/                 # FAISS index storage directory
├── careercampus.db              # SQLite Database
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start & Installation Guide (Windows)

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm

### 1. Clone Repository & Setup Virtual Environment
```powershell
git clone https://github.com/Pre1102/Placement-Assistant.git
cd Placement-Assistant

# Create & activate Python virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install Python backend dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic PDF Knowledge Base & Ingest Data
```powershell
# Step 1: Generate 13 demo PDF notices
python scripts/generate_demo_pdfs.py

# Step 2: Ingest PDFs into SQLite and FAISS vector index
python scripts/ingest_documents.py

# Step 3: (Optional) Run 35-question benchmark evaluation suite
python scripts/evaluate.py
```

### 3. Install Frontend Dependencies
```powershell
cd frontend
npm install
cd ..
```

---

## 💻 Running the Servers

### Start FastAPI Backend (Port 8000)
```powershell
# Run from repository root
cmd /c "set PYTHONPATH=c:\Projects\Gen Ai\backend&& .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
```
*Backend API Health Check*: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### Start Vite React Frontend (Port 5173)
```powershell
cd frontend
npm run dev
```
*Application UI*: [http://localhost:5173](http://localhost:5173)

---

## 📊 Evaluation & Viva Defense Q&A

### 1. How is hallucination prevented in CareerCampusAI?
CareerCampusAI employs a **Hybrid RAG architecture**. User queries are vectorized using `all-MiniLM-L6-v2` and matched against top-K text chunks in FAISS using Cosine Similarity (`IndexFlatIP`). The LLM prompt is strictly constrained to synthesize answers *only* using the retrieved context block. If top retrieval similarity scores fall below the minimum threshold (0.20), an **Unknown Query** flag is raised, advising the student to consult the placement cell directly.

### 2. How does the Placement Eligibility Engine work?
Unlike traditional text generation, eligibility evaluation is **data-driven**. The `PlacementEligibilityEngine` parses requirements (min CGPA, max backlogs, eligible branches) from company notices, compares them deterministically against the student's active SQLite profile, and generates a pass/fail matrix with explicit reasons.

---

## 📄 License
This capstone project is developed for academic evaluation purposes under the Semester VII Multidisciplinary Generative AI curriculum.
