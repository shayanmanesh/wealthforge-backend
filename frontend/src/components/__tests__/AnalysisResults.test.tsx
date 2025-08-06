import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import AnalysisResults from '../AnalysisResults';
import { CompleteAnalysis } from '../../services/api';

// Mock Recharts components to avoid rendering issues in tests
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => <div data-testid="responsive-container">{children}</div>,
  PieChart: ({ children }: any) => <div data-testid="pie-chart">{children}</div>,
  Pie: () => <div data-testid="pie" />,
  Cell: () => <div data-testid="cell" />,
  BarChart: ({ children }: any) => <div data-testid="bar-chart">{children}</div>,
  Bar: () => <div data-testid="bar" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Legend: () => <div data-testid="legend" />,
}));

// Mock the API service
jest.mock('../../services/api', () => ({
  formatCurrency: jest.fn((amount: number) => `$${amount.toLocaleString()}`),
  formatPercentage: jest.fn((value: number, decimals = 1) => `${(value * 100).toFixed(decimals)}%`),
  formatNumber: jest.fn((value: number, decimals = 0) => value.toFixed(decimals)),
  getStatusColor: jest.fn((status: string) => {
    switch (status.toLowerCase()) {
      case 'compliant':
      case 'healthy':
        return 'status-success';
      case 'warning':
        return 'status-warning';
      case 'violation':
        return 'status-danger';
      default:
        return 'status-warning';
    }
  }),
}));

const mockAnalysis: CompleteAnalysis = {
  client_profile: {
    goals: {
      strategy: 'aggressive growth',
      timeline: '7 years',
      target_amount: 150000,
      risk_tolerance: 'high',
      secondary_goals: ['Early Retirement'],
    },
    constraints: {
      capital: 15000,
      contributions: 300,
      contribution_frequency: 'monthly',
      max_risk_percentage: 85,
    },
    additional_preferences: {
      age: 28,
      ira_contributions: 6000,
      '401k_contributions': 18000,
      esg_investing: false,
      sector_focus: ['Technology'],
      international_exposure: 'medium',
      alternative_investments: false,
      impact_investing: false,
    },
    financial_info: {
      annual_income: 65000,
      net_worth: 25000,
      liquid_assets: 15000,
      investment_experience: 'intermediate',
      risk_capacity: 'high',
      time_horizon: 'long-term',
    },
  },
  arena_result: {
    strategies_generated: 50,
    winner: {
      agent_name: 'GrowthOptimizer-47',
      agent_role: 'Aggressive Growth Specialist',
      alpha_score: 0.8432,
    },
    execution_time: 45.7,
    top_strategies: [],
  },
  portfolio_synthesis: {
    portfolio_id: 'portfolio-001',
    final_allocation: {
      'US_STOCKS': 0.70,
      'INTL_STOCKS': 0.15,
      'BONDS': 0.10,
      'ALTERNATIVES': 0.05,
    },
    expected_return: 0.085,
    risk_score: 0.18,
    sharpe_ratio: 0.47,
    synthesis_confidence: 0.92,
    contributing_agents: ['GrowthOptimizer-47', 'RiskBalancer-23'],
    optimization_method: 'pareto_optimal',
    risk_analysis: {
      volatility: 0.16,
      var_95: -0.045,
      max_drawdown: 0.25,
      beta: 1.15,
    },
    cost_analysis: {
      total_expense_ratio: 0.0075,
      tax_efficiency_score: 0.85,
      fee_optimization_savings: 0.0025,
    },
  },
  compliance_audit: {
    audit_id: 'audit-001',
    overall_compliance: 'compliant',
    audit_score: 92,
    requires_manual_review: false,
    capital_validation: {
      compliance_status: 'compliant',
      total_capital: 15000,
      investment_capital: 12750,
      warnings: [],
    },
    contribution_validation: {
      compliance_status: 'compliant',
      ira_contributions: 6000,
      ira_limit: 6500,
      violations: [],
    },
    regulatory_analysis: {
      client_classification: 'retail_investor',
      regulatory_risk_score: 0.15,
      applicable_regulations: ['Regulation BI', 'Know Your Customer'],
      suitability_assessment: {},
    },
    violations: [],
    recommendations: ['Consider increasing emergency fund', 'Monitor risk exposure'],
  },
  optimization: {
    optimization_id: 'opt-001',
    original_goal_probability: 0.65,
    optimized_goal_probability: 0.82,
    improvement_factor: 1.26,
    recommended_scenarios: [
      {
        scenario_id: 'scenario-1',
        scenario_name: 'Aggressive Contribution Increase',
        probability_of_success: 0.88,
        excess_achievement: 0.15,
        implementation_score: 0.75,
        time_to_goal: 6.2,
        adjustments: [
          {
            adjustment_type: 'monthly_contribution',
            description: 'Increase monthly contributions',
            current_value: 300,
            suggested_value: 450,
            impact_magnitude: 0.23,
            implementation_difficulty: 0.4,
          },
        ],
      },
    ],
    sensitivity_analysis: {
      capital: {
        sensitivity_coefficient: 0.0125,
        elasticity: 0.85,
        critical_threshold: 10000,
        risk_factors: ['Market volatility', 'Liquidity constraints'],
      },
    },
    implementation_roadmap: 'Phase 1: Increase contributions by $150/month\nPhase 2: Optimize asset allocation\nPhase 3: Monitor and rebalance quarterly',
    risk_assessment: {},
  },
};

