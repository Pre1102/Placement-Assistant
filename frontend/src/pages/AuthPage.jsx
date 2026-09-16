import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, LogIn, UserPlus, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, signup } = useAuth();

  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Form Fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('student');
  const [branch, setBranch] = useState('Computer Engineering');
  const [cgpa, setCgpa] = useState('7.5');
  const [backlogs, setBacklogs] = useState('0');
  const [graduationYear, setGraduationYear] = useState('2027');
  const [preferredRole, setPreferredRole] = useState('Data Analyst');
  const [skills, setSkills] = useState('Python, SQL, HTML, CSS');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isSignup) {
        await signup({
          name,
          email,
          password,
          role,
          branch,
          cgpa: parseFloat(cgpa) || 7.2,
          backlogs: parseInt(backlogs, 10) || 0,
          graduation_year: parseInt(graduationYear, 10) || 2027,
          preferred_role: preferredRole,
          skills
        });
      } else {
        await login(email, password);
      }
      // Redirect to home dashboard
      navigate('/');
    } catch (err) {
      console.error("Auth submit error:", err);
      setError(err.response?.data?.detail || "Authentication failed. Please check your details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-6">
        
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 shadow-sm mb-1">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">CareerCampusAI</h1>
          <p className="text-xs text-slate-500">
            Source-Grounded Placement Intelligence & Career Guidance System
          </p>
        </div>

        {/* Auth Card */}
        <Card className="p-6">
          
          {/* Tab Switcher */}
          <div className="grid grid-cols-2 p-1 bg-slate-100 rounded-xl mb-6 text-xs font-bold text-center">
            <button
              onClick={() => { setIsSignup(false); setError(''); }}
              className={`py-2 rounded-lg transition-all ${!isSignup ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
            >
              Sign In
            </button>
            <button
              onClick={() => { setIsSignup(true); setError(''); }}
              className={`py-2 rounded-lg transition-all ${isSignup ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
            >
              Create Account
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 text-xs font-medium">
            
            {isSignup && (
              <>
                {/* Account Role Selector */}
                <div>
                  <label className="block text-slate-700 font-bold mb-1">Account Role</label>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => setRole('student')}
                      className={`py-2 px-3 rounded-xl border text-xs font-bold text-center transition-colors ${
                        role === 'student' ? 'border-emerald-600 bg-emerald-50 text-emerald-900' : 'border-slate-200 text-slate-600'
                      }`}
                    >
                      🎓 Student
                    </button>
                    <button
                      type="button"
                      onClick={() => setRole('admin')}
                      className={`py-2 px-3 rounded-xl border text-xs font-bold text-center transition-colors ${
                        role === 'admin' ? 'border-purple-600 bg-purple-50 text-purple-900' : 'border-slate-200 text-slate-600'
                      }`}
                    >
                      🛡️ Placement Admin
                    </button>
                  </div>
                </div>

                {/* Full Name */}
                <div>
                  <label className="block text-slate-700 font-bold mb-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Alex Morgan"
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                  />
                </div>
              </>
            )}

            {/* Email Address */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@college.edu"
                className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>

            {/* Additional Academic Details for Student Signup */}
            {isSignup && role === 'student' && (
              <div className="pt-2 border-t border-slate-100 space-y-3">
                <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block">Academic Placement Details</span>
                
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-700 font-bold mb-1">Branch</label>
                    <select
                      value={branch}
                      onChange={(e) => setBranch(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                    >
                      <option value="Computer Engineering">Computer Engineering</option>
                      <option value="Information Technology">Information Technology</option>
                      <option value="Electronics & Telecom">Electronics & Telecom</option>
                      <option value="Mechanical Engineering">Mechanical Engineering</option>
                      <option value="Electrical Engineering">Electrical Engineering</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-700 font-bold mb-1">Current CGPA</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      value={cgpa}
                      onChange={(e) => setCgpa(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-700 font-bold mb-1">Active Backlogs</label>
                    <input
                      type="number"
                      min="0"
                      value={backlogs}
                      onChange={(e) => setBacklogs(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-700 font-bold mb-1">Graduation Year</label>
                    <input
                      type="number"
                      value={graduationYear}
                      onChange={(e) => setGraduationYear(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-700 font-bold mb-1">Target Career Role</label>
                  <select
                    value={preferredRole}
                    onChange={(e) => setPreferredRole(e.target.value)}
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
                  <label className="block text-slate-700 font-bold mb-1">Technical Skills</label>
                  <input
                    type="text"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    placeholder="Python, C++, SQL, Git"
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                  />
                </div>
              </div>
            )}

            <Button type="submit" disabled={loading} className="w-full py-2.5 mt-2 shadow-xs">
              {isSignup ? <UserPlus className="w-4 h-4 mr-1.5" /> : <LogIn className="w-4 h-4 mr-1.5" />}
              <span>{loading ? 'Processing...' : isSignup ? 'Create Account & Continue' : 'Sign In to Dashboard'}</span>
            </Button>

          </form>

        </Card>

      </div>
    </div>
  );
}
