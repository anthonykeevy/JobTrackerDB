import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  AcademicCapIcon, 
  BriefcaseIcon, 
  CurrencyDollarIcon,
  MapPinIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types';

interface CareerAspirationStepProps {
  data: ProfileData;
  updateData: (data: Partial<ProfileData>) => void;
  onNext: () => void;
  onPrevious: () => void;
}

const schema = z.object({
  currentTitle: z.string().min(2, 'Current title is required'),
  shortTermRole: z.string().min(2, 'Short-term role goal is required'),
  longTermRole: z.string().min(2, 'Long-term role goal is required'),
  aspirationStatement: z.string().min(10, 'Please provide a detailed career aspiration statement'),
  targetIndustries: z.array(z.string()).min(1, 'Please select at least one target industry'),
  workPreferences: z.object({
    arrangements: z.array(z.object({
      type: z.enum(['remote', 'hybrid', 'onsite', 'flexible']),
      preference: z.number().min(1).max(4),
    })),
    willingToRelocate: z.boolean(),
  }),
  salaryExpectations: z.object({
    employmentType: z.enum(['full-time', 'part-time', 'contract', 'temporary', 'freelance']),
    amount: z.string().min(1, 'Salary amount is required'),
    period: z.enum(['hourly', 'daily', 'weekly', 'fortnightly', 'monthly', 'annually']),
    currency: z.string().min(3, 'Currency is required'),
    flexible: z.boolean(),
    notes: z.string().optional(),
  }),
});

type FormData = z.infer<typeof schema>;

const POPULAR_INDUSTRIES = [
  'Technology & Software', 'Healthcare & Medicine', 'Finance & Banking', 'Education & Training',
  'Marketing & Advertising', 'Manufacturing & Engineering', 'Retail & E-commerce', 'Consulting',
  'Media & Entertainment', 'Real Estate', 'Transportation & Logistics', 'Energy & Utilities',
  'Government & Public Sector', 'Non-profit & NGO', 'Hospitality & Tourism', 'Sports & Recreation',
  'Agriculture & Food', 'Legal Services', 'Architecture & Construction', 'Art & Design'
];

