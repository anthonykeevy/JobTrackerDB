// Profile Data Types for ProfileBuilder
export interface ProfileData {
  resumeData?: {
    fileName: string;
    fileSize: number;
    uploadedAt: string;
    processed: boolean;
    extractedData?: any;
  };
  basicInfo: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    // Full address fields
    address: {
      streetAddress: string;
      apartment?: string;
      city: string;
      state: string;
      postalCode: string;
      country: string;
    };
    // Birth and nationality
    dateOfBirth?: string;
    countryOfBirth: string;
    nationality: string;
    // Work authorization
    workAuthorization: {
      status: 'citizen' | 'permanent_resident' | 'work_visa' | 'student_visa' | 'other';
      visaType?: string;
      expiryDate?: string;
      details?: string;
      otherType?: string;
      seekingSponsorship?: boolean;
    };
    // Professional links (prioritized)
    professionalLinks: {
      linkedInURL?: string;
      githubURL?: string;
      portfolioURL?: string;
      personalWebsite?: string;
    };
    // Optional social media (secondary)
    socialLinks?: {
      twitterURL?: string;
      instagramURL?: string;
      facebookURL?: string;
      other?: Array<{name: string; url: string}>;
    };
  };
  careerAspiration: {
    currentTitle: string;
    shortTermRole: string;
    longTermRole: string;
    aspirationStatement: string;
    targetIndustries: string[];
    workPreferences: {
      arrangements: Array<{
        type: 'remote' | 'hybrid' | 'onsite' | 'flexible';
        preference: number; // 1 = most preferred, 4 = least preferred
      }>;
      willingToRelocate: boolean;
    };
    salaryExpectations: {
      employmentType: 'full-time' | 'part-time' | 'contract' | 'temporary' | 'freelance';
      amount: string;
      period: 'hourly' | 'daily' | 'weekly' | 'fortnightly' | 'monthly' | 'annually';
      currency: string;
      flexible: boolean;
      notes?: string;
    };
  };
  education: Array<{
    id: string;
    institutionName: string;
    degree: string;
    fieldOfStudy: string;
    startDate: string;
    endDate?: string;
    isCurrentlyEnrolled: boolean;
    gpa?: number;
    description?: string;
  }>;
  workExperience: Array<{
    id: string;
    companyName: string;
    jobTitle: string;
    startDate: string;
    endDate?: string;
    isCurrentRole: boolean;
    description: string;
    achievements: string[];
    skills: string[];
  }>;
  skills: Array<{
    id: string;
    skillName: string;
    proficiency: 'beginner' | 'intermediate' | 'advanced' | 'expert';
    skillType: 'technical' | 'soft' | 'language' | 'certification';
    yearsOfExperience?: number;
  }>;
  projects: Array<{
    id: string;
    projectName: string;
    description: string;
    technologies: string[];
    projectURL?: string;
    startDate: string;
    endDate?: string;
    isOngoing: boolean;
  }>;
  certifications: Array<{
    id: string;
    certificationName: string;
    issuingOrganization: string;
    issueDate: string;
    expiryDate?: string;
    credentialID?: string;
    description?: string;
  }>;
}