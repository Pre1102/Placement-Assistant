import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Files, Database, SearchCode, ArrowRight } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import { getKBStatus } from '../services/api';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [kbStatus, setKbStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStatus() {
      try {
        const status = await getKBStatus();
        setKbStatus(status);
      } catch (err) {
        console.error("KB status load error:", err);
      } finally {
        setLoading(false);
      }
    }
    loadStatus();
  }, []);

  if (loading) return <LoadingSpinner label="Loading Admin Cell Metrics..." size="lg" />;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <ShieldCheck className="w-6 h-6 text-emerald-600" />
          <span>Placement Cell Administration</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage knowledge base documents, FAISS vector embeddings, and test retrieval accuracy.
        </p>
      </div>

      {/* Metrics Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        
        <Card className="bg-white">
          <span className="text-xs text-slate-500 font-semibold block mb-1">Knowledge Base Status</span>
          <span className="text-xl font-extrabold text-emerald-600">{kbStatus?.status || 'Active'}</span>
        </Card>

        <Card className="bg-white">
          <span className="text-xs text-slate-500 font-semibold block mb-1">Indexed PDF Documents</span>
          <span className="text-xl font-extrabold text-slate-900">{kbStatus?.total_documents ?? 0} Docs</span>
        </Card>

        <Card className="bg-white">
          <span className="text-xs text-slate-500 font-semibold block mb-1">Total Extracted Chunks</span>
          <span className="text-xl font-extrabold text-slate-900">{kbStatus?.total_chunks ?? 0} Chunks</span>
        </Card>

        <Card className="bg-white">
          <span className="text-xs text-slate-500 font-semibold block mb-1">FAISS Index Vector Count</span>
          <span className="text-xl font-extrabold text-purple-700">{kbStatus?.vector_count ?? 0} Vectors</span>
        </Card>

      </div>

      {/* Admin Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <Card onClick={() => navigate('/admin/documents')} className="group cursor-pointer">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
            <Files className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1 group-hover:text-emerald-700 transition-colors">Document Management</h3>
          <p className="text-xs text-slate-500 mb-4">Upload new PDF placement notices, edit tags, re-process, or remove documents.</p>
          <div className="flex items-center text-xs font-bold text-emerald-600">
            <span>Manage Documents</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </div>
        </Card>

        <Card onClick={() => navigate('/admin/knowledge-base')} className="group cursor-pointer">
          <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center mb-4">
            <Database className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1 group-hover:text-purple-700 transition-colors">Knowledge Base & Index</h3>
          <p className="text-xs text-slate-500 mb-4">View FAISS index health status and trigger full index rebuilds.</p>
          <div className="flex items-center text-xs font-bold text-purple-600">
            <span>View Index Status</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </div>
        </Card>

        <Card onClick={() => navigate('/admin/retrieval-test')} className="group cursor-pointer">
          <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
            <SearchCode className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1 group-hover:text-amber-700 transition-colors">Retrieval Testing</h3>
          <p className="text-xs text-slate-500 mb-4">Test vector search chunk accuracy and similarity scores for viva demonstration.</p>
          <div className="flex items-center text-xs font-bold text-amber-600">
            <span>Test Retrieval</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </div>
        </Card>

      </div>

    </div>
  );
}
