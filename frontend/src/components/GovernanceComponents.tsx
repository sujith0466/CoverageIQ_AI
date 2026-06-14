import { useEffect, useState } from 'react';
import { reportClient, GovernanceOverviewResponse, ReportHistoryResponse } from '../api/reportClient';
import { Clock, Server } from 'lucide-react';

export function GovernanceOverviewCards() {
  const [data, setData] = useState<GovernanceOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGov() {
      try {
        const res = await reportClient.getGovernanceOverview();
        if (res.success) {
          setData(res);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchGov();
  }, []);

  if (loading || !data) {
    return (
      <section className="w-full py-12 px-6 border-b border-slate-800 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center"><Server className="mr-2 text-indigo-400" /> System Governance & Intelligence</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 animate-pulse">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-slate-800 p-4 rounded-xl border border-slate-700 h-24"></div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="w-full py-12 px-6 border-b border-slate-800 bg-slate-900/50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center"><Server className="mr-2 text-indigo-400" /> System Governance & Intelligence</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Reports Analyzed</div>
            <div className="text-2xl font-bold text-white">{data.reports_analyzed}</div>
          </div>
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Functions Scanned</div>
            <div className="text-2xl font-bold text-white">{data.functions_scanned}</div>
          </div>
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Coverage Gaps</div>
            <div className="text-2xl font-bold text-rose-400">{data.coverage_gaps_found}</div>
          </div>
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Tests Generated</div>
            <div className="text-2xl font-bold text-emerald-400">{data.tests_generated}</div>
          </div>
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Avg Coverage</div>
            <div className="text-2xl font-bold text-blue-400">{data.average_coverage}%</div>
          </div>
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <div className="text-sm text-slate-400 mb-1">Avg Health Score</div>
            <div className="text-2xl font-bold text-indigo-400">{data.average_health_score}</div>
          </div>
        </div>
      </div>
    </section>
  );
}

export function ReportHistoryTable() {
  const [data, setData] = useState<ReportHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await reportClient.getReportHistory();
        if (res.success && res.reports.length > 0) {
          setData(res);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, []);

  if (loading) {
    return (
      <section className="w-full py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-1 flex items-center"><Clock className="mr-2 text-indigo-400" /> Recent Reports</h2>
          <p className="text-slate-400 text-sm mb-6">Latest 10 analysis runs</p>
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden animate-pulse">
            <table className="w-full text-left">
              <thead className="bg-slate-800/50 text-slate-400 text-sm border-b border-slate-800">
                <tr>
                  <th className="p-4">Date</th><th className="p-4">Coverage</th><th className="p-4">Files</th><th className="p-4">Functions</th><th className="p-4">Tests Gen</th><th className="p-4">Latest Audit Status</th>
                </tr>
              </thead>
              <tbody>
                {[...Array(3)].map((_, i) => (
                  <tr key={i} className="border-b border-slate-800/50">
                    <td className="p-4"><div className="h-4 bg-slate-800 rounded w-24"></div></td>
                    <td className="p-4"><div className="h-4 bg-slate-800 rounded w-16"></div></td>
                    <td className="p-4"><div className="h-4 bg-slate-800 rounded w-12"></div></td>
                    <td className="p-4"><div className="h-4 bg-slate-800 rounded w-16"></div></td>
                    <td className="p-4"><div className="h-4 bg-slate-800 rounded w-16"></div></td>
                    <td className="p-4"><div className="h-6 bg-slate-800 rounded-full w-24"></div></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    );
  }

  if (!data || data.reports.length === 0) return null;

  const sortedReports = [...data.reports]
    .sort((a, b) => new Date(b.uploaded_at).getTime() - new Date(a.uploaded_at).getTime())
    .slice(0, 10);

  return (
    <section className="w-full py-12 px-6">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-2xl font-bold text-white mb-1 flex items-center"><Clock className="mr-2 text-indigo-400" /> Recent Reports</h2>
        <p className="text-slate-400 text-sm mb-6">Latest 10 analysis runs</p>
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-slate-800/50 text-slate-400 text-sm border-b border-slate-800">
              <tr>
                <th className="p-4 font-medium">Date</th>
                <th className="p-4 font-medium">Coverage</th>
                <th className="p-4 font-medium">Files</th>
                <th className="p-4 font-medium">Functions</th>
                <th className="p-4 font-medium">Tests Gen</th>
                <th className="p-4 font-medium">Latest Audit Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {sortedReports.map((report) => (
                <tr key={report.report_id} className="hover:bg-slate-800/20 transition-colors">
                  <td className="p-4 text-slate-300">{new Date(report.uploaded_at).toLocaleString()}</td>
                  <td className="p-4 text-white font-medium">{report.coverage_percent ?? 0}%</td>
                  <td className="p-4 text-slate-300">{report.files_analyzed}</td>
                  <td className="p-4 text-slate-300">{report.functions_found}</td>
                  <td className="p-4 text-emerald-400 font-medium">{report.tests_generated}</td>
                  <td className="p-4 text-indigo-300 text-sm">{report.latest_status || 'UNKNOWN'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
