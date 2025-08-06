import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import ReviewStep from './ReviewStep';
import type { ProfileData } from '../types';

const mockProfileData: ProfileData = {
  basicInfo: {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    phone: '1234567890',
    address: {
      streetName: '123 Main St',
      suburb: 'Test City',
      state: 'NSW',
      postcode: '2000',
      country: 'Australia'
    },
    linkedin: 'https://linkedin.com/in/johndoe',
    github: 'https://github.com/johndoe',
    portfolio: 'https://johndoe.com',
    nationality: 'Australian',
    workAuthorization: {
      status: 'citizen',
      visaType: null
    }
  },
  careerAspiration: {
    currentTitle: 'Software Developer',
    shortTermRole: 'Senior Developer',
    longTermRole: 'Tech Lead',
    aspirationStatement: 'I want to lead innovative projects and mentor junior developers',
    employmentType: 'full-time',
    paymentPeriod: 'annual',
    currency: 'AUD',
    expectedAmount: 80000,
    workPreferences: []
  },
  education: [
    {
      id: 'edu-1',
      institutionName: 'University of Technology',
      degree: 'Bachelor of Science',
      fieldOfStudy: 'Computer Science',
      startDate: '2018-01',
      endDate: '2022-12',
      currentlyEnrolled: false,
      gpa: 3.8,
      description: 'Focused on software engineering and algorithms'
    }
  ],
  workExperience: [
    {
      id: 'exp-1',
      companyName: 'Tech Corp',
      jobTitle: 'Software Developer',
      startDate: '2022-01',
      endDate: '2023-12',
      currentlyWorking: false,
      description: 'Developed web applications using React and Node.js',
      achievements: ['Improved performance by 50%', 'Led team of 3 developers'],
      skills: ['React', 'Node.js', 'TypeScript']
    }
  ],
  skills: [
    {
      id: 'skill-1',
      skillName: 'React',
      category: 'technical',
      proficiency: 'advanced',
      yearsOfExperience: 3
    },
    {
      id: 'skill-2',
      skillName: 'JavaScript',
      category: 'technical',
      proficiency: 'advanced',
      yearsOfExperience: 5
    },
    {
      id: 'skill-3',
      skillName: 'Leadership',
      category: 'soft',
      proficiency: 'intermediate',
      yearsOfExperience: 2
    }
  ],
  projects: [
    {
      id: 'proj-1',
      projectName: 'E-commerce Platform',
      description: 'A full-stack e-commerce application with payment integration',
      technologies: ['React', 'Node.js', 'MongoDB'],
      projectURL: 'https://example.com',
      githubURL: 'https://github.com/example',
      startDate: '2023-01',
      endDate: '2023-06',
      isOngoing: false,
      projectType: 'personal',
      teamSize: 1,
      role: 'Full Stack Developer',
      achievements: ['Implemented payment gateway', 'Achieved 99.9% uptime'],
      challenges: 'Handling high traffic and payment security'
    }
  ]
};

const mockUpdateData = vi.fn();
const mockOnNext = vi.fn();
const mockOnPrev = vi.fn();
const mockOnJumpToStep = vi.fn();

const defaultProps = {
  data: mockProfileData,
  updateData: mockUpdateData,
  onNext: mockOnNext,
  onPrev: mockOnPrev,
  onJumpToStep: mockOnJumpToStep,
  isFirstStep: false,
  isLastStep: true
};

