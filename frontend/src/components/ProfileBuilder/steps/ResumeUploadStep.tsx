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

interface ParsedResumeData {
  personal_info?: {
    name?: string;
    email?: string;
    phone?: string;
    location?: string;
  };
  summary?: string;
  work_experience?: Array<{
    company: string;
    position: string;
    start_date: string;
    end_date: string;
    description: string;
  }>;
  education?: Array<{
    institution: string;
    degree: string;
    field_of_study: string;
    graduation_date: string;
    gpa?: string;
  }>;
  skills?: Array<{
    category: string;
    skills: string[];
  }>;
  certifications?: Array<{
    name: string;
    issuer: string;
    date_earned: string;
    expiry_date?: string;
  }>;
  projects?: Array<{
    name: string;
    description: string;
    technologies: string[];
    url?: string;
  }>;
}

const ResumeUploadStep: React.FC<ResumeUploadStepProps> = ({ data, updateData, onNext }) => {
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'processing' | 'success' | 'error'>('idle');
  const [dragActive, setDragActive] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [parsedData, setParsedData] = useState<ParsedResumeData | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

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
      setErrorMessage('Invalid file type. Please upload a PDF, DOC, or DOCX file.');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setUploadState('error');
      setErrorMessage('File size too large. Please upload a file smaller than 10MB.');
      return;
    }

    setUploadState('uploading');
    setErrorMessage('');

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', file);

      // Upload and parse resume
      const response = await fetch('http://localhost:8000/api/v1/resume/parse?user_id=1', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to parse resume');
      }

      const result = await response.json();
      
      if (result.success && result.extracted_data) {
        setParsedData(result.extracted_data);
        
        // Save the parsed data to the database
        try {
          const saveResponse = await fetch('http://localhost:8000/api/v1/resume/save-first', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: 1, // TODO: Get actual user ID from auth context
              resume_data: result.extracted_data
            }),
          });

          if (saveResponse.ok) {
            const saveResult = await saveResponse.json();
            console.log('✅ Resume data saved to database:', saveResult.message);
            setUploadState('success');
          } else {
            console.error('❌ Failed to save resume data to database');
            setUploadState('success'); // Still show success for parsing, but log the save error
          }
        } catch (saveError) {
          console.error('❌ Error saving resume data to database:', saveError);
          setUploadState('success'); // Still show success for parsing
        }
      } else {
        throw new Error(result.error || 'Failed to extract data from resume');
      }

    } catch (error) {
      console.error('Resume parsing error:', error);
      setUploadState('error');
      setErrorMessage(error instanceof Error ? error.message : 'Failed to parse resume');
    }
  };

  const proceedWithParsedData = () => {
    if (parsedData) {
      // Update profile data with parsed information
      if (parsedData.personal_info) {
        const personalInfo = parsedData.personal_info;
        updateData('basicInfo', {
          ...data.basicInfo,
          firstName: personalInfo.name?.split(' ')[0] || '',
          lastName: personalInfo.name?.split(' ').slice(1).join(' ') || '',
          email: personalInfo.email || '',
          phone: personalInfo.phone || '',
          location: personalInfo.location || '',
        });
      }

      if (parsedData.summary) {
        updateData('basicInfo', {
          ...data.basicInfo,
          summary: parsedData.summary,
        });
      }

      if (parsedData.work_experience) {
        updateData('workExperience', {
          ...data.workExperience,
          experiences: parsedData.work_experience.map(exp => ({
            company: exp.company,
            position: exp.position,
            startDate: exp.start_date,
            endDate: exp.end_date,
            description: exp.description,
            achievements: [],
            technologies: [],
          })),
        });
      }

      if (parsedData.education) {
        updateData('education', {
          ...data.education,
          institutions: parsedData.education.map(edu => ({
            institution: edu.institution,
            degree: edu.degree,
            fieldOfStudy: edu.field_of_study,
            graduationDate: edu.graduation_date,
            gpa: edu.gpa || '',
            certifications: [],
          })),
        });
      }

      if (parsedData.skills) {
        const skillsData = {
          technical: [],
          soft: [],
          languages: [],
          other: [],
        };

        parsedData.skills.forEach(skillGroup => {
          if (skillGroup.category.toLowerCase().includes('technical')) {
            skillsData.technical = skillGroup.skills;
          } else if (skillGroup.category.toLowerCase().includes('soft')) {
            skillsData.soft = skillGroup.skills;
          } else if (skillGroup.category.toLowerCase().includes('language')) {
            skillsData.languages = skillGroup.skills;
          } else {
            skillsData.other = skillGroup.skills;
          }
        });

        updateData('skills', skillsData);
      }

      if (parsedData.projects) {
        updateData('projects', {
          ...data.projects,
          projects: parsedData.projects.map(project => ({
            name: project.name,
            description: project.description,
            technologies: project.technologies,
            url: project.url || '',
            imageUrl: '',
          })),
        });
      }
    }

    onNext();
  };

  const skipUpload = () => {
    onNext();
  };

  const getExtractedDataSummary = () => {
    if (!parsedData) return [];
    
    const summary = [];
    if (parsedData.work_experience?.length) {
      summary.push(`✓ Found ${parsedData.work_experience.length} work experience${parsedData.work_experience.length > 1 ? 's' : ''}`);
    }
    if (parsedData.education?.length) {
      summary.push(`✓ Found ${parsedData.education.length} education record${parsedData.education.length > 1 ? 's' : ''}`);
    }
    if (parsedData.skills?.length) {
      const totalSkills = parsedData.skills.reduce((acc, skill) => acc + skill.skills.length, 0);
      summary.push(`✓ Identified ${totalSkills} skills across ${parsedData.skills.length} categories`);
    }
    if (parsedData.certifications?.length) {
      summary.push(`✓ Found ${parsedData.certifications.length} certification${parsedData.certifications.length > 1 ? 's' : ''}`);
    }
    if (parsedData.projects?.length) {
      summary.push(`✓ Identified ${parsedData.projects.length} project${parsedData.projects.length > 1 ? 's' : ''}`);
    }
    if (parsedData.personal_info?.name) {
      summary.push(`✓ Extracted personal information`);
    }
    
    return summary;
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
              ].map((benefit) => (
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
              {getExtractedDataSummary().map((item, index) => (
                <div key={index}>{item}</div>
              ))}
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
            {errorMessage || 'Please make sure your file is a PDF, DOC, or DOCX format and under 10MB.'}
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