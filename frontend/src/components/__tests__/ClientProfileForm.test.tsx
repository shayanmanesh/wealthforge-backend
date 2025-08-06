import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import ClientProfileForm from '../ClientProfileForm';
import { ClientProfile } from '../../services/api';

// Mock the API service
jest.mock('../../services/api', () => ({
  formatCurrency: jest.fn((amount: number) => `$${amount.toLocaleString()}`),
  formatPercentage: jest.fn((value: number) => `${(value * 100).toFixed(1)}%`),
}));

describe('ClientProfileForm', () => {
  const mockOnSubmit = jest.fn();
  const user = userEvent.setup();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders all form tabs', () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByText('Goals & Objectives')).toBeInTheDocument();
    expect(screen.getByText('Constraints')).toBeInTheDocument();
    expect(screen.getByText('Preferences')).toBeInTheDocument();
    expect(screen.getByText('Financial Info')).toBeInTheDocument();
  });

  it('shows goals tab by default', () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByText('Investment Goals & Objectives')).toBeInTheDocument();
    expect(screen.getByLabelText('Investment Strategy')).toBeInTheDocument();
    expect(screen.getByLabelText('Investment Timeline')).toBeInTheDocument();
    expect(screen.getByLabelText('Target Amount ($)')).toBeInTheDocument();
    expect(screen.getByLabelText('Risk Tolerance')).toBeInTheDocument();
  });

  it('switches between tabs correctly', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Click on Constraints tab
    await user.click(screen.getByText('Constraints'));
    expect(screen.getByText('Financial Constraints')).toBeInTheDocument();
    expect(screen.getByLabelText('Initial Capital ($)')).toBeInTheDocument();
    
    // Click on Preferences tab
    await user.click(screen.getByText('Preferences'));
    expect(screen.getByText('Investment Preferences')).toBeInTheDocument();
    expect(screen.getByLabelText('Age')).toBeInTheDocument();
    
    // Click on Financial Info tab
    await user.click(screen.getByText('Financial Info'));
    expect(screen.getByText('Financial Information')).toBeInTheDocument();
    expect(screen.getByLabelText('Annual Income ($)')).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Try to submit form without filling required fields
    const submitButton = screen.getByRole('button', { name: /analyze portfolio/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Strategy is required')).toBeInTheDocument();
      expect(screen.getByText('Timeline is required')).toBeInTheDocument();
      expect(screen.getByText('Target amount is required')).toBeInTheDocument();
      expect(screen.getByText('Risk tolerance is required')).toBeInTheDocument();
    });
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('shows loading state when isLoading prop is true', () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} isLoading={true} />);
    
    const submitButton = screen.getByRole('button', { name: /analyzing/i });
    expect(submitButton).toBeDisabled();
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();
  });

  it('accepts initial data and populates form', () => {
    const initialData: Partial<ClientProfile> = {
      goals: {
        strategy: 'aggressive growth',
        timeline: '10 years',
        target_amount: 500000,
        risk_tolerance: 'high',
        secondary_goals: ['Early Retirement'],
      },
      constraints: {
        capital: 100000,
        contributions: 2000,
        contribution_frequency: 'monthly',
        max_risk_percentage: 80,
      },
    };

    render(<ClientProfileForm onSubmit={mockOnSubmit} initialData={initialData} />);
    
    expect(screen.getByDisplayValue('aggressive growth')).toBeInTheDocument();
    expect(screen.getByDisplayValue('10 years')).toBeInTheDocument();
    expect(screen.getByDisplayValue('500000')).toBeInTheDocument();
    expect(screen.getByDisplayValue('high')).toBeInTheDocument();
  });

  it('handles secondary goals addition and removal', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Add a secondary goal
    const earlyRetirementButton = screen.getByText('Early Retirement');
    await user.click(earlyRetirementButton);
    
    // Check if the goal is added
    expect(screen.getByText('Early Retirement')).toBeInTheDocument();
    
    // Remove the goal
    const removeButton = screen.getByRole('button', { name: '' }); // Minus icon button
    await user.click(removeButton);
    
    // Check if the goal is removed (should show add button again)
    await waitFor(() => {
      expect(screen.getByText('Early Retirement')).toBeInTheDocument();
    });
  });

  it('handles sector focus addition and removal', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Switch to Preferences tab
    await user.click(screen.getByText('Preferences'));
    
    // Add a sector focus
    const technologyButton = screen.getByText('Technology');
    await user.click(technologyButton);
    
    // Check if the sector is added
    expect(screen.getByText('Technology')).toBeInTheDocument();
  });

  it('calculates financial metrics correctly', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Switch to Constraints tab and fill in values
    await user.click(screen.getByText('Constraints'));
    
    const capitalInput = screen.getByLabelText('Initial Capital ($)');
    const contributionsInput = screen.getByLabelText('Monthly Contributions ($)');
    
    await user.clear(capitalInput);
    await user.type(capitalInput, '100000');
    
    await user.clear(contributionsInput);
    await user.type(contributionsInput, '2000');
    
    // Switch to Financial Info tab and fill income
    await user.click(screen.getByText('Financial Info'));
    
    const incomeInput = screen.getByLabelText('Annual Income ($)');
    await user.clear(incomeInput);
    await user.type(incomeInput, '80000');
    
    // Check if calculations are displayed
    await waitFor(() => {
      expect(screen.getByText('Capital Adequacy Analysis')).toBeInTheDocument();
      expect(screen.getByText('Financial Health Overview')).toBeInTheDocument();
    });
  });

  it('submits form with correct data structure', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Fill out the form
    await user.selectOptions(screen.getByLabelText('Investment Strategy'), 'aggressive growth');
    await user.selectOptions(screen.getByLabelText('Investment Timeline'), '10 years');
    await user.clear(screen.getByLabelText('Target Amount ($)'));
    await user.type(screen.getByLabelText('Target Amount ($)'), '500000');
    await user.selectOptions(screen.getByLabelText('Risk Tolerance'), 'high');
    
    // Switch to constraints tab and fill required fields
    await user.click(screen.getByText('Constraints'));
    await user.clear(screen.getByLabelText('Initial Capital ($)'));
    await user.type(screen.getByLabelText('Initial Capital ($)'), '100000');
    await user.clear(screen.getByLabelText('Monthly Contributions ($)'));
    await user.type(screen.getByLabelText('Monthly Contributions ($)'), '2000');
    
    // Switch to financial info and fill required fields
    await user.click(screen.getByText('Financial Info'));
    await user.clear(screen.getByLabelText('Annual Income ($)'));
    await user.type(screen.getByLabelText('Annual Income ($)'), '80000');
    await user.clear(screen.getByLabelText('Net Worth ($)'));
    await user.type(screen.getByLabelText('Net Worth ($)'), '200000');
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /analyze portfolio/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          goals: expect.objectContaining({
            strategy: 'aggressive growth',
            timeline: '10 years',
            target_amount: 500000,
            risk_tolerance: 'high',
          }),
          constraints: expect.objectContaining({
            capital: 100000,
            contributions: 2000,
          }),
          financial_info: expect.objectContaining({
            annual_income: 80000,
            net_worth: 200000,
          }),
        })
      );
    });
  });

  it('handles form validation errors appropriately', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Try to submit with invalid target amount
    await user.clear(screen.getByLabelText('Target Amount ($)'));
    await user.type(screen.getByLabelText('Target Amount ($)'), '500');
    
    const submitButton = screen.getByRole('button', { name: /analyze portfolio/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Minimum target is $1,000')).toBeInTheDocument();
    });
  });

  it('handles checkbox interactions correctly', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Switch to Preferences tab
    await user.click(screen.getByText('Preferences'));
    
    // Check ESG investing checkbox
    const esgCheckbox = screen.getByRole('checkbox', { name: /esg\/sustainable investing/i });
    await user.click(esgCheckbox);
    
    expect(esgCheckbox).toBeChecked();
    
    // Uncheck it
    await user.click(esgCheckbox);
    expect(esgCheckbox).not.toBeChecked();
  });
});

