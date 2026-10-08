import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LoadingSpinner from './components/LoadingSpinner';

// Auth Page
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

function AppShell() {
  const { user, loading } = useAuth();

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

  const isAdmin = user.role === 'admin';

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />

      <div className="flex-1 max-w-7xl w-full mx-auto flex">
        <Sidebar />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-x-hidden">
          <Routes>
            {/* Admin Workspace Routes */}
            {isAdmin ? (
              <>
                <Route path="/admin" element={<AdminDashboard />} />
                <Route path="/admin/documents" element={<AdminDocuments />} />
                <Route path="/admin/knowledge-base" element={<AdminKnowledgeBase />} />
                <Route path="/admin/retrieval-test" element={<AdminRetrievalTest />} />
                <Route path="*" element={<Navigate to="/admin" replace />} />
              </>
            ) : (
              /* Student Workspace Routes */
              <>
                <Route path="/" element={<Dashboard />} />
                <Route path="/ai-assistant" element={<AIAssistant />} />
                <Route path="/placement" element={<PlacementChecker />} />
                <Route path="/companies" element={<CompanyExplorer />} />
                <Route path="/career" element={<CareerGuidance />} />
                <Route path="/interview-prep" element={<InterviewPrep />} />
                <Route path="/resume-guidance" element={<ResumeGuidance />} />
                <Route path="/profile" element={<ProfilePage onProfileUpdated={() => {}} />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </>
            )}
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
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/*" element={<AppShell />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
