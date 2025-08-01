import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CodeBracketIcon,
  PlusIcon,
  TrashIcon,
  ComputerDesktopIcon,
  ChatBubbleLeftRightIcon,
  LanguageIcon,
  CheckBadgeIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

const skillsSchema = z.object({
  skills: z.array(z.object({
    id: z.string(),
    skillName: z.string().min(2, 'Skill name is required'),
    proficiency: z.enum(['beginner', 'intermediate', 'advanced', 'expert']),
    skillType: z.enum(['technical', 'soft', 'language', 'certification']),
    yearsOfExperience: z.number().min(0).max(50).optional(),
  })),
});

type SkillsFormData = z.infer<typeof skillsSchema>;

interface SkillsStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const SkillsStep: React.FC<SkillsStepProps> = ({ 
  data, 
  updateData, 
  onNext 
}) => {
  const [activeCategory, setActiveCategory] = useState<'technical' | 'soft' | 'language' | 'certification'>('technical');
  const [skillSuggestions] = useState({
    technical: [
      'JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'AWS', 'Docker', 'Git',
      'TypeScript', 'Java', 'C++', 'MongoDB', 'PostgreSQL', 'Redis', 'Kubernetes',
      'GraphQL', 'REST APIs', 'Machine Learning', 'Data Analysis', 'DevOps'
    ],
    soft: [
      'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Project Management',
      'Critical Thinking', 'Adaptability', 'Time Management', 'Mentoring', 'Negotiation',
      'Presentation Skills', 'Conflict Resolution', 'Strategic Planning', 'Innovation'
    ],
    language: [
      'English', 'Spanish', 'French', 'German', 'Chinese (Mandarin)', 'Japanese',
      'Portuguese', 'Italian', 'Russian', 'Arabic', 'Hindi', 'Korean'
    ],
    certification: [
      'AWS Certified Solutions Architect', 'Google Cloud Professional', 'Azure Fundamentals',
      'PMP', 'Scrum Master', 'CompTIA Security+', 'CISSP', 'Six Sigma', 'Salesforce Admin'
    ]
  });

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
    setValue
  } = useForm<SkillsFormData>({
    resolver: zodResolver(skillsSchema),
    defaultValues: {
      skills: data.skills.length > 0 ? data.skills : []
    }
  });

  const { fields: skillFields, append: appendSkill, remove: removeSkill } = useFieldArray({
    control,
    name: 'skills'
  });

  // Remove real-time updates to prevent infinite loops
  // Data will be updated on form submission instead

  const onSubmit = (formData: SkillsFormData) => {
    updateData('skills', formData.skills);
    onNext();
  };

  const addSkill = (skillType: typeof activeCategory, skillName: string = '') => {
    appendSkill({
      id: crypto.randomUUID(),
      skillName,
      proficiency: 'intermediate',
      skillType,
      yearsOfExperience: undefined,
    });
  };

  const addCustomSkill = () => {
    addSkill(activeCategory);
  };

  const addSuggestedSkill = (skillName: string) => {
    addSkill(activeCategory, skillName);
  };

  const getSkillsByCategory = (category: string) => {
    return skillFields.filter((_, index) => 
      watch(`skills.${index}.skillType`) === category
    );
  };

  const getProficiencyColor = (level: string) => {
    switch (level) {
      case 'beginner': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'intermediate': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'advanced': return 'bg-green-100 text-green-800 border-green-300';
      case 'expert': return 'bg-purple-100 text-purple-800 border-purple-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'technical': return ComputerDesktopIcon;
      case 'soft': return ChatBubbleLeftRightIcon;
      case 'language': return LanguageIcon;
      case 'certification': return CheckBadgeIcon;
      default: return CodeBracketIcon;
    }
  };

  const categoryInfo = {
    technical: {
      title: 'Technical Skills',
      description: 'Programming languages, frameworks, tools, and technologies',
      color: 'blue'
    },
    soft: {
      title: 'Soft Skills',
      description: 'Leadership, communication, and interpersonal abilities',
      color: 'green'
    },
    language: {
      title: 'Languages',
      description: 'Spoken languages and proficiency levels',
      color: 'purple'
    },
    certification: {
      title: 'Certifications',
      description: 'Professional certifications and credentials',
      color: 'yellow'
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Skills & Expertise
        </h2>
        <p className="text-gray-600">
          Showcase your technical skills, soft skills, languages, and certifications with proficiency levels.
        </p>
      </div>

      {/* Category Navigation */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-8">
        {Object.entries(categoryInfo).map(([key, info]) => {
          const IconComponent = getCategoryIcon(key);
          const isActive = activeCategory === key;
          const categorySkills = getSkillsByCategory(key);
          
          return (
            <button
              key={key}
              type="button"
              onClick={() => setActiveCategory(key as any)}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                isActive
                  ? `border-${info.color}-500 bg-${info.color}-50`
                  : 'border-gray-200 hover:border-gray-300 bg-white'
              }`}
            >
              <div className="flex items-center mb-2">
                <IconComponent className={`w-5 h-5 mr-2 ${
                  isActive ? `text-${info.color}-600` : 'text-gray-500'
                }`} />
                <span className={`font-medium ${
                  isActive ? `text-${info.color}-900` : 'text-gray-900'
                }`}>
                  {info.title}
                </span>
              </div>
              <p className={`text-xs ${
                isActive ? `text-${info.color}-700` : 'text-gray-500'
              }`}>
                {categorySkills.length} skills
              </p>
            </button>
          );
        })}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeCategory}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
            className="space-y-6"
          >
            {/* Category Header */}
            <div className={`bg-${categoryInfo[activeCategory].color}-50 rounded-lg p-6 border border-${categoryInfo[activeCategory].color}-200`}>
              <div className="flex items-center mb-3">
                {React.createElement(getCategoryIcon(activeCategory), {
                  className: `w-6 h-6 text-${categoryInfo[activeCategory].color}-600 mr-3`
                })}
                <h3 className={`text-xl font-semibold text-${categoryInfo[activeCategory].color}-900`}>
                  {categoryInfo[activeCategory].title}
                </h3>
              </div>
              <p className={`text-${categoryInfo[activeCategory].color}-700 mb-4`}>
                {categoryInfo[activeCategory].description}
              </p>
              
              {/* Skill Suggestions */}
              <div className="flex flex-wrap gap-2">
                {skillSuggestions[activeCategory].slice(0, 8).map((skill) => (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => addSuggestedSkill(skill)}
                    className={`px-3 py-1 text-sm bg-white border border-${categoryInfo[activeCategory].color}-300 text-${categoryInfo[activeCategory].color}-700 rounded-full hover:bg-${categoryInfo[activeCategory].color}-100 transition-colors`}
                  >
                    + {skill}
                  </button>
                ))}
              </div>
            </div>

            {/* Skills List */}
            <div className="space-y-4">
              {skillFields.map((field, index) => {
                if (watch(`skills.${index}.skillType`) !== activeCategory) return null;

                return (
                  <motion.div
                    key={field.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm"
                  >
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      {/* Skill Name */}
                      <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Skill Name *
                        </label>
                        <input
                          {...register(`skills.${index}.skillName`)}
                          type="text"
                          placeholder={`Enter ${activeCategory} skill...`}
                          className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                            errors.skills?.[index]?.skillName 
                              ? 'border-red-300 bg-red-50' 
                              : 'border-gray-300'
                          }`}
                        />
                        {errors.skills?.[index]?.skillName && (
                          <p className="mt-1 text-sm text-red-600">
                            {errors.skills[index]?.skillName?.message}
                          </p>
                        )}
                      </div>

                      {/* Proficiency */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Proficiency *
                        </label>
                        <select
                          {...register(`skills.${index}.proficiency`)}
                          className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="beginner">Beginner</option>
                          <option value="intermediate">Intermediate</option>
                          <option value="advanced">Advanced</option>
                          <option value="expert">Expert</option>
                        </select>
                      </div>

                      {/* Years of Experience & Remove Button */}
                      <div className="flex items-end space-x-2">
                        <div className="flex-1">
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Years
                          </label>
                          <input
                            {...register(`skills.${index}.yearsOfExperience`, { valueAsNumber: true })}
                            type="number"
                            min="0"
                            max="50"
                            placeholder="0"
                            className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <button
                          type="button"
                          onClick={() => removeSkill(index)}
                          className="p-2 text-red-500 hover:text-red-700 transition-colors"
                        >
                          <TrashIcon className="w-5 h-5" />
                        </button>
                      </div>
                    </div>

                    {/* Proficiency Badge */}
                    <div className="mt-3 flex items-center">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full border ${
                        getProficiencyColor(watch(`skills.${index}.proficiency`))
                      }`}>
                        {watch(`skills.${index}.proficiency`)} Level
                      </span>
                      {watch(`skills.${index}.yearsOfExperience`) && (
                        <span className="ml-2 text-sm text-gray-500">
                          • {watch(`skills.${index}.yearsOfExperience`)} year
                          {watch(`skills.${index}.yearsOfExperience`) !== 1 ? 's' : ''} experience
                        </span>
                      )}
                    </div>

                    {/* Hidden field for skill type */}
                    <input
                      {...register(`skills.${index}.skillType`)}
                      type="hidden"
                      value={activeCategory}
                    />
                  </motion.div>
                );
              })}

              {/* Add Custom Skill Button */}
              <motion.button
                type="button"
                onClick={addCustomSkill}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-${categoryInfo[activeCategory].color}-400 hover:text-${categoryInfo[activeCategory].color}-600 transition-colors flex items-center justify-center`}
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Add Custom {categoryInfo[activeCategory].title.slice(0, -1)}
              </motion.button>

              {/* Empty State */}
              {getSkillsByCategory(activeCategory).length === 0 && (
                <div className="text-center py-8">
                  <div className={`w-16 h-16 bg-${categoryInfo[activeCategory].color}-100 rounded-full flex items-center justify-center mx-auto mb-4`}>
                    {React.createElement(getCategoryIcon(activeCategory), {
                      className: `w-8 h-8 text-${categoryInfo[activeCategory].color}-600`
                    })}
                  </div>
                  <p className="text-gray-500 mb-4">
                    No {categoryInfo[activeCategory].title.toLowerCase()} added yet
                  </p>
                  <p className="text-sm text-gray-400">
                    Click the suggestions above or add a custom skill to get started.
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Skills Summary */}
        {skillFields.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-gray-50 rounded-lg p-6 border"
          >
            <h4 className="font-medium text-gray-900 mb-4">Skills Summary</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              {Object.entries(categoryInfo).map(([key, info]) => {
                const count = getSkillsByCategory(key).length;
                return (
                  <div key={key} className="bg-white rounded-lg p-3">
                    <div className={`text-2xl font-bold text-${info.color}-600`}>
                      {count}
                    </div>
                    <div className="text-sm text-gray-600">{info.title}</div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}

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
            Continue to Projects
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default SkillsStep;