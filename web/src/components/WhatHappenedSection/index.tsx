import React, { useState } from 'react';
import { 
  History, 
  BarChart2, 
  ListOrdered, 
  Cpu, 
  AlertTriangle, 
  FileCode, 
  CheckCircle2, 
  Zap, 
  TrendingUp, 
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { ResearchTimeline } from './ResearchTimeline';
import { BenchmarkCharts } from './BenchmarkCharts';
import { PerAttributeAnalysis } from './PerAttributeAnalysis';
import { ArchitecturalDeepDive } from './ArchitecturalDeepDive';
import { TECHNICAL_SPECIFICATIONS } from '../../data/researchData';

export const WhatHappenedSection: React.FC = () => {
  const [subTab, setSubTab] = useState<'timeline' | 'charts' | 'matrix' | 'architecture' | 'failures'>(
    'timeline'
  );

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Hero Header */}
      <div className="relative rounded-3xl p-6 sm:p-8 bg-gradient-to-br from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 overflow-hidden shadow-2xl">
        <div className="absolute -right-16 -top-16 w-80 h-80 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-4xl space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-cyan-950 text-cyan-300 border border-cyan-800/60 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" /> Project Evolution & Autonomous Research Audit
            </span>
            <span className="text-xs text-slate-400">
              Complete Documentation of Experiments, Hypotheses, and SOTA Breakthroughs
            </span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            How SurgWound Assist Evolved from Baseline Failure to State-of-the-Art
          </h2>

          <p className="text-sm text-slate-300 leading-relaxed">
            In early versions (v6 and v7.5), surgical wound assessment suffered severe minority class collapse: 
            medium and high infection risks had 0% recall, rare exudate types collapsed, and numerical NaN crashes plagued FP16 training. 
            Through systematic autonomous experimentation in <strong>v8</strong>, the system introduced 
            <strong> Logit-Adjusted Loss</strong>, <strong>PubMedBERT Semantic Text Prototypes</strong>, and 
            <strong> Dual-Stream Multi-Scale Crop Fusion</strong>, pushing Macro-F1 from 
            <strong> 51.10%</strong> to a record <strong>58.73%</strong>.
          </p>

          {/* Quick Stat Highlights */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3">
            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">SOTA Macro-F1</span>
              <span className="text-xl font-extrabold text-cyan-400 font-mono">58.73%</span>
              <span className="text-[10px] text-emerald-400 block font-mono">+7.63% Over Baseline</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Location Gain</span>
              <span className="text-xl font-extrabold text-teal-400 font-mono">+25.69%</span>
              <span className="text-[10px] text-slate-400 block font-mono">40.76% → 66.45%</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Infection Risk Gain</span>
              <span className="text-xl font-extrabold text-amber-400 font-mono">+36.18%</span>
              <span className="text-[10px] text-slate-400 block font-mono">29.63% → 65.81%</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Exact Match Ratio</span>
              <span className="text-xl font-extrabold text-indigo-400 font-mono">20.00%</span>
              <span className="text-[10px] text-slate-400 block font-mono">1 in 5 Patients 8/8 Correct</span>
            </div>
          </div>
        </div>
      </div>

      {/* Sub Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
        <button
          onClick={() => setSubTab('timeline')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            subTab === 'timeline'
              ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/40'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <History className="w-4 h-4" />
          <span>Timeline (v6 → v8.3)</span>
        </button>

        <button
          onClick={() => setSubTab('charts')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            subTab === 'charts'
              ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/40'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <BarChart2 className="w-4 h-4" />
          <span>Benchmark Charts</span>
        </button>

        <button
          onClick={() => setSubTab('matrix')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            subTab === 'matrix'
              ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/40'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <ListOrdered className="w-4 h-4" />
          <span>Per-Attribute Breakdown</span>
        </button>

        <button
          onClick={() => setSubTab('architecture')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            subTab === 'architecture'
              ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/40'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Cpu className="w-4 h-4" />
          <span>Architectural Deep Dive</span>
        </button>

        <button
          onClick={() => setSubTab('failures')}
          className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
            subTab === 'failures'
              ? 'bg-cyan-600 text-white shadow-sm shadow-cyan-900/40'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <AlertTriangle className="w-4 h-4" />
          <span>Failure Catalog & Lessons</span>
        </button>
      </div>

      {/* Sub Tab Views */}
      <div>
        {subTab === 'timeline' && <ResearchTimeline />}
        {subTab === 'charts' && <BenchmarkCharts />}
        {subTab === 'matrix' && <PerAttributeAnalysis />}
        {subTab === 'architecture' && <ArchitecturalDeepDive />}
        {subTab === 'failures' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-400" />
                  <span>Documented Failures & Negative Results Catalog</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Documenting what failed prevented repeat errors and guided the final SOTA configuration.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-red-950 text-red-300 border border-red-800/50">
                  Experiment Failure 1
                </span>
                <h4 className="text-sm font-bold text-white">
                  LDAM Loss Margin Gradient Overflow in FP16 / AMP
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Hypothesis:</strong> Increasing LDAM scale factor $s$ to 30 will force the network to prioritize rare purulent exudate cases.<br />
                  <strong>Outcome:</strong> In FP16 Mixed Precision on RTX 3060, large margin penalties caused gradient norms to exceed 65,504, triggering gradient unscaling NaN crashes across all 8 heads in epoch 4.<br />
                  <strong>Resolution:</strong> Replaced LDAM with Fisher-consistent Logit-Adjusted Loss ($\tau=1.0$), which operates natively inside standard softmax bounds without numerical divergence.
                </p>
              </div>

              <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950 text-amber-300 border border-amber-800/50">
                  Experiment Failure 2
                </span>
                <h4 className="text-sm font-bold text-white">
                  Direct Global Downsampling (Destroyed Micro-Textures)
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Hypothesis:</strong> A single ViT-B/16 operating on standard 224×224 images can learn both anatomical context and suture types simultaneously.<br />
                  <strong>Outcome:</strong> Downsampling high-resolution clinical photos (853×640) directly down to 224×224 destroyed fine thread knot patterns and small staple prongs, leading to 0% F1 on staples.<br />
                  <strong>Resolution:</strong> Engineered dual-stream multi-scale ViT, combining 224×224 global view with a localized 65% wound-bed high-resolution crop, lifting closure method F1 by +9.85%.
                </p>
              </div>

              <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950 text-amber-300 border border-amber-800/50">
                  Experiment Failure 3
                </span>
                <h4 className="text-sm font-bold text-white">
                  Heavy Foundation Backbones (DINOv2-Large 304M)
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  <strong>Hypothesis:</strong> Scaling parameter count to 304M via DINOv2-Large will enhance feature representational capacity.<br />
                  <strong>Outcome:</strong> Latency skyrocketed to &gt;180ms per image and VRAM peaked at 5.9 GB, leaving no headroom for multi-scale cropping or test-time augmentation.<br />
                  <strong>Resolution:</strong> Re-anchored to domain-specific BiomedCLIP ViT-B/16 (203M params), achieving higher F1 while maintaining 4.19 GB VRAM and ~45ms inference latency.
                </p>
              </div>

              <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-800/50">
                  Scientific Conclusion
                </span>
                <h4 className="text-sm font-bold text-white">
                  Domain Alignment Outperformed Brute-Force Scaling
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  The primary driver of progress in SurgWound Assist was not parameter scale, but <strong>medical domain grounding</strong> (PubMedBERT text prototypes) and <strong>spatial multi-scale inductive bias</strong> (local wound crops).
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
