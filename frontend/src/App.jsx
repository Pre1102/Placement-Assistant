import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';

import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LoadingSpinner from './components/LoadingSpinner';

// Auth
import AuthPage from './pages/AuthPage';

// Student Pages
import Dashboard from './pages/Dashboard';
import AIAssistant from './pages/AIAssistant';
import PlacementChecker from './pages/PlacementChecker';
import CompanyExplorer from './pages/CompanyExplorer';
import CareerGuidance from './pages/CareerGuidance';
import InterviewPrep from './pages/InterviewPrep';
import ResumeGuidance from './pages/ResumeGuidance';
import ProfilePage from './pages/ProfilePage';

// Admin Pages
import AdminDashboard from './pages/AdminDashboard';
import AdminDocuments from './pages/AdminDocuments';
import AdminKnowledgeBase from './pages/AdminKnowledgeBase';
import AdminRetrievalTest from './pages/AdminRetrievalTest';

// Protected layout component
function AppShell() {
  const { user, profile, loading } = useAuth();
  const [activeRole, setActiveRole] = useState('student');

  // Sync active role from auth user role
  useEffect(() => {
    if (user?.role === 'admin') setActiveRole('admin');
    else setActiveRole('student');
  }, [user]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <LoadingSpinner label="Restoring your session..." size="lg" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/auth" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar activeRole={activeRole} setActiveRole={setActiveRole} />

      <div className="flex-1 max-w-7xl w-full mx-auto flex">
        <Sidebar activeRole={activeRole} />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-x-hidden">
          <Routes>
            {/* Student Routes */}
            <Route path="/" element={<Dashboard />} />
            <Route path="/ai-assistant" element={<AIAssistant />} />
            <Route path="/placement" element={<PlacementChecker />} />
            <Route path="/companies" element={<CompanyExplorer />} />
            <Route path="/career" element={<CareerGuidance />} />
            <Route path="/interview-prep" element={<InterviewPrep />} />
            <Route path="/resume-guidance" element={<ResumeGuidance />} />
            <Route path="/profile" element={<ProfilePage onProfileUpdated={() => {}} />} />

            {/* Admin Routes */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/documents" element={<AdminDocuments />} />
            <Route path="/admin/knowledge-base" element={<AdminKnowledgeBase />} />
            <Route path="/admin/retrieval-test" element={<AdminRetrievalTest />} />

            {/* Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Auth Route */}
          <Route path="/auth" element={<AuthPage />} />
          {/* Everything else protected */}
          <Route path="/*" element={<AppShell />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
