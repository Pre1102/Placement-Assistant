import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, ShieldCheck, UserCheck, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ activeRole, setActiveRole }) {
  const navigate = useNavigate();
  const { user, profile, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* Brand Logo & Tagline */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-md shadow-emerald-600/20">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">CareerCampus<span className="text-emerald-600">AI</span></span>
              <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded-full border border-emerald-200">RAG v1.0</span>
            </div>
            <p className="text-xs text-slate-500 font-medium hidden sm:block">Placement Intelligence & Career Guidance</p>
          </div>
        </div>

        {/* Right Side: Profile Chip + Role Switcher + Logout */}
        <div className="flex items-center space-x-3">

          {/* Logged-in User Chip */}
          {user && (
            <div
              className="hidden md:flex items-center space-x-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 text-xs text-slate-600 cursor-pointer hover:border-emerald-300 hover:bg-emerald-50 transition-colors"
              onClick={() => navigate('/profile')}
            >
              <div className="w-6 h-6 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-[11px] flex-shrink-0">
                {user.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div>
                <span className="font-bold text-slate-900 block leading-tight">{user.name}</span>
                {profile && activeRole === 'student' && (
                  <span className="text-slate-500 text-[10px]">CGPA {profile.cgpa} · {profile.backlogs} Backlogs</span>
                )}
              </div>
            </div>
          )}

          {/* Role Selector Tabs */}
          <div className="bg-slate-100 p-1 rounded-xl flex items-center space-x-1 border border-slate-200">
            <button
              onClick={() => setActiveRole('student')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeRole === 'student'
                  ? 'bg-white text-emerald-700 shadow-xs border border-slate-200/60'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>Student</span>
            </button>
            <button
              onClick={() => setActiveRole('admin')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeRole === 'admin'
                  ? 'bg-white text-emerald-700 shadow-xs border border-slate-200/60'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Admin Cell</span>
            </button>
          </div>

          {/* Logout Button */}
          {user && (
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-2 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}

        </div>

      </div>
    </header>
  );
}
