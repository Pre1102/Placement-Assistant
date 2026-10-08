import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, ShieldCheck, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const navigate = useNavigate();
  const { user, profile, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const isAdmin = user?.role === 'admin';

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* Brand Logo & Tagline */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate(isAdmin ? '/admin' : '/')}>
          <div className={`w-10 h-10 rounded-xl ${isAdmin ? 'bg-purple-600 shadow-purple-600/20' : 'bg-emerald-600 shadow-emerald-600/20'} flex items-center justify-center text-white shadow-md`}>
            {isAdmin ? <ShieldCheck className="w-6 h-6" /> : <GraduationCap className="w-6 h-6" />}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">CareerCampus<span className={isAdmin ? 'text-purple-600' : 'text-emerald-600'}>AI</span></span>
              <span className={`px-2 py-0.5 text-xs font-semibold rounded-full border ${isAdmin ? 'bg-purple-100 text-purple-800 border-purple-200' : 'bg-emerald-100 text-emerald-800 border-emerald-200'}`}>
                {isAdmin ? 'Admin Portal' : 'Student Portal'}
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium hidden sm:block">
              {isAdmin ? 'Placement Cell Administration & Knowledge Base' : 'Placement Intelligence & Career Guidance'}
            </p>
          </div>
        </div>

        {/* Right Side: Logged-in User Profile & Logout */}
        <div className="flex items-center space-x-3">

          {user && (
            <div
              className="flex items-center space-x-2.5 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200 text-xs cursor-pointer hover:bg-slate-100 transition-colors"
              onClick={() => !isAdmin && navigate('/profile')}
            >
              <div className={`w-7 h-7 rounded-full ${isAdmin ? 'bg-purple-600' : 'bg-emerald-600'} text-white flex items-center justify-center font-bold text-xs flex-shrink-0`}>
                {user.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div>
                <span className="font-bold text-slate-900 block leading-tight">{user.name}</span>
                <span className="text-slate-500 text-[10px]">
                  {isAdmin ? '🛡️ Placement Officer' : profile ? `CGPA ${profile.cgpa} · ${profile.branch}` : 'Student'}
                </span>
              </div>
            </div>
          )}

          {/* Logout Button */}
          {user && (
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-2 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors border border-transparent hover:border-rose-200"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}

        </div>

      </div>
    </header>
  );
}
