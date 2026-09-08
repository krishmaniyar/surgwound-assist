import type { FC } from 'react';
import { AlertCircle, CheckCircle, Clock } from 'lucide-react';
import type { AttributePrediction } from '../api/client';

interface ResultBannerProps {
    urgency: AttributePrediction;
    infectionRisk: AttributePrediction;
}

export const ResultBanner: FC<ResultBannerProps> = ({ urgency, infectionRisk }) => {
    // Map urgency to styling
    let bgColor = 'triage-green';
    let Icon = CheckCircle;
    let title = 'Home Care';
    let subtitle = 'Manage with routine care';
    
    const label = urgency.label.toLowerCase();
    if (label.includes('yellow') || label.includes('clinic')) {
        bgColor = 'triage-yellow';
        Icon = Clock;
        title = 'Clinic Visit';
        subtitle = 'Requires professional evaluation within 48 hours';
    } else if (label.includes('red') || label.includes('emergency')) {
        bgColor = 'triage-red';
        Icon = AlertCircle;
        title = 'Emergency Care';
        subtitle = 'Seek immediate medical attention';
    }
    
    // Risk styling
    let riskColor = 'bg-slate-100 text-slate-700';
    if (infectionRisk.label.toLowerCase() === 'high') {
        riskColor = 'bg-red-100 text-red-800 border border-red-200';
    } else if (infectionRisk.label.toLowerCase() === 'medium') {
        riskColor = 'bg-yellow-100 text-yellow-800 border border-yellow-200';
    } else {
        riskColor = 'bg-green-100 text-green-800 border border-green-200';
    }

    return (
        <div className={`w-full p-6 rounded-xl border ${bgColor} flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-sm`}>
            <div className="flex items-center gap-4">
                <Icon size={40} className="shrink-0" />
                <div>
                    <h2 className="text-2xl font-bold">{title}</h2>
                    <p className="text-sm font-medium opacity-90">{subtitle}</p>
                </div>
            </div>
            
            <div className="flex flex-col items-end">
                <span className="text-xs font-semibold uppercase tracking-wider mb-1 opacity-75">Infection Risk</span>
                <span className={`px-4 py-1.5 rounded-full text-sm font-bold ${riskColor}`}>
                    {infectionRisk.label.toUpperCase()}
                </span>
            </div>
        </div>
    );
};