describe('AnalysisResults', () => {
  const user = userEvent.setup();

  it('renders loading state correctly', () => {
    render(<AnalysisResults analysis={mockAnalysis} isLoading={true} />);
    
    expect(screen.getAllByTestId('loading-shimmer')).toHaveLength(0); // Using shimmer class instead
    // Check for loading skeleton elements
    const loadingElements = document.querySelectorAll('.animate-pulse');
    expect(loadingElements.length).toBeGreaterThan(0);
  });

  it('renders all tab navigation correctly', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    expect(screen.getByText('Overview')).toBeInTheDocument();
    expect(screen.getByText('Portfolio')).toBeInTheDocument();
    expect(screen.getByText('Compliance')).toBeInTheDocument();
    expect(screen.getByText('Optimization')).toBeInTheDocument();
  });

  it('shows overview tab by default', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    expect(screen.getByText('WealthForge Analysis Results')).toBeInTheDocument();
    expect(screen.getByText('Expected Return')).toBeInTheDocument();
    expect(screen.getByText('Risk Score')).toBeInTheDocument();
    expect(screen.getByText('Sharpe Ratio')).toBeInTheDocument();
    expect(screen.getByText('Compliance Score')).toBeInTheDocument();
  });

  it('displays key metrics correctly in overview', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    // Check if metrics are displayed with proper formatting
    expect(screen.getByText('8.5%')).toBeInTheDocument(); // Expected return
    expect(screen.getByText('18.0%')).toBeInTheDocument(); // Risk score
    expect(screen.getByText('0.47')).toBeInTheDocument(); // Sharpe ratio
    expect(screen.getByText('92')).toBeInTheDocument(); // Compliance score
  });

  it('displays winning strategy information', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    expect(screen.getByText('Winning Strategy')).toBeInTheDocument();
    expect(screen.getByText('GrowthOptimizer-47')).toBeInTheDocument();
    expect(screen.getByText('Aggressive Growth Specialist')).toBeInTheDocument();
    expect(screen.getByText('0.8432')).toBeInTheDocument();
  });

  it('displays goal achievement improvement', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    expect(screen.getByText('Goal Achievement Improvement')).toBeInTheDocument();
    expect(screen.getByText('65.0%')).toBeInTheDocument(); // Original probability
    expect(screen.getByText('82.0%')).toBeInTheDocument(); // Optimized probability
    expect(screen.getByText('1.26x')).toBeInTheDocument(); // Improvement factor
  });

  it('switches to portfolio tab and displays allocation', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Portfolio'));
    
    expect(screen.getByText('Asset Allocation')).toBeInTheDocument();
    expect(screen.getByText('Risk Analysis')).toBeInTheDocument();
    expect(screen.getByText('Cost Analysis')).toBeInTheDocument();
    
    // Check for chart components
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });

  it('displays portfolio allocation breakdown', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Portfolio'));
    
    expect(screen.getByText('Allocation Breakdown')).toBeInTheDocument();
    expect(screen.getByText('US_STOCKS')).toBeInTheDocument();
    expect(screen.getByText('INTL_STOCKS')).toBeInTheDocument();
    expect(screen.getByText('BONDS')).toBeInTheDocument();
    expect(screen.getByText('ALTERNATIVES')).toBeInTheDocument();
  });

  it('displays cost analysis metrics', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Portfolio'));
    
    expect(screen.getByText('Total Expense Ratio')).toBeInTheDocument();
    expect(screen.getByText('Tax Efficiency Score')).toBeInTheDocument();
    expect(screen.getByText('Fee Optimization Savings')).toBeInTheDocument();
  });

  it('switches to compliance tab and displays audit results', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Compliance'));
    
    expect(screen.getByText('Compliance Overview')).toBeInTheDocument();
    expect(screen.getByText('Overall Compliance')).toBeInTheDocument();
    expect(screen.getByText('Audit Score')).toBeInTheDocument();
    expect(screen.getByText('Manual Review Required')).toBeInTheDocument();
  });

  it('displays capital validation results', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Compliance'));
    
    expect(screen.getByText('Capital Validation')).toBeInTheDocument();
    expect(screen.getByText('$15,000')).toBeInTheDocument(); // Total capital
    expect(screen.getByText('$12,750')).toBeInTheDocument(); // Investment capital
  });

  it('displays regulatory analysis', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Compliance'));
    
    expect(screen.getByText('Regulatory Analysis')).toBeInTheDocument();
    expect(screen.getByText('retail investor')).toBeInTheDocument();
    expect(screen.getByText('Regulation BI')).toBeInTheDocument();
    expect(screen.getByText('Know Your Customer')).toBeInTheDocument();
  });

  it('switches to optimization tab and displays results', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Optimization'));
    
    expect(screen.getByText('Optimization Results')).toBeInTheDocument();
    expect(screen.getByText('Original Goal Probability')).toBeInTheDocument();
    expect(screen.getByText('Optimized Probability')).toBeInTheDocument();
    expect(screen.getByText('Improvement Factor')).toBeInTheDocument();
  });

  it('displays recommended scenarios', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Optimization'));
    
    expect(screen.getByText('Recommended Scenarios')).toBeInTheDocument();
    expect(screen.getByText('Aggressive Contribution Increase')).toBeInTheDocument();
    expect(screen.getByText('Required Adjustments:')).toBeInTheDocument();
    expect(screen.getByText('Increase monthly contributions')).toBeInTheDocument();
  });

  it('displays sensitivity analysis', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Optimization'));
    
    expect(screen.getByText('Sensitivity Analysis')).toBeInTheDocument();
    expect(screen.getByText('Capital')).toBeInTheDocument();
    expect(screen.getByText('Sensitivity Coefficient')).toBeInTheDocument();
    expect(screen.getByText('Market volatility')).toBeInTheDocument();
  });

  it('displays implementation roadmap', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    await user.click(screen.getByText('Optimization'));
    
    expect(screen.getByText('Implementation Roadmap')).toBeInTheDocument();
    expect(screen.getByText(/Phase 1: Increase contributions/)).toBeInTheDocument();
  });

  it('handles violations display when present', async () => {
    const analysisWithViolations = {
      ...mockAnalysis,
      compliance_audit: {
        ...mockAnalysis.compliance_audit,
        violations: [
          {
            violation_id: 'V001',
            severity: 'high',
            description: 'Risk exposure exceeds guidelines',
            recommendation: 'Reduce equity allocation by 10%',
          },
        ],
      },
    };

    render(<AnalysisResults analysis={analysisWithViolations} />);
    
    await user.click(screen.getByText('Compliance'));
    
    expect(screen.getByText('Compliance Violations (1)')).toBeInTheDocument();
    expect(screen.getByText('Risk exposure exceeds guidelines')).toBeInTheDocument();
    expect(screen.getByText('Reduce equity allocation by 10%')).toBeInTheDocument();
  });

  it('handles empty scenarios gracefully', async () => {
    const analysisWithoutScenarios = {
      ...mockAnalysis,
      optimization: {
        ...mockAnalysis.optimization,
        recommended_scenarios: [],
      },
    };

    render(<AnalysisResults analysis={analysisWithoutScenarios} />);
    
    await user.click(screen.getByText('Optimization'));
    
    expect(screen.getByText('Recommended Scenarios')).toBeInTheDocument();
    // Should not crash even with empty scenarios
  });

  it('applies correct status colors', () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    // Check if status badges are rendered (mocked getStatusColor should be called)
    const { getStatusColor } = require('../../services/api');
    expect(getStatusColor).toHaveBeenCalledWith('compliant');
  });
});

