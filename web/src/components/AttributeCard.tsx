import type { FC } from 'react';
import type { AttributePrediction } from '../api/client';

interface AttributeCardProps {
    title: string;
    prediction: AttributePrediction;
}

export const AttributeCard: FC<AttributeCardProps> = ({ title, prediction }) => {
    const confidencePct = Math.round(prediction.confidence * 100);
    
    return (
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between h-full">
            <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{title}</h3>
                <p className="text-lg font-bold text-slate-800 mb-4">{prediction.label}</p>
            </div>
            
            <div>
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                    <span>Confidence</span>
                    <span className="font-medium">{confidencePct}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-1.5">
                    <div 
                        className="bg-blue-500 h-1.5 rounded-full transition-all duration-1000 ease-out" 
                        style={{ width: `${confidencePct}%` }}
                    />
                </div>
            </div>
        </div>
    );
};
