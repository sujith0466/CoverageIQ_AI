import re

landing_page_content = """import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Activity, GitCommit, PlayCircle, BarChart3, TrendingUp, FolderSearch, Zap } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex-1 flex flex-col items-center">
      {/* Hero Section */}
      <section className="w-full py-20 px-6 flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 to-slate-950 text-center border-b border-slate-800">
        <h1 className="text-6xl font-extrabold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 drop-shadow-sm">
          CoverageIQ AI
        </h1>
        <p className="text-2xl text-slate-300 max-w-3xl mb-10 font-light">
          Enterprise Coverage Intelligence & AI Test Generation
        </p>
        <div className="flex items-center justify-center space-x-6">
          <Link 
            to="/upload" 
            className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-lg shadow-lg shadow-indigo-500/25 transition-all flex items-center space-x-2"
          >
            <PlayCircle size={24} />
            <span>Start Analysis</span>
          </Link>
          <Link 
            to="/dashboard" 
            className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold text-lg border border-slate-700 transition-all flex items-center space-x-2"
          >
            <BarChart3 size={24} className="text-slate-400" />
            <span>View Dashboard</span>
          </Link>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className="w-full max-w-7xl mx-auto py-24 px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Transform Your Testing Strategy</h2>
          <p className="text-slate-400 text-lg">CoverageIQ turns raw XML reports into actionable engineering intelligence.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl hover:border-blue-500/50 transition-colors">
            <div className="p-3 bg-blue-500/10 w-fit rounded-lg mb-6">
              <FolderSearch className="text-blue-400" size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AST Gap Detection</h3>
            <p className="text-slate-400 leading-relaxed">
              We parse your codebase's Abstract Syntax Tree (AST) to map XML metrics directly to real Python functions, instantly identifying untested logic.
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl hover:border-rose-500/50 transition-colors">
            <div className="p-3 bg-rose-500/10 w-fit rounded-lg mb-6">
              <ShieldAlert className="text-rose-400" size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Risk & Dependency Engine</h3>
            <p className="text-slate-400 leading-relaxed">
              Calculates real-time Risk Scores and Dependency Impact Radii for every uncovered function, so you know exactly what breaks if a module fails.
            </p>
          </div>
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl hover:border-emerald-500/50 transition-colors">
            <div className="p-3 bg-emerald-500/10 w-fit rounded-lg mb-6">
              <Zap className="text-emerald-400" size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">AI Test Generation</h3>
            <p className="text-slate-400 leading-relaxed">
              Dynamically invokes LLMs to author complete, executable unit tests for your highest-risk gaps, drastically accelerating coverage gains.
            </p>
          </div>
        </div>
      </section>

      {/* Workflow Visualization */}
      <section className="w-full bg-slate-900 py-24 px-6 border-t border-slate-800">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-16">The Intelligence Workflow</h2>
          <div className="flex flex-col md:flex-row items-center justify-between space-y-8 md:space-y-0">
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center text-xl font-bold text-white mb-4">1</div>
              <p className="font-medium text-slate-300">Upload XML</p>
            </div>
            <GitCommit className="text-slate-700 hidden md:block" size={32} />
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center text-xl font-bold text-white mb-4">2</div>
              <p className="font-medium text-slate-300">Scan Codebase</p>
            </div>
            <GitCommit className="text-slate-700 hidden md:block" size={32} />
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-indigo-500 flex items-center justify-center text-xl font-bold text-indigo-400 mb-4 shadow-[0_0_15px_rgba(99,102,241,0.5)]">3</div>
              <p className="font-medium text-indigo-300">Predict ROI</p>
            </div>
            <GitCommit className="text-slate-700 hidden md:block" size={32} />
            <div className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-full bg-slate-800 border-2 border-emerald-500 flex items-center justify-center text-xl font-bold text-emerald-400 mb-4 shadow-[0_0_15px_rgba(16,185,129,0.5)]">4</div>
              <p className="font-medium text-emerald-300">Dashboard</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
"""

with open("frontend/src/pages/LandingPage.tsx", "w", encoding="utf-8") as f:
    f.write(landing_page_content)


executive_dashboard_content = """import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { reportClient, ExecutiveDashboardResponse } from '../api/reportClient';
import { ShieldAlert, Activity, ActivitySquare, Loader2, TrendingUp, LayoutDashboard, CheckCircle2 } from 'lucide-react';

export default function ExecutiveDashboard() {
  const { reportId } = useParams();
  const navigate = useNavigate();
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
"""

with open("frontend/src/pages/ExecutiveDashboard.tsx", "w", encoding="utf-8") as f:
    f.write(executive_dashboard_content)


app_content = """import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import UploadReport from './pages/UploadReport';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import { Activity, Upload, LayoutDashboard, Home } from 'lucide-react';

function Navigation() {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path || (path === '/dashboard' && location.pathname.startsWith('/dashboard'));

  return (
    <nav className="bg-slate-950 border-b border-slate-800 p-4 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 text-white hover:opacity-80 transition-opacity">
          <Activity className="text-emerald-400" />
          <span className="font-bold text-xl tracking-tight">CoverageIQ</span>
        </Link>
        <div className="flex space-x-8">
          <Link 
            to="/" 
            className={`font-medium transition-colors flex items-center space-x-1.5 ${isActive('/') ? 'text-emerald-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Home size={18} />
            <span>Home</span>
          </Link>
          <Link 
            to="/upload" 
            className={`font-medium transition-colors flex items-center space-x-1.5 ${isActive('/upload') ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Upload size={18} />
            <span>Upload</span>
          </Link>
          <Link 
            to="/dashboard" 
            className={`font-medium transition-colors flex items-center space-x-1.5 ${isActive('/dashboard') ? 'text-pink-400' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-950 flex flex-col font-sans">
        <Navigation />
        <main className="flex-1 flex flex-col w-full">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/upload" element={<UploadReport />} />
            <Route path="/dashboard" element={<ExecutiveDashboard />} />
            <Route path="/dashboard/:reportId" element={<ExecutiveDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
"""

with open("frontend/src/App.tsx", "w", encoding="utf-8") as f:
    f.write(app_content)
