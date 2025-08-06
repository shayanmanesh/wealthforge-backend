import React, { useState } from 'react';
import {
  TrendingUp,
  Shield,
  DollarSign,
  BarChart3,
  AlertTriangle,
  CheckCircle,
  Target,
  Settings,
  PieChart,
  Activity,
  Info,
  ExternalLink,
} from 'lucide-react';
import {
  LineChart,
  Line,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  CompleteAnalysis,
  PortfolioSynthesis,
  ComplianceAudit,
  OptimizationResult,
  formatCurrency,
  formatPercentage,
  formatNumber,
  getStatusColor,
} from '../services/api';

interface AnalysisResultsProps {
  analysis: CompleteAnalysis;
  isLoading?: boolean;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis, isLoading = false }) => {
  const [activeTab, setActiveTab] = useState('overview');

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-slate-200 rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-32 bg-slate-200 rounded-lg"></div>
            ))}
          </div>
          <div className="h-64 bg-slate-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'portfolio', label: 'Portfolio', icon: PieChart },
    { id: 'compliance', label: 'Compliance', icon: Shield },
    { id: 'optimization', label: 'Optimization', icon: TrendingUp },
  ];

  // Prepare chart data
  const allocationData = Object.entries(analysis.portfolio_synthesis.final_allocation).map(([asset, weight]) => ({
    name: asset,
    value: weight * 100,
    amount: analysis.client_profile.constraints.capital * weight,
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'];

  const optimizationScenarios = analysis.optimization.recommended_scenarios.slice(0, 3).map((scenario, index) => ({
    name: scenario.scenario_name,
    success: scenario.probability_of_success * 100,
    implementation: scenario.implementation_score * 100,
    excess: scenario.excess_achievement * 100,
  }));

  const riskMetrics = [
    { name: 'Volatility', value: analysis.portfolio_synthesis.risk_analysis.volatility * 100 },
    { name: 'VaR (95%)', value: Math.abs(analysis.portfolio_synthesis.risk_analysis.var_95) * 100 },
    { name: 'Max Drawdown', value: analysis.portfolio_synthesis.risk_analysis.max_drawdown * 100 },
    { name: 'Beta', value: analysis.portfolio_synthesis.risk_analysis.beta },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-2">WealthForge Analysis Results</h2>
        <p className="text-slate-600">
          Comprehensive investment analysis powered by AI agents and advanced optimization
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-slate-200 mb-8">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                }`}
              >
                <Icon className="w-5 h-5 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Expected Return</p>
                  <p className="text-2xl font-bold text-success-600">
                    {formatPercentage(analysis.portfolio_synthesis.expected_return)}
                  </p>
                </div>
                <TrendingUp className="w-8 h-8 text-success-600" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Risk Score</p>
                  <p className="text-2xl font-bold text-warning-600">
                    {formatPercentage(analysis.portfolio_synthesis.risk_score)}
                  </p>
                </div>
                <Shield className="w-8 h-8 text-warning-600" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Sharpe Ratio</p>
                  <p className="text-2xl font-bold text-primary-600">
                    {formatNumber(analysis.portfolio_synthesis.sharpe_ratio, 2)}
                  </p>
                </div>
                <Activity className="w-8 h-8 text-primary-600" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Compliance Score</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {formatNumber(analysis.compliance_audit.audit_score)}
                  </p>
                </div>
                <CheckCircle className="w-8 h-8 text-success-600" />
              </div>
            </div>
          </div>

          {/* Strategy Winner */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <Target className="w-5 h-5 mr-2 text-primary-600" />
                Winning Strategy
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Agent Name</p>
                  <p className="text-xl font-semibold text-slate-900">
                    {analysis.arena_result.winner.agent_name}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Agent Role</p>
                  <p className="text-lg text-slate-700">{analysis.arena_result.winner.agent_role}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Alpha Score</p>
                  <p className="text-lg font-semibold text-primary-600">
                    {formatNumber(analysis.arena_result.winner.alpha_score, 4)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Optimization Improvement */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-success-600" />
                Goal Achievement Improvement
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Original Probability</p>
                  <p className="text-2xl font-bold text-slate-600">
                    {formatPercentage(analysis.optimization.original_goal_probability)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Optimized Probability</p>
                  <p className="text-2xl font-bold text-success-600">
                    {formatPercentage(analysis.optimization.optimized_goal_probability)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Improvement Factor</p>
                  <p className="text-2xl font-bold text-primary-600">
                    {formatNumber(analysis.optimization.improvement_factor, 2)}x
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Portfolio Tab */}
      {activeTab === 'portfolio' && (
        <div className="space-y-8">
          {/* Asset Allocation Chart */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <PieChart className="w-5 h-5 mr-2 text-primary-600" />
                Asset Allocation
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsPieChart>
                      <Pie
                        data={allocationData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                      >
                        {allocationData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => `${Number(value).toFixed(1)}%`} />
                    </RechartsPieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-4">
                  <h4 className="font-medium text-slate-900">Allocation Breakdown</h4>
                  {allocationData.map((item, index) => (
                    <div key={item.name} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div
                          className="w-4 h-4 rounded mr-3"
                          style={{ backgroundColor: COLORS[index % COLORS.length] }}
                        ></div>
                        <span className="text-sm text-slate-700">{item.name}</span>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium text-slate-900">
                          {formatCurrency(item.amount)}
                        </div>
                        <div className="text-xs text-slate-500">{item.value.toFixed(1)}%</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Risk Analysis */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <Shield className="w-5 h-5 mr-2 text-warning-600" />
                Risk Analysis
              </h3>
            </div>
            <div className="card-body">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={riskMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => `${Number(value).toFixed(2)}${value < 5 ? '' : '%'}`} />
                    <Bar dataKey="value" fill="#f59e0b" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Cost Analysis */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <DollarSign className="w-5 h-5 mr-2 text-success-600" />
                Cost Analysis
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Total Expense Ratio</p>
                  <p className="text-xl font-semibold text-slate-900">
                    {formatPercentage(analysis.portfolio_synthesis.cost_analysis.total_expense_ratio, 3)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Tax Efficiency Score</p>
                  <p className="text-xl font-semibold text-success-600">
                    {formatPercentage(analysis.portfolio_synthesis.cost_analysis.tax_efficiency_score)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Fee Optimization Savings</p>
                  <p className="text-xl font-semibold text-primary-600">
                    {formatPercentage(analysis.portfolio_synthesis.cost_analysis.fee_optimization_savings, 3)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Compliance Tab */}
      {activeTab === 'compliance' && (
        <div className="space-y-8">
          {/* Compliance Overview */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <Shield className="w-5 h-5 mr-2 text-primary-600" />
                Compliance Overview
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Overall Compliance</p>
                  <span
                    className={`status-badge ${getStatusColor(analysis.compliance_audit.overall_compliance)}`}
                  >
                    {analysis.compliance_audit.overall_compliance.toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Audit Score</p>
                  <p className="text-xl font-semibold text-slate-900">
                    {formatNumber(analysis.compliance_audit.audit_score)}/100
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Manual Review Required</p>
                  <span
                    className={`status-badge ${
                      analysis.compliance_audit.requires_manual_review ? 'status-warning' : 'status-success'
                    }`}
                  >
                    {analysis.compliance_audit.requires_manual_review ? 'YES' : 'NO'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Capital Validation */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900">Capital Validation</h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Status</p>
                  <span
                    className={`status-badge ${getStatusColor(
                      analysis.compliance_audit.capital_validation.compliance_status
                    )}`}
                  >
                    {analysis.compliance_audit.capital_validation.compliance_status.toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Total Capital</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatCurrency(analysis.compliance_audit.capital_validation.total_capital)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Investment Capital</p>
                  <p className="text-lg font-semibold text-success-600">
                    {formatCurrency(analysis.compliance_audit.capital_validation.investment_capital)}
                  </p>
                </div>
              </div>
              {analysis.compliance_audit.capital_validation.warnings.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-warning-800 mb-2">Warnings:</h4>
                  <ul className="space-y-1">
                    {analysis.compliance_audit.capital_validation.warnings.map((warning, index) => (
                      <li key={index} className="text-sm text-warning-700 flex items-start">
                        <AlertTriangle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                        {warning}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Violations */}
          {analysis.compliance_audit.violations.length > 0 && (
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-slate-900 text-danger-600">
                  Compliance Violations ({analysis.compliance_audit.violations.length})
                </h3>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  {analysis.compliance_audit.violations.map((violation) => (
                    <div key={violation.violation_id} className="border border-danger-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <span className={`status-badge ${getStatusColor(violation.severity)}`}>
                              {violation.severity.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-sm text-slate-900 font-medium mb-1">{violation.description}</p>
                          <p className="text-sm text-slate-600">{violation.recommendation}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Regulatory Analysis */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900">Regulatory Analysis</h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Client Classification</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {analysis.compliance_audit.regulatory_analysis.client_classification.replace(/_/g, ' ')}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Regulatory Risk Score</p>
                  <p className="text-lg font-semibold text-warning-600">
                    {formatNumber(analysis.compliance_audit.regulatory_analysis.regulatory_risk_score, 3)}
                  </p>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-sm text-slate-600 mb-2">Applicable Regulations:</p>
                <div className="flex flex-wrap gap-2">
                  {analysis.compliance_audit.regulatory_analysis.applicable_regulations.map((regulation) => (
                    <span key={regulation} className="status-badge status-success">
                      {regulation}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Optimization Tab */}
      {activeTab === 'optimization' && (
        <div className="space-y-8">
          {/* Optimization Overview */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-success-600" />
                Optimization Results
              </h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-slate-600">Original Goal Probability</p>
                  <p className="text-2xl font-bold text-slate-600">
                    {formatPercentage(analysis.optimization.original_goal_probability)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Optimized Probability</p>
                  <p className="text-2xl font-bold text-success-600">
                    {formatPercentage(analysis.optimization.optimized_goal_probability)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-600">Improvement Factor</p>
                  <p className="text-2xl font-bold text-primary-600">
                    {formatNumber(analysis.optimization.improvement_factor, 2)}x
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Recommended Scenarios */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <Settings className="w-5 h-5 mr-2 text-primary-600" />
                Recommended Scenarios
              </h3>
            </div>
            <div className="card-body">
              <div className="space-y-6">
                {analysis.optimization.recommended_scenarios.slice(0, 3).map((scenario, index) => (
                  <div key={scenario.scenario_id} className="border border-slate-200 rounded-lg p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h4 className="text-lg font-semibold text-slate-900">{scenario.scenario_name}</h4>
                        <p className="text-sm text-slate-600">Scenario {index + 1}</p>
                      </div>
                      <span className="status-badge status-success">
                        {formatPercentage(scenario.probability_of_success)} Success
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-slate-600">Success Probability</p>
                        <p className="text-lg font-semibold text-success-600">
                          {formatPercentage(scenario.probability_of_success)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-slate-600">Excess Achievement</p>
                        <p className="text-lg font-semibold text-primary-600">
                          {formatPercentage(scenario.excess_achievement)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-slate-600">Implementation Score</p>
                        <p className="text-lg font-semibold text-warning-600">
                          {formatPercentage(scenario.implementation_score)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-slate-600">Time to Goal</p>
                        <p className="text-lg font-semibold text-slate-900">
                          {formatNumber(scenario.time_to_goal, 1)} years
                        </p>
                      </div>
                    </div>

                    {/* Adjustments */}
                    <div>
                      <h5 className="text-sm font-medium text-slate-900 mb-3">Required Adjustments:</h5>
                      <div className="space-y-3">
                        {scenario.adjustments.map((adjustment, adjIndex) => (
                          <div key={adjIndex} className="bg-slate-50 rounded-lg p-4">
                            <div className="flex items-center justify-between mb-2">
                              <p className="text-sm font-medium text-slate-900">{adjustment.description}</p>
                              <span
                                className={`status-badge ${
                                  adjustment.implementation_difficulty < 0.5 ? 'status-success' : 'status-warning'
                                }`}
                              >
                                {adjustment.implementation_difficulty < 0.5 ? 'Easy' : 'Moderate'}
                              </span>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                              <div>
                                <span className="text-slate-600">Current:</span>
                                <span className="block font-medium">
                                  {adjustment.adjustment_type.includes('contribution') ||
                                  adjustment.adjustment_type.includes('capital')
                                    ? formatCurrency(adjustment.current_value)
                                    : formatNumber(adjustment.current_value)}
                                </span>
                              </div>
                              <div>
                                <span className="text-slate-600">Suggested:</span>
                                <span className="block font-medium text-primary-600">
                                  {adjustment.adjustment_type.includes('contribution') ||
                                  adjustment.adjustment_type.includes('capital')
                                    ? formatCurrency(adjustment.suggested_value)
                                    : formatNumber(adjustment.suggested_value)}
                                </span>
                              </div>
                              <div>
                                <span className="text-slate-600">Impact:</span>
                                <span className="block font-medium">
                                  {formatPercentage(adjustment.impact_magnitude)}
                                </span>
                              </div>
                              <div>
                                <span className="text-slate-600">Difficulty:</span>
                                <span className="block font-medium">
                                  {formatPercentage(adjustment.implementation_difficulty)}
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sensitivity Analysis */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
                Sensitivity Analysis
              </h3>
            </div>
            <div className="card-body">
              <div className="space-y-4">
                {Object.entries(analysis.optimization.sensitivity_analysis).map(([parameter, analysis]) => (
                  <div key={parameter} className="border border-slate-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-lg font-semibold text-slate-900 capitalize">{parameter}</h4>
                      <span className="text-sm text-slate-600">
                        Elasticity: {formatNumber(analysis.elasticity, 2)}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-slate-600">Sensitivity Coefficient</p>
                        <p className="text-lg font-semibold text-primary-600">
                          {formatNumber(analysis.sensitivity_coefficient, 4)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-slate-600">Elasticity</p>
                        <p className="text-lg font-semibold text-slate-900">
                          {formatNumber(analysis.elasticity, 2)}
                        </p>
                      </div>
                      {analysis.critical_threshold && (
                        <div>
                          <p className="text-sm text-slate-600">Critical Threshold</p>
                          <p className="text-lg font-semibold text-warning-600">
                            {formatNumber(analysis.critical_threshold, 2)}
                          </p>
                        </div>
                      )}
                    </div>
                    {analysis.risk_factors.length > 0 && (
                      <div className="mt-3">
                        <p className="text-sm text-slate-600 mb-2">Risk Factors:</p>
                        <div className="flex flex-wrap gap-2">
                          {analysis.risk_factors.map((factor, index) => (
                            <span key={index} className="status-badge status-warning">
                              {factor}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Implementation Roadmap */}
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                <Target className="w-5 h-5 mr-2 text-primary-600" />
                Implementation Roadmap
              </h3>
            </div>
            <div className="card-body">
              <div className="prose prose-slate max-w-none">
                <p className="text-slate-700 whitespace-pre-line">{analysis.optimization.implementation_roadmap}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;