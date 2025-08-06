import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import WealthForgeDashboard from '../WealthForgeDashboard';
import { WealthForgeAPI } from '../../services/api';

// Mock the entire API service
jest.mock('../../services/api', () => ({
  WealthForgeAPI: {
    getHealth: jest.fn(),
    runCompleteAnalysis: jest.fn(),
  },
  formatCurrency: jest.fn((amount: number) => `$${amount.toLocaleString()}`),
  formatPercentage: jest.fn((value: number) => `${(value * 100).toFixed(1)}%`),
  formatNumber: jest.fn((value: number) => value.toFixed(0)),
  getStatusColor: jest.fn(() => 'status-success'),
}));

// Mock child components
jest.mock('../ClientProfileForm', () => {
  return function MockClientProfileForm({ onSubmit, isLoading }: any) {
    return (
      <div data-testid="client-profile-form">
        <button
          onClick={() => onSubmit({
            goals: { strategy: 'aggressive growth', timeline: '7 years' },
            constraints: { capital: 15000, contributions: 300 }
          })}
          disabled={isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Submit Form'}
        </button>
      </div>
    );
  };
});

jest.mock('../AnalysisResults', () => {
  return function MockAnalysisResults({ analysis }: any) {
    return (
      <div data-testid="analysis-results">
        <h2>Analysis Results</h2>
        <p>Expected Return: {analysis.portfolio_synthesis.expected_return}</p>
      </div>
    );
  };
});

const mockHealthStatus = {
  api: 'healthy',
  redis: 'connected',
  kafka: 'connected',
  timestamp: '2024-01-01T00:00:00Z',
};

const mockCompleteAnalysis = {
  complete_analysis: {
    client_profile: {
      goals: { strategy: 'aggressive growth', timeline: '7 years' },
      constraints: { capital: 15000, contributions: 300 },
    },
    arena_result: {
      strategies_generated: 50,
      winner: { agent_name: 'TestAgent', agent_role: 'Growth', alpha_score: 0.85 },
      execution_time: 30,
      top_strategies: [],
    },
    portfolio_synthesis: {
      portfolio_id: 'test-001',
      final_allocation: { stocks: 0.8, bonds: 0.2 },
      expected_return: 0.08,
      risk_score: 0.15,
      sharpe_ratio: 0.53,
      synthesis_confidence: 0.9,
      contributing_agents: ['TestAgent'],
      optimization_method: 'pareto',
      risk_analysis: { volatility: 0.12, var_95: -0.03, max_drawdown: 0.15, beta: 1.0 },
      cost_analysis: { total_expense_ratio: 0.005, tax_efficiency_score: 0.9, fee_optimization_savings: 0.002 },
    },
    compliance_audit: {
      audit_id: 'audit-001',
      overall_compliance: 'compliant',
      audit_score: 95,
      requires_manual_review: false,
      capital_validation: { compliance_status: 'compliant', total_capital: 15000, investment_capital: 12750, warnings: [] },
      contribution_validation: { compliance_status: 'compliant', ira_contributions: 6000, ira_limit: 6500, violations: [] },
      regulatory_analysis: { client_classification: 'retail', regulatory_risk_score: 0.1, applicable_regulations: [], suitability_assessment: {} },
      violations: [],
      recommendations: [],
    },
    optimization: {
      optimization_id: 'opt-001',
      original_goal_probability: 0.6,
      optimized_goal_probability: 0.8,
      improvement_factor: 1.33,
      recommended_scenarios: [],
      sensitivity_analysis: {},
      implementation_roadmap: 'Test roadmap',
      risk_assessment: {},
    },
  },
};

describe('WealthForgeDashboard', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    jest.clearAllMocks();
    (WealthForgeAPI.getHealth as jest.Mock).mockResolvedValue(mockHealthStatus);
    (WealthForgeAPI.runCompleteAnalysis as jest.Mock).mockResolvedValue(mockCompleteAnalysis);
  });

  it('renders dashboard header correctly', () => {
    render(<WealthForgeDashboard />);
    
    expect(screen.getByText('WealthForge')).toBeInTheDocument();
    expect(screen.getByText('AI-Powered Investment Platform')).toBeInTheDocument();
  });

  it('checks API health on mount', async () => {
    render(<WealthForgeDashboard />);
    
    await waitFor(() => {
      expect(WealthForgeAPI.getHealth).toHaveBeenCalledTimes(1);
    });
  });

  it('displays health status indicators', async () => {
    render(<WealthForgeDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('API')).toBeInTheDocument();
      expect(screen.getByText('Cache')).toBeInTheDocument();
      expect(screen.getByText('Queue')).toBeInTheDocument();
    });
  });

  it('shows form step by default', () => {
    render(<WealthForgeDashboard />);
    
    expect(screen.getByText('Complete Investment Analysis')).toBeInTheDocument();
    expect(screen.getByText('50+ AI Agents')).toBeInTheDocument();
    expect(screen.getByText('Pareto Optimization')).toBeInTheDocument();
    expect(screen.getByText('Goal Optimization')).toBeInTheDocument();
    expect(screen.getByTestId('client-profile-form')).toBeInTheDocument();
  });

  it('displays progress indicator correctly', () => {
    render(<WealthForgeDashboard />);
    
    expect(screen.getByText('Client Profile')).toBeInTheDocument();
    expect(screen.getByText('AI Analysis')).toBeInTheDocument();
    expect(screen.getByText('Results')).toBeInTheDocument();
  });

  it('handles form submission and shows analysis step', async () => {
    render(<WealthForgeDashboard />);
    
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Running WealthForge Analysis')).toBeInTheDocument();
      expect(screen.getByText('Our AI agents are analyzing your profile')).toBeInTheDocument();
    });
  });

  it('shows loading states during analysis', async () => {
    render(<WealthForgeDashboard />);
    
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Parsing goals and constraints')).toBeInTheDocument();
      expect(screen.getByText('50 agents generating strategies')).toBeInTheDocument();
      expect(screen.getByText('Portfolio synthesis and optimization')).toBeInTheDocument();
    });
  });

  it('displays results after successful analysis', async () => {
    render(<WealthForgeDashboard />);
    
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(WealthForgeAPI.runCompleteAnalysis).toHaveBeenCalledWith({
        goals: { strategy: 'aggressive growth', timeline: '7 years' },
        constraints: { capital: 15000, contributions: 300 },
      });
    });

    await waitFor(() => {
      expect(screen.getByText('Your Investment Analysis')).toBeInTheDocument();
      expect(screen.getByTestId('analysis-results')).toBeInTheDocument();
      expect(screen.getByText('Expected Return: 0.08')).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    const errorMessage = 'API Error: Connection failed';
    (WealthForgeAPI.runCompleteAnalysis as jest.Mock).mockRejectedValue(
      new Error(errorMessage)
    );

    render(<WealthForgeDashboard />);
    
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Analysis Error')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    // Should return to form step
    expect(screen.getByTestId('client-profile-form')).toBeInTheDocument();
  });

  it('handles detailed API error responses', async () => {
    const detailedError = {
      response: {
        data: {
          detail: 'Validation error: Invalid risk tolerance',
        },
      },
    };
    (WealthForgeAPI.runCompleteAnalysis as jest.Mock).mockRejectedValue(detailedError);

    render(<WealthForgeDashboard />);
    
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Validation error: Invalid risk tolerance')).toBeInTheDocument();
    });
  });

  it('provides start over functionality', async () => {
    render(<WealthForgeDashboard />);
    
    // Complete analysis
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Your Investment Analysis')).toBeInTheDocument();
    });

    // Click start over
    const startOverButton = screen.getByText('New Analysis');
    await user.click(startOverButton);
    
    // Should return to form step
    expect(screen.getByText('Complete Investment Analysis')).toBeInTheDocument();
    expect(screen.getByTestId('client-profile-form')).toBeInTheDocument();
  });

  it('handles health check failure gracefully', async () => {
    (WealthForgeAPI.getHealth as jest.Mock).mockRejectedValue(new Error('Health check failed'));

    render(<WealthForgeDashboard />);
    
    await waitFor(() => {
      // Should still render the dashboard even if health check fails
      expect(screen.getByText('WealthForge')).toBeInTheDocument();
    });
  });

  it('shows correct health status colors', async () => {
    const healthyStatus = { api: 'healthy', redis: 'connected', kafka: 'connected', timestamp: '2024-01-01T00:00:00Z' };
    (WealthForgeAPI.getHealth as jest.Mock).mockResolvedValue(healthyStatus);

    render(<WealthForgeDashboard />);
    
    await waitFor(() => {
      // Check for health indicator elements (color indicators are CSS classes)
      const healthIndicators = screen.getAllByText('API');
      expect(healthIndicators.length).toBeGreaterThan(0);
    });
  });

  it('displays footer information', () => {
    render(<WealthForgeDashboard />);
    
    expect(screen.getByText('WealthForge v1.0.0 - AI-Powered Investment Platform')).toBeInTheDocument();
    expect(screen.getByText('Powered by FastAPI, React, and Advanced AI Optimization')).toBeInTheDocument();
  });

  it('updates progress indicator based on current step', async () => {
    render(<WealthForgeDashboard />);
    
    // Initially on form step
    const step1 = screen.getByText('Client Profile').closest('div');
    expect(step1).toHaveClass('bg-primary-600');
    
    // Submit form to go to analysis step
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    await waitFor(() => {
      const step2 = screen.getByText('AI Analysis').closest('div');
      expect(step2).toHaveClass('bg-primary-600');
    });
  });
});

