import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import EducationStep from './EducationStep';
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
const mockOnPrev = vi.fn();

describe('EducationStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders education and certifications tabs', () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    expect(screen.getByText('Education & Certifications')).toBeInTheDocument();
    expect(screen.getByText('Education')).toBeInTheDocument();
    expect(screen.getByText('Certifications')).toBeInTheDocument();
  });

  it('allows switching between education and certifications tabs', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Initially education tab should be active
    expect(screen.getByText('Institution Name *')).toBeInTheDocument();

    // Click on certifications tab
    fireEvent.click(screen.getByText('Certifications'));

    // Should show certification fields
    await waitFor(() => {
      expect(screen.getByText('Certification Name *')).toBeInTheDocument();
    });
  });

  it('allows adding and removing education entries', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Should have one education entry by default
    expect(screen.getByText('Education 1')).toBeInTheDocument();

    // Add another education entry
    fireEvent.click(screen.getByText('Add Another Education'));

    // Should now have two education entries
    await waitFor(() => {
      expect(screen.getByText('Education 1')).toBeInTheDocument();
      expect(screen.getByText('Education 2')).toBeInTheDocument();
    });

    // Remove the second education entry
    const removeButtons = screen.getAllByRole('button').filter(button => 
      button.innerHTML.includes('TrashIcon')
    );
    if (removeButtons.length > 1) {
      fireEvent.click(removeButtons[1]);
    }

    // Should be back to one education entry
    await waitFor(() => {
      expect(screen.getByText('Education 1')).toBeInTheDocument();
      expect(screen.queryByText('Education 2')).not.toBeInTheDocument();
    });
  });

  it('validates required education fields', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Try to submit without filling required fields
    const submitButton = screen.getByText('Continue to Work Experience');
    fireEvent.click(submitButton);

    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText('Institution name is required')).toBeInTheDocument();
      expect(screen.getByText('Degree is required')).toBeInTheDocument();
      expect(screen.getByText('Field of study is required')).toBeInTheDocument();
      expect(screen.getByText('Start date is required')).toBeInTheDocument();
    });
  });

  it('allows filling education form fields', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Fill in education fields
    fireEvent.change(screen.getByPlaceholderText('e.g., Stanford University'), {
      target: { value: 'MIT' },
    });

    fireEvent.change(screen.getByDisplayValue('Select degree'), {
      target: { value: 'Bachelor\'s Degree' },
    });

    fireEvent.change(screen.getByPlaceholderText('e.g., Computer Science'), {
      target: { value: 'Computer Science' },
    });

    fireEvent.change(screen.getByLabelText(/Start Date/), {
      target: { value: '2020-09' },
    });

    // Check if values are set
    expect(screen.getByDisplayValue('MIT')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Bachelor\'s Degree')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Computer Science')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2020-09')).toBeInTheDocument();
  });

  it('allows adding and removing certification entries', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Switch to certifications tab
    fireEvent.click(screen.getByText('Certifications'));

    // Add a certification - the text is split across elements
    const addCertButton = screen.getByRole('button', { name: /Add Certification/i });
    fireEvent.click(addCertButton);

    // Should have certification fields
    await waitFor(() => {
      expect(screen.getByText('Certification Name *')).toBeInTheDocument();
    });
  });

  it('validates required certification fields', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Switch to certifications tab
    fireEvent.click(screen.getByText('Certifications'));

    // Add a certification first
    const addCertButton = screen.getByRole('button', { name: /Add Certification/i });
    fireEvent.click(addCertButton);

    // Wait for the certification form to appear
    await waitFor(() => {
      expect(screen.getByText('Certification Name *')).toBeInTheDocument();
    });

    // Try to submit without filling required fields
    const submitButton = screen.getByText('Continue to Work Experience');
    fireEvent.click(submitButton);

    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText('Certification name is required')).toBeInTheDocument();
      expect(screen.getByText('Issuing organization is required')).toBeInTheDocument();
      expect(screen.getByText('Issue date is required')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    // Fill in required education fields
    fireEvent.change(screen.getByPlaceholderText('e.g., Stanford University'), {
      target: { value: 'MIT' },
    });

    fireEvent.change(screen.getByDisplayValue('Select degree'), {
      target: { value: 'Bachelor\'s Degree' },
    });

    fireEvent.change(screen.getByPlaceholderText('e.g., Computer Science'), {
      target: { value: 'Computer Science' },
    });

    fireEvent.change(screen.getByLabelText(/Start Date/), {
      target: { value: '2020-09' },
    });

    // Wait for animations to complete
    await waitFor(() => {
      expect(screen.getByDisplayValue('MIT')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Bachelor\'s Degree')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Computer Science')).toBeInTheDocument();
      expect(screen.getByDisplayValue('2020-09')).toBeInTheDocument();
    });

    // Submit form
    const submitButton = screen.getByText('Continue to Work Experience');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith('education', expect.arrayContaining([
        expect.objectContaining({
          institutionName: 'MIT',
          degree: 'Bachelor\'s Degree',
          fieldOfStudy: 'Computer Science',
          startDate: '2020-09',
        }),
      ]));
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('handles currently enrolled checkbox', () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    const currentlyEnrolledCheckbox = screen.getByLabelText(/Currently enrolled/);
    fireEvent.click(currentlyEnrolledCheckbox);

    expect(currentlyEnrolledCheckbox).toBeChecked();
  });

  it('handles GPA field', () => {
    render(
      <EducationStep
        data={mockProfileData}
        updateData={mockUpdateData}
        onNext={mockOnNext}
        onPrev={mockOnPrev}
        isFirstStep={false}
        isLastStep={false}
      />
    );

    const gpaInput = screen.getByPlaceholderText('e.g., 3.8');
    fireEvent.change(gpaInput, { target: { value: '3.8' } });

    expect(gpaInput).toHaveValue(3.8);
  });
}); 