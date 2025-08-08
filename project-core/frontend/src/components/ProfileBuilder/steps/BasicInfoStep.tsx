import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion } from 'framer-motion';
import { 
  UserCircleIcon, 
  EnvelopeIcon, 
  PhoneIcon, 
  MapPinIcon,
  CalendarIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  LinkIcon,
  IdentificationIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types';
import MapComponent from '../../Map/MapComponent';
import apiLogger from '../../../utils/apiLogger';

// Simple debounce function
const debounce = (func: Function, delay: number) => {
  let timeoutId: number;
  return (...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(null, args), delay);
  };
};

const basicInfoSchema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  phone: z.string().min(8, 'Please enter a valid phone number'),
  address: z.object({
    streetNumber: z.string().optional(),
    streetName: z.string().min(2, 'Street name is required'),
    streetType: z.string().optional(),
    unitNumber: z.string().optional(),
    unitType: z.string().optional(),
    suburb: z.string().min(2, 'Suburb/City is required'),
    state: z.string().min(2, 'State/Province is required'),
    postcode: z.string().min(3, 'Postcode is required'),
    country: z.string().min(2, 'Country is required'),
    propertyId: z.string().optional(),
    latitude: z.number().optional(),
    longitude: z.number().optional(),
    propertyType: z.string().optional(),
    landArea: z.number().optional(),
    floorArea: z.number().optional(),
    isValidated: z.boolean().optional(),
    validationSource: z.enum(['geoscape', 'smarty_streets', 'manual']).optional(),
    confidenceScore: z.number().min(0).max(1).optional(),
    validationDate: z.string().optional(),
    isPrimary: z.boolean().optional(),
    addressType: z.enum(['residential', 'work', 'mailing', 'temporary']).optional(),
  }),
  dateOfBirth: z.string().optional(),
  countryOfBirth: z.string().min(2, 'Country of birth is required'),
  nationality: z.string().min(2, 'Nationality is required'),
  workAuthorization: z.object({
    status: z.enum(['citizen', 'permanent_resident', 'work_visa', 'student_visa', 'other']),
    visaType: z.string().optional(),
    expiryDate: z.string().optional(),
    details: z.string().optional(),
    otherType: z.string().optional(),
    seekingSponsorship: z.boolean().optional(),
  }),
  professionalLinks: z.object({
    linkedInURL: z.string().optional().or(z.literal('')),
    githubURL: z.string().optional().or(z.literal('')),
    portfolioURL: z.string().optional().or(z.literal('')),
    personalWebsite: z.string().optional().or(z.literal('')),
  }),
  socialLinks: z.object({
    twitterURL: z.string().optional().or(z.literal('')),
    instagramURL: z.string().optional().or(z.literal('')),
    facebookURL: z.string().optional().or(z.literal('')),
  }).optional(),
});

type BasicInfoFormData = z.infer<typeof basicInfoSchema>;

interface BasicInfoStepProps {
  data: ProfileData;
  updateData: (section: keyof ProfileData, data: any) => void;
  onNext: () => void;
  onPrev: () => void;
  onJumpToStep?: (stepIndex: number) => void;
  isFirstStep: boolean;
  isLastStep: boolean;
}

