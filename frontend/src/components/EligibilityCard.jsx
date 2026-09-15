import React from 'react';
import { CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

export default function EligibilityCard({ eligibility }) {
  if (!eligibility) return null;

  const { company_name, status, reasons, checks, sources } = eligibility;

  const statusConfig = {
    "Eligible": {
      bg: "bg-emerald-50/80 border-emerald-200 text-emerald-900",
      badge: "bg-emerald-600 text-white",
      icon: CheckCircle2,
      label: "✅ Eligible for Campus Drive"
    },
    "Not Eligible": {
      bg: "bg-rose-50/80 border-rose-200 text-rose-900",
      badge: "bg-rose-600 text-white",
      icon: XCircle,
      label: "❌ Not Eligible"
    },
    "Requirement Unknown": {
      bg: "bg-amber-50/80 border-amber-200 text-amber-900",
      badge: "bg-amber-600 text-white",
      icon: AlertCircle,
      label: "⚠️ Requirement Unknown"
    }
  };

  const config = statusConfig[status] || statusConfig["Requirement Unknown"];
  const Icon = config.icon;

  return (
    <div className={`rounded-2xl border p-4 sm:p-5 my-3 ${config.bg}`}>
      
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
        <div className="flex items-center space-x-2">
          <Icon className="w-5 h-5 flex-shrink-0" />
          <h4 className="font-bold text-base">{company_name} — Eligibility Result</h4>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold ${config.badge}`}>
          {status}
        </span>
      </div>

      {/* Explanatory Reasons */}
      {reasons && reasons.length > 0 && (
        <div className="mb-4 text-xs font-medium space-y-1 text-slate-700">
          {reasons.map((r, i) => (
            <p key={i}>• {r}</p>
          ))}
        </div>
      )}

      {/* Requirement Breakdown Table */}
      {checks && checks.length > 0 && (
        <div className="overflow-x-auto bg-white rounded-xl border border-slate-200 shadow-2xs">
          <table className="min-w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-3 py-2">Criterion</th>
                <th className="px-3 py-2">Company Requirement</th>
                <th className="px-3 py-2">Your Profile</th>
                <th className="px-3 py-2 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {checks.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50/50">
                  <td className="px-3 py-2 font-medium text-slate-900">{item.requirement_name}</td>
                  <td className="px-3 py-2 text-slate-600">{item.required_value}</td>
                  <td className="px-3 py-2 font-semibold text-slate-800">{item.student_value}</td>
                  <td className="px-3 py-2 text-center">
                    {item.satisfied ? (
                      <span className="inline-flex items-center text-emerald-600 font-bold">✓</span>
                    ) : (
                      <span className="inline-flex items-center text-rose-600 font-bold">✕</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Source references */}
      {sources && sources.length > 0 && (
        <div className="mt-3 text-[11px] text-slate-500 font-medium">
          Source Document: <strong className="text-slate-700">{sources[0].document_name}</strong> (Page {sources[0].page_number})
        </div>
      )}

    </div>
  );
}
