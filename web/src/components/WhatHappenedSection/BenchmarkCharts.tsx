import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Legend,
  Cell
} from 'recharts';
import { BarChart3, TrendingUp, Sparkles, Award } from 'lucide-react';
import { RESEARCH_MILESTONES, PER_ATTRIBUTE_METRICS } from '../../data/researchData';

export const BenchmarkCharts: React.FC = () => {
  // Timeline comparison data
  const timelineChartData = RESEARCH_MILESTONES.map((m) => ({
    version: m.version,
    macroF1: m.macroF1,
    minorityHeads: m.minorityHeadsF1,
    accuracy: m.meanAccuracy,
    exactMatch: m.exactMatchRatio,
  }));

  // Per-attribute comparison data
  const attributeComparisonData = PER_ATTRIBUTE_METRICS.map((attr) => ({
    name: attr.attribute.replace(' (Redness)', '').replace(' (Swelling)', ''),
    Baseline_v7_5: attr.v7_5_f1,
    SOTA_v8_3: attr.v8_sota_f1,
    Delta: attr.delta,
  }));

  const customTooltipStyle = {
    backgroundColor: '#0f172a',
    borderColor: '#334155',
    borderRadius: '12px',
    color: '#f8fafc',
    fontSize: '12px',
    fontFamily: 'monospace',
    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.5)',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            <span>Empirical Benchmark Comparisons: v7.5 Baseline vs v8 SOTA</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Statistical validation on 349-image multi-hospital SurgWound evaluation split.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Overall Macro-F1 & Minority Heads Leap */}
        <div className="rounded-2xl glass-panel-elevated p-5 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-bold text-slate-200">
                Macro-F1 & Minority Attribute Progression
              </h4>
              <span className="text-[11px] text-slate-400">
                Critical minority heads: Exudate, Infection, Closure, Edema
              </span>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-800/50">
              +16.99% Minority F1
            </span>
          </div>

          <div className="h-64 sm:h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={timelineChartData} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="version" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 70]} />
                <Tooltip contentStyle={customTooltipStyle} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="macroF1" name="Mean Macro-F1 (%)" fill="#0891b2" radius={[4, 4, 0, 0]}>
                  {timelineChartData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={index === timelineChartData.length - 1 ? '#22d3ee' : '#0891b2'} 
                    />
                  ))}
                </Bar>
                <Bar dataKey="minorityHeads" name="Minority Heads F1 (%)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Per-Attribute Baseline vs SOTA Head-to-Head */}
        <div className="rounded-2xl glass-panel-elevated p-5 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-bold text-slate-200">
                Head-to-Head Attribute Improvement (Macro-F1)
              </h4>
              <span className="text-[11px] text-slate-400">
                v7.5 BiomedCLIP Baseline vs v8.3 Deep Multi-Scale Ensemble
              </span>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800/50">
              +36.2% Infection
            </span>
          </div>

          <div className="h-64 sm:h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={attributeComparisonData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="name" 
                  stroke="#94a3b8" 
                  fontSize={10} 
                  angle={-25} 
                  textAnchor="end" 
                  interval={0} 
                />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                <Tooltip contentStyle={customTooltipStyle} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '15px' }} />
                <Bar dataKey="Baseline_v7_5" name="v7.5 Baseline (%)" fill="#475569" radius={[4, 4, 0, 0]} />
                <Bar dataKey="SOTA_v8_3" name="v8.3 SOTA (%)" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
