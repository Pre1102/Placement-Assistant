import React, { useState, useEffect } from 'react';
import { Files, Upload, RefreshCw, Trash2, CheckCircle2, AlertCircle } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { getDocuments, uploadDocument, deleteDocument, reprocessDocument } from '../services/api';

export default function AdminDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  // Upload Form State
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState("Placement Rules");
  const [company, setCompany] = useState("");

  const loadDocs = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("category", category);
    if (company) formData.append("company", company);

    try {
      await uploadDocument(formData);
      setMessage(`Document '${file.name}' uploaded and indexed successfully!`);
      setFile(null);
      setCompany("");
      loadDocs();
    } catch (err) {
      console.error("Upload error:", err);
      setMessage("Failed to upload document. Please ensure it is a valid PDF.");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId, filename) => {
    if (!window.confirm(`Are you sure you want to delete '${filename}'?`)) return;
    try {
      await deleteDocument(docId);
      setMessage(`Document '${filename}' deleted successfully.`);
      loadDocs();
    } catch (err) {
      console.error("Delete error:", err);
      setMessage("Failed to delete document.");
    }
  };

  const handleReprocess = async (docId, filename) => {
    try {
      await reprocessDocument(docId);
      setMessage(`Document '${filename}' reprocessed successfully!`);
      loadDocs();
    } catch (err) {
      console.error("Reprocess error:", err);
      setMessage("Failed to reprocess document.");
    }
  };

  if (loading) return <LoadingSpinner label="Loading Document Inventory..." size="lg" />;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <Files className="w-6 h-6 text-emerald-600" />
          <span>Document Ingestion & Management</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Upload PDF policy documents, company notices, and guidelines to update the FAISS vector knowledge base.
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

      {/* Upload Form Card */}
      <Card className="p-5">
        <h3 className="font-bold text-slate-900 text-base mb-3 flex items-center space-x-2">
          <Upload className="w-4 h-4 text-emerald-600" />
          <span>Upload PDF Document</span>
        </h3>

        <form onSubmit={handleUpload} className="space-y-4 text-xs font-medium">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            
            {/* File Input */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Select PDF File</label>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100 cursor-pointer"
                required
              />
            </div>

            {/* Category */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Document Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              >
                <option value="Placement Rules">Placement Rules</option>
                <option value="Company Notices">Company Notices</option>
                <option value="Placement Procedures">Placement Procedures</option>
                <option value="Placement FAQs">Placement FAQs</option>
                <option value="Internship">Internship Guidelines</option>
                <option value="Career Guidance">Career Guidance</option>
              </select>
            </div>

            {/* Company Tag */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Target Company (Optional)</label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="e.g. Demo Company A"
                className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>

          </div>

          <div className="flex justify-end pt-1">
            <Button type="submit" disabled={!file || uploading} size="sm">
              <span>{uploading ? 'Processing PDF & Vectorizing...' : 'Upload & Index PDF'}</span>
            </Button>
          </div>
        </form>
      </Card>

      {/* Document Inventory Table */}
      <Card className="overflow-x-auto">
        <h3 className="font-bold text-slate-900 text-base mb-3">Indexed Documents Inventory ({documents.length})</h3>
        <table className="min-w-full text-xs text-left">
          <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
            <tr>
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Filename</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Company Tag</th>
              <th className="px-4 py-3">Chunks</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {documents.map((doc) => (
              <tr key={doc.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-mono text-slate-400">#{doc.id}</td>
                <td className="px-4 py-3 font-bold text-slate-900">{doc.filename}</td>
                <td className="px-4 py-3">
                  <Badge variant={doc.category === 'Company Notices' ? 'purple' : 'emerald'}>
                    {doc.category}
                  </Badge>
                </td>
                <td className="px-4 py-3 text-slate-600">{doc.company || '—'}</td>
                <td className="px-4 py-3 font-semibold text-slate-800">{doc.chunk_count} Chunks</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px] uppercase">
                    {doc.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-right space-x-2">
                  <button
                    onClick={() => handleReprocess(doc.id, doc.filename)}
                    title="Reprocess & Re-vectorize"
                    className="p-1.5 text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 rounded-lg transition-colors"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(doc.id, doc.filename)}
                    title="Delete Document"
                    className="p-1.5 text-slate-500 hover:text-rose-700 hover:bg-rose-50 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

    </div>
  );
}
