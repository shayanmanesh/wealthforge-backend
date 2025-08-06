"""
Fine-Tuning Engine with GoalExceedPredictor and SensitivityAnalyzer

Advanced scenario modeling and constraint optimization system that simulates
adjustments to help clients exceed their financial goals through intelligent
parameter tuning and sensitivity analysis.
"""

import asyncio
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import warnings
from scipy.optimize import minimize, differential_evolution
from itertools import combinations
import copy
warnings.filterwarnings('ignore')

# Import existing components
from goal_constraint_parser import parse_goal_constraints
from portfolio_surgeon import synthesize_optimal_portfolio, PortfolioSynthesis
from strategy_optimization_arena import run_strategy_optimization, MarketData
from constraint_compliance_auditor import perform_compliance_audit


class AdjustmentType(Enum):
    """Types of constraint adjustments."""
    INCREASE_CAPITAL = "increase_capital"
    INCREASE_CONTRIBUTIONS = "increase_contributions"
    EXTEND_TIMELINE = "extend_timeline"
    ADJUST_RISK_TOLERANCE = "adjust_risk_tolerance"
    OPTIMIZE_TAX_ACCOUNTS = "optimize_tax_accounts"
    REDUCE_EXPENSES = "reduce_expenses"
    INCREASE_INCOME = "increase_income"
    REBALANCE_ALLOCATION = "rebalance_allocation"


class OptimizationStrategy(Enum):
    """Optimization strategies for goal achievement."""
    CONSERVATIVE = "conservative"  # Minimal changes, high confidence
    BALANCED = "balanced"         # Moderate changes, balanced approach
    AGGRESSIVE = "aggressive"     # Significant changes, maximum optimization
    CUSTOM = "custom"            # User-defined parameters


class SensitivityMetric(Enum):
    """Metrics for sensitivity analysis."""
    GOAL_ACHIEVEMENT_PROBABILITY = "goal_achievement_probability"
    TIME_TO_GOAL = "time_to_goal"
    EXCESS_RETURN = "excess_return"
    RISK_ADJUSTED_RETURN = "risk_adjusted_return"
    SHORTFALL_RISK = "shortfall_risk"
    DOWNSIDE_PROTECTION = "downside_protection"


@dataclass
class ConstraintAdjustment:
    """Represents a constraint adjustment suggestion."""
    adjustment_id: str
    adjustment_type: AdjustmentType
    description: str
    current_value: Any
    suggested_value: Any
    impact_magnitude: float  # 0-1, higher = more impact
    implementation_difficulty: float  # 0-1, higher = more difficult
    confidence_score: float  # 0-1, higher = more confident
    expected_improvement: float  # Expected improvement in goal achievement
    side_effects: List[str] = field(default_factory=list)
    implementation_timeline: str = "immediate"
    cost_benefit_ratio: float = 0.0


@dataclass
class SensitivityAnalysis:
    """Results of sensitivity analysis for a parameter."""
    parameter_name: str
    base_value: Any
    sensitivity_coefficient: float  # How much goal achievement changes per unit change
    elasticity: float  # Percentage change in goal / percentage change in parameter
    confidence_interval: Tuple[float, float]
    critical_threshold: Optional[float]  # Value where behavior changes significantly
    diminishing_returns_point: Optional[float]  # Point where additional changes have less impact
    risk_factors: List[str] = field(default_factory=list)


@dataclass
class GoalExceedScenario:
    """Scenario for exceeding financial goals."""
    scenario_id: str
    scenario_name: str
    adjustments: List[ConstraintAdjustment]
    projected_outcome: Dict[str, Any]
    probability_of_success: float
    time_to_goal: float  # Years
    excess_achievement: float  # How much goals are exceeded (percentage)
    risk_score: float
    implementation_score: float  # How feasible the scenario is
    total_cost: float  # Additional costs/commitments required
    confidence_level: float


@dataclass
class OptimizationResult:
    """Result of fine-tuning optimization."""
    optimization_id: str
    timestamp: datetime
    original_goal_probability: float
    optimized_goal_probability: float
    improvement_factor: float
    recommended_scenarios: List[GoalExceedScenario]
    sensitivity_analysis: Dict[str, SensitivityAnalysis]
    optimization_summary: Dict[str, Any]
    implementation_roadmap: List[str]
    risk_assessment: Dict[str, float]


