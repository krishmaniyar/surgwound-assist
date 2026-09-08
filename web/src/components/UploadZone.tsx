import { useCallback, type FC } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Camera, FileImage } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface UploadZoneProps {
    onFileSelected: (file: File) => void;
    isLoading: boolean;
}

export const UploadZone: FC<UploadZoneProps> = ({ onFileSelected, isLoading }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            onFileSelected(acceptedFiles[0]);
        }
    }, [onFileSelected]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.jpg', '.png']
        },
        multiple: false,
        disabled: isLoading
    });

    return (
        <div
            {...getRootProps()}
            className={cn(
                "w-full p-8 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all duration-200 ease-in-out cursor-pointer",
                isDragActive ? "border-blue-500 bg-blue-50" : "border-slate-300 bg-white hover:border-slate-400 hover:bg-slate-50",
                isLoading && "opacity-50 cursor-not-allowed"
            )}
        >
            <input {...getInputProps()} capture="environment" />
            
            <div className="flex gap-4 mb-4 text-slate-400">
                <Camera size={32} />
                <FileImage size={32} />
                <Upload size={32} />
            </div>
            
            <h3 className="text-lg font-semibold text-slate-700 mb-2">
                {isDragActive ? "Drop the photo here" : "Upload Wound Photo"}
            </h3>
            
            <p className="text-sm text-slate-500 text-center max-w-sm">
                Drag and drop a clear photo of the wound, or click to browse files or use your camera.
            </p>
        </div>
    );
};
