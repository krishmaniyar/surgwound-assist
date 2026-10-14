import React, { useState, useEffect } from 'react';
import { Header, ActiveTab } from './components/Header';
import { ImageViewer } from './components/DiagnosticStudio/ImageViewer';
import { ImageUploader } from './components/DiagnosticStudio/ImageUploader';
import { TriageBanner } from './components/DiagnosticStudio/TriageBanner';
import { AttributeMatrix } from './components/DiagnosticStudio/AttributeMatrix';
import { ClinicalSummaryReport } from './components/DiagnosticStudio/ClinicalSummaryReport';
import { WhatHappenedSection } from './components/WhatHappenedSection';
import { PipelineTelemetry } from './components/PipelineTelemetry';
import { CaseLibrary } from './components/CaseLibrary';
import { Footer } from './components/Footer';
import { checkBackendHealth, analyzeWoundImage, BackendHealth } from './api/client';
import { SurgWoundAssessment, ClinicalSampleCase } from './types/clinical';
import { AlertCircle, RefreshCw, Sparkles } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('studio');
  const [backendHealth, setBackendHealth] = useState<BackendHealth>({
    isOnline: false,
    message: 'Checking API status...',
    endpoint: 'http://localhost:8000',
  });

  const [imageBlobUrl, setImageBlobUrl] = useState<string | null>(null);
  const [assessment, setAssessment] = useState<SurgWoundAssessment | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Check backend health on initial load
  useEffect(() => {
    checkBackendHealth().then((health) => setBackendHealth(health));
    const interval = setInterval(() => {
      checkBackendHealth().then((health) => setBackendHealth(health));
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleImageSelected = async (file: File | Blob, caseId?: string) => {
    // Revoke previous blob if exists
    if (imageBlobUrl && imageBlobUrl.startsWith('blob:')) {
      URL.revokeObjectURL(imageBlobUrl);
    }

    const previewUrl = URL.createObjectURL(file);
    setImageBlobUrl(previewUrl);
    setIsAnalyzing(true);
    setErrorMessage(null);

    try {
      const result = await analyzeWoundImage(file, caseId);
      setAssessment(result);
    } catch (err: any) {
      setErrorMessage(err.message || 'Inference failed. Please try another image.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    if (imageBlobUrl && imageBlobUrl.startsWith('blob:')) {
      URL.revokeObjectURL(imageBlobUrl);
    }
    setImageBlobUrl(null);
    setAssessment(null);
    setErrorMessage(null);
  };

  const handleSelectCaseFromLibrary = (sampleCase: ClinicalSampleCase) => {
    // Switch to studio tab and populate assessment
    setActiveTab('studio');
    // Generate canvas blob for this case
    const canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      const gradient = ctx.createLinearGradient(0, 0, 640, 480);
      gradient.addColorStop(0, '#cda185');
      gradient.addColorStop(1, '#be9074');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 640, 480);

      if (sampleCase.urgency.includes('Red')) {
        ctx.fillStyle = 'rgba(180, 20, 20, 0.7)';
        ctx.beginPath();
        ctx.ellipse(320, 240, 160, 60, Math.PI / 12, 0, 2 * Math.PI);
        ctx.fill();

        ctx.fillStyle = '#6b1111';
        ctx.beginPath();
        ctx.ellipse(320, 240, 120, 25, Math.PI / 12, 0, 2 * Math.PI);
        ctx.fill();

        ctx.fillStyle = '#e8d489';
        ctx.beginPath();
        ctx.arc(310, 235, 14, 0, 2 * Math.PI);
        ctx.arc(345, 245, 10, 0, 2 * Math.PI);
        ctx.fill();
      } else if (sampleCase.urgency.includes('Yellow')) {
        ctx.fillStyle = 'rgba(210, 80, 80, 0.45)';
        ctx.beginPath();
        ctx.ellipse(320, 240, 140, 50, -Math.PI / 16, 0, 2 * Math.PI);
        ctx.fill();

        ctx.strokeStyle = '#7c2525';
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(220, 230);
        ctx.lineTo(420, 250);
        ctx.stroke();

        ctx.strokeStyle = '#2b2b2b';
        ctx.lineWidth = 2;
        for (let x = 240; x <= 400; x += 30) {
          ctx.beginPath();
          ctx.moveTo(x, 220);
          ctx.lineTo(x, 260);
          ctx.stroke();
        }
      } else {
        ctx.strokeStyle = '#8a5a44';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(220, 240);
        ctx.lineTo(420, 240);
        ctx.stroke();

        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.beginPath();
        ctx.ellipse(320, 240, 110, 20, 0, 0, 2 * Math.PI);
        ctx.fill();
      }

      canvas.toBlob((blob) => {
        if (blob) {
          handleImageSelected(blob, sampleCase.id);
        }
      }, 'image/jpeg');
    }
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/20 selection:text-cyan-300">
      <Header
        activeTab={activeTab}
        onTabChange={(tab) => setActiveTab(tab)}
        backendHealth={backendHealth}
        onReset={handleReset}
        hasActiveResult={!!assessment}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Error banner if inference fails */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/40 border border-red-800 text-red-200 text-sm flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-xs text-red-400 hover:text-red-200 underline font-mono"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Tab 1: Clinical Diagnostic Studio */}
        {activeTab === 'studio' && (
          <div className="space-y-6">
            {!imageBlobUrl ? (
              <div className="max-w-4xl mx-auto space-y-6">
                <div className="text-center space-y-2">
                  <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                    Autonomous Multi-Attribute Surgical Wound Assessment
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto">
                    Evaluate surgical incisions across 8 clinical variables with dual-stream BiomedCLIP ViT-B/16, 
                    PubMedBERT semantic prototypes, and calibrated triage classification.
                  </p>
                </div>

                <ImageUploader
                  onImageSelected={handleImageSelected}
                  isLoading={isAnalyzing}
                />
              </div>
            ) : (
              <div className="space-y-6 animate-in fade-in duration-300">
                {/* Triage Urgency Priority Banner */}
                {assessment && (
                  <TriageBanner
                    urgency={assessment.urgency_level}
                    infectionRisk={assessment.infection_risk}
                    processingTimeMs={assessment.processingTimeMs}
                  />
                )}

                {/* 2-Column Clinical Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                  {/* Left Column (5/12): Image Viewport */}
                  <div className="lg:col-span-5 space-y-4">
                    <ImageViewer imageSrc={imageBlobUrl} isAnalyzing={isAnalyzing} />

                    <div className="flex items-center justify-between">
                      <button
                        onClick={handleReset}
                        className="text-xs text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1.5"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        <span>Upload Different Wound Photo</span>
                      </button>

                      <span className="text-[11px] font-mono text-slate-400">
                        {assessment?.modelArchitecture || 'BiomedCLIP v8.3 SOTA'}
                      </span>
                    </div>
                  </div>

                  {/* Right Column (7/12): 8 Attributes & Clinical Synthesis */}
                  <div className="lg:col-span-7 space-y-6">
                    {assessment ? (
                      <>
                        <AttributeMatrix
                          location={assessment.wound_location}
                          healingStatus={assessment.healing_status}
                          closureMethod={assessment.closure_method}
                          exudateType={assessment.exudate_type}
                          erythema={assessment.erythema}
                          edema={assessment.edema}
                        />

                        <ClinicalSummaryReport assessment={assessment} />
                      </>
                    ) : (
                      <div className="h-72 rounded-2xl glass-panel-elevated flex flex-col items-center justify-center p-8 text-center space-y-3">
                        <div className="w-10 h-10 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin" />
                        <span className="text-sm font-semibold text-cyan-300 font-mono">
                          Synthesizing 8 Multi-Task Predictions...
                        </span>
                        <span className="text-xs text-slate-400">
                          Aligning high-res crop textures with PubMedBERT semantic prototypes
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: What Happened & Autonomous Research Audit */}
        {activeTab === 'audit' && <WhatHappenedSection />}

        {/* Tab 3: End-to-End Pipeline Telemetry */}
        {activeTab === 'telemetry' && <PipelineTelemetry />}

        {/* Tab 4: Curated Clinical Case Library */}
        {activeTab === 'cases' && (
          <CaseLibrary onSelectCase={handleSelectCaseFromLibrary} />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
