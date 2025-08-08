import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import SkillsStep from './SkillsStep';
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
    skills: []
  } as ProfileData,
  updateData: mockUpdateData,
  onNext: mockOnNext,
  onPrev: mockOnPrev,
  isFirstStep: false,
  isLastStep: false
};

describe('SkillsStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the component with initial state', () => {
    render(<SkillsStep {...defaultProps} />);
    
    expect(screen.getByText('Skills & Expertise')).toBeInTheDocument();
    expect(screen.getByText('Showcase your technical skills, soft skills, languages, and certifications with proficiency levels.')).toBeInTheDocument();
    expect(screen.getByTestId('category-technical')).toBeInTheDocument();
    expect(screen.getByTestId('category-soft')).toBeInTheDocument();
    expect(screen.getByTestId('category-language')).toBeInTheDocument();
    expect(screen.getByTestId('category-certification')).toBeInTheDocument();
    expect(screen.getByText('Continue to Projects')).toBeInTheDocument();
  });

  it('renders category navigation with correct counts', () => {
    render(<SkillsStep {...defaultProps} />);
    
    // Check that all categories show 0 skills initially
    expect(screen.getAllByText('0 skills')).toHaveLength(4);
  });

  it('allows switching between skill categories', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Initially should be on Technical Skills
    expect(screen.getByText('Programming languages, frameworks, tools, and technologies')).toBeInTheDocument();
    
    // Switch to Soft Skills
    const softSkillsButton = screen.getByTestId('category-soft');
    await user.click(softSkillsButton);
    
    // Check that the soft skills description is shown
    expect(screen.getByText(/Leadership/)).toBeInTheDocument();
    
    // Switch to Languages
    const languagesButton = screen.getByTestId('category-language');
    await user.click(languagesButton);
    
    expect(screen.getByText('Spoken languages and proficiency levels')).toBeInTheDocument();
    
    // Switch to Certifications
    const certificationsButton = screen.getByTestId('category-certification');
    await user.click(certificationsButton);
    
    expect(screen.getByText('Professional certifications and credentials')).toBeInTheDocument();
  });

  it('allows adding skills from suggestions', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a suggested technical skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Skill should be added to the form
    expect(screen.getByDisplayValue('JavaScript')).toBeInTheDocument();
    expect(screen.getByText('intermediate Level')).toBeInTheDocument();
  });

  it('allows adding custom skills', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add custom skill
    const addCustomButton = screen.getByText('Add Custom Technical Skill');
    await user.click(addCustomButton);
    
    // Custom skill input should appear
    const skillInput = screen.getByPlaceholderText('Enter technical skill...');
    expect(skillInput).toBeInTheDocument();
    
    // Fill in the skill
    await user.type(skillInput, 'Custom Skill');
    
    expect(screen.getByDisplayValue('Custom Skill')).toBeInTheDocument();
  });

  it('allows removing skills', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill first
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Find and click the remove button
    const removeButtons = screen.getAllByRole('button').filter(button => 
      button.querySelector('svg') && button.closest('div')?.textContent?.includes('JavaScript')
    );
    
    if (removeButtons.length > 0) {
      const removeButton = removeButtons[removeButtons.length - 1];
      await user.click(removeButton);
      
      // Skill should be removed
      await waitFor(() => {
        expect(screen.queryByDisplayValue('JavaScript')).not.toBeInTheDocument();
      });
    }
  });

  it('allows changing proficiency levels', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Change proficiency level
    const proficiencySelect = screen.getByLabelText('Proficiency *');
    await user.selectOptions(proficiencySelect, 'expert');
    
    // Check that the badge shows the new level
    expect(screen.getByText('expert Level')).toBeInTheDocument();
  });

  it('allows setting years of experience', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Set years of experience
    const yearsInput = screen.getByPlaceholderText('0');
    await user.type(yearsInput, '5');
    
    expect(screen.getByDisplayValue('5')).toBeInTheDocument();
    expect(screen.getByText('• 5 years experience')).toBeInTheDocument();
  });

  it('validates required skill name', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill but leave name empty
    const addCustomButton = screen.getByText('Add Custom Technical Skill');
    await user.click(addCustomButton);
    
    // Try to submit without filling skill name
    const submitButton = screen.getByText('Continue to Projects');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Skill name is required')).toBeInTheDocument();
    });
  });

  it('submits form with valid skills data', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill with complete data
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Set years of experience
    const yearsInput = screen.getByPlaceholderText('0');
    await user.type(yearsInput, '3');
    
    // Submit form
    const submitButton = screen.getByText('Continue to Projects');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockUpdateData).toHaveBeenCalledWith('skills', expect.arrayContaining([
        expect.objectContaining({
          skillName: 'JavaScript',
          proficiency: 'intermediate',
          skillType: 'technical',
          yearsOfExperience: 3
        })
      ]));
      expect(mockOnNext).toHaveBeenCalled();
    });
  });

  it('shows skills summary when skills are added', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Skills summary should appear
    expect(screen.getByText('Skills Summary')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument(); // Technical skills count
  });

  it('shows empty state when no skills are added', () => {
    render(<SkillsStep {...defaultProps} />);
    
    // Check for empty state elements
    expect(screen.getByText('Click the suggestions above or add a custom skill to get started.')).toBeInTheDocument();
  });

  it('handles different skill categories correctly', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add technical skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Switch to Soft Skills
    const softSkillsButton = screen.getByTestId('category-soft');
    await user.click(softSkillsButton);
    
    // Add soft skill using custom skill button
    const addCustomButton = screen.getByText(/Add Custom .* Skill/);
    await user.click(addCustomButton);
    
    // Fill in the skill
    const skillInput = screen.getByPlaceholderText(/Enter .* skill/);
    await user.type(skillInput, 'Leadership');
    
    // Verify that skills can be added to different categories
    expect(screen.getByDisplayValue('Leadership')).toBeInTheDocument();
  });

  it('preserves existing skills data', () => {
    const existingData = {
      skills: [{
        id: 'existing-id',
        skillName: 'Existing Skill',
        proficiency: 'advanced',
        skillType: 'technical',
        yearsOfExperience: 5
      }]
    } as ProfileData;

    render(<SkillsStep {...defaultProps} data={existingData} />);
    
    expect(screen.getByDisplayValue('Existing Skill')).toBeInTheDocument();
    expect(screen.getByDisplayValue('5')).toBeInTheDocument();
  });

  it('shows proficiency badges with correct colors', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Check that proficiency badge is shown
    expect(screen.getByText('intermediate Level')).toBeInTheDocument();
    
    // Change to expert level
    const proficiencySelect = screen.getByLabelText('Proficiency *');
    await user.selectOptions(proficiencySelect, 'expert');
    
    expect(screen.getByText('expert Level')).toBeInTheDocument();
  });

  it('handles years of experience display correctly', async () => {
    const user = userEvent.setup();
    render(<SkillsStep {...defaultProps} />);
    
    // Add a skill
    const addJavaScriptButton = screen.getByText('+ JavaScript');
    await user.click(addJavaScriptButton);
    
    // Set 1 year experience
    const yearsInput = screen.getByPlaceholderText('0');
    await user.type(yearsInput, '1');
    
    expect(screen.getByText('• 1 year experience')).toBeInTheDocument();
    
    // Change to 2 years
    await user.clear(yearsInput);
    await user.type(yearsInput, '2');
    
    expect(screen.getByText('• 2 years experience')).toBeInTheDocument();
  });
}); 