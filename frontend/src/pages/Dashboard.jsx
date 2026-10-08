import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, BotMessageSquare, Building2, Compass, 
  HelpCircle, Sparkles, FileText, ArrowRight, User 
} from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { getDocuments } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, profile } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const docsData = await getDocuments();
        setDocuments(docsData.slice(0, 5));
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <LoadingSpinner label="Loading Student Dashboard..." size="lg" />;

  return (
    <div className="space-y-8">
      
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-emerald-700 to-emerald-900 text-white p-6 sm:p-8 rounded-3xl shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-emerald-200 text-xs font-semibold uppercase tracking-wider mb-1">
              <Sparkles className="w-4 h-4" />
              <span>Student Placement Hub</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {user?.name || profile?.name || 'Student'}!
            </h1>
            <p className="text-emerald-100 text-sm mt-1">
              Plan your placement journey with CareerCampusAI.
            </p>
          </div>
          <Button 
            variant="outline" 
            onClick={() => navigate('/profile')} 
            className="bg-white/10 hover:bg-white/20 text-white border-white/20 hover:border-white/40 shadow-none self-start md:self-auto"
          >
            <User className="w-4 h-4 mr-2" />
            <span>Edit Profile</span>
          </Button>
        </div>

        {/* Dynamic Profile Summary Cards inside Header Banner */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-emerald-600/50 text-xs">
          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
            <span className="text-emerald-200 text-[11px] block">Branch</span>
            <span className="font-bold text-white text-sm truncate block">{profile?.branch || 'Computer Engineering'}</span>
          </div>
          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
            <span className="text-emerald-200 text-[11px] block">Overall CGPA</span>
            <span className="font-bold text-white text-sm">{profile?.cgpa !== undefined ? profile.cgpa : '8.0'} / 10.0</span>
          </div>
          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
            <span className="text-emerald-200 text-[11px] block">Active Backlogs</span>
            <span className="font-bold text-white text-sm">{profile?.backlogs !== undefined ? profile.backlogs : 0} Backlog(s)</span>
          </div>
          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/10">
            <span className="text-emerald-200 text-[11px] block">Target Role</span>
            <span className="font-bold text-white text-sm truncate block">{profile?.preferred_role || 'Data Analyst'}</span>
          </div>
        </div>
      </div>

      {/* Quick Actions Grid */}
      <div>
        <h2 className="text-base font-bold text-slate-900 mb-4 flex items-center space-x-2">
          <span>Quick Actions</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          
          <Card onClick={() => navigate('/placement')} className="group cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-3">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-sm mb-1 group-hover:text-emerald-700 transition-colors">Check Eligibility</h3>
            <p className="text-xs text-slate-500">Check eligibility for available company drives.</p>
          </Card>

          <Card onClick={() => navigate('/ai-assistant')} className="group cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center mb-3">
              <BotMessageSquare className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-sm mb-1 group-hover:text-purple-700 transition-colors">Ask AI Assistant</h3>
            <p className="text-xs text-slate-500">Ask placement or career questions in natural language.</p>
          </Card>

          <Card onClick={() => navigate('/companies')} className="group cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-3">
              <Building2 className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-sm mb-1 group-hover:text-amber-700 transition-colors">Explore Companies</h3>
            <p className="text-xs text-slate-500">Compare company eligibility requirements side by side.</p>
          </Card>

          <Card onClick={() => navigate('/career')} className="group cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center mb-3">
              <Compass className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-sm mb-1 group-hover:text-emerald-800 transition-colors">Career Roadmap</h3>
            <p className="text-xs text-slate-500">Explore step-by-step preparation roadmaps.</p>
          </Card>

          <Card onClick={() => navigate('/interview-prep')} className="group cursor-pointer">
            <div className="w-9 h-9 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center mb-3">
              <HelpCircle className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-slate-900 text-sm mb-1 group-hover:text-rose-700 transition-colors">Interview Prep</h3>
            <p className="text-xs text-slate-500">Practice questions for your target technical role.</p>
          </Card>

        </div>
      </div>

      {/* Knowledge Base Documents Feed */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-2xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-base">Indexed Placement Notices & Documents</h3>
            <p className="text-xs text-slate-500">Official institutional rules available in the knowledge base</p>
          </div>
          <Button variant="ghost" size="sm" onClick={() => navigate('/companies')}>
            <span>View All</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>

        {documents.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-400">
            No placement documents indexed yet. Check back soon.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {documents.map((doc) => (
              <div key={doc.id} className="py-3 flex items-center justify-between text-xs">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center font-bold">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-slate-900">{doc.filename}</h4>
                    <p className="text-[11px] text-slate-500">{doc.chunk_count} chunks indexed • Category: {doc.category}</p>
                  </div>
                </div>
                <Badge variant={doc.category === 'Company Notices' ? 'purple' : 'emerald'}>
                  {doc.category}
                </Badge>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
