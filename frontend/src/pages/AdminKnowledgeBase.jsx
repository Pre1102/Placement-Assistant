import React, { useState, useEffect } from 'react';
import { Database, RefreshCw, CheckCircle2, ShieldCheck } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import { getKBStatus, rebuildKBIndex } from '../services/api';

export default function AdminKnowledgeBase() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rebuilding, setRebuilding] = useState(false);
  const [message, setMessage] = useState("");

  const loadStatus = async () => {
    try {
      const data = await getKBStatus();
      setStatus(data);
    } catch (err) {
      console.error("KB status error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleRebuild = async () => {
    if (!window.confirm("Rebuilding the index will clear the FAISS vector store and re-vectorize all documents in SQLite. Proceed?")) return;
    setRebuilding(true);
    setMessage("");
    try {
      const newStatus = await rebuildKBIndex();
      setStatus(newStatus);
      setMessage("FAISS Vector Index rebuilt successfully from database documents!");
    } catch (err) {
      console.error("Rebuild error:", err);
      setMessage("Failed to rebuild FAISS vector index.");
    } finally {
      setRebuilding(false);
    }
  };

  if (loading) return <LoadingSpinner label="Loading Knowledge Base Index Metrics..." size="lg" />;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <Database className="w-6 h-6 text-purple-600" />
          <span>FAISS Vector Index & Knowledge Base Health</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Monitor embedding vector counts, index synchronization, and trigger full index rebuilds.
        </p>
      </div>

      {message && (
        <div className={`p-4 rounded-xl border text-xs font-semibold flex items-center space-x-2 ${
          message.includes('successfully') ? 'bg-emerald-50 text-emerald-800 border-emerald-200' : 'bg-rose-50 text-rose-800 border-rose-200'
        }`}>
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{message}</span>
        </div>
      )}

      {/* Metrics Card */}
      <Card className="p-6 bg-white">
        <h3 className="font-bold text-slate-900 text-base mb-4">Vector Store Synchronization Health</h3>
        
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 block mb-1">Index Status</span>
            <span className="font-bold text-emerald-600 text-sm">{status?.status || 'Active'}</span>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 block mb-1">Total Indexed Documents</span>
            <span className="font-bold text-slate-900 text-sm">{status?.total_documents ?? 0}</span>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 block mb-1">Extracted Text Chunks</span>
            <span className="font-bold text-slate-900 text-sm">{status?.total_chunks ?? 0}</span>
          </div>

          <div className="p-3 bg-purple-50 rounded-xl border border-purple-200">
            <span className="text-purple-800 font-semibold block mb-1">FAISS Vectors</span>
            <span className="font-bold text-purple-900 text-sm">{status?.vector_count ?? 0}</span>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span>Last Index Refresh: <strong>{status?.last_updated || 'Just now'}</strong></span>
          <Button onClick={handleRebuild} disabled={rebuilding} variant="primary">
            <RefreshCw className={`w-4 h-4 mr-2 ${rebuilding ? 'animate-spin' : ''}`} />
            <span>{rebuilding ? 'Rebuilding Index...' : 'Rebuild FAISS Vector Index'}</span>
          </Button>
        </div>
      </Card>

    </div>
  );
}
