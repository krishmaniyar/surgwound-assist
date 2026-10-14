import React, { useState } from 'react';
import { 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Sun, 
  Layers, 
  Scan, 
  Sparkles,
  Maximize2
} from 'lucide-react';

interface ImageViewerProps {
  imageSrc: string;
  isAnalyzing?: boolean;
}

export const ImageViewer: React.FC<ImageViewerProps> = ({ imageSrc, isAnalyzing }) => {
  const [zoom, setZoom] = useState<number>(1);
  const [highContrast, setHighContrast] = useState<boolean>(false);
  const [showMultiScaleCrop, setShowMultiScaleCrop] = useState<boolean>(true);
  const [showGrid, setShowGrid] = useState<boolean>(false);
  const [inverted, setInverted] = useState<boolean>(false);

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 0.25, 2.5));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 0.25, 0.75));
  const handleReset = () => {
    setZoom(1);
    setHighContrast(false);
    setInverted(false);
    setShowGrid(false);
    setShowMultiScaleCrop(true);
  };

  return (
    <div className="relative flex flex-col rounded-2xl glass-panel-elevated overflow-hidden border border-slate-800">
      {/* Viewer Header / Toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 text-xs text-slate-300">
        <div className="flex items-center gap-2">
          <Scan className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-slate-200">Clinical Image Inspector</span>
          <span className="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 font-mono text-[10px] border border-cyan-800/40">
            224×224 Dual-ViT
          </span>
        </div>

        {/* Toolbar Controls */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setShowMultiScaleCrop(!showMultiScaleCrop)}
            className={`px-2 py-1 rounded flex items-center gap-1 text-[11px] transition-colors ${
              showMultiScaleCrop
                ? 'bg-cyan-600/30 text-cyan-300 border border-cyan-500/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Toggle 65% Local Wound-Bed Crop Bounding Box"
          >
            <Layers className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Multi-Scale Crop</span>
          </button>

          <button
            onClick={() => setHighContrast(!highContrast)}
            className={`p-1.5 rounded transition-colors ${
              highContrast
                ? 'bg-amber-600/30 text-amber-300 border border-amber-500/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Enhance Erythema & Vascular Contrast"
          >
            <Sun className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setInverted(!inverted)}
            className={`p-1.5 rounded transition-colors ${
              inverted
                ? 'bg-purple-600/30 text-purple-300 border border-purple-500/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Invert Tonal Radiance (Exudate Inspection)"
          >
            <Sparkles className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setShowGrid(!showGrid)}
            className={`p-1.5 rounded transition-colors ${
              showGrid
                ? 'bg-teal-600/30 text-teal-300 border border-teal-500/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Toggle Clinical Dimension Grid"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>

          <div className="h-4 w-px bg-slate-800 mx-1" />

          <button
            onClick={handleZoomOut}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded"
            title="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="font-mono text-[11px] text-slate-400 w-8 text-center">
            {Math.round(zoom * 100)}%
          </span>
          <button
            onClick={handleZoomIn}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded"
            title="Zoom In"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={handleReset}
            className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded"
            title="Reset Controls"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Image Canvas Viewport */}
      <div className="relative w-full h-[380px] sm:h-[440px] bg-slate-950 flex items-center justify-center overflow-hidden scanline">
        {/* Dimension Grid Overlay */}
        {showGrid && (
          <div 
            className="absolute inset-0 pointer-events-none z-10 opacity-30"
            style={{
              backgroundImage: 'linear-gradient(to right, #0891b2 1px, transparent 1px), linear-gradient(to bottom, #0891b2 1px, transparent 1px)',
              backgroundSize: '28px 28px'
            }}
          />
        )}

        {/* The Surgical Image */}
        <div 
          className="relative transition-transform duration-200 ease-out flex items-center justify-center"
          style={{ transform: `scale(${zoom})` }}
        >
          <img
            src={imageSrc}
            alt="Surgical Wound Subject"
            className={`max-w-full max-h-[360px] sm:max-h-[420px] object-contain rounded-lg transition-all duration-300 ${
              highContrast ? 'contrast-150 brightness-110 saturate-125' : ''
            } ${inverted ? 'invert hue-rotate-180' : ''}`}
          />

          {/* v8.2 Multi-Scale High-Resolution Crop Bounding Box Visualizer */}
          {showMultiScaleCrop && (
            <div className="absolute inset-[17%] border-2 border-dashed border-cyan-400/90 bg-cyan-500/10 rounded-lg pointer-events-none transition-all animate-pulse">
              <div className="absolute -top-3 left-2 px-1.5 py-0.5 rounded bg-cyan-900/95 text-cyan-200 text-[10px] font-mono border border-cyan-500/60 shadow">
                v8.2 High-Res 65% Wound-Bed Crop
              </div>
              <div className="absolute -bottom-3 right-2 px-1.5 py-0.5 rounded bg-slate-900/95 text-slate-300 text-[9px] font-mono border border-slate-700">
                1024-dim Fusion Layer
              </div>
            </div>
          )}
        </div>

        {/* Live Analysis Scan Line animation */}
        {isAnalyzing && (
          <div className="absolute inset-0 pointer-events-none z-20 flex flex-col justify-between bg-cyan-950/20 backdrop-blur-[1px]">
            <div className="w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_15px_#22d3ee] animate-bounce" />
            <div className="p-4 text-center">
              <span className="px-3 py-1 rounded-full bg-slate-900/90 text-cyan-300 text-xs font-mono border border-cyan-500/50 shadow-lg inline-flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                Extracting Dual-Stream BiomedCLIP Features & Semantic Prototypes...
              </span>
            </div>
            <div className="w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_15px_#22d3ee] animate-bounce" />
          </div>
        )}
      </div>

      {/* Footer Info Pill */}
      <div className="px-4 py-2 bg-slate-900/80 border-t border-slate-800 text-[11px] text-slate-400 flex flex-wrap items-center justify-between gap-2">
        <span className="flex items-center gap-1.5 font-mono">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
          Backbone: Shared BiomedCLIP ViT-B/16 (203.4M params)
        </span>
        <span className="text-slate-500">
          Native Resolution: 640×853 $\to$ Normalized Multi-Crop
        </span>
      </div>
    </div>
  );
};
