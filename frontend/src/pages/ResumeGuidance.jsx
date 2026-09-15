import React, { useState, useEffect } from 'react';
import { FileText, Sparkles, AlertCircle, CheckCircle2, Award } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { getProfile, getResumeGuidance } from '../services/api';

export default function ResumeGuidance() {
  const [targetRole, setTargetRole] = useState("Software Developer");
  const [skills, setSkills] = useState("Python, SQL, HTML, CSS");
  const [projects, setProjects] = useState("Placement portal using Python and SQLite");
  const [guidance, setGuidance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        const prof = await getProfile();
        if (prof) {
          setSkills(prof.skills || skills);
          setTargetRole(prof.preferred_role || targetRole);
        }
        const data = await getResumeGuidance(prof?.preferred_role || targetRole, prof?.skills || skills, projects);
        setGuidance(data);
      } catch (err) {
        console.error("Resume guidance error:", err);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    try {
      const data = await getResumeGuidance(targetRole, skills, projects);
      setGuidance(data);
    } catch (err) {
      console.error("Resume analysis error:", err);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) return <LoadingSpinner label="Analyzing resume alignment..." size="lg" />;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <FileText className="w-6 h-6 text-emerald-600" />
          <span>Resume & ATS Alignment Analyzer</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Optimize your technical resume bullet points and key skills for automated company ATS filters.
        </p>
      </div>

      {/* Input Form */}
      <Card className="p-5">
        <div className="space-y-4 text-xs font-medium">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-bold mb-1">Target Job Role</label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              >
                <option value="Software Developer">Software Developer</option>
                <option value="Data Analyst">Data Analyst</option>
                <option value="AI/ML Engineer">AI/ML Engineer</option>
                <option value="Web Developer">Web Developer</option>
                <option value="Cybersecurity">Cybersecurity Analyst</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-700 font-bold mb-1">Current Technical Skills</label>
              <input
                type="text"
                value={skills}
                onChange={(e) => setSkills(e.target.value)}
                placeholder="Python, C++, SQL, Git"
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-700 font-bold mb-1">Key Academic / Personal Projects</label>
            <textarea
              rows="2"
              value={projects}
              onChange={(e) => setProjects(e.target.value)}
              placeholder="Describe 1-2 projects you've built..."
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            ></textarea>
          </div>

          <div className="flex justify-end">
            <Button onClick={handleAnalyze} disabled={analyzing} className="shadow-xs">
              <Sparkles className="w-4 h-4 mr-1.5" />
              <span>{analyzing ? 'Analyzing Alignment...' : 'Analyze Resume Alignment'}</span>
            </Button>
          </div>

        </div>
      </Card>

      {/* Analysis Output */}
      {guidance && (
        <div className="space-y-6">
          
          {/* Score Banner */}
          <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <span className="text-emerald-400 font-semibold text-xs uppercase tracking-wider">ATS Alignment Score</span>
              <h2 className="text-3xl font-extrabold mt-1">{guidance.alignment_score}</h2>
              <p className="text-xs text-slate-300 mt-1">Based on role expectations for {guidance.target_role}</p>
            </div>
            <div className="bg-white/10 p-4 rounded-xl border border-white/10 text-center">
              <span className="text-xs text-slate-300 block">Missing Key Skills</span>
              <span className="text-amber-400 font-bold text-sm">{guidance.missing_skills.length} Critical Skill(s)</span>
            </div>
          </div>

          {/* Missing Skills Grid */}
          <Card>
            <h3 className="font-bold text-slate-900 text-base mb-2 flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-amber-600" />
              <span>Recommended Skills to Add to Resume</span>
            </h3>
            <div className="flex flex-wrap gap-2 pt-1">
              {guidance.missing_skills.map((sk, idx) => (
                <span key={idx} className="px-3 py-1 bg-amber-50 text-amber-900 border border-amber-200 rounded-lg text-xs font-semibold">
                  + {sk}
                </span>
              ))}
            </div>
          </Card>

          {/* STAR Bullet Point Suggestions */}
          <Card>
            <h3 className="font-bold text-slate-900 text-base mb-3 flex items-center space-x-2">
              <Award className="w-5 h-5 text-emerald-600" />
              <span>ATS-Optimized Bullet Point Suggestions (STAR Format)</span>
            </h3>
            <div className="space-y-2.5 text-xs">
              {guidance.bullet_suggestions.map((bullet, idx) => (
                <div key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-800 font-medium leading-relaxed flex items-start space-x-2">
                  <span className="text-emerald-600 font-bold text-sm">•</span>
                  <span>{bullet}</span>
                </div>
              ))}
            </div>
          </Card>

        </div>
      )}

    </div>
  );
}
