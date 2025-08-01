import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  DocumentArrowUpIcon,
  CloudArrowUpIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

interface ResumeUploadStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const ResumeUploadStep: React.FC<ResumeUploadStepProps> = ({ onNext }) => {
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'processing' | 'success' | 'error'>('idle');
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [processingProgress, setProcessingProgress] = useState(0);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
    if (!validTypes.includes(file.type)) {
      setUploadState('error');
      return;
    }

    setUploadedFile(file);
    setUploadState('uploading');

    // Simulate upload progress
    for (let i = 0; i <= 100; i += 10) {
      setProcessingProgress(i);
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    setUploadState('processing');
    setProcessingProgress(0);

    // Simulate AI processing
    for (let i = 0; i <= 100; i += 5) {
      setProcessingProgress(i);
      await new Promise(resolve => setTimeout(resolve, 150));
    }

    setUploadState('success');
  };

  const proceedWithParsedData = () => {
    // In a real implementation, this would pass the parsed data to the profile
    onNext();
  };

  const skipUpload = () => {
    onNext();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Your Resume
        </h2>
        <p className="text-gray-600">
          Upload your latest resume and let our AI extract your career information to get started quickly.
        </p>
      </div>

      {uploadState === 'idle' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          {/* File Upload Area */}
          <div
            className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
              dragActive 
                ? 'border-blue-400 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400 bg-gray-50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="resume-upload"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              accept=".pdf,.doc,.docx"
              onChange={handleFileSelect}
            />
            
            <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Drop your resume here, or click to browse
            </h3>
            
            <p className="text-gray-500 mb-4">
              Supports PDF, DOC, and DOCX files up to 10MB
            </p>
            
            <button
              type="button"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <DocumentArrowUpIcon className="w-5 h-5 mr-2" />
              Choose File
            </button>
          </div>

          {/* Benefits */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-8 bg-blue-50 rounded-lg p-6"
          >
            <div className="flex items-center mb-4">
              <SparklesIcon className="w-6 h-6 text-blue-600 mr-2" />
              <h3 className="text-lg font-medium text-blue-900">
                AI-Powered Profile Creation
              </h3>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              {[
                'Automatically extract work experience and job titles',
                'Parse education and certification details',
                'Identify and categorize your skills',
                'Extract project information and achievements',
                'Smart data validation and error checking',
                'Save hours of manual data entry'
              ].map((benefit, index) => (
                <div key={benefit} className="flex items-start space-x-2">
                  <CheckCircleIcon className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                  <span className="text-blue-800">{benefit}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Skip Option */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="mt-6 text-center"
          >
            <p className="text-gray-500 text-sm mb-3">
              Don't have a resume ready?
            </p>
            <button
              onClick={skipUpload}
              className="text-blue-600 hover:text-blue-700 underline text-sm font-medium"
            >
              Skip and fill out manually
            </button>
          </motion.div>
        </motion.div>
      )}

      {(uploadState === 'uploading' || uploadState === 'processing') && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="text-center py-8"
        >
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <SparklesIcon className="w-8 h-8 text-blue-600 animate-spin" />
          </div>
          
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {uploadState === 'uploading' ? 'Uploading your resume...' : 'AI is analyzing your resume...'}
          </h3>
          
          <p className="text-gray-600 mb-6">
            {uploadState === 'uploading' 
              ? 'Please wait while we securely upload your file.'
              : 'Our AI is extracting your career information. This may take a few moments.'}
          </p>
          
          {/* Progress Bar */}
          <div className="max-w-md mx-auto">
            <div className="bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${processingProgress}%` }}
              />
            </div>
            <p className="text-sm text-gray-500">{processingProgress}% complete</p>
          </div>
        </motion.div>
      )}

      {uploadState === 'success' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="text-center py-8"
        >
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircleIcon className="w-8 h-8 text-green-600" />
          </div>
          
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Resume processed successfully!
          </h3>
          
          <p className="text-gray-600 mb-6">
            We've extracted your career information and pre-filled your profile. You can review and edit everything in the next steps.
          </p>

          {/* Extracted Data Preview */}
          <div className="bg-green-50 rounded-lg p-6 mb-6 text-left">
            <h4 className="font-medium text-green-900 mb-3">Extracted Information:</h4>
            <div className="space-y-2 text-sm text-green-800">
              <div>✓ Found 3 work experiences</div>
              <div>✓ Identified 15 technical skills</div>
              <div>✓ Extracted education details</div>
              <div>✓ Found 2 certifications</div>
              <div>✓ Identified 4 projects</div>
            </div>
          </div>

          <div className="flex justify-center space-x-4">
            <button
              onClick={proceedWithParsedData}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              Continue with Extracted Data
            </button>
            <button
              onClick={skipUpload}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Start from Scratch
            </button>
          </div>
        </motion.div>
      )}

      {uploadState === 'error' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="text-center py-8"
        >
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <ExclamationTriangleIcon className="w-8 h-8 text-red-600" />
          </div>
          
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Upload failed
          </h3>
          
          <p className="text-gray-600 mb-6">
            Please make sure your file is a PDF, DOC, or DOCX format and under 10MB.
          </p>

          <div className="flex justify-center space-x-4">
            <button
              onClick={() => setUploadState('idle')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Try Again
            </button>
            <button
              onClick={skipUpload}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Skip Upload
            </button>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ResumeUploadStep;