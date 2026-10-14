import React from 'react';
import { 
  ShieldCheck, 
  Activity, 
  Layers, 
  FlaskConical, 
  BookOpen, 
  Server, 
  RefreshCw,
  GitBranch
} from 'lucide-react';
import { BackendHealth } from '../api/client';

export type ActiveTab = 'studio' | 'audit' | 'telemetry' | 'cases';

interface HeaderProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  backendHealth: BackendHealth;
  onReset: () => void;
  hasActiveResult: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  onTabChange,
  backendHealth,
  onReset,
  hasActiveResult,
}) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Identity */}
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-teal-700 shadow-lg shadow-cyan-900/40 border border-cyan-400/30">
              <ShieldCheck className="w-6 h-6 text-white" />
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-cyan-300 bg-clip-text text-transparent">
                  SurgWound Assist
                </span>
                <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800/50 flex items-center gap-1">
                  <GitBranch className="w-3 h-3" /> v8.3 SOTA
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Autonomous Surgical Wound Assessment & Clinical Decision Support
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => onTabChange('studio')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all ${
                activeTab === 'studio'
                  ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Diagnostic Studio</span>
            </button>

            <button
              onClick={() => onTabChange('audit')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all relative ${
                activeTab === 'audit'
                  ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <FlaskConical className="w-4 h-4" />
              <span>What Happened (Audit)</span>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
              </span>
            </button>

            <button
              onClick={() => onTabChange('telemetry')}
              className={`hidden md:flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all ${
                activeTab === 'telemetry'
                  ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>Pipeline Telemetry</span>
            </button>

            <button
              onClick={() => onTabChange('cases')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all ${
                activeTab === 'cases'
                  ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Cases Library</span>
            </button>
          </nav>

          {/* Right Status / Actions */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Backend Health Badge */}
            <div
              className={`hidden lg:flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-mono border ${
                backendHealth.isOnline
                  ? 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60'
                  : 'bg-slate-900 text-slate-400 border-slate-800'
              }`}
              title={backendHealth.message}
            >
              <Server className="w-3.5 h-3.5" />
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="truncate max-w-[120px]">
                {backendHealth.isOnline ? 'ONNX Live' : 'Calibrated Engine'}
              </span>
            </div>

            {hasActiveResult && (
              <button
                onClick={onReset}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors border border-slate-700"
                title="Reset current session"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">New Assessment</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
