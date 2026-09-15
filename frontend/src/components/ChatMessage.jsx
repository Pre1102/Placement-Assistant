import React from 'react';
import { Bot, User, AlertTriangle } from 'lucide-react';
import Badge from './Badge';
import EligibilityCard from './EligibilityCard';
import SourceCard from './SourceCard';

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';

  const categoryBadgeVariant = {
    "PLACEMENT_ELIGIBILITY": "emerald",
    "COMPANY_REQUIREMENTS": "purple",
    "PLACEMENT_PROCEDURE": "amber",
    "INTERNSHIP": "purple",
    "CAREER_GUIDANCE": "emerald",
    "INTERVIEW_PREPARATION": "amber",
    "RESUME_GUIDANCE": "emerald",
    "GENERAL": "slate"
  };

  return (
    <div className={`flex items-start space-x-3 my-4 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      
      {/* Avatar Icon */}
      <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-white flex-shrink-0 shadow-xs ${
        isUser ? 'bg-slate-800' : 'bg-emerald-600'
      }`}>
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Bubble Container */}
      <div className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 shadow-2xs ${
        isUser 
          ? 'bg-slate-900 text-white rounded-tr-xs' 
          : 'bg-white border border-slate-200 text-slate-800 rounded-tl-xs'
      }`}>
        
        {/* Category Badge & Timestamp for Assistant */}
        {!isUser && (
          <div className="flex items-center justify-between mb-2 pb-1.5 border-b border-slate-100">
            {message.category && (
              <Badge variant={categoryBadgeVariant[message.category] || "slate"}>
                {message.category.replace("_", " ")}
              </Badge>
            )}
            <span className="text-[10px] text-slate-400 font-medium">Source-Grounded AI</span>
          </div>
        )}

        {/* Query or Answer Text */}
        <div className="text-sm leading-relaxed whitespace-pre-line">
          {message.text}
        </div>

        {/* Unknown Query Warning Alert */}
        {message.unknown_query && (
          <div className="mt-3 p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Information Not Found in Knowledge Base</p>
              <p className="text-[11px] text-amber-800 mt-0.5">Please check with the placement cell or upload the relevant authorized notice.</p>
            </div>
          </div>
        )}

        {/* Structured Eligibility Card if applicable */}
        {message.eligibility_result && (
          <EligibilityCard eligibility={message.eligibility_result} />
        )}

        {/* Grounded Source Citations */}
        {message.sources && message.sources.length > 0 && (
          <SourceCard sources={message.sources} />
        )}

      </div>

    </div>
  );
}
