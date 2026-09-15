import React from 'react';

export default function Card({ children, className = "", onClick = null }) {
  return (
    <div 
      onClick={onClick}
      className={`bg-white rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-all duration-200 p-6 ${onClick ? 'cursor-pointer hover:border-emerald-300' : ''} ${className}`}
    >
      {children}
    </div>
  );
}