// Integration test for tab switching
describe('AnalysisResults Tab Integration', () => {
  const user = userEvent.setup();

  it('maintains data consistency across tab switches', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    // Start on Overview
    expect(screen.getByText('Expected Return')).toBeInTheDocument();
    
    // Switch to Portfolio
    await user.click(screen.getByText('Portfolio'));
    expect(screen.getByText('Asset Allocation')).toBeInTheDocument();
    
    // Switch to Compliance
    await user.click(screen.getByText('Compliance'));
    expect(screen.getByText('Compliance Overview')).toBeInTheDocument();
    
    // Switch to Optimization
    await user.click(screen.getByText('Optimization'));
    expect(screen.getByText('Optimization Results')).toBeInTheDocument();
    
    // Switch back to Overview
    await user.click(screen.getByText('Overview'));
    expect(screen.getByText('Expected Return')).toBeInTheDocument();
  });

  it('highlights active tab correctly', async () => {
    render(<AnalysisResults analysis={mockAnalysis} />);
    
    // Overview should be active by default
    const overviewTab = screen.getByText('Overview').closest('button');
    expect(overviewTab).toHaveClass('border-primary-500', 'text-primary-600');
    
    // Switch to Portfolio tab
    await user.click(screen.getByText('Portfolio'));
    const portfolioTab = screen.getByText('Portfolio').closest('button');
    expect(portfolioTab).toHaveClass('border-primary-500', 'text-primary-600');
  });
});