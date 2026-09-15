import os
import sys
import time

# Ensure backend app path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.config import settings
from app.core.database import SessionLocal, Base, engine
from app.services.vector_store import VectorStoreManager
from app.services.retriever import HybridRetriever
from app.services.rag_engine import RAGEngine

EVALUATION_QUESTIONS = [
    # 1. Eligibility Questions
    {"query": "What is the minimum CGPA required for Demo Company A?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "Can I apply for Demo Company B with 1 active backlog?", "expected_category": "PLACEMENT_ELIGIBILITY", "should_find_source": True},
    {"query": "Can a student with 2 active backlogs apply for Demo Company C?", "expected_category": "PLACEMENT_ELIGIBILITY", "should_find_source": True},
    {"query": "Which branches are eligible for Demo Company B?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "What is the active backlog policy for Demo Company D?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "Am I eligible for campus placement if my CGPA is 5.5?", "expected_category": "PLACEMENT_ELIGIBILITY", "should_find_source": True},
    {"query": "Can I apply for Tier 1 companies with 3 backlogs?", "expected_category": "PLACEMENT_ELIGIBILITY", "should_find_source": True},
    
    # 2. Company Notices & Packages
    {"query": "What is the offered CTC for Demo Company A?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "What is the salary package for Demo Company C?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "What are the job roles offered by Demo Company B?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "What is the selection procedure for Demo Company A?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},
    {"query": "What is the offered package for Demo Company D?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": True},

    # 3. Placement Procedures & Registration
    {"query": "What documents are required for placement registration?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    {"query": "When does placement registration open and close?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    {"query": "What is the One Student One Job policy?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    {"query": "What is the Dream Option for placed students?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    {"query": "What happens if I miss an interview after being shortlisted?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    {"query": "What are the standard stages of campus recruitment?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": True},
    
    # 4. Internship Guidelines
    {"query": "What are the guidelines for Semester VIII full time internship?", "expected_category": "INTERNSHIP", "should_find_source": True},
    {"query": "What is the minimum recommended monthly stipend for technical internship?", "expected_category": "INTERNSHIP", "should_find_source": True},
    {"query": "What should a student do if offered a PPO during internship?", "expected_category": "INTERNSHIP", "should_find_source": True},
    {"query": "Who countersigns the monthly progress reports for interns?", "expected_category": "INTERNSHIP", "should_find_source": True},

    # 5. Career Guidance & Roadmaps
    {"query": "How should I prepare for a Data Analyst role?", "expected_category": "CAREER_GUIDANCE", "should_find_source": True},
    {"query": "What skills are needed for a Software Developer position?", "expected_category": "CAREER_GUIDANCE", "should_find_source": True},
    {"query": "What is the learning roadmap for AI/ML Engineer?", "expected_category": "CAREER_GUIDANCE", "should_find_source": True},
    {"query": "What are the key learning phases for a Cybersecurity Analyst?", "expected_category": "CAREER_GUIDANCE", "should_find_source": True},

    # 6. Unknown Query Handling (Mandatory Safety Checks)
    {"query": "What is the package for Demo Company Z?", "expected_category": "COMPANY_REQUIREMENTS", "should_find_source": False},
    {"query": "Does Demo Company X allow 4 active backlogs?", "expected_category": "PLACEMENT_ELIGIBILITY", "should_find_source": False},
    {"query": "What is the campus dress code for Sunday lectures?", "expected_category": "GENERAL", "should_find_source": False},
    {"query": "What is the placement policy for 2035 batch?", "expected_category": "PLACEMENT_PROCEDURE", "should_find_source": False},
    {"query": "Can I get a stipend of 5 Lakhs per month in Company Y?", "expected_category": "INTERNSHIP", "should_find_source": False}
]

def run_evaluation():
    print("=" * 70)
    print("CareerCampusAI — Automated RAG & Intelligence Evaluation Suite")
    print("=" * 70)

    db = SessionLocal()
    vector_store = VectorStoreManager(index_dir=settings.VECTORSTORE_DIR, dimension=384)
    retriever = HybridRetriever(vector_store=vector_store)
    rag_engine = RAGEngine(retriever=retriever)

    total_queries = len(EVALUATION_QUESTIONS)
    correct_classifications = 0
    correct_source_attributions = 0
    unknown_handled_correctly = 0
    total_time_ms = 0

    print(f"[*] Running evaluation across {total_queries} benchmark test cases...\n")

    for idx, test in enumerate(EVALUATION_QUESTIONS, 1):
        q = test["query"]
        t0 = time.time()
        res = rag_engine.process_query(db, q, user_id=1)
        elapsed_ms = (time.time() - t0) * 1000
        total_time_ms += elapsed_ms

        cat_match = (res["category"] == test["expected_category"])
        if cat_match:
            correct_classifications += 1

        has_sources = len(res["sources"]) > 0
        if test["should_find_source"]:
            if has_sources:
                correct_source_attributions += 1
        else:
            if not has_sources or res["unknown_query"]:
                unknown_handled_correctly += 1

        print(f"[{idx}/{total_queries}] Query: '{q[:45]}...'")
        print(f"      Category: {res['category']} (Expected: {test['expected_category']}) [{'✓' if cat_match else 'X'}]")
        print(f"      Sources: {len(res['sources'])} found | Unknown Flag: {res['unknown_query']} | Time: {elapsed_ms:.1f}ms")
        print("-" * 70)

    db.close()

    avg_latency = total_time_ms / total_queries
    cat_accuracy = (correct_classifications / total_queries) * 100
    expected_known = sum(1 for t in EVALUATION_QUESTIONS if t["should_find_source"])
    expected_unknown = total_queries - expected_known
    
    source_acc = (correct_source_attributions / expected_known) * 100
    unknown_acc = (unknown_handled_correctly / expected_unknown) * 100

    print("\n" + "=" * 70)
    print("FINAL EVALUATION METRICS REPORT")
    print("=" * 70)
    print(f"Total Test Cases Evaluated   : {total_queries}")
    print(f"Query Classification Accuracy : {cat_accuracy:.1f}% ({correct_classifications}/{total_queries})")
    print(f"Source Retrieval Accuracy     : {source_acc:.1f}% ({correct_source_attributions}/{expected_known})")
    print(f"Unknown Query Safety Accuracy : {unknown_acc:.1f}% ({unknown_handled_correctly}/{expected_unknown})")
    print(f"Average System Latency        : {avg_latency:.1f} ms / query")
    print("=" * 70)

if __name__ == "__main__":
    run_evaluation()