class GoalExceedPredictor:
    """
    Advanced predictor for goal achievement and exceedance scenarios.
    Uses Monte Carlo simulation and machine learning techniques.
    """
    
    def __init__(self):
        """Initialize GoalExceedPredictor."""
        self.simulation_runs = 10000
        self.confidence_levels = [0.5, 0.7, 0.8, 0.9, 0.95]
        self.market_scenarios = self._initialize_market_scenarios()
        self.prediction_models = self._initialize_prediction_models()
        
    def _initialize_market_scenarios(self) -> Dict[str, Dict[str, float]]:
        """Initialize market scenario parameters."""
        return {
            'bull_market': {
                'probability': 0.25,
                'return_multiplier': 1.4,
                'volatility_multiplier': 0.8,
                'duration_years': 3
            },
            'bear_market': {
                'probability': 0.15,
                'return_multiplier': 0.6,
                'volatility_multiplier': 1.5,
                'duration_years': 1.5
            },
            'normal_market': {
                'probability': 0.50,
                'return_multiplier': 1.0,
                'volatility_multiplier': 1.0,
                'duration_years': 'variable'
            },
            'recession': {
                'probability': 0.10,
                'return_multiplier': 0.3,
                'volatility_multiplier': 2.0,
                'duration_years': 2
            }
        }
    
    def _initialize_prediction_models(self) -> Dict[str, Any]:
        """Initialize prediction model parameters."""
        return {
            'goal_achievement_model': {
                'base_success_rate': 0.65,
                'variance_factor': 0.15,
                'time_decay_factor': 0.02,
                'risk_adjustment_factor': -0.3
            },
            'market_timing_model': {
                'sequence_risk_factor': 0.1,
                'withdrawal_rate_impact': -2.5,
                'rebalancing_benefit': 0.05
            },
            'behavioral_model': {
                'discipline_factor': 0.9,
                'panic_selling_probability': 0.15,
                'contribution_consistency': 0.85
            }
        }
    
    async def predict_goal_achievement(self, client_profile: Dict[str, Any], 
                                     portfolio_result: Optional[PortfolioSynthesis] = None,
                                     adjustment_scenario: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """
        Predict probability of goal achievement under current or adjusted scenario.
        """
        # Parse client information
        goals = client_profile.get('goals', {})
        constraints = client_profile.get('constraints', {})
        
        # Extract key parameters
        current_capital = float(constraints.get('capital', 0))
        monthly_contributions = float(constraints.get('contributions', 0))
        target_amount = float(goals.get('target_amount', current_capital * 5))
        timeline_years = self._extract_timeline_years(goals.get('timeline', '10 years'))
        
        # Apply adjustment scenario if provided
        if adjustment_scenario:
            current_capital = adjustment_scenario.get('capital', current_capital)
            monthly_contributions = adjustment_scenario.get('contributions', monthly_contributions)
            timeline_years = adjustment_scenario.get('timeline_years', timeline_years)
        
        # Get portfolio parameters
        if portfolio_result:
            expected_return = portfolio_result.expected_return
            risk_score = portfolio_result.risk_score
        else:
            expected_return = 0.07  # Default 7% return
            risk_score = 0.15  # Default 15% volatility
        
        # Run Monte Carlo simulation
        results = await self._run_monte_carlo_simulation(
            current_capital, monthly_contributions, target_amount, 
            timeline_years, expected_return, risk_score
        )
        
        return results
    
    async def _run_monte_carlo_simulation(self, initial_capital: float, 
                                        monthly_contributions: float,
                                        target_amount: float, timeline_years: float,
                                        expected_return: float, volatility: float) -> Dict[str, float]:
        """Run Monte Carlo simulation for goal achievement."""
        
        simulation_results = []
        months = int(timeline_years * 12)
        annual_return = expected_return
        monthly_return = annual_return / 12
        monthly_volatility = volatility / np.sqrt(12)
        
        for run in range(self.simulation_runs):
            portfolio_value = initial_capital
            
            for month in range(months):
                # Generate random return for this month
                random_return = np.random.normal(monthly_return, monthly_volatility)
                
                # Apply market scenario adjustments
                scenario_multiplier = self._get_scenario_multiplier(month, timeline_years)
                adjusted_return = random_return * scenario_multiplier
                
                # Update portfolio value
                portfolio_value = portfolio_value * (1 + adjusted_return) + monthly_contributions
                
                # Apply behavioral factors
                if month % 12 == 0:  # Annual review
                    portfolio_value *= self._apply_behavioral_factors(adjusted_return)
            
            simulation_results.append(portfolio_value)
        
        # Calculate statistics
        simulation_array = np.array(simulation_results)
        
        # Goal achievement probabilities
        goal_achievement_prob = np.mean(simulation_array >= target_amount)
        exceed_by_25_prob = np.mean(simulation_array >= target_amount * 1.25)
        exceed_by_50_prob = np.mean(simulation_array >= target_amount * 1.50)
        
        # Risk metrics
        shortfall_prob = 1 - goal_achievement_prob
        average_shortfall = np.mean(np.maximum(0, target_amount - simulation_array))
        worst_case_5th_percentile = np.percentile(simulation_array, 5)
        
        # Excess achievement metrics
        median_outcome = np.median(simulation_array)
        expected_excess = max(0, (median_outcome - target_amount) / target_amount)
        
        return {
            'goal_achievement_probability': goal_achievement_prob,
            'exceed_by_25_percent_probability': exceed_by_25_prob,
            'exceed_by_50_percent_probability': exceed_by_50_prob,
            'shortfall_probability': shortfall_prob,
            'average_shortfall': average_shortfall,
            'worst_case_5th_percentile': worst_case_5th_percentile,
            'median_outcome': median_outcome,
            'expected_excess_percentage': expected_excess,
            'mean_final_value': np.mean(simulation_array),
            'standard_deviation': np.std(simulation_array),
            'confidence_interval_90': [np.percentile(simulation_array, 5), 
                                     np.percentile(simulation_array, 95)]
        }
    
    def _get_scenario_multiplier(self, month: int, timeline_years: float) -> float:
        """Get market scenario multiplier for given month."""
        # Simulate market cycles
        cycle_position = (month / (timeline_years * 12)) * 2 * np.pi
        base_cycle = 1.0 + 0.1 * np.sin(cycle_position)
        
        # Add random scenario events
        if np.random.random() < 0.02:  # 2% chance of significant event per month
            scenario_type = np.random.choice(list(self.market_scenarios.keys()), 
                                           p=[0.25, 0.15, 0.50, 0.10])
            return self.market_scenarios[scenario_type]['return_multiplier']
        
        return base_cycle
    
    def _apply_behavioral_factors(self, annual_return: float) -> float:
        """Apply behavioral factors to portfolio performance."""
        behavioral_model = self.prediction_models['behavioral_model']
        
        # Discipline factor (people don't always stick to plan)
        discipline_adjustment = behavioral_model['discipline_factor']
        
        # Panic selling during bad years
        if annual_return < -0.1:  # If down more than 10%
            panic_prob = behavioral_model['panic_selling_probability']
            if np.random.random() < panic_prob:
                discipline_adjustment *= 0.9  # 10% performance hit from panic selling
        
        return discipline_adjustment
    
    def _extract_timeline_years(self, timeline_str: str) -> float:
        """Extract number of years from timeline string."""
        import re
        numbers = re.findall(r'\d+', str(timeline_str).lower())
        if numbers:
            return float(numbers[0])
        
        # Default mappings
        timeline_lower = str(timeline_str).lower()
        if 'short' in timeline_lower:
            return 3
        elif 'medium' in timeline_lower:
            return 7
        elif 'long' in timeline_lower:
            return 15
        else:
            return 10
    
    async def predict_time_to_goal(self, client_profile: Dict[str, Any],
                                 target_amount: float,
                                 adjustment_scenario: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """Predict time required to reach goal under different scenarios."""
        constraints = client_profile.get('constraints', {})
        
        current_capital = float(constraints.get('capital', 0))
        monthly_contributions = float(constraints.get('contributions', 0))
        
        if adjustment_scenario:
            current_capital = adjustment_scenario.get('capital', current_capital)
            monthly_contributions = adjustment_scenario.get('contributions', monthly_contributions)
        
        # Estimate time to goal under different return scenarios
        return_scenarios = [0.04, 0.06, 0.07, 0.08, 0.10, 0.12]
        time_estimates = {}
        
        for annual_return in return_scenarios:
            time_years = self._calculate_time_to_goal(
                current_capital, monthly_contributions, target_amount, annual_return
            )
            time_estimates[f'return_{annual_return:.0%}'] = time_years
        
        # Calculate probabilistic time estimate
        weighted_time = sum(time * 0.1667 for time in time_estimates.values())
        
        return {
            'scenario_estimates': time_estimates,
            'expected_time_years': weighted_time,
            'conservative_estimate': max(time_estimates.values()),
            'optimistic_estimate': min(time_estimates.values())
        }
    
    def _calculate_time_to_goal(self, current_capital: float, monthly_contribution: float,
                              target_amount: float, annual_return: float) -> float:
        """Calculate time to reach goal with given parameters."""
        if current_capital >= target_amount:
            return 0
        
        if monthly_contribution <= 0:
            if annual_return <= 0:
                return float('inf')
            return np.log(target_amount / current_capital) / np.log(1 + annual_return)
        
        # Formula for future value of growing annuity
        monthly_rate = annual_return / 12
        if monthly_rate == 0:
            return (target_amount - current_capital) / (monthly_contribution * 12)
        
        # Solve for time using iterative approach
        for months in range(1, 600):  # Up to 50 years
            future_value = (current_capital * (1 + monthly_rate) ** months + 
                          monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate))
            if future_value >= target_amount:
                return months / 12
        
        return 50  # Maximum time horizon


class SensitivityAnalyzer:
    """
    Advanced sensitivity analyzer for constraint parameter impacts.
    Analyzes how changes in constraints affect goal achievement.
    """
    
    def __init__(self, goal_predictor: GoalExceedPredictor):
        """Initialize SensitivityAnalyzer."""
        self.goal_predictor = goal_predictor
        self.sensitivity_ranges = {
            'capital': [0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0],
            'contributions': [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0],
            'timeline': [0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0],
            'risk_tolerance': ['conservative', 'moderate', 'aggressive']
        }
        
    async def analyze_parameter_sensitivity(self, client_profile: Dict[str, Any],
                                          parameter: str,
                                          portfolio_result: Optional[PortfolioSynthesis] = None) -> SensitivityAnalysis:
        """
        Analyze sensitivity of goal achievement to a specific parameter.
        """
        base_prediction = await self.goal_predictor.predict_goal_achievement(
            client_profile, portfolio_result
        )
        base_prob = base_prediction['goal_achievement_probability']
        
        # Get parameter sensitivity range
        if parameter not in self.sensitivity_ranges:
            raise ValueError(f"Parameter {parameter} not supported for sensitivity analysis")
        
        sensitivity_results = []
        parameter_values = []
        
        # Test different parameter values
        for multiplier in self.sensitivity_ranges[parameter]:
            if parameter == 'risk_tolerance':
                adjusted_profile = self._adjust_risk_tolerance(client_profile, multiplier)
            else:
                adjusted_profile = self._adjust_parameter(client_profile, parameter, multiplier)
            
            prediction = await self.goal_predictor.predict_goal_achievement(
                adjusted_profile, portfolio_result
            )
            
            sensitivity_results.append(prediction['goal_achievement_probability'])
            parameter_values.append(multiplier if parameter != 'risk_tolerance' else multiplier)
        
        # Calculate sensitivity metrics
        sensitivity_coefficient = self._calculate_sensitivity_coefficient(
            parameter_values, sensitivity_results, base_prob
        )
        
        elasticity = self._calculate_elasticity(parameter_values, sensitivity_results)
        
        confidence_interval = self._calculate_confidence_interval(sensitivity_results)
        
        critical_threshold = self._find_critical_threshold(parameter_values, sensitivity_results)
        
        diminishing_returns_point = self._find_diminishing_returns_point(
            parameter_values, sensitivity_results
        )
        
        risk_factors = self._identify_risk_factors(parameter, sensitivity_results)
        
        return SensitivityAnalysis(
            parameter_name=parameter,
            base_value=client_profile.get('constraints', {}).get(parameter, 1.0),
            sensitivity_coefficient=sensitivity_coefficient,
            elasticity=elasticity,
            confidence_interval=confidence_interval,
            critical_threshold=critical_threshold,
            diminishing_returns_point=diminishing_returns_point,
            risk_factors=risk_factors
        )
    
    def _adjust_parameter(self, client_profile: Dict[str, Any], 
                         parameter: str, multiplier: float) -> Dict[str, Any]:
        """Adjust a parameter in client profile."""
        adjusted_profile = copy.deepcopy(client_profile)
        constraints = adjusted_profile.get('constraints', {})
        
        if parameter == 'capital':
            constraints['capital'] = float(constraints.get('capital', 0)) * multiplier
        elif parameter == 'contributions':
            constraints['contributions'] = float(constraints.get('contributions', 0)) * multiplier
        elif parameter == 'timeline':
            goals = adjusted_profile.get('goals', {})
            current_timeline = goals.get('timeline', '10 years')
            current_years = self.goal_predictor._extract_timeline_years(current_timeline)
            new_years = current_years * multiplier
            goals['timeline'] = f"{new_years:.1f} years"
        
        return adjusted_profile
    
    def _adjust_risk_tolerance(self, client_profile: Dict[str, Any], 
                              risk_level: str) -> Dict[str, Any]:
        """Adjust risk tolerance in client profile."""
        adjusted_profile = copy.deepcopy(client_profile)
        goals = adjusted_profile.get('goals', {})
        goals['risk_tolerance'] = risk_level
        return adjusted_profile
    
    def _calculate_sensitivity_coefficient(self, parameter_values: List[float],
                                         sensitivity_results: List[float],
                                         base_prob: float) -> float:
        """Calculate sensitivity coefficient (change in goal prob per unit change in parameter)."""
        if len(parameter_values) < 2:
            return 0.0
        
        # Linear regression slope
        x = np.array(parameter_values)
        y = np.array(sensitivity_results)
        
        if len(x) > 1 and np.std(x) > 0:
            correlation_matrix = np.corrcoef(x, y)
            correlation = correlation_matrix[0, 1] if not np.isnan(correlation_matrix[0, 1]) else 0
            return correlation * (np.std(y) / np.std(x))
        
        return 0.0
    
    def _calculate_elasticity(self, parameter_values: List[float],
                            sensitivity_results: List[float]) -> float:
        """Calculate elasticity (% change in goal prob per % change in parameter)."""
        if len(parameter_values) < 2:
            return 0.0
        
        # Find base case (multiplier = 1.0)
        base_idx = None
        for i, val in enumerate(parameter_values):
            if abs(val - 1.0) < 0.01:
                base_idx = i
                break
        
        if base_idx is None or base_idx == 0:
            return 0.0
        
        base_param = parameter_values[base_idx]
        base_result = sensitivity_results[base_idx]
        
        # Calculate average elasticity across all points
        elasticities = []
        for i, (param, result) in enumerate(zip(parameter_values, sensitivity_results)):
            if i != base_idx and param != base_param and base_result > 0:
                param_change = (param - base_param) / base_param
                result_change = (result - base_result) / base_result
                if param_change != 0:
                    elasticities.append(result_change / param_change)
        
        return np.mean(elasticities) if elasticities else 0.0
    
    def _calculate_confidence_interval(self, sensitivity_results: List[float]) -> Tuple[float, float]:
        """Calculate confidence interval for sensitivity results."""
        if len(sensitivity_results) < 2:
            return (0.0, 1.0)
        
        results_array = np.array(sensitivity_results)
        return (np.percentile(results_array, 5), np.percentile(results_array, 95))
    
    def _find_critical_threshold(self, parameter_values: List[float],
                               sensitivity_results: List[float]) -> Optional[float]:
        """Find critical threshold where behavior changes significantly."""
        if len(parameter_values) < 3:
            return None
        
        # Look for inflection points
        for i in range(1, len(sensitivity_results) - 1):
            slope_before = sensitivity_results[i] - sensitivity_results[i-1]
            slope_after = sensitivity_results[i+1] - sensitivity_results[i]
            
            # Check for significant change in slope
            if abs(slope_after - slope_before) > 0.1:
                return parameter_values[i]
        
        return None
    
    def _find_diminishing_returns_point(self, parameter_values: List[float],
                                      sensitivity_results: List[float]) -> Optional[float]:
        """Find point where additional changes have diminishing returns."""
        if len(parameter_values) < 3:
            return None
        
        # Calculate second derivatives (rate of change of sensitivity)
        for i in range(2, len(sensitivity_results)):
            second_derivative = (sensitivity_results[i] - 2*sensitivity_results[i-1] + 
                               sensitivity_results[i-2])
            
            # Look for where second derivative becomes significantly negative
            if second_derivative < -0.05:
                return parameter_values[i-1]
        
        return None
    
    def _identify_risk_factors(self, parameter: str, 
                             sensitivity_results: List[float]) -> List[str]:
        """Identify risk factors associated with parameter changes."""
        risk_factors = []
        
        max_prob = max(sensitivity_results)
        min_prob = min(sensitivity_results)
        
        if max_prob - min_prob > 0.3:
            risk_factors.append("High sensitivity to parameter changes")
        
        if parameter == 'capital':
            risk_factors.extend([
                "Liquidity requirements may limit flexibility",
                "Market timing risk for additional investments"
            ])
        elif parameter == 'contributions':
            risk_factors.extend([
                "Income stability required for sustained contributions",
                "Lifestyle inflation may reduce contribution capacity"
            ])
        elif parameter == 'timeline':
            risk_factors.extend([
                "Sequence of returns risk over longer periods",
                "Changing life circumstances may affect timeline"
            ])
        
        return risk_factors
    
    async def comprehensive_sensitivity_analysis(self, client_profile: Dict[str, Any],
                                                portfolio_result: Optional[PortfolioSynthesis] = None) -> Dict[str, SensitivityAnalysis]:
        """
        Perform comprehensive sensitivity analysis across all key parameters.
        """
        parameters = ['capital', 'contributions', 'timeline']
        sensitivity_results = {}
        
        for parameter in parameters:
            try:
                analysis = await self.analyze_parameter_sensitivity(
                    client_profile, parameter, portfolio_result
                )
                sensitivity_results[parameter] = analysis
            except Exception as e:
                print(f"Error analyzing {parameter}: {e}")
                continue
        
        return sensitivity_results


class FineTuningEngine:
    """
    Main Fine-Tuning Engine that orchestrates goal optimization through
    constraint adjustments using GoalExceedPredictor and SensitivityAnalyzer.
    """
    
    def __init__(self):
        """Initialize Fine-Tuning Engine."""
        self.goal_predictor = GoalExceedPredictor()
        self.sensitivity_analyzer = SensitivityAnalyzer(self.goal_predictor)
        self.optimization_strategies = self._initialize_optimization_strategies()
        
    def _initialize_optimization_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize optimization strategy parameters."""
        return {
            'conservative': {
                'max_capital_increase': 1.2,
                'max_contribution_increase': 1.3,
                'max_timeline_extension': 1.1,
                'risk_tolerance_change': False,
                'confidence_threshold': 0.8
            },
            'balanced': {
                'max_capital_increase': 1.5,
                'max_contribution_increase': 2.0,
                'max_timeline_extension': 1.3,
                'risk_tolerance_change': True,
                'confidence_threshold': 0.7
            },
            'aggressive': {
                'max_capital_increase': 2.0,
                'max_contribution_increase': 3.0,
                'max_timeline_extension': 1.5,
                'risk_tolerance_change': True,
                'confidence_threshold': 0.6
            }
        }
    
    async def optimize_for_goal_exceedance(self, client_profile: Dict[str, Any],
                                         target_exceedance: float = 0.25,
                                         strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
                                         portfolio_result: Optional[PortfolioSynthesis] = None) -> OptimizationResult:
        """
        Main optimization function to find constraint adjustments for goal exceedance.
        
        Args:
            client_profile: Client's current profile
            target_exceedance: Target exceedance percentage (0.25 = 25% above goal)
            strategy: Optimization strategy (conservative, balanced, aggressive)
            portfolio_result: Current portfolio optimization result
        
        Returns:
            OptimizationResult with recommended adjustments and scenarios
        """
        optimization_id = f"optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🔧 FINE-TUNING ENGINE: Goal Exceedance Optimization")
        print(f"   Target Exceedance: {target_exceedance:.1%}")
        print(f"   Strategy: {strategy.value}")
        
        # Step 1: Baseline analysis
        print("   📊 Step 1: Baseline goal achievement analysis...")
        baseline_prediction = await self.goal_predictor.predict_goal_achievement(
            client_profile, portfolio_result
        )
        
        # Step 2: Comprehensive sensitivity analysis
        print("   🔍 Step 2: Comprehensive sensitivity analysis...")
        sensitivity_results = await self.sensitivity_analyzer.comprehensive_sensitivity_analysis(
            client_profile, portfolio_result
        )
        
        # Step 3: Generate constraint adjustments
        print("   ⚙️ Step 3: Generating constraint adjustments...")
        adjustment_scenarios = await self._generate_adjustment_scenarios(
            client_profile, sensitivity_results, target_exceedance, strategy
        )
        
        # Step 4: Evaluate scenarios
        print("   📈 Step 4: Evaluating optimization scenarios...")
        evaluated_scenarios = await self._evaluate_scenarios(
            client_profile, adjustment_scenarios, portfolio_result
        )
        
        # Step 5: Rank and select best scenarios
        print("   🏆 Step 5: Ranking and selecting optimal scenarios...")
        ranked_scenarios = self._rank_scenarios(evaluated_scenarios, target_exceedance)
        
        # Step 6: Create implementation roadmap
        print("   🗺️ Step 6: Creating implementation roadmap...")
        implementation_roadmap = self._create_implementation_roadmap(ranked_scenarios[:3])
        
        # Calculate improvement metrics
        original_prob = baseline_prediction['goal_achievement_probability']
        best_scenario_prob = ranked_scenarios[0].probability_of_success if ranked_scenarios else original_prob
        improvement_factor = best_scenario_prob / original_prob if original_prob > 0 else 1.0
        
        # Risk assessment
        risk_assessment = self._assess_optimization_risks(ranked_scenarios, sensitivity_results)
        
        # Optimization summary
        optimization_summary = {
            'baseline_goal_probability': original_prob,
            'baseline_excess_probability': baseline_prediction.get('exceed_by_25_percent_probability', 0),
            'target_exceedance': target_exceedance,
            'scenarios_generated': len(adjustment_scenarios),
            'scenarios_evaluated': len(evaluated_scenarios),
            'top_scenarios_selected': min(3, len(ranked_scenarios)),
            'max_improvement_achieved': improvement_factor - 1.0,
            'strategy_used': strategy.value
        }
        
        print(f"   ✅ Optimization complete: {improvement_factor:.1%} improvement potential")
        
        return OptimizationResult(
            optimization_id=optimization_id,
            timestamp=datetime.now(),
            original_goal_probability=original_prob,
            optimized_goal_probability=best_scenario_prob,
            improvement_factor=improvement_factor,
            recommended_scenarios=ranked_scenarios[:3],
            sensitivity_analysis=sensitivity_results,
            optimization_summary=optimization_summary,
            implementation_roadmap=implementation_roadmap,
            risk_assessment=risk_assessment
        )
    
    async def _generate_adjustment_scenarios(self, client_profile: Dict[str, Any],
                                           sensitivity_results: Dict[str, SensitivityAnalysis],
                                           target_exceedance: float,
                                           strategy: OptimizationStrategy) -> List[Dict[str, Any]]:
        """Generate potential constraint adjustment scenarios."""
        scenarios = []
        strategy_params = self.optimization_strategies[strategy.value]
        
        # Single parameter adjustments
        for param_name, sensitivity in sensitivity_results.items():
            if sensitivity.sensitivity_coefficient > 0.1:  # Only consider impactful parameters
                scenarios.extend(
                    self._generate_single_parameter_scenarios(
                        client_profile, param_name, sensitivity, strategy_params
                    )
                )
        
        # Two-parameter combinations
        param_combinations = list(combinations(sensitivity_results.keys(), 2))
        for param1, param2 in param_combinations:
            scenarios.extend(
                self._generate_two_parameter_scenarios(
                    client_profile, param1, param2, 
                    sensitivity_results[param1], sensitivity_results[param2], 
                    strategy_params
                )
            )
        
        # Three-parameter comprehensive scenarios
        if len(sensitivity_results) >= 3:
            scenarios.extend(
                self._generate_comprehensive_scenarios(
                    client_profile, sensitivity_results, strategy_params
                )
            )
        
        return scenarios
    
    def _generate_single_parameter_scenarios(self, client_profile: Dict[str, Any],
                                           parameter: str, sensitivity: SensitivityAnalysis,
                                           strategy_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scenarios adjusting a single parameter."""
        scenarios = []
        constraints = client_profile.get('constraints', {})
        
        if parameter == 'capital':
            current_value = float(constraints.get('capital', 0))
            max_multiplier = strategy_params['max_capital_increase']
            
            for multiplier in [1.1, 1.25, 1.5, max_multiplier]:
                if multiplier <= max_multiplier:
                    scenarios.append({
                        'scenario_name': f"Increase Capital by {(multiplier-1)*100:.0f}%",
                        'adjustments': {
                            'capital': current_value * multiplier
                        },
                        'adjustment_types': [AdjustmentType.INCREASE_CAPITAL]
                    })
        
        elif parameter == 'contributions':
            current_value = float(constraints.get('contributions', 0))
            max_multiplier = strategy_params['max_contribution_increase']
            
            for multiplier in [1.2, 1.5, 2.0, max_multiplier]:
                if multiplier <= max_multiplier:
                    scenarios.append({
                        'scenario_name': f"Increase Contributions by {(multiplier-1)*100:.0f}%",
                        'adjustments': {
                            'contributions': current_value * multiplier
                        },
                        'adjustment_types': [AdjustmentType.INCREASE_CONTRIBUTIONS]
                    })
        
        elif parameter == 'timeline':
            goals = client_profile.get('goals', {})
            current_timeline = goals.get('timeline', '10 years')
            current_years = self.goal_predictor._extract_timeline_years(current_timeline)
            max_multiplier = strategy_params['max_timeline_extension']
            
            for multiplier in [1.1, 1.2, 1.3, max_multiplier]:
                if multiplier <= max_multiplier:
                    new_years = current_years * multiplier
                    scenarios.append({
                        'scenario_name': f"Extend Timeline to {new_years:.1f} Years",
                        'adjustments': {
                            'timeline_years': new_years
                        },
                        'adjustment_types': [AdjustmentType.EXTEND_TIMELINE]
                    })
        
        return scenarios
    
    def _generate_two_parameter_scenarios(self, client_profile: Dict[str, Any],
                                        param1: str, param2: str,
                                        sensitivity1: SensitivityAnalysis,
                                        sensitivity2: SensitivityAnalysis,
                                        strategy_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scenarios adjusting two parameters simultaneously."""
        scenarios = []
        constraints = client_profile.get('constraints', {})
        goals = client_profile.get('goals', {})
        
        # Moderate adjustments to both parameters
        adjustments = {}
        adjustment_types = []
        scenario_name_parts = []
        
        if param1 == 'capital':
            current_capital = float(constraints.get('capital', 0))
            new_capital = current_capital * 1.25
            adjustments['capital'] = new_capital
            adjustment_types.append(AdjustmentType.INCREASE_CAPITAL)
            scenario_name_parts.append("Capital +25%")
        
        if param1 == 'contributions':
            current_contributions = float(constraints.get('contributions', 0))
            new_contributions = current_contributions * 1.5
            adjustments['contributions'] = new_contributions
            adjustment_types.append(AdjustmentType.INCREASE_CONTRIBUTIONS)
            scenario_name_parts.append("Contributions +50%")
        
        if param2 == 'capital' and 'capital' not in adjustments:
            current_capital = float(constraints.get('capital', 0))
            new_capital = current_capital * 1.25
            adjustments['capital'] = new_capital
            adjustment_types.append(AdjustmentType.INCREASE_CAPITAL)
            scenario_name_parts.append("Capital +25%")
        
        if param2 == 'contributions' and 'contributions' not in adjustments:
            current_contributions = float(constraints.get('contributions', 0))
            new_contributions = current_contributions * 1.5
            adjustments['contributions'] = new_contributions
            adjustment_types.append(AdjustmentType.INCREASE_CONTRIBUTIONS)
            scenario_name_parts.append("Contributions +50%")
        
        if param2 == 'timeline' and 'timeline_years' not in adjustments:
            current_timeline = goals.get('timeline', '10 years')
            current_years = self.goal_predictor._extract_timeline_years(current_timeline)
            new_years = current_years * 1.15
            adjustments['timeline_years'] = new_years
            adjustment_types.append(AdjustmentType.EXTEND_TIMELINE)
            scenario_name_parts.append(f"Timeline +{(new_years-current_years):.1f}yr")
        
        if adjustments and len(scenario_name_parts) >= 2:
            scenarios.append({
                'scenario_name': f"Combined: {' + '.join(scenario_name_parts)}",
                'adjustments': adjustments,
                'adjustment_types': adjustment_types
            })
        
        return scenarios
    
    def _generate_comprehensive_scenarios(self, client_profile: Dict[str, Any],
                                        sensitivity_results: Dict[str, SensitivityAnalysis],
                                        strategy_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive scenarios adjusting multiple parameters."""
        scenarios = []
        constraints = client_profile.get('constraints', {})
        goals = client_profile.get('goals', {})
        
        # Comprehensive optimization scenario
        adjustments = {}
        adjustment_types = []
        
        # Capital increase
        if 'capital' in sensitivity_results:
            current_capital = float(constraints.get('capital', 0))
            multiplier = min(1.3, strategy_params['max_capital_increase'])
            adjustments['capital'] = current_capital * multiplier
            adjustment_types.append(AdjustmentType.INCREASE_CAPITAL)
        
        # Contribution increase
        if 'contributions' in sensitivity_results:
            current_contributions = float(constraints.get('contributions', 0))
            multiplier = min(1.75, strategy_params['max_contribution_increase'])
            adjustments['contributions'] = current_contributions * multiplier
            adjustment_types.append(AdjustmentType.INCREASE_CONTRIBUTIONS)
        
        # Timeline extension
        if 'timeline' in sensitivity_results:
            current_timeline = goals.get('timeline', '10 years')
            current_years = self.goal_predictor._extract_timeline_years(current_timeline)
            multiplier = min(1.2, strategy_params['max_timeline_extension'])
            adjustments['timeline_years'] = current_years * multiplier
            adjustment_types.append(AdjustmentType.EXTEND_TIMELINE)
        
        scenarios.append({
            'scenario_name': "Comprehensive Optimization: Multi-Parameter Enhancement",
            'adjustments': adjustments,
            'adjustment_types': adjustment_types
        })
        
        return scenarios
    
    async def _evaluate_scenarios(self, client_profile: Dict[str, Any],
                                scenarios: List[Dict[str, Any]],
                                portfolio_result: Optional[PortfolioSynthesis] = None) -> List[GoalExceedScenario]:
        """Evaluate all generated scenarios."""
        evaluated_scenarios = []
        
        for i, scenario in enumerate(scenarios):
            scenario_id = f"scenario_{i+1:03d}"
            
            # Create adjusted client profile
            adjusted_profile = self._apply_adjustments(client_profile, scenario['adjustments'])
            
            # Predict outcomes
            prediction = await self.goal_predictor.predict_goal_achievement(
                adjusted_profile, portfolio_result
            )
            
            # Calculate implementation metrics
            implementation_score = self._calculate_implementation_score(
                scenario['adjustments'], client_profile
            )
            
            total_cost = self._calculate_total_cost(scenario['adjustments'], client_profile)
            
            # Create constraint adjustments
            constraint_adjustments = self._create_constraint_adjustments(
                scenario['adjustments'], scenario['adjustment_types'], client_profile
            )
            
            # Calculate time to goal
            time_prediction = await self.goal_predictor.predict_time_to_goal(
                adjusted_profile, 
                float(client_profile.get('goals', {}).get('target_amount', 1000000))
            )
            
            evaluated_scenario = GoalExceedScenario(
                scenario_id=scenario_id,
                scenario_name=scenario['scenario_name'],
                adjustments=constraint_adjustments,
                projected_outcome={
                    'goal_achievement_probability': prediction['goal_achievement_probability'],
                    'exceed_by_25_percent': prediction.get('exceed_by_25_percent_probability', 0),
                    'expected_excess_percentage': prediction.get('expected_excess_percentage', 0),
                    'median_outcome': prediction.get('median_outcome', 0),
                    'worst_case_5th_percentile': prediction.get('worst_case_5th_percentile', 0)
                },
                probability_of_success=prediction['goal_achievement_probability'],
                time_to_goal=time_prediction.get('expected_time_years', 0),
                excess_achievement=prediction.get('expected_excess_percentage', 0),
                risk_score=1.0 - prediction['goal_achievement_probability'],
                implementation_score=implementation_score,
                total_cost=total_cost,
                confidence_level=0.8  # Default confidence level
            )
            
            evaluated_scenarios.append(evaluated_scenario)
        
        return evaluated_scenarios
    
    def _apply_adjustments(self, client_profile: Dict[str, Any], 
                         adjustments: Dict[str, Any]) -> Dict[str, Any]:
        """Apply adjustments to client profile."""
        adjusted_profile = copy.deepcopy(client_profile)
        constraints = adjusted_profile.get('constraints', {})
        goals = adjusted_profile.get('goals', {})
        
        for key, value in adjustments.items():
            if key in ['capital', 'contributions']:
                constraints[key] = value
            elif key == 'timeline_years':
                goals['timeline'] = f"{value:.1f} years"
        
        return adjusted_profile
    
    def _calculate_implementation_score(self, adjustments: Dict[str, Any], 
                                      client_profile: Dict[str, Any]) -> float:
        """Calculate how feasible the scenario is to implement."""
        score = 1.0
        constraints = client_profile.get('constraints', {})
        
        # Capital increase difficulty
        if 'capital' in adjustments:
            current_capital = float(constraints.get('capital', 0))
            new_capital = adjustments['capital']
            increase_ratio = new_capital / current_capital if current_capital > 0 else 2.0
            
            if increase_ratio > 2.0:
                score *= 0.3  # Very difficult
            elif increase_ratio > 1.5:
                score *= 0.6  # Moderately difficult
            elif increase_ratio > 1.2:
                score *= 0.8  # Somewhat difficult
        
        # Contribution increase difficulty
        if 'contributions' in adjustments:
            current_contributions = float(constraints.get('contributions', 0))
            new_contributions = adjustments['contributions']
            increase_ratio = new_contributions / current_contributions if current_contributions > 0 else 2.0
            
            if increase_ratio > 3.0:
                score *= 0.2  # Very difficult
            elif increase_ratio > 2.0:
                score *= 0.5  # Moderately difficult
            elif increase_ratio > 1.5:
                score *= 0.7  # Somewhat difficult
        
        return max(0.1, score)  # Minimum 10% feasibility
    
    def _calculate_total_cost(self, adjustments: Dict[str, Any], 
                           client_profile: Dict[str, Any]) -> float:
        """Calculate total additional cost/commitment required."""
        total_cost = 0.0
        constraints = client_profile.get('constraints', {})
        
        # Additional capital required
        if 'capital' in adjustments:
            current_capital = float(constraints.get('capital', 0))
            additional_capital = adjustments['capital'] - current_capital
            total_cost += additional_capital
        
        # Additional annual contributions
        if 'contributions' in adjustments:
            current_contributions = float(constraints.get('contributions', 0))
            additional_monthly = adjustments['contributions'] - current_contributions
            total_cost += additional_monthly * 12 * 10  # 10-year commitment value
        
        return total_cost
    
    def _create_constraint_adjustments(self, adjustments: Dict[str, Any],
                                     adjustment_types: List[AdjustmentType],
                                     client_profile: Dict[str, Any]) -> List[ConstraintAdjustment]:
        """Create ConstraintAdjustment objects from adjustments."""
        constraint_adjustments = []
        constraints = client_profile.get('constraints', {})
        
        for adj_type in adjustment_types:
            if adj_type == AdjustmentType.INCREASE_CAPITAL and 'capital' in adjustments:
                current_capital = float(constraints.get('capital', 0))
                new_capital = adjustments['capital']
                
                constraint_adjustments.append(ConstraintAdjustment(
                    adjustment_id=f"capital_adj_{datetime.now().strftime('%H%M%S')}",
                    adjustment_type=adj_type,
                    description=f"Increase initial capital from ${current_capital:,.0f} to ${new_capital:,.0f}",
                    current_value=current_capital,
                    suggested_value=new_capital,
                    impact_magnitude=0.8,
                    implementation_difficulty=0.6,
                    confidence_score=0.85,
                    expected_improvement=0.15,
                    side_effects=["Requires additional liquidity", "May affect other investment goals"],
                    implementation_timeline="immediate",
                    cost_benefit_ratio=(new_capital - current_capital) / max(1, new_capital - current_capital)
                ))
            
            elif adj_type == AdjustmentType.INCREASE_CONTRIBUTIONS and 'contributions' in adjustments:
                current_contributions = float(constraints.get('contributions', 0))
                new_contributions = adjustments['contributions']
                
                constraint_adjustments.append(ConstraintAdjustment(
                    adjustment_id=f"contrib_adj_{datetime.now().strftime('%H%M%S')}",
                    adjustment_type=adj_type,
                    description=f"Increase monthly contributions from ${current_contributions:,.0f} to ${new_contributions:,.0f}",
                    current_value=current_contributions,
                    suggested_value=new_contributions,
                    impact_magnitude=0.9,
                    implementation_difficulty=0.4,
                    confidence_score=0.9,
                    expected_improvement=0.25,
                    side_effects=["Requires sustained income", "May affect lifestyle"],
                    implementation_timeline="next month",
                    cost_benefit_ratio=(new_contributions - current_contributions) * 12 / max(1, (new_contributions - current_contributions) * 12)
                ))
        
        return constraint_adjustments
    
    def _rank_scenarios(self, scenarios: List[GoalExceedScenario], 
                       target_exceedance: float) -> List[GoalExceedScenario]:
        """Rank scenarios by effectiveness and feasibility."""
        def scenario_score(scenario: GoalExceedScenario) -> float:
            # Multi-criteria scoring
            goal_achievement_score = scenario.probability_of_success * 0.4
            exceedance_score = min(1.0, scenario.excess_achievement / target_exceedance) * 0.3
            feasibility_score = scenario.implementation_score * 0.2
            risk_score = (1.0 - scenario.risk_score) * 0.1
            
            return goal_achievement_score + exceedance_score + feasibility_score + risk_score
        
        ranked_scenarios = sorted(scenarios, key=scenario_score, reverse=True)
        return ranked_scenarios
    
    def _create_implementation_roadmap(self, top_scenarios: List[GoalExceedScenario]) -> List[str]:
        """Create implementation roadmap for top scenarios."""
        roadmap = [
            "🎯 Fine-Tuning Implementation Roadmap:",
            "",
            "Phase 1: Immediate Actions (0-30 days)",
            "• Review and validate scenario assumptions",
            "• Assess current financial capacity for adjustments",
            "• Prioritize high-impact, low-difficulty adjustments"
        ]
        
        if top_scenarios:
            best_scenario = top_scenarios[0]
            roadmap.extend([
                "",
                f"Phase 2: Primary Optimization - {best_scenario.scenario_name}",
                f"• Target probability improvement: {best_scenario.probability_of_success:.1%}",
                f"• Implementation difficulty: {best_scenario.implementation_score:.1%}",
                f"• Expected time to goal: {best_scenario.time_to_goal:.1f} years"
            ])
            
            for adjustment in best_scenario.adjustments[:2]:
                roadmap.append(f"• {adjustment.description}")
        
        roadmap.extend([
            "",
            "Phase 3: Monitoring and Adjustment (Ongoing)",
            "• Monthly progress tracking",
            "• Quarterly scenario re-evaluation",
            "• Annual comprehensive optimization review",
            "",
            "Phase 4: Contingency Planning",
            "• Alternative scenarios if primary plan faces obstacles",
            "• Risk mitigation strategies",
            "• Regular compliance and constraint validation"
        ])
        
        return roadmap
    
    def _assess_optimization_risks(self, scenarios: List[GoalExceedScenario],
                                 sensitivity_results: Dict[str, SensitivityAnalysis]) -> Dict[str, float]:
        """Assess risks associated with optimization scenarios."""
        risk_assessment = {
            'implementation_risk': 0.0,
            'market_risk': 0.0,
            'behavioral_risk': 0.0,
            'liquidity_risk': 0.0,
            'regulatory_risk': 0.0
        }
        
        if scenarios:
            # Implementation risk based on scenario difficulty
            avg_implementation_score = np.mean([s.implementation_score for s in scenarios[:3]])
            risk_assessment['implementation_risk'] = 1.0 - avg_implementation_score
            
            # Market risk based on sensitivity to market conditions
            market_sensitivity = max([s.sensitivity_coefficient for s in sensitivity_results.values()])
            risk_assessment['market_risk'] = min(1.0, market_sensitivity * 2)
            
            # Behavioral risk based on magnitude of changes required
            total_adjustments = sum([len(s.adjustments) for s in scenarios[:3]]) / 3
            risk_assessment['behavioral_risk'] = min(1.0, total_adjustments * 0.2)
            
            # Liquidity risk based on capital requirements
            avg_total_cost = np.mean([s.total_cost for s in scenarios[:3]])
            risk_assessment['liquidity_risk'] = min(1.0, avg_total_cost / 500000)  # Normalized to $500k
            
            # Regulatory risk (low for constraint adjustments)
            risk_assessment['regulatory_risk'] = 0.1
        
        return risk_assessment


# Convenience function for easy integration
async def optimize_goal_exceedance(client_profile: Dict[str, Any],
                                 target_exceedance: float = 0.25,
                                 strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
                                 portfolio_result: Optional[PortfolioSynthesis] = None) -> OptimizationResult:
    """
    Convenience function to perform goal exceedance optimization.
    """
    engine = FineTuningEngine()
    return await engine.optimize_for_goal_exceedance(
        client_profile, target_exceedance, strategy, portfolio_result
    )


if __name__ == "__main__":
    # Example usage
    async def main():
        # Sample client profile for testing
        client_profile = {
            "goals": {
                "strategy": "balanced growth",
                "timeline": "15 years",
                "target_amount": 1000000,
                "risk_tolerance": "moderate"
            },
            "constraints": {
                "capital": 150000,
                "contributions": 2000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 70
            },
            "additional_preferences": {
                "age": 40,
                "tax_optimization": True
            }
        }
        
        # Perform optimization
        result = await optimize_goal_exceedance(
            client_profile, 
            target_exceedance=0.30,  # Target 30% exceedance
            strategy=OptimizationStrategy.BALANCED
        )
        
        # Display results
        print(f"Optimization Results:")
        print(f"Original probability: {result.original_goal_probability:.1%}")
        print(f"Optimized probability: {result.optimized_goal_probability:.1%}")
        print(f"Improvement factor: {result.improvement_factor:.2f}x")
        print(f"Top scenarios: {len(result.recommended_scenarios)}")
        
        for scenario in result.recommended_scenarios:
            print(f"\n{scenario.scenario_name}:")
            print(f"  Success probability: {scenario.probability_of_success:.1%}")
            print(f"  Implementation score: {scenario.implementation_score:.1%}")
    
    # Run example
    asyncio.run(main())