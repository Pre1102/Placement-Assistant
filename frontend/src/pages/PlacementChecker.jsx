import React, { useState, useEffect } from 'react';
import { CheckCircle2, Building2, Filter, Search } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import EligibilityCard from '../components/EligibilityCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { checkEligibility, getCompanies } from '../services/api';

export default function PlacementChecker() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [results, setResults] = useState(null);
  const [profileSummary, setProfileSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    async function init() {
      try {
        const [compData, checkData] = await Promise.all([
          getCompanies(),
          checkEligibility()
        ]);
        setCompanies(compData);
        setResults(checkData.results);
        setProfileSummary(checkData.profile);
      } catch (err) {
        console.error("Eligibility checker initialization error:", err);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const handleRunCheck = async () => {
    setChecking(true);
    try {
      const data = await checkEligibility(selectedCompany || null);
      setResults(data.results);
    } catch (err) {
      console.error("Eligibility check error:", err);
    } finally {
      setChecking(false);
    }
  };

  if (loading) return <LoadingSpinner label="Evaluating placement eligibility metrics..." size="lg" />;

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <CheckCircle2 className="w-6 h-6 text-emerald-600" />
          <span>Placement Eligibility Analyzer</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Evaluate your profile (CGPA, Branch, Backlogs) against institutional placement rules and company notices.
        </p>
      </div>

      {/* Filter & Target Company Selector Bar */}
      <Card className="p-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-medium">
          
          <div className="flex items-center space-x-3 w-full sm:w-auto">
            <Filter className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span className="font-bold text-slate-700">Filter Target Company:</span>
            <select
              value={selectedCompany}
              onChange={(e) => setSelectedCompany(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-200 bg-white text-slate-900 focus:outline-none focus:border-emerald-500 text-xs flex-1 sm:w-64"
            >
              <option value="">Check All Drive Companies</option>
              {companies.map((c) => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
          </div>

          <Button onClick={handleRunCheck} disabled={checking} className="w-full sm:w-auto">
            <Search className="w-4 h-4 mr-2" />
            <span>{checking ? 'Evaluating...' : 'Run Eligibility Check'}</span>
          </Button>

        </div>
      </Card>

      {/* Active Profile Context Summary */}
      {profileSummary && (
        <div className="bg-slate-100 p-3.5 rounded-xl border border-slate-200 text-xs flex flex-wrap items-center justify-between gap-2 text-slate-700 font-medium">
          <div>
            Evaluated for: <strong className="text-slate-900 font-bold">{profileSummary.branch}</strong>
          </div>
          <div className="flex items-center space-x-4">
            <span>CGPA: <strong className="text-emerald-700 font-bold">{profileSummary.cgpa}</strong></span>
            <span>Backlogs: <strong className="text-slate-900 font-bold">{profileSummary.backlogs}</strong></span>
          </div>
        </div>
      )}

      {/* Results List */}
      <div className="space-y-4">
        {results && results.length > 0 ? (
          results.map((res, idx) => (
            <EligibilityCard key={idx} eligibility={res} />
          ))
        ) : (
          <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
            No eligibility results found. Click "Run Eligibility Check" to evaluate.
          </div>
        )}
      </div>

    </div>
  );
}
