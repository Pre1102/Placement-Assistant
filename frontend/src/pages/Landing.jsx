import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Compass, BotMessageSquare, Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 sm:py-12 space-y-12">
      
      {/* Hero Section */}
      <div className="text-center space-y-6 max-w-3xl mx-auto pt-6">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 text-emerald-800 border border-emerald-200 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
          <span>Multidisciplinary Generative AI Capstone Project</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
          CareerCampus<span className="text-emerald-600">AI</span>
        </h1>
        
        <p className="text-lg sm:text-xl font-medium text-slate-600 leading-relaxed">
          Your AI-powered placement and career companion.
        </p>

        <p className="text-sm sm:text-base text-slate-500 max-w-2xl mx-auto leading-relaxed">
          Understand placement requirements, check eligibility, explore career paths, and prepare for your next opportunity with source-grounded AI assistance.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Button size="lg" onClick={() => navigate('/ai-assistant')} className="shadow-lg shadow-emerald-600/20">
            <span>Ask CareerCampusAI</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
          <Button variant="outline" size="lg" onClick={() => navigate('/placement')}>
            <span>Check My Eligibility</span>
          </Button>
        </div>
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 pt-6">
        
        <Card className="hover:-translate-y-1 transition-transform">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4 font-bold">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1">Placement Intelligence</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Understand institutional placement policies, eligibility rules, and company backlog restrictions.
          </p>
        </Card>

        <Card className="hover:-translate-y-1 transition-transform">
          <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center mb-4 font-bold">
            <Compass className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1">Career Guidance</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Get structured, step-by-step roadmaps for target roles like Data Analyst, Software Developer, and AI/ML.
          </p>
        </Card>

        <Card className="hover:-translate-y-1 transition-transform">
          <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4 font-bold">
            <BotMessageSquare className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1">AI Assistant</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Ask placement queries in natural language with automatic category classification.
          </p>
        </Card>

        <Card className="hover:-translate-y-1 transition-transform">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center mb-4 font-bold">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-base mb-1">Source-Grounded</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Every answer cites official document names and page numbers without hallucination.
          </p>
        </Card>

      </div>

    </div>
  );
}
