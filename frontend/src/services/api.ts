import axios, { AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_TOKEN = process.env.REACT_APP_API_TOKEN || 'demo-api-token';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`,
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes timeout for complex operations
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Type definitions
export interface ClientProfile {
  goals: {
    strategy: string;
    timeline: string;
    target_amount: number;
    risk_tolerance: string;
    secondary_goals?: string[];
  };
  constraints: {
    capital: number;
    contributions: number;
    contribution_frequency: string;
    max_risk_percentage: number;
    liquidity_needs?: string;
    monthly_expenses?: number;
    tax_optimization_priority?: string;
  };
  additional_preferences?: {
    age: number;
    ira_contributions?: number;
    '401k_contributions'?: number;
    esg_investing?: boolean;
    sector_focus?: string[];
    international_exposure?: string;
    alternative_investments?: boolean;
    impact_investing?: boolean;
  };
  financial_info?: {
    annual_income: number;
    net_worth: number;
    liquid_assets?: number;
    investment_experience?: string;
    risk_capacity?: string;
    time_horizon?: string;
  };
}

export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  execution_time?: number;
  timestamp: string;
}

export interface HealthStatus {
  api: string;
  redis: string;
  kafka: string;
  timestamp: string;
}

export interface StrategyOptimizationResult {
  arena_result: {
    strategies_generated: number;
    winner: {
      agent_name: string;
      agent_role: string;
      alpha_score: number;
    };
    execution_time: number;
    top_strategies: any[];
  };
  optimization_timestamp: string;
  user_id: string;
  num_agents_used: number;
}

export interface PortfolioSynthesis {
  portfolio_id: string;
  final_allocation: Record<string, number>;
  expected_return: number;
  risk_score: number;
  sharpe_ratio: number;
  synthesis_confidence: number;
  contributing_agents: string[];
  optimization_method: string;
  risk_analysis: {
    volatility: number;
    var_95: number;
    max_drawdown: number;
    beta: number;
  };
  cost_analysis: {
    total_expense_ratio: number;
    tax_efficiency_score: number;
    fee_optimization_savings: number;
  };
}

export interface ComplianceAudit {
  audit_id: string;
  overall_compliance: string;
  audit_score: number;
  requires_manual_review: boolean;
  capital_validation: {
    compliance_status: string;
    total_capital: number;
    investment_capital: number;
    warnings: string[];
  };
  contribution_validation: {
    compliance_status: string;
    ira_contributions: number;
    ira_limit: number;
    violations: string[];
  };
  regulatory_analysis: {
    client_classification: string;
    regulatory_risk_score: number;
    applicable_regulations: string[];
    suitability_assessment: Record<string, any>;
  };
  violations: Array<{
    violation_id: string;
    severity: string;
    description: string;
    recommendation: string;
  }>;
  recommendations: string[];
}

export interface OptimizationResult {
  optimization_id: string;
  original_goal_probability: number;
  optimized_goal_probability: number;
  improvement_factor: number;
  recommended_scenarios: Array<{
    scenario_id: string;
    scenario_name: string;
    probability_of_success: number;
    excess_achievement: number;
    implementation_score: number;
    time_to_goal: number;
    adjustments: Array<{
      adjustment_type: string;
      description: string;
      current_value: number;
      suggested_value: number;
      impact_magnitude: number;
      implementation_difficulty: number;
    }>;
  }>;
  sensitivity_analysis: Record<string, {
    sensitivity_coefficient: number;
    elasticity: number;
    critical_threshold?: number;
    risk_factors: string[];
  }>;
  implementation_roadmap: string;
  risk_assessment: Record<string, any>;
}

export interface MarketData {
  symbol: string;
  count: number;
  results: Array<{
    timestamp: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  }>;
  status: string;
  request_id?: string;
}

export interface EconomicData {
  series_id: string;
  count: number;
  observations: Array<{
    date: string;
    value: string;
  }>;
  status: string;
  units: string;
}

export interface CompleteAnalysis {
  client_profile: ClientProfile;
  arena_result: StrategyOptimizationResult['arena_result'];
  portfolio_synthesis: PortfolioSynthesis;
  compliance_audit: ComplianceAudit;
  optimization: OptimizationResult;
}

// API Service Class
export class WealthForgeAPI {
  // Health and system endpoints
  static async getHealth(): Promise<HealthStatus> {
    const response: AxiosResponse<APIResponse<HealthStatus>> = await apiClient.get('/health');
    return response.data.data!;
  }

  static async getRoot(): Promise<any> {
    const response: AxiosResponse<APIResponse> = await apiClient.get('/');
    return response.data.data;
  }

  // Core WealthForge component endpoints
  static async parseGoals(clientProfile: ClientProfile): Promise<any> {
    const response: AxiosResponse<APIResponse> = await apiClient.post('/api/v1/parse-goals', clientProfile);
    return response.data.data;
  }

  static async runStrategyOptimization(
    clientProfile: ClientProfile,
    numAgents: number = 50,
    strategyFocus: string = 'balanced'
  ): Promise<StrategyOptimizationResult> {
    const response: AxiosResponse<APIResponse<StrategyOptimizationResult>> = await apiClient.post(
      '/api/v1/strategy-optimization',
      {
        client_profile: clientProfile,
        num_agents: numAgents,
        strategy_focus: strategyFocus,
      }
    );
    return response.data.data!;
  }

  static async synthesizePortfolio(
    clientProfile: ClientProfile,
    portfolioValue: number,
    useRealData: boolean = true
  ): Promise<{ synthesis_result: PortfolioSynthesis }> {
    const response: AxiosResponse<APIResponse<{ synthesis_result: PortfolioSynthesis }>> = await apiClient.post(
      '/api/v1/portfolio-synthesis',
      {
        client_profile: clientProfile,
        portfolio_value: portfolioValue,
        use_real_data: useRealData,
      }
    );
    return response.data.data!;
  }

  static async auditCompliance(
    clientProfile: ClientProfile,
    portfolioId?: string
  ): Promise<{ audit_report: ComplianceAudit }> {
    const response: AxiosResponse<APIResponse<{ audit_report: ComplianceAudit }>> = await apiClient.post(
      '/api/v1/compliance-audit',
      {
        client_profile: clientProfile,
        portfolio_id: portfolioId,
      }
    );
    return response.data.data!;
  }

  static async optimizeConstraints(
    clientProfile: ClientProfile,
    targetExceedance: number = 0.25,
    strategy: string = 'balanced',
    portfolioId?: string
  ): Promise<{ optimization_result: OptimizationResult }> {
    const response: AxiosResponse<APIResponse<{ optimization_result: OptimizationResult }>> = await apiClient.post(
      '/api/v1/fine-tuning',
      {
        client_profile: clientProfile,
        target_exceedance: targetExceedance,
        strategy,
        portfolio_id: portfolioId,
      }
    );
    return response.data.data!;
  }

  static async runCompleteAnalysis(clientProfile: ClientProfile): Promise<{ complete_analysis: CompleteAnalysis }> {
    const response: AxiosResponse<APIResponse<{ complete_analysis: CompleteAnalysis }>> = await apiClient.post(
      '/api/v1/complete-analysis',
      clientProfile
    );
    return response.data.data!;
  }

  // External data endpoints
  static async getMarketData(
    symbols: string[],
    timespan: string = 'day',
    limit: number = 100
  ): Promise<{ market_data: Record<string, MarketData> }> {
    const response: AxiosResponse<APIResponse<{ market_data: Record<string, MarketData> }>> = await apiClient.post(
      '/api/v1/market-data',
      {
        symbols,
        timespan,
        limit,
      }
    );
    return response.data.data!;
  }

  static async getEconomicData(
    seriesId: string,
    startDate?: string,
    endDate?: string
  ): Promise<{ economic_data: EconomicData }> {
    const response: AxiosResponse<APIResponse<{ economic_data: EconomicData }>> = await apiClient.post(
      '/api/v1/economic-data',
      {
        series_id: seriesId,
        start_date: startDate,
        end_date: endDate,
      }
    );
    return response.data.data!;
  }
}

// Utility functions
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatPercentage = (value: number, decimals: number = 1): string => {
  return `${(value * 100).toFixed(decimals)}%`;
};

export const formatNumber = (value: number, decimals: number = 0): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

export const getStatusColor = (status: string): string => {
  switch (status.toLowerCase()) {
    case 'compliant':
    case 'healthy':
    case 'connected':
    case 'success':
      return 'status-success';
    case 'warning':
    case 'moderate':
      return 'status-warning';
    case 'violation':
    case 'failed':
    case 'high':
    case 'error':
      return 'status-danger';
    default:
      return 'status-warning';
  }
};

export default WealthForgeAPI;