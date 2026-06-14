modal = """

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
"""

with open('frontend/src/pages/UploadReport.tsx', encoding='utf-8') as f:
    c = f.read()

c = c.rstrip()
# find the last occurrence of "  );\n}"
idx = c.rfind('  );\n}')
if idx != -1:
    c = c[:idx] + modal + '\n  );\n}\n'
    with open('frontend/src/pages/UploadReport.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Modal inserted successfully')
else:
    print('Pattern not found, last 200 chars:', repr(c[-200:]))
