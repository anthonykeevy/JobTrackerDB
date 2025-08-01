import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  RocketLaunchIcon,
  PlusIcon,
  TrashIcon,
  LinkIcon,
  CodeBracketIcon,
  CalendarIcon,
  EyeIcon,
  StarIcon,
  CheckCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

const projectsSchema = z.object({
  projects: z.array(z.object({
    id: z.string(),
    projectName: z.string().min(2, 'Project name is required'),
    description: z.string().min(10, 'Please provide a detailed description'),
    technologies: z.array(z.string()),
    projectURL: z.string().url('Please enter a valid URL').optional().or(z.literal('')),
    githubURL: z.string().url('Please enter a valid GitHub URL').optional().or(z.literal('')),
    startDate: z.string().min(1, 'Start date is required'),
    endDate: z.string().optional(),
    isOngoing: z.boolean(),
    projectType: z.enum(['personal', 'professional', 'open-source', 'academic', 'freelance']),
    teamSize: z.number().min(1).optional(),
    role: z.string().optional(),
    achievements: z.array(z.string()),
    challenges: z.string().optional(),
  })),
});

type ProjectsFormData = z.infer<typeof projectsSchema>;

interface ProjectsStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const ProjectsStep: React.FC<ProjectsStepProps> = ({ 
  data, 
  updateData, 
  onNext 
}) => {
  const [expandedSections, setExpandedSections] = useState<{[key: number]: string[]}>({});
  const [techInput, setTechInput] = useState<{[key: number]: string}>({});

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
    setValue,
    getValues
  } = useForm<ProjectsFormData>({
    resolver: zodResolver(projectsSchema),
    defaultValues: {
      projects: data.projects.length > 0 ? data.projects : [{
        id: crypto.randomUUID(),
        projectName: '',
        description: '',
        technologies: [],
        projectURL: '',
        githubURL: '',
        startDate: '',
        endDate: '',
        isOngoing: false,
        projectType: 'personal',
        teamSize: 1,
        role: '',
        achievements: [],
        challenges: '',
      }]
    }
  });

  const { fields: projectFields, append: appendProject, remove: removeProject } = useFieldArray({
    control,
    name: 'projects'
  });

  // Remove real-time updates to prevent infinite loops
  // Data will be updated on form submission instead

  const onSubmit = (formData: ProjectsFormData) => {
    updateData('projects', formData.projects);
    onNext();
  };

  const addProject = () => {
    appendProject({
      id: crypto.randomUUID(),
      projectName: '',
      description: '',
      technologies: [],
      projectURL: '',
      githubURL: '',
      startDate: '',
      endDate: '',
      isOngoing: false,
      projectType: 'personal',
      teamSize: 1,
      role: '',
      achievements: [],
      challenges: '',
    });
  };

  const addTechnology = (projectIndex: number) => {
    const input = techInput[projectIndex]?.trim();
    if (input) {
      const currentTechs = getValues(`projects.${projectIndex}.technologies`) || [];
      if (!currentTechs.includes(input)) {
        setValue(`projects.${projectIndex}.technologies`, [...currentTechs, input]);
        setTechInput(prev => ({ ...prev, [projectIndex]: '' }));
      }
    }
  };

  const removeTechnology = (projectIndex: number, techIndex: number) => {
    const currentTechs = getValues(`projects.${projectIndex}.technologies`) || [];
    setValue(`projects.${projectIndex}.technologies`, 
      currentTechs.filter((_, index) => index !== techIndex)
    );
  };

  const addAchievement = (projectIndex: number) => {
    const currentAchievements = getValues(`projects.${projectIndex}.achievements`) || [];
    setValue(`projects.${projectIndex}.achievements`, [...currentAchievements, '']);
  };

  const removeAchievement = (projectIndex: number, achievementIndex: number) => {
    const currentAchievements = getValues(`projects.${projectIndex}.achievements`) || [];
    setValue(`projects.${projectIndex}.achievements`, 
      currentAchievements.filter((_, index) => index !== achievementIndex)
    );
  };

  const toggleSection = (projectIndex: number, section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [projectIndex]: prev[projectIndex]?.includes(section) 
        ? prev[projectIndex].filter(s => s !== section)
        : [...(prev[projectIndex] || []), section]
    }));
  };

  const projectTypes = [
    { value: 'personal', label: 'Personal Project', color: 'blue' },
    { value: 'professional', label: 'Professional Work', color: 'green' },
    { value: 'open-source', label: 'Open Source', color: 'purple' },
    { value: 'academic', label: 'Academic Project', color: 'orange' },
    { value: 'freelance', label: 'Freelance Work', color: 'pink' },
  ];

  const getProjectTypeColor = (type: string) => {
    const typeObj = projectTypes.find(t => t.value === type);
    return typeObj?.color || 'gray';
  };

  const popularTechnologies = [
    'React', 'Node.js', 'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 
    'AWS', 'Docker', 'MongoDB', 'PostgreSQL', 'Git', 'REST APIs', 'GraphQL',
    'Vue.js', 'Angular', 'Express.js', 'Django', 'Flask', 'Spring Boot'
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Projects & Portfolio
        </h2>
        <p className="text-gray-600">
          Showcase your best work, side projects, and technical accomplishments to demonstrate your skills in action.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {projectFields.map((field, index) => (
          <motion.div
            key={field.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-lg transition-shadow duration-200"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className={`p-3 rounded-lg bg-${getProjectTypeColor(watch(`projects.${index}.projectType`))}-100`}>
                  <RocketLaunchIcon className={`w-6 h-6 text-${getProjectTypeColor(watch(`projects.${index}.projectType`))}-600`} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">
                  Project {index + 1}
                </h3>
                <span className={`px-3 py-1 text-xs font-medium rounded-full bg-${getProjectTypeColor(watch(`projects.${index}.projectType`))}-100 text-${getProjectTypeColor(watch(`projects.${index}.projectType`))}-800`}>
                  {projectTypes.find(t => t.value === watch(`projects.${index}.projectType`))?.label}
                </span>
              </div>
              {projectFields.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeProject(index)}
                  className="text-red-500 hover:text-red-700 transition-colors p-2 hover:bg-red-50 rounded-lg"
                >
                  <TrashIcon className="w-5 h-5" />
                </button>
              )}
            </div>

            <div className="space-y-6">
              {/* Basic Project Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Project Name */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Name *
                  </label>
                  <input
                    {...register(`projects.${index}.projectName`)}
                    type="text"
                    placeholder="e.g., E-commerce Platform, AI Chatbot, Mobile App"
                    className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      errors.projects?.[index]?.projectName 
                        ? 'border-red-300 bg-red-50' 
                        : 'border-gray-300'
                    }`}
                  />
                  {errors.projects?.[index]?.projectName && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.projects[index]?.projectName?.message}
                    </p>
                  )}
                </div>

                {/* Project Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Type *
                  </label>
                  <select
                    {...register(`projects.${index}.projectType`)}
                    className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {projectTypes.map((type) => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </select>
                </div>

                {/* Team Size & Role */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Team Size
                  </label>
                  <select
                    {...register(`projects.${index}.teamSize`, { valueAsNumber: true })}
                    className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value={1}>Solo Project</option>
                    <option value={2}>2 people</option>
                    <option value={3}>3 people</option>
                    <option value={4}>4 people</option>
                    <option value={5}>5+ people</option>
                  </select>
                </div>

                {/* Role */}
                {watch(`projects.${index}.teamSize`) > 1 && (
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Role
                    </label>
                    <input
                      {...register(`projects.${index}.role`)}
                      type="text"
                      placeholder="e.g., Lead Developer, Frontend Developer, Project Manager"
                      className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                )}

                {/* Dates */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Start Date *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CalendarIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`projects.${index}.startDate`)}
                      type="month"
                      className={`block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.projects?.[index]?.startDate 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                    />
                  </div>
                  {errors.projects?.[index]?.startDate && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.projects[index]?.startDate?.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    End Date
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CalendarIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`projects.${index}.endDate`)}
                      type="month"
                      disabled={watch(`projects.${index}.isOngoing`)}
                      className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                    />
                  </div>
                </div>

                {/* Ongoing Project */}
                <div className="md:col-span-2">
                  <label className="flex items-center">
                    <input
                      {...register(`projects.${index}.isOngoing`)}
                      type="checkbox"
                      className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                    />
                    <span className="ml-2 text-sm text-gray-700">This is an ongoing project</span>
                  </label>
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Description *
                </label>
                <textarea
                  {...register(`projects.${index}.description`)}
                  rows={4}
                  placeholder="Describe what the project does, its purpose, and key features..."
                  className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                    errors.projects?.[index]?.description 
                      ? 'border-red-300 bg-red-50' 
                      : 'border-gray-300'
                  }`}
                />
                {errors.projects?.[index]?.description && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.projects[index]?.description?.message}
                  </p>
                )}
              </div>

              {/* Technologies */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Technologies & Tools
                </label>
                
                {/* Technology Input */}
                <div className="flex space-x-2 mb-3">
                  <input
                    type="text"
                    value={techInput[index] || ''}
                    onChange={(e) => setTechInput(prev => ({ ...prev, [index]: e.target.value }))}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTechnology(index))}
                    placeholder="Add technology (e.g., React, Python, AWS)"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={() => addTechnology(index)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <PlusIcon className="w-4 h-4" />
                  </button>
                </div>

                {/* Popular Technologies */}
                <div className="mb-3">
                  <p className="text-xs text-gray-500 mb-2">Popular technologies:</p>
                  <div className="flex flex-wrap gap-2">
                    {popularTechnologies.slice(0, 8).map((tech) => (
                      <button
                        key={tech}
                        type="button"
                        onClick={() => {
                          const currentTechs = getValues(`projects.${index}.technologies`) || [];
                          if (!currentTechs.includes(tech)) {
                            setValue(`projects.${index}.technologies`, [...currentTechs, tech]);
                          }
                        }}
                        className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-md hover:bg-blue-100 hover:text-blue-700 transition-colors"
                      >
                        + {tech}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Technology Tags */}
                <div className="flex flex-wrap gap-2">
                  {(watch(`projects.${index}.technologies`) || []).map((tech, techIndex) => (
                    <span
                      key={techIndex}
                      className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                    >
                      <CodeBracketIcon className="w-4 h-4 mr-1" />
                      {tech}
                      <button
                        type="button"
                        onClick={() => removeTechnology(index, techIndex)}
                        className="ml-2 text-blue-600 hover:text-blue-800"
                      >
                        <XMarkIcon className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* URLs */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project URL (Demo/Live Site)
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <LinkIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`projects.${index}.projectURL`)}
                      type="url"
                      placeholder="https://your-project.com"
                      className={`block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.projects?.[index]?.projectURL 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                    />
                  </div>
                  {errors.projects?.[index]?.projectURL && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.projects[index]?.projectURL?.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    GitHub URL
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <CodeBracketIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      {...register(`projects.${index}.githubURL`)}
                      type="url"
                      placeholder="https://github.com/username/repo"
                      className={`block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.projects?.[index]?.githubURL 
                          ? 'border-red-300 bg-red-50' 
                          : 'border-gray-300'
                      }`}
                    />
                  </div>
                  {errors.projects?.[index]?.githubURL && (
                    <p className="mt-1 text-sm text-red-600">
                      {errors.projects[index]?.githubURL?.message}
                    </p>
                  )}
                </div>
              </div>

              {/* Expandable Sections */}
              <div className="border-t pt-6 space-y-4">
                {/* Achievements */}
                <div>
                  <button
                    type="button"
                    onClick={() => toggleSection(index, 'achievements')}
                    className="flex items-center justify-between w-full text-left"
                  >
                    <div className="flex items-center space-x-2">
                      <StarIcon className="w-5 h-5 text-yellow-500" />
                      <h4 className="font-medium text-gray-900">Key Achievements</h4>
                      <span className="text-sm text-gray-500">
                        ({(watch(`projects.${index}.achievements`) || []).length})
                      </span>
                    </div>
                    <span className="text-gray-400">
                      {expandedSections[index]?.includes('achievements') ? '▼' : '▶'}
                    </span>
                  </button>

                  {expandedSections[index]?.includes('achievements') && (
                    <div className="mt-3 space-y-3">
                      {(watch(`projects.${index}.achievements`) || []).map((_, achievementIndex) => (
                        <div key={achievementIndex} className="flex items-center space-x-2">
                          <input
                            {...register(`projects.${index}.achievements.${achievementIndex}`)}
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
                </div>

                {/* Challenges */}
                <div>
                  <button
                    type="button"
                    onClick={() => toggleSection(index, 'challenges')}
                    className="flex items-center justify-between w-full text-left"
                  >
                    <div className="flex items-center space-x-2">
                      <CheckCircleIcon className="w-5 h-5 text-green-500" />
                      <h4 className="font-medium text-gray-900">Challenges & Solutions</h4>
                    </div>
                    <span className="text-gray-400">
                      {expandedSections[index]?.includes('challenges') ? '▼' : '▶'}
                    </span>
                  </button>

                  {expandedSections[index]?.includes('challenges') && (
                    <div className="mt-3">
                      <textarea
                        {...register(`projects.${index}.challenges`)}
                        rows={3}
                        placeholder="Describe any challenges you faced and how you solved them..."
                        className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ))}

        {/* Add Project Button */}
        <motion.button
          type="button"
          onClick={addProject}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full py-4 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors flex items-center justify-center space-x-2"
        >
          <PlusIcon className="w-6 h-6" />
          <span className="font-medium">Add Another Project</span>
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
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center space-x-2"
          >
            <span>Continue to Review</span>
            <EyeIcon className="w-5 h-5" />
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default ProjectsStep;