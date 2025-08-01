import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion } from 'framer-motion';
import { 
  BriefcaseIcon,
  PlusIcon,
  TrashIcon,
  BuildingOfficeIcon,
  CalendarIcon,
  TrophyIcon,
  CodeBracketIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

const workExperienceSchema = z.object({
  workExperience: z.array(z.object({
    id: z.string(),
    companyName: z.string().min(2, 'Company name is required'),
    jobTitle: z.string().min(2, 'Job title is required'),
    startDate: z.string().min(1, 'Start date is required'),
    endDate: z.string().optional(),
    isCurrentRole: z.boolean(),
    description: z.string().min(10, 'Job description is required'),
    achievements: z.array(z.string()),
    skills: z.array(z.string()),
  })),
});

type WorkExperienceFormData = z.infer<typeof workExperienceSchema>;

interface WorkExperienceStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const WorkExperienceStep: React.FC<WorkExperienceStepProps> = ({ 
  data, 
  updateData, 
  onNext 
}) => {
  const [expandedAchievements, setExpandedAchievements] = useState<{[key: number]: boolean}>({});
  const [expandedSkills, setExpandedSkills] = useState<{[key: number]: boolean}>({});

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
    setValue,
    getValues
  } = useForm<WorkExperienceFormData>({
    resolver: zodResolver(workExperienceSchema),
    defaultValues: {
      workExperience: data.workExperience.length > 0 ? data.workExperience : [{
        id: crypto.randomUUID(),
        companyName: '',
        jobTitle: '',
        startDate: '',
        endDate: '',
        isCurrentRole: false,
        description: '',
        achievements: [],
        skills: [],
      }]
    }
  });

  const { fields: experienceFields, append: appendExperience, remove: removeExperience } = useFieldArray({
    control,
    name: 'workExperience'
  });

  // Keep watch for UI updates only (not for data sync)

  const onSubmit = (formData: WorkExperienceFormData) => {
    updateData('workExperience', formData.workExperience);
    onNext();
  };

  const addExperience = () => {
    appendExperience({
      id: crypto.randomUUID(),
      companyName: '',
      jobTitle: '',
      startDate: '',
      endDate: '',
      isCurrentRole: false,
      description: '',
      achievements: [],
      skills: [],
    });
  };

  const addAchievement = (experienceIndex: number) => {
    const currentAchievements = getValues(`workExperience.${experienceIndex}.achievements`) || [];
    setValue(`workExperience.${experienceIndex}.achievements`, [...currentAchievements, '']);
  };

  const removeAchievement = (experienceIndex: number, achievementIndex: number) => {
    const currentAchievements = getValues(`workExperience.${experienceIndex}.achievements`) || [];
    setValue(`workExperience.${experienceIndex}.achievements`, 
      currentAchievements.filter((_, index) => index !== achievementIndex)
    );
  };

  const addSkill = (experienceIndex: number) => {
    const currentSkills = getValues(`workExperience.${experienceIndex}.skills`) || [];
    setValue(`workExperience.${experienceIndex}.skills`, [...currentSkills, '']);
  };

  const removeSkill = (experienceIndex: number, skillIndex: number) => {
    const currentSkills = getValues(`workExperience.${experienceIndex}.skills`) || [];
    setValue(`workExperience.${experienceIndex}.skills`, 
      currentSkills.filter((_, index) => index !== skillIndex)
    );
  };

  const toggleAchievements = (index: number) => {
    setExpandedAchievements(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const toggleSkills = (index: number) => {
    setExpandedSkills(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Work Experience
        </h2>
        <p className="text-gray-600">
          Detail your professional experience, achievements, and skills gained in each role.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {experienceFields.map((field, index) => (
          <motion.div
            key={field.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <BriefcaseIcon className="w-6 h-6 text-blue-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900">
                  Experience {index + 1}
                </h3>
              </div>
              {experienceFields.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeExperience(index)}
                  className="text-red-500 hover:text-red-700 transition-colors"
                >
                  <TrashIcon className="w-5 h-5" />
                </button>
              )}
            </div>

            <div className="space-y-6">
              {/* Basic Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Job Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title *
                  </label>
                  <input
                    {...register(`workExperience.${index}.jobTitle`)}
                    type="text"
                    placeholder="e.g., Senior Software Engineer"
                    className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      errors.workExperience?.[index]?.jobTitle 
                        ? 'border-red-300 bg-red-50' 
                        : 'border-gray-300'
                    }`}
                  />
                  {errors.workExperience?.[index]?.jobTitle && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.workExperience[index]?.jobTitle?.message}
                    </p>
                  )}
                </div>

                {/* Company Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <BuildingOfficeIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`workExperience.${index}.companyName`)}
                      type="text"
                      placeholder="e.g., Google Inc."
                      className={`block w-full pl-10 pr-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.workExperience?.[index]?.companyName 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                    />
                  </div>
                  {errors.workExperience?.[index]?.companyName && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.workExperience[index]?.companyName?.message}
                    </p>
                  )}
                </div>

                {/* Start Date */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Start Date *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CalendarIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`workExperience.${index}.startDate`)}
                      type="month"
                      className={`block w-full pl-10 pr-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.workExperience?.[index]?.startDate 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                    />
                  </div>
                  {errors.workExperience?.[index]?.startDate && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.workExperience[index]?.startDate?.message}
                    </p>
                  )}
                </div>

                {/* End Date */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    End Date
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CalendarIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`workExperience.${index}.endDate`)}
                      type="month"
                      disabled={watch(`workExperience.${index}.isCurrentRole`)}
                      className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                    />
                  </div>
                </div>

                {/* Current Role Checkbox */}
                <div className="md:col-span-2">
                  <label className="flex items-center">
                    <input
                      {...register(`workExperience.${index}.isCurrentRole`)}
                      type="checkbox"
                      className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                    />
                    <span className="ml-2 text-sm text-gray-700">This is my current role</span>
                  </label>
                </div>
              </div>

              {/* Job Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Description *
                </label>
                <textarea
                  {...register(`workExperience.${index}.description`)}
                  rows={4}
                  placeholder="Describe your role, responsibilities, and key contributions..."
                  className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                    errors.workExperience?.[index]?.description 
                      ? 'border-red-300 bg-red-50' 
                      : 'border-gray-300'
                  }`}
                />
                {errors.workExperience?.[index]?.description && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.workExperience[index]?.description?.message}
                  </p>
                )}
              </div>

              {/* Achievements Section */}
              <div className="border-t pt-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <TrophyIcon className="w-5 h-5 text-yellow-500 mr-2" />
                    <h4 className="text-lg font-medium text-gray-900">Key Achievements</h4>
                  </div>
                  <button
                    type="button"
                    onClick={() => toggleAchievements(index)}
                    className="text-sm text-blue-600 hover:text-blue-700"
                  >
                    {expandedAchievements[index] ? 'Collapse' : 'Expand'}
                  </button>
                </div>

                {(expandedAchievements[index] || (watch(`workExperience.${index}.achievements`) || []).length > 0) && (
                  <div className="space-y-3">
                    {(watch(`workExperience.${index}.achievements`) || []).map((_, achievementIndex) => (
                      <div key={achievementIndex} className="flex items-center space-x-2">
                        <input
                          {...register(`workExperience.${index}.achievements.${achievementIndex}`)}
                          type="text"
                          placeholder={`Achievement ${achievementIndex + 1}...`}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <button
                          type="button"
                          onClick={() => removeAchievement(index, achievementIndex)}
                          className="text-red-500 hover:text-red-700 transition-colors"
                        >
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                    
                    <button
                      type="button"
                      onClick={() => addAchievement(index)}
                      className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                    >
                      <PlusIcon className="w-4 h-4 mr-1" />
                      Add Achievement
                    </button>
                  </div>
                )}

                {!expandedAchievements[index] && (watch(`workExperience.${index}.achievements`) || []).length === 0 && (
                  <button
                    type="button"
                    onClick={() => {
                      toggleAchievements(index);
                      addAchievement(index);
                    }}
                    className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-yellow-400 hover:text-yellow-600 transition-colors text-sm"
                  >
                    + Add your key achievements and accomplishments
                  </button>
                )}
              </div>

              {/* Skills Section */}
              <div className="border-t pt-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <CodeBracketIcon className="w-5 h-5 text-green-500 mr-2" />
                    <h4 className="text-lg font-medium text-gray-900">Skills Used</h4>
                  </div>
                  <button
                    type="button"
                    onClick={() => toggleSkills(index)}
                    className="text-sm text-blue-600 hover:text-blue-700"
                  >
                    {expandedSkills[index] ? 'Collapse' : 'Expand'}
                  </button>
                </div>

                {(expandedSkills[index] || (watch(`workExperience.${index}.skills`) || []).length > 0) && (
                  <div className="space-y-3">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {(watch(`workExperience.${index}.skills`) || []).map((_, skillIndex) => (
                        <div key={skillIndex} className="flex items-center space-x-2">
                          <input
                            {...register(`workExperience.${index}.skills.${skillIndex}`)}
                            type="text"
                            placeholder="e.g., React, Python, Leadership..."
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                          <button
                            type="button"
                            onClick={() => removeSkill(index, skillIndex)}
                            className="text-red-500 hover:text-red-700 transition-colors"
                          >
                            <TrashIcon className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                    
                    <button
                      type="button"
                      onClick={() => addSkill(index)}
                      className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                    >
                      <PlusIcon className="w-4 h-4 mr-1" />
                      Add Skill
                    </button>
                  </div>
                )}

                {!expandedSkills[index] && (watch(`workExperience.${index}.skills`) || []).length === 0 && (
                  <button
                    type="button"
                    onClick={() => {
                      toggleSkills(index);
                      addSkill(index);
                    }}
                    className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-green-400 hover:text-green-600 transition-colors text-sm"
                  >
                    + Add skills and technologies you used in this role
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}

        {/* Add Experience Button */}
        <motion.button
          type="button"
          onClick={addExperience}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full py-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors flex items-center justify-center"
        >
          <PlusIcon className="w-6 h-6 mr-2" />
          Add Another Work Experience
        </motion.button>

        {/* Continue Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="flex justify-end pt-6 border-t"
        >
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Continue to Skills
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default WorkExperienceStep;