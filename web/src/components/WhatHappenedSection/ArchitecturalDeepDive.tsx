import React from 'react';
import { Layers, Network, Zap, BookOpen, ShieldAlert, Cpu, Sparkles } from 'lucide-react';

export const ArchitecturalDeepDive: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Network className="w-5 h-5 text-cyan-400" />
            <span>Architectural Innovations & Mathematical Formulations</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            The three core breakthroughs that powered the transition from baseline failure to project SOTA.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Pillar 1: Logit-Adjusted Loss */}
        <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3.5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-xl bg-cyan-950 border border-cyan-800/50 text-cyan-400">
                <Zap className="w-4 h-4" />
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-cyan-300 border border-slate-700">
                Loss Formulation
              </span>
            </div>

            <h4 className="text-sm font-bold text-white mt-3">
              1. Single-Stage Logit-Adjusted Loss ($\tau=1.0$)
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed mt-1.5">
              Replaced two-phase LDAM margin loss. LDAM suffered severe FP16/AMP gradient scaling explosions ($s=30$) and NaN crashes. Logit adjustment enforces Fisher-consistent balanced error rates:
            </p>

            <div className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 font-mono text-[11px] text-cyan-300 my-2.5 overflow-x-auto">
              {"L(y, f(x)) = -log [ exp(f_y(x) + τ log π_y) / Σ_j exp(f_j(x) + τ log π_j) ]"}
            </div>

            <p className="text-[11px] text-slate-400 leading-relaxed">
              Where $\pi_y$ is class prior probability. This recovered minority infection risk detection from 0.0% to 79.6% recall.
            </p>
          </div>

          <div className="pt-3 border-t border-slate-800/80 text-[11px] font-mono text-emerald-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Eliminated AMP NaN Crashes</span>
          </div>
        </div>

        {/* Pillar 2: PubMedBERT Text Prototypes */}
        <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3.5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-xl bg-teal-950 border border-teal-800/50 text-teal-400">
                <BookOpen className="w-4 h-4" />
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-teal-300 border border-slate-700">
                Semantic Adapters
              </span>
            </div>

            <h4 className="text-sm font-bold text-white mt-3">
              2. PubMedBERT Semantic Text Prototypes
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed mt-1.5">
              Instead of random MLP initialization, classification head weights are anchored to precomputed PubMedBERT medical text embeddings:
            </p>

            <div className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 font-mono text-[11px] text-teal-300 my-2.5 overflow-x-auto">
              {"W_attr = Normalize( PubMedBERT( prompt_clinical_definition ) )"}
            </div>

            <p className="text-[11px] text-slate-400 leading-relaxed">
              Provides domain-aligned semantic coordinate frames for rare anatomical sites, propelling Location F1 from 40.8% to 66.5% (+25.7%).
            </p>
          </div>

          <div className="pt-3 border-t border-slate-800/80 text-[11px] font-mono text-teal-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            <span>+25.69% Location F1 Leap</span>
          </div>
        </div>

        {/* Pillar 3: Multi-Scale Crop Fusion */}
        <div className="p-5 rounded-2xl glass-panel-elevated border border-slate-800 space-y-3.5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-xl bg-indigo-950 border border-indigo-800/50 text-indigo-400">
                <Layers className="w-4 h-4" />
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-indigo-300 border border-slate-700">
                Multi-Scale ViT
              </span>
            </div>

            <h4 className="text-sm font-bold text-white mt-3">
              3. Dual-Stream Multi-Scale Crop Fusion
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed mt-1.5">
              Downsampling 853×640 photos directly to 224×224 destroyed micro-textures (sutures vs staples, purulence). Fusing global and local streams solved this:
            </p>

            <div className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 font-mono text-[11px] text-indigo-300 my-2.5 overflow-x-auto">
              {"Z_fused = Linear_Projection( [ ViT(x_global) || ViT(x_crop_65%) ] )"}
            </div>

            <p className="text-[11px] text-slate-400 leading-relaxed">
              Concatenates two 512-dim BiomedCLIP embeddings into a 1024-dim representation projected to 512, boosting closure method F1 by +9.85%.
            </p>
          </div>

          <div className="pt-3 border-t border-slate-800/80 text-[11px] font-mono text-indigo-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            <span>+14.58% Minority Attribute Boost</span>
          </div>
        </div>
      </div>
    </div>
  );
};