const CURRENCIES = [
  { code: 'AUD', symbol: 'A$', name: 'Australian Dollar' },
  { code: 'USD', symbol: '$', name: 'US Dollar' },
  { code: 'EUR', symbol: '€', name: 'Euro' },
  { code: 'GBP', symbol: '£', name: 'British Pound' },
  { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar' },
  { code: 'NZD', symbol: 'NZ$', name: 'New Zealand Dollar' },
  { code: 'SGD', symbol: 'S$', name: 'Singapore Dollar' },
];

const WORK_ARRANGEMENT_INFO = {
  remote: { label: 'Remote', description: 'Work from anywhere, full virtual collaboration' },
  hybrid: { label: 'Hybrid', description: 'Mix of office and remote work' },
  onsite: { label: 'On-site', description: 'Work from office/company location' },
  flexible: { label: 'Flexible', description: 'Open to various arrangements' },
};

export default function CareerAspirationStep({ data, updateData, onNext, onPrevious }: CareerAspirationStepProps) {
  const [industrySearch, setIndustrySearch] = useState('');
  const [showAllIndustries, setShowAllIndustries] = useState(false);

  const { register, handleSubmit, formState: { errors }, watch, setValue, getValues } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      currentTitle: data.careerAspiration?.currentTitle || '',
      shortTermRole: data.careerAspiration?.shortTermRole || '',
      longTermRole: data.careerAspiration?.longTermRole || '',
      aspirationStatement: data.careerAspiration?.aspirationStatement || '',
      targetIndustries: data.careerAspiration?.targetIndustries || [],
      workPreferences: {
        arrangements: data.careerAspiration?.workPreferences?.arrangements || [
          { type: 'remote', preference: 1 },
          { type: 'hybrid', preference: 2 },
          { type: 'onsite', preference: 3 },
          { type: 'flexible', preference: 4 },
        ],
        willingToRelocate: data.careerAspiration?.workPreferences?.willingToRelocate || false,
      },
      salaryExpectations: {
        employmentType: data.careerAspiration?.salaryExpectations?.employmentType || 'full-time',
        amount: data.careerAspiration?.salaryExpectations?.amount || '',
        period: data.careerAspiration?.salaryExpectations?.period || 'annually',
        currency: data.careerAspiration?.salaryExpectations?.currency || 'AUD',
        flexible: data.careerAspiration?.salaryExpectations?.flexible ?? true,
        notes: data.careerAspiration?.salaryExpectations?.notes || '',
      },
    },
  });

  const watchedArrangements = watch('workPreferences.arrangements');
  const watchedTargetIndustries = watch('targetIndustries');
  const watchedEmploymentType = watch('salaryExpectations.employmentType');
  const watchedPeriod = watch('salaryExpectations.period');
  const watchedCurrency = watch('salaryExpectations.currency');

  const onSubmit = (formData: FormData) => {
    updateData({ careerAspiration: formData });
    onNext();
  };

  const toggleIndustry = (industry: string) => {
    const current = getValues('targetIndustries');
    const updated = current.includes(industry)
      ? current.filter(i => i !== industry)
      : [...current, industry];
    setValue('targetIndustries', updated);
  };

  const movePreference = (index: number, direction: 'up' | 'down') => {
    const arrangements = [...watchedArrangements];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;
    
    if (targetIndex >= 0 && targetIndex < arrangements.length) {
      // Swap preference values
      const temp = arrangements[index].preference;
      arrangements[index].preference = arrangements[targetIndex].preference;
      arrangements[targetIndex].preference = temp;
      
      // Swap positions in array
      [arrangements[index], arrangements[targetIndex]] = [arrangements[targetIndex], arrangements[index]];
      
      setValue('workPreferences.arrangements', arrangements);
    }
  };

  const filteredIndustries = POPULAR_INDUSTRIES.filter(industry =>
    industry.toLowerCase().includes(industrySearch.toLowerCase())
  );

  const selectedCurrency = CURRENCIES.find(c => c.code === watchedCurrency);

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Career Goals & Aspirations</h2>
        <p className="text-gray-600">
          Define your career journey from where you are now to where you want to be
        </p>
      </motion.div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        
        {/* Current & Future Roles */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-6">
            <BriefcaseIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Career Progression</h3>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Job Title *
                <span className="text-xs text-gray-500 ml-1">(What's your current position?)</span>
              </label>
              <input
                {...register('currentTitle')}
                type="text"
                placeholder="e.g., Senior Software Engineer, Marketing Manager"
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.currentTitle ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.currentTitle && (
                <p className="mt-1 text-sm text-red-600">{errors.currentTitle.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Short-term Goal (1-2 years) *
                </label>
                <input
                  {...register('shortTermRole')}
                  type="text"
                  placeholder="e.g., Lead Developer, Senior Manager"
                  className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.shortTermRole ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {errors.shortTermRole && (
                  <p className="mt-1 text-sm text-red-600">{errors.shortTermRole.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Long-term Goal (3-5 years) *
                </label>
                <input
                  {...register('longTermRole')}
                  type="text"
                  placeholder="e.g., Engineering Director, VP of Marketing"
                  className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.longTermRole ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {errors.longTermRole && (
                  <p className="mt-1 text-sm text-red-600">{errors.longTermRole.message}</p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Career Vision Statement *
              </label>
              <textarea
                {...register('aspirationStatement')}
                rows={4}
                placeholder="Describe your career aspirations, what drives you professionally, and the impact you want to make..."
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                  errors.aspirationStatement ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.aspirationStatement && (
                <p className="mt-1 text-sm text-red-600">{errors.aspirationStatement.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Target Industries */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-6">
            <AcademicCapIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Target Industries</h3>
          </div>
          
          <div className="mb-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search industries..."
                value={industrySearch}
                onChange={(e) => setIndustrySearch(e.target.value)}
                className="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {(showAllIndustries ? filteredIndustries : filteredIndustries.slice(0, 12)).map((industry) => (
                <button
                  key={industry}
                  type="button"
                  onClick={() => toggleIndustry(industry)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                    watchedTargetIndustries.includes(industry)
                      ? 'bg-blue-600 text-white shadow-md transform scale-105'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm'
                  }`}
                >
                  {industry}
                </button>
              ))}
            </div>

            {filteredIndustries.length > 12 && (
              <button
                type="button"
                onClick={() => setShowAllIndustries(!showAllIndustries)}
                className="text-blue-600 text-sm font-medium hover:text-blue-700"
              >
                {showAllIndustries ? 'Show Less' : `Show ${filteredIndustries.length - 12} More Industries`}
              </button>
            )}

            {watchedTargetIndustries.length > 0 && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-900 mb-2">Selected Industries:</p>
                <div className="flex flex-wrap gap-2">
                  {watchedTargetIndustries.map((industry) => (
                    <span
                      key={industry}
                      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {industry}
                      <button
                        type="button"
                        onClick={() => toggleIndustry(industry)}
                        className="ml-2 inline-flex items-center justify-center w-4 h-4 rounded-full hover:bg-blue-200"
                      >
                        <XMarkIcon className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {errors.targetIndustries && (
              <p className="text-sm text-red-600">{errors.targetIndustries.message}</p>
            )}
          </div>
        </div>

        {/* Work Preferences */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-6">
            <MapPinIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Work Preferences</h3>
          </div>

          <div className="space-y-6">
            <div>
              <div className="flex items-center mb-4">
                <h4 className="text-md font-medium text-gray-900">Preferred Work Arrangements</h4>
                <div className="ml-2 group relative">
                  <InformationCircleIcon className="w-4 h-4 text-gray-400 cursor-help" />
                  <div className="absolute left-0 bottom-6 hidden group-hover:block w-64 p-2 bg-gray-800 text-white text-xs rounded-lg shadow-lg z-10">
                    Drag to reorder by preference: 1st = most preferred, 4th = least preferred
                  </div>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-4">
                Rank your preferences from most preferred (top) to least preferred (bottom)
              </p>

              <div className="space-y-3">
                {watchedArrangements
                  .sort((a, b) => a.preference - b.preference)
                  .map((arrangement, index) => {
                    const info = WORK_ARRANGEMENT_INFO[arrangement.type];
                    return (
                      <motion.div
                        key={arrangement.type}
                        layout
                        className="flex items-center justify-between p-4 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-semibold text-sm">
                            {arrangement.preference}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">{info.label}</p>
                            <p className="text-sm text-gray-600">{info.description}</p>
                          </div>
                        </div>
                        
                        <div className="flex flex-col space-y-1">
                          <button
                            type="button"
                            onClick={() => movePreference(index, 'up')}
                            disabled={index === 0}
                            className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <ArrowUpIcon className="w-4 h-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => movePreference(index, 'down')}
                            disabled={index === watchedArrangements.length - 1}
                            className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <ArrowDownIcon className="w-4 h-4" />
                          </button>
                        </div>
                      </motion.div>
                    );
                  })}
              </div>
            </div>

            <div>
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  {...register('workPreferences.willingToRelocate')}
                  type="checkbox"
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <div>
                  <span className="text-sm font-medium text-gray-900">
                    I'm willing to relocate for the right opportunity
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>

        {/* Salary Expectations */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-6">
            <CurrencyDollarIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Salary Expectations</h3>
          </div>

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Employment Type *
                </label>
                <select
                  {...register('salaryExpectations.employmentType')}
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="full-time">Full-time</option>
                  <option value="part-time">Part-time</option>
                  <option value="contract">Contract</option>
                  <option value="temporary">Temporary</option>
                  <option value="freelance">Freelance</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Period *
                </label>
                <select
                  {...register('salaryExpectations.period')}
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {watchedEmploymentType === 'freelance' || watchedEmploymentType === 'contract' ? (
                    <>
                      <option value="hourly">Per Hour</option>
                      <option value="daily">Per Day</option>
                      <option value="weekly">Per Week</option>
                      <option value="monthly">Per Month</option>
                    </>
                  ) : (
                    <>
                      <option value="annually">Annually</option>
                      <option value="monthly">Monthly</option>
                      <option value="fortnightly">Fortnightly</option>
                      <option value="weekly">Weekly</option>
                    </>
                  )}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Currency *
                </label>
                <select
                  {...register('salaryExpectations.currency')}
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {CURRENCIES.map((currency) => (
                    <option key={currency.code} value={currency.code}>
                      {currency.code} ({currency.symbol}) - {currency.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expected Amount *
                  <span className="text-xs text-gray-500 ml-1">
                    ({selectedCurrency?.symbol} {watchedPeriod})
                  </span>
                </label>
                <input
                  {...register('salaryExpectations.amount')}
                  type="text"
                  placeholder={`e.g., ${selectedCurrency?.symbol}${watchedPeriod === 'hourly' ? '50' : watchedPeriod === 'daily' ? '400' : watchedPeriod === 'weekly' ? '2000' : watchedPeriod === 'monthly' ? '8000' : '100000'}`}
                  className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.salaryExpectations?.amount ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
                {errors.salaryExpectations?.amount && (
                  <p className="mt-1 text-sm text-red-600">{errors.salaryExpectations.amount.message}</p>
                )}
              </div>
            </div>

            <div>
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  {...register('salaryExpectations.flexible')}
                  type="checkbox"
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <div>
                  <span className="text-sm font-medium text-gray-900">
                    I'm flexible on salary expectations
                  </span>
                  <p className="text-xs text-gray-500">
                    This indicates you're open to negotiation based on the complete package
                  </p>
                </div>
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Additional Notes (Optional)
              </label>
              <textarea
                {...register('salaryExpectations.notes')}
                rows={3}
                placeholder="Any additional context about your salary expectations, benefits preferences, or negotiation factors..."
                className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-between pt-6"
        >
          <button
            type="button"
            onClick={onPrevious}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors"
          >
            Previous
          </button>
          
          <button
            type="submit"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
          >
            Continue to Education
          </button>
        </motion.div>
      </form>
    </div>
  );
}