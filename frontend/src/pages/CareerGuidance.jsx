import React, { useState, useEffect } from 'react';
import { Compass, Sparkles, CheckCircle2, BookOpen, Code, Trophy } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { getCareerRoadmap } from '../services/api';

export default function CareerGuidance() {
  const [targetRole, setTargetRole] = useState("Data Analyst");
  const [skillLevel, setSkillLevel] = useState("Beginner");
  const [prepTime, setPrepTime] = useState("3 Months");
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchRoadmap = async () => {
    setLoading(true);
    try {
      const data = await getCareerRoadmap(targetRole, skillLevel, prepTime);
      setRoadmap(data);
    } catch (err) {
      console.error("Career roadmap error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, [targetRole, skillLevel, prepTime]);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <Compass className="w-6 h-6 text-emerald-600" />
          <span>Career Guidance & Skill Roadmaps</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Structured learning sequences, portfolio projects, and preparation timelines for tech roles.
        </p>
      </div>

      {/* Control Filters */}
      <Card className="p-4 bg-white">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-medium">
          <div>
            <label className="block text-slate-700 font-bold mb-1">Target Career Role</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="Data Analyst">Data Analyst</option>
              <option value="Software Developer">Software Developer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Web Developer">Web Developer</option>
              <option value="Cybersecurity">Cybersecurity Analyst</option>
              <option value="Cloud Engineer">Cloud Engineer</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-700 font-bold mb-1">Current Skill Level</label>
            <select
              value={skillLevel}
              onChange={(e) => setSkillLevel(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="Beginner">Beginner (Foundations)</option>
              <option value="Intermediate">Intermediate (Practitioner)</option>
              <option value="Advanced">Advanced (Placement Ready)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-700 font-bold mb-1">Preparation Timeline</label>
            <select
              value={prepTime}
              onChange={(e) => setPrepTime(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="1 Month">1 Month Fast-Track</option>
              <option value="3 Months">3 Months Standard</option>
              <option value="6 Months">6 Months Comprehensive</option>
            </select>
          </div>
        </div>
      </Card>

      {loading ? (
        <LoadingSpinner label="Generating customized career roadmap..." size="lg" />
      ) : roadmap ? (
        <div className="space-y-6">
          
          {/* Phase-by-Phase Roadmap Timeline */}
          <Card>
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-base flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-emerald-600" />
                <span>Step-by-Step Learning Timeline</span>
              </h3>
              <Badge variant="emerald">{roadmap.preparation_time} Plan</Badge>
            </div>

            <div className="space-y-4">
              {roadmap.phases.map((phase, idx) => (
                <div key={idx} className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 text-xs">
                  <div className="flex items-center justify-between font-bold text-slate-900 mb-1">
                    <span className="text-emerald-700 font-extrabold">{phase.phase}</span>
                    <span className="text-slate-500 text-[11px] font-normal">{phase.duration}</span>
                  </div>
                  <h4 className="font-bold text-slate-800 mb-2">{phase.title}</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {phase.topics.map((top, tIdx) => (
                      <span key={tIdx} className="px-2.5 py-1 bg-white border border-slate-200 text-slate-700 rounded-md text-[11px]">
                        ✓ {top}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Recommended Portfolio Projects */}
          <Card>
            <h3 className="font-bold text-slate-900 text-base mb-3 flex items-center space-x-2">
              <Code className="w-5 h-5 text-purple-600" />
              <span>Recommended Portfolio Projects</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              {roadmap.portfolio_projects.map((proj, pIdx) => (
                <div key={pIdx} className="p-3 bg-purple-50/50 border border-purple-200 rounded-xl text-purple-900 font-semibold">
                  🚀 {proj}
                </div>
              ))}
            </div>
          </Card>

          {/* Interview Tips */}
          <Card className="bg-amber-50/50 border-amber-200">
            <h3 className="font-bold text-amber-900 text-base mb-2 flex items-center space-x-2">
              <Trophy className="w-5 h-5 text-amber-600" />
              <span>Placement Officer's Pro Tips</span>
            </h3>
            <ul className="list-disc list-inside space-y-1 text-xs text-amber-800 font-medium">
              {roadmap.interview_tips.map((tip, tIdx) => (
                <li key={tIdx}>{tip}</li>
              ))}
            </ul>
          </Card>

        </div>
      ) : null}

    </div>
  );
}
