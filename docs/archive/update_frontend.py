import re

with open("frontend/src/pages/UploadReport.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Imports
if "PredictionAnalysisResponse" not in content:
    content = content.replace(
        "DependencyAnalysisResponse, GapFunctionData } from '../api/reportClient';",
        "DependencyAnalysisResponse, PredictionAnalysisResponse, GapFunctionData } from '../api/reportClient';"
    )

if "const [isPredictingCoverage" not in content:
    # State
    state_injection = """  const [isAnalyzingDependencies, setIsAnalyzingDependencies] = useState(false);
  const [dependencyResult, setDependencyResult] = useState<DependencyAnalysisResponse | null>(null);
  const [selectedDepFunction, setSelectedDepFunction] = useState<any | null>(null);
  
  const [isPredictingCoverage, setIsPredictingCoverage] = useState(false);
  const [predictionResult, setPredictionResult] = useState<PredictionAnalysisResponse | null>(null);
"""
    content = content.replace(
        "  const [isAnalyzingDependencies, setIsAnalyzingDependencies] = useState(false);\n  const [dependencyResult, setDependencyResult] = useState<DependencyAnalysisResponse | null>(null);\n  const [selectedDepFunction, setSelectedDepFunction] = useState<any | null>(null);",
        state_injection
    )

if "setPredictionResult(null);" not in content.replace("setIsPredictingCoverage", ""):
    # Reset state
    content = content.replace("setDependencyResult(null);", "setDependencyResult(null);\n    setPredictionResult(null);")

if "handlePredictCoverage" not in content:
    # handlePredictCoverage
    handler_injection = """  const handleAnalyzeDependencies = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsAnalyzingDependencies(true);
    setDependencyResult(null);
    setPredictionResult(null);

    const res = await reportClient.analyzeDependencies(uploadResult.report_id);
    setDependencyResult(res);
    setIsAnalyzingDependencies(false);
  };

  const handlePredictCoverage = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsPredictingCoverage(true);
    setPredictionResult(null);

    const res = await reportClient.predictCoverage(uploadResult.report_id);
    setPredictionResult(res);
    setIsPredictingCoverage(false);
  };
"""
    content = content.replace(
        "  const handleAnalyzeDependencies = async () => {\n    if (!uploadResult || !uploadResult.report_id) return;\n    setIsAnalyzingDependencies(true);\n    setDependencyResult(null);\n    setPredictionResult(null);\n\n    const res = await reportClient.analyzeDependencies(uploadResult.report_id);\n    setDependencyResult(res);\n    setIsAnalyzingDependencies(false);\n  };",
        handler_injection
    )
    # Also handle if it hasn't been replaced yet with setPredictionResult(null) inside handleAnalyzeDependencies:
    content = content.replace(
        "  const handleAnalyzeDependencies = async () => {\n    if (!uploadResult || !uploadResult.report_id) return;\n    setIsAnalyzingDependencies(true);\n    setDependencyResult(null);\n\n    const res = await reportClient.analyzeDependencies(uploadResult.report_id);\n    setDependencyResult(res);\n    setIsAnalyzingDependencies(false);\n  };",
        handler_injection
    )

if "TrendingUp" not in content:
    content = content.replace(
        "import { AlertCircle, ShieldAlert, FileCode2, Play, Activity, ActivitySquare, Plus, Loader2 } from 'lucide-react';",
        "import { AlertCircle, ShieldAlert, FileCode2, Play, Activity, ActivitySquare, Plus, Loader2, TrendingUp } from 'lucide-react';"
    )

if "Predict Coverage Optimization" not in content:
    # Dependency Dashboard title + button
    dep_title_old = """                        <h3 className="text-lg font-semibold text-white mb-6 flex items-center space-x-2">
                          <Activity className="text-indigo-400" />
                          <span>Dependency & Impact Intelligence</span>
                        </h3>"""
    dep_title_new = """                        <div className="flex items-center justify-between mb-6">
                          <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
                            <Activity className="text-indigo-400" />
                            <span>Dependency & Impact Intelligence</span>
                          </h3>
                          {!predictionResult && (
                            <button
                              onClick={handlePredictCoverage}
                              disabled={isPredictingCoverage}
                              className="flex items-center space-x-2 px-4 py-2 bg-pink-600 hover:bg-pink-500 text-white rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                            >
                              {isPredictingCoverage ? <Loader2 className="animate-spin" size={16} /> : <TrendingUp size={16} />}
                              <span>Predict Coverage Optimization</span>
                            </button>
                          )}
                        </div>"""
    content = content.replace(dep_title_old, dep_title_new)

if "Coverage Optimization Engine" not in content:
    prediction_dashboard = """                    {/* Prediction Dashboard */}
                    {predictionResult?.success && (
                      <div className="mt-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <h3 className="text-lg font-semibold text-white mb-6 flex items-center space-x-2">
                          <TrendingUp className="text-pink-400" />
                          <span>Coverage Optimization Engine</span>
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                          <div className="bg-slate-900 border border-slate-700 rounded-xl p-5">
                            <div className="text-slate-400 text-sm font-semibold mb-1 tracking-wider">Current Coverage</div>
                            <div className="text-3xl font-bold text-white mt-1">{predictionResult.current_coverage}%</div>
                          </div>
                          <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5">
                            <div className="text-emerald-400 text-sm font-semibold mb-1 tracking-wider">Potential Coverage</div>
                            <div className="text-3xl font-bold text-emerald-400 mt-1">{predictionResult.potential_coverage}%</div>
                          </div>
                          <div className="bg-slate-900 border border-pink-500/30 rounded-xl p-5">
                            <div className="text-pink-400 text-sm font-semibold mb-1 tracking-wider">Improvement Potential</div>
                            <div className="text-3xl font-bold text-pink-400 mt-1">+{predictionResult.improvement_potential}%</div>
                          </div>
                          <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5">
                            <div className="text-indigo-400 text-sm font-semibold mb-1 tracking-wider leading-tight">Highest Gain</div>
                            <div className="text-3xl font-bold text-white mt-1">+{predictionResult.highest_gain}%</div>
                            <div className="text-[10px] text-slate-400 mt-1 truncate" title={predictionResult.highest_gain_function}>{predictionResult.highest_gain_function}</div>
                          </div>
                        </div>

                        <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden mb-6">
                          <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
                            <h4 className="font-medium text-slate-200">Recommended Test Priority</h4>
                          </div>
                          <div className="max-h-[500px] overflow-y-auto">
                            <table className="w-full text-left text-sm text-slate-300">
                              <thead className="text-xs uppercase bg-slate-800/80 text-slate-400 sticky top-0 z-10">
                                <tr>
                                  <th className="px-6 py-4 w-12 text-center">#</th>
                                  <th className="px-6 py-4">Function</th>
                                  <th className="px-6 py-4">Coverage Gain</th>
                                  <th className="px-6 py-4">Priority Score</th>
                                  <th className="px-6 py-4">Priority Category</th>
                                  <th className="px-6 py-4">Recommendation</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-slate-700/50">
                                {predictionResult.recommendations?.map((func: any) => (
                                  <tr key={func.id} className="hover:bg-slate-800/40 transition-colors">
                                    <td className="px-6 py-4 font-mono font-bold text-slate-500 text-center">{func.recommended_test_order}</td>
                                    <td className="px-6 py-4 font-medium text-slate-200">{func.name}</td>
                                    <td className="px-6 py-4 font-mono text-emerald-400 font-bold">+{func.potential_coverage_gain}%</td>
                                    <td className="px-6 py-4 font-mono font-bold text-white">{func.test_priority_score}</td>
                                    <td className="px-6 py-4">
                                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase border ${
                                        func.recommendation_category === 'TEST IMMEDIATELY' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                                        func.recommendation_category === 'HIGH VALUE' ? 'bg-orange-500/10 text-orange-400 border-orange-500/20' :
                                        func.recommendation_category === 'MEDIUM VALUE' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                                        'bg-slate-500/10 text-slate-400 border-slate-500/20'
                                      }`}>
                                        {func.recommendation_category}
                                      </span>
                                    </td>
                                    <td className="px-6 py-4 text-xs max-w-[300px] truncate text-slate-400" title={func.recommendation}>{func.recommendation}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    )}"""

    end_of_modal = """                        </div>
                      </div>
                    )}"""

    if end_of_modal in content:
        content = content.replace(end_of_modal, end_of_modal + "\n" + prediction_dashboard)

with open("frontend/src/pages/UploadReport.tsx", "w", encoding="utf-8") as f:
    f.write(content)