// Integration test for complete dashboard flow
describe('WealthForgeDashboard Integration', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    jest.clearAllMocks();
    (WealthForgeAPI.getHealth as jest.Mock).mockResolvedValue(mockHealthStatus);
    (WealthForgeAPI.runCompleteAnalysis as jest.Mock).mockResolvedValue(mockCompleteAnalysis);
  });

  it('completes full analysis workflow', async () => {
    render(<WealthForgeDashboard />);
    
    // Step 1: Verify initial state
    expect(screen.getByText('Complete Investment Analysis')).toBeInTheDocument();
    expect(screen.getByTestId('client-profile-form')).toBeInTheDocument();
    
    // Step 2: Submit form
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    // Step 3: Verify analysis state
    await waitFor(() => {
      expect(screen.getByText('Running WealthForge Analysis')).toBeInTheDocument();
    });
    
    // Step 4: Verify results state
    await waitFor(() => {
      expect(screen.getByText('Your Investment Analysis')).toBeInTheDocument();
      expect(screen.getByTestId('analysis-results')).toBeInTheDocument();
    });
    
    // Step 5: Verify API was called with correct data
    expect(WealthForgeAPI.runCompleteAnalysis).toHaveBeenCalledWith({
      goals: { strategy: 'aggressive growth', timeline: '7 years' },
      constraints: { capital: 15000, contributions: 300 },
    });
    
    // Step 6: Test start over functionality
    const startOverButton = screen.getByText('New Analysis');
    await user.click(startOverButton);
    
    expect(screen.getByText('Complete Investment Analysis')).toBeInTheDocument();
    expect(screen.getByTestId('client-profile-form')).toBeInTheDocument();
  });

  it('maintains health status throughout workflow', async () => {
    render(<WealthForgeDashboard />);
    
    // Health status should be displayed initially
    await waitFor(() => {
      expect(screen.getByText('API')).toBeInTheDocument();
    });
    
    // Submit form
    const submitButton = screen.getByText('Submit Form');
    await user.click(submitButton);
    
    // Health status should persist during analysis
    await waitFor(() => {
      expect(screen.getByText('API')).toBeInTheDocument();
    });
    
    // Health status should persist in results
    await waitFor(() => {
      expect(screen.getByText('Your Investment Analysis')).toBeInTheDocument();
      expect(screen.getByText('API')).toBeInTheDocument();
    });
  });
});