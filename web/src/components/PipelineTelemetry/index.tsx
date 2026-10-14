import React, { useState } from 'react';
import { 
  Layers, 
  Cpu, 
  ArrowRight, 
  Sparkles, 
  Activity, 
  Database, 
  ShieldCheck, 
  Workflow,
  CheckCircle2
} from 'lucide-react';
import { TECHNICAL_SPECIFICATIONS } from '../../data/researchData';

export const PipelineTelemetry: React.FC = () => {
  const [activeStage, setActiveStage] = useState<number>(3);

  const stages = [
    {
      id: 1,
      title: '1. Multi-Scale Normalization',
      badge: 'Input Prep',
      tensor: 'Input: [1, 3, 224, 224] & [1, 3, 224, 224]',
      latency: '~2 ms',
      description:
        'Original surgical photo (up to 853×640) is processed into two streams: Global Context (Resize 256×256 → CenterCrop 224×224) and High-Res 65% Local Wound Bed Window. Normalization applied via ImageNet & BiomedCLIP mean/std vectors.',
    },
    {
      id: 2,
      title: '2. Shared BiomedCLIP ViT-B/16',
      badge: 'Feature Encoder',
      tensor: 'Latent: [1, 512] + [1, 512] → [1, 1024]',
      latency: '~32 ms',
      description:
        'Dual streams pass through a shared 12-layer Vision Transformer (BiomedCLIP pre-trained on 15 million PubMed Central image-text pairs). 768-dim patch tokens pooled and projected into twin 512-dim embedding spaces.',
    },
    {
      id: 3,
      title: '3. Multi-Scale Fusion Projection',
      badge: 'Projection Layer',
      tensor: 'Fused Embedding: [1, 512]',
      latency: '~1 ms',
      description:
        'Global and local 512-dim vectors are concatenated into a 1024-dim joint representation, passed through a LayerNorm + Linear projection layer back to 512-dim, capturing both anatomical context and microscopic suture/exudate detail.',
    },
    {
      id: 4,
      title: '4. PubMedBERT Text-Informed Adapters',
      badge: 'Semantic Alignment',
      tensor: 'Residual Adapter: [1, 256] → Prototype Matching',
      latency: '~3 ms',
      description:
        'Classifier head weights are anchored to normalized PubMedBERT text embeddings of clinical definitions. Residual adapter branches (hidden_dim=256) refine predictions while preserving semantic coordinate frames.',
    },
    {
      id: 5,
      title: '5. Logit-Adjusted Joint Triage',
      badge: 'Multi-Task Output',
      tensor: 'Outputs: 8 Tensors → Softmax Probs',
      latency: '~4 ms',
      description:
        'Logit adjustment offsets softmax boundaries using training distribution class frequencies (+τ log π_y). Regularized validation calibration applies per-class decision thresholds to produce the 8 clinical attributes and triage recommendation.',
    },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Workflow className="w-5 h-5 text-cyan-400" />
            <span>End-to-End Inference Pipeline & Neural Telemetry</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Step-by-step trace through the 5-stage dual-stream BiomedCLIP inference architecture.
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full bg-cyan-950 text-cyan-300 font-mono text-xs border border-cyan-800/60">
          Total Latency: ~42ms (GPU) / ~78ms (CPU)
        </span>
      </div>

      {/* Pipeline Stages Visual Flow */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        {stages.map((stage) => {
          const isActive = activeStage === stage.id;

          return (
            <div
              key={stage.id}
              onClick={() => setActiveStage(stage.id)}
              className={`p-3.5 rounded-2xl border text-left cursor-pointer transition-all duration-200 relative ${
                isActive
                  ? 'border-cyan-400 bg-cyan-950/60 shadow-lg shadow-cyan-950/60 ring-1 ring-cyan-400/40'
                  : 'border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-cyan-300 border border-slate-700">
                  {stage.badge}
                </span>
                <span className="text-[10px] font-mono text-slate-400">{stage.latency}</span>
              </div>

              <h4 className="text-xs font-bold text-white mb-1">{stage.title}</h4>
              <p className="text-[10px] font-mono text-cyan-400/80 truncate">{stage.tensor}</p>
            </div>
          );
        })}
      </div>

      {/* Active Stage Deep Inspection */}
      {(() => {
        const current = stages.find((s) => s.id === activeStage)!;
        return (
          <div className="rounded-2xl glass-panel-elevated p-6 border border-slate-800 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-cyan-950 border border-cyan-800/60 text-cyan-400">
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-base font-extrabold text-white">{current.title}</h4>
                  <span className="text-xs font-mono text-cyan-300">{current.tensor}</span>
                </div>
              </div>

              <span className="px-3 py-1 rounded-full bg-slate-900 text-slate-300 font-mono text-xs border border-slate-800">
                Execution Time: {current.latency}
              </span>
            </div>

            <p className="text-sm text-slate-300 leading-relaxed font-sans">
              {current.description}
            </p>
          </div>
        );
      })()}

      {/* System Technical Telemetry Specs */}
      <div className="rounded-2xl glass-panel-elevated p-6 border border-slate-800 space-y-4">
        <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>System Execution Specifications & Memory Footprint</span>
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-slate-400 block mb-1">Architecture</span>
            <span className="text-cyan-300 font-bold">{TECHNICAL_SPECIFICATIONS.backbone}</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-slate-400 block mb-1">Inference Engine</span>
            <span className="text-teal-300 font-bold">{TECHNICAL_SPECIFICATIONS.inferenceEngine}</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-slate-400 block mb-1">Peak Training VRAM</span>
            <span className="text-emerald-300 font-bold">{TECHNICAL_SPECIFICATIONS.targetVramFootprint}</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-slate-400 block mb-1">Total Parameters</span>
            <span className="text-amber-300 font-bold">203.4M (Vision-Language)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
