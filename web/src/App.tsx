import { useState } from 'react';
import { ShieldAlert, ArrowLeft, Loader2, Download, AlertTriangle } from 'lucide-react';
import { UploadZone } from './components/UploadZone';
import { ResultBanner } from './components/ResultBanner';
import { AttributeCard } from './components/AttributeCard';
import { predictWound, type PredictResponse } from './api/client';

function App() {
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<PredictResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelected = (selectedFile: File) => {
        setFile(selectedFile);
        const objectUrl = URL.createObjectURL(selectedFile);
        setPreview(objectUrl);
        setResult(null);
        setError(null);
    };

    const handleAnalyze = async () => {
        if (!file) return;
        
        setIsLoading(true);
        setError(null);
        
        try {
            const data = await predictWound(file);
            setResult(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || "Failed to analyze image");
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => {
        setFile(null);
        setPreview(null);
        setResult(null);
        setError(null);
    };

    const handleDownloadReport = () => {
        if (!result) return;
        
        const reportContent = `
SurgWound Assist - Assessment Report
====================================

Urgency Level: ${result.urgency_level.label}
Infection Risk: ${result.infection_risk.label}

Attributes:
- Wound Location: ${result.wound_location.label}
- Healing Status: ${result.healing_status.label}
- Closure Method: ${result.closure_method.label}
- Exudate Type: ${result.exudate_type.label}
- Erythema: ${result.erythema.label}
- Edema: ${result.edema.label}

Clinical Summary:
${result.report}

Disclaimer: This tool provides an informational assessment only, is not a medical diagnosis, and does not replace professional evaluation.
        `.trim();
        
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'wound-assessment-report.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="min-h-screen bg-slate-50 text-slate-800">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
                <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2 text-blue-600">
                        <ShieldAlert size={24} />
                        <h1 className="font-bold text-xl tracking-tight">SurgWound Assist</h1>
                    </div>
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-4 py-8">
                {/* Global Medical Disclaimer */}
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-8 flex items-start gap-3">
                    <AlertTriangle className="text-amber-500 shrink-0 mt-0.5" size={20} />
                    <p className="text-sm text-amber-800">
                        <strong>Disclaimer:</strong> This tool provides an informational assessment only, is not a medical diagnosis, 
                        and does not replace professional evaluation. It is built on a research dataset for educational purposes.
                    </p>
                </div>

                {!result ? (
                    <div className="max-w-2xl mx-auto">
                        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8">
                            <h2 className="text-2xl font-bold mb-6 text-center">Post-Operative Wound Assessment</h2>
                            
                            {!preview ? (
                                <UploadZone onFileSelected={handleFileSelected} isLoading={isLoading} />
                            ) : (
                                <div className="space-y-6">
                                    <div className="relative rounded-xl overflow-hidden border border-slate-200 bg-slate-100 flex justify-center items-center h-64 md:h-80">
                                        <img 
                                            src={preview} 
                                            alt="Wound preview" 
                                            className="max-w-full max-h-full object-contain"
                                        />
                                    </div>
                                    
                                    {error && (
                                        <div className="p-4 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200">
                                            {error}
                                        </div>
                                    )}
                                    
                                    <div className="flex gap-4">
                                        <button 
                                            onClick={handleReset}
                                            disabled={isLoading}
                                            className="flex-1 py-3 px-4 border border-slate-300 rounded-lg font-medium text-slate-600 hover:bg-slate-50 transition-colors disabled:opacity-50"
                                        >
                                            Try Another Photo
                                        </button>
                                        <button 
                                            onClick={handleAnalyze}
                                            disabled={isLoading}
                                            className="flex-2 py-3 px-8 bg-blue-600 text-white rounded-lg font-bold shadow-sm hover:bg-blue-700 transition-colors disabled:opacity-70 flex items-center justify-center gap-2 flex-grow"
                                        >
                                            {isLoading ? (
                                                <>
                                                    <Loader2 className="animate-spin" size={20} />
                                                    Analyzing...
                                                </>
                                            ) : (
                                                "Analyze Wound"
                                            )}
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ) : (
                    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        {/* Back Button */}
                        <button 
                            onClick={handleReset}
                            className="flex items-center gap-2 text-slate-500 hover:text-slate-800 transition-colors text-sm font-medium"
                        >
                            <ArrowLeft size={16} />
                            Upload Another Photo
                        </button>
                        
                        {/* Top Banner - Triage */}
                        <ResultBanner 
                            urgency={result.urgency_level} 
                            infectionRisk={result.infection_risk} 
                        />
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Left Column: Image & Report */}
                            <div className="md:col-span-1 space-y-6">
                                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                                    <div className="aspect-square rounded-lg overflow-hidden bg-slate-100 border border-slate-200 mb-4">
                                        <img src={preview!} alt="Analyzed wound" className="w-full h-full object-cover" />
                                    </div>
                                    <h3 className="font-semibold text-slate-800 mb-2">Clinical Summary</h3>
                                    <p className="text-sm text-slate-600 leading-relaxed">
                                        {result.report}
                                    </p>
                                    
                                    <button 
                                        onClick={handleDownloadReport}
                                        className="w-full mt-4 py-2 border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 flex justify-center items-center gap-2"
                                    >
                                        <Download size={16} />
                                        Download Report
                                    </button>
                                </div>
                            </div>
                            
                            {/* Right Column: Attribute Cards */}
                            <div className="md:col-span-2">
                                <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
                                    <AttributeCard title="Location" prediction={result.wound_location} />
                                    <AttributeCard title="Healing Status" prediction={result.healing_status} />
                                    <AttributeCard title="Closure Method" prediction={result.closure_method} />
                                    <AttributeCard title="Exudate Type" prediction={result.exudate_type} />
                                    <AttributeCard title="Erythema" prediction={result.erythema} />
                                    <AttributeCard title="Edema" prediction={result.edema} />
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
