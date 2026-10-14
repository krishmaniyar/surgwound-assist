import React from 'react';
import { Table, ArrowUpRight, CheckCircle2, ShieldCheck } from 'lucide-react';
import { PER_ATTRIBUTE_METRICS } from '../../data/researchData';

export const PerAttributeAnalysis: React.FC = () => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Table className="w-5 h-5 text-cyan-400" />
            <span>Comprehensive Per-Attribute Breakdown Matrix</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Individual performance metrics across all 8 multi-task classification heads (Macro-F1, Accuracy, Precision, Recall, AUC).
          </p>
        </div>
      </div>

      <div className="rounded-2xl glass-panel-elevated border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/90 text-slate-400 font-mono text-[11px] uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="px-4 py-3.5">Clinical Attribute</th>
                <th className="px-3 py-3.5">v7.5 Baseline F1</th>
                <th className="px-3 py-3.5">v8.3 SOTA F1</th>
                <th className="px-3 py-3.5">Delta Gain</th>
                <th className="px-3 py-3.5">Accuracy</th>
                <th className="px-3 py-3.5">Precision</th>
                <th className="px-3 py-3.5">Recall</th>
                <th className="px-3 py-3.5">ROC-AUC</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80 font-sans">
              {PER_ATTRIBUTE_METRICS.map((attr, idx) => {
                const isHighDelta = attr.delta >= 10;

                return (
                  <tr
                    key={idx}
                    className="hover:bg-slate-800/40 transition-colors"
                  >
                    <td className="px-4 py-3.5">
                      <div className="font-bold text-slate-200">
                        {attr.attribute}
                      </div>
                      <div className="text-[11px] text-slate-400 mt-0.5 line-clamp-1">
                        {attr.description}
                      </div>
                    </td>

                    <td className="px-3 py-3.5 font-mono text-slate-400">
                      {attr.v7_5_f1.toFixed(1)}%
                    </td>

                    <td className="px-3 py-3.5 font-mono font-bold text-cyan-300">
                      {attr.v8_sota_f1.toFixed(1)}%
                    </td>

                    <td className="px-3 py-3.5 font-mono">
                      <span
                        className={`inline-flex items-center gap-0.5 px-2 py-0.5 rounded font-bold ${
                          isHighDelta
                            ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/50'
                            : 'bg-slate-900 text-cyan-400 border border-slate-800'
                        }`}
                      >
                        <ArrowUpRight className="w-3 h-3" />
                        +{attr.delta.toFixed(1)}%
                      </span>
                    </td>

                    <td className="px-3 py-3.5 font-mono text-slate-300">
                      {attr.accuracy.toFixed(1)}%
                    </td>

                    <td className="px-3 py-3.5 font-mono text-slate-300">
                      {attr.precision.toFixed(1)}%
                    </td>

                    <td className="px-3 py-3.5 font-mono text-slate-300">
                      {attr.recall.toFixed(1)}%
                    </td>

                    <td className="px-3 py-3.5 font-mono font-bold text-teal-300">
                      {attr.auc.toFixed(4)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="p-3.5 bg-slate-900/60 border-t border-slate-800 text-[11px] text-slate-400 flex flex-wrap items-center justify-between gap-3">
          <span className="flex items-center gap-1.5 font-mono">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            Minority-Heads Macro-F1 (Exudate, Infection, Closure, Edema): <strong>47.11%</strong> (vs 24.26% Baseline)
          </span>
          <span className="font-mono text-slate-500">
            Validation Protocol: 7× TTA with Cosine Calibrated Thresholds
          </span>
        </div>
      </div>
    </div>
  );
};
