import React, { useState, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion } from 'framer-motion';
import { 
  UserIcon, 
  EnvelopeIcon, 
  PhoneIcon, 
  MapPinIcon,
  CalendarIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  LinkIcon,
  BuildingOffice2Icon,
  IdentificationIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import type { ProfileData } from '../types.ts';
import MapComponent from '../../Map/MapComponent.tsx';

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
    linkedInURL: z.string().url('Please enter a valid LinkedIn URL').optional().or(z.literal('')),
    githubURL: z.string().url('Please enter a valid GitHub URL').optional().or(z.literal('')),
    portfolioURL: z.string().url('Please enter a valid portfolio URL').optional().or(z.literal('')),
    personalWebsite: z.string().url('Please enter a valid website URL').optional().or(z.literal('')),
  }),
  socialLinks: z.object({
    twitterURL: z.string().url('Please enter a valid Twitter URL').optional().or(z.literal('')),
    instagramURL: z.string().url('Please enter a valid Instagram URL').optional().or(z.literal('')),
    facebookURL: z.string().url('Please enter a valid Facebook URL').optional().or(z.literal('')),
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
  
  // Geoscape autocomplete state
  const [addressSearch, setAddressSearch] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [addressSuggestions, setAddressSuggestions] = useState<Array<{address: string, id: string, data?: any}>>([]);
  const [selectedAddress, setSelectedAddress] = useState<any>(null);
  const [addressValidation, setAddressValidation] = useState<{
    status: 'idle' | 'validating' | 'valid' | 'invalid';
    message?: string;
  }>({ status: 'idle' });
  const [isSearching, setIsSearching] = useState(false);
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  // API usage tracking is handled on backend only

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
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
    updateData('basicInfo', formData);
    onNext();
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
        
        // Simulate Geoscape autocomplete API call
        await new Promise(resolve => setTimeout(resolve, 300));
        
        await performAddressSearch(query);
        setIsSearching(false);
      } catch (error) {
        setAddressValidation({
          status: 'invalid',
          message: 'Address search failed. Please try again.'
        });
        setIsSearching(false);
      }
    }, 500); // 500ms debounce delay
  }, []);

  // Address autocomplete functionality
  const performAddressSearch = async (query: string) => {
      
      // Enhanced address parsing for full address format
      const parseAddressQuery = (query: string) => {
        console.log('🔍 PARSING QUERY:', query);
        
        // Handle full address format: "4 Milburn Place, St Ives Chase NSW 2075"
        if (query.includes(',')) {
          const [streetPart, locationPart] = query.split(',').map(part => part.trim());
          console.log('📋 SPLIT ADDRESS:', { streetPart, locationPart });
          
          // Parse street part: "4 Milburn Place"
          const streetParts = streetPart.split(' ');
          const streetNumber = streetParts[0] && /^\d+/.test(streetParts[0]) ? streetParts[0] : '';
          
          // Remove number and find street name/type
          const remainingStreet = streetNumber ? streetParts.slice(1) : streetParts;
          const streetTypes = ['PL', 'PLACE', 'ST', 'STREET', 'RD', 'ROAD', 'AVE', 'AVENUE', 'DR', 'DRIVE'];
          
          let streetType = '';
          let streetName = '';
          
          if (remainingStreet.length > 0) {
            const lastWord = remainingStreet[remainingStreet.length - 1].toUpperCase();
            console.log('🔍 CHECKING LAST WORD:', lastWord);
            console.log('🔍 AVAILABLE STREET TYPES:', streetTypes);
            
            if (streetTypes.includes(lastWord)) {
              streetType = lastWord === 'PL' ? 'PLACE' : lastWord;
              streetName = remainingStreet.slice(0, -1).join(' ').toUpperCase();
              console.log('✅ FOUND STREET TYPE:', streetType);
              console.log('✅ EXTRACTED STREET NAME:', streetName);
            } else {
              streetName = remainingStreet.join(' ').toUpperCase();
              console.log('⚠️ NO STREET TYPE FOUND, USING FULL NAME:', streetName);
            }
          }
          
          const result = { streetNumber, streetName, streetType };
          console.log('✅ PARSED FULL ADDRESS:', result);
          return result;
        }
        
        // Handle simple format: "4 Milburn Place"
        const parts = query.trim().split(' ');
        const streetNumber = parts[0] && /^\d+/.test(parts[0]) ? parts[0] : '';
        
        // Remove number if it exists, then find street type
        const remaining = streetNumber ? parts.slice(1) : parts;
        const streetTypes = ['PL', 'PLACE', 'ST', 'STREET', 'RD', 'ROAD', 'AVE', 'AVENUE', 'DR', 'DRIVE'];
        
        let streetType = '';
        let streetName = '';
        
        // Look for street type at the end
        if (remaining.length > 0) {
          const lastWord = remaining[remaining.length - 1].toUpperCase();
          console.log('🔍 SIMPLE FORMAT - CHECKING LAST WORD:', lastWord);
          console.log('🔍 SIMPLE FORMAT - AVAILABLE STREET TYPES:', streetTypes);
          
          if (streetTypes.includes(lastWord)) {
            streetType = lastWord === 'PL' ? 'PLACE' : lastWord;
            streetName = remaining.slice(0, -1).join(' ').toUpperCase();
            console.log('✅ SIMPLE FORMAT - FOUND STREET TYPE:', streetType);
            console.log('✅ SIMPLE FORMAT - EXTRACTED STREET NAME:', streetName);
          } else {
            streetName = remaining.join(' ').toUpperCase();
            console.log('⚠️ SIMPLE FORMAT - NO STREET TYPE FOUND, USING FULL NAME:', streetName);
          }
        }
        
        const result = { streetNumber, streetName, streetType };
        console.log('✅ PARSED SIMPLE ADDRESS:', result);
        return result;
      };

      // Mock suggestions with proper address parsing and intelligent filtering
      const { streetNumber, streetName, streetType } = parseAddressQuery(query);
      
      console.log('🔍 ADDRESS PARSING DEBUG:', {
        originalQuery: query,
        parsedComponents: { streetNumber, streetName, streetType }
      });

      // Detect location context from query
      const queryLower = query.toLowerCase();
      const hasSuburbContext = queryLower.includes('st ives') || queryLower.includes('chase');
      const hasStateContext = queryLower.includes('nsw') || queryLower.includes('vic') || queryLower.includes('tas');
      const hasPostcodeContext = queryLower.includes('2075') || queryLower.includes('3064') || queryLower.includes('7010');
      
      console.log('🎯 LOCATION CONTEXT DETECTION:', {
        hasSuburbContext,
        hasStateContext, 
        hasPostcodeContext,
        shouldFilter: hasSuburbContext || hasStateContext || hasPostcodeContext
      });

      // All possible addresses
      const allAddresses = [
        {
          address: `${streetNumber || '4'} MILBURN PLACE, CRAIGIEBURN VIC 3064`,
          id: "G4VIC4242188",
          data: {
            streetNumber: streetNumber || '4',
            streetName: streetName || 'MILBURN',
            streetType: streetType || 'PLACE',
            suburb: 'CRAIGIEBURN',
            state: 'VIC',
            postcode: '3064',
            latitude: -37.5850,
            longitude: 144.9400
          },
          matchScore: 0.95
        },
        {
          address: `${streetNumber || '4'} MILBURN PLACE, GLENORCHY TAS 7010`,
          id: "GTAS7010189",
          data: {
            streetNumber: streetNumber || '4',
            streetName: streetName || 'MILBURN',
            streetType: streetType || 'PLACE',
            suburb: 'GLENORCHY',
            state: 'TAS',
            postcode: '7010',
            latitude: -42.8280,
            longitude: 147.2610
          },
          matchScore: 0.90
        },
        {
          address: `${streetNumber || '4'} MILBURN PLACE, ST IVES CHASE NSW 2075`,
          id: streetNumber === '14' ? "GNSW2075191" : "GNSW2075190",
          data: {
            streetNumber: streetNumber || '4',
            streetName: streetName || 'MILBURN',
            streetType: streetType || 'PLACE',
            suburb: 'ST IVES CHASE',
            state: 'NSW',
            postcode: '2075',
            // More realistic coordinates for St Ives Chase area
            latitude: streetNumber === '14' ? -33.7238 : -33.7235,
            longitude: streetNumber === '14' ? 151.1482 : 151.1478
          },
          matchScore: 0.98
        }
      ];

      // Smart filtering based on context
      let filteredAddresses = allAddresses;

      if (hasSuburbContext || hasStateContext || hasPostcodeContext) {
        console.log('🔍 APPLYING INTELLIGENT FILTERING...');
        
        filteredAddresses = allAddresses.filter(addr => {
          let matches = false;
          
          // Check suburb match
          if (hasSuburbContext) {
            const suburbMatch = queryLower.includes('st ives') && addr.data.suburb.toLowerCase().includes('st ives');
            matches = matches || suburbMatch;
            console.log(`   ${addr.data.suburb}: suburb match = ${suburbMatch}`);
          }
          
          // Check state match  
          if (hasStateContext) {
            const stateMatch = (queryLower.includes('nsw') && addr.data.state === 'NSW') ||
                              (queryLower.includes('vic') && addr.data.state === 'VIC') ||
                              (queryLower.includes('tas') && addr.data.state === 'TAS');
            matches = matches || stateMatch;
            console.log(`   ${addr.data.state}: state match = ${stateMatch}`);
          }
          
          // Check postcode match
          if (hasPostcodeContext) {
            const postcodeMatch = queryLower.includes(addr.data.postcode.toLowerCase());
            matches = matches || postcodeMatch;
            console.log(`   ${addr.data.postcode}: postcode match = ${postcodeMatch}`);
          }
          
          // If no context provided, show all (early typing)
          if (!hasSuburbContext && !hasStateContext && !hasPostcodeContext) {
            matches = true;
          }
          
          console.log(`   🎯 ${addr.data.suburb} ${addr.data.state}: final match = ${matches}`);
          return matches;
        });
        
        console.log(`📊 FILTERED: ${allAddresses.length} → ${filteredAddresses.length} addresses`);
      }

      // Sort by match score (highest first)
      filteredAddresses.sort((a, b) => b.matchScore - a.matchScore);

      // Convert to the expected format
      const mockSuggestions = filteredAddresses.map(addr => ({
        address: addr.address,
        id: addr.id,
        data: addr.data
      }));

      console.log('📦 FINAL SUGGESTIONS (after filtering):', mockSuggestions);

      setAddressSuggestions(mockSuggestions);
      setShowSuggestions(true);
      setAddressValidation({ status: 'idle' });
  };

  // Clean up timeout on unmount
  React.useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  const selectAddress = React.useCallback((suggestion: any) => {
    console.log('🏠 ADDRESS SELECTION DEBUG:', {
      selectedAddress: suggestion.address,
      suggestionData: suggestion.data,
      propertyId: suggestion.id
    });

    setAddressSearch(suggestion.address);
    setShowSuggestions(false);
    setSelectedAddress(suggestion.data);
    
    // Auto-populate form fields with detailed logging
    if (suggestion.data) {
      console.log('📋 POPULATING FORM FIELDS:');
      
      const fieldMappings = [
        { field: 'address.streetNumber', value: suggestion.data.streetNumber || '' },
        { field: 'address.streetName', value: suggestion.data.streetName || '' },
        { field: 'address.streetType', value: suggestion.data.streetType || '' },
        { field: 'address.suburb', value: suggestion.data.suburb || '' },
        { field: 'address.state', value: suggestion.data.state || '' },
        { field: 'address.postcode', value: suggestion.data.postcode || '' },
        { field: 'address.latitude', value: suggestion.data.latitude || undefined },
        { field: 'address.longitude', value: suggestion.data.longitude || undefined },
        { field: 'address.isValidated', value: true },
        { field: 'address.validationSource', value: 'geoscape' },
        { field: 'address.confidenceScore', value: 0.95 },
        { field: 'address.validationDate', value: new Date().toISOString() },
        { field: 'address.propertyId', value: suggestion.id }
      ];

      fieldMappings.forEach(({ field, value }) => {
        console.log(`setValue('${field}', ${JSON.stringify(value)})`);
        setValue(field as any, value);
      });

      // Special attention to streetType
      console.log('🚨 STREET TYPE SPECIFIC DEBUG:', {
        originalValue: suggestion.data.streetType,
        afterSetValue: watch('address.streetType'),
        formState: getValues('address.streetType')
      });
      
      // Force a small delay to check if value persists
      setTimeout(() => {
        const currentStreetType = getValues('address.streetType');
        console.log('🔍 STREET TYPE AFTER DELAY:', currentStreetType);
        if (!currentStreetType) {
          console.error('❌ STREET TYPE LOST AFTER DELAY!');
        }
      }, 100);
    }

    setAddressValidation({
      status: 'valid',
      message: 'Address selected and validated'
    });
  }, [setValue, watch, getValues]); // Added watch and getValues dependencies

  // Usage tracking removed from frontend - handled on backend

  // Handle address search input changes
  const handleAddressSearchChange = (value: string) => {
    setAddressSearch(value);
    debouncedSearch(value);
  };

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

  const validateAddress = async () => {
    const address = watch('address');
    if (!address.streetName || !address.suburb || !address.country) {
      setAddressValidation({
        status: 'invalid',
        message: 'Please enter street name, suburb, and country to validate address.'
      });
      return;
    }

    setAddressValidation({ status: 'validating' });
    
    try {
      // Simulate Geoscape API call (in real app, call actual API)
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock Geoscape API response
      const mockGeoscapeResponse = {
        valid: Math.random() > 0.2, // 80% success rate for demo
        confidence_score: Math.random() * 0.4 + 0.6, // 0.6 to 1.0
        suggestions: [],
        street_number: address.streetNumber || '123',
        street_name: address.streetName,
        street_type: address.streetType || 'Street',
        suburb: address.suburb,
        state: address.state,
        postcode: address.postcode,
        country: address.country,
        property_id: `PROP_${Math.random().toString(36).substr(2, 9)}`,
        latitude: -33.8688 + (Math.random() - 0.5) * 0.1, // Sydney area
        longitude: 151.2093 + (Math.random() - 0.5) * 0.1,
        property_type: 'Residential',
        land_area: Math.floor(Math.random() * 500) + 200, // 200-700 sqm
        floor_area: Math.floor(Math.random() * 200) + 100, // 100-300 sqm
        demographics: {},
        market_data: {}
      };
      
      if (mockGeoscapeResponse.valid) {
        // Update form with validated address data
        const form = getValues();
        form.address = {
          ...form.address,
          ...mockGeoscapeResponse,
          isValidated: true,
          validationSource: 'geoscape',
          confidenceScore: mockGeoscapeResponse.confidence_score,
          validationDate: new Date().toISOString(),
          propertyId: mockGeoscapeResponse.property_id,
          latitude: mockGeoscapeResponse.latitude,
          longitude: mockGeoscapeResponse.longitude,
          propertyType: mockGeoscapeResponse.property_type,
          landArea: mockGeoscapeResponse.land_area,
          floorArea: mockGeoscapeResponse.floor_area,
        };
        
        setValue('address', form.address);
        
        setAddressValidation({
          status: 'valid',
          message: `Address validated with ${Math.round(mockGeoscapeResponse.confidence_score * 100)}% confidence`
        });
      } else {
        setAddressValidation({
          status: 'invalid',
          message: 'Unable to validate address. Please check and try again.'
        });
      }
    } catch (error) {
      setAddressValidation({
        status: 'invalid',
        message: 'Address validation service temporarily unavailable. Please try again later.'
      });
    }
  };

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
            <UserIcon className="w-5 h-5 text-blue-600 mr-2" />
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
                onChange={(e) => handleAddressSearchChange(e.target.value)}
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

          {/* Validation Status */}
          {addressValidation.status !== 'idle' && (
            <div className={`mb-6 p-3 rounded-lg flex items-center ${
              addressValidation.status === 'valid' ? 'bg-green-50 text-green-800' :
              addressValidation.status === 'invalid' ? 'bg-red-50 text-red-800' :
              'bg-blue-50 text-blue-800'
            }`}>
              {addressValidation.status === 'valid' ? (
                <CheckCircleIcon className="w-4 h-4 mr-2" />
              ) : addressValidation.status === 'invalid' ? (
                <ExclamationTriangleIcon className="w-4 h-4 mr-2" />
              ) : (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              )}
              <span className="text-sm">{addressValidation.message}</span>
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
                <option value="Place">Place</option>
                <option value="Crescent">Crescent</option>
                <option value="Boulevard">Boulevard</option>
                <option value="Way">Way</option>
                <option value="Close">Close</option>
                <option value="Terrace">Terrace</option>
                <option value="Parade">Parade</option>
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

          {/* Address Validation Status */}
          {watch('address.isValidated') && (
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
          <div className="flex items-center mb-4">
            <LinkIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Professional Links & Social Media</h3>
          </div>
          
          <p className="text-sm text-gray-600 mb-6">
            Add your professional profiles and social media accounts. These help employers understand your professional presence and networking approach.
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