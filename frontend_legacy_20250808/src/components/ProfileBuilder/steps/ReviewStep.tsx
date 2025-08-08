import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CheckCircleIcon,
  PencilIcon,
  ShareIcon,
  ArrowDownTrayIcon,
  SparklesIcon,
  UserCircleIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  CodeBracketIcon,
  ChartBarIcon,
  TrophyIcon,
  // CalendarIcon,
  MapPinIcon,
  EnvelopeIcon,
  // PhoneIcon,
  // LinkIcon,
  // StarIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

interface ReviewStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const ReviewStep: React.FC<ReviewStepProps> = ({ 
  data, 
  onJumpToStep 
}) => {
  // const [activeSection, setActiveSection] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    // Simulate API submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    setIsCompleted(true);
    
    // Here you would normally send data to backend
    console.log('Profile submitted:', data);
  };

  const calculateCompleteness = () => {
    let totalFields = 0;
    let filledFields = 0;

    // Basic Info
    const basicFields = ['firstName', 'lastName', 'email', 'phone'];
    totalFields += basicFields.length + 3; // +3 for address, nationality, work auth
    filledFields += basicFields.filter(field => data.basicInfo[field as keyof typeof data.basicInfo]).length;
    
    // Address completeness
    if (data.basicInfo.address?.streetName && data.basicInfo.address?.suburb && data.basicInfo.address?.country) {
      filledFields += 1;
    }
    
    // Nationality
    if (data.basicInfo.nationality) {
      filledFields += 1;
    }
    
    // Work Authorization
    if (data.basicInfo.workAuthorization?.status) {
      filledFields += 1;
    }

    // Career Aspiration
    const careerFields = ['shortTermRole', 'longTermRole', 'aspirationStatement'];
    totalFields += careerFields.length;
    filledFields += careerFields.filter(field => data.careerAspiration[field as keyof typeof data.careerAspiration]).length;

    // Education
    totalFields += 1;
    if (data.education.length > 0) filledFields += 1;

    // Work Experience
    totalFields += 1;
    if (data.workExperience.length > 0) filledFields += 1;

    // Skills
    totalFields += 1;
    if (data.skills.length > 0) filledFields += 1;

    // Projects
    totalFields += 1;
    if (data.projects.length > 0) filledFields += 1;

    return Math.round((filledFields / totalFields) * 100);
  };

  const completeness = calculateCompleteness();

  const sections = [
    {
      id: 'basic',
      title: 'Basic Information',
      icon: UserCircleIcon,
      color: 'blue',
      stepIndex: 2,
      data: data.basicInfo,
      isEmpty: !data.basicInfo.firstName && !data.basicInfo.lastName
    },
    {
      id: 'career',
      title: 'Career Goals',
      icon: ChartBarIcon,
      color: 'purple',
      stepIndex: 3,
      data: data.careerAspiration,
      isEmpty: !data.careerAspiration.shortTermRole && !data.careerAspiration.longTermRole
    },
    {
      id: 'education',
      title: 'Education',
      icon: AcademicCapIcon,
      color: 'green',
      stepIndex: 4,
      data: data.education,
      isEmpty: data.education.length === 0
    },
    {
      id: 'experience',
      title: 'Work Experience',
      icon: BriefcaseIcon,
      color: 'orange',
      stepIndex: 5,
      data: data.workExperience,
      isEmpty: data.workExperience.length === 0
    },
    {
      id: 'skills',
      title: 'Skills',
      icon: CodeBracketIcon,
      color: 'indigo',
      stepIndex: 6,
      data: data.skills,
      isEmpty: data.skills.length === 0
    },
    {
      id: 'projects',
      title: 'Projects',
      icon: TrophyIcon,
      color: 'pink',
      stepIndex: 7,
      data: data.projects,
      isEmpty: data.projects.length === 0
    }
  ];

  if (isCompleted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, type: "spring" }}
        className="text-center py-12"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="w-32 h-32 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-8"
        >
          <CheckCircleIcon className="w-16 h-16 text-white" />
        </motion.div>

        <motion.h1
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-4xl font-bold text-gray-900 mb-4"
        >
          🎉 Profile Complete!
        </motion.h1>

        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto"
        >
          Congratulations! Your professional profile has been successfully created. 
          You're now ready to unlock personalized job recommendations and career insights.
        </motion.p>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="grid md:grid-cols-3 gap-4 max-w-4xl mx-auto mb-8"
        >
          <div className="bg-blue-50 rounded-xl p-6 text-center">
            <SparklesIcon className="w-8 h-8 text-blue-600 mx-auto mb-3" />
            <h3 className="font-semibold text-blue-900 mb-2">AI Job Matching</h3>
            <p className="text-sm text-blue-700">Get personalized job recommendations</p>
          </div>
          <div className="bg-green-50 rounded-xl p-6 text-center">
            <TrophyIcon className="w-8 h-8 text-green-600 mx-auto mb-3" />
            <h3 className="font-semibold text-green-900 mb-2">Resume Generation</h3>
            <p className="text-sm text-green-700">Create tailored resumes instantly</p>
          </div>
          <div className="bg-purple-50 rounded-xl p-6 text-center">
            <ChartBarIcon className="w-8 h-8 text-purple-600 mx-auto mb-3" />
            <h3 className="font-semibold text-purple-900 mb-2">Career Analytics</h3>
            <p className="text-sm text-purple-700">Track your career progress</p>
          </div>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="space-y-4"
        >
          <button
            onClick={() => window.location.href = '/dashboard'}
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl mr-4"
          >
            Go to Dashboard
            <SparklesIcon className="w-5 h-5 ml-2" />
          </button>
          
          <button
            onClick={() => setIsCompleted(false)}
            className="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-all duration-200"
          >
            Review Profile Again
            <PencilIcon className="w-4 h-4 ml-2" />
          </button>
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-6xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring" }}
          className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6"
        >
          <CheckCircleIcon className="w-10 h-10 text-white" />
        </motion.div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Review Your Profile
        </h1>
        
        <p className="text-lg text-gray-600 mb-6 max-w-3xl mx-auto">
          Take a moment to review your professional profile. You can edit any section by clicking on it, 
          or submit your profile to start your career journey.
        </p>

        {/* Completeness Score */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-8 max-w-md mx-auto">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-gray-700">Profile Completeness</span>
            <span className="text-2xl font-bold text-blue-600">{completeness}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <motion.div 
              initial={{ width: 0 }}
              animate={{ width: `${completeness}%` }}
              transition={{ duration: 1, delay: 0.5 }}
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full"
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {completeness === 100 ? 'Perfect! Your profile is complete.' : 
             completeness >= 80 ? 'Great! Your profile is looking strong.' :
             completeness >= 60 ? 'Good progress! Consider adding more details.' :
             'Keep going! Add more information to strengthen your profile.'}
          </p>
        </div>
      </div>

      {/* Profile Sections */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {sections.map((section, index) => (
          <motion.div
            key={section.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className={`bg-white border-2 rounded-xl p-6 cursor-pointer transition-all duration-200 hover:shadow-lg ${
              section.isEmpty 
                ? 'border-gray-200 hover:border-gray-300' 
                : `border-${section.color}-200 hover:border-${section.color}-300 bg-${section.color}-50/30`
            }`}
            onClick={() => onJumpToStep?.(section.stepIndex)}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-lg ${
                  section.isEmpty 
                    ? 'bg-gray-100' 
                    : `bg-${section.color}-100`
                }`}>
                  <section.icon className={`w-6 h-6 ${
                    section.isEmpty 
                      ? 'text-gray-400' 
                      : `text-${section.color}-600`
                  }`} />
                </div>
                <h3 className={`font-semibold ${
                  section.isEmpty ? 'text-gray-600' : 'text-gray-900'
                }`}>
                  {section.title}
                </h3>
              </div>
              <div className="flex items-center space-x-2">
                {section.isEmpty ? (
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
                    Empty
                  </span>
                ) : (
                  <CheckCircleIcon className={`w-5 h-5 text-${section.color}-500`} />
                )}
                <PencilIcon className="w-4 h-4 text-gray-400" />
              </div>
            </div>

            {/* Section Preview */}
            <div className="space-y-2">
              {section.id === 'basic' && !section.isEmpty && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900">
                    {data.basicInfo.firstName} {data.basicInfo.lastName}
                  </p>
                  <div className="flex items-center text-xs text-gray-600 space-x-3">
                    {data.basicInfo.email && (
                      <span className="flex items-center">
                        <EnvelopeIcon className="w-3 h-3 mr-1" />
                        {data.basicInfo.email}
                      </span>
                    )}
                    {data.basicInfo.address?.suburb && data.basicInfo.address?.country && (
                      <span className="flex items-center">
                        <MapPinIcon className="w-3 h-3 mr-1" />
                        {data.basicInfo.address.suburb}, {data.basicInfo.address.country}
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-gray-500">
                    {data.basicInfo.workAuthorization?.status === 'citizen' && 'Citizen'}
                    {data.basicInfo.workAuthorization?.status === 'permanent_resident' && 'Permanent Resident'}
                    {data.basicInfo.workAuthorization?.status === 'work_visa' && `Work Visa${data.basicInfo.workAuthorization.visaType ? ` (${data.basicInfo.workAuthorization.visaType})` : ''}`}
                    {data.basicInfo.workAuthorization?.status === 'student_visa' && 'Student Visa'}
                    {data.basicInfo.workAuthorization?.status === 'other' && 'Other Work Authorization'}
                  </div>
                </div>
              )}

              {section.id === 'career' && !section.isEmpty && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900">
                    {data.careerAspiration.shortTermRole}
                  </p>
                  <p className="text-xs text-gray-600 line-clamp-2">
                    {data.careerAspiration.aspirationStatement}
                  </p>
                </div>
              )}

              {section.id === 'education' && !section.isEmpty && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900">
                    {data.education[0]?.degree} in {data.education[0]?.fieldOfStudy}
                  </p>
                  <p className="text-xs text-gray-600">
                    {data.education[0]?.institutionName}
                  </p>
                  {data.education.length > 1 && (
                    <p className="text-xs text-blue-600">
                      +{data.education.length - 1} more
                    </p>
                  )}
                </div>
              )}

              {section.id === 'experience' && !section.isEmpty && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900">
                    {data.workExperience[0]?.jobTitle}
                  </p>
                  <p className="text-xs text-gray-600">
                    {data.workExperience[0]?.companyName}
                  </p>
                  {data.workExperience.length > 1 && (
                    <p className="text-xs text-blue-600">
                      +{data.workExperience.length - 1} more positions
                    </p>
                  )}
                </div>
              )}

              {section.id === 'skills' && !section.isEmpty && (
                <div className="space-y-1">
                  <div className="flex flex-wrap gap-1">
                    {data.skills.slice(0, 3).map((skill, idx) => (
                      <span key={idx} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        {skill.skillName}
                      </span>
                    ))}
                    {data.skills.length > 3 && (
                      <span className="text-xs text-blue-600">
                        +{data.skills.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              {section.id === 'projects' && !section.isEmpty && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-900">
                    {data.projects[0]?.projectName}
                  </p>
                  <p className="text-xs text-gray-600 line-clamp-1">
                    {data.projects[0]?.description}
                  </p>
                  {data.projects.length > 1 && (
                    <p className="text-xs text-blue-600">
                      +{data.projects.length - 1} more projects
                    </p>
                  )}
                </div>
              )}

              {section.isEmpty && (
                <p className="text-sm text-gray-500 italic">
                  Click to add {section.title.toLowerCase()}
                </p>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.8 }}
        className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 pt-8 border-t"
      >
        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={`flex items-center px-8 py-4 rounded-xl font-semibold text-white transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl ${
            isSubmitting
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700'
          }`}
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
              Submitting Profile...
            </>
          ) : (
            <>
              <CheckCircleIcon className="w-5 h-5 mr-3" />
              Complete Profile
            </>
          )}
        </button>

        <div className="flex space-x-3">
          <button
            className="flex items-center px-4 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-all duration-200"
          >
            <ShareIcon className="w-4 h-4 mr-2" />
            Share
          </button>
          
          <button
            className="flex items-center px-4 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-all duration-200"
          >
            <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
            Export
          </button>
        </div>
      </motion.div>

      {/* Profile Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.0 }}
        className="mt-12 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          Your Profile at a Glance
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-blue-600">{data.education.length}</div>
            <div className="text-sm text-gray-600">Education</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{data.workExperience.length}</div>
            <div className="text-sm text-gray-600">Experience</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600">{data.skills.length}</div>
            <div className="text-sm text-gray-600">Skills</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-orange-600">{data.projects.length}</div>
            <div className="text-sm text-gray-600">Projects</div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default ReviewStep;