import React, { useState, useEffect } from 'react';
import { User, Save, CheckCircle2 } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import { getProfile, updateProfile } from '../services/api';

export default function ProfilePage({ onProfileUpdated }) {
  const [profile, setProfile] = useState({
    branch: "Computer Engineering",
    cgpa: 7.2,
    graduation_year: 2027,
    backlogs: 1,
    skills: "Python, C++, SQL, HTML, CSS",
    preferred_role: "Data Analyst"
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getProfile();
        setProfile(data);
      } catch (err) {
        console.error("Failed to load profile:", err);
      } finally {
        setLoading(false);
      }
    }
    loadProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      const updated = await updateProfile(profile);
      setProfile(updated);
      setMessage("Profile updated successfully!");
      if (onProfileUpdated) onProfileUpdated(updated);
    } catch (err) {
      console.error("Failed to update profile:", err);
      setMessage("Failed to update profile. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner label="Loading Profile Details..." size="lg" />;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <User className="w-6 h-6 text-emerald-600" />
          <span>My Student Profile</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Your profile metrics are compared dynamically against company placement criteria in the eligibility engine.
        </p>
      </div>

      {message && (
        <div className={`p-4 rounded-xl border text-xs font-semibold flex items-center space-x-2 ${
          message.includes('successfully') ? 'bg-emerald-50 text-emerald-800 border-emerald-200' : 'bg-rose-50 text-rose-800 border-rose-200'
        }`}>
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{message}</span>
        </div>
      )}

      <Card>
        <form onSubmit={handleSubmit} className="space-y-5 text-xs font-medium">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Branch */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Academic Branch</label>
              <select
                value={profile.branch}
                onChange={(e) => setProfile({ ...profile, branch: e.target.value })}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
              >
                <option value="Computer Engineering">Computer Engineering (CE)</option>
                <option value="Computer Science & Engineering">Computer Science & Engineering (CSE)</option>
                <option value="Information Technology">Information Technology (IT)</option>
                <option value="Electronics & Communication">Electronics & Communication (ECE)</option>
                <option value="Electrical Engineering">Electrical Engineering (EE)</option>
              </select>
            </div>

            {/* CGPA */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Cumulative CGPA (0.0 – 10.0)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                value={profile.cgpa}
                onChange={(e) => setProfile({ ...profile, cgpa: parseFloat(e.target.value) || 0 })}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
                required
              />
            </div>

            {/* Active Backlogs */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Active Backlogs</label>
              <input
                type="number"
                min="0"
                max="10"
                value={profile.backlogs}
                onChange={(e) => setProfile({ ...profile, backlogs: parseInt(e.target.value) || 0 })}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
                required
              />
            </div>

            {/* Graduation Year */}
            <div>
              <label className="block text-slate-700 font-bold mb-1">Graduation Year</label>
              <input
                type="number"
                value={profile.graduation_year}
                onChange={(e) => setProfile({ ...profile, graduation_year: parseInt(e.target.value) || 2027 })}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
                required
              />
            </div>

          </div>

          {/* Preferred Role */}
          <div>
            <label className="block text-slate-700 font-bold mb-1">Preferred Target Role</label>
            <select
              value={profile.preferred_role}
              onChange={(e) => setProfile({ ...profile, preferred_role: e.target.value })}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
            >
              <option value="Data Analyst">Data Analyst</option>
              <option value="Software Developer">Software Developer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Web Developer">Web Developer</option>
              <option value="Cybersecurity">Cybersecurity Analyst</option>
              <option value="Cloud Engineer">Cloud Engineer</option>
            </select>
          </div>

          {/* Technical Skills */}
          <div>
            <label className="block text-slate-700 font-bold mb-1">Technical Skills (Comma separated)</label>
            <input
              type="text"
              value={profile.skills}
              onChange={(e) => setProfile({ ...profile, skills: e.target.value })}
              placeholder="Python, SQL, React, C++"
              className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/10 text-xs"
            />
          </div>

          <div className="pt-2 flex justify-end">
            <Button type="submit" disabled={saving} className="shadow-md shadow-emerald-600/20">
              <Save className="w-4 h-4 mr-2" />
              <span>{saving ? 'Saving Profile...' : 'Save Profile Updates'}</span>
            </Button>
          </div>

        </form>
      </Card>

    </div>
  );
}
