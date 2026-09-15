import React from 'react';

export default function Badge({ children, variant = "emerald", className = "" }) {
  const variants = {
    emerald: "bg-emerald-50 text-emerald-800 border-emerald-200",
    amber: "bg-amber-50 text-amber-800 border-amber-200",
    purple: "bg-purple-50 text-purple-800 border-purple-200",
    rose: "bg-rose-50 text-rose-800 border-rose-200",
    slate: "bg-slate-100 text-slate-700 border-slate-200"
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-semibold border ${variants[variant] || variants.emerald} ${className}`}>
      {children}
    </span>
  );
}
