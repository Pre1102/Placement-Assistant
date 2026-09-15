import React, { useState } from 'react';
import { SearchCode, Search, Sparkles, FileText, CheckCircle2 } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { testRetrieval } from '../services/api';

const SAMPLE_QUERIES = [
  "What is the minimum CGPA for Demo Company A?",
  "What is the policy for active backlogs in campus drives?",
  "What documents are needed for placement registration?",
  "What are the internship stipend guidelines for Semester 8?"
];

export default function AdminRetrievalTest() {
  const [query, setQuery] = useState(SAMPLE_QUERIES[0]);
  const [topK, setTopK] = useState(5);
  const [results, setResults] = useState(null);
  const [testing, setTesting] = useState(false);

  const handleTest = async (testQuery = query) => {
    if (!testQuery.trim()) return;
    setTesting(true);
    try {
      const data = await testRetrieval(testQuery, topK);
      setResults(data);
    } catch (err) {
      console.error("Retrieval test error:", err);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <SearchCode className="w-6 h-6 text-amber-600" />
          <span>FAISS Vector Retrieval Inspector (Viva Evaluation Tool)</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Inspect raw top-K vector search results, embedding similarity scores, and document chunks without LLM synthesis.
        </p>
      </div>

      {/* Query Tester Card */}
      <Card className="p-5">
        <div className="space-y-4 text-xs font-medium">
          
          <div>
            <label className="block text-slate-700 font-bold mb-1">Test Search Query</label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter query to test vector store retrieval..."
                className="flex-1 px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
              <Button onClick={() => handleTest(query)} disabled={testing} className="shadow-xs">
                <Search className="w-4 h-4 mr-1.5" />
                <span>{testing ? 'Searching...' : 'Test Vector Search'}</span>
              </Button>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-100">
            <div className="flex items-center space-x-2">
              <span className="text-slate-500 font-bold">Top-K Chunks:</span>
              {[3, 5, 8, 10].map((k) => (
                <button
                  key={k}
                  onClick={() => setTopK(k)}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                    topK === k ? 'bg-amber-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  K={k}
                </button>
              ))}
            </div>

            {/* Sample Chips */}
            <div className="flex items-center space-x-1.5 overflow-x-auto">
              <span className="text-slate-400 text-[11px] font-bold">Sample Queries:</span>
              {SAMPLE_QUERIES.map((sq, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setQuery(sq);
                    handleTest(sq);
                  }}
                  className="px-2 py-0.5 bg-slate-100 hover:bg-amber-50 text-slate-700 hover:text-amber-800 rounded text-[11px] font-medium transition-colors whitespace-nowrap"
                >
                  Query #{idx + 1}
                </button>
              ))}
            </div>
          </div>

        </div>
      </Card>

      {/* Retrieval Results List */}
      {testing ? (
        <LoadingSpinner label="Computing vector embedding distances & retrieving top chunks..." size="lg" />
      ) : results ? (
        <div className="space-y-4">
          
          <div className="flex items-center justify-between text-xs text-slate-500 px-1">
            <span>Query: <strong className="text-slate-900">"{results.query}"</strong></span>
            <Badge variant="amber">{results.results.length} Chunks Retrieved</Badge>
          </div>

          {results.results.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
              No matching chunks found above threshold distance.
            </div>
          ) : (
            results.results.map((chunk, idx) => (
              <Card key={idx} className="p-4 sm:p-5 border-l-4 border-l-amber-500">
                <div className="flex items-center justify-between flex-wrap gap-2 mb-2 pb-2 border-b border-slate-100 text-xs">
                  <div className="flex items-center space-x-2">
                    <span className="font-extrabold text-amber-700">Rank #{idx + 1}</span>
                    <span className="text-slate-400">|</span>
                    <span className="font-bold text-slate-900">📄 {chunk.document_name}</span>
                    <span className="text-slate-500">(Page {chunk.page_number})</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="bg-amber-100 text-amber-900 font-bold px-2 py-0.5 rounded text-[11px]">
                      Similarity Score: {chunk.similarity_score}
                    </span>
                    {chunk.category && <Badge variant="purple">{chunk.category}</Badge>}
                  </div>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200/80 font-mono text-xs text-slate-800 leading-relaxed whitespace-pre-line">
                  {chunk.text}
                </div>
              </Card>
            ))
          )}

        </div>
      ) : null}

    </div>
  );
}
