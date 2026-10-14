import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, Clock, Zap, ArrowRightCircle } from 'lucide-react';
import { AttributePrediction } from '../../types/clinical';

interface TriageBannerProps {
  urgency: AttributePrediction;
  infectionRisk: AttributePrediction;
  processingTimeMs: number;
}

export const TriageBanner: React.FC<TriageBannerProps> = ({
  urgency,
  infectionRisk,
  processingTimeMs,
}) => {
  const isRed = urgency.label.includes('Red') || urgency.label.includes('Emergency');
  const isYellow = urgency.label.includes('Yellow') || urgency.label.includes('Clinic');

  const theme = isRed
    ? {
        bg: 'bg-red-950/40',
        border: 'border-red-600/60',
        glow: 'shadow-[0_0_30px_-5px_rgba(239,68,68,0.25)]',
        badgeBg: 'bg-red-600',
        badgeText: 'text-white',
        titleColor: 'text-red-200',
        icon: <ShieldAlert className="w-8 h-8 text-red-400 shrink-0 animate-bounce" />,
        actionText: 'Urgent Surgical Team Escalation Required',
        pathway:
          'High probability of acute surgical site complication or deep tissue involvement. Do not delay.',
      }
    : isYellow
    ? {
        bg: 'bg-amber-950/40',
        border: 'border-amber-600/60',
        glow: 'shadow-[0_0_30px_-5px_rgba(245,158,11,0.25)]',
        badgeBg: 'bg-amber-500',
        badgeText: 'text-slate-950',
        titleColor: 'text-amber-200',
        icon: <AlertTriangle className="w-8 h-8 text-amber-400 shrink-0" />,
        actionText: 'Schedule In-Person Outpatient Clinical Review (<48h)',
        pathway:
          'Observable periwound inflammation, erythema, or serous drainage. Requires margin tracing.',
      }
    : {
        bg: 'bg-emerald-950/40',
        border: 'border-emerald-600/60',
        glow: 'shadow-[0_0_30px_-5px_rgba(16,185,129,0.25)]',
        badgeBg: 'bg-emerald-600',
        badgeText: 'text-white',
        titleColor: 'text-emerald-200',
        icon: <CheckCircle className="w-8 h-8 text-emerald-400 shrink-0" />,
        actionText: 'Standard Post-Operative Home Care Protocol',
        pathway:
          'Clean, appropriately approximated wound edges. Continue scheduled wound hygiene and monitoring.',
      };

  return (
    <div
      className={`rounded-2xl p-5 sm:p-6 border ${theme.bg} ${theme.border} ${theme.glow} transition-all duration-300 relative overflow-hidden`}
    >
      {/* Background visual element */}
      <div className="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-white/5 blur-2xl pointer-events-none" />

      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-5">
        {/* Left Side: Priority Level */}
        <div className="flex items-start sm:items-center gap-4">
          <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-700/80 shadow-md">
            {theme.icon}
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span
                className={`px-3 py-1 rounded-full text-xs font-black tracking-wider uppercase ${theme.badgeBg} ${theme.badgeText} shadow-sm`}
              >
                {urgency.label}
              </span>

              <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-900/80 text-slate-300 border border-slate-700">
                Confidence: {(urgency.confidence * 100).toFixed(1)}%
              </span>

              <span className="text-xs font-mono text-slate-400 flex items-center gap-1">
                <Clock className="w-3 h-3 text-cyan-400" />
                {processingTimeMs}ms inference
              </span>
            </div>

            <h2 className={`text-lg sm:text-xl font-extrabold tracking-tight ${theme.titleColor}`}>
              {theme.actionText}
            </h2>

            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
              {theme.pathway}
            </p>
          </div>
        </div>

        {/* Right Side: Infection Risk Badge */}
        <div className="shrink-0 flex sm:flex-col items-center sm:items-end justify-between border-t sm:border-t-0 sm:border-l border-slate-800/80 pt-3 sm:pt-0 sm:pl-6">
          <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold mb-1">
            Infection Risk Rating
          </span>
          <div className="flex items-center gap-2">
            <span
              className={`text-base sm:text-lg font-black tracking-tight ${
                infectionRisk.label === 'High'
                  ? 'text-red-400'
                  : infectionRisk.label === 'Medium'
                  ? 'text-amber-400'
                  : 'text-emerald-400'
              }`}
            >
              {infectionRisk.label.toUpperCase()} RISK
            </span>
            <span className="text-xs font-mono text-slate-400">
              ({(infectionRisk.confidence * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-[10px] text-slate-400 font-mono mt-1">
            Logit-Adjusted Decision Head
          </span>
        </div>
      </div>
    </div>
  );
};