const BasicInfoStep: React.FC<BasicInfoStepProps> = ({ 
  data, 
  updateData, 
  onNext 
}) => {
  const [showSocialLinks, setShowSocialLinks] = useState(false);
  
  // Debug: Log the data being passed to this component
  React.useEffect(() => {
    console.log('🔍 BasicInfoStep received data:', data);
    console.log('🔍 BasicInfo data:', data.basicInfo);
  }, [data]);
  
  // Geoscape autocomplete state
  const [addressSearch, setAddressSearch] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [addressSuggestions, setAddressSuggestions] = useState<Array<{address: string, id: string, data?: any}>>([]);
  const [selectedAddress, setSelectedAddress] = useState<any>(null);
  const [addressValidation, setAddressValidation] = useState<{
    status: 'idle' | 'validating' | 'valid' | 'invalid' | 'error' | 'skipped';
    message?: string;
  }>({ status: 'idle' });
  const [isSearching, setIsSearching] = useState(false);
  const searchTimeoutRef = useRef<number | null>(null);
  
  // API usage tracking is handled on backend only

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    getValues,
    setValue
  } = useForm<BasicInfoFormData>({
    resolver: zodResolver(basicInfoSchema),
    defaultValues: {
      firstName: data.basicInfo.firstName || '',
      lastName: data.basicInfo.lastName || '',
      email: data.basicInfo.email || '',
      phone: data.basicInfo.phone || '',
      address: {
        streetNumber: data.basicInfo.address?.streetNumber || '',
        streetName: data.basicInfo.address?.streetName || '',
        streetType: data.basicInfo.address?.streetType || '',
        unitNumber: data.basicInfo.address?.unitNumber || '',
        unitType: data.basicInfo.address?.unitType || '',
        suburb: data.basicInfo.address?.suburb || '',
        state: data.basicInfo.address?.state || '',
        postcode: data.basicInfo.address?.postcode || '',
        country: data.basicInfo.address?.country || 'Australia',
        propertyId: data.basicInfo.address?.propertyId || '',
        latitude: data.basicInfo.address?.latitude || undefined,
        longitude: data.basicInfo.address?.longitude || undefined,
        propertyType: data.basicInfo.address?.propertyType || '',
        landArea: data.basicInfo.address?.landArea || undefined,
        floorArea: data.basicInfo.address?.floorArea || undefined,
        isValidated: data.basicInfo.address?.isValidated || false,
        validationSource: data.basicInfo.address?.validationSource || undefined,
        confidenceScore: data.basicInfo.address?.confidenceScore || undefined,
        validationDate: data.basicInfo.address?.validationDate || '',
        isPrimary: data.basicInfo.address?.isPrimary || true,
        addressType: data.basicInfo.address?.addressType || 'residential',
      },
      dateOfBirth: data.basicInfo.dateOfBirth || '',
      countryOfBirth: data.basicInfo.countryOfBirth || '',
      nationality: data.basicInfo.nationality || '',
      workAuthorization: {
        status: data.basicInfo.workAuthorization?.status || 'citizen',
        visaType: data.basicInfo.workAuthorization?.visaType || '',
        expiryDate: data.basicInfo.workAuthorization?.expiryDate || '',
        details: data.basicInfo.workAuthorization?.details || '',
        otherType: data.basicInfo.workAuthorization?.otherType || '',
        seekingSponsorship: data.basicInfo.workAuthorization?.seekingSponsorship || false,
      },
      professionalLinks: {
        linkedInURL: data.basicInfo.professionalLinks?.linkedInURL || '',
        githubURL: data.basicInfo.professionalLinks?.githubURL || '',
        portfolioURL: data.basicInfo.professionalLinks?.portfolioURL || '',
        personalWebsite: data.basicInfo.professionalLinks?.personalWebsite || '',
      },
      socialLinks: {
        twitterURL: data.basicInfo.socialLinks?.twitterURL || '',
        instagramURL: data.basicInfo.socialLinks?.instagramURL || '',
        facebookURL: data.basicInfo.socialLinks?.facebookURL || '',
      },
    },
    mode: 'onChange'
  });

  const watchWorkAuth = watch('workAuthorization.status');
  const watchCountry = watch('address.country');

  const onSubmit = (formData: BasicInfoFormData) => {
    console.log('💾 Saving BasicInfo data:', formData);
    updateData('basicInfo', formData);
    
    // Save to database
    saveToDatabase(formData);
    
    onNext();
  };

  const saveToDatabase = async (formData: BasicInfoFormData) => {
    try {
      // Get user session
      const userSession = localStorage.getItem('userSession');
      if (!userSession) {
        console.error('❌ No user session found for saving data');
        return;
      }
      
      const sessionData = JSON.parse(userSession);
      const userId = sessionData.userId;
      
      console.log('💾 SAVING BASIC INFO TO DATABASE:', formData);
      console.log('👤 USER ID:', userId);
      
      const response = await fetch('http://localhost:8000/api/v1/profile/save-section', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          section: 'basic_info',
          data: formData
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✅ BasicInfo data saved to database:', result);
      } else {
        console.error('❌ Failed to save BasicInfo data to database:', response.status);
        const errorText = await response.text();
        console.error('❌ Error details:', errorText);
      }
    } catch (error) {
      console.error('❌ Error saving BasicInfo data to database:', error);
    }
  };

  // Debounced address search to prevent focus issues
  const debouncedSearch = React.useCallback((query: string) => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (query.length < 3) {
      setAddressSuggestions([]);
      setShowSuggestions(false);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);

    searchTimeoutRef.current = setTimeout(async () => {
      try {
        setAddressValidation({ status: 'validating' });
        
        // API usage tracking is handled on backend for billing
        
        // Call the address search API
        const suggestions = await performAddressSearch(query);
        
        // Update the suggestions state
        setAddressSuggestions(suggestions);
        setShowSuggestions(suggestions.length > 0);
        setIsSearching(false);
      } catch (error: unknown) {
        console.error('Address search error:', error);
        setAddressSuggestions([]);
        setShowSuggestions(false);
        setAddressValidation({
          status: 'error',
          message: error instanceof Error ? error.message : 'Address lookup service is not available. Please use manual address entry below.'
        });
        setIsSearching(false);
      }
    }, 500); // 500ms debounce delay
  }, []);

  // Address autocomplete functionality
  const performAddressSearch = async (query: string) => {
    const startTime = Date.now();
    const requestData = { query, country: 'AU', limit: 5 };
    
    try {
      console.log('🔍 PERFORMING ADDRESS SEARCH:', query);
      console.log('📤 REQUEST DATA:', requestData);
      
      // Call the real backend API with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
      const response = await fetch(`http://127.0.0.1:8000/api/address/search?q=${encodeURIComponent(query)}&country=AU&limit=5`, {
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      const responseTime = Date.now() - startTime;
      
      if (!response.ok) {
        const errorData = { error: `HTTP error! status: ${response.status}` };
        console.error('❌ ADDRESS SEARCH HTTP ERROR:', response.status, response.statusText);
        apiLogger.logAPICall(
          '/api/address/search',
          'GET',
          requestData,
          errorData,
          response.status,
          responseTime,
          `HTTP error! status: ${response.status}`
        );
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ ADDRESS SEARCH RESPONSE:', data);
      console.log('📊 RESPONSE TIME:', responseTime + 'ms');
      console.log('🔢 SUGGESTIONS COUNT:', data.suggestions?.length || 0);
      
      // Log each suggestion in detail
      if (data.suggestions && data.suggestions.length > 0) {
        console.log('📋 DETAILED SUGGESTIONS:');
        data.suggestions.forEach((suggestion: any, index: number) => {
          console.log(`  ${index + 1}. ${suggestion.full_address || suggestion.address}`);
          console.log(`     Property ID: ${suggestion.property_id || 'N/A'}`);
          console.log(`     Confidence: ${suggestion.confidence_score || 'N/A'}`);
          console.log(`     Coordinates: ${suggestion.latitude || 'N/A'}, ${suggestion.longitude || 'N/A'}`);
        });
      }
      
      apiLogger.logAPICall(
        '/api/address/search',
        'GET',
        requestData,
        data,
        response.status,
        responseTime,
        'Success'
      );
      
      return data.suggestions || [];
    } catch (error: unknown) {
      const responseTime = Date.now() - startTime;
      console.error('❌ ADDRESS SEARCH ERROR:', error);
      console.error('⏱️ RESPONSE TIME:', responseTime + 'ms');
      
      apiLogger.logAPICall(
        '/api/address/search',
        'GET',
        requestData,
        { error: error instanceof Error ? error.message : 'Unknown error' },
        0,
        responseTime,
        error instanceof Error ? error.message : 'Unknown error'
      );
      
      throw error;
    }
  };

  // Clean up timeout on unmount
  React.useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  const selectAddress = React.useCallback(async (suggestion: any) => {
    console.log('🏠 ADDRESS SELECTION DEBUG:', {
      selectedAddress: suggestion.address,
      suggestionData: suggestion.data,
      propertyId: suggestion.id
    });

    setAddressSearch(suggestion.address);
    setShowSuggestions(false);
    
    try {
      // Get precise coordinates from the backend
      console.log('📍 GETTING PRECISE COORDINATES...');
      
      const requestData = {
        address: suggestion.address,
        property_id: suggestion.id,
        country: 'AU'
      };
      
      console.log('📤 COORDINATES REQUEST DATA:', requestData);
      const startTime = Date.now();
      
      const response = await fetch('http://127.0.0.1:8000/api/address/coordinates', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const responseTime = Date.now() - startTime;
      console.log('⏱️ COORDINATES API RESPONSE TIME:', responseTime + 'ms');

      if (!response.ok) {
        console.error('❌ COORDINATES API HTTP ERROR:', response.status, response.statusText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const coordinatesResult = await response.json();
      console.log('📍 COORDINATES RESULT:', coordinatesResult);
      console.log('📊 COORDINATES RESPONSE DETAILS:', {
        success: coordinatesResult.success,
        latitude: coordinatesResult.latitude,
        longitude: coordinatesResult.longitude,
        confidence_score: coordinatesResult.confidence_score,
        property_id: coordinatesResult.property_id,
        full_response: coordinatesResult
      });

      if (coordinatesResult.success && coordinatesResult.latitude && coordinatesResult.longitude) {
        // Use precise coordinates from the API
        const preciseLat = parseFloat(coordinatesResult.latitude.toFixed(15));
        const preciseLng = parseFloat(coordinatesResult.longitude.toFixed(15));
        
        console.log('✅ PRECISE COORDINATES:', { lat: preciseLat, lng: preciseLng });
        
        const addressData = {
          ...suggestion.data,
          latitude: preciseLat,
          longitude: preciseLng
        };
        
        setSelectedAddress(addressData);
        
        // Auto-populate form fields with precise coordinates
        if (suggestion.data) {
          console.log('📋 POPULATING FORM FIELDS WITH PRECISE COORDINATES:');
          
          const fieldMappings = [
            { field: 'address.streetNumber', value: suggestion.data.streetNumber || '' },
            { field: 'address.streetName', value: suggestion.data.streetName || '' },
            { field: 'address.streetType', value: suggestion.data.streetType || '' },
            { field: 'address.suburb', value: suggestion.data.suburb || '' },
            { field: 'address.state', value: suggestion.data.state || '' },
            { field: 'address.postcode', value: suggestion.data.postcode || '' },
            { field: 'address.latitude', value: preciseLat },
            { field: 'address.longitude', value: preciseLng },
            { field: 'address.isValidated', value: true },
            { field: 'address.validationSource', value: 'geoscape' },
            { field: 'address.confidenceScore', value: coordinatesResult.confidence_score || 0.95 },
            { field: 'address.validationDate', value: new Date().toISOString() },
            { field: 'address.propertyId', value: suggestion.id }
          ];

          fieldMappings.forEach(({ field, value }) => {
            console.log(`setValue('${field}', ${JSON.stringify(value)})`);
            setValue(field as any, value);
          });
        }
        
        setAddressValidation({
          status: 'valid',
          message: 'Address validated with Geoscape'
        });
        
      } else {
        // Don't use fallback coordinates - let the map component handle missing coordinates
        console.warn('⚠️ COORDINATES API FAILED - NO FALLBACK COORDINATES');
        console.warn('❌ COORDINATES API RESPONSE ISSUES:', {
          success: coordinatesResult.success,
          hasLatitude: !!coordinatesResult.latitude,
          hasLongitude: !!coordinatesResult.longitude,
          latitude: coordinatesResult.latitude,
          longitude: coordinatesResult.longitude
        });
        
        setAddressValidation({
          status: 'error',
          message: 'Could not get precise coordinates for this address'
        });
      }
      
    } catch (error: unknown) {
      console.error('❌ ERROR GETTING COORDINATES:', error);
      console.error('⏱️ COORDINATES API ERROR TIME:', Date.now());
      
      // Don't use fallback coordinates on error
      console.warn('⚠️ COORDINATES API ERROR - NO FALLBACK COORDINATES');
      
      setAddressValidation({
        status: 'error',
        message: 'Could not get coordinates for this address'
      });
    }
  }, [setValue, watch, getValues]); // Added watch and getValues dependencies

  // Usage tracking removed from frontend - handled on backend

  // Click outside handler to close suggestions
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Element;
      if (!target.closest('.address-search-container')) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

    // Address validation function - kept for future implementation
  // const validateAddress = async () => {
  //   // Implementation would go here
  // };

  // Comprehensive country list - in production, this should come from API
  const countries = [
    'Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria',
    'Cambodia', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 'Czech Republic',
    'Denmark', 'Ecuador', 'Egypt', 'Estonia', 'Ethiopia', 'Finland', 'France',
    'Georgia', 'Germany', 'Ghana', 'Greece', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
    'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg',
    'Malaysia', 'Mexico', 'Morocco', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway',
    'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
    'Saudi Arabia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland',
    'Taiwan', 'Thailand', 'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela', 'Vietnam',
    'Other'
  ];

  const workAuthOptions = [
    { value: 'citizen', label: 'Citizen', description: 'Citizen of this country' },
    { value: 'permanent_resident', label: 'Permanent Resident', description: 'Permanent residency or equivalent' },
    { value: 'work_visa', label: 'Work Visa', description: 'Temporary work authorization' },
    { value: 'student_visa', label: 'Student Visa', description: 'Student with work rights' },
    { value: 'other', label: 'Other', description: 'Other work authorization' },
  ];

  const australianVisaTypes = [
    'Temporary Skill Shortage (TSS) - Subclass 482',
    'Skilled Independent - Subclass 189',
    'Skilled Nominated - Subclass 190', 
    'Working Holiday - Subclass 417',
    'Work and Holiday - Subclass 462',
    'Employer Nomination Scheme - Subclass 186',
    'Regional Sponsored Migration - Subclass 187',
    'Business Innovation and Investment - Subclass 188',
    'Distinguished Talent - Subclass 858',
    'Student Visa - Subclass 500',
    'Other'
  ];

  // Auto-save functionality
  const autoSave = useCallback(async (formData: BasicInfoFormData) => {
    try {
      console.log('💾 Auto-saving BasicInfo data:', formData);
      
      const userSession = localStorage.getItem('userSession');
      if (!userSession) {
        console.error('❌ No user session found for auto-save');
        return;
      }
      
      const sessionData = JSON.parse(userSession);
      const userId = sessionData.userId;
      
      console.log('👤 AUTO-SAVE USER ID:', userId);
      
      const response = await fetch('http://localhost:8000/api/v1/profile/save-section', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          section: 'basic_info',
          data: formData
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✅ Auto-save successful:', result);
      } else {
        console.error('❌ Auto-save failed:', response.status);
        const errorText = await response.text();
        console.error('❌ Auto-save error details:', errorText);
      }
    } catch (error) {
      console.error('❌ Auto-save error:', error);
    }
  }, []);

  // Debounced auto-save
  const debouncedAutoSave = useCallback(
    debounce((formData: BasicInfoFormData) => {
      autoSave(formData);
    }, 1000), // 1 second delay
    [autoSave]
  );

  // Watch for form changes and auto-save
  useEffect(() => {
    const subscription = watch((formData) => {
      if (formData && Object.keys(formData).length > 0) {
        debouncedAutoSave(formData as BasicInfoFormData);
      }
    });
    
    return () => subscription.unsubscribe();
  }, [watch, debouncedAutoSave]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Basic Information
        </h2>
        <p className="text-gray-600">
          Let's start with your personal details. All information is securely stored and used only for your profile.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Personal Details */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-4">
            <UserCircleIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Personal Details</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Name *
              </label>
              <input
                {...register('firstName')}
                type="text"
                placeholder="Enter your first name"
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.firstName ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.firstName && (
                <p className="mt-1 text-sm text-red-600">{errors.firstName.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Last Name *
              </label>
              <input
                {...register('lastName')}
                type="text"
                placeholder="Enter your last name"
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.lastName ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.lastName && (
                <p className="mt-1 text-sm text-red-600">{errors.lastName.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('email')}
                  type="email"
                  placeholder="your.email@example.com"
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.email ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone Number *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <PhoneIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('phone')}
                  type="tel"
                  placeholder="+61 4XX XXX XXX"
                  className={`block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.phone ? 'border-red-300 bg-red-50' : 'border-gray-300'
                  }`}
                />
              </div>
              {errors.phone && (
                <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date of Birth
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <CalendarIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('dateOfBirth')}
                  type="date"
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Address Information - Geoscape Style */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <MapPinIcon className="w-5 h-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Address Information</h3>
            </div>
            <div className="text-xs text-gray-500">
              Powered by <span className="font-semibold text-blue-600">Geoscape</span>
            </div>
          </div>

          {/* Address Search - Geoscape Style */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Address Search
            </label>
            <div className="relative address-search-container">
              <input
                type="text"
                placeholder="Start typing to get auto-complete suggestions from the API"
                className="block w-full px-4 py-3 pr-10 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={addressSearch}
                onChange={(e) => {
                  const value = e.target.value;
                  setAddressSearch(value);
                  debouncedSearch(value);
                }}
                onFocus={() => setShowSuggestions(true)}
              />
              {(addressValidation.status === 'validating' || isSearching) && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                </div>
              )}
              
              {/* Address Suggestions Dropdown */}
              {showSuggestions && addressSuggestions.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                  {addressSuggestions.map((suggestion, index) => (
                    <div
                      key={index}
                      className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                      onClick={() => selectAddress(suggestion)}
                    >
                      <div className="font-medium text-gray-900">{suggestion.address}</div>
                      <div className="text-sm text-gray-500">{suggestion.id}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Usage tracking is now backend-only for billing management */}

          {/* Map Integration */}
          {selectedAddress && selectedAddress.latitude && selectedAddress.longitude && (
            <div className="mb-6">
              <MapComponent
                latitude={selectedAddress.latitude}
                longitude={selectedAddress.longitude}
                address={addressSearch}
                className="w-full h-64 rounded-lg border border-gray-300"
              />
            </div>
          )}
          
          {/* Validation Status - IMPROVED */}
          {addressValidation.status !== 'idle' && addressValidation.status !== 'skipped' && (
            <div className={`mb-6 p-3 rounded-lg flex items-center ${
              addressValidation.status === 'valid' ? 'bg-green-50 text-green-800' :
              addressValidation.status === 'invalid' || addressValidation.status === 'error' ? 'bg-red-50 text-red-800' :
              'bg-blue-50 text-blue-800'
            }`}>
              {addressValidation.status === 'valid' ? (
                <CheckCircleIcon className="w-4 h-4 mr-2" />
              ) : addressValidation.status === 'invalid' || addressValidation.status === 'error' ? (
                <ExclamationTriangleIcon className="w-4 h-4 mr-2" />
              ) : (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              )}
              <span className="text-sm">{addressValidation.message}</span>
            </div>
          )}

          {/* Skip Address Validation Option - CONDITIONAL */}
          {!selectedAddress && addressValidation.status === 'idle' && !watch('address.streetName') && (
            <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 mr-2" />
                  <div>
                    <h4 className="text-sm font-medium text-yellow-800">Address Validation</h4>
                    <p className="text-xs text-yellow-700 mt-1">
                      Address validation helps ensure accurate location data. You can skip this step and enter your address manually below.
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setAddressValidation({
                      status: 'skipped',
                      message: 'Address validation skipped - you can enter address manually below'
                    });
                    setShowSuggestions(false);
                    setAddressSuggestions([]);
                  }}
                  className="px-4 py-2 text-sm font-medium text-yellow-800 bg-yellow-100 border border-yellow-300 rounded-md hover:bg-yellow-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2"
                >
                  Skip Validation
                </button>
              </div>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Street Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Number
              </label>
              <input
                {...register('address.streetNumber')}
                type="text"
                placeholder="123"
                className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Street Name */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Name *
              </label>
              <input
                {...register('address.streetName')}
                type="text"
                placeholder="Main Street"
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address?.streetName ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.address?.streetName && (
                <p className="mt-1 text-sm text-red-600">{errors.address.streetName.message}</p>
              )}
            </div>

            {/* Street Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Type
              </label>
              <select
                {...register('address.streetType')}
                className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select type</option>
                <option value="Street">Street</option>
                <option value="Road">Road</option>
                <option value="Avenue">Avenue</option>
                <option value="Drive">Drive</option>
                <option value="Lane">Lane</option>
                <option value="Court">Court</option>
                <option value="CCT">Court (CCT)</option>
                <option value="Place">Place</option>
                <option value="Crescent">Crescent</option>
                <option value="Boulevard">Boulevard</option>
                <option value="Way">Way</option>
                <option value="Close">Close</option>
                <option value="Terrace">Terrace</option>
                <option value="Parade">Parade</option>
                <option value="ST">Street (ST)</option>
                <option value="RD">Road (RD)</option>
                <option value="AVE">Avenue (AVE)</option>
                <option value="DR">Drive (DR)</option>
                <option value="LN">Lane (LN)</option>
                <option value="PL">Place (PL)</option>
                <option value="CRES">Crescent (CRES)</option>
                <option value="BLVD">Boulevard (BLVD)</option>
                <option value="CL">Close (CL)</option>
                <option value="TCE">Terrace (TCE)</option>
                <option value="PDE">Parade (PDE)</option>
              </select>
            </div>

            {/* Unit Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Unit Number
              </label>
              <input
                {...register('address.unitNumber')}
                type="text"
                placeholder="4B"
                className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Unit Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Unit Type
              </label>
              <select
                {...register('address.unitType')}
                className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select type</option>
                <option value="Unit">Unit</option>
                <option value="Apartment">Apartment</option>
                <option value="Suite">Suite</option>
                <option value="Floor">Floor</option>
                <option value="Level">Level</option>
                <option value="Room">Room</option>
                <option value="Shop">Shop</option>
                <option value="Office">Office</option>
              </select>
            </div>

            {/* Suburb */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Suburb/City *
              </label>
              <input
                {...register('address.suburb')}
                type="text"
                placeholder="Sydney"
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address?.suburb ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.address?.suburb && (
                <p className="mt-1 text-sm text-red-600">{errors.address.suburb.message}</p>
              )}
            </div>

            {/* State */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {watchCountry === 'Australia' ? 'State' : watchCountry === 'United States' ? 'State' : 'Province/State'} *
              </label>
              <input
                {...register('address.state')}
                type="text"
                placeholder={watchCountry === 'Australia' ? 'NSW' : watchCountry === 'United States' ? 'CA' : 'Province/State'}
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address?.state ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.address?.state && (
                <p className="mt-1 text-sm text-red-600">{errors.address.state.message}</p>
              )}
            </div>

            {/* Postcode */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {watchCountry === 'Australia' ? 'Postcode' : watchCountry === 'United States' ? 'ZIP Code' : 'Postal Code'} *
              </label>
              <input
                {...register('address.postcode')}
                type="text"
                placeholder={watchCountry === 'Australia' ? '2000' : watchCountry === 'United States' ? '10001' : 'Postal Code'}
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address?.postcode ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.address?.postcode && (
                <p className="mt-1 text-sm text-red-600">{errors.address.postcode.message}</p>
              )}
            </div>

            {/* Country */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Country *
              </label>
              <select
                {...register('address.country')}
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address?.country ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              >
                {countries.map((country) => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              {errors.address?.country && (
                <p className="mt-1 text-sm text-red-600">{errors.address.country.message}</p>
              )}
            </div>
          </div>

          {/* Address Validation Status - IMPROVED */}
          {watch('address.isValidated') && watch('address.validationSource') && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center">
                <CheckCircleIcon className="w-5 h-5 text-green-600 mr-2" />
                <div>
                  <h4 className="text-sm font-medium text-green-900">Address Validated</h4>
                  <p className="text-sm text-green-700">
                    Validated via {watch('address.validationSource')} with {Math.round((watch('address.confidenceScore') || 0) * 100)}% confidence
                  </p>
                  {watch('address.propertyId') && (
                    <p className="text-xs text-green-600 mt-1">
                      Property ID: {watch('address.propertyId')}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Nationality & Birth Information */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-4">
            <GlobeAltIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Nationality & Birth Information</h3>
          </div>
          
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="w-5 h-5 text-blue-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h4 className="text-sm font-medium text-blue-900">Help with these fields:</h4>
                <div className="mt-1 text-sm text-blue-700">
                  <p><strong>Country of Birth:</strong> Where you were physically born (e.g., "South Africa")</p>
                  <p><strong>Current Citizenship:</strong> Which passport(s) you currently hold (e.g., "Australia")</p>
                  <p className="mt-1 italic">Example: Born in Durban, South Africa → Birth: "South Africa", Citizenship: "Australia"</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Country of Birth *
                <span className="text-xs text-gray-500 ml-1">(Where you were born)</span>
              </label>
              <select
                {...register('countryOfBirth')}
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.countryOfBirth ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              >
                <option value="">Select country where you were born</option>
                {countries.map((country) => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              {errors.countryOfBirth && (
                <p className="mt-1 text-sm text-red-600">{errors.countryOfBirth.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Citizenship *
                <span className="text-xs text-gray-500 ml-1">(Passport you hold)</span>
              </label>
              <select
                {...register('nationality')}
                className={`block w-full px-4 py-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.nationality ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              >
                <option value="">Select your current citizenship</option>
                {countries.map((country) => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              {errors.nationality && (
                <p className="mt-1 text-sm text-red-600">{errors.nationality.message}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                If you have multiple citizenships, select your primary one
              </p>
            </div>
          </div>
        </div>

        {/* Work Authorization */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center mb-4">
            <ShieldCheckIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Work Authorization</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Work Authorization Status *
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {workAuthOptions.map((option) => (
                  <label key={option.value} className="relative flex cursor-pointer">
                    <input
                      {...register('workAuthorization.status')}
                      type="radio"
                      value={option.value}
                      className="sr-only"
                    />
                    <div className={`flex-1 p-4 border-2 rounded-lg transition-all duration-200 ${
                      watchWorkAuth === option.value 
                        ? 'border-blue-500 bg-blue-50' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}>
                      <div className="flex items-center">
                        <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                          watchWorkAuth === option.value
                            ? 'border-blue-500 bg-blue-500'
                            : 'border-gray-300'
                        }`}>
                          {watchWorkAuth === option.value && (
                            <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>
                          )}
                        </div>
                        <div>
                          <div className={`font-medium ${
                            watchWorkAuth === option.value ? 'text-blue-900' : 'text-gray-900'
                          }`}>
                            {option.label}
                          </div>
                          <div className={`text-xs ${
                            watchWorkAuth === option.value ? 'text-blue-700' : 'text-gray-500'
                          }`}>
                            {option.description}
                          </div>
                        </div>
                      </div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {(watchWorkAuth === 'work_visa' || watchWorkAuth === 'student_visa' || watchWorkAuth === 'other') && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.3 }}
                className="space-y-4"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {watchWorkAuth === 'work_visa' ? 'Visa Type' : 
                       watchWorkAuth === 'student_visa' ? 'Student Visa Type' : 'Authorization Type'}
                    </label>
                    {watchWorkAuth === 'work_visa' && watchCountry === 'Australia' ? (
                      <select
                        {...register('workAuthorization.visaType')}
                        className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">Select visa type</option>
                        {australianVisaTypes.map((visa) => (
                          <option key={visa} value={visa}>{visa}</option>
                        ))}
                      </select>
                    ) : watchWorkAuth === 'other' ? (
                      <input
                        {...register('workAuthorization.otherType')}
                        type="text"
                        placeholder="Please specify your work authorization type"
                        className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    ) : (
                      <input
                        {...register('workAuthorization.visaType')}
                        type="text"
                        placeholder="e.g., H1-B, TSS 482, Student Visa"
                        className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Expiry Date
                    </label>
                    <input
                      {...register('workAuthorization.expiryDate')}
                      type="date"
                      className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Additional Details (Optional)
                    </label>
                    <textarea
                      {...register('workAuthorization.details')}
                      rows={2}
                      placeholder="Any additional information about your work authorization..."
                      className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    />
                  </div>
                </div>
              </motion.div>
            )}

            {/* Sponsorship Question - Show for non-citizens */}
            {(watchWorkAuth === 'work_visa' || watchWorkAuth === 'student_visa' || watchWorkAuth === 'other') && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.3, delay: 0.1 }}
                className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg"
              >
                <label className="flex items-start space-x-3 cursor-pointer">
                  <input
                    {...register('workAuthorization.seekingSponsorship')}
                    type="checkbox"
                    className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <div>
                    <div className="text-sm font-medium text-amber-900">
                      I am seeking work sponsorship
                    </div>
                    <div className="text-xs text-amber-700 mt-1">
                      Check this if you need an employer to sponsor your work authorization or visa extension
                    </div>
                  </div>
                </label>
              </motion.div>
            )}
          </div>
        </div>

        {/* Professional Links & Social Media */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <LinkIcon className="w-5 h-5 text-blue-600 mr-2" />
              <h3 className="text-lg font-semibold text-gray-900">Professional Links & Social Media</h3>
            </div>
            <span className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full font-medium">
              Optional Section
            </span>
          </div>
          
          <p className="text-sm text-gray-600 mb-6">
            Add your professional profiles and social media accounts. These help employers understand your professional presence and networking approach. 
            <span className="font-medium text-blue-600"> All fields are completely optional - you can skip any or all of these if you prefer.</span>
          </p>

          {/* Core Professional Links */}
          <div className="mb-6">
            <h4 className="text-md font-medium text-gray-900 mb-3">Core Professional Profiles</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  LinkedIn Profile
                  <span className="text-xs text-gray-500 ml-1">(Highly recommended)</span>
                </label>
                <input
                  {...register('professionalLinks.linkedInURL')}
                  type="url"
                  placeholder="https://linkedin.com/in/yourprofile"
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {errors.professionalLinks?.linkedInURL && (
                  <p className="mt-1 text-sm text-red-600">{errors.professionalLinks.linkedInURL.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Portfolio Website
                  <span className="text-xs text-gray-500 ml-1">(For creative professionals)</span>
                </label>
                <input
                  {...register('professionalLinks.portfolioURL')}
                  type="url"
                  placeholder="https://yourportfolio.com"
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {errors.professionalLinks?.portfolioURL && (
                  <p className="mt-1 text-sm text-red-600">{errors.professionalLinks.portfolioURL.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  GitHub Profile
                  <span className="text-xs text-gray-500 ml-1">(For developers)</span>
                </label>
                <input
                  {...register('professionalLinks.githubURL')}
                  type="url"
                  placeholder="https://github.com/yourusername"
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {errors.professionalLinks?.githubURL && (
                  <p className="mt-1 text-sm text-red-600">{errors.professionalLinks.githubURL.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Personal Website
                  <span className="text-xs text-gray-500 ml-1">(Professional blog, etc.)</span>
                </label>
                <input
                  {...register('professionalLinks.personalWebsite')}
                  type="url"
                  placeholder="https://yourwebsite.com"
                  className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {errors.professionalLinks?.personalWebsite && (
                  <p className="mt-1 text-sm text-red-600">{errors.professionalLinks.personalWebsite.message}</p>
                )}
              </div>
            </div>
          </div>

          {/* Professional Social Media */}
          <div className="pt-6 border-t">
            <button
              type="button"
              onClick={() => setShowSocialLinks(!showSocialLinks)}
              className="flex items-center text-sm text-blue-600 hover:text-blue-700 mb-4"
            >
              <span>Professional Social Media Profiles (Optional)</span>
              <motion.div
                animate={{ rotate: showSocialLinks ? 180 : 0 }}
                transition={{ duration: 0.2 }}
                className="ml-2"
              >
                ↓
              </motion.div>
            </button>

            <p className="text-xs text-gray-500 mb-4">
              Many professionals use social media for networking, thought leadership, and industry engagement. 
              Only include profiles that represent your professional brand.
              <span className="font-medium text-blue-600"> You can leave all social media fields empty if you prefer not to share these.</span>
            </p>

            {showSocialLinks && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ duration: 0.3 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-4"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Twitter/X
                    <span className="text-xs text-gray-500 ml-1">(Professional networking)</span>
                  </label>
                  <input
                    {...register('socialLinks.twitterURL')}
                    type="url"
                    placeholder="https://twitter.com/yourusername"
                    className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Instagram
                    <span className="text-xs text-gray-500 ml-1">(Visual portfolio, brand)</span>
                  </label>
                  <input
                    {...register('socialLinks.instagramURL')}
                    type="url"
                    placeholder="https://instagram.com/yourusername"
                    className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Facebook
                    <span className="text-xs text-gray-500 ml-1">(Professional page)</span>
                  </label>
                  <input
                    {...register('socialLinks.facebookURL')}
                    type="url"
                    placeholder="https://facebook.com/yourprofessionalpage"
                    className="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Submit Button */}
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
            <span>Continue to Career Goals</span>
            <IdentificationIcon className="w-5 h-5" />
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
};

export default BasicInfoStep;