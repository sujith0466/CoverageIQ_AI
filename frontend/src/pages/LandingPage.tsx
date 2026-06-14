// import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, GitCommit, PlayCircle, BarChart3, FolderSearch, Zap } from 'lucide-react';
import { GovernanceOverviewCards } from '../components/GovernanceComponents';

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

      {/* Governance & History */}
      <GovernanceOverviewCards />

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
