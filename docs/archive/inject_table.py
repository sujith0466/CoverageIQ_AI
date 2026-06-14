import os

file_path = 'frontend/src/pages/UploadReport.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

table_jsx = """
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
"""

target = '          <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">'

if 'File Coverage Table' not in content:
    content = content.replace(target, table_jsx + '\n' + target)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File Table injected successfully.")
else:
    print("File Table already exists.")
