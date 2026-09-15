import React, { useState, useEffect } from 'react';
import { Building2, Columns, Check, X } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import LoadingSpinner from '../components/LoadingSpinner';
import { getCompanies, compareCompanies } from '../services/api';

export default function CompanyExplorer() {
  const [companies, setCompanies] = useState([]);
  const [selectedForCompare, setSelectedForCompare] = useState([]);
  const [comparisonMatrix, setComparisonMatrix] = useState(null);
  const [loading, setLoading] = useState(true);
  const [comparing, setComparing] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getCompanies();
        setCompanies(data);
        if (data.length > 0) {
          setSelectedForCompare([data[0].name, data[1]?.name].filter(Boolean));
        }
      } catch (err) {
        console.error("Failed to load companies:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const toggleSelect = (name) => {
    if (selectedForCompare.includes(name)) {
      setSelectedForCompare(selectedForCompare.filter((n) => n !== name));
    } else {
      if (selectedForCompare.length >= 4) return;
      setSelectedForCompare([...selectedForCompare, name]);
    }
  };

  const handleRunCompare = async () => {
    if (selectedForCompare.length === 0) return;
    setComparing(true);
    try {
      const data = await compareCompanies(selectedForCompare);
      setComparisonMatrix(data.matrix);
    } catch (err) {
      console.error("Comparison error:", err);
    } finally {
      setComparing(false);
    }
  };

  if (loading) return <LoadingSpinner label="Loading Company Placement Directory..." size="lg" />;

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center space-x-2">
          <Building2 className="w-6 h-6 text-emerald-600" />
          <span>Company Drives & Requirement Comparison</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Explore campus recruiters or select up to 4 companies for a side-by-side comparison matrix.
        </p>
      </div>

      {/* Compare Control Bar */}
      <Card className="p-4 bg-emerald-50/50 border-emerald-200">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <div>
            <span className="font-bold text-slate-900 text-sm">Side-by-Side Matrix Compare</span>
            <p className="text-slate-600 text-[11px] mt-0.5">
              Selected ({selectedForCompare.length}/4): {selectedForCompare.join(', ') || 'None'}
            </p>
          </div>
          <Button onClick={handleRunCompare} disabled={selectedForCompare.length === 0 || comparing} size="sm">
            <Columns className="w-4 h-4 mr-1.5" />
            <span>{comparing ? 'Generating Matrix...' : 'Compare Selected Companies'}</span>
          </Button>
        </div>
      </Card>

      {/* Side-by-Side Matrix Table */}
      {comparisonMatrix && (
        <Card className="overflow-x-auto">
          <h3 className="font-bold text-slate-900 text-base mb-3">Side-by-Side Requirement Comparison Matrix</h3>
          <table className="min-w-full text-xs text-left">
            <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
              <tr>
                {comparisonMatrix.headers.map((h, i) => (
                  <th key={i} className="px-4 py-3">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {comparisonMatrix.rows.map((row, idx) => (
                <tr key={idx} className={row.feature.includes("Status") ? "bg-slate-50 font-bold" : "hover:bg-slate-50/50"}>
                  <td className="px-4 py-3 font-semibold text-slate-900">{row.feature}</td>
                  {row.values.map((val, vIdx) => (
                    <td key={vIdx} className="px-4 py-3">
                      {val === "Eligible" ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">
                          <Check className="w-3.5 h-3.5 mr-1" /> Eligible
                        </span>
                      ) : val === "Not Eligible" ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-bold">
                          <X className="w-3.5 h-3.5 mr-1" /> Not Eligible
                        </span>
                      ) : (
                        <span className="text-slate-700">{val}</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}

      {/* Company Cards Directory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {companies.map((company) => {
          const isSelected = selectedForCompare.includes(company.name);

          return (
            <Card key={company.id} className={isSelected ? 'border-emerald-500 ring-2 ring-emerald-500/10' : ''}>
              
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">{company.name}</h3>
                  <div className="flex items-center space-x-2 mt-1">
                    <Badge variant="purple">Offered CTC: {company.ctc}</Badge>
                    <Badge variant="slate">Source: {company.doc_source}</Badge>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => toggleSelect(company.name)}
                  className="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500 cursor-pointer mt-1"
                />
              </div>

              {/* Requirement Summary Table */}
              <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="text-slate-500 block text-[11px]">Min CGPA</span>
                  <span className="font-bold text-slate-900">{company.min_cgpa ?? 'No Min'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[11px]">Max Active Backlogs</span>
                  <span className="font-bold text-slate-900">{company.max_backlogs ?? 'Not Restricted'}</span>
                </div>
              </div>

              {/* Eligible Branches */}
              <div className="mt-3 text-xs">
                <span className="text-slate-500 block text-[11px] mb-1">Eligible Branches</span>
                <div className="flex flex-wrap gap-1">
                  {company.eligible_branches.map((b, bIdx) => (
                    <span key={bIdx} className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-[11px]">
                      {b}
                    </span>
                  ))}
                </div>
              </div>

              {/* Selection Process */}
              {company.selection_process && (
                <div className="mt-3 text-xs">
                  <span className="text-slate-500 block text-[11px] mb-1">Selection Rounds</span>
                  <p className="text-slate-600 text-[11px]">
                    {company.selection_process.join(' → ')}
                  </p>
                </div>
              )}

            </Card>
          );
        })}
      </div>

    </div>
  );
}
