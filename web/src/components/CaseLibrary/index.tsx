import React from 'react';
import { BookOpen, ArrowRight, ShieldCheck, AlertTriangle, AlertOctagon, CheckCircle2 } from 'lucide-react';
import { CLINICAL_SAMPLE_CASES } from '../../data/researchData';
import { ClinicalSampleCase } from '../../types/clinical';

interface CaseLibraryProps {
  onSelectCase: (sampleCase: ClinicalSampleCase) => void;
}

export const CaseLibrary: React.FC<CaseLibraryProps> = ({ onSelectCase }) => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <span>Curated Clinical Benchmark Case Library</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Real surgical wound profiles with known clinical outcomes for validation and testing.
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full bg-cyan-950 text-cyan-300 font-mono text-xs border border-cyan-800/60">
          3 Clinical Profiles Ready
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {CLINICAL_SAMPLE_CASES.map((sampleCase) => {
          const isRed = sampleCase.urgency.includes('Red');
          const isYellow = sampleCase.urgency.includes('Yellow');

          return (
            <div
              key={sampleCase.id}
              className={`rounded-2xl glass-panel-elevated p-6 border transition-all duration-300 flex flex-col justify-between ${
                isRed
                  ? 'border-red-900/50 hover:border-red-500/70'
                  : isYellow
                  ? 'border-amber-900/50 hover:border-amber-500/70'
                  : 'border-emerald-900/50 hover:border-emerald-500/70'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-black uppercase tracking-wider border ${
                      isRed
                        ? 'bg-red-900/40 text-red-300 border-red-700/60'
                        : isYellow
                        ? 'bg-amber-900/40 text-amber-300 border-amber-700/60'
                        : 'bg-emerald-900/40 text-emerald-300 border-emerald-700/60'
                    }`}
                  >
                    {sampleCase.urgency}
                  </span>

                  <span className="text-xs font-mono text-slate-400 px-2 py-0.5 rounded bg-slate-900 border border-slate-800">
                    {sampleCase.location}
                  </span>
                </div>

                <h4 className="text-base font-extrabold text-white mb-2">
                  {sampleCase.title}
                </h4>

                <p className="text-xs text-slate-300 leading-relaxed mb-4">
                  {sampleCase.patientProfile}
                </p>

                {/* Clinical Notes Card */}
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 space-y-1 mb-4">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
                    Physician Clinical Notes
                  </span>
                  <p className="text-[11px] leading-relaxed text-slate-300">
                    {sampleCase.clinicalNotes}
                  </p>
                </div>

                {/* Key Attributes Overview */}
                <div className="space-y-1.5 text-xs font-mono text-slate-300 border-t border-slate-800/80 pt-3">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Infection Risk:</span>
                    <span
                      className={`font-bold ${
                        sampleCase.infectionRisk === 'High'
                          ? 'text-red-400'
                          : sampleCase.infectionRisk === 'Medium'
                          ? 'text-amber-400'
                          : 'text-emerald-400'
                      }`}
                    >
                      {sampleCase.infectionRisk}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-slate-400">Closure Method:</span>
                    <span className="text-slate-200">{sampleCase.assessment.closure_method.label}</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-slate-400">Exudate Status:</span>
                    <span className="text-slate-200">{sampleCase.assessment.exudate_type.label}</span>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <button
                onClick={() => onSelectCase(sampleCase)}
                className="mt-6 w-full py-2.5 px-4 rounded-xl text-xs font-bold bg-cyan-600 hover:bg-cyan-500 text-white transition-all shadow-md shadow-cyan-950/60 flex items-center justify-center gap-2 group"
              >
                <span>Load & Inspect in Diagnostic Studio</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
