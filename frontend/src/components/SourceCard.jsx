import React from 'react';
import { FileText } from 'lucide-react';

export default function SourceCard({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-200/80">
      <h5 className="text-xs font-semibold text-slate-500 mb-2 flex items-center space-x-1.5">
        <FileText className="w-3.5 h-3.5 text-emerald-600" />
        <span>Grounded Knowledge Sources ({sources.length})</span>
      </h5>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {sources.map((src, i) => (
          <div key={i} className="p-2 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-200 transition-colors text-xs">
            <div className="font-medium text-slate-900 truncate">
              📄 {src.document_name}
            </div>
            <div className="flex items-center justify-between text-[11px] text-slate-500 mt-1">
              <span>Page {src.page_number}</span>
              {src.category && <span className="bg-slate-200/70 text-slate-700 px-1.5 py-0.5 rounded text-[10px]">{src.category}</span>}
            </div>
            {src.snippet && (
              <p className="mt-1 text-[11px] text-slate-600 italic line-clamp-2">
                "{src.snippet}"
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
