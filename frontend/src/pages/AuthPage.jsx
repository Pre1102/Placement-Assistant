import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, ShieldCheck, LogIn, UserPlus, AlertCircle, ArrowLeft } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

export default function AuthPage() {
  const navigate = useNavigate();
  const { login, signup } = useAuth();

  // Portal selection state: null | 'student' | 'admin'
  const [selectedRole, setSelectedRole] = useState(null);
  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Form Fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
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
      let res;
      if (isSignup) {
        res = await signup({
          name,
          email,
          password,
          role: selectedRole,
          branch,
          cgpa: parseFloat(cgpa) || 7.2,
          backlogs: parseInt(backlogs, 10) || 0,
          graduation_year: parseInt(graduationYear, 10) || 2027,
          preferred_role: preferredRole,
          skills
        });
      } else {
        res = await login(email, password);
      }

      // Navigate based on actual user role
      if (res.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/');
      }
    } catch (err) {
      console.error("Auth submit error:", err);
      setError(err.response?.data?.detail || "Authentication failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  // Step 1: Role Selection Portal
  if (!selectedRole) {
    return (
      <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center p-4">
        <div className="max-w-xl w-full space-y-8">
          
          {/* Brand Header */}
          <div className="text-center space-y-2">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-emerald-600 text-white shadow-lg shadow-emerald-600/30 mb-2">
              <GraduationCap className="w-8 h-8" />
            </div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">CareerCampusAI</h1>
            <p className="text-sm text-slate-500 font-medium">
              Source-Grounded Placement Intelligence & Career Guidance System
            </p>
          </div>

          <div className="text-center text-xs font-bold text-slate-400 uppercase tracking-wider">
            Select Your Account Type to Continue
          </div>

          {/* Portal Selection Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            
            {/* Student Portal Card */}
            <Card
              onClick={() => { setSelectedRole('student'); setIsSignup(false); setError(''); }}
              className="p-6 cursor-pointer hover:border-emerald-500 hover:ring-2 hover:ring-emerald-500/20 transition-all text-left group"
            >
              <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                <GraduationCap className="w-6 h-6" />
              </div>
              <h3 className="font-extrabold text-slate-900 text-lg mb-1">Student Portal</h3>
              <p className="text-xs text-slate-500 leading-relaxed mb-4">
                Access placement eligibility checks, company requirements, AI query assistant, interview prep, and career roadmaps.
              </p>
              <div className="inline-flex items-center text-xs font-bold text-emerald-600 group-hover:text-emerald-700">
                <span>Student Login / Register</span>
                <span className="ml-1">→</span>
              </div>
            </Card>

            {/* Admin Cell Portal Card */}
            <Card
              onClick={() => { setSelectedRole('admin'); setIsSignup(false); setError(''); }}
              className="p-6 cursor-pointer hover:border-purple-500 hover:ring-2 hover:ring-purple-500/20 transition-all text-left group"
            >
              <div className="w-12 h-12 rounded-2xl bg-purple-100 text-purple-700 flex items-center justify-center mb-4 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="font-extrabold text-slate-900 text-lg mb-1">Placement Admin Cell</h3>
              <p className="text-xs text-slate-500 leading-relaxed mb-4">
                Upload institutional policy notices, manage FAISS vector knowledge base, re-index documents, and inspect retrieval scores.
              </p>
              <div className="inline-flex items-center text-xs font-bold text-purple-600 group-hover:text-purple-700">
                <span>Admin Login / Register</span>
                <span className="ml-1">→</span>
              </div>
            </Card>

          </div>

        </div>
      </div>
    );
  }

  // Step 2: Dedicated Auth Form (Student or Admin)
  const isStudent = selectedRole === 'student';

  return (
    <div className="min-h-[calc(100vh-6rem)] flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-6">

        {/* Back to Portal Selector */}
        <button
          onClick={() => setSelectedRole(null)}
          className="inline-flex items-center text-xs font-bold text-slate-500 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          <span>Switch Account Type</span>
        </button>

        {/* Form Title Banner */}
        <div className="text-center space-y-1">
          <div className={`inline-flex items-center justify-center w-12 h-12 rounded-2xl ${isStudent ? 'bg-emerald-100 text-emerald-700' : 'bg-purple-100 text-purple-700'} mb-1`}>
            {isStudent ? <GraduationCap className="w-6 h-6" /> : <ShieldCheck className="w-6 h-6" />}
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {isStudent ? 'Student Workspace' : 'Placement Cell Admin'}
          </h2>
          <p className="text-xs text-slate-500">
            {isSignup ? `Create a new ${isStudent ? 'Student' : 'Admin'} Account` : `Sign in to your ${isStudent ? 'Student' : 'Admin'} Account`}
          </p>
        </div>

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
              <div>
                <label className="block text-slate-700 font-bold mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder={isStudent ? "e.g. Alex Morgan" : "e.g. Dr. R. K. Sharma"}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
                />
              </div>
            )}

            <div>
              <label className="block text-slate-700 font-bold mb-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={isStudent ? "student@college.edu" : "placement.cell@college.edu"}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>

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

            {/* Academic details for student signup */}
            {isSignup && isStudent && (
              <div className="pt-2 border-t border-slate-100 space-y-3">
                <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block">Academic Profile</span>

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
              </div>
            )}

            <Button
              type="submit"
              disabled={loading}
              className={`w-full py-2.5 mt-2 shadow-xs ${!isStudent ? 'bg-purple-600 hover:bg-purple-700' : ''}`}
            >
              {isSignup ? <UserPlus className="w-4 h-4 mr-1.5" /> : <LogIn className="w-4 h-4 mr-1.5" />}
              <span>{loading ? 'Processing...' : isSignup ? `Register as ${isStudent ? 'Student' : 'Admin'}` : `Sign In to ${isStudent ? 'Student' : 'Admin'} Portal`}</span>
            </Button>

          </form>

        </Card>
      </div>
    </div>
  );
}
