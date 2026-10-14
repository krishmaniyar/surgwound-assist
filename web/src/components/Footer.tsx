import React from 'react';
import { ShieldCheck, FileText, ExternalLink, GitBranch } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-16 border-t border-slate-900 bg-slate-950/80 text-slate-400 text-xs py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-lg bg-cyan-950 border border-cyan-800/60 flex items-center justify-center text-cyan-400">
            <ShieldCheck className="w-3.5 h-3.5" />
          </div>
          <div>
            <span className="font-bold text-slate-200">SurgWound Assist v8.3 SOTA</span>
            <span className="mx-2 text-slate-700">|</span>
            <span>BiomedCLIP Multi-Scale Vision Transformers & Semantic Prototypes</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-[11px] font-mono text-slate-400">
          <span>Protocol: Aligned with SurgWound Research Governance</span>
          <span>•</span>
          <span>Test Macro-F1: 58.73%</span>
          <span>•</span>
          <span>Minority F1: 41.25%</span>
        </div>
      </div>
    </footer>
  );
};
