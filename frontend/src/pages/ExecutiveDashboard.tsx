import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { reportClient, ExecutiveDashboardResponse } from '../api/reportClient';
import { ShieldAlert, Activity, ActivitySquare, Loader2, TrendingUp, LayoutDashboard, CheckCircle2 } from 'lucide-react';

export default function ExecutiveDashboard() {
  const { reportId } = useParams();
    const [isLoading, setIsLoading] = useState(true);
  const [dashboardResult, setDashboardResult] = useState<ExecutiveDashboardResponse | null>(null);

  useEffect(() => {
    async function fetchDashboard() {
      setIsLoading(true);
      let targetReportId = reportId;
      
      // If no reportId in URL, check localStorage
      if (!targetReportId) {
        targetReportId = localStorage.getItem('latestReportId') || undefined;
      }
      
      // If still no reportId, ask API for the latest
      if (!targetReportId) {
        const latestRes = await reportClient.getLatestReport();
        if (latestRes.success && latestRes.report_id) {
          targetReportId = latestRes.report_id;
        }
      }
      
      if (!targetReportId) {
        setDashboardResult(null);
        setIsLoading(false);
        return;
      }
      
      const res = await reportClient.getExecutiveDashboard(targetReportId);
      setDashboardResult(res);
      setIsLoading(false);
    }
    
    fetchDashboard();
  }, [reportId]);

  if (isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center min-h-[500px]">
        <Loader2 className="animate-spin text-indigo-500 mb-4" size={48} />
        <p className="text-slate-400 text-lg">Compiling Executive Intelligence...</p>
      </div>
    );
  }

  // Empty State
  if (!dashboardResult || !dashboardResult.success) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center min-h-[600px] px-6 text-center">
        <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center mb-6 border border-slate-700">
          <LayoutDashboard className="text-slate-500" size={40} />
        </div>
        <h2 className="text-3xl font-bold text-white mb-4">No Analysis Found</h2>
        <p className="text-slate-400 max-w-md mb-8">
          We couldn't locate an active coverage report. Please upload a coverage.xml file and run the analysis workflow to generate the Executive Dashboard.
        </p>
        <Link 
          to="/upload" 
          className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold shadow-lg transition-colors"
        >
          Start Analysis
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 lg:p-8 space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-3xl font-bold text-white flex items-center space-x-3">
          <LayoutDashboard className="text-indigo-500" />
          <span>Executive Intelligence Dashboard</span>
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className={`col-span-1 md:col-span-3 bg-gradient-to-br ${
            dashboardResult.status === 'EXCELLENT' ? 'from-emerald-900/40 to-emerald-800/20 border-emerald-500/50' :
            dashboardResult.status === 'GOOD' ? 'from-blue-900/40 to-blue-800/20 border-blue-500/50' :
            dashboardResult.status === 'NEEDS ATTENTION' ? 'from-orange-900/40 to-orange-800/20 border-orange-500/50' :
            'from-red-900/40 to-red-800/20 border-red-500/50'
          } border rounded-2xl p-8 flex items-center justify-between shadow-2xl`}>
          <div>
            <h3 className="text-xl font-medium text-slate-300 mb-2 tracking-wide">Project Health Score</h3>
            <div className="flex items-baseline space-x-4">
              <span className="text-6xl font-black text-white">{dashboardResult.project_health_score}</span>
              <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-widest uppercase ${
                dashboardResult.status === 'EXCELLENT' ? 'bg-emerald-500/20 text-emerald-300' :
                dashboardResult.status === 'GOOD' ? 'bg-blue-500/20 text-blue-300' :
                dashboardResult.status === 'NEEDS ATTENTION' ? 'bg-orange-500/20 text-orange-300' :
                'bg-red-500/20 text-red-300'
              }`}>
                {dashboardResult.status}
              </span>
            </div>
          </div>
          <div className="hidden md:block w-1/3 text-slate-300 text-sm whitespace-pre-line leading-relaxed border-l border-slate-700/50 pl-6">
            {dashboardResult.executive_summary}
          </div>
        </div>

        {/* Sub-Health Cards */}
        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6 hover:border-indigo-500/30 transition-colors">
          <h4 className="text-slate-400 font-medium mb-4 flex items-center"><ActivitySquare size={16} className="mr-2 text-indigo-400"/> Coverage Health</h4>
          <div className="text-3xl font-bold text-white mb-4">{dashboardResult.coverage.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-400">Current</span> <span className="text-white font-medium">{dashboardResult.coverage.current_coverage}%</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Potential</span> <span className="text-emerald-400 font-medium">{dashboardResult.coverage.potential_coverage}%</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Improvement</span> <span className="text-pink-400 font-medium">+{dashboardResult.coverage.improvement_potential}%</span></div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6 hover:border-rose-500/30 transition-colors">
          <h4 className="text-slate-400 font-medium mb-4 flex items-center"><ShieldAlert size={16} className="mr-2 text-rose-400"/> Risk Health</h4>
          <div className="text-3xl font-bold text-white mb-4">{dashboardResult.risk.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-400">High Risk Funcs</span> <span className="text-rose-400 font-medium">{dashboardResult.risk.high_risk_functions}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Project Risk</span> <span className="text-white font-medium">{dashboardResult.risk.project_risk_score}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Highest Risk</span> <span className="text-slate-300 font-mono truncate w-24 text-right" title={dashboardResult.highest_risk_function}>{dashboardResult.highest_risk_function}</span></div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6 hover:border-amber-500/30 transition-colors">
          <h4 className="text-slate-400 font-medium mb-4 flex items-center"><Activity size={16} className="mr-2 text-amber-400"/> Dependency Health</h4>
          <div className="text-3xl font-bold text-white mb-4">{dashboardResult.dependencies.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-400">Critical Deps</span> <span className="text-amber-400 font-medium">{dashboardResult.dependencies.critical_dependencies}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Max Impact Radius</span> <span className="text-white font-medium">{dashboardResult.dependencies.largest_impact_radius}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Largest Impact</span> <span className="text-slate-300 font-mono truncate w-24 text-right" title={dashboardResult.largest_impact_function}>{dashboardResult.largest_impact_function}</span></div>
          </div>
        </div>

        {/* Recommendations and Priorities */}
        <div className="col-span-1 md:col-span-2 bg-slate-900 border border-slate-700/50 rounded-xl p-6">
          <h4 className="text-slate-200 font-medium mb-4 flex items-center space-x-2">
            <CheckCircle2 className="text-emerald-400" size={18} />
            <span>Executive Recommendations</span>
          </h4>
          <ul className="space-y-3">
            {dashboardResult.recommendations?.map((rec: string, i: number) => (
              <li key={i} className="flex items-start space-x-3 text-slate-300 text-sm bg-slate-800/50 p-4 rounded-lg border border-slate-700/50 hover:bg-slate-800 transition-colors">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span className="leading-relaxed">{rec}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="col-span-1 bg-slate-900 border border-slate-700/50 rounded-xl p-6 flex flex-col">
          <h4 className="text-slate-200 font-medium mb-4 flex items-center space-x-2">
            <TrendingUp className="text-pink-400" size={18} />
            <span>Top Testing Priorities</span>
          </h4>
          <div className="space-y-3 text-sm flex-1">
            {dashboardResult.testing.top_5_functions?.map((f: any, i: number) => (
              <div key={i} className="flex justify-between items-center bg-slate-800/30 p-3 rounded-lg border border-slate-700/30 hover:border-pink-500/30 transition-colors">
                <span className="text-slate-300 font-mono truncate max-w-[140px]" title={f.name}>{i+1}. {f.name}</span>
                <span className="text-white font-bold bg-slate-800 px-2 py-1 rounded">{f.score}</span>
              </div>
            ))}
            {(!dashboardResult.testing.top_5_functions || dashboardResult.testing.top_5_functions.length === 0) && (
              <div className="text-slate-500 text-center py-4">No priority functions identified</div>
            )}
          </div>
        </div>
        
        {/* Trends Placeholders */}
        <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500 min-h-[120px]">
          <TrendingUp size={24} className="mb-2 opacity-50" />
          <span className="text-sm font-medium">Coverage Trend Analytics</span>
          <span className="text-xs mt-1">Coming in next update</span>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500 min-h-[120px]">
          <ShieldAlert size={24} className="mb-2 opacity-50" />
          <span className="text-sm font-medium">Risk Trend Analytics</span>
          <span className="text-xs mt-1">Coming in next update</span>
        </div>
        <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500 min-h-[120px]">
          <ActivitySquare size={24} className="mb-2 opacity-50" />
          <span className="text-sm font-medium">Quality Trend Analytics</span>
          <span className="text-xs mt-1">Coming in next update</span>
        </div>

      </div>
    </div>
  );
}
