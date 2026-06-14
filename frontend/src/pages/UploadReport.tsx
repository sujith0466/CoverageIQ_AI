import React, { useState, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Copy, Download, LayoutDashboard, TrendingUp, CheckCircle, AlertCircle, Loader2, PieChart, FileText, List, Activity, Code, FolderSearch, ShieldAlert, Target, ShieldCheck, Filter, Bot, PlayCircle, X } from 'lucide-react';
import { reportClient, UploadResponse, AnalyzeResponse, ScanResponse, DetectGapsResponse, GenerateTestsResponse, RiskAnalysisResponse, DependencyAnalysisResponse, PredictionAnalysisResponse, } from '../api/reportClient';

type FilterType = 'ALL' | 'COVERED' | 'PARTIAL' | 'UNCOVERED';

export default function UploadReport() {
  const navigate = useNavigate();
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  
  // Loading states
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [isDetectingGaps, setIsDetectingGaps] = useState(false);
  const [isGeneratingTests, setIsGeneratingTests] = useState(false);
  
  // Form state
  const [scanPath, setScanPath] = useState('');
  const [gapFilter, setGapFilter] = useState<FilterType>('ALL');
  const [selectedFunctions, setSelectedFunctions] = useState<Set<string>>(new Set());
  
  // Result states
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [analyzeResult, setAnalyzeResult] = useState<AnalyzeResponse | null>(null);
  const [scanResult, setScanResult] = useState<ScanResponse | null>(null);
  const [gapResult, setGapResult] = useState<DetectGapsResponse | null>(null);
  const [testResult, setTestResult] = useState<GenerateTestsResponse | null>(null);
  
  const [isAnalyzingRisks, setIsAnalyzingRisks] = useState(false);
  const [riskResult, setRiskResult] = useState<RiskAnalysisResponse | null>(null);
  const [selectedRiskFunction, setSelectedRiskFunction] = useState<any | null>(null);
    
  const [isAnalyzingDependencies, setIsAnalyzingDependencies] = useState(false);
  const [dependencyResult, setDependencyResult] = useState<DependencyAnalysisResponse | null>(null);
    
    const [predictionResult, setPredictionResult] = useState<PredictionAnalysisResponse | null>(null);





  

  const handleLoadDashboard = () => navigate('/dashboard');
  
  const handleAnalyzeDependencies = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsAnalyzingDependencies(true);
    setDependencyResult(null);
    try {
      const res = await reportClient.analyzeDependencies(uploadResult.report_id);
      setDependencyResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzingDependencies(false);
    }
  };
  
  const inputRef = useRef<HTMLInputElement>(null);


  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    setUploadResult(null);
    setAnalyzeResult(null);
    setScanResult(null);
    setGapResult(null);
    setTestResult(null);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);
    if (selectedFile.type !== 'text/xml' && !selectedFile.name.endsWith('.xml')) {
      setUploadResult({ success: false, message: 'Only XML files are allowed.' });
      setFile(null);
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      setUploadResult({ success: false, message: 'File exceeds the 10 MB limit.' });
      setFile(null);
      return;
    }
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setUploadResult(null);
    setAnalyzeResult(null);
    setScanResult(null);
    setGapResult(null);
    setTestResult(null);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);

    const res = await reportClient.uploadReport(file);
    setUploadResult(res);
    setIsUploading(false);
    
    if (res.success && res.report_id) {
      localStorage.setItem('latestReportId', res.report_id);
      setFile(null);
    }
  };

  const handleAnalyze = async () => {
    console.log("Analyze clicked");
    if (!uploadResult || !uploadResult.report_id) return;
    setIsAnalyzing(true);
    setAnalyzeResult(null);

    try {
      const res = await reportClient.analyzeReport(uploadResult.report_id);
      setAnalyzeResult(res);
    } catch (error: any) {
      console.error(error);
      setAnalyzeResult({ success: false, message: error.message || "An unexpected error occurred." });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleScan = async () => {
    if (!uploadResult || !uploadResult.report_id || !scanPath) return;
    setIsScanning(true);
    setScanResult(null);
    setGapResult(null);
    setTestResult(null);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);

    const res = await reportClient.scanCode(uploadResult.report_id, scanPath);
    setScanResult(res);
    setIsScanning(false);
  };

  const handleDetectGaps = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsDetectingGaps(true);
    setGapResult(null);
    setTestResult(null);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);

    const res = await reportClient.detectGaps(uploadResult.report_id);
    setGapResult(res);
    setIsDetectingGaps(false);
  };

  const handleGenerateTests = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsGeneratingTests(true);
    setTestResult(null);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);

    const functionIds = selectedFunctions.size > 0 ? Array.from(selectedFunctions) : undefined;
    const res = await reportClient.generateTests(uploadResult.report_id, functionIds);
    setTestResult(res);
    setIsGeneratingTests(false);
  };

  const handleAnalyzeRisks = async () => {
    if (!uploadResult || !uploadResult.report_id) return;
    setIsAnalyzingRisks(true);
    setRiskResult(null);
    setDependencyResult(null);
    setPredictionResult(null);

    const res = await reportClient.analyzeRisks(uploadResult.report_id);
    setRiskResult(res);
    setIsAnalyzingRisks(false);
  };

  const toggleFunctionSelection = (id: string | undefined) => {
    if (!id) return;
    const newSelection = new Set(selectedFunctions);
    if (newSelection.has(id)) {
      newSelection.delete(id);
    } else {
      newSelection.add(id);
    }
    setSelectedFunctions(newSelection);
  };

  const filteredFunctions = useMemo(() => {
    if (!gapResult?.functions) return [];
    if (gapFilter === 'ALL') return gapResult.functions;
    return gapResult.functions.filter(f => f.coverage_status === gapFilter);
  }, [gapResult, gapFilter]);

  const unhandledCount = useMemo(() => {
    if (!gapResult) return 0;
  
  
  return (
gapResult.uncovered || 0) + (gapResult.partial || 0);
  }, [gapResult]);

    const handleCopyTest = (code: string) => {
    navigator.clipboard.writeText(code);
  };

  const handleDownloadTest = (filename: string, code: string) => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <>
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-white mb-2">Coverage Report Center</h1>
        <p className="text-slate-400">Upload and instantly analyze your XML coverage data.</p>
      </div>

      <div 
        className={`relative border-2 border-dashed rounded-xl p-10 text-center transition-all duration-300 ${
          dragActive ? 'border-blue-500 bg-blue-500/10 scale-[1.01]' : 'border-slate-700 hover:border-slate-500 bg-slate-800/40'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input ref={inputRef} type="file" className="hidden" accept=".xml,text/xml" onChange={handleChange} />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="p-4 bg-slate-800 rounded-full text-blue-400">
            <UploadCloud size={40} />
          </div>
          
          {file ? (
            <div className="text-slate-200">
              <span className="font-semibold text-emerald-400">{file.name}</span> selected ({(file.size / 1024 / 1024).toFixed(2)} MB)
            </div>
          ) : (
            <div>
              <p className="text-lg text-slate-200 font-medium">Drag & drop your XML file here</p>
              <p className="text-slate-400 mt-1">or click to browse</p>
            </div>
          )}

          {!file && (
            <button
              onClick={() => inputRef.current?.click()}
              className="mt-4 px-6 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors"
            >
              Browse Files
            </button>
          )}
        </div>
      </div>

      {uploadResult && (
        <div className={`p-4 rounded-lg flex items-start space-x-3 transition-all ${uploadResult.success ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400' : 'bg-red-500/10 border border-red-500/20 text-red-400'}`}>
          {uploadResult.success ? <CheckCircle className="shrink-0 mt-0.5" size={20} /> : <AlertCircle className="shrink-0 mt-0.5" size={20} />}
          <div className="flex-1">
            <h3 className="font-semibold">{uploadResult.success ? 'Upload Successful' : 'Upload Failed'}</h3>
            <p className="text-sm mt-1 opacity-90">
              {uploadResult.success ? `Report staged with ID: ${uploadResult.report_id}. Ready for analysis.` : uploadResult.message}
            </p>
          </div>
        </div>
      )}

      <div className="flex justify-end space-x-4">
        {predictionResult?.success && (
          <button
            onClick={handleLoadDashboard}
            className="flex items-center space-x-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold shadow-lg transition-colors"
          >
            <LayoutDashboard size={20} />
            <span>View Executive Dashboard</span>
          </button>
        )}
        
        {file && (
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold bg-slate-700 hover:bg-slate-600 text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUploading && <Loader2 className="animate-spin" size={20} />}
            <span>{isUploading ? 'Uploading...' : 'Upload'}</span>
          </button>
        )}
        
        {uploadResult?.success && !analyzeResult?.success && (
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? <Loader2 className="animate-spin" size={20} /> : <Activity size={20} />}
            <span>{isAnalyzing ? 'Analyzing XML...' : 'Analyze Report'}</span>
          </button>
        )}
      </div>

      {analyzeResult && !analyzeResult.success && (
        <div className="mt-4 p-4 rounded-lg flex items-start space-x-3 bg-red-500/10 border border-red-500/20 text-red-400 transition-all">
          <AlertCircle className="shrink-0 mt-0.5" size={20} />
          <div className="flex-1">
            <h3 className="font-semibold">Analysis Failed</h3>
            <p className="text-sm mt-1 opacity-90">{analyzeResult.message}</p>
          </div>
        </div>
      )}

      {analyzeResult?.success && (
        <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
            <PieChart className="text-blue-400" />
            <span>Analysis Results</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
              <div className="text-slate-400 text-sm font-medium mb-1">Coverage</div>
              <div className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-400">
                {analyzeResult.coverage_percent}%
              </div>
            </div>
            <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
              <div className="text-slate-400 text-sm font-medium mb-1 flex items-center space-x-1">
                <FileText size={16} /> <span>Files Analyzed</span>
              </div>
              <div className="text-2xl font-bold text-white">{analyzeResult.total_files}</div>
            </div>
            <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
              <div className="text-slate-400 text-sm font-medium mb-1 flex items-center space-x-1">
                <List size={16} /> <span>Total Classes</span>
              </div>
              <div className="text-2xl font-bold text-white">{analyzeResult.total_classes}</div>
            </div>
            <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
              <div className="text-slate-400 text-sm font-medium mb-1">Covered / Total Lines</div>
              <div className="text-2xl font-bold text-white">
                <span className="text-emerald-400">{analyzeResult.covered_lines}</span> 
                <span className="text-slate-500 mx-1">/</span> 
                <span className="text-slate-300">{analyzeResult.total_lines}</span>
              </div>
            </div>
          </div>


          {/* File Coverage Table */}
          {analyzeResult.files && Array.isArray(analyzeResult.files) && analyzeResult.files.length > 0 && (
            <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6 mb-8">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
                <FileText className="text-blue-400" />
                <span>File Coverage Details</span>
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="text-xs text-slate-400 uppercase bg-slate-900/50">
                    <tr>
                      <th className="px-4 py-3 rounded-tl-lg">File Name</th>
                      <th className="px-4 py-3 text-center">Lines Valid</th>
                      <th className="px-4 py-3 text-center">Lines Covered</th>
                      <th className="px-4 py-3 text-right rounded-tr-lg">Coverage %</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700/50">
                    {analyzeResult.files.map((f, idx) => (
                      <tr key={idx} className="hover:bg-slate-700/30 transition-colors">
                        <td className="px-4 py-3 font-mono text-slate-300">{f.filename}</td>
                        <td className="px-4 py-3 text-center text-slate-400">{f.lines_valid}</td>
                        <td className="px-4 py-3 text-center text-slate-400">{f.lines_covered}</td>
                        <td className="px-4 py-3 text-right font-semibold">
                          <span className={f.coverage_percent >= 80 ? "text-emerald-400" : f.coverage_percent >= 50 ? "text-amber-400" : "text-red-400"}>
                            {f.coverage_percent.toFixed(2)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
              <FolderSearch className="text-emerald-400" />
              <span>AST Source Scan</span>
            </h3>
            <p className="text-slate-400 text-sm mb-4">
              Enter the absolute or relative path to the Python source directory corresponding to this report. The engine will walk the Abstract Syntax Tree to map functions.
            </p>
            <div className="flex space-x-3">
              <input
                type="text"
                placeholder="/app/backend or ./src"
                value={scanPath}
                onChange={(e) => setScanPath(e.target.value)}
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
              <button
                onClick={handleScan}
                disabled={isScanning || !scanPath}
                className="flex items-center space-x-2 px-6 py-2.5 rounded-lg font-semibold bg-emerald-600 hover:bg-emerald-500 text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isScanning ? <Loader2 className="animate-spin" size={20} /> : <Code size={20} />}
                <span>{isScanning ? 'Scanning...' : 'Scan AST'}</span>
              </button>
            </div>
          </div>

            {scanResult && (
              <div className="mt-6">
                <div className={`p-4 rounded-lg flex items-start space-x-3 mb-6 ${scanResult.success ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400' : 'bg-red-500/10 border border-red-500/20 text-red-400'}`}>
                  {scanResult.success ? <CheckCircle className="shrink-0 mt-0.5" size={20} /> : <AlertCircle className="shrink-0 mt-0.5" size={20} />}
                  <div className="flex-1">
                    <h3 className="font-semibold">{scanResult.success ? `Scan Complete: ${scanResult.total_functions_found} Functions Mapped` : 'Scan Failed'}</h3>
                    <p className="text-sm mt-1 opacity-90">{scanResult.message}</p>
                  </div>
                  {scanResult.success && !gapResult && (
                    <button
                      onClick={handleDetectGaps}
                      disabled={isDetectingGaps}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                    >
                      {isDetectingGaps ? <Loader2 className="animate-spin" size={16} /> : <Target size={16} />}
                      <span>Detect Gaps</span>
                    </button>
                  )}
                </div>

                {/* Coverage Gap Dashboard */}
                {gapResult?.success && (
                  <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
                        <Target className="text-blue-400" />
                        <span>Coverage Gap Dashboard</span>
                      </h3>
                      {!riskResult && (
                        <button
                          onClick={handleAnalyzeRisks}
                          disabled={isAnalyzingRisks}
                          className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                        >
                          {isAnalyzingRisks ? <Loader2 className="animate-spin" size={16} /> : <ShieldAlert size={16} />}
                          <span>Analyze Risks</span>
                        </button>
                      )}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-20"><ShieldCheck size={48} className="text-emerald-500" /></div>
                        <div className="text-emerald-400 text-sm font-semibold mb-1 uppercase tracking-wider">Covered</div>
                        <div className="text-3xl font-bold text-white">{gapResult.covered}</div>
                      </div>
                      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-20"><Activity size={48} className="text-yellow-500" /></div>
                        <div className="text-yellow-400 text-sm font-semibold mb-1 uppercase tracking-wider">Partial</div>
                        <div className="text-3xl font-bold text-white">{gapResult.partial}</div>
                      </div>
                      <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-20"><ShieldAlert size={48} className="text-red-500" /></div>
                        <div className="text-red-400 text-sm font-semibold mb-1 uppercase tracking-wider">Uncovered</div>
                        <div className="text-3xl font-bold text-white">{gapResult.uncovered}</div>
                      </div>
                    </div>

                    <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden mb-6">
                      <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex flex-col sm:flex-row justify-between items-center gap-4">
                        <h4 className="font-medium text-slate-200 flex items-center">
                          <Filter size={16} className="mr-2 text-slate-400" /> Functions ({filteredFunctions.length})
                        </h4>
                        <div className="flex items-center space-x-4">
                          <div className="flex space-x-2 bg-slate-900 p-1 rounded-lg">
                            {['ALL', 'COVERED', 'PARTIAL', 'UNCOVERED'].map(filter => (
                              <button
                                key={filter}
                                onClick={() => setGapFilter(filter as FilterType)}
                                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                                  gapFilter === filter 
                                    ? 'bg-slate-700 text-white' 
                                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                                }`}
                              >
                                {filter}
                              </button>
                            ))}
                          </div>
                          
                          {unhandledCount > 0 && (
                            <button
                              onClick={handleGenerateTests}
                              disabled={isGeneratingTests}
                              className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                            >
                              {isGeneratingTests ? <Loader2 className="animate-spin" size={16} /> : <Bot size={16} />}
                              <span>
                                Generate Tests 
                                {selectedFunctions.size > 0 ? ` (${selectedFunctions.size})` : ` (${unhandledCount})`}
                              </span>
                            </button>
                          )}
                        </div>
                      </div>
                      
                      <div className="max-h-[500px] overflow-y-auto">
                        <table className="w-full text-left text-sm text-slate-300">
                          <thead className="text-xs uppercase bg-slate-800/80 text-slate-400 sticky top-0 z-10 backdrop-blur-sm">
                            <tr>
                              <th className="px-6 py-4 w-12">
                                {/* Optional: Select All checkbox */}
                              </th>
                              <th className="px-6 py-4">Function Name</th>
                              <th className="px-6 py-4">Status</th>
                              <th className="px-6 py-4">Coverage %</th>
                              <th className="px-6 py-4">File Path</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-700/50">
                            {filteredFunctions.map((func, idx) => {
                              const isTarget = func.coverage_status === 'UNCOVERED' || func.coverage_status === 'PARTIAL';
                              return (
                                <tr key={idx} className={`hover:bg-slate-800/40 transition-colors ${selectedFunctions.has(func.id || '') ? 'bg-indigo-500/5' : ''}`}>
                                  <td className="px-6 py-4">
                                    <input 
                                      type="checkbox" 
                                      disabled={!isTarget}
                                      checked={selectedFunctions.has(func.id || '')}
                                      onChange={() => toggleFunctionSelection(func.id)}
                                      className="w-4 h-4 rounded border-slate-600 text-indigo-500 focus:ring-indigo-500/20 bg-slate-800 disabled:opacity-50"
                                    />
                                  </td>
                                  <td className="px-6 py-4 font-medium text-slate-200">
                                    <div className="flex items-center space-x-2">
                                      {func.is_async && <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wide bg-purple-500/10 px-1.5 py-0.5 rounded">async</span>}
                                      <span>{func.name}</span>
                                    </div>
                                  </td>
                                  <td className="px-6 py-4">
                                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                                      func.coverage_status === 'COVERED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                                      func.coverage_status === 'PARTIAL' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                                      func.coverage_status === 'UNCOVERED' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                                      'bg-slate-500/10 text-slate-400 border-slate-500/20'
                                    }`}>
                                      {func.coverage_status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4">
                                    <div className="flex items-center space-x-3">
                                      <div className="w-full bg-slate-800 rounded-full h-1.5 max-w-[4rem]">
                                        <div 
                                          className={`h-1.5 rounded-full ${
                                            func.coverage_percent === 100 ? 'bg-emerald-500' :
                                            (func.coverage_percent || 0) > 0 ? 'bg-yellow-500' : 'bg-red-500'
                                          }`}
                                          style={{ width: `${Math.max(func.coverage_percent || 0, 5)}%` }}
                                        ></div>
                                      </div>
                                      <span className="font-mono text-xs">{func.coverage_percent}%</span>
                                    </div>
                                  </td>
                                  <td className="px-6 py-4 font-mono text-[11px] text-slate-500 truncate max-w-[200px]" title={func.file_path}>
                                    {func.file_path}
                                  </td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                        {filteredFunctions.length === 0 && (
                          <div className="p-8 text-center text-slate-500">
                            No functions found matching this filter.
                          </div>
                        )}
                      </div>
                    </div>
                    
                    {/* Test Generation Results */}
                    {testResult?.success && (
                      <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex items-center justify-between mb-6">
                          <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
                            <Bot className="text-indigo-400" />
                            <span>AI Generated Tests ({testResult.generated_count})</span>
                          </h3>
                        </div>
                        
                        <div className="space-y-6">
                          {testResult.tests?.map((test, idx) => (
                            <div key={idx} className="bg-[#0d1117] border border-slate-700/50 rounded-xl overflow-hidden">
                              <div className="px-5 py-4 border-b border-slate-700/50 flex flex-col md:flex-row justify-between items-start md:items-center bg-slate-800/20 gap-4">
                                <div>
                                  <div className="flex flex-wrap items-center gap-3 mb-2">
                                    <PlayCircle size={16} className="text-emerald-400 shrink-0" />
                                    <span className="text-sm font-bold text-slate-200">test_{test.function_name}.py</span>
                                    <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded ${test.status === 'SUCCESS' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
                                      {test.status}
                                    </span>
                                    {test.test_quality_score !== undefined && test.test_quality_score !== null && (
                                      <span className="text-[10px] font-bold px-2 py-1 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                        QUALITY: {test.test_quality_score}/100
                                      </span>
                                    )}
                                  </div>
                                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
                                    <span className="flex items-center"><Bot size={12} className="mr-1" /> {test.model_used}</span>
                                    {test.coverage_percent !== undefined && test.coverage_percent !== null && <span>Coverage: {test.coverage_percent}%</span>}
                                    {test.risk_score !== undefined && test.risk_score !== null && <span>Risk: {test.risk_score.toFixed(1)}</span>}
                                    {test.potential_coverage_gain !== undefined && test.potential_coverage_gain !== null && <span>Gain: +{test.potential_coverage_gain.toFixed(1)}%</span>}
                                  </div>
                                </div>
                                <div className="flex items-center space-x-2 shrink-0">
                                  <button onClick={() => handleCopyTest(test.test_code)} className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md transition-colors text-slate-300 hover:text-white" title="Copy to clipboard">
                                    <Copy size={16} />
                                  </button>
                                  <button onClick={() => handleDownloadTest(`test_${test.function_name}.py`, test.test_code)} className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md transition-colors text-slate-300 hover:text-white" title="Download file">
                                    <Download size={16} />
                                  </button>
                                </div>
                              </div>
                              <div className="p-5 overflow-x-auto text-sm font-mono text-slate-300">
                                <pre><code>{test.test_code}</code></pre>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Prediction Dashboard */}
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
                    )}
                  </div>
                )}
                    {/* Risk Intelligence Dashboard */}
                    {riskResult?.success && (
                      <div className="mt-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex items-center justify-between mb-6">
                          <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
                            <ShieldAlert className="text-purple-400" />
                            <span>AI Risk Intelligence Dashboard</span>
                          </h3>
                          {!dependencyResult && (
                            <button
                              onClick={handleAnalyzeDependencies}
                              disabled={isAnalyzingDependencies}
                              className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md text-sm font-medium transition-colors disabled:opacity-50"
                            >
                              {isAnalyzingDependencies ? <Loader2 className="animate-spin" size={16} /> : <Activity size={16} />}
                              <span>Analyze Dependencies</span>
                            </button>
                          )}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                          <div className="bg-slate-900 border border-purple-500/30 rounded-xl p-5 relative overflow-hidden">
                            <div className="text-purple-400 text-sm font-semibold mb-1 uppercase tracking-wider">Project Risk Score</div>
                            <div className="text-3xl font-bold text-white">{riskResult.project_risk_score}</div>
                          </div>
                          <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5 relative overflow-hidden">
                            <div className="text-red-400 text-sm font-semibold mb-1 uppercase tracking-wider">High Risk</div>
                            <div className="text-3xl font-bold text-white">{riskResult.summary?.high_risk}</div>
                          </div>
                          <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5 relative overflow-hidden">
                            <div className="text-yellow-400 text-sm font-semibold mb-1 uppercase tracking-wider">Medium Risk</div>
                            <div className="text-3xl font-bold text-white">{riskResult.summary?.medium_risk}</div>
                          </div>
                          <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5 relative overflow-hidden">
                            <div className="text-emerald-400 text-sm font-semibold mb-1 uppercase tracking-wider">Low Risk</div>
                            <div className="text-3xl font-bold text-white">{riskResult.summary?.low_risk}</div>
                          </div>
                        </div>

                        <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden mb-6">
                          <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
                            <h4 className="font-medium text-slate-200">Risk Ranking</h4>
                          </div>
                          <div className="max-h-[500px] overflow-y-auto">
                            <table className="w-full text-left text-sm text-slate-300">
                              <thead className="text-xs uppercase bg-slate-800/80 text-slate-400 sticky top-0 z-10">
                                <tr>
                                  <th className="px-6 py-4">Rank</th>
                                  <th className="px-6 py-4">Function</th>
                                  <th className="px-6 py-4">Risk Level</th>
                                  <th className="px-6 py-4">Score</th>
                                  <th className="px-6 py-4 text-right">Action</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-slate-700/50">
                                {riskResult.functions?.map((func: any, idx) => (
                                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                                    <td className="px-6 py-4 text-slate-400 font-mono">#{func.risk_priority_rank}</td>
                                    <td className="px-6 py-4 font-medium text-slate-200">{func.name}</td>
                                    <td className="px-6 py-4">
                                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                                        func.risk_level === 'HIGH' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                                        func.risk_level === 'MEDIUM' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                                        'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                                      }`}>
                                        {func.risk_level}
                                      </span>
                                    </td>
                                    <td className="px-6 py-4 font-mono font-bold">{func.risk_score}</td>
                                    <td className="px-6 py-4 text-right">
                                      <button 
                                        onClick={() => setSelectedRiskFunction(func)}
                                        className="text-purple-400 hover:text-purple-300 font-medium text-xs uppercase tracking-wider"
                                      >
                                        View Reasons
                                      </button>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>

    {/* View Reasons Modal */}
    {selectedRiskFunction && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={() => setSelectedRiskFunction(null)}>
        <div className="bg-[#0d1117] border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
            <div>
              <h3 className="text-lg font-bold text-white">{selectedRiskFunction.name}</h3>
              <p className="text-xs text-slate-400 mt-0.5">{selectedRiskFunction.file_path}</p>
            </div>
            <button onClick={() => setSelectedRiskFunction(null)} className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors">
              <X size={18} />
            </button>
          </div>
          <div className="px-6 py-4 border-b border-slate-700 flex items-center gap-6">
            <div>
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Risk Score</p>
              <p className="text-2xl font-extrabold text-white">{selectedRiskFunction.risk_score}</p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Risk Level</p>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border ${
                selectedRiskFunction.risk_level === 'HIGH' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                selectedRiskFunction.risk_level === 'MEDIUM' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
              }`}>{selectedRiskFunction.risk_level}</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1 uppercase tracking-wider">Coverage</p>
              <p className="text-2xl font-extrabold text-white">{selectedRiskFunction.coverage_percent ?? 0}%</p>
            </div>
          </div>
          <div className="px-6 py-4 max-h-72 overflow-y-auto">
            <p className="text-xs text-slate-400 uppercase tracking-wider mb-3">Risk Reasons</p>
            {selectedRiskFunction.risk_reasons && selectedRiskFunction.risk_reasons.length > 0 ? (
              <ul className="space-y-2">
                {selectedRiskFunction.risk_reasons.map((reason: string, i: number) => (
                  <li key={i} className="flex items-start space-x-2 text-sm text-slate-300">
                    <ShieldAlert size={14} className="text-red-400 mt-0.5 shrink-0" />
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-slate-500 text-sm">No specific risk reasons recorded.</p>
            )}
          </div>
          <div className="px-6 py-4 border-t border-slate-700">
            <button onClick={() => setSelectedRiskFunction(null)} className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium text-slate-300 hover:text-white transition-colors">
              Close
            </button>
          </div>
        </div>
      </div>
    )}
    </>
  );
}
