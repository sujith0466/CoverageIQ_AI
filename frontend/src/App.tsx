import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
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
