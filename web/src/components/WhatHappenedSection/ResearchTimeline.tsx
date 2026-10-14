import React, { useState } from 'react';
import { 
  GitCommit, 
  Calendar, 
  AlertCircle, 
  Lightbulb, 
  ChevronRight, 
  TrendingUp, 
  Cpu, 
  CheckCircle2,
  Award
} from 'lucide-react';
import { RESEARCH_MILESTONES } from '../../data/researchData';
import { ResearchMilestone } from '../../types/clinical';

export const ResearchTimeline: React.FC = () => {
  const [selectedMilestone, setSelectedMilestone] = useState<ResearchMilestone>(
    RESEARCH_MILESTONES[RESEARCH_MILESTONES.length - 1]
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <GitCommit className="w-5 h-5 text-cyan-400" />
            <span>Autonomous Evolution Timeline: v6.0 → v8.3 SOTA</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Full chronological audit of hypotheses, architecture migrations, bottlenecks, and breakthroughs.
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full bg-cyan-950 text-cyan-300 font-mono text-xs border border-cyan-800/60">
          5 Iterations Recorded
        </span>
      </div>

      {/* Timeline Step Selector */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 sm:gap-3">
        {RESEARCH_MILESTONES.map((m) => {
          const isSelected = selectedMilestone.version === m.version;
          const isSota = m.status === 'active_sota';
          const isBaseline = m.status === 'baseline';

          return (
            <button
              key={m.version}
              onClick={() => setSelectedMilestone(m)}
              className={`p-3 rounded-xl border text-left transition-all relative ${
                isSelected
                  ? 'border-cyan-400 bg-cyan-950/50 shadow-md shadow-cyan-950/60 ring-1 ring-cyan-400/40'
                  : 'border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900'
              }`}
            >
              {isSota && (
                <span className="absolute -top-2 right-2 px-1.5 py-0.2 rounded bg-cyan-500 text-slate-950 text-[9px] font-black uppercase tracking-wider">
                  SOTA
                </span>
              )}
              {isBaseline && (
                <span className="absolute -top-2 right-2 px-1.5 py-0.2 rounded bg-slate-700 text-slate-300 text-[9px] font-black uppercase tracking-wider">
                  Baseline
                </span>
              )}

              <div className="font-extrabold text-sm sm:text-base text-white">
                {m.version}
              </div>
              <div className="text-[10px] text-slate-400 flex items-center gap-1 mt-0.5 font-mono">
                <Calendar className="w-2.5 h-2.5 text-slate-400" />
                {m.date}
              </div>

              <div className="mt-2 text-xs font-mono font-bold text-cyan-300 flex items-center justify-between">
                <span>F1:</span>
                <span className="text-sm">{m.macroF1.toFixed(1)}%</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected Milestone Detail Inspector */}
      <div className="rounded-2xl glass-panel-elevated p-6 border border-slate-800 space-y-6">
        {/* Top Summary Bar */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 rounded text-xs font-black font-mono bg-cyan-950 text-cyan-300 border border-cyan-800/60">
                {selectedMilestone.version}
              </span>
              <span className="text-xs text-slate-400">Date: {selectedMilestone.date}</span>
              {selectedMilestone.status === 'active_sota' && (
                <span className="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 text-[10px] font-bold border border-emerald-800/60 flex items-center gap-1">
                  <Award className="w-3 h-3" /> Current Best State-of-the-Art
                </span>
              )}
            </div>
            <h4 className="text-lg font-extrabold text-white">
              {selectedMilestone.title}
            </h4>
            <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-cyan-400" />
              <span>{selectedMilestone.architecture}</span>
            </p>
          </div>

          {/* Metric Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            <div className="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-center">
              <span className="text-[10px] uppercase tracking-wider text-slate-400 block font-semibold">
                Mean Macro-F1
              </span>
              <span className="text-base font-extrabold text-cyan-400 font-mono">
                {selectedMilestone.macroF1.toFixed(2)}%
              </span>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-center">
              <span className="text-[10px] uppercase tracking-wider text-slate-400 block font-semibold">
                Accuracy
              </span>
              <span className="text-base font-extrabold text-white font-mono">
                {selectedMilestone.meanAccuracy.toFixed(1)}%
              </span>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-center">
              <span className="text-[10px] uppercase tracking-wider text-slate-400 block font-semibold">
                Minority Heads
              </span>
              <span className="text-base font-extrabold text-amber-400 font-mono">
                {selectedMilestone.minorityHeadsF1.toFixed(1)}%
              </span>
            </div>

            <div className="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-center">
              <span className="text-[10px] uppercase tracking-wider text-slate-400 block font-semibold">
                Exact Match (8/8)
              </span>
              <span className="text-base font-extrabold text-emerald-400 font-mono">
                {selectedMilestone.exactMatchRatio.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        {/* 2-Column: Key Bottlenecks Encountered vs Key Innovations Developed */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* Bottlenecks / Failures */}
          <div className="p-4 rounded-xl bg-red-950/20 border border-red-900/40 space-y-2.5">
            <div className="flex items-center gap-2 text-red-300 font-bold text-xs uppercase tracking-wider">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <span>Scientific Bottlenecks & Failure Modes</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300 leading-relaxed">
              {selectedMilestone.keyBottlenecks.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-400 mt-1.5 shrink-0" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Innovations / Breakthroughs */}
          <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/40 space-y-2.5">
            <div className="flex items-center gap-2 text-emerald-300 font-bold text-xs uppercase tracking-wider">
              <Lightbulb className="w-4 h-4 text-emerald-400" />
              <span>Algorithmic Solutions & Breakthroughs</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300 leading-relaxed">
              {selectedMilestone.keyInnovations.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
