import React from 'react';
import { 
  MapPin, 
  HeartPulse, 
  Scissors, 
  Droplets, 
  Flame, 
  Maximize, 
  AlertOctagon, 
  ShieldCheck,
  Info
} from 'lucide-react';
import { AttributePrediction } from '../../types/clinical';

interface AttributeMatrixProps {
  location: AttributePrediction;
  healingStatus: AttributePrediction;
  closureMethod: AttributePrediction;
  exudateType: AttributePrediction;
  erythema: AttributePrediction;
  edema: AttributePrediction;
}

export const AttributeMatrix: React.FC<AttributeMatrixProps> = ({
  location,
  healingStatus,
  closureMethod,
  exudateType,
  erythema,
  edema,
}) => {
  const cards = [
    {
      title: 'Anatomical Location',
      icon: <MapPin className="w-4 h-4 text-cyan-400" />,
      prediction: location,
      prototypes: 'PubMedBERT Anchored',
      description: 'Anatomical coordinate frame resolved using medical semantic prototypes.',
      badgeColor: 'bg-cyan-950 text-cyan-300 border-cyan-800/40',
    },
    {
      title: 'Healing Status',
      icon: <HeartPulse className="w-4 h-4 text-emerald-400" />,
      prediction: healingStatus,
      prototypes: 'Epithelial Integrity',
      description: 'Granulation tissue, wound edge approximation, and cutaneous integrity.',
      badgeColor:
        healingStatus.label === 'Healed'
          ? 'bg-emerald-950 text-emerald-300 border-emerald-800/40'
          : 'bg-amber-950 text-amber-300 border-amber-800/40',
    },
    {
      title: 'Closure Method',
      icon: <Scissors className="w-4 h-4 text-indigo-400" />,
      prediction: closureMethod,
      prototypes: 'High-Res Crop ViT',
      description: 'Surgical fixation hardware: thread sutures, metallic staples, or adhesives.',
      badgeColor: 'bg-indigo-950 text-indigo-300 border-indigo-800/40',
    },
    {
      title: 'Exudate Discharge',
      icon: <Droplets className="w-4 h-4 text-blue-400" />,
      prediction: exudateType,
      prototypes: 'Color & Texture Stream',
      description: 'Fluid discharge character: serous, sanguineous, or purulent exudate.',
      badgeColor:
        exudateType.label === 'Purulent'
          ? 'bg-red-950 text-red-300 border-red-800/40'
          : exudateType.label !== 'Non-existent'
          ? 'bg-amber-950 text-amber-300 border-amber-800/40'
          : 'bg-slate-900 text-slate-300 border-slate-700',
    },
    {
      title: 'Periwound Erythema',
      icon: <Flame className="w-4 h-4 text-rose-400" />,
      prediction: erythema,
      prototypes: 'Capillary Dilation',
      description: 'Periwound cutaneous redness indicating active inflammatory response.',
      badgeColor:
        erythema.label === 'Existent'
          ? 'bg-rose-950 text-rose-300 border-rose-800/40'
          : 'bg-slate-900 text-slate-300 border-slate-700',
    },
    {
      title: 'Periwound Edema',
      icon: <Maximize className="w-4 h-4 text-violet-400" />,
      prediction: edema,
      prototypes: 'Interstitial Fluid',
      description: 'Localized swelling and margin elevation surrounding the incision.',
      badgeColor:
        edema.label === 'Existent'
          ? 'bg-violet-950 text-violet-300 border-violet-800/40'
          : 'bg-slate-900 text-slate-300 border-slate-700',
    },
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <Info className="w-3.5 h-3.5 text-cyan-400" />
          <span>BiomedCLIP 6-Core Clinical Attributes</span>
        </h3>
        <span className="text-[11px] font-mono text-cyan-400">Multi-Head Joint Predictor</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {cards.map((card, idx) => {
          const confidencePct = Math.round(card.prediction.confidence * 100);

          return (
            <div
              key={idx}
              className="p-4 rounded-xl glass-panel-elevated border border-slate-800/90 hover:border-slate-700 transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-slate-900 border border-slate-800">
                      {card.icon}
                    </div>
                    <span className="text-xs font-semibold text-slate-300">{card.title}</span>
                  </div>

                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${card.badgeColor}`}
                  >
                    {card.prototypes}
                  </span>
                </div>

                <div className="my-2.5">
                  <div className="text-base sm:text-lg font-extrabold text-white tracking-tight">
                    {card.prediction.label}
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
                    {card.description}
                  </p>
                </div>
              </div>

              {/* Confidence Progress Meter */}
              <div className="mt-3 pt-2.5 border-t border-slate-800/70">
                <div className="flex items-center justify-between text-[11px] font-mono mb-1.5">
                  <span className="text-slate-400">Head Confidence</span>
                  <span className="text-cyan-400 font-bold">{confidencePct}%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-cyan-600 to-teal-400 transition-all duration-500"
                    style={{ width: `${confidencePct}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
