import React, { useState, useEffect } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Sparkles, Award } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { generateInterviewPrep } from '../services/api';

export default function InterviewPrep() {
  const [targetRole, setTargetRole] = useState("Software Developer");
  const [topic, setTopic] = useState("All");
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [prepData, setPrepData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openIndex, setOpenIndex] = useState(null);

  const fetchQuestions = async () => {
    setLoading(true);
    setOpenIndex(null);
    try {
      const data = await generateInterviewPrep(targetRole, topic, difficulty);
      setPrepData(data);
    } catch (err) {
      console.error("Interview prep error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, [targetRole, topic, difficulty]);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <HelpCircle className="w-6 h-6 text-emerald-600" />
          <span>Interview Question Generator</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Practice technical, analytical, and HR interview questions tailored to company campus drives.
        </p>
      </div>

      {/* Control Filters */}
      <Card className="p-4 bg-white">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-medium">
          <div>
            <label className="block text-slate-700 font-bold mb-1">Target Role</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="Software Developer">Software Developer</option>
              <option value="Data Analyst">Data Analyst</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Web Developer">Web Developer</option>
              <option value="Cybersecurity">Cybersecurity Analyst</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-700 font-bold mb-1">Topic Filter</label>
            <select
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="All">All Topics</option>
              <option value="Data Structures & Algorithms">Data Structures & Algorithms</option>
              <option value="SQL & Databases">SQL & Databases</option>
              <option value="System Design">System Design</option>
              <option value="Behavioral & HR">Behavioral & HR</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-700 font-bold mb-1">Difficulty Level</label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
            >
              <option value="Beginner">Beginner (Screening)</option>
              <option value="Intermediate">Intermediate (Technical R1)</option>
              <option value="Advanced">Advanced (Technical R2)</option>
            </select>
          </div>
        </div>
      </Card>

      {loading ? (
        <LoadingSpinner label="Generating interview question suite..." size="lg" />
      ) : prepData && prepData.questions ? (
        <div className="space-y-4">
          
          <div className="flex items-center justify-between text-xs text-slate-500 px-1">
            <span>Generated {prepData.questions.length} Questions for <strong className="text-slate-900">{prepData.target_role}</strong></span>
            <Badge variant="purple">{prepData.difficulty}</Badge>
          </div>

          {prepData.questions.map((q, idx) => {
            const isOpen = openIndex === idx;

            return (
              <Card key={idx} className="p-4 sm:p-5">
                <div 
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="flex items-start justify-between cursor-pointer select-none space-x-3"
                >
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-extrabold text-emerald-700 text-sm">Q{idx + 1}.</span>
                      <h3 className="font-bold text-slate-900 text-sm">{q.question}</h3>
                    </div>
                    <div className="flex items-center space-x-2 text-[11px]">
                      <Badge variant="slate">{q.topic}</Badge>
                    </div>
                  </div>
                  <button className="text-slate-400 hover:text-slate-600 mt-1">
                    {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>

                {isOpen && (
                  <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-700 space-y-3 animate-fadeIn">
                    <div className="bg-emerald-50/60 p-3.5 rounded-xl border border-emerald-200/80">
                      <span className="font-bold text-emerald-900 block mb-1">Model Answer / Key Points:</span>
                      <p className="leading-relaxed text-slate-800 font-medium whitespace-pre-line">{q.answer}</p>
                    </div>
                  </div>
                )}
              </Card>
            );
          })}

        </div>
      ) : null}

    </div>
  );
}
