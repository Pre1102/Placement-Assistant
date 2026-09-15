import React from 'react';

export default function Button({ 
  children, 
  variant = "primary", 
  size = "md", 
  className = "", 
  disabled = false,
  onClick = () => {},
  type = "button"
}) {
  const base = "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-emerald-500/20";
  
  const variants = {
    primary: "bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm shadow-emerald-600/20 active:scale-[0.98]",
    secondary: "bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-200 active:scale-[0.98]",
    outline: "bg-white hover:bg-emerald-50 text-emerald-700 border border-emerald-300 hover:border-emerald-400 active:scale-[0.98]",
    ghost: "text-slate-600 hover:text-slate-900 hover:bg-slate-100",
    danger: "bg-rose-600 hover:bg-rose-700 text-white shadow-sm shadow-rose-600/20 active:scale-[0.98]"
  };

  const sizes = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-4 py-2.5 text-sm",
    lg: "px-5 py-3 text-base"
  };

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`${base} ${variants[variant] || variants.primary} ${sizes[size] || sizes.md} ${className}`}
    >
      {children}
    </button>
  );
}
