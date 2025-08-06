import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  AcademicCapIcon,
  PlusIcon,
  TrashIcon,
  BuildingLibraryIcon,
  StarIcon,
  CheckBadgeIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';

const educationSchema = z.object({
  education: z.array(z.object({
    id: z.string(),
    institutionName: z.string().min(2, 'Institution name is required'),
    degree: z.string().min(2, 'Degree is required'),
    fieldOfStudy: z.string().min(2, 'Field of study is required'),
    startDate: z.string().min(1, 'Start date is required'),
    endDate: z.string().optional(),
    isCurrentlyEnrolled: z.boolean(),
    gpa: z.number().min(0).max(4).optional(),
    description: z.string().optional(),
  })),
  certifications: z.array(z.object({
    id: z.string(),
    certificationName: z.string().min(2, 'Certification name is required'),
    issuingOrganization: z.string().min(2, 'Issuing organization is required'),
    issueDate: z.string().min(1, 'Issue date is required'),
    expiryDate: z.string().optional(),
    credentialID: z.string().optional(),
    description: z.string().optional(),
  })),
});

type EducationFormData = z.infer<typeof educationSchema>;

interface EducationStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const EducationStep: React.FC<EducationStepProps> = ({ 
  data, 
  updateData, 
  onNext 
}) => {
  const [activeTab, setActiveTab] = useState<'education' | 'certifications'>('education');

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch
  } = useForm<EducationFormData>({
    resolver: zodResolver(educationSchema),
    defaultValues: {
      education: data.education.length > 0 ? data.education : [{
        id: crypto.randomUUID(),
        institutionName: '',
        degree: '',
        fieldOfStudy: '',
        startDate: '',
        endDate: '',
        isCurrentlyEnrolled: false,
        gpa: undefined,
        description: '',
      }],
      certifications: data.certifications.length > 0 ? data.certifications : []
    }
  });

  const { fields: educationFields, append: appendEducation, remove: removeEducation } = useFieldArray({
    control,
    name: 'education'
  });

  const { fields: certificationFields, append: appendCertification, remove: removeCertification } = useFieldArray({
    control,
    name: 'certifications'
  });

  // Remove real-time updates to prevent infinite loops
  // Data will be updated on form submission instead

  const onSubmit = (formData: EducationFormData) => {
    updateData('education', formData.education);
    updateData('certifications', formData.certifications);
    onNext();
  };

  const addEducation = () => {
    appendEducation({
      id: crypto.randomUUID(),
      institutionName: '',
      degree: '',
      fieldOfStudy: '',
      startDate: '',
      endDate: '',
      isCurrentlyEnrolled: false,
      gpa: undefined,
      description: '',
    });
  };

  const addCertification = () => {
    appendCertification({
      id: crypto.randomUUID(),
      certificationName: '',
      issuingOrganization: '',
      issueDate: '',
      expiryDate: '',
      credentialID: '',
      description: '',
    });
  };

  const degreeOptions = [
    'High School Diploma',
    'Associate Degree',
    'Bachelor\'s Degree',
    'Master\'s Degree',
    'PhD/Doctorate',
    'Professional Certificate',
    'Bootcamp Certificate',
    'Other'
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Education & Certifications
        </h2>
        <p className="text-gray-600">
          Add your educational background and professional certifications to showcase your qualifications.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-8">
        <button
          type="button"
          onClick={() => setActiveTab('education')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'education'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <AcademicCapIcon className="w-4 h-4 inline mr-2" />
          Education
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('certifications')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            activeTab === 'certifications'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <CheckBadgeIcon className="w-4 h-4 inline mr-2" />
          Certifications
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Education Tab */}
        <AnimatePresence mode="wait">
          {activeTab === 'education' && (
            <motion.div
              key="education"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              {educationFields.map((field, index) => (
                <motion.div
                  key={field.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <BuildingLibraryIcon className="w-5 h-5 text-blue-600 mr-2" />
                      <h3 className="text-lg font-medium text-gray-900">
                        Education {index + 1}
                      </h3>
                    </div>
                    {educationFields.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeEducation(index)}
                        className="text-red-500 hover:text-red-700 transition-colors"
                      >
                        <TrashIcon className="w-5 h-5" />
                      </button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Institution Name */}
                    <div className="md:col-span-2">
                      <label htmlFor={`institutionName-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                        Institution Name *
                      </label>
                      <input
                        {...register(`education.${index}.institutionName`)}
                        id={`institutionName-${index}`}
                        type="text"
                        placeholder="e.g., Stanford University"
                        className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                          errors.education?.[index]?.institutionName 
                            ? 'border-red-300 bg-red-50' 
                            : 'border-gray-300'
                        }`}
                      />
                      {errors.education?.[index]?.institutionName && (
                        <p className="mt-1 text-sm text-red-600">
                          {errors.education[index]?.institutionName?.message}
                        </p>
                      )}
                    </div>

                    {/* Degree */}
                    <div>
                      <label htmlFor={`degree-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                        Degree *
                      </label>
                      <select
                        {...register(`education.${index}.degree`)}
                        id={`degree-${index}`}
                        className={`block w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                          errors.education?.[index]?.degree 
                            ? 'border-red-300 bg-red-50' 
                            : 'border-gray-300'
                        }`}
                      >
                        <option value="">Select degree</option>
                        {degreeOptions.map((degree) => (
                          <option key={degree} value={degree}>{degree}</option>
                        ))}
                      </select>
                      {errors.education?.[index]?.degree && (
                        <p className="mt-1 text-sm text-red-600">
                          {errors.education[index]?.degree?.message}
                        </p>
                      )}
                    </div>

                    {/* Field of Study */}
                    <div>
                      <label htmlFor={`fieldOfStudy-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                        Field of Study *
                      </label>
                      <input
                        {...register(`education.${index}.fieldOfStudy`)}
                        id={`fieldOfStudy-${index}`}
                        type="text"
                        placeholder="e.g., Computer Science"
                        className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                          errors.education?.[index]?.fieldOfStudy 
                            ? 'border-red-300 bg-red-50' 
                            : 'border-gray-300'
                        }`}
                      />
                      {errors.education?.[index]?.fieldOfStudy && (
                        <p className="mt-1 text-sm text-red-600">
                          {errors.education[index]?.fieldOfStudy?.message}
                        </p>
                      )}
                    </div>

                    {/* Dates */}
                    <div>
                      <label htmlFor={`startDate-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                        Start Date *
                      </label>
                      <input
                        {...register(`education.${index}.startDate`)}
                        id={`startDate-${index}`}
                        type="month"
                        className={`block w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                          errors.education?.[index]?.startDate 
                            ? 'border-red-300 bg-red-50' 
                            : 'border-gray-300'
                        }`}
                      />
                      {errors.education?.[index]?.startDate && (
                        <p className="mt-1 text-sm text-red-600">
                          {errors.education[index]?.startDate?.message}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        End Date
                      </label>
                      <input
                        {...register(`education.${index}.endDate`)}
                        type="month"
                        disabled={watch(`education.${index}.isCurrentlyEnrolled`)}
                        className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                      />
                    </div>

                    {/* Currently Enrolled & GPA */}
                    <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor={`currentlyEnrolled-${index}`} className="flex items-center">
                          <input
                            {...register(`education.${index}.isCurrentlyEnrolled`)}
                            id={`currentlyEnrolled-${index}`}
                            type="checkbox"
                            className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                          />
                          <span className="ml-2 text-sm text-gray-700">Currently enrolled</span>
                        </label>
                      </div>

                      <div>
                        <label htmlFor={`gpa-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                          GPA (optional)
                        </label>
                        <input
                          {...register(`education.${index}.gpa`, { 
                            valueAsNumber: true,
                            setValueAs: (value) => value === '' ? undefined : Number(value)
                          })}
                          id={`gpa-${index}`}
                          type="number"
                          step="0.01"
                          min="0"
                          max="4"
                          placeholder="e.g., 3.8"
                          className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>

                    {/* Description */}
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Description (optional)
                      </label>
                      <textarea
                        {...register(`education.${index}.description`)}
                        rows={3}
                        placeholder="Notable achievements, coursework, activities..."
                        className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      />
                    </div>
                  </div>
                </motion.div>
              ))}

              <motion.button
                type="button"
                onClick={addEducation}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-blue-400 hover:text-blue-600 transition-colors flex items-center justify-center"
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Add Another Education
              </motion.button>
            </motion.div>
          )}

          {/* Certifications Tab */}
          {activeTab === 'certifications' && (
            <motion.div
              key="certifications"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              {certificationFields.length === 0 ? (
                <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                  <CheckBadgeIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500 mb-4">No certifications added yet</p>
                  <button
                    type="button"
                    onClick={addCertification}
                    className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <PlusIcon className="w-4 h-4 mr-2" />
                    Add Certification
                  </button>
                </div>
              ) : (
                <>
                  {certificationFields.map((field, index) => (
                    <motion.div
                      key={field.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                      className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center">
                          <StarIcon className="w-5 h-5 text-yellow-500 mr-2" />
                          <h3 className="text-lg font-medium text-gray-900">
                            Certification {index + 1}
                          </h3>
                        </div>
                        <button
                          type="button"
                          onClick={() => removeCertification(index)}
                          className="text-red-500 hover:text-red-700 transition-colors"
                        >
                          <TrashIcon className="w-5 h-5" />
                        </button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Certification Name */}
                        <div className="md:col-span-2">
                        <label htmlFor={`certificationName-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                          Certification Name *
                        </label>
                        <input
                          {...register(`certifications.${index}.certificationName`)}
                          id={`certificationName-${index}`}
                          type="text"
                          placeholder="e.g., AWS Certified Solutions Architect"
                          className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                            errors.certifications?.[index]?.certificationName 
                              ? 'border-red-300 bg-red-50' 
                              : 'border-gray-300'
                          }`}
                        />
                          {errors.certifications?.[index]?.certificationName && (
                            <p className="mt-1 text-sm text-red-600">
                              {errors.certifications[index]?.certificationName?.message}
                            </p>
                          )}
                        </div>

                        {/* Issuing Organization */}
                        <div>
                          <label htmlFor={`issuingOrganization-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                            Issuing Organization *
                          </label>
                          <input
                            {...register(`certifications.${index}.issuingOrganization`)}
                            id={`issuingOrganization-${index}`}
                            type="text"
                            placeholder="e.g., Amazon Web Services"
                            className={`block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                              errors.certifications?.[index]?.issuingOrganization 
                                ? 'border-red-300 bg-red-50' 
                                : 'border-gray-300'
                            }`}
                          />
                          {errors.certifications?.[index]?.issuingOrganization && (
                            <p className="mt-1 text-sm text-red-600">
                              {errors.certifications[index]?.issuingOrganization?.message}
                            </p>
                          )}
                        </div>

                        {/* Issue Date */}
                        <div>
                          <label htmlFor={`issueDate-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                            Issue Date *
                          </label>
                          <input
                            {...register(`certifications.${index}.issueDate`)}
                            id={`issueDate-${index}`}
                            type="month"
                            className={`block w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                              errors.certifications?.[index]?.issueDate 
                                ? 'border-red-300 bg-red-50' 
                                : 'border-gray-300'
                            }`}
                          />
                          {errors.certifications?.[index]?.issueDate && (
                            <p className="mt-1 text-sm text-red-600">
                              {errors.certifications[index]?.issueDate?.message}
                            </p>
                          )}
                        </div>

                        {/* Expiry Date & Credential ID */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Expiry Date (optional)
                          </label>
                          <input
                            {...register(`certifications.${index}.expiryDate`)}
                            type="month"
                            className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Credential ID (optional)
                          </label>
                          <input
                            {...register(`certifications.${index}.credentialID`)}
                            type="text"
                            placeholder="e.g., AWS-123456"
                            className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>

                        {/* Description */}
                        <div className="md:col-span-2">
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Description (optional)
                          </label>
                          <textarea
                            {...register(`certifications.${index}.description`)}
                            rows={2}
                            placeholder="Skills and knowledge gained..."
                            className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                          />
                        </div>
                      </div>
                    </motion.div>
                  ))}

                  <motion.button
                    type="button"
                    onClick={addCertification}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-yellow-400 hover:text-yellow-600 transition-colors flex items-center justify-center"
                  >
                    <PlusIcon className="w-5 h-5 mr-2" />
                    Add Another Certification
                  </motion.button>
                </>
              )}
            </motion.div>
          )}
        </AnimatePresence>

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
            Continue to Work Experience
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default EducationStep;