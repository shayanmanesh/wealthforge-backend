import React, { useState, useEffect } from 'react';
import { Loader2, AlertCircle, CheckCircle, TrendingUp, BarChart3, Users, Zap } from 'lucide-react';
import ClientProfileForm from './ClientProfileForm';
import AnalysisResults from './AnalysisResults';
import { WealthForgeAPI, ClientProfile, CompleteAnalysis, HealthStatus } from '../services/api';

interface DashboardState {
  step: 'form' | 'analysis' | 'results';
  isLoading: boolean;
  error: string | null;
  clientProfile: ClientProfile | null;
  analysisResults: CompleteAnalysis | null;
  healthStatus: HealthStatus | null;
}

const WealthForgeDashboard: React.FC = () => {
  const [state, setState] = useState<DashboardState>({
    step: 'form',
    isLoading: false,
    error: null,
    clientProfile: null,
    analysisResults: null,
    healthStatus: null,
  });

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await WealthForgeAPI.getHealth();
        setState((prev) => ({ ...prev, healthStatus: health }));
      } catch (error) {
        console.warn('Health check failed:', error);
        setState((prev) => ({
          ...prev,
          healthStatus: { api: 'error', redis: 'error', kafka: 'error', timestamp: new Date().toISOString() },
        }));
      }
    };

    checkHealth();
  }, []);

  const handleFormSubmit = async (clientProfile: ClientProfile) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null, clientProfile }));

    try {
      setState((prev) => ({ ...prev, step: 'analysis' }));

      // Run complete analysis
      const result = await WealthForgeAPI.runCompleteAnalysis(clientProfile);

      setState((prev) => ({
        ...prev,
        isLoading: false,
        step: 'results',
        analysisResults: result.complete_analysis,
      }));
    } catch (error: any) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error?.response?.data?.detail || error?.message || 'Analysis failed. Please try again.',
        step: 'form',
      }));
    }
  };

  const handleStartOver = () => {
    setState({
      step: 'form',
      isLoading: false,
      error: null,
      clientProfile: null,
      analysisResults: null,
      healthStatus: state.healthStatus, // Keep health status
    });
  };

  const getHealthStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'connected':
        return 'text-success-600';
      case 'disconnected':
        return 'text-warning-600';
      case 'error':
        return 'text-danger-600';
      default:
        return 'text-slate-600';
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 text-primary-600 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-slate-900">WealthForge</h1>
                <p className="text-sm text-slate-600">AI-Powered Investment Platform</p>
              </div>
            </div>

            {/* Health Status */}
            {state.healthStatus && (
              <div className="flex items-center space-x-4 text-sm">
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-2 ${getHealthStatusColor(state.healthStatus.api)}`}></div>
                  <span className="text-slate-600">API</span>
                </div>
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-2 ${getHealthStatusColor(state.healthStatus.redis)}`}></div>
                  <span className="text-slate-600">Cache</span>
                </div>
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-2 ${getHealthStatusColor(state.healthStatus.kafka)}`}></div>
                  <span className="text-slate-600">Queue</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-8">
            <div className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  state.step === 'form'
                    ? 'bg-primary-600 text-white'
                    : state.step === 'analysis' || state.step === 'results'
                    ? 'bg-success-600 text-white'
                    : 'bg-slate-200 text-slate-600'
                }`}
              >
                {state.step === 'form' ? (
                  '1'
                ) : state.step === 'analysis' || state.step === 'results' ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  '1'
                )}
              </div>
              <span className="ml-2 text-sm font-medium text-slate-700">Client Profile</span>
            </div>

            <div className="w-16 h-0.5 bg-slate-300"></div>

            <div className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  state.step === 'analysis'
                    ? 'bg-primary-600 text-white'
                    : state.step === 'results'
                    ? 'bg-success-600 text-white'
                    : 'bg-slate-200 text-slate-600'
                }`}
              >
                {state.step === 'analysis' ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : state.step === 'results' ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  '2'
                )}
              </div>
              <span className="ml-2 text-sm font-medium text-slate-700">AI Analysis</span>
            </div>

            <div className="w-16 h-0.5 bg-slate-300"></div>

            <div className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  state.step === 'results'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-200 text-slate-600'
                }`}
              >
                {state.step === 'results' ? <BarChart3 className="w-5 h-5" /> : '3'}
              </div>
              <span className="ml-2 text-sm font-medium text-slate-700">Results</span>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {state.error && (
          <div className="mb-8">
            <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-danger-600 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <h3 className="text-sm font-medium text-danger-800">Analysis Error</h3>
                  <p className="text-sm text-danger-700 mt-1">{state.error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Form Step */}
        {state.step === 'form' && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-slate-900 mb-4">Complete Investment Analysis</h2>
              <p className="text-lg text-slate-600 max-w-3xl mx-auto">
                Get personalized investment recommendations powered by 50+ AI agents, advanced optimization algorithms,
                and comprehensive compliance analysis.
              </p>
            </div>

            {/* Features Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="card text-center">
                <div className="card-body">
                  <Users className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">50+ AI Agents</h3>
                  <p className="text-sm text-slate-600">
                    Specialized financial experts compete to generate optimal investment strategies
                  </p>
                </div>
              </div>
              <div className="card text-center">
                <div className="card-body">
                  <TrendingUp className="w-12 h-12 text-success-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Pareto Optimization</h3>
                  <p className="text-sm text-slate-600">
                    Advanced multi-objective optimization balancing return, risk, and cost
                  </p>
                </div>
              </div>
              <div className="card text-center">
                <div className="card-body">
                  <Zap className="w-12 h-12 text-warning-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-slate-900 mb-2">Goal Optimization</h3>
                  <p className="text-sm text-slate-600">
                    Fine-tune constraints to exceed financial goals with Monte Carlo analysis
                  </p>
                </div>
              </div>
            </div>

            <ClientProfileForm onSubmit={handleFormSubmit} isLoading={state.isLoading} />
          </div>
        )}

        {/* Analysis Step */}
        {state.step === 'analysis' && (
          <div className="text-center py-16">
            <div className="max-w-2xl mx-auto">
              <Loader2 className="w-16 h-16 text-primary-600 mx-auto mb-6 animate-spin" />
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Running WealthForge Analysis</h2>
              <p className="text-lg text-slate-600 mb-8">
                Our AI agents are analyzing your profile and generating personalized investment recommendations...
              </p>

              {/* Analysis Steps */}
              <div className="space-y-4 text-left bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-success-600 mr-3" />
                  <span className="text-sm text-slate-700">Parsing goals and constraints</span>
                </div>
                <div className="flex items-center">
                  <Loader2 className="w-5 h-5 text-primary-600 mr-3 animate-spin" />
                  <span className="text-sm text-slate-700">50 agents generating strategies</span>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-slate-200 mr-3"></div>
                  <span className="text-sm text-slate-500">Portfolio synthesis and optimization</span>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-slate-200 mr-3"></div>
                  <span className="text-sm text-slate-500">Compliance audit and validation</span>
                </div>
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-slate-200 mr-3"></div>
                  <span className="text-sm text-slate-500">Fine-tuning and goal optimization</span>
                </div>
              </div>

              <p className="text-sm text-slate-500 mt-6">
                This process typically takes 30-60 seconds. Please wait while we generate your personalized analysis.
              </p>
            </div>
          </div>
        )}

        {/* Results Step */}
        {state.step === 'results' && state.analysisResults && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Your Investment Analysis</h2>
                <p className="text-slate-600">Comprehensive AI-powered investment recommendations</p>
              </div>
              <button onClick={handleStartOver} className="btn-secondary">
                New Analysis
              </button>
            </div>

            <AnalysisResults analysis={state.analysisResults} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <TrendingUp className="w-6 h-6 text-primary-600 mr-2" />
              <span className="text-sm text-slate-600">
                WealthForge v1.0.0 - AI-Powered Investment Platform
              </span>
            </div>
            <div className="text-sm text-slate-500">
              Powered by FastAPI, React, and Advanced AI Optimization
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default WealthForgeDashboard;