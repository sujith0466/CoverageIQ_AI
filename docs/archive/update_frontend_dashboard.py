import re

with open("frontend/src/pages/UploadReport.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Imports
if "ExecutiveDashboardResponse" not in content:
    content = content.replace(
        "DependencyAnalysisResponse, PredictionAnalysisResponse, GapFunctionData } from '../api/reportClient';",
        "DependencyAnalysisResponse, PredictionAnalysisResponse, ExecutiveDashboardResponse, GapFunctionData } from '../api/reportClient';"
    )

if "const [isLoadingDashboard" not in content:
    # State
    state_injection = """  const [isPredictingCoverage, setIsPredictingCoverage] = useState(false);
  const [predictionResult, setPredictionResult] = useState<PredictionAnalysisResponse | null>(null);

  const [isLoadingDashboard, setIsLoadingDashboard] = useState(false);
  const [dashboardResult, setDashboardResult] = useState<ExecutiveDashboardResponse | null>(null);
  const [viewMode, setViewMode] = useState<'workflow' | 'dashboard'>('workflow');
"""
    content = content.replace(
        "  const [isPredictingCoverage, setIsPredictingCoverage] = useState(false);\n  const [predictionResult, setPredictionResult] = useState<PredictionAnalysisResponse | null>(null);",
        state_injection
    )

if "handleLoadDashboard" not in content:
    handler_injection = """  const handlePredictCoverage = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsPredictingCoverage(true);
    setPredictionResult(null);

    const res = await reportClient.predictCoverage(uploadResult.report_id);
    setPredictionResult(res);
    setIsPredictingCoverage(false);
  };

  const handleLoadDashboard = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsLoadingDashboard(true);
    const res = await reportClient.getExecutiveDashboard(uploadResult.report_id);
    setDashboardResult(res);
    setViewMode('dashboard');
    setIsLoadingDashboard(false);
  };
"""
    content = content.replace(
        "  const handlePredictCoverage = async () => {\n    if (!uploadResult || !uploadResult.report_id) return;\n    setIsPredictingCoverage(true);\n    setPredictionResult(null);\n\n    const res = await reportClient.predictCoverage(uploadResult.report_id);\n    setPredictionResult(res);\n    setIsPredictingCoverage(false);\n  };",
        handler_injection
    )

if "LayoutDashboard" not in content:
    content = content.replace(
        "import { AlertCircle, ShieldAlert, FileCode2, Play, Activity, ActivitySquare, Plus, Loader2, TrendingUp } from 'lucide-react';",
        "import { AlertCircle, ShieldAlert, FileCode2, Play, Activity, ActivitySquare, Plus, Loader2, TrendingUp, LayoutDashboard, ArrowLeft, CheckCircle2 } from 'lucide-react';"
    )

if "Dashboard View" not in content:
    dashboard_view = """
      {viewMode === 'dashboard' && dashboardResult?.success && (
        <div className="max-w-6xl mx-auto space-y-6">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-4">
              <button onClick={() => setViewMode('workflow')} className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors">
                <ArrowLeft size={20} />
              </button>
              <h2 className="text-3xl font-bold text-white flex items-center space-x-3">
                <LayoutDashboard className="text-indigo-500" />
                <span>Executive Intelligence Dashboard</span>
              </h2>
            </div>
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
              <div className="hidden md:block w-1/3 text-slate-300 text-sm whitespace-pre-line leading-relaxed">
                {dashboardResult.executive_summary}
              </div>
            </div>

            {/* Sub-Health Cards */}
            <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6">
              <h4 className="text-slate-400 font-medium mb-4 flex items-center"><ActivitySquare size={16} className="mr-2 text-indigo-400"/> Coverage Health</h4>
              <div className="text-3xl font-bold text-white mb-4">{dashboardResult.coverage.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">Current</span> <span className="text-white font-medium">{dashboardResult.coverage.current_coverage}%</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Potential</span> <span className="text-emerald-400 font-medium">{dashboardResult.coverage.potential_coverage}%</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Improvement</span> <span className="text-pink-400 font-medium">+{dashboardResult.coverage.improvement_potential}%</span></div>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6">
              <h4 className="text-slate-400 font-medium mb-4 flex items-center"><ShieldAlert size={16} className="mr-2 text-rose-400"/> Risk Health</h4>
              <div className="text-3xl font-bold text-white mb-4">{dashboardResult.risk.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">High Risk Funcs</span> <span className="text-rose-400 font-medium">{dashboardResult.risk.high_risk_functions}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Project Risk</span> <span className="text-white font-medium">{dashboardResult.risk.project_risk_score}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Highest Risk</span> <span className="text-slate-300 font-mono truncate w-24 text-right" title={dashboardResult.highest_risk_function}>{dashboardResult.highest_risk_function}</span></div>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6">
              <h4 className="text-slate-400 font-medium mb-4 flex items-center"><Activity size={16} className="mr-2 text-amber-400"/> Dependency Health</h4>
              <div className="text-3xl font-bold text-white mb-4">{dashboardResult.dependencies.health_score} <span className="text-sm font-normal text-slate-500">/ 100</span></div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">Critical Deps</span> <span className="text-amber-400 font-medium">{dashboardResult.dependencies.critical_dependencies}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Max Impact Radius</span> <span className="text-white font-medium">{dashboardResult.dependencies.largest_impact_radius}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Largest Impact</span> <span className="text-slate-300 font-mono truncate w-24 text-right" title={dashboardResult.largest_impact_function}>{dashboardResult.largest_impact_function}</span></div>
              </div>
            </div>

            <div className="col-span-1 md:col-span-2 bg-slate-900 border border-slate-700/50 rounded-xl p-6">
              <h4 className="text-slate-200 font-medium mb-4 flex items-center space-x-2">
                <CheckCircle2 className="text-emerald-400" size={18} />
                <span>Executive Recommendations</span>
              </h4>
              <ul className="space-y-3">
                {dashboardResult.recommendations?.map((rec: string, i: number) => (
                  <li key={i} className="flex items-start space-x-3 text-slate-300 text-sm bg-slate-800/50 p-3 rounded-lg border border-slate-700/50">
                    <span className="text-emerald-500 mt-0.5">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="col-span-1 bg-slate-900 border border-slate-700/50 rounded-xl p-6">
              <h4 className="text-slate-200 font-medium mb-4 flex items-center space-x-2">
                <TrendingUp className="text-pink-400" size={18} />
                <span>Top Testing Priorities</span>
              </h4>
              <div className="space-y-2 text-sm">
                {dashboardResult.testing.top_5_functions?.map((f: any, i: number) => (
                  <div key={i} className="flex justify-between items-center bg-slate-800/30 p-2 rounded border border-slate-700/30">
                    <span className="text-slate-300 font-mono truncate w-32" title={f.name}>{i+1}. {f.name}</span>
                    <span className="text-white font-bold">{f.score}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Trends Placeholders */}
            <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500">
              <TrendingUp size={24} className="mb-2 opacity-50" />
              <span className="text-sm font-medium">Coverage Trend Analytics</span>
              <span className="text-xs mt-1">Coming in next update</span>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500">
              <ShieldAlert size={24} className="mb-2 opacity-50" />
              <span className="text-sm font-medium">Risk Trend Analytics</span>
              <span className="text-xs mt-1">Coming in next update</span>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500">
              <ActivitySquare size={24} className="mb-2 opacity-50" />
              <span className="text-sm font-medium">Quality Trend Analytics</span>
              <span className="text-xs mt-1">Coming in next update</span>
            </div>

          </div>
        </div>
      )}
"""
    content = content.replace(
        "    <div className=\"min-h-screen bg-slate-950 p-8\">",
        "    <div className=\"min-h-screen bg-slate-950 p-8\">" + dashboard_view
    )

if "viewMode === 'workflow' &&" not in content:
    content = content.replace(
        "    <div className=\"min-h-screen bg-slate-950 p-8\">\n" + dashboard_view + "\n      <div className=\"max-w-4xl mx-auto space-y-6\">\n        <div className=\"flex items-center justify-between mb-8\">",
        "    <div className=\"min-h-screen bg-slate-950 p-8\">\n" + dashboard_view + "\n      {viewMode === 'workflow' && (<div className=\"max-w-4xl mx-auto space-y-6\">\n        <div className=\"flex items-center justify-between mb-8\">"
    )
    # find the end of max-w-4xl div to close the bracket
    # It ends right before the last </div>
    idx = content.rfind("</div>")
    idx = content.rfind("</div>", 0, idx)
    content = content[:idx] + "      </div>\n      )}\n" + content[idx:]

if "Load Executive Dashboard" not in content:
    dash_button = """
            {predictionResult?.success && (
              <button
                onClick={handleLoadDashboard}
                disabled={isLoadingDashboard}
                className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md font-medium transition-colors disabled:opacity-50"
              >
                {isLoadingDashboard ? <Loader2 className="animate-spin" size={20} /> : <LayoutDashboard size={20} />}
                <span>Executive Dashboard</span>
              </button>
            )}"""
    
    # insert before <button onClick={handleUpload}
    content = content.replace(
        "          <button\n            onClick={handleUpload}",
        dash_button + "\n          <button\n            onClick={handleUpload}"
    )

with open("frontend/src/pages/UploadReport.tsx", "w", encoding="utf-8") as f:
    f.write(content)
