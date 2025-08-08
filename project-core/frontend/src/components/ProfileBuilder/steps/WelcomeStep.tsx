import React, { useState } from 'react';
import { 
  UserCircleIcon, 
  AcademicCapIcon, 
  BriefcaseIcon, 
  CodeBracketIcon,
  ChartBarIcon,
  // CheckCircleIcon,
  ClockIcon,
  SparklesIcon,
  ListBulletIcon,
  ArrowPathIcon,
  DocumentPlusIcon
} from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

interface WelcomeStepProps {
  onNext: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
  data?: any; // Added data prop
}

const WelcomeStep: React.FC<WelcomeStepProps> = ({ onNext, onJumpToStep, data }) => {
  const [selectedMode, setSelectedMode] = useState<'guided' | 'independent'>('guided');
  
  // Check if user has existing profile data
  const hasExistingData = data && (
    data.basicInfo?.firstName || 
    data.basicInfo?.lastName || 
    data.basicInfo?.email ||
    data.workExperience?.length > 0 ||
    data.education?.length > 0 ||
    data.skills?.technical?.length > 0 ||
    data.skills?.soft?.length > 0
  );

  const isReturningUser = hasExistingData;

  const handleGetStarted = () => {
    if (isReturningUser) {
      // For returning users, go directly to Basic Info
      if (onJumpToStep) {
        onJumpToStep(2); // Basic Info step
      }
    } else {
      // For new users, go to Resume Upload
      onNext();
    }
  };

  const handleGuidedWizard = () => {
    if (isReturningUser) {
      // For returning users, go directly to Basic Info
      if (onJumpToStep) {
        onJumpToStep(2); // Basic Info step
      }
    } else {
      // For new users, go to Resume Upload
      onNext();
    }
  };

  const profileSections = [
    {
      icon: UserCircleIcon,
      title: 'Basic Information',
      description: 'Personal details and contact information',
      stepIndex: 2, // After resume upload
      estimatedTime: '2 min'
    },
    {
      icon: ChartBarIcon,
      title: 'Career Goals',
      description: 'Your aspirations and target roles',
      stepIndex: 3,
      estimatedTime: '3 min'
    },
    {
      icon: AcademicCapIcon,
      title: 'Education & Certifications',
      description: 'Academic background and credentials',
      stepIndex: 4,
      estimatedTime: '4 min'
    },
    {
      icon: BriefcaseIcon,
      title: 'Work Experience',
      description: 'Professional history and achievements',
      stepIndex: 5,
      estimatedTime: '5 min'
    },
    {
      icon: CodeBracketIcon,
      title: 'Skills',
      description: 'Technical abilities and competencies',
      stepIndex: 6,
      estimatedTime: '3 min'
    },
    {
      icon: CodeBracketIcon,
      title: 'Projects',
      description: 'Portfolio and project showcase',
      stepIndex: 7,
      estimatedTime: '4 min'
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto"
    >
      {isReturningUser ? (
        // Returning User Welcome
        <div className="text-center">
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
            className="w-24 h-24 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-8"
          >
            <UserCircleIcon className="w-12 h-12 text-white" />
          </motion.div>
          
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome Back! 👋
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            We found your existing profile. You can review and update your information, 
            or continue building your profile with new details.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <button
              onClick={handleGetStarted}
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <UserCircleIcon className="w-5 h-5 mr-2" />
              Review & Update Profile
            </button>
            
            <button
              onClick={() => onNext()}
              className="inline-flex items-center px-8 py-4 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transform hover:scale-105 transition-all duration-200"
            >
              <DocumentPlusIcon className="w-5 h-5 mr-2" />
              Upload New Resume
            </button>
          </div>
          
          <div className="mt-8 p-6 bg-blue-50 rounded-xl border border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              💡 Quick Tips
            </h3>
            <ul className="text-sm text-blue-800 space-y-1 text-left max-w-md mx-auto">
              <li>• Your existing data has been loaded</li>
              <li>• You can update any section at any time</li>
              <li>• New resume uploads will merge with existing data</li>
              <li>• Profile changes create new versions for tracking</li>
            </ul>
          </div>
        </div>
      ) : (
        // New User Welcome (existing content)
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white text-center mb-8"
          >
            <div className="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0">
              <div className="flex items-center space-x-4">
                <div className="bg-white/20 rounded-full p-3">
                  <SparklesIcon className="w-8 h-8" />
                </div>
                <div className="text-left">
                  <h1 className="text-2xl sm:text-3xl font-bold mb-1">
                    Build Your Career Profile
                  </h1>
                  <div className="flex items-center space-x-4 text-blue-100">
                    <div className="flex items-center space-x-1">
                      <ClockIcon className="w-4 h-4" />
                      <span className="text-sm font-medium">10-15 minutes</span>
                    </div>
                    <span className="text-sm">• Save & continue anytime</span>
                  </div>
                </div>
              </div>
              
              <motion.button
                onClick={handleGetStarted}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-white text-blue-600 px-6 sm:px-8 py-3 rounded-xl font-semibold hover:bg-blue-50 transition-all duration-200 shadow-lg flex items-center space-x-2 min-w-[160px] justify-center"
              >
                <span>Get Started</span>
                <ArrowPathIcon className="w-5 h-5" />
              </motion.button>
            </div>
          </motion.div>

          {/* Mode Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mb-8"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              Choose how you'd like to build your profile:
            </h2>
            
            <div className="grid md:grid-cols-2 gap-4 max-w-4xl mx-auto">
              {/* Guided Mode */}
              <motion.button
                onClick={handleGuidedWizard}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-6 rounded-xl border-2 transition-all duration-200 text-left ${
                  selectedMode === 'guided'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg ${
                    selectedMode === 'guided' ? 'bg-blue-100' : 'bg-gray-100'
                  }`}>
                    <SparklesIcon className={`w-6 h-6 ${
                      selectedMode === 'guided' ? 'text-blue-600' : 'text-gray-600'
                    }`} />
                  </div>
                  <div className="flex-1">
                    <h3 className={`font-semibold mb-2 ${
                      selectedMode === 'guided' ? 'text-blue-900' : 'text-gray-900'
                    }`}>
                      Guided Wizard (Recommended)
                    </h3>
                    <p className={`text-sm ${
                      selectedMode === 'guided' ? 'text-blue-700' : 'text-gray-600'
                    }`}>
                      Step-by-step guidance through each section with helpful tips and AI-powered suggestions.
                    </p>
                    <div className="mt-3 flex items-center space-x-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        selectedMode === 'guided' 
                          ? 'bg-blue-200 text-blue-800' 
                          : 'bg-gray-200 text-gray-700'
                      }`}>
                        Best for first-time users
                      </span>
                    </div>
                  </div>
                </div>
              </motion.button>

              {/* Independent Mode */}
              <motion.button
                onClick={() => setSelectedMode('independent')}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`p-6 rounded-xl border-2 transition-all duration-200 text-left ${
                  selectedMode === 'independent'
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg ${
                    selectedMode === 'independent' ? 'bg-green-100' : 'bg-gray-100'
                  }`}>
                    <ListBulletIcon className={`w-6 h-6 ${
                      selectedMode === 'independent' ? 'text-green-600' : 'text-gray-600'
                    }`} />
                  </div>
                  <div className="flex-1">
                    <h3 className={`font-semibold mb-2 ${
                      selectedMode === 'independent' ? 'text-green-900' : 'text-gray-900'
                    }`}>
                      Fill Sections Independently
                    </h3>
                    <p className={`text-sm ${
                      selectedMode === 'independent' ? 'text-green-700' : 'text-gray-600'
                    }`}>
                      Jump directly to any section and fill them in your preferred order.
                    </p>
                    <div className="mt-3 flex items-center space-x-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        selectedMode === 'independent' 
                          ? 'bg-green-200 text-green-800' 
                          : 'bg-gray-200 text-gray-700'
                      }`}>
                        For experienced users
                      </span>
                    </div>
                  </div>
                </div>
              </motion.button>
            </div>
          </motion.div>

          {/* Profile Sections - Independent Navigation */}
          {selectedMode === 'independent' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mb-8"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
                Jump to any section to get started:
              </h3>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {profileSections.map((section, index) => (
                  <motion.button
                    key={section.title}
                    onClick={() => onJumpToStep?.(section.stepIndex)}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="bg-white border border-gray-200 rounded-xl p-4 text-left hover:shadow-lg hover:border-gray-300 transition-all duration-200 group"
                  >
                    <div className="flex items-start space-x-3">
                      <div className="bg-gray-100 group-hover:bg-blue-100 rounded-lg p-2 transition-colors duration-200">
                        <section.icon className="w-5 h-5 text-gray-600 group-hover:text-blue-600 transition-colors duration-200" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-semibold text-gray-900 group-hover:text-blue-900 transition-colors duration-200">
                            {section.title}
                          </h4>
                          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                            {section.estimatedTime}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 group-hover:text-gray-700 transition-colors duration-200">
                          {section.description}
                        </p>
                      </div>
                    </div>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Benefits - Shown for both modes */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: selectedMode === 'independent' ? 0.4 : 0.2 }}
            className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 mb-8"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
              What you'll unlock:
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 text-left">
              {[
                { icon: '🎯', text: 'AI-powered job matching based on your profile' },
                { icon: '📊', text: 'Personalized career recommendations' },
                { icon: '🔍', text: 'Skills gap analysis and development suggestions' },
                { icon: '📄', text: 'Professional resume and cover letter generation' },
                { icon: '🎤', text: 'Interview preparation tailored to your background' },
                { icon: '📈', text: 'Career progress tracking and analytics' },
              ].map((benefit, index) => (
                <motion.div
                  key={benefit.text}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: (selectedMode === 'independent' ? 0.5 : 0.3) + index * 0.1 }}
                  className="flex items-start space-x-3"
                >
                  <span className="text-2xl">{benefit.icon}</span>
                  <span className="text-gray-700 text-sm">{benefit.text}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Action Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: selectedMode === 'independent' ? 0.6 : 0.4 }}
            className="text-center"
          >
            {selectedMode === 'guided' ? (
              <div>
                <p className="text-gray-600 mb-4">
                  Ready to start building your professional profile?
                </p>
                <button
                  onClick={handleGuidedWizard}
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                  Start Guided Experience
                  <SparklesIcon className="w-5 h-5 ml-2" />
                </button>
              </div>
            ) : (
              <div>
                <p className="text-gray-600 mb-4">
                  Click any section above to start building your profile, or begin with the guided experience:
                </p>
                <div className="flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4">
                  <button
                    onClick={handleGuidedWizard}
                    className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-all duration-200"
                  >
                    Start with Guided Flow
                    <SparklesIcon className="w-4 h-4 ml-2" />
                  </button>
                  <span className="text-gray-400">or</span>
                  <button
                    onClick={() => onJumpToStep?.(2)}
                    className="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-all duration-200"
                  >
                    Jump to Basic Info
                    <UserCircleIcon className="w-4 h-4 ml-2" />
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      )}
    </motion.div>
  );
};

export default WelcomeStep;