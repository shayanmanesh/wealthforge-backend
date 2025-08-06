import React, { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { User, Target, DollarSign, Shield, Settings, Plus, Minus } from 'lucide-react';
import { ClientProfile } from '../services/api';

interface ClientProfileFormProps {
  onSubmit: (data: ClientProfile) => void;
  isLoading?: boolean;
  initialData?: Partial<ClientProfile>;
}

const ClientProfileForm: React.FC<ClientProfileFormProps> = ({
  onSubmit,
  isLoading = false,
  initialData = {},
}) => {
  const [activeTab, setActiveTab] = useState('goals');
  const [sectorFocus, setSectorFocus] = useState<string[]>(
    initialData.additional_preferences?.sector_focus || []
  );
  const [secondaryGoals, setSecondaryGoals] = useState<string[]>(
    initialData.goals?.secondary_goals || []
  );

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    watch,
    setValue,
  } = useForm<ClientProfile>({
    defaultValues: {
      goals: {
        strategy: 'balanced growth',
        timeline: '10 years',
        target_amount: 500000,
        risk_tolerance: 'moderate',
        secondary_goals: [],
        ...initialData.goals,
      },
      constraints: {
        capital: 100000,
        contributions: 2000,
        contribution_frequency: 'monthly',
        max_risk_percentage: 70,
        liquidity_needs: 'low',
        monthly_expenses: 5000,
        tax_optimization_priority: 'medium',
        ...initialData.constraints,
      },
      additional_preferences: {
        age: 35,
        ira_contributions: 6000,
        '401k_contributions': 18000,
        esg_investing: false,
        sector_focus: [],
        international_exposure: 'medium',
        alternative_investments: false,
        impact_investing: false,
        ...initialData.additional_preferences,
      },
      financial_info: {
        annual_income: 80000,
        net_worth: 200000,
        liquid_assets: 50000,
        investment_experience: 'intermediate',
        risk_capacity: 'high',
        time_horizon: 'long-term',
        ...initialData.financial_info,
      },
    },
  });

  const watchedCapital = watch('constraints.capital');
  const watchedIncome = watch('financial_info.annual_income');

  const tabs = [
    { id: 'goals', label: 'Goals & Objectives', icon: Target },
    { id: 'constraints', label: 'Constraints', icon: Shield },
    { id: 'preferences', label: 'Preferences', icon: Settings },
    { id: 'financial', label: 'Financial Info', icon: DollarSign },
  ];

  const addSectorFocus = (sector: string) => {
    if (sector && !sectorFocus.includes(sector)) {
      const newSectors = [...sectorFocus, sector];
      setSectorFocus(newSectors);
      setValue('additional_preferences.sector_focus', newSectors);
    }
  };

  const removeSectorFocus = (sector: string) => {
    const newSectors = sectorFocus.filter((s) => s !== sector);
    setSectorFocus(newSectors);
    setValue('additional_preferences.sector_focus', newSectors);
  };

  const addSecondaryGoal = (goal: string) => {
    if (goal && !secondaryGoals.includes(goal)) {
      const newGoals = [...secondaryGoals, goal];
      setSecondaryGoals(newGoals);
      setValue('goals.secondary_goals', newGoals);
    }
  };

  const removeSecondaryGoal = (goal: string) => {
    const newGoals = secondaryGoals.filter((g) => g !== goal);
    setSecondaryGoals(newGoals);
    setValue('goals.secondary_goals', newGoals);
  };

  const onFormSubmit = (data: ClientProfile) => {
    // Ensure arrays are properly set
    data.additional_preferences = {
      ...data.additional_preferences,
      sector_focus: sectorFocus,
    };
    data.goals = {
      ...data.goals,
      secondary_goals: secondaryGoals,
    };
    onSubmit(data);
  };

  const commonSectors = [
    'Technology',
    'Healthcare',
    'Financial Services',
    'Renewable Energy',
    'Real Estate',
    'Consumer Goods',
    'Industrial',
    'Biotechnology',
    'Artificial Intelligence',
    'Cybersecurity',
  ];

  const commonSecondaryGoals = [
    'Early Retirement',
    'Legacy Planning',
    'Philanthropic Giving',
    'Education Funding',
    'Home Purchase',
    'Emergency Fund',
    'Travel Fund',
    'Business Investment',
  ];

  return (
    <div className="max-w-4xl mx-auto">
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

      <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-8">
        {/* Goals & Objectives Tab */}
        {activeTab === 'goals' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                  <Target className="w-5 h-5 mr-2 text-primary-600" />
                  Investment Goals & Objectives
                </h3>
                <p className="text-sm text-slate-600 mt-1">
                  Define your primary investment strategy and financial targets
                </p>
              </div>
              <div className="card-body">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="form-group">
                    <label className="label-field">Investment Strategy</label>
                    <select
                      {...register('goals.strategy', { required: 'Strategy is required' })}
                      className="input-field"
                    >
                      <option value="conservative">Conservative</option>
                      <option value="balanced">Balanced</option>
                      <option value="balanced growth">Balanced Growth</option>
                      <option value="aggressive growth">Aggressive Growth</option>
                      <option value="income focused">Income Focused</option>
                      <option value="ESG focused">ESG Focused</option>
                    </select>
                    {errors.goals?.strategy && (
                      <p className="text-sm text-danger-600 mt-1">{errors.goals.strategy.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Investment Timeline</label>
                    <select
                      {...register('goals.timeline', { required: 'Timeline is required' })}
                      className="input-field"
                    >
                      <option value="3 years">3 Years</option>
                      <option value="5 years">5 Years</option>
                      <option value="10 years">10 Years</option>
                      <option value="15 years">15 Years</option>
                      <option value="20 years">20 Years</option>
                      <option value="25+ years">25+ Years</option>
                    </select>
                    {errors.goals?.timeline && (
                      <p className="text-sm text-danger-600 mt-1">{errors.goals.timeline.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Target Amount ($)</label>
                    <input
                      type="number"
                      {...register('goals.target_amount', {
                        required: 'Target amount is required',
                        min: { value: 1000, message: 'Minimum target is $1,000' },
                      })}
                      className="input-field"
                      placeholder="500000"
                    />
                    {errors.goals?.target_amount && (
                      <p className="text-sm text-danger-600 mt-1">{errors.goals.target_amount.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Risk Tolerance</label>
                    <select
                      {...register('goals.risk_tolerance', { required: 'Risk tolerance is required' })}
                      className="input-field"
                    >
                      <option value="very low">Very Low</option>
                      <option value="low">Low</option>
                      <option value="moderate">Moderate</option>
                      <option value="high">High</option>
                      <option value="very high">Very High</option>
                    </select>
                    {errors.goals?.risk_tolerance && (
                      <p className="text-sm text-danger-600 mt-1">{errors.goals.risk_tolerance.message}</p>
                    )}
                  </div>
                </div>

                {/* Secondary Goals */}
                <div className="form-group">
                  <label className="label-field">Secondary Goals (Optional)</label>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {secondaryGoals.map((goal) => (
                      <span
                        key={goal}
                        className="inline-flex items-center bg-primary-100 text-primary-800 text-sm px-3 py-1 rounded-full"
                      >
                        {goal}
                        <button
                          type="button"
                          onClick={() => removeSecondaryGoal(goal)}
                          className="ml-2 text-primary-600 hover:text-primary-800"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {commonSecondaryGoals
                      .filter((goal) => !secondaryGoals.includes(goal))
                      .map((goal) => (
                        <button
                          key={goal}
                          type="button"
                          onClick={() => addSecondaryGoal(goal)}
                          className="inline-flex items-center bg-slate-100 text-slate-700 text-sm px-3 py-1 rounded-full hover:bg-slate-200 transition-colors"
                        >
                          <Plus className="w-3 h-3 mr-1" />
                          {goal}
                        </button>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Constraints Tab */}
        {activeTab === 'constraints' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                  <Shield className="w-5 h-5 mr-2 text-primary-600" />
                  Financial Constraints
                </h3>
                <p className="text-sm text-slate-600 mt-1">
                  Set your investment limits and contribution capacity
                </p>
              </div>
              <div className="card-body">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="form-group">
                    <label className="label-field">Initial Capital ($)</label>
                    <input
                      type="number"
                      {...register('constraints.capital', {
                        required: 'Initial capital is required',
                        min: { value: 1000, message: 'Minimum capital is $1,000' },
                      })}
                      className="input-field"
                      placeholder="100000"
                    />
                    {errors.constraints?.capital && (
                      <p className="text-sm text-danger-600 mt-1">{errors.constraints.capital.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Monthly Contributions ($)</label>
                    <input
                      type="number"
                      {...register('constraints.contributions', {
                        required: 'Monthly contributions are required',
                        min: { value: 0, message: 'Cannot be negative' },
                      })}
                      className="input-field"
                      placeholder="2000"
                    />
                    {errors.constraints?.contributions && (
                      <p className="text-sm text-danger-600 mt-1">{errors.constraints.contributions.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Contribution Frequency</label>
                    <select {...register('constraints.contribution_frequency')} className="input-field">
                      <option value="monthly">Monthly</option>
                      <option value="quarterly">Quarterly</option>
                      <option value="annually">Annually</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="label-field">Maximum Risk Percentage (%)</label>
                    <input
                      type="number"
                      {...register('constraints.max_risk_percentage', {
                        required: 'Max risk percentage is required',
                        min: { value: 0, message: 'Cannot be negative' },
                        max: { value: 100, message: 'Cannot exceed 100%' },
                      })}
                      className="input-field"
                      placeholder="70"
                    />
                    {errors.constraints?.max_risk_percentage && (
                      <p className="text-sm text-danger-600 mt-1">
                        {errors.constraints.max_risk_percentage.message}
                      </p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Monthly Expenses ($)</label>
                    <input
                      type="number"
                      {...register('constraints.monthly_expenses')}
                      className="input-field"
                      placeholder="5000"
                    />
                  </div>

                  <div className="form-group">
                    <label className="label-field">Liquidity Needs</label>
                    <select {...register('constraints.liquidity_needs')} className="input-field">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>

                  <div className="form-group md:col-span-2">
                    <label className="label-field">Tax Optimization Priority</label>
                    <select {...register('constraints.tax_optimization_priority')} className="input-field">
                      <option value="low">Low Priority</option>
                      <option value="medium">Medium Priority</option>
                      <option value="high">High Priority</option>
                    </select>
                  </div>
                </div>

                {/* Capital Adequacy Indicator */}
                {watchedCapital && (
                  <div className="mt-6 p-4 bg-slate-50 rounded-lg">
                    <h4 className="text-sm font-medium text-slate-900 mb-2">Capital Adequacy Analysis</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-slate-600">Emergency Fund:</span>
                        <span className="block font-medium">
                          ${((watchedCapital * 0.15) || 0).toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Investment Capital:</span>
                        <span className="block font-medium">
                          ${((watchedCapital * 0.85) || 0).toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Annual Contribution:</span>
                        <span className="block font-medium">
                          ${((watch('constraints.contributions') || 0) * 12).toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Contribution Rate:</span>
                        <span className="block font-medium">
                          {watchedIncome
                            ? (((watch('constraints.contributions') || 0) * 12) / watchedIncome * 100).toFixed(1)
                            : 0}%
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                  <Settings className="w-5 h-5 mr-2 text-primary-600" />
                  Investment Preferences
                </h3>
                <p className="text-sm text-slate-600 mt-1">
                  Customize your investment approach and preferences
                </p>
              </div>
              <div className="card-body">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="form-group">
                    <label className="label-field">Age</label>
                    <input
                      type="number"
                      {...register('additional_preferences.age', {
                        min: { value: 18, message: 'Must be at least 18' },
                        max: { value: 100, message: 'Must be less than 100' },
                      })}
                      className="input-field"
                      placeholder="35"
                    />
                    {errors.additional_preferences?.age && (
                      <p className="text-sm text-danger-600 mt-1">{errors.additional_preferences.age.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">International Exposure</label>
                    <select {...register('additional_preferences.international_exposure')} className="input-field">
                      <option value="low">Low (0-10%)</option>
                      <option value="medium">Medium (10-30%)</option>
                      <option value="high">High (30%+)</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="label-field">Annual IRA Contributions ($)</label>
                    <input
                      type="number"
                      {...register('additional_preferences.ira_contributions')}
                      className="input-field"
                      placeholder="6000"
                    />
                  </div>

                  <div className="form-group">
                    <label className="label-field">Annual 401(k) Contributions ($)</label>
                    <input
                      type="number"
                      {...register('additional_preferences.401k_contributions')}
                      className="input-field"
                      placeholder="18000"
                    />
                  </div>
                </div>

                {/* Investment Preferences Checkboxes */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                  <div className="space-y-4">
                    <h4 className="text-sm font-medium text-slate-900">Investment Approaches</h4>
                    <label className="flex items-center">
                      <Controller
                        name="additional_preferences.esg_investing"
                        control={control}
                        render={({ field }) => (
                          <input
                            type="checkbox"
                            {...field}
                            value=""
                            checked={field.value}
                            className="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                          />
                        )}
                      />
                      <span className="ml-2 text-sm text-slate-700">ESG/Sustainable Investing</span>
                    </label>
                    <label className="flex items-center">
                      <Controller
                        name="additional_preferences.alternative_investments"
                        control={control}
                        render={({ field }) => (
                          <input
                            type="checkbox"
                            {...field}
                            value=""
                            checked={field.value}
                            className="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                          />
                        )}
                      />
                      <span className="ml-2 text-sm text-slate-700">Alternative Investments</span>
                    </label>
                    <label className="flex items-center">
                      <Controller
                        name="additional_preferences.impact_investing"
                        control={control}
                        render={({ field }) => (
                          <input
                            type="checkbox"
                            {...field}
                            value=""
                            checked={field.value}
                            className="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                          />
                        )}
                      />
                      <span className="ml-2 text-sm text-slate-700">Impact Investing</span>
                    </label>
                  </div>
                </div>

                {/* Sector Focus */}
                <div className="form-group">
                  <label className="label-field">Sector Focus (Optional)</label>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {sectorFocus.map((sector) => (
                      <span
                        key={sector}
                        className="inline-flex items-center bg-primary-100 text-primary-800 text-sm px-3 py-1 rounded-full"
                      >
                        {sector}
                        <button
                          type="button"
                          onClick={() => removeSectorFocus(sector)}
                          className="ml-2 text-primary-600 hover:text-primary-800"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {commonSectors
                      .filter((sector) => !sectorFocus.includes(sector))
                      .map((sector) => (
                        <button
                          key={sector}
                          type="button"
                          onClick={() => addSectorFocus(sector)}
                          className="inline-flex items-center bg-slate-100 text-slate-700 text-sm px-3 py-1 rounded-full hover:bg-slate-200 transition-colors"
                        >
                          <Plus className="w-3 h-3 mr-1" />
                          {sector}
                        </button>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Financial Info Tab */}
        {activeTab === 'financial' && (
          <div className="space-y-6">
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                  <DollarSign className="w-5 h-5 mr-2 text-primary-600" />
                  Financial Information
                </h3>
                <p className="text-sm text-slate-600 mt-1">
                  Provide details about your current financial situation
                </p>
              </div>
              <div className="card-body">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="form-group">
                    <label className="label-field">Annual Income ($)</label>
                    <input
                      type="number"
                      {...register('financial_info.annual_income', {
                        required: 'Annual income is required',
                        min: { value: 0, message: 'Cannot be negative' },
                      })}
                      className="input-field"
                      placeholder="80000"
                    />
                    {errors.financial_info?.annual_income && (
                      <p className="text-sm text-danger-600 mt-1">{errors.financial_info.annual_income.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Net Worth ($)</label>
                    <input
                      type="number"
                      {...register('financial_info.net_worth', {
                        required: 'Net worth is required',
                      })}
                      className="input-field"
                      placeholder="200000"
                    />
                    {errors.financial_info?.net_worth && (
                      <p className="text-sm text-danger-600 mt-1">{errors.financial_info.net_worth.message}</p>
                    )}
                  </div>

                  <div className="form-group">
                    <label className="label-field">Liquid Assets ($)</label>
                    <input
                      type="number"
                      {...register('financial_info.liquid_assets')}
                      className="input-field"
                      placeholder="50000"
                    />
                  </div>

                  <div className="form-group">
                    <label className="label-field">Investment Experience</label>
                    <select {...register('financial_info.investment_experience')} className="input-field">
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="professional">Professional</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="label-field">Risk Capacity</label>
                    <select {...register('financial_info.risk_capacity')} className="input-field">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="very high">Very High</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="label-field">Time Horizon</label>
                    <select {...register('financial_info.time_horizon')} className="input-field">
                      <option value="short-term">Short-term (< 3 years)</option>
                      <option value="medium-term">Medium-term (3-10 years)</option>
                      <option value="long-term">Long-term (> 10 years)</option>
                    </select>
                  </div>
                </div>

                {/* Financial Health Overview */}
                {watchedIncome && watchedCapital && (
                  <div className="mt-6 p-4 bg-slate-50 rounded-lg">
                    <h4 className="text-sm font-medium text-slate-900 mb-2">Financial Health Overview</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-slate-600">Savings Rate:</span>
                        <span className="block font-medium">
                          {(((watch('constraints.contributions') || 0) * 12) / watchedIncome * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Capital to Income:</span>
                        <span className="block font-medium">
                          {(watchedCapital / watchedIncome).toFixed(1)}x
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Liquid Assets:</span>
                        <span className="block font-medium">
                          ${(watch('financial_info.liquid_assets') || 0).toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-600">Net Worth:</span>
                        <span className="block font-medium">
                          ${(watch('financial_info.net_worth') || 0).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end space-x-4 pt-6 border-t border-slate-200">
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyzing...
              </>
            ) : (
              <>
                <Target className="w-4 h-4 mr-2" />
                Analyze Portfolio
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClientProfileForm;