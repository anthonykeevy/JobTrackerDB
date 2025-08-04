import React, { useState, useCallback } from 'react';
import { ChevronLeftIcon, ChevronRightIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';

// Step Components
import WelcomeStep from './steps/WelcomeStep.tsx';
import ResumeUploadStep from './steps/ResumeUploadStep.tsx';
import BasicInfoStep from './steps/BasicInfoStep.tsx';
import CareerAspirationStep from './steps/CareerAspirationStep.tsx';
import EducationStep from './steps/EducationStep.tsx';
import WorkExperienceStep from './steps/WorkExperienceStep.tsx';
import SkillsStep from './steps/SkillsStep.tsx';
import ProjectsStep from './steps/ProjectsStep.tsx';
import ReviewStep from './steps/ReviewStep.tsx';

// Types
import type { ProfileData } from './types.ts';
export type { ProfileData } from './types.ts';

const STEPS = [
  { id: 'welcome', title: 'Welcome', component: WelcomeStep },
  { id: 'resume-upload', title: 'Resume Upload', component: ResumeUploadStep },
  { id: 'basic-info', title: 'Basic Info', component: BasicInfoStep },
  { id: 'career', title: 'Career Goals', component: CareerAspirationStep },
  { id: 'education', title: 'Education', component: EducationStep },
  { id: 'experience', title: 'Experience', component: WorkExperienceStep },
  { id: 'skills', title: 'Skills', component: SkillsStep },
  { id: 'projects', title: 'Projects', component: ProjectsStep },
  { id: 'review', title: 'Review', component: ReviewStep },
];

const ProfileBuilder: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [profileData, setProfileData] = useState<ProfileData>({
    resumeData: undefined,
    basicInfo: {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: {
        streetNumber: '',
        streetName: '',
        streetType: '',
        unitNumber: '',
        unitType: '',
        suburb: '',
        state: '',
        postcode: '',
        country: 'Australia',
        propertyId: '',
        latitude: undefined,
        longitude: undefined,
        propertyType: '',
        landArea: undefined,
        floorArea: undefined,
        isValidated: false,
        validationSource: undefined,
        confidenceScore: undefined,
        validationDate: '',
        isPrimary: true,
        addressType: 'residential',
      },
      dateOfBirth: '',
      countryOfBirth: '',
      nationality: '',
      workAuthorization: {
        status: 'citizen',
        visaType: '',
        expiryDate: '',
        details: '',
        otherType: '',
        seekingSponsorship: false,
      },
      professionalLinks: {
        linkedInURL: '',
        githubURL: '',
        portfolioURL: '',
        personalWebsite: '',
      },
      socialLinks: {
        twitterURL: '',
        instagramURL: '',
        facebookURL: '',
      },
    },
          careerAspiration: {
        currentTitle: '',
        shortTermRole: '',
        longTermRole: '',
        aspirationStatement: '',
        targetIndustries: [],
        workPreferences: {
          arrangements: [
            { type: 'remote', preference: 1 },
            { type: 'hybrid', preference: 2 },
            { type: 'onsite', preference: 3 },
            { type: 'flexible', preference: 4 },
          ],
          willingToRelocate: false,
        },
        salaryExpectations: {
          employmentType: 'full-time',
          amount: '',
          period: 'annually',
          currency: 'AUD',
          flexible: true,
          notes: '',
        },
      },
    education: [],
    workExperience: [],
    skills: [],
    projects: [],
    certifications: [],
  });

  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const updateProfileData = useCallback((section: keyof ProfileData, data: Partial<ProfileData[keyof ProfileData]>) => {
    setProfileData(prev => ({
      ...prev,
      [section]: data,
    }));
  }, []);

  const markStepComplete = (stepIndex: number) => {
    setCompletedSteps(prev => new Set([...prev, stepIndex]));
  };

  const goToStep = useCallback((stepIndex: number) => {
    if (stepIndex >= 0 && stepIndex < STEPS.length) {
      setCurrentStep(stepIndex);
    }
  }, []);

  const nextStep = () => {
    if (currentStep < STEPS.length - 1) {
      markStepComplete(currentStep);
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const CurrentStepComponent = STEPS[currentStep].component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Progress Bar - Full Width Responsive */}
      <div className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="w-full max-w-none px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16">
          <div className="py-3 sm:py-4">
            {/* Header - Responsive Layout */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 sm:mb-2">
              <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 mb-1 sm:mb-0">
                Build Your Profile
              </h1>
              <div className="flex items-center space-x-4">
                <span className="text-xs sm:text-sm text-gray-500 font-medium">
                  Step {currentStep + 1} of {STEPS.length}
                </span>
                <div className="w-24 sm:w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            {/* Progress Steps - Mobile Optimized */}
            <div className="block sm:hidden">
              {/* Mobile: Show current step only */}
              <div className="flex items-center justify-center">
                <span className="text-sm font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                  {STEPS[currentStep].title}
                </span>
              </div>
            </div>
            
            {/* Progress Steps - Tablet & Desktop */}
            <div className="hidden sm:flex items-center space-x-2 lg:space-x-4 overflow-x-auto pb-2">
              {STEPS.map((step, index) => (
                <div key={step.id} className="flex items-center flex-shrink-0">
                  <button
                    onClick={() => goToStep(index)}
                    className={`flex items-center justify-center w-7 h-7 lg:w-8 lg:h-8 rounded-full border-2 transition-all duration-200 ${
                      index === currentStep
                        ? 'border-blue-600 bg-blue-600 text-white'
                        : completedSteps.has(index)
                        ? 'border-green-500 bg-green-500 text-white'
                        : index < currentStep
                        ? 'border-blue-300 bg-blue-100 text-blue-600 hover:border-blue-400'
                        : 'border-gray-300 bg-gray-50 text-gray-400'
                    }`}
                    disabled={index > currentStep && !completedSteps.has(index)}
                  >
                    {completedSteps.has(index) ? (
                      <CheckCircleIcon className="w-4 h-4 lg:w-5 lg:h-5" />
                    ) : (
                      <span className="text-xs lg:text-sm font-medium">{index + 1}</span>
                    )}
                  </button>
                  <span className={`ml-1 lg:ml-2 text-xs lg:text-sm font-medium hidden md:inline ${
                    index === currentStep ? 'text-blue-600' : 
                    completedSteps.has(index) ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {step.title}
                  </span>
                  {index < STEPS.length - 1 && (
                    <div className={`w-4 lg:w-8 h-0.5 ml-2 lg:ml-4 ${
                      completedSteps.has(index) ? 'bg-green-200' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Full Responsive Layout */}
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 py-4 sm:py-6 lg:py-8">
        {/* Responsive Content Container */}
        <div className="max-w-none lg:max-w-7xl xl:max-w-none 2xl:max-w-screen-2xl mx-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-xl shadow-lg p-4 sm:p-6 lg:p-8 xl:p-10"
            >
              <CurrentStepComponent
                data={profileData}
                updateData={updateProfileData}
                onNext={nextStep}
                onPrev={prevStep}
                onJumpToStep={goToStep}
                isFirstStep={currentStep === 0}
                isLastStep={currentStep === STEPS.length - 1}
              />
            </motion.div>
          </AnimatePresence>
        </div>
      </div>

      {/* Enhanced Responsive Navigation */}
      {currentStep > 0 && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-20">
          <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 py-3 sm:py-4">
            <div className="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
              {/* Previous Button */}
              <button
                onClick={prevStep}
                className="flex items-center justify-center w-full sm:w-auto px-4 sm:px-6 py-3 sm:py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-lg transition-all duration-200 font-medium"
              >
                <ChevronLeftIcon className="w-5 h-5 mr-2" />
                Previous
              </button>
              
              {/* Progress Indicator - Mobile */}
              <div className="flex sm:hidden items-center space-x-2">
                <span className="text-sm text-gray-500">
                  {currentStep + 1} of {STEPS.length}
                </span>
                <div className="w-20 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center space-x-3">
                {currentStep < STEPS.length - 1 ? (
                  <button
                    onClick={nextStep}
                    className="flex items-center justify-center w-full sm:w-auto px-6 py-3 sm:py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-lg hover:shadow-xl transition-all duration-200 font-medium transform hover:scale-105"
                  >
                    Continue
                    <ChevronRightIcon className="w-5 h-5 ml-2" />
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      // Handle profile submission
                      console.log('Profile submitted:', profileData);
                    }}
                    className="flex items-center justify-center w-full sm:w-auto px-6 py-3 sm:py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 shadow-lg hover:shadow-xl transition-all duration-200 font-medium transform hover:scale-105"
                  >
                    <CheckCircleIcon className="w-5 h-5 mr-2" />
                    Complete Profile
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileBuilder;