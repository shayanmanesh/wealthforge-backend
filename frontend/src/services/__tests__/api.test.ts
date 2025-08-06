import axios from 'axios';
import { WealthForgeAPI, formatCurrency, formatPercentage, formatNumber, getStatusColor } from '../api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock axios.create
const mockAxiosInstance = {
  get: jest.fn(),
  post: jest.fn(),
  interceptors: {
    request: { use: jest.fn() },
    response: { use: jest.fn() },
  },
};

mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

describe('WealthForgeAPI', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Health API', () => {
    it('calls health endpoint correctly', async () => {
      const mockHealthResponse = {
        data: {
          data: {
            api: 'healthy',
            redis: 'connected',
            kafka: 'connected',
            timestamp: '2024-01-01T00:00:00Z',
          },
        },
      };

      mockAxiosInstance.get.mockResolvedValue(mockHealthResponse);

      const result = await WealthForgeAPI.getHealth();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/health');
      expect(result).toEqual(mockHealthResponse.data.data);
    });

    it('calls root endpoint correctly', async () => {
      const mockRootResponse = {
        data: {
          data: {
            message: 'WealthForge API v1.0.0',
            status: 'operational',
          },
        },
      };

      mockAxiosInstance.get.mockResolvedValue(mockRootResponse);

      const result = await WealthForgeAPI.getRoot();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/');
      expect(result).toEqual(mockRootResponse.data.data);
    });
  });

  describe('Core Component APIs', () => {
    const mockClientProfile = {
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
    };

    it('calls parse goals endpoint correctly', async () => {
      const mockParseResponse = {
        data: {
          data: {
            status: 'success',
            parsed_data: mockClientProfile,
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockParseResponse);

      const result = await WealthForgeAPI.parseGoals(mockClientProfile);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/parse-goals', mockClientProfile);
      expect(result).toEqual(mockParseResponse.data.data);
    });

    it('calls strategy optimization endpoint correctly', async () => {
      const mockStrategyResponse = {
        data: {
          data: {
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
            optimization_timestamp: '2024-01-01T00:00:00Z',
            user_id: 'user-123',
            num_agents_used: 50,
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockStrategyResponse);

      const result = await WealthForgeAPI.runStrategyOptimization(mockClientProfile, 50, 'balanced');

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/strategy-optimization', {
        client_profile: mockClientProfile,
        num_agents: 50,
        strategy_focus: 'balanced',
      });
      expect(result).toEqual(mockStrategyResponse.data.data);
    });

    it('calls portfolio synthesis endpoint correctly', async () => {
      const mockPortfolioResponse = {
        data: {
          data: {
            synthesis_result: {
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
              contributing_agents: ['GrowthOptimizer-47'],
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
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockPortfolioResponse);

      const result = await WealthForgeAPI.synthesizePortfolio(mockClientProfile, 100000, true);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/portfolio-synthesis', {
        client_profile: mockClientProfile,
        portfolio_value: 100000,
        use_real_data: true,
      });
      expect(result).toEqual(mockPortfolioResponse.data.data);
    });

    it('calls compliance audit endpoint correctly', async () => {
      const mockComplianceResponse = {
        data: {
          data: {
            audit_report: {
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
                applicable_regulations: ['Regulation BI'],
                suitability_assessment: {},
              },
              violations: [],
              recommendations: [],
            },
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockComplianceResponse);

      const result = await WealthForgeAPI.auditCompliance(mockClientProfile, 'portfolio-001');

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/compliance-audit', {
        client_profile: mockClientProfile,
        portfolio_id: 'portfolio-001',
      });
      expect(result).toEqual(mockComplianceResponse.data.data);
    });

    it('calls optimization endpoint correctly', async () => {
      const mockOptimizationResponse = {
        data: {
          data: {
            optimization_result: {
              optimization_id: 'opt-001',
              original_goal_probability: 0.65,
              optimized_goal_probability: 0.82,
              improvement_factor: 1.26,
              recommended_scenarios: [],
              sensitivity_analysis: {},
              implementation_roadmap: 'Test roadmap',
              risk_assessment: {},
            },
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockOptimizationResponse);

      const result = await WealthForgeAPI.optimizeConstraints(mockClientProfile, 0.25, 'balanced', 'portfolio-001');

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/fine-tuning', {
        client_profile: mockClientProfile,
        target_exceedance: 0.25,
        strategy: 'balanced',
        portfolio_id: 'portfolio-001',
      });
      expect(result).toEqual(mockOptimizationResponse.data.data);
    });

    it('calls complete analysis endpoint correctly', async () => {
      const mockCompleteResponse = {
        data: {
          data: {
            complete_analysis: {
              client_profile: mockClientProfile,
              arena_result: {},
              portfolio_synthesis: {},
              compliance_audit: {},
              optimization: {},
            },
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockCompleteResponse);

      const result = await WealthForgeAPI.runCompleteAnalysis(mockClientProfile);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/complete-analysis', mockClientProfile);
      expect(result).toEqual(mockCompleteResponse.data.data);
    });
  });

  describe('External Data APIs', () => {
    it('calls market data endpoint correctly', async () => {
      const mockMarketResponse = {
        data: {
          data: {
            market_data: {
              AAPL: {
                symbol: 'AAPL',
                count: 10,
                results: [
                  {
                    timestamp: '2024-01-01',
                    open: 150,
                    high: 155,
                    low: 148,
                    close: 153,
                    volume: 1000000,
                  },
                ],
                status: 'OK',
              },
            },
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockMarketResponse);

      const result = await WealthForgeAPI.getMarketData(['AAPL', 'SPY'], 'day', 100);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/market-data', {
        symbols: ['AAPL', 'SPY'],
        timespan: 'day',
        limit: 100,
      });
      expect(result).toEqual(mockMarketResponse.data.data);
    });

    it('calls economic data endpoint correctly', async () => {
      const mockEconomicResponse = {
        data: {
          data: {
            economic_data: {
              series_id: 'GDP',
              count: 5,
              observations: [
                { date: '2024-01-01', value: '25000' },
                { date: '2024-02-01', value: '25100' },
              ],
              status: 'OK',
              units: 'Billions of Dollars',
            },
          },
        },
      };

      mockAxiosInstance.post.mockResolvedValue(mockEconomicResponse);

      const result = await WealthForgeAPI.getEconomicData('GDP', '2024-01-01', '2024-12-31');

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/api/v1/economic-data', {
        series_id: 'GDP',
        start_date: '2024-01-01',
        end_date: '2024-12-31',
      });
      expect(result).toEqual(mockMarketResponse.data.data);
    });
  });

  describe('Error Handling', () => {
    it('handles API errors correctly', async () => {
      const mockError = {
        response: {
          data: {
            detail: 'Validation error',
          },
          status: 422,
        },
      };

      mockAxiosInstance.get.mockRejectedValue(mockError);

      await expect(WealthForgeAPI.getHealth()).rejects.toEqual(mockError);
    });

    it('handles network errors correctly', async () => {
      const networkError = new Error('Network Error');
      mockAxiosInstance.get.mockRejectedValue(networkError);

      await expect(WealthForgeAPI.getHealth()).rejects.toEqual(networkError);
    });
  });
});

describe('Utility Functions', () => {
  describe('formatCurrency', () => {
    it('formats currency correctly', () => {
      expect(formatCurrency(1000)).toBe('$1,000');
      expect(formatCurrency(1000000)).toBe('$1,000,000');
      expect(formatCurrency(1234.56)).toBe('$1,235');
      expect(formatCurrency(0)).toBe('$0');
    });

    it('handles negative values', () => {
      expect(formatCurrency(-1000)).toBe('-$1,000');
    });
  });

  describe('formatPercentage', () => {
    it('formats percentage correctly', () => {
      expect(formatPercentage(0.1)).toBe('10.0%');
      expect(formatPercentage(0.855)).toBe('85.5%');
      expect(formatPercentage(1.0)).toBe('100.0%');
      expect(formatPercentage(0)).toBe('0.0%');
    });

    it('handles custom decimal places', () => {
      expect(formatPercentage(0.1234, 2)).toBe('12.34%');
      expect(formatPercentage(0.1234, 0)).toBe('12%');
      expect(formatPercentage(0.1234, 3)).toBe('12.340%');
    });

    it('handles negative percentages', () => {
      expect(formatPercentage(-0.05)).toBe('-5.0%');
    });
  });

  describe('formatNumber', () => {
    it('formats numbers correctly', () => {
      expect(formatNumber(1000)).toBe('1,000');
      expect(formatNumber(1234.56)).toBe('1,235');
      expect(formatNumber(1234.56, 2)).toBe('1,234.56');
      expect(formatNumber(0)).toBe('0');
    });

    it('handles custom decimal places', () => {
      expect(formatNumber(1234.5678, 1)).toBe('1,234.6');
      expect(formatNumber(1234.5678, 3)).toBe('1,234.568');
    });

    it('handles negative numbers', () => {
      expect(formatNumber(-1000)).toBe('-1,000');
      expect(formatNumber(-1234.56, 2)).toBe('-1,234.56');
    });
  });

  describe('getStatusColor', () => {
    it('returns correct colors for compliant statuses', () => {
      expect(getStatusColor('compliant')).toBe('status-success');
      expect(getStatusColor('healthy')).toBe('status-success');
      expect(getStatusColor('connected')).toBe('status-success');
      expect(getStatusColor('success')).toBe('status-success');
    });

    it('returns correct colors for warning statuses', () => {
      expect(getStatusColor('warning')).toBe('status-warning');
      expect(getStatusColor('moderate')).toBe('status-warning');
    });

    it('returns correct colors for danger statuses', () => {
      expect(getStatusColor('violation')).toBe('status-danger');
      expect(getStatusColor('failed')).toBe('status-danger');
      expect(getStatusColor('high')).toBe('status-danger');
      expect(getStatusColor('error')).toBe('status-danger');
    });

    it('returns default color for unknown statuses', () => {
      expect(getStatusColor('unknown')).toBe('status-warning');
      expect(getStatusColor('pending')).toBe('status-warning');
      expect(getStatusColor('')).toBe('status-warning');
    });

    it('handles case insensitive input', () => {
      expect(getStatusColor('COMPLIANT')).toBe('status-success');
      expect(getStatusColor('Warning')).toBe('status-warning');
      expect(getStatusColor('ERROR')).toBe('status-danger');
    });
  });
});

describe('API Configuration', () => {
  it('creates axios instance with correct configuration', () => {
    expect(mockedAxios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000',
      headers: {
        'Authorization': 'Bearer demo-api-token',
        'Content-Type': 'application/json',
      },
      timeout: 120000,
    });
  });

  it('sets up request and response interceptors', () => {
    expect(mockAxiosInstance.interceptors.request.use).toHaveBeenCalled();
    expect(mockAxiosInstance.interceptors.response.use).toHaveBeenCalled();
  });
});