describe('ReviewStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the component with initial state', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Review Your Profile')).toBeInTheDocument();
    expect(screen.getByText(/Take a moment to review/)).toBeInTheDocument();
    expect(screen.getByText('Complete Profile')).toBeInTheDocument();
    expect(screen.getByText('Profile Completeness')).toBeInTheDocument();
  });

  it('displays all profile sections', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Basic Information')).toBeInTheDocument();
    expect(screen.getByText('Career Goals')).toBeInTheDocument();
    expect(screen.getAllByText('Education')).toHaveLength(2); // Section title and stats
    expect(screen.getByText('Work Experience')).toBeInTheDocument();
    expect(screen.getAllByText('Skills')).toHaveLength(2); // Section title and stats
    expect(screen.getAllByText('Projects')).toHaveLength(2); // Section title and stats
  });

  it('shows profile completeness percentage', () => {
    render(<ReviewStep {...defaultProps} />);
    
    const completenessElement = screen.getByText(/\d+%/);
    expect(completenessElement).toBeInTheDocument();
  });

  it('displays basic information correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('Test City, Australia')).toBeInTheDocument();
    expect(screen.getByText('Citizen')).toBeInTheDocument();
  });

  it('displays career goals correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Senior Developer')).toBeInTheDocument();
    expect(screen.getByText(/I want to lead innovative projects/)).toBeInTheDocument();
  });

  it('displays education information correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Bachelor of Science in Computer Science')).toBeInTheDocument();
    expect(screen.getByText('University of Technology')).toBeInTheDocument();
  });

  it('displays work experience correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Software Developer')).toBeInTheDocument();
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
  });

  it('displays skills correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('React')).toBeInTheDocument();
    expect(screen.getByText('JavaScript')).toBeInTheDocument();
    expect(screen.getByText('Leadership')).toBeInTheDocument();
  });

  it('displays projects correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('E-commerce Platform')).toBeInTheDocument();
    expect(screen.getByText(/A full-stack e-commerce application/)).toBeInTheDocument();
  });

  it('allows editing sections by clicking on them', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    const basicInfoSection = screen.getByText('Basic Information').closest('div');
    fireEvent.click(basicInfoSection!);
    
    expect(mockOnJumpToStep).toHaveBeenCalledWith(2);
  });

  it('handles profile submission', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    // Should show loading state
    await waitFor(() => {
      expect(screen.getByText('Submitting Profile...')).toBeInTheDocument();
    });
    
    // Wait for submission to complete
    await waitFor(() => {
      expect(screen.getByText('🎉 Profile Complete!')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('shows completion screen after submission', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('🎉 Profile Complete!')).toBeInTheDocument();
      expect(screen.getByText(/Congratulations!/)).toBeInTheDocument();
      expect(screen.getByText('Go to Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Review Profile Again')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('allows returning to review from completion screen', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    // Submit profile first
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('🎉 Profile Complete!')).toBeInTheDocument();
    }, { timeout: 3000 });
    
    // Click "Review Profile Again"
    const reviewAgainButton = screen.getByText('Review Profile Again');
    fireEvent.click(reviewAgainButton);
    
    // Should return to review screen
    expect(screen.getByText('Review Your Profile')).toBeInTheDocument();
  });

  it('displays profile statistics correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Your Profile at a Glance')).toBeInTheDocument();
    expect(screen.getAllByText('1')).toHaveLength(3); // Education, Experience, and Projects count
    expect(screen.getByText('3')).toBeInTheDocument(); // Skills count
  });

  it('shows share and export buttons', () => {
    render(<ReviewStep {...defaultProps} />);
    
    expect(screen.getByText('Share')).toBeInTheDocument();
    expect(screen.getByText('Export')).toBeInTheDocument();
  });

  it('handles empty profile data gracefully', () => {
    const emptyData = {
      basicInfo: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address: {
          streetName: '',
          suburb: '',
          state: '',
          postcode: '',
          country: ''
        },
        linkedin: '',
        github: '',
        portfolio: '',
        nationality: '',
        workAuthorization: {
          status: '',
          visaType: null
        }
      },
      careerAspiration: {
        currentTitle: '',
        shortTermRole: '',
        longTermRole: '',
        aspirationStatement: '',
        employmentType: 'full-time',
        paymentPeriod: 'annual',
        currency: 'AUD',
        expectedAmount: 0,
        workPreferences: []
      },
      education: [],
      workExperience: [],
      skills: [],
      projects: []
    };
    
    render(<ReviewStep {...defaultProps} data={emptyData} />);
    
    // Should show empty states
    expect(screen.getByText('Click to add basic information')).toBeInTheDocument();
    expect(screen.getByText('Click to add career goals')).toBeInTheDocument();
    expect(screen.getByText('Click to add education')).toBeInTheDocument();
    expect(screen.getByText('Click to add work experience')).toBeInTheDocument();
    expect(screen.getByText('Click to add skills')).toBeInTheDocument();
    expect(screen.getByText('Click to add projects')).toBeInTheDocument();
  });

  it('calculates completeness score correctly', () => {
    render(<ReviewStep {...defaultProps} />);
    
    const completenessElement = screen.getByText(/\d+%/);
    const completenessValue = parseInt(completenessElement.textContent!);
    
    // Should be a reasonable percentage (not 0% or 100% for this test data)
    expect(completenessValue).toBeGreaterThan(0);
    expect(completenessValue).toBeLessThanOrEqual(100);
  });

  it('shows appropriate completeness message', () => {
    render(<ReviewStep {...defaultProps} />);
    
    // Should show one of the completeness messages
    const hasCompletenessMessage = screen.getByText(/Perfect!|Great!|Good progress!|Keep going!/);
    expect(hasCompletenessMessage).toBeInTheDocument();
  });

  it('disables submit button during submission', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Submitting Profile...')).toBeInTheDocument();
      expect(submitButton).toBeDisabled();
    });
  });

  it('handles navigation to dashboard', async () => {
    // Mock window.location
    const originalLocation = window.location;
    delete (window as any).location;
    window.location = { ...originalLocation, href: '' };
    
    render(<ReviewStep {...defaultProps} />);
    
    // Submit profile first
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('🎉 Profile Complete!')).toBeInTheDocument();
    }, { timeout: 3000 });
    
    // Click "Go to Dashboard"
    const dashboardButton = screen.getByText('Go to Dashboard');
    fireEvent.click(dashboardButton);
    
    // Should navigate to dashboard
    expect(window.location.href).toBe('/dashboard');
    
    // Restore original location
    window.location = originalLocation;
  });

  it('shows completion features after submission', async () => {
    render(<ReviewStep {...defaultProps} />);
    
    const submitButton = screen.getByText('Complete Profile');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('🎉 Profile Complete!')).toBeInTheDocument();
      expect(screen.getByText('AI Job Matching')).toBeInTheDocument();
      expect(screen.getByText('Resume Generation')).toBeInTheDocument();
      expect(screen.getByText('Career Analytics')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('handles multiple education entries display', () => {
    const dataWithMultipleEducation = {
      ...mockProfileData,
      education: [
        ...mockProfileData.education,
        {
          id: 'edu-2',
          institutionName: 'Online University',
          degree: 'Master of Science',
          fieldOfStudy: 'Data Science',
          startDate: '2023-01',
          endDate: '2024-01',
          currentlyEnrolled: false,
          gpa: 3.9,
          description: 'Specialized in machine learning'
        }
      ]
    };
    
    render(<ReviewStep {...defaultProps} data={dataWithMultipleEducation} />);
    
    expect(screen.getByText('+1 more')).toBeInTheDocument();
  });

  it('handles multiple work experience entries display', () => {
    const dataWithMultipleExperience = {
      ...mockProfileData,
      workExperience: [
        ...mockProfileData.workExperience,
        {
          id: 'exp-2',
          companyName: 'Startup Inc',
          jobTitle: 'Senior Developer',
          startDate: '2024-01',
          endDate: '',
          currentlyWorking: true,
          description: 'Leading development team',
          achievements: ['Increased team productivity'],
          skills: ['React', 'Python', 'AWS']
        }
      ]
    };
    
    render(<ReviewStep {...defaultProps} data={dataWithMultipleExperience} />);
    
    expect(screen.getByText('+1 more positions')).toBeInTheDocument();
  });

  it('handles multiple projects display', () => {
    const dataWithMultipleProjects = {
      ...mockProfileData,
      projects: [
        ...mockProfileData.projects,
        {
          id: 'proj-2',
          projectName: 'Mobile App',
          description: 'Cross-platform mobile application',
          technologies: ['React Native', 'Firebase'],
          projectURL: 'https://mobile-app.com',
          githubURL: 'https://github.com/mobile-app',
          startDate: '2024-01',
          endDate: '2024-06',
          isOngoing: true,
          projectType: 'personal',
          teamSize: 2,
          role: 'Lead Developer',
          achievements: ['Published to app stores'],
          challenges: 'Cross-platform compatibility'
        }
      ]
    };
    
    render(<ReviewStep {...defaultProps} data={dataWithMultipleProjects} />);
    
    expect(screen.getByText('+1 more projects')).toBeInTheDocument();
  });
}); 