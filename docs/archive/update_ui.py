import re

file_path = 'frontend/src/pages/UploadReport.tsx'
with open(file_path, encoding='utf-8') as f:
    c = f.read()

# 1. Imports
c = re.sub(r'import \{ UploadCloud,', 'import { UploadCloud, Copy, Download,', c)

# 2. Add Handlers (we can put them inside the component before return)
handlers = """
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
"""
c = c.replace('  return (', handlers, 1)

# 3. Replace the Test Generation UI block
idx_start = c.find('{/* Test Generation Results */}')
idx_end = c.find('{/* Prediction Dashboard */}')

new_block = """{/* Test Generation Results */}
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
                    
                    """

c = c[:idx_start] + new_block + c[idx_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)
