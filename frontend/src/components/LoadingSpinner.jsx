import React from 'react';

export default function LoadingSpinner({ label = "Loading...", size = "md" }) {
  const sizeClasses = {
    sm: "w-4 h-4 border-2",
    md: "w-6 h-6 border-2",
    lg: "w-8 h-8 border-3"
  };

  return (
    <div className="flex items-center justify-center space-x-2 py-4 text-slate-600">
      <div className={`animate-spin rounded-full border-emerald-600 border-t-transparent ${sizeClasses[size] || sizeClasses.md}`}></div>
      {label && <span className="text-sm font-medium text-slate-600">{label}</span>}
    </div>
  );
}
