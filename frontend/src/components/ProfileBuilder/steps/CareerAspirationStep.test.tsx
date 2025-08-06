import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import CareerAspirationStep from './CareerAspirationStep';
import type { ProfileData } from '../types';

// Mock the ProfileData type
const mockProfileData: ProfileData = {
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
      country: 'Australia',
    },
    countryOfBirth: '',
    nationality: '',
    workAuthorization: {
      status: 'citizen',
      visaType: '',
      expiryDate: '',
      details: '',
      otherType: '',
      seekingSponsorship: false,
    },
    professionalLinks: {
      linkedInURL: '',
      githubURL: '',
      portfolioURL: '',
      personalWebsite: '',
    },
    socialLinks: {
      twitterURL: '',
      instagramURL: '',
      facebookURL: '',
    },
  },
  careerAspiration: {
    currentTitle: '',
    shortTermRole: '',
    longTermRole: '',
    aspirationStatement: '',
    targetIndustries: [],
    workPreferences: {
      arrangements: [
        { type: 'remote', preference: 1 },
        { type: 'hybrid', preference: 2 },
        { type: 'onsite', preference: 3 },
        { type: 'flexible', preference: 4 },
      ],
      willingToRelocate: false,
    },
    salaryExpectations: {
      employmentType: 'full-time',
      amount: '',
      period: 'annually',
      currency: 'AUD',
      flexible: true,
      notes: '',
    },
  },
  education: [],
  workExperience: [],
  skills: [],
  projects: [],
  certifications: [],
};

const mockUpdateData = vi.fn();
const mockOnNext = vi.fn();
const mockOnPrevious = vi.fn();

describe('CareerAspirationStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Check for main sections
    expect(screen.getByText('Career Goals & Aspirations')).toBeInTheDocument();
    expect(screen.getByText('Career Progression')).toBeInTheDocument();
    expect(screen.getByText('Target Industries')).toBeInTheDocument();
    expect(screen.getByText('Work Preferences')).toBeInTheDocument();
    expect(screen.getByText('Salary Expectations')).toBeInTheDocument();

    // Check for form fields
    expect(screen.getByLabelText(/Current Job Title/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Short-term Goal/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Long-term Goal/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Career Vision Statement/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Employment Type/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Payment Period/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Currency/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Expected Amount/)).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Try to submit without filling required fields
    const submitButton = screen.getByText('Continue to Education');
    fireEvent.click(submitButton);

    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText('Current title is required')).toBeInTheDocument();
      expect(screen.getByText('Short-term role goal is required')).toBeInTheDocument();
      expect(screen.getByText('Long-term role goal is required')).toBeInTheDocument();
      expect(screen.getByText('Please provide a detailed career aspiration statement')).toBeInTheDocument();
      expect(screen.getByText('Please select at least one target industry')).toBeInTheDocument();
      expect(screen.getByText('Salary amount is required')).toBeInTheDocument();
    });
  });

  it('allows industry selection', async () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Find and click an industry
    const technologyIndustry = screen.getByText('Technology & Software');
    fireEvent.click(technologyIndustry);

    // Check if it's selected
    expect(technologyIndustry).toHaveClass('bg-blue-600');
  });

  it('allows work preference reordering', () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Find the up/down arrows for work preferences
    const upButtons = screen.getAllByTestId('move-up');
    const downButtons = screen.getAllByTestId('move-down');

    expect(upButtons.length).toBeGreaterThan(0);
    expect(downButtons.length).toBeGreaterThan(0);
  });

  it('handles salary period changes based on employment type', async () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Change employment type to freelance
    const employmentTypeSelect = screen.getByLabelText(/Employment Type/);
    fireEvent.change(employmentTypeSelect, { target: { value: 'freelance' } });

    // Check if period options change
    await waitFor(() => {
      expect(screen.getByText('Per Hour')).toBeInTheDocument();
      expect(screen.getByText('Per Day')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    // Fill in required fields
    fireEvent.change(screen.getByLabelText(/Current Job Title/), {
      target: { value: 'Software Engineer' },
    });
    fireEvent.change(screen.getByLabelText(/Short-term Goal/), {
      target: { value: 'Senior Software Engineer' },
    });
    fireEvent.change(screen.getByLabelText(/Long-term Goal/), {
      target: { value: 'Engineering Manager' },
    });
    fireEvent.change(screen.getByLabelText(/Career Vision Statement/), {
      target: { value: 'I want to lead engineering teams and drive technical innovation.' },
    });
    fireEvent.change(screen.getByLabelText(/Expected Amount/), {
      target: { value: '100000' },
    });

    // Select an industry
    fireEvent.click(screen.getByText('Technology & Software'));

    // Submit form
    const submitButton = screen.getByText('Continue to Education');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith({
        careerAspiration: expect.objectContaining({
          currentTitle: 'Software Engineer',
          shortTermRole: 'Senior Software Engineer',
          longTermRole: 'Engineering Manager',
          aspirationStatement: 'I want to lead engineering teams and drive technical innovation.',
          targetIndustries: ['Technology & Software'],
          salaryExpectations: expect.objectContaining({
            amount: '100000',
          }),
        }),
      });
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('handles previous button click', () => {
    render(
      <CareerAspirationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrevious={mockOnPrevious}
      />
    );

    const previousButton = screen.getByText('Previous');
    fireEvent.click(previousButton);

    expect(mockOnPrevious).toHaveBeenCalled();
  });
}); 