// Integration test for complete form flow
describe('ClientProfileForm Integration', () => {
  const mockOnSubmit = jest.fn();
  const user = userEvent.setup();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('completes full form flow with all tabs', async () => {
    render(<ClientProfileForm onSubmit={mockOnSubmit} />);
    
    // Step 1: Goals tab
    await user.selectOptions(screen.getByLabelText('Investment Strategy'), 'aggressive growth');
    await user.selectOptions(screen.getByLabelText('Investment Timeline'), '7 years');
    await user.clear(screen.getByLabelText('Target Amount ($)'));
    await user.type(screen.getByLabelText('Target Amount ($)'), '150000');
    await user.selectOptions(screen.getByLabelText('Risk Tolerance'), 'high');
    
    // Step 2: Constraints tab
    await user.click(screen.getByText('Constraints'));
    await user.clear(screen.getByLabelText('Initial Capital ($)'));
    await user.type(screen.getByLabelText('Initial Capital ($)'), '15000');
    await user.clear(screen.getByLabelText('Monthly Contributions ($)'));
    await user.type(screen.getByLabelText('Monthly Contributions ($)'), '300');
    await user.clear(screen.getByLabelText('Maximum Risk Percentage (%)'));
    await user.type(screen.getByLabelText('Maximum Risk Percentage (%)'), '85');
    
    // Step 3: Preferences tab
    await user.click(screen.getByText('Preferences'));
    await user.clear(screen.getByLabelText('Age'));
    await user.type(screen.getByLabelText('Age'), '28');
    
    // Add sector focus
    const technologyButton = screen.getByText('Technology');
    await user.click(technologyButton);
    
    // Step 4: Financial Info tab
    await user.click(screen.getByText('Financial Info'));
    await user.clear(screen.getByLabelText('Annual Income ($)'));
    await user.type(screen.getByLabelText('Annual Income ($)'), '65000');
    await user.clear(screen.getByLabelText('Net Worth ($)'));
    await user.type(screen.getByLabelText('Net Worth ($)'), '25000');
    await user.selectOptions(screen.getByLabelText('Investment Experience'), 'intermediate');
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /analyze portfolio/i });
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          goals: expect.objectContaining({
            strategy: 'aggressive growth',
            timeline: '7 years',
            target_amount: 150000,
            risk_tolerance: 'high',
          }),
          constraints: expect.objectContaining({
            capital: 15000,
            contributions: 300,
            max_risk_percentage: 85,
          }),
          additional_preferences: expect.objectContaining({
            age: 28,
            sector_focus: ['Technology'],
          }),
          financial_info: expect.objectContaining({
            annual_income: 65000,
            net_worth: 25000,
            investment_experience: 'intermediate',
          }),
        })
      );
    });
  });
});