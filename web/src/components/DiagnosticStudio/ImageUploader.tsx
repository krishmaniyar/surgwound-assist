import React, { useRef, useState } from 'react';
import { UploadCloud, Image as ImageIcon, Sparkles, FileText, CheckCircle2 } from 'lucide-react';
import { CLINICAL_SAMPLE_CASES } from '../../data/researchData';
import { ClinicalSampleCase } from '../../types/clinical';

interface ImageUploaderProps {
  onImageSelected: (file: File | Blob, caseId?: string) => void;
  isLoading: boolean;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageSelected, isLoading }) => {
  const [isDragOver, setIsDragOver] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        onImageSelected(file);
      }
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onImageSelected(e.target.files[0]);
    }
  };

  const handleSelectSampleCase = async (sampleCase: ClinicalSampleCase) => {
    // Generate a simulated SVG wound canvas blob representing the sample case
    const canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      // Background skin tone
      const gradient = ctx.createLinearGradient(0, 0, 640, 480);
      gradient.addColorStop(0, '#cda185');
      gradient.addColorStop(1, '#be9074');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 640, 480);

      // Wound site based on case severity
      if (sampleCase.urgency.includes('Red')) {
        // Severe erythema & purulent exudate
        ctx.fillStyle = 'rgba(180, 20, 20, 0.7)';
        ctx.beginPath();
        ctx.ellipse(320, 240, 160, 60, Math.PI / 12, 0, 2 * Math.PI);
        ctx.fill();

        ctx.fillStyle = '#6b1111';
        ctx.beginPath();
        ctx.ellipse(320, 240, 120, 25, Math.PI / 12, 0, 2 * Math.PI);
        ctx.fill();

        // Purulent spots
        ctx.fillStyle = '#e8d489';
        ctx.beginPath();
        ctx.arc(310, 235, 14, 0, 2 * Math.PI);
        ctx.arc(345, 245, 10, 0, 2 * Math.PI);
        ctx.fill();
      } else if (sampleCase.urgency.includes('Yellow')) {
        // Moderate erythema
        ctx.fillStyle = 'rgba(210, 80, 80, 0.45)';
        ctx.beginPath();
        ctx.ellipse(320, 240, 140, 50, -Math.PI / 16, 0, 2 * Math.PI);
        ctx.fill();

        // Incision line
        ctx.strokeStyle = '#7c2525';
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(220, 230);
        ctx.lineTo(420, 250);
        ctx.stroke();

        // Cross sutures
        ctx.strokeStyle = '#2b2b2b';
        ctx.lineWidth = 2;
        for (let x = 240; x <= 400; x += 30) {
          ctx.beginPath();
          ctx.moveTo(x, 220);
          ctx.lineTo(x, 260);
          ctx.stroke();
        }
      } else {
        // Clean healed wound
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
          onImageSelected(blob, sampleCase.id);
        }
      }, 'image/jpeg');
    }
  };

  return (
    <div className="space-y-6">
      {/* Main Drag-and-Drop Dropzone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center p-8 sm:p-12 rounded-2xl border-2 border-dashed transition-all duration-300 cursor-pointer ${
          isDragOver
            ? 'border-cyan-400 bg-cyan-950/40 scale-[1.01]'
            : 'border-slate-700/80 hover:border-cyan-500/70 bg-slate-900/40 hover:bg-slate-900/70'
        } ${isLoading ? 'pointer-events-none opacity-60' : ''}`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          accept="image/*"
          className="hidden"
        />

        <div className="w-16 h-16 mb-4 rounded-2xl bg-gradient-to-tr from-cyan-900/60 to-slate-800 flex items-center justify-center border border-cyan-500/30 shadow-inner group">
          <UploadCloud className="w-8 h-8 text-cyan-400 group-hover:scale-110 transition-transform" />
        </div>

        <h3 className="text-base sm:text-lg font-bold text-slate-100 mb-1">
          Upload Post-Operative Surgical Wound Photo
        </h3>
        <p className="text-xs sm:text-sm text-slate-400 text-center max-w-md mb-4">
          Drag & drop high-resolution incision photography, or click to browse.
          Supports standard clinical JPG, PNG, and WebP formats.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-2 text-[11px] font-mono text-slate-400">
          <span className="px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700">
            BiomedCLIP Dual-ViT
          </span>
          <span className="px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700">
            8 Joint Clinical Heads
          </span>
          <span className="px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700">
            Automated SSI Risk
          </span>
        </div>
      </div>

      {/* Pre-Curated Clinical Test Cases (Instant 1-Click Evaluation) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Instant Evaluation: Pre-Curated Benchmark Cases</span>
          </div>
          <span className="text-xs text-cyan-400">1-Click Test</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {CLINICAL_SAMPLE_CASES.map((sampleCase) => {
            const isRed = sampleCase.urgency.includes('Red');
            const isYellow = sampleCase.urgency.includes('Yellow');

            return (
              <div
                key={sampleCase.id}
                onClick={() => handleSelectSampleCase(sampleCase)}
                className={`p-3.5 rounded-xl border text-left cursor-pointer transition-all duration-200 glass-card-interactive ${
                  isRed
                    ? 'border-red-900/60 bg-red-950/20 hover:border-red-500/80'
                    : isYellow
                    ? 'border-amber-900/60 bg-amber-950/20 hover:border-amber-500/80'
                    : 'border-emerald-900/60 bg-emerald-950/20 hover:border-emerald-500/80'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase border ${
                      isRed
                        ? 'bg-red-900/50 text-red-300 border-red-700/60'
                        : isYellow
                        ? 'bg-amber-900/50 text-amber-300 border-amber-700/60'
                        : 'bg-emerald-900/50 text-emerald-300 border-emerald-700/60'
                    }`}
                  >
                    {isRed ? 'Acute Emergency' : isYellow ? 'Clinic Review' : 'Home Care'}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    {sampleCase.location}
                  </span>
                </div>

                <h4 className="text-xs font-semibold text-slate-200 mb-1 line-clamp-1">
                  {sampleCase.title}
                </h4>
                <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                  {sampleCase.patientProfile}
                </p>

                <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                  <span className="text-slate-400">
                    Infection Risk: <strong className="text-slate-200">{sampleCase.infectionRisk}</strong>
                  </span>
                  <span className="text-cyan-400 font-medium hover:underline flex items-center gap-1">
                    Load Case →
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
