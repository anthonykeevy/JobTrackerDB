import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import WorkExperienceStep from './WorkExperienceStep';
import type { ProfileData } from '../types';

// Mock crypto.randomUUID with unique IDs
let uuidCounter = 0;
Object.defineProperty(global, 'crypto', {
  value: {
    randomUUID: () => `test-uuid-${++uuidCounter}`
  }
});

const mockUpdateData = vi.fn();
const mockOnNext = vi.fn();
const mockOnPrev = vi.fn();

const defaultProps = {
  data: {
    workExperience: []
  } as ProfileData,
  updateData: mockUpdateData,
  onNext: mockOnNext,
  onPrev: mockOnPrev,
  isFirstStep: false,
  isLastStep: false
};

describe('WorkExperienceStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the component with initial state', () => {
    render(<WorkExperienceStep {...defaultProps} />);
    
    expect(screen.getByText('Work Experience')).toBeInTheDocument();
    expect(screen.getByText('Detail your professional experience, achievements, and skills gained in each role.')).toBeInTheDocument();
    expect(screen.getByText('Experience 1')).toBeInTheDocument();
    expect(screen.getByText('Add Another Work Experience')).toBeInTheDocument();
    expect(screen.getByText('Continue to Skills')).toBeInTheDocument();
  });

  it('renders form fields with proper labels', () => {
    render(<WorkExperienceStep {...defaultProps} />);
    
    expect(screen.getByLabelText('Job Title *')).toBeInTheDocument();
    expect(screen.getByLabelText('Company Name *')).toBeInTheDocument();
    expect(screen.getByLabelText('Start Date *')).toBeInTheDocument();
    expect(screen.getByLabelText('End Date')).toBeInTheDocument();
    expect(screen.getByLabelText('This is my current role')).toBeInTheDocument();
    expect(screen.getByLabelText('Job Description *')).toBeInTheDocument();
  });

  it('allows adding and removing work experiences', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Add another experience
    const addButton = screen.getByText('Add Another Work Experience');
    await user.click(addButton);
    
    expect(screen.getByText('Experience 1')).toBeInTheDocument();
    expect(screen.getByText('Experience 2')).toBeInTheDocument();
    
    // Find the remove button for the second experience
    const experienceCards = screen.getAllByText(/Experience \d+/);
    const secondExperienceCard = experienceCards.find(card => card.textContent?.includes('Experience 2'));
    
    if (secondExperienceCard) {
      const removeButton = secondExperienceCard.closest('div')?.querySelector('button[type="button"]');
      if (removeButton) {
        await user.click(removeButton);
        
        // Wait for the removal to complete
        await waitFor(() => {
          expect(screen.getByText('Experience 1')).toBeInTheDocument();
          expect(screen.queryByText('Experience 2')).not.toBeInTheDocument();
        });
      }
    }
  });

  it('validates required fields', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Try to submit without filling required fields
    const submitButton = screen.getByText('Continue to Skills');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Job title is required')).toBeInTheDocument();
      expect(screen.getByText('Company name is required')).toBeInTheDocument();
      expect(screen.getByText('Start date is required')).toBeInTheDocument();
      expect(screen.getByText('Job description is required')).toBeInTheDocument();
    });
  });

  it('allows filling and submitting valid data', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Fill required fields
    const jobTitleInput = screen.getByLabelText('Job Title *');
    const companyNameInput = screen.getByLabelText('Company Name *');
    const startDateInput = screen.getByLabelText('Start Date *');
    const descriptionInput = screen.getByLabelText('Job Description *');
    
    await user.type(jobTitleInput, 'Software Engineer');
    await user.type(companyNameInput, 'Tech Corp');
    await user.type(startDateInput, '2023-01');
    await user.type(descriptionInput, 'Developed web applications using React and Node.js');
    
    // Submit form
    const submitButton = screen.getByText('Continue to Skills');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith('workExperience', expect.arrayContaining([
        expect.objectContaining({
          jobTitle: 'Software Engineer',
          companyName: 'Tech Corp',
          startDate: '2023-01',
          description: 'Developed web applications using React and Node.js'
        })
      ]));
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('handles current role checkbox correctly', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    const currentRoleCheckbox = screen.getByLabelText('This is my current role');
    const endDateInput = screen.getByLabelText('End Date');
    
    // Initially, end date should be enabled
    expect(endDateInput).not.toBeDisabled();
    
    // Check current role
    await user.click(currentRoleCheckbox);
    
    // End date should be disabled
    expect(endDateInput).toBeDisabled();
    
    // Uncheck current role
    await user.click(currentRoleCheckbox);
    
    // End date should be enabled again
    expect(endDateInput).not.toBeDisabled();
  });

  it('allows adding and removing achievements', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Initially, achievements section should be collapsed
    expect(screen.getByText('+ Add your key achievements and accomplishments')).toBeInTheDocument();
    
    // Expand achievements section
    const expandButton = screen.getByTestId('expand-achievements-0');
    await user.click(expandButton);
    
    // Add achievement
    const addAchievementButton = screen.getByText('Add Achievement');
    await user.click(addAchievementButton);
    
    // Achievement input should appear
    const achievementInput = screen.getByPlaceholderText('Achievement 1...');
    expect(achievementInput).toBeInTheDocument();
    
    // Fill achievement
    await user.type(achievementInput, 'Led team of 5 developers');
    
    // Find and click the remove button for the achievement
    const achievementContainer = achievementInput.closest('div');
    const removeButton = achievementContainer?.querySelector('button[type="button"]');
    
    if (removeButton) {
      await user.click(removeButton);
      
      // Wait for the removal to complete
      await waitFor(() => {
        expect(screen.queryByPlaceholderText('Achievement 1...')).not.toBeInTheDocument();
      });
    }
  });

  it('allows adding and removing skills', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Initially, skills section should be collapsed
    expect(screen.getByText('+ Add skills and technologies you used in this role')).toBeInTheDocument();
    
    // Expand skills section
    const skillsExpandButton = screen.getByTestId('expand-skills-0');
    await user.click(skillsExpandButton);
    
    // Add skill
    const addSkillButton = screen.getByText('Add Skill');
    await user.click(addSkillButton);
    
    // Skill input should appear
    const skillInput = screen.getByPlaceholderText('e.g., React, Python, Leadership...');
    expect(skillInput).toBeInTheDocument();
    
    // Fill skill
    await user.type(skillInput, 'React');
    
    // Find and click the remove button for the skill
    const skillContainer = skillInput.closest('div');
    const removeButton = skillContainer?.querySelector('button[type="button"]');
    
    if (removeButton) {
      await user.click(removeButton);
      
      // Wait for the removal to complete
      await waitFor(() => {
        expect(screen.queryByPlaceholderText('e.g., React, Python, Leadership...')).not.toBeInTheDocument();
      });
    }
  });

  it('expands sections when adding items directly', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Click on "Add your key achievements" button
    const addAchievementsButton = screen.getByText('+ Add your key achievements and accomplishments');
    await user.click(addAchievementsButton);
    
    // Achievements section should be expanded
    expect(screen.getByText('Add Achievement')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Achievement 1...')).toBeInTheDocument();
    
    // Click on "Add skills" button
    const addSkillsButton = screen.getByText('+ Add skills and technologies you used in this role');
    await user.click(addSkillsButton);
    
    // Skills section should be expanded
    expect(screen.getByText('Add Skill')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('e.g., React, Python, Leadership...')).toBeInTheDocument();
  });

  it('submits form with achievements and skills data', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Fill basic required fields
    const jobTitleInput = screen.getByLabelText('Job Title *');
    const companyNameInput = screen.getByLabelText('Company Name *');
    const startDateInput = screen.getByLabelText('Start Date *');
    const descriptionInput = screen.getByLabelText('Job Description *');
    
    await user.type(jobTitleInput, 'Senior Developer');
    await user.type(companyNameInput, 'Innovation Inc');
    await user.type(startDateInput, '2022-06');
    await user.type(descriptionInput, 'Developed scalable web applications');
    
    // Add achievement
    const addAchievementsButton = screen.getByText('+ Add your key achievements and accomplishments');
    await user.click(addAchievementsButton);
    const achievementInput = screen.getByPlaceholderText('Achievement 1...');
    await user.type(achievementInput, 'Improved performance by 40%');
    
    // Add skill
    const addSkillsButton = screen.getByText('+ Add skills and technologies you used in this role');
    await user.click(addSkillsButton);
    const skillInput = screen.getByPlaceholderText('e.g., React, Python, Leadership...');
    await user.type(skillInput, 'TypeScript');
    
    // Submit form
    const submitButton = screen.getByText('Continue to Skills');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith('workExperience', expect.arrayContaining([
        expect.objectContaining({
          jobTitle: 'Senior Developer',
          companyName: 'Innovation Inc',
          startDate: '2022-06',
          description: 'Developed scalable web applications',
          achievements: ['Improved performance by 40%'],
          skills: ['TypeScript']
        })
      ]));
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('handles multiple work experiences correctly', async () => {
    const user = userEvent.setup();
    render(<WorkExperienceStep {...defaultProps} />);
    
    // Fill first experience
    const jobTitleInput = screen.getByLabelText('Job Title *');
    const companyNameInput = screen.getByLabelText('Company Name *');
    const startDateInput = screen.getByLabelText('Start Date *');
    const descriptionInput = screen.getByLabelText('Job Description *');
    
    await user.type(jobTitleInput, 'Junior Developer');
    await user.type(companyNameInput, 'Startup Co');
    await user.type(startDateInput, '2021-01');
    await user.type(descriptionInput, 'Built frontend components');
    
    // Add second experience
    const addExperienceButton = screen.getByText('Add Another Work Experience');
    await user.click(addExperienceButton);
    
    // Fill second experience
    const secondJobTitleInput = screen.getAllByLabelText('Job Title *')[1];
    const secondCompanyNameInput = screen.getAllByLabelText('Company Name *')[1];
    const secondStartDateInput = screen.getAllByLabelText('Start Date *')[1];
    const secondDescriptionInput = screen.getAllByLabelText('Job Description *')[1];
    
    await user.type(secondJobTitleInput, 'Senior Developer');
    await user.type(secondCompanyNameInput, 'Tech Giant');
    await user.type(secondStartDateInput, '2023-01');
    await user.type(secondDescriptionInput, 'Led development team');
    
    // Submit form
    const submitButton = screen.getByText('Continue to Skills');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith('workExperience', expect.arrayContaining([
        expect.objectContaining({
          jobTitle: 'Junior Developer',
          companyName: 'Startup Co'
        }),
        expect.objectContaining({
          jobTitle: 'Senior Developer',
          companyName: 'Tech Giant'
        })
      ]));
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('preserves existing data when component re-renders', () => {
    const existingData = {
      workExperience: [{
        id: 'existing-id',
        companyName: 'Existing Corp',
        jobTitle: 'Existing Role',
        startDate: '2020-01',
        endDate: '2022-12',
        isCurrentRole: false,
        description: 'Existing description',
        achievements: ['Existing achievement'],
        skills: ['Existing skill']
      }]
    } as ProfileData;

    render(<WorkExperienceStep {...defaultProps} data={existingData} />);
    
    expect(screen.getByDisplayValue('Existing Corp')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing Role')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2020-01')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2022-12')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing description')).toBeInTheDocument();
  });
}); 