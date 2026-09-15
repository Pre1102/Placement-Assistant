import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Student Pages
import Landing from './pages/Landing';
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

import { getProfile } from './services/api';

export default function App() {
  const [activeRole, setActiveRole] = useState('student'); // 'student' | 'admin'
  const [studentProfile, setStudentProfile] = useState(null);

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getProfile();
        setStudentProfile(data);
      } catch (err) {
        console.error("Failed to load profile for App shell:", err);
      }
    }
    loadProfile();
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
        
        {/* Header Bar */}
        <Navbar 
          activeRole={activeRole} 
          setActiveRole={setActiveRole} 
          studentProfile={studentProfile} 
        />

        {/* Main Body Shell */}
        <div className="flex-1 max-w-7xl w-full mx-auto flex">
          
          {/* Navigation Sidebar */}
          <Sidebar activeRole={activeRole} />

          {/* Router View Content Area */}
          <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-x-hidden">
            <Routes>
              {/* Student Routes */}
              <Route path="/" element={<Dashboard />} />
              <Route path="/landing" element={<Landing />} />
              <Route path="/ai-assistant" element={<AIAssistant />} />
              <Route path="/placement" element={<PlacementChecker />} />
              <Route path="/companies" element={<CompanyExplorer />} />
              <Route path="/career" element={<CareerGuidance />} />
              <Route path="/interview-prep" element={<InterviewPrep />} />
              <Route path="/resume-guidance" element={<ResumeGuidance />} />
              <Route 
                path="/profile" 
                element={<ProfilePage onProfileUpdated={(updated) => setStudentProfile(updated)} />} 
              />

              {/* Admin Routes */}
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/admin/documents" element={<AdminDocuments />} />
              <Route path="/admin/knowledge-base" element={<AdminKnowledgeBase />} />
              <Route path="/admin/retrieval-test" element={<AdminRetrievalTest />} />

              {/* Catch-all Redirect */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>

        </div>

      </div>
    </Router>
  );
}
