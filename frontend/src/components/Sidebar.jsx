import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, BotMessageSquare, CheckCircle2, Building2, 
  Compass, HelpCircle, FileText, User, BarChart3, Files, Database, SearchCode 
} from 'lucide-react';

export default function Sidebar({ activeRole }) {
  const studentNav = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'AI Assistant', path: '/ai-assistant', icon: BotMessageSquare },
    { name: 'Placement Checker', path: '/placement', icon: CheckCircle2 },
    { name: 'Companies', path: '/companies', icon: Building2 },
    { name: 'Career Guidance', path: '/career', icon: Compass },
    { name: 'Interview Prep', path: '/interview-prep', icon: HelpCircle },
    { name: 'Resume Guidance', path: '/resume-guidance', icon: FileText },
    { name: 'My Profile', path: '/profile', icon: User },
  ];

  const adminNav = [
    { name: 'Admin Dashboard', path: '/admin', icon: BarChart3 },
    { name: 'Documents', path: '/admin/documents', icon: Files },
    { name: 'Knowledge Base', path: '/admin/knowledge-base', icon: Database },
    { name: 'Retrieval Testing', path: '/admin/retrieval-test', icon: SearchCode },
  ];

  const currentNav = activeRole === 'student' ? studentNav : adminNav;

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between hidden md:block">
      <div className="space-y-6">
        <div>
          <h2 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            {activeRole === 'student' ? 'Student Workspace' : 'Placement Cell Admin'}
          </h2>
          <nav className="space-y-1">
            {currentNav.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/' || item.path === '/admin'}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-emerald-50 text-emerald-700 font-semibold shadow-xs border border-emerald-100'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 text-emerald-600" />
                  <span>{item.name}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Footer info badge */}
      <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-xs text-slate-500">
        <p className="font-semibold text-slate-700">Controlled Knowledge Base</p>
        <p className="mt-0.5 text-[11px] text-slate-500">Source-Grounded Institutional AI</p>
      </div>
    </aside>
  );
}
