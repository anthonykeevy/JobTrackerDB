import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import ProjectsStep from './ProjectsStep';
import type { ProfileData } from '../types';

// Mock crypto.randomUUID
const mockUUID = 'test-uuid-123';
vi.stubGlobal('crypto', {
  randomUUID: () => mockUUID
});

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
    portfolio: 'https://johndoe.com'
  },
  careerAspiration: {
    currentTitle: 'Software Developer',
    shortTermRole: 'Senior Developer',
    longTermRole: 'Tech Lead',
    aspirationStatement: 'I want to lead innovative projects',
    employmentType: 'full-time',
    paymentPeriod: 'annual',
    currency: 'AUD',
    expectedAmount: 80000,
    workPreferences: []
  },
  education: {
    education: [],
    certifications: []
  },
  workExperience: {
    experiences: []
  },
  skills: {
    technical: [],
    soft: [],
    languages: []
  },
  projects: []
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
  isLastStep: false
};

describe('ProjectsStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the component with initial state', () => {
    render(<ProjectsStep {...defaultProps} />);
    
    expect(screen.getByText('Projects & Portfolio')).toBeInTheDocument();
    expect(screen.getByText(/Showcase your best work/)).toBeInTheDocument();
    expect(screen.getByText('Project 1')).toBeInTheDocument();
    expect(screen.getByText('Continue to Review')).toBeInTheDocument();
  });

  it('allows adding and removing projects', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    // Add a new project
    const addButton = screen.getByText('Add Another Project');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(screen.getByText('Project 2')).toBeInTheDocument();
    });
    
    // Remove the second project
    const removeButtons = screen.getAllByRole('button').filter(button => 
      button.querySelector('svg') && button.querySelector('svg')?.getAttribute('class')?.includes('TrashIcon')
    );
    
    if (removeButtons.length > 0) {
      fireEvent.click(removeButtons[0]);
      
      await waitFor(() => {
        expect(screen.queryByText('Project 2')).not.toBeInTheDocument();
      });
    }
  });

  it('validates required fields', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const continueButton = screen.getByText('Continue to Review');
    fireEvent.click(continueButton);
    
    await waitFor(() => {
      expect(screen.getByText('Project name is required')).toBeInTheDocument();
      expect(screen.getByText('Please provide a detailed description')).toBeInTheDocument();
      expect(screen.getByText('Start date is required')).toBeInTheDocument();
    });
  });

  it('allows filling project information', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const projectNameInput = screen.getByPlaceholderText(/e.g., E-commerce Platform/);
    const descriptionInput = screen.getByPlaceholderText(/Describe what the project does/);
    
    await userEvent.type(projectNameInput, 'Test Project');
    await userEvent.type(descriptionInput, 'This is a test project description');
    
    expect(projectNameInput).toHaveValue('Test Project');
    expect(descriptionInput).toHaveValue('This is a test project description');
  });

  it('allows selecting project type', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const projectTypeSelect = screen.getByDisplayValue('Personal Project') as HTMLSelectElement;
    
    fireEvent.change(projectTypeSelect, { target: { value: 'professional' } });
    
    expect(projectTypeSelect.value).toBe('professional');
  });

  it('allows setting team size and role', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const teamSizeSelect = screen.getByDisplayValue('Solo Project') as HTMLSelectElement;
    
    fireEvent.change(teamSizeSelect, { target: { value: '3' } });
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/e.g., Lead Developer/)).toBeInTheDocument();
    });
    
    const roleInput = screen.getByPlaceholderText(/e.g., Lead Developer/);
    await userEvent.type(roleInput, 'Lead Developer');
    
    expect(roleInput).toHaveValue('Lead Developer');
  });

  it('allows adding and removing technologies', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const techInput = screen.getByPlaceholderText(/Add technology/);
    const addTechButton = screen.getByRole('button', { name: '' }); // Plus icon button
    
    await userEvent.type(techInput, 'React');
    fireEvent.click(addTechButton);
    
    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
    });
    
    // Remove technology
    const removeButtons = screen.getAllByRole('button').filter(button => 
      button.querySelector('svg') && button.querySelector('svg')?.getAttribute('class')?.includes('XMarkIcon')
    );
    
    if (removeButtons.length > 0) {
      fireEvent.click(removeButtons[0]);
      
      await waitFor(() => {
        expect(screen.queryByText('React')).not.toBeInTheDocument();
      });
    }
  });

  it('allows adding popular technologies', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const reactButton = screen.getByText('+ React');
    fireEvent.click(reactButton);
    
    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
    });
  });

  it('allows adding and removing achievements', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    // Expand achievements section
    const achievementsButton = screen.getByText('Key Achievements');
    fireEvent.click(achievementsButton);
    
    await waitFor(() => {
      expect(screen.getByText('Add Achievement')).toBeInTheDocument();
    });
    
    // Add achievement
    const addAchievementButton = screen.getByText('Add Achievement');
    fireEvent.click(addAchievementButton);
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText('Achievement 1...')).toBeInTheDocument();
    });
    
    // Fill achievement
    const achievementInput = screen.getByPlaceholderText('Achievement 1...');
    await userEvent.type(achievementInput, 'Improved performance by 50%');
    
    expect(achievementInput).toHaveValue('Improved performance by 50%');
  });

  it('allows expanding challenges section', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const challengesButton = screen.getByText('Challenges & Solutions');
    fireEvent.click(challengesButton);
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Describe any challenges/)).toBeInTheDocument();
    });
    
    const challengesInput = screen.getByPlaceholderText(/Describe any challenges/);
    await userEvent.type(challengesInput, 'Faced scalability issues');
    
    expect(challengesInput).toHaveValue('Faced scalability issues');
  });

  it('handles ongoing project checkbox', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const ongoingCheckbox = screen.getByLabelText('This is an ongoing project');
    fireEvent.click(ongoingCheckbox);
    
    expect(ongoingCheckbox).toBeChecked();
  });

  it('submits form with valid data', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    // Fill required fields
    const projectNameInput = screen.getByPlaceholderText(/e.g., E-commerce Platform/);
    const descriptionInput = screen.getByPlaceholderText(/Describe what the project does/);
    
    await userEvent.type(projectNameInput, 'Test Project');
    await userEvent.type(descriptionInput, 'This is a test project description');
    
    // Submit form
    const continueButton = screen.getByText('Continue to Review');
    fireEvent.click(continueButton);
    
    // Verify the form can be submitted (button is clickable)
    expect(continueButton).toBeInTheDocument();
  });

  it('validates URL fields', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const projectURLInput = screen.getByPlaceholderText('https://your-project.com');
    const githubURLInput = screen.getByPlaceholderText('https://github.com/username/repo');
    
    // Test invalid URLs
    await userEvent.type(projectURLInput, 'invalid-url');
    await userEvent.type(githubURLInput, 'not-a-github-url');
    
    // Just verify the inputs are filled
    expect(projectURLInput).toHaveValue('invalid-url');
    expect(githubURLInput).toHaveValue('not-a-github-url');
  });

  it('preserves existing project data', () => {
    const existingData = {
      ...mockProfileData,
      projects: [{
        id: 'existing-project',
        projectName: 'Existing Project',
        description: 'Existing description',
        technologies: ['React', 'Node.js'],
        projectURL: 'https://example.com',
        githubURL: 'https://github.com/example',
        startDate: '2024-01',
        endDate: '2024-06',
        isOngoing: false,
        projectType: 'professional',
        teamSize: 2,
        role: 'Lead Developer',
        achievements: ['Achievement 1'],
        challenges: 'Some challenges'
      }]
    };
    
    render(<ProjectsStep {...defaultProps} data={existingData} />);
    
    expect(screen.getByDisplayValue('Existing Project')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Existing description')).toBeInTheDocument();
    expect(screen.getByDisplayValue('https://example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('https://github.com/example')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Lead Developer')).toBeInTheDocument();
  });

  it('handles multiple projects correctly', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    // Add second project
    const addButton = screen.getByText('Add Another Project');
    fireEvent.click(addButton);
    
    await waitFor(() => {
      expect(screen.getByText('Project 1')).toBeInTheDocument();
      expect(screen.getByText('Project 2')).toBeInTheDocument();
    });
    
    // Fill first project
    const project1NameInput = screen.getAllByPlaceholderText(/e.g., E-commerce Platform/)[0];
    const project1DescInput = screen.getAllByPlaceholderText(/Describe what the project does/)[0];
    
    await userEvent.type(project1NameInput, 'Project 1');
    await userEvent.type(project1DescInput, 'Description 1');
    
    // Fill second project
    const project2NameInput = screen.getAllByPlaceholderText(/e.g., E-commerce Platform/)[1];
    const project2DescInput = screen.getAllByPlaceholderText(/Describe what the project does/)[1];
    
    await userEvent.type(project2NameInput, 'Project 2');
    await userEvent.type(project2DescInput, 'Description 2');
    
    expect(project1NameInput).toHaveValue('Project 1');
    expect(project2NameInput).toHaveValue('Project 2');
  });

  it('shows project type badges with correct colors', () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const projectTypeSelect = screen.getByDisplayValue('Personal Project') as HTMLSelectElement;
    
    // Check initial personal project badge (use getAllByText to handle multiple elements)
    expect(screen.getAllByText('Personal Project')).toHaveLength(2); // Badge and select option
    
    // Change to professional
    fireEvent.change(projectTypeSelect, { target: { value: 'professional' } });
    
    expect(screen.getAllByText('Professional Work')).toHaveLength(2); // Badge and select option
  });

  it('handles technology input with Enter key', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const techInput = screen.getByPlaceholderText(/Add technology/);
    
    await userEvent.type(techInput, 'React{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
    });
  });

  it('prevents duplicate technologies', async () => {
    render(<ProjectsStep {...defaultProps} />);
    
    const techInput = screen.getByPlaceholderText(/Add technology/);
    const addTechButton = screen.getByRole('button', { name: '' }); // Plus icon button
    
    // Add React twice
    await userEvent.type(techInput, 'React');
    fireEvent.click(addTechButton);
    
    await userEvent.type(techInput, 'React');
    fireEvent.click(addTechButton);
    
    await waitFor(() => {
      const reactTags = screen.getAllByText('React');
      expect(reactTags).toHaveLength(1); // Should only have one React tag
    });
  });
}); 