"""
Portfolio Surgeon: Advanced Portfolio Optimization with Pareto-Optimal Synthesis

This module implements a sophisticated portfolio optimization system that synthesizes
multiple agent proposals using Pareto-optimal logic, integrated with NeuralDarkPool
for risk analysis and FeeAnnihilator for cost optimization.
"""

import numpy as np
import pandas as pd
import asyncio
import json
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import scipy.optimize as optimize
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

# Import existing components
from strategy_optimization_arena import (
    StrategyOptimizationArena, 
    AgentStrategy, 
    AgentRole, 
    StrategyType,
    MarketData
)
from goal_constraint_parser import parse_goal_constraints


class OptimizationObjective(Enum):
    """Portfolio optimization objectives."""
    MAXIMIZE_RETURN = "maximize_return"
    MINIMIZE_RISK = "minimize_risk"
    MAXIMIZE_SHARPE = "maximize_sharpe"
    MINIMIZE_DRAWDOWN = "minimize_drawdown"
    MAXIMIZE_UTILITY = "maximize_utility"
    MINIMIZE_COSTS = "minimize_costs"


class RiskMetric(Enum):
    """Risk analysis metrics."""
    VOLATILITY = "volatility"
    VAR_95 = "var_95"
    VAR_99 = "var_99"
    EXPECTED_SHORTFALL = "expected_shortfall"
    MAX_DRAWDOWN = "max_drawdown"
    TAIL_RISK = "tail_risk"
    CORRELATION_RISK = "correlation_risk"
    CONCENTRATION_RISK = "concentration_risk"


@dataclass
class ParetoPoint:
    """Represents a point on the Pareto frontier."""
    portfolio_id: str
    expected_return: float
    risk_score: float
    cost_score: float
    utility_score: float
    weights: Dict[str, float]
    source_agents: List[str]
    synthesis_method: str
    dominance_rank: int = 0
    pareto_efficient: bool = False


@dataclass
class RiskAnalysis:
    """Comprehensive risk analysis results."""
    volatility: float
    var_95: float
    var_99: float
    expected_shortfall: float
    max_drawdown: float
    beta: float
    correlation_matrix: np.ndarray
    tail_risk_score: float
    concentration_risk: float
    liquidity_risk: float
    stress_test_results: Dict[str, float]
    risk_attribution: Dict[str, float]


@dataclass
class CostAnalysis:
    """Cost analysis and optimization results."""
    total_expense_ratio: float
    transaction_costs: float
    bid_ask_spreads: float
    market_impact_costs: float
    rebalancing_costs: float
    tax_efficiency_score: float
    cost_per_basis_point: float
    fee_optimization_savings: float
    cost_breakdown: Dict[str, float]


@dataclass
class PortfolioSynthesis:
    """Result of portfolio synthesis process."""
    portfolio_id: str
    final_allocation: Dict[str, float]
    expected_return: float
    risk_score: float
    cost_score: float
    sharpe_ratio: float
    utility_score: float
    synthesis_confidence: float
    contributing_agents: List[str]
    pareto_rank: int
    optimization_method: str
    risk_analysis: RiskAnalysis
    cost_analysis: CostAnalysis
    improvement_metrics: Dict[str, float]


class NeuralDarkPool:
    """
    Advanced neural network-based risk analysis system.
    Simulates deep learning risk modeling for portfolio optimization.
    """
    
    def __init__(self, lookback_days: int = 252, confidence_levels: List[float] = None):
        """Initialize NeuralDarkPool risk analyzer."""
        self.lookback_days = lookback_days
        self.confidence_levels = confidence_levels or [0.95, 0.99]
        self.risk_models = self._initialize_risk_models()
        self.neural_weights = self._generate_neural_weights()
        
    def _initialize_risk_models(self) -> Dict[str, Any]:
        """Initialize simulated neural risk models."""
        return {
            'volatility_predictor': {
                'layers': [64, 32, 16, 1],
                'activation': 'relu',
                'weights': np.random.normal(0, 0.1, (64, 32))
            },
            'correlation_estimator': {
                'layers': [128, 64, 32, 16],
                'activation': 'tanh',
                'weights': np.random.normal(0, 0.05, (128, 64))
            },
            'tail_risk_detector': {
                'layers': [32, 16, 8, 1],
                'activation': 'sigmoid',
                'weights': np.random.normal(0, 0.2, (32, 16))
            },
            'regime_classifier': {
                'layers': [96, 48, 24, 4],
                'activation': 'softmax',
                'weights': np.random.normal(0, 0.1, (96, 48))
            }
        }
    
    def _generate_neural_weights(self) -> Dict[str, float]:
        """Generate neural network importance weights."""
        return {
            'market_stress': 0.25,
            'correlation_shifts': 0.20,
            'volatility_clustering': 0.18,
            'tail_dependencies': 0.15,
            'liquidity_dynamics': 0.12,
            'regime_changes': 0.10
        }
    
    async def analyze_portfolio_risk(self, allocation: Dict[str, float], 
                                   market_data: List[MarketData]) -> RiskAnalysis:
        """
        Perform comprehensive neural risk analysis on portfolio allocation.
        """
        # Simulate neural network processing
        await asyncio.sleep(0.01)  # Simulate computation time
        
        # Extract market features for analysis
        returns_data = self._extract_returns_data(market_data)
        
        # Neural volatility prediction
        volatility = self._predict_volatility(allocation, returns_data)
        
        # Value at Risk calculations
        var_95, var_99 = self._calculate_var(allocation, returns_data)
        
        # Expected Shortfall (Conditional VaR)
        expected_shortfall = self._calculate_expected_shortfall(allocation, returns_data)
        
        # Maximum Drawdown estimation
        max_drawdown = self._estimate_max_drawdown(allocation, returns_data)
        
        # Beta calculation (vs market)
        beta = self._calculate_portfolio_beta(allocation, returns_data)
        
        # Correlation matrix estimation
        correlation_matrix = self._estimate_correlation_matrix(allocation)
        
        # Advanced risk metrics
        tail_risk_score = self._calculate_tail_risk(allocation, returns_data)
        concentration_risk = self._calculate_concentration_risk(allocation)
        liquidity_risk = self._estimate_liquidity_risk(allocation)
        
        # Stress testing
        stress_test_results = self._perform_stress_tests(allocation, returns_data)
        
        # Risk attribution
        risk_attribution = self._calculate_risk_attribution(allocation)
        
        return RiskAnalysis(
            volatility=volatility,
            var_95=var_95,
            var_99=var_99,
            expected_shortfall=expected_shortfall,
            max_drawdown=max_drawdown,
            beta=beta,
            correlation_matrix=correlation_matrix,
            tail_risk_score=tail_risk_score,
            concentration_risk=concentration_risk,
            liquidity_risk=liquidity_risk,
            stress_test_results=stress_test_results,
            risk_attribution=risk_attribution
        )
    
    def _extract_returns_data(self, market_data: List[MarketData]) -> np.ndarray:
        """Extract returns data for analysis."""
        if len(market_data) < 2:
            return np.random.normal(0.0008, 0.015, (252, 6))  # Simulated returns
        
        # Calculate returns from market data
        prices = np.array([
            [d.spy_price, d.vix, d.ten_year_yield, d.dollar_index, d.oil_price, d.gold_price]
            for d in market_data[-self.lookback_days:]
        ])
        
        if len(prices) < 2:
            return np.random.normal(0.0008, 0.015, (252, 6))
        
        returns = np.diff(prices, axis=0) / prices[:-1]
        return returns
    
    def _predict_volatility(self, allocation: Dict[str, float], returns_data: np.ndarray) -> float:
        """Neural network volatility prediction."""
        # Simulate neural network prediction
        base_volatility = np.std(returns_data[:, 0]) * np.sqrt(252) if len(returns_data) > 0 else 0.15
        
        # Apply neural adjustments based on allocation
        allocation_risk = sum(w * self._get_asset_volatility(asset) for asset, w in allocation.items())
        
        # Neural enhancement factor
        neural_factor = 1.0 + np.random.normal(0, 0.1) * self.neural_weights['volatility_clustering']
        
        return max(0.05, allocation_risk * neural_factor)
    
    def _get_asset_volatility(self, asset: str) -> float:
        """Get asset-specific volatility estimates."""
        volatilities = {
            'Stocks': 0.16,
            'Bonds': 0.04,
            'Real Estate': 0.12,
            'Commodities': 0.20,
            'Cash': 0.01,
            'Alternatives': 0.18,
            'International': 0.18,
            'Emerging Markets': 0.25,
            'Technology': 0.22,
            'Healthcare': 0.14
        }
        return volatilities.get(asset, 0.15)
    
    def _calculate_var(self, allocation: Dict[str, float], 
                      returns_data: np.ndarray) -> Tuple[float, float]:
        """Calculate Value at Risk at different confidence levels."""
        portfolio_vol = self._predict_volatility(allocation, returns_data)
        
        # Assume normal distribution for simplicity (neural models would be more sophisticated)
        var_95 = -1.645 * portfolio_vol / np.sqrt(252)  # Daily VaR
        var_99 = -2.326 * portfolio_vol / np.sqrt(252)  # Daily VaR
        
        return var_95, var_99
    
    def _calculate_expected_shortfall(self, allocation: Dict[str, float], 
                                    returns_data: np.ndarray) -> float:
        """Calculate Expected Shortfall (Conditional VaR)."""
        var_95, _ = self._calculate_var(allocation, returns_data)
        
        # Expected Shortfall is typically 20-30% worse than VaR
        return var_95 * 1.25
    
    def _estimate_max_drawdown(self, allocation: Dict[str, float], 
                             returns_data: np.ndarray) -> float:
        """Estimate maximum drawdown using neural models."""
        portfolio_vol = self._predict_volatility(allocation, returns_data)
        
        # Neural estimation of max drawdown based on volatility and allocation
        base_drawdown = portfolio_vol * 0.8  # Rough approximation
        
        # Adjust for allocation concentration
        concentration_penalty = self._calculate_concentration_risk(allocation) * 0.1
        
        return min(0.6, base_drawdown + concentration_penalty)
    
    def _calculate_portfolio_beta(self, allocation: Dict[str, float], 
                                returns_data: np.ndarray) -> float:
        """Calculate portfolio beta versus market."""
        # Asset betas (vs market)
        asset_betas = {
            'Stocks': 1.0,
            'Bonds': 0.1,
            'Real Estate': 0.7,
            'Commodities': 0.3,
            'Cash': 0.0,
            'Alternatives': 0.6,
            'International': 0.8,
            'Technology': 1.3,
            'Healthcare': 0.9
        }
        
        portfolio_beta = sum(w * asset_betas.get(asset, 0.8) for asset, w in allocation.items())
        return portfolio_beta
    
    def _estimate_correlation_matrix(self, allocation: Dict[str, float]) -> np.ndarray:
        """Estimate correlation matrix using neural models."""
        assets = list(allocation.keys())
        n_assets = len(assets)
        
        # Generate realistic correlation matrix
        base_corr = np.random.uniform(0.1, 0.7, (n_assets, n_assets))
        corr_matrix = (base_corr + base_corr.T) / 2  # Make symmetric
        np.fill_diagonal(corr_matrix, 1.0)  # Diagonal = 1
        
        # Ensure positive semi-definite
        eigenvals, eigenvecs = np.linalg.eigh(corr_matrix)
        eigenvals = np.maximum(eigenvals, 0.01)  # Ensure positive
        corr_matrix = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
        
        return corr_matrix
    
    def _calculate_tail_risk(self, allocation: Dict[str, float], 
                           returns_data: np.ndarray) -> float:
        """Calculate tail risk score using neural models."""
        # Simulate neural tail risk detection
        portfolio_vol = self._predict_volatility(allocation, returns_data)
        concentration = self._calculate_concentration_risk(allocation)
        
        # Neural tail risk model
        tail_features = np.array([portfolio_vol, concentration, len(allocation)])
        tail_risk = 0.3 + 0.4 * np.tanh(tail_features[0] * 2) + 0.3 * tail_features[1]
        
        return min(1.0, max(0.0, tail_risk))
    
    def _calculate_concentration_risk(self, allocation: Dict[str, float]) -> float:
        """Calculate portfolio concentration risk."""
        weights = np.array(list(allocation.values()))
        
        # Herfindahl-Hirschman Index
        hhi = np.sum(weights ** 2)
        
        # Normalize to 0-1 scale
        max_hhi = 1.0  # Single asset
        min_hhi = 1.0 / len(allocation)  # Equal weights
        
        if max_hhi == min_hhi:
            return 0.0
        
        concentration_risk = (hhi - min_hhi) / (max_hhi - min_hhi)
        return min(1.0, max(0.0, concentration_risk))
    
    def _estimate_liquidity_risk(self, allocation: Dict[str, float]) -> float:
        """Estimate portfolio liquidity risk."""
        # Asset liquidity scores (higher = more liquid)
        liquidity_scores = {
            'Stocks': 0.9,
            'Bonds': 0.7,
            'Real Estate': 0.3,
            'Commodities': 0.6,
            'Cash': 1.0,
            'Alternatives': 0.2,
            'International': 0.7,
            'Technology': 0.8,
            'Healthcare': 0.8
        }
        
        weighted_liquidity = sum(w * liquidity_scores.get(asset, 0.5) 
                               for asset, w in allocation.items())
        
        # Convert to risk score (lower liquidity = higher risk)
        liquidity_risk = 1.0 - weighted_liquidity
        return max(0.0, min(1.0, liquidity_risk))
    
    def _perform_stress_tests(self, allocation: Dict[str, float], 
                            returns_data: np.ndarray) -> Dict[str, float]:
        """Perform stress testing scenarios."""
        base_vol = self._predict_volatility(allocation, returns_data)
        base_return = sum(w * self._get_asset_expected_return(asset) 
                         for asset, w in allocation.items())
        
        stress_scenarios = {
            'market_crash_2008': base_return - 3.5 * base_vol,
            'covid_shock_2020': base_return - 2.8 * base_vol,
            'tech_bubble_2000': base_return - 4.2 * base_vol,
            'inflation_spike': base_return - 1.5 * base_vol,
            'interest_rate_shock': base_return - 2.0 * base_vol,
            'geopolitical_crisis': base_return - 2.5 * base_vol,
            'liquidity_crisis': base_return - 3.0 * base_vol
        }
        
        return stress_scenarios
    
    def _get_asset_expected_return(self, asset: str) -> float:
        """Get asset expected returns."""
        expected_returns = {
            'Stocks': 0.10,
            'Bonds': 0.04,
            'Real Estate': 0.08,
            'Commodities': 0.06,
            'Cash': 0.02,
            'Alternatives': 0.12,
            'International': 0.09,
            'Technology': 0.12,
            'Healthcare': 0.10
        }
        return expected_returns.get(asset, 0.08)
    
    def _calculate_risk_attribution(self, allocation: Dict[str, float]) -> Dict[str, float]:
        """Calculate risk attribution by asset class."""
        portfolio_vol = sum(w * self._get_asset_volatility(asset) 
                          for asset, w in allocation.items())
        
        risk_attribution = {}
        for asset, weight in allocation.items():
            asset_vol = self._get_asset_volatility(asset)
            risk_contribution = (weight * asset_vol) / portfolio_vol if portfolio_vol > 0 else 0
            risk_attribution[asset] = risk_contribution
        
        return risk_attribution


class FeeAnnihilator:
    """
    Advanced cost optimization system for portfolio management.
    Minimizes fees, transaction costs, and tax impacts.
    """
    
    def __init__(self, tax_rate: float = 0.25, rebalancing_threshold: float = 0.05):
        """Initialize FeeAnnihilator cost optimizer."""
        self.tax_rate = tax_rate
        self.rebalancing_threshold = rebalancing_threshold
        self.cost_models = self._initialize_cost_models()
        
    def _initialize_cost_models(self) -> Dict[str, Any]:
        """Initialize cost optimization models."""
        return {
            'expense_ratios': {
                'Stocks': 0.0050,  # 0.50% annual
                'Bonds': 0.0030,   # 0.30% annual
                'Real Estate': 0.0075,  # 0.75% annual
                'Commodities': 0.0065,  # 0.65% annual
                'Cash': 0.0000,    # 0.00% annual
                'Alternatives': 0.0120,  # 1.20% annual
                'International': 0.0070,  # 0.70% annual
                'Technology': 0.0045,   # 0.45% annual
                'Healthcare': 0.0040    # 0.40% annual
            },
            'transaction_costs': {
                'Stocks': 0.0005,  # 5 bps
                'Bonds': 0.0008,   # 8 bps
                'Real Estate': 0.0015,  # 15 bps
                'Commodities': 0.0012,  # 12 bps
                'Cash': 0.0000,    # 0 bps
                'Alternatives': 0.0025,  # 25 bps
                'International': 0.0010,  # 10 bps
                'Technology': 0.0006,   # 6 bps
                'Healthcare': 0.0005    # 5 bps
            },
            'bid_ask_spreads': {
                'Stocks': 0.0002,  # 2 bps
                'Bonds': 0.0005,   # 5 bps
                'Real Estate': 0.0010,  # 10 bps
                'Commodities': 0.0008,  # 8 bps
                'Cash': 0.0000,    # 0 bps
                'Alternatives': 0.0020,  # 20 bps
                'International': 0.0006,  # 6 bps
                'Technology': 0.0003,   # 3 bps
                'Healthcare': 0.0002    # 2 bps
            }
        }
    
    async def optimize_costs(self, allocation: Dict[str, float], 
                           portfolio_value: float = 100000,
                           turnover_rate: float = 0.5) -> CostAnalysis:
        """
        Perform comprehensive cost optimization analysis.
        """
        # Calculate total expense ratio
        total_expense_ratio = self._calculate_expense_ratio(allocation)
        
        # Calculate transaction costs
        transaction_costs = self._calculate_transaction_costs(allocation, portfolio_value, turnover_rate)
        
        # Calculate bid-ask spread costs
        bid_ask_spreads = self._calculate_bid_ask_costs(allocation, portfolio_value, turnover_rate)
        
        # Calculate market impact costs
        market_impact_costs = self._calculate_market_impact_costs(allocation, portfolio_value)
        
        # Calculate rebalancing costs
        rebalancing_costs = self._calculate_rebalancing_costs(allocation, portfolio_value)
        
        # Calculate tax efficiency score
        tax_efficiency_score = self._calculate_tax_efficiency(allocation)
        
        # Calculate cost per basis point
        total_costs = (total_expense_ratio + transaction_costs + bid_ask_spreads + 
                      market_impact_costs + rebalancing_costs)
        cost_per_basis_point = total_costs * 10000  # Convert to basis points
        
        # Calculate fee optimization savings
        fee_optimization_savings = self._calculate_optimization_savings(allocation)
        
        # Create cost breakdown
        cost_breakdown = {
            'expense_ratios': total_expense_ratio,
            'transaction_costs': transaction_costs,
            'bid_ask_spreads': bid_ask_spreads,
            'market_impact': market_impact_costs,
            'rebalancing': rebalancing_costs,
            'tax_drag': (1.0 - tax_efficiency_score) * 0.01  # Estimated tax drag
        }
        
        return CostAnalysis(
            total_expense_ratio=total_expense_ratio,
            transaction_costs=transaction_costs,
            bid_ask_spreads=bid_ask_spreads,
            market_impact_costs=market_impact_costs,
            rebalancing_costs=rebalancing_costs,
            tax_efficiency_score=tax_efficiency_score,
            cost_per_basis_point=cost_per_basis_point,
            fee_optimization_savings=fee_optimization_savings,
            cost_breakdown=cost_breakdown
        )
    
    def _calculate_expense_ratio(self, allocation: Dict[str, float]) -> float:
        """Calculate weighted average expense ratio."""
        expense_ratios = self.cost_models['expense_ratios']
        total_expense_ratio = sum(w * expense_ratios.get(asset, 0.006) 
                                for asset, w in allocation.items())
        return total_expense_ratio
    
    def _calculate_transaction_costs(self, allocation: Dict[str, float], 
                                   portfolio_value: float, turnover_rate: float) -> float:
        """Calculate transaction costs based on turnover."""
        transaction_costs = self.cost_models['transaction_costs']
        weighted_transaction_cost = sum(w * transaction_costs.get(asset, 0.001) 
                                      for asset, w in allocation.items())
        
        # Apply turnover rate
        annual_transaction_costs = weighted_transaction_cost * turnover_rate
        return annual_transaction_costs
    
    def _calculate_bid_ask_costs(self, allocation: Dict[str, float], 
                               portfolio_value: float, turnover_rate: float) -> float:
        """Calculate bid-ask spread costs."""
        bid_ask_spreads = self.cost_models['bid_ask_spreads']
        weighted_bid_ask_cost = sum(w * bid_ask_spreads.get(asset, 0.0005) 
                                  for asset, w in allocation.items())
        
        # Apply turnover rate
        annual_bid_ask_costs = weighted_bid_ask_cost * turnover_rate
        return annual_bid_ask_costs
    
    def _calculate_market_impact_costs(self, allocation: Dict[str, float], 
                                     portfolio_value: float) -> float:
        """Calculate market impact costs based on portfolio size."""
        # Market impact increases with trade size and decreases with liquidity
        base_impact = 0.0002  # 2 bps base impact
        
        # Size factor (larger portfolios have higher impact)
        size_factor = min(2.0, portfolio_value / 1000000)  # Cap at 2x for $1M+
        
        # Liquidity adjustment
        liquidity_weights = {
            'Stocks': 1.0,      # Highly liquid
            'Bonds': 1.2,       # Moderately liquid
            'Real Estate': 2.0, # Less liquid
            'Commodities': 1.5, # Moderately liquid
            'Cash': 0.0,        # No impact
            'Alternatives': 3.0, # Illiquid
            'International': 1.3,
            'Technology': 1.0,
            'Healthcare': 1.1
        }
        
        weighted_impact = sum(w * base_impact * liquidity_weights.get(asset, 1.5) 
                            for asset, w in allocation.items())
        
        return weighted_impact * size_factor
    
    def _calculate_rebalancing_costs(self, allocation: Dict[str, float], 
                                   portfolio_value: float) -> float:
        """Calculate costs associated with portfolio rebalancing."""
        # Assume quarterly rebalancing
        rebalancing_frequency = 4  # times per year
        
        # Average rebalancing amount (percentage of portfolio that needs rebalancing)
        avg_rebalancing_amount = 0.1  # 10% of portfolio on average
        
        # Transaction costs for rebalancing
        avg_transaction_cost = sum(w * self.cost_models['transaction_costs'].get(asset, 0.001) 
                                 for asset, w in allocation.items())
        
        annual_rebalancing_costs = (avg_transaction_cost * avg_rebalancing_amount * 
                                  rebalancing_frequency)
        
        return annual_rebalancing_costs
    
    def _calculate_tax_efficiency(self, allocation: Dict[str, float]) -> float:
        """Calculate tax efficiency score (0-1, higher is better)."""
        # Tax efficiency by asset class
        tax_efficiency_scores = {
            'Stocks': 0.85,      # Tax-efficient index funds
            'Bonds': 0.70,       # Interest taxed as income
            'Real Estate': 0.80, # Some tax advantages
            'Commodities': 0.60, # Complex tax treatment
            'Cash': 0.95,        # No capital gains
            'Alternatives': 0.50, # Often tax-inefficient
            'International': 0.75, # Foreign tax credits
            'Technology': 0.85,   # Growth-oriented, tax-efficient
            'Healthcare': 0.85    # Growth-oriented, tax-efficient
        }
        
        weighted_tax_efficiency = sum(w * tax_efficiency_scores.get(asset, 0.75) 
                                    for asset, w in allocation.items())
        
        return weighted_tax_efficiency
    
    def _calculate_optimization_savings(self, allocation: Dict[str, float]) -> float:
        """Calculate potential savings from fee optimization."""
        # Compare to high-cost alternatives
        high_cost_expense_ratios = {
            'Stocks': 0.015,     # 1.50% (actively managed)
            'Bonds': 0.012,      # 1.20% (actively managed)
            'Real Estate': 0.020, # 2.00% (real estate funds)
            'Commodities': 0.018, # 1.80% (commodity funds)
            'Cash': 0.005,       # 0.50% (money market funds)
            'Alternatives': 0.025, # 2.50% (hedge funds)
            'International': 0.016,
            'Technology': 0.014,
            'Healthcare': 0.013
        }
        
        current_costs = self._calculate_expense_ratio(allocation)
        high_cost_alternative = sum(w * high_cost_expense_ratios.get(asset, 0.015) 
                                  for asset, w in allocation.items())
        
        savings = high_cost_alternative - current_costs
        return max(0.0, savings)
    
    def optimize_allocation_for_costs(self, allocation: Dict[str, float]) -> Dict[str, float]:
        """Optimize allocation to minimize costs while maintaining diversification."""
        # Simple cost optimization: increase weights of low-cost assets
        expense_ratios = self.cost_models['expense_ratios']
        
        # Calculate cost efficiency scores (inverse of expense ratios)
        cost_efficiency = {asset: 1.0 / (expense_ratios.get(asset, 0.006) + 0.001) 
                          for asset in allocation}
        
        # Normalize efficiency scores
        total_efficiency = sum(cost_efficiency.values())
        efficiency_weights = {asset: eff / total_efficiency 
                            for asset, eff in cost_efficiency.items()}
        
        # Blend with original allocation (70% original, 30% cost-optimized)
        optimized_allocation = {}
        for asset in allocation:
            original_weight = allocation[asset]
            efficiency_weight = efficiency_weights[asset]
            optimized_weight = 0.7 * original_weight + 0.3 * efficiency_weight
            optimized_allocation[asset] = optimized_weight
        
        # Normalize to sum to 1.0
        total_weight = sum(optimized_allocation.values())
        if total_weight > 0:
            optimized_allocation = {asset: weight / total_weight 
                                  for asset, weight in optimized_allocation.items()}
        
        return optimized_allocation


class ParetoOptimizer:
    """
    Pareto frontier optimization for multi-objective portfolio optimization.
    """
    
    def __init__(self, objectives: List[OptimizationObjective] = None):
        """Initialize Pareto optimizer."""
        self.objectives = objectives or [
            OptimizationObjective.MAXIMIZE_RETURN,
            OptimizationObjective.MINIMIZE_RISK,
            OptimizationObjective.MINIMIZE_COSTS
        ]
        self.pareto_points: List[ParetoPoint] = []
        
    def find_pareto_frontier(self, agent_proposals: List[AgentStrategy]) -> List[ParetoPoint]:
        """
        Find Pareto-optimal frontier from agent proposals.
        """
        if not agent_proposals:
            return []
        
        # Convert agent strategies to candidate points
        candidate_points = []
        for i, strategy in enumerate(agent_proposals):
            point = ParetoPoint(
                portfolio_id=f"portfolio_{i:03d}",
                expected_return=strategy.expected_return,
                risk_score=strategy.risk_score,
                cost_score=self._estimate_cost_score(strategy),
                utility_score=self._calculate_utility_score(strategy),
                weights=strategy.asset_allocation,
                source_agents=[strategy.agent_name],
                synthesis_method="single_agent",
                dominance_rank=0,
                pareto_efficient=False
            )
            candidate_points.append(point)
        
        # Find Pareto-efficient points
        pareto_points = self._identify_pareto_efficient(candidate_points)
        
        # Generate synthetic points through interpolation
        synthetic_points = self._generate_synthetic_points(agent_proposals)
        all_points = pareto_points + synthetic_points
        
        # Re-evaluate Pareto efficiency with synthetic points
        final_pareto_points = self._identify_pareto_efficient(all_points)
        
        # Rank points by dominance
        self._rank_by_dominance(final_pareto_points)
        
        self.pareto_points = final_pareto_points
        return final_pareto_points
    
    def _estimate_cost_score(self, strategy: AgentStrategy) -> float:
        """Estimate cost score for a strategy."""
        # Simple cost estimation based on allocation complexity
        num_assets = len([w for w in strategy.asset_allocation.values() if w > 0.01])
        complexity_penalty = num_assets * 0.0005  # 5 bps per asset
        
        # Base cost estimate
        base_cost = 0.005  # 50 bps base cost
        
        return base_cost + complexity_penalty
    
    def _calculate_utility_score(self, strategy: AgentStrategy) -> float:
        """Calculate utility score combining return, risk, and other factors."""
        # Simple utility function: Return - 0.5 * Risk^2
        utility = strategy.expected_return - 0.5 * (strategy.risk_score ** 2)
        
        # Add timeline fit bonus
        utility += strategy.timeline_fit * 0.02
        
        # Add capital efficiency bonus
        utility += strategy.capital_efficiency * 0.01
        
        return utility
    
    def _identify_pareto_efficient(self, points: List[ParetoPoint]) -> List[ParetoPoint]:
        """Identify Pareto-efficient points from candidates."""
        if not points:
            return []
        
        pareto_efficient = []
        
        for i, point_a in enumerate(points):
            is_dominated = False
            
            for j, point_b in enumerate(points):
                if i == j:
                    continue
                
                # Check if point_b dominates point_a
                if self._dominates(point_b, point_a):
                    is_dominated = True
                    break
            
            if not is_dominated:
                point_a.pareto_efficient = True
                pareto_efficient.append(point_a)
        
        return pareto_efficient
    
    def _dominates(self, point_a: ParetoPoint, point_b: ParetoPoint) -> bool:
        """Check if point_a dominates point_b."""
        # Point A dominates point B if:
        # 1. A is at least as good as B in all objectives
        # 2. A is strictly better than B in at least one objective
        
        # For maximization objectives (return, utility), higher is better
        # For minimization objectives (risk, cost), lower is better
        
        better_return = point_a.expected_return >= point_b.expected_return
        better_risk = point_a.risk_score <= point_b.risk_score
        better_cost = point_a.cost_score <= point_b.cost_score
        better_utility = point_a.utility_score >= point_b.utility_score
        
        # All objectives must be at least as good
        at_least_as_good = better_return and better_risk and better_cost and better_utility
        
        # At least one objective must be strictly better
        strictly_better = (point_a.expected_return > point_b.expected_return or
                          point_a.risk_score < point_b.risk_score or
                          point_a.cost_score < point_b.cost_score or
                          point_a.utility_score > point_b.utility_score)
        
        return at_least_as_good and strictly_better
    
    def _generate_synthetic_points(self, agent_proposals: List[AgentStrategy]) -> List[ParetoPoint]:
        """Generate synthetic portfolio points through interpolation and optimization."""
        if len(agent_proposals) < 2:
            return []
        
        synthetic_points = []
        
        # Generate convex combinations of agent proposals
        for i in range(len(agent_proposals)):
            for j in range(i + 1, len(agent_proposals)):
                for alpha in [0.25, 0.5, 0.75]:  # Interpolation weights
                    synthetic_point = self._interpolate_strategies(
                        agent_proposals[i], agent_proposals[j], alpha
                    )
                    if synthetic_point:
                        synthetic_points.append(synthetic_point)
        
        # Generate optimized points for specific objectives
        optimized_points = self._generate_optimized_points(agent_proposals)
        synthetic_points.extend(optimized_points)
        
        return synthetic_points
    
    def _interpolate_strategies(self, strategy_a: AgentStrategy, strategy_b: AgentStrategy, 
                              alpha: float) -> Optional[ParetoPoint]:
        """Create interpolated strategy between two agent strategies."""
        try:
            # Interpolate asset allocations
            all_assets = set(strategy_a.asset_allocation.keys()) | set(strategy_b.asset_allocation.keys())
            
            interpolated_allocation = {}
            for asset in all_assets:
                weight_a = strategy_a.asset_allocation.get(asset, 0.0)
                weight_b = strategy_b.asset_allocation.get(asset, 0.0)
                interpolated_weight = alpha * weight_a + (1 - alpha) * weight_b
                if interpolated_weight > 0.001:  # Only include meaningful weights
                    interpolated_allocation[asset] = interpolated_weight
            
            # Normalize weights
            total_weight = sum(interpolated_allocation.values())
            if total_weight > 0:
                interpolated_allocation = {asset: weight / total_weight 
                                         for asset, weight in interpolated_allocation.items()}
            else:
                return None
            
            # Interpolate performance metrics
            expected_return = alpha * strategy_a.expected_return + (1 - alpha) * strategy_b.expected_return
            risk_score = alpha * strategy_a.risk_score + (1 - alpha) * strategy_b.risk_score
            cost_score = self._estimate_cost_from_allocation(interpolated_allocation)
            
            # Create synthetic strategy for utility calculation
            synthetic_strategy = AgentStrategy(
                agent_id="synthetic",
                agent_name="interpolated",
                agent_role=strategy_a.agent_role,
                strategy_type=strategy_a.strategy_type,
                asset_allocation=interpolated_allocation,
                expected_return=expected_return,
                risk_score=risk_score,
                timeline_fit=(strategy_a.timeline_fit + strategy_b.timeline_fit) / 2,
                capital_efficiency=(strategy_a.capital_efficiency + strategy_b.capital_efficiency) / 2
            )
            
            utility_score = self._calculate_utility_score(synthetic_strategy)
            
            return ParetoPoint(
                portfolio_id=f"interpolated_{strategy_a.agent_id}_{strategy_b.agent_id}_{alpha:.2f}",
                expected_return=expected_return,
                risk_score=risk_score,
                cost_score=cost_score,
                utility_score=utility_score,
                weights=interpolated_allocation,
                source_agents=[strategy_a.agent_name, strategy_b.agent_name],
                synthesis_method=f"interpolation_{alpha:.2f}",
                dominance_rank=0,
                pareto_efficient=False
            )
        
        except Exception as e:
            print(f"Error interpolating strategies: {e}")
            return None
    
    def _estimate_cost_from_allocation(self, allocation: Dict[str, float]) -> float:
        """Estimate cost score from allocation."""
        # Use FeeAnnihilator for more accurate cost estimation
        fee_annihilator = FeeAnnihilator()
        expense_ratio = fee_annihilator._calculate_expense_ratio(allocation)
        
        # Add complexity penalty
        num_assets = len([w for w in allocation.values() if w > 0.01])
        complexity_penalty = num_assets * 0.0003
        
        return expense_ratio + complexity_penalty
    
    def _generate_optimized_points(self, agent_proposals: List[AgentStrategy]) -> List[ParetoPoint]:
        """Generate points optimized for specific objectives."""
        optimized_points = []
        
        # Extract all unique assets
        all_assets = set()
        for strategy in agent_proposals:
            all_assets.update(strategy.asset_allocation.keys())
        all_assets = list(all_assets)
        
        if not all_assets:
            return []
        
        # Generate points optimized for different objectives
        try:
            # Maximum return portfolio
            max_return_point = self._optimize_for_objective(
                all_assets, agent_proposals, OptimizationObjective.MAXIMIZE_RETURN
            )
            if max_return_point:
                optimized_points.append(max_return_point)
            
            # Minimum risk portfolio
            min_risk_point = self._optimize_for_objective(
                all_assets, agent_proposals, OptimizationObjective.MINIMIZE_RISK
            )
            if min_risk_point:
                optimized_points.append(min_risk_point)
            
            # Minimum cost portfolio
            min_cost_point = self._optimize_for_objective(
                all_assets, agent_proposals, OptimizationObjective.MINIMIZE_COSTS
            )
            if min_cost_point:
                optimized_points.append(min_cost_point)
            
            # Maximum Sharpe ratio portfolio
            max_sharpe_point = self._optimize_for_objective(
                all_assets, agent_proposals, OptimizationObjective.MAXIMIZE_SHARPE
            )
            if max_sharpe_point:
                optimized_points.append(max_sharpe_point)
        
        except Exception as e:
            print(f"Error generating optimized points: {e}")
        
        return optimized_points
    
    def _optimize_for_objective(self, assets: List[str], agent_proposals: List[AgentStrategy], 
                              objective: OptimizationObjective) -> Optional[ParetoPoint]:
        """Optimize portfolio for a specific objective."""
        try:
            n_assets = len(assets)
            
            # Define optimization bounds and constraints
            bounds = [(0.0, 1.0) for _ in range(n_assets)]  # Weights between 0 and 1
            constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}]  # Sum to 1
            
            # Initial guess (equal weights)
            x0 = np.ones(n_assets) / n_assets
            
            # Define objective function based on optimization target
            def objective_function(weights):
                allocation = {assets[i]: weights[i] for i in range(n_assets)}
                
                if objective == OptimizationObjective.MAXIMIZE_RETURN:
                    return -self._estimate_return_from_allocation(allocation)
                elif objective == OptimizationObjective.MINIMIZE_RISK:
                    return self._estimate_risk_from_allocation(allocation)
                elif objective == OptimizationObjective.MINIMIZE_COSTS:
                    return self._estimate_cost_from_allocation(allocation)
                elif objective == OptimizationObjective.MAXIMIZE_SHARPE:
                    ret = self._estimate_return_from_allocation(allocation)
                    risk = self._estimate_risk_from_allocation(allocation)
                    return -(ret - 0.02) / max(risk, 0.001)  # Risk-free rate = 2%
                else:
                    return 0.0
            
            # Optimize
            result = optimize.minimize(
                objective_function, x0, method='SLSQP', 
                bounds=bounds, constraints=constraints,
                options={'maxiter': 1000}
            )
            
            if result.success:
                optimal_weights = result.x
                allocation = {assets[i]: optimal_weights[i] for i in range(n_assets) 
                            if optimal_weights[i] > 0.001}
                
                # Normalize allocation
                total_weight = sum(allocation.values())
                if total_weight > 0:
                    allocation = {asset: weight / total_weight 
                                for asset, weight in allocation.items()}
                
                expected_return = self._estimate_return_from_allocation(allocation)
                risk_score = self._estimate_risk_from_allocation(allocation)
                cost_score = self._estimate_cost_from_allocation(allocation)
                
                # Create synthetic strategy for utility calculation
                synthetic_strategy = AgentStrategy(
                    agent_id="optimized",
                    agent_name="optimized",
                    agent_role=AgentRole.PORTFOLIO_MANAGER,
                    strategy_type=StrategyType.QUANTITATIVE,
                    asset_allocation=allocation,
                    expected_return=expected_return,
                    risk_score=risk_score,
                    timeline_fit=0.8,
                    capital_efficiency=0.8
                )
                
                utility_score = self._calculate_utility_score(synthetic_strategy)
                
                return ParetoPoint(
                    portfolio_id=f"optimized_{objective.value}",
                    expected_return=expected_return,
                    risk_score=risk_score,
                    cost_score=cost_score,
                    utility_score=utility_score,
                    weights=allocation,
                    source_agents=["optimizer"],
                    synthesis_method=f"optimization_{objective.value}",
                    dominance_rank=0,
                    pareto_efficient=False
                )
        
        except Exception as e:
            print(f"Error optimizing for {objective.value}: {e}")
            return None
    
    def _estimate_return_from_allocation(self, allocation: Dict[str, float]) -> float:
        """Estimate expected return from allocation."""
        # Asset expected returns
        expected_returns = {
            'Stocks': 0.10,
            'Bonds': 0.04,
            'Real Estate': 0.08,
            'Commodities': 0.06,
            'Cash': 0.02,
            'Alternatives': 0.12,
            'International': 0.09,
            'Technology': 0.12,
            'Healthcare': 0.10
        }
        
        portfolio_return = sum(w * expected_returns.get(asset, 0.08) 
                             for asset, w in allocation.items())
        return portfolio_return
    
    def _estimate_risk_from_allocation(self, allocation: Dict[str, float]) -> float:
        """Estimate risk from allocation."""
        # Asset volatilities
        volatilities = {
            'Stocks': 0.16,
            'Bonds': 0.04,
            'Real Estate': 0.12,
            'Commodities': 0.20,
            'Cash': 0.01,
            'Alternatives': 0.18,
            'International': 0.18,
            'Technology': 0.22,
            'Healthcare': 0.14
        }
        
        portfolio_vol = sum(w * volatilities.get(asset, 0.15) 
                          for asset, w in allocation.items())
        return portfolio_vol
    
    def _rank_by_dominance(self, points: List[ParetoPoint]):
        """Rank points by dominance level."""
        for point in points:
            dominance_count = 0
            for other_point in points:
                if point != other_point and self._dominates(point, other_point):
                    dominance_count += 1
            point.dominance_rank = dominance_count
        
        # Sort by dominance rank (higher rank = dominates more points)
        points.sort(key=lambda p: p.dominance_rank, reverse=True)


class PortfolioSurgeon:
    """
    Main Portfolio Surgeon class that synthesizes agent proposals using Pareto-optimal logic,
    integrated with NeuralDarkPool for risk analysis and FeeAnnihilator for cost optimization.
    """
    
    def __init__(self, tax_rate: float = 0.25, rebalancing_threshold: float = 0.05):
        """Initialize Portfolio Surgeon."""
        self.neural_darkpool = NeuralDarkPool()
        self.fee_annihilator = FeeAnnihilator(tax_rate, rebalancing_threshold)
        self.pareto_optimizer = ParetoOptimizer()
        self.synthesis_history: List[PortfolioSynthesis] = []
        
    async def synthesize_portfolio(self, agent_proposals: List[AgentStrategy], 
                                 client_goals: Dict[str, Any],
                                 market_data: List[MarketData],
                                 portfolio_value: float = 100000) -> PortfolioSynthesis:
        """
        Main synthesis method that combines all components to create optimal portfolio.
        """
        if not agent_proposals:
            raise ValueError("No agent proposals provided for synthesis")
        
        print(f"🔬 PORTFOLIO SURGEON: Synthesizing {len(agent_proposals)} agent proposals")
        
        # Step 1: Find Pareto frontier
        print("   📊 Finding Pareto-optimal frontier...")
        pareto_points = self.pareto_optimizer.find_pareto_frontier(agent_proposals)
        
        if not pareto_points:
            raise ValueError("No Pareto-optimal points found")
        
        print(f"   ✅ Found {len(pareto_points)} Pareto-optimal points")
        
        # Step 2: Select best point based on client preferences
        print("   🎯 Selecting optimal portfolio based on client preferences...")
        selected_point = self._select_optimal_point(pareto_points, client_goals)
        
        # Step 3: Apply NeuralDarkPool risk analysis
        print("   🧠 Running NeuralDarkPool risk analysis...")
        risk_analysis = await self.neural_darkpool.analyze_portfolio_risk(
            selected_point.weights, market_data
        )
        
        # Step 4: Apply FeeAnnihilator cost optimization
        print("   💰 Running FeeAnnihilator cost optimization...")
        cost_analysis = await self.fee_annihilator.optimize_costs(
            selected_point.weights, portfolio_value
        )
        
        # Step 5: Final optimization and synthesis
        print("   🔧 Performing final portfolio optimization...")
        final_allocation = self._apply_final_optimization(
            selected_point.weights, risk_analysis, cost_analysis, client_goals
        )
        
        # Step 6: Calculate performance metrics
        final_metrics = self._calculate_final_metrics(
            final_allocation, risk_analysis, cost_analysis
        )
        
        # Step 7: Create synthesis result
        synthesis_result = PortfolioSynthesis(
            portfolio_id=f"synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            final_allocation=final_allocation,
            expected_return=final_metrics['expected_return'],
            risk_score=risk_analysis.volatility,
            cost_score=cost_analysis.total_expense_ratio,
            sharpe_ratio=final_metrics['sharpe_ratio'],
            utility_score=final_metrics['utility_score'],
            synthesis_confidence=self._calculate_synthesis_confidence(agent_proposals, selected_point),
            contributing_agents=selected_point.source_agents,
            pareto_rank=selected_point.dominance_rank,
            optimization_method=selected_point.synthesis_method,
            risk_analysis=risk_analysis,
            cost_analysis=cost_analysis,
            improvement_metrics=self._calculate_improvement_metrics(
                agent_proposals, final_allocation, final_metrics
            )
        )
        
        # Store in history
        self.synthesis_history.append(synthesis_result)
        
        print("   ✅ Portfolio synthesis complete!")
        
        return synthesis_result
    
    def _select_optimal_point(self, pareto_points: List[ParetoPoint], 
                            client_goals: Dict[str, Any]) -> ParetoPoint:
        """Select optimal Pareto point based on client preferences."""
        if len(pareto_points) == 1:
            return pareto_points[0]
        
        # Extract client preferences with safe handling
        goals = client_goals.get('goals', {}) if client_goals else {}
        risk_tolerance_raw = goals.get('risk_tolerance', 'moderate')
        strategy_raw = goals.get('strategy', 'balanced')
        timeline_raw = goals.get('timeline', 'medium-term')
        
        # Safely convert to lowercase
        risk_tolerance = risk_tolerance_raw.lower() if risk_tolerance_raw else 'moderate'
        strategy = strategy_raw.lower() if strategy_raw else 'balanced'
        timeline = timeline_raw.lower() if timeline_raw else 'medium-term'
        
        # Define scoring weights based on client preferences
        weights = self._get_client_preference_weights(risk_tolerance, strategy, timeline)
        
        # Score each Pareto point
        best_point = None
        best_score = -float('inf')
        
        for point in pareto_points:
            score = (
                weights['return'] * point.expected_return * 10 +  # Scale return
                weights['risk'] * (1.0 - point.risk_score) * 10 +  # Lower risk is better
                weights['cost'] * (1.0 - point.cost_score) * 100 +  # Lower cost is better
                weights['utility'] * point.utility_score * 10
            )
            
            if score > best_score:
                best_score = score
                best_point = point
        
        return best_point or pareto_points[0]
    
    def _get_client_preference_weights(self, risk_tolerance: str, strategy: str, 
                                     timeline: str) -> Dict[str, float]:
        """Get preference weights based on client characteristics."""
        # Base weights
        weights = {'return': 0.3, 'risk': 0.3, 'cost': 0.2, 'utility': 0.2}
        
        # Adjust based on risk tolerance
        if 'conservative' in risk_tolerance or 'low' in risk_tolerance:
            weights['risk'] = 0.5
            weights['return'] = 0.2
        elif 'aggressive' in risk_tolerance or 'high' in risk_tolerance:
            weights['return'] = 0.5
            weights['risk'] = 0.1
        
        # Adjust based on strategy
        if 'growth' in strategy or 'aggressive' in strategy:
            weights['return'] += 0.1
            weights['risk'] -= 0.05
        elif 'income' in strategy or 'conservative' in strategy:
            weights['risk'] += 0.1
            weights['return'] -= 0.05
        
        # Adjust based on timeline
        if 'short' in timeline:
            weights['risk'] += 0.1
            weights['cost'] += 0.05
        elif 'long' in timeline:
            weights['return'] += 0.1
            weights['cost'] -= 0.05
        
        # Normalize weights
        total = sum(weights.values())
        return {k: v/total for k, v in weights.items()}
    
    def _apply_final_optimization(self, base_allocation: Dict[str, float],
                                risk_analysis: RiskAnalysis,
                                cost_analysis: CostAnalysis,
                                client_goals: Dict[str, Any]) -> Dict[str, float]:
        """Apply final optimization adjustments."""
        optimized_allocation = base_allocation.copy()
        
        # Apply cost optimization
        if cost_analysis.total_expense_ratio > 0.008:  # If costs are high (>80 bps)
            cost_optimized = self.fee_annihilator.optimize_allocation_for_costs(base_allocation)
            # Blend with original (80% original, 20% cost-optimized)
            for asset in optimized_allocation:
                original_weight = optimized_allocation[asset]
                cost_weight = cost_optimized.get(asset, 0)
                optimized_allocation[asset] = 0.8 * original_weight + 0.2 * cost_weight
        
        # Apply risk adjustments
        if risk_analysis.concentration_risk > 0.7:  # High concentration risk
            # Diversify by reducing largest positions
            sorted_assets = sorted(optimized_allocation.items(), key=lambda x: x[1], reverse=True)
            max_weight = 0.4  # Cap at 40% for any single asset
            
            for asset, weight in sorted_assets:
                if weight > max_weight:
                    excess = weight - max_weight
                    optimized_allocation[asset] = max_weight
                    
                    # Redistribute excess to other assets
                    other_assets = [a for a in optimized_allocation if a != asset]
                    if other_assets:
                        per_asset_addition = excess / len(other_assets)
                        for other_asset in other_assets:
                            optimized_allocation[other_asset] += per_asset_addition
        
        # Normalize to sum to 1.0
        total_weight = sum(optimized_allocation.values())
        if total_weight > 0:
            optimized_allocation = {asset: weight / total_weight 
                                  for asset, weight in optimized_allocation.items()}
        
        # Remove very small allocations (< 1%)
        optimized_allocation = {asset: weight for asset, weight in optimized_allocation.items() 
                              if weight >= 0.01}
        
        # Final normalization
        total_weight = sum(optimized_allocation.values())
        if total_weight > 0:
            optimized_allocation = {asset: weight / total_weight 
                                  for asset, weight in optimized_allocation.items()}
        
        return optimized_allocation
    
    def _calculate_final_metrics(self, allocation: Dict[str, float],
                               risk_analysis: RiskAnalysis,
                               cost_analysis: CostAnalysis) -> Dict[str, float]:
        """Calculate final portfolio performance metrics."""
        # Expected return
        expected_returns = {
            'Stocks': 0.10, 'Bonds': 0.04, 'Real Estate': 0.08,
            'Commodities': 0.06, 'Cash': 0.02, 'Alternatives': 0.12,
            'International': 0.09, 'Technology': 0.12, 'Healthcare': 0.10
        }
        
        expected_return = sum(w * expected_returns.get(asset, 0.08) 
                            for asset, w in allocation.items())
        
        # Adjust for costs
        net_return = expected_return - cost_analysis.total_expense_ratio
        
        # Sharpe ratio
        risk_free_rate = 0.02
        sharpe_ratio = (net_return - risk_free_rate) / max(risk_analysis.volatility, 0.001)
        
        # Utility score (mean-variance utility)
        risk_aversion = 3.0  # Typical risk aversion parameter
        utility_score = net_return - 0.5 * risk_aversion * (risk_analysis.volatility ** 2)
        
        return {
            'expected_return': expected_return,
            'net_return': net_return,
            'sharpe_ratio': sharpe_ratio,
            'utility_score': utility_score
        }
    
    def _calculate_synthesis_confidence(self, agent_proposals: List[AgentStrategy],
                                      selected_point: ParetoPoint) -> float:
        """Calculate confidence in the synthesis result."""
        if not agent_proposals:
            return 0.0
        
        # Base confidence from agent agreement
        agent_confidences = [strategy.confidence for strategy in agent_proposals]
        avg_agent_confidence = np.mean(agent_confidences)
        
        # Pareto efficiency bonus
        pareto_bonus = 0.1 if selected_point.pareto_efficient else 0.0
        
        # Diversification bonus
        num_assets = len([w for w in selected_point.weights.values() if w > 0.01])
        diversification_bonus = min(0.15, num_assets * 0.02)
        
        # Dominance rank bonus
        dominance_bonus = min(0.1, selected_point.dominance_rank * 0.02)
        
        synthesis_confidence = (avg_agent_confidence + pareto_bonus + 
                              diversification_bonus + dominance_bonus)
        
        return min(1.0, max(0.0, synthesis_confidence))
    
    def _calculate_improvement_metrics(self, agent_proposals: List[AgentStrategy],
                                     final_allocation: Dict[str, float],
                                     final_metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate improvement metrics compared to individual agent proposals."""
        if not agent_proposals:
            return {}
        
        # Calculate average metrics from agent proposals
        avg_return = np.mean([s.expected_return for s in agent_proposals])
        avg_risk = np.mean([s.risk_score for s in agent_proposals])
        avg_alpha_score = np.mean([s.alpha_score for s in agent_proposals])
        
        # Calculate improvements
        return_improvement = final_metrics['expected_return'] - avg_return
        risk_improvement = avg_risk - final_metrics['net_return']  # Lower risk is better
        sharpe_improvement = final_metrics['sharpe_ratio'] - (avg_return - 0.02) / avg_risk
        
        return {
            'return_improvement': return_improvement,
            'risk_improvement': risk_improvement,
            'sharpe_improvement': sharpe_improvement,
            'alpha_score_improvement': 0.0,  # Would need to recalculate
            'diversification_improvement': len(final_allocation) - np.mean([len(s.asset_allocation) for s in agent_proposals])
        }
    
    def get_synthesis_summary(self, synthesis: PortfolioSynthesis) -> Dict[str, Any]:
        """Get comprehensive summary of synthesis results."""
        return {
            'portfolio_id': synthesis.portfolio_id,
            'synthesis_overview': {
                'expected_return': f"{synthesis.expected_return:.2%}",
                'risk_score': f"{synthesis.risk_score:.3f}",
                'sharpe_ratio': f"{synthesis.sharpe_ratio:.3f}",
                'cost_score': f"{synthesis.cost_score:.3f}",
                'synthesis_confidence': f"{synthesis.synthesis_confidence:.1%}"
            },
            'final_allocation': {asset: f"{weight:.1%}" for asset, weight in synthesis.final_allocation.items()},
            'contributing_agents': synthesis.contributing_agents,
            'optimization_method': synthesis.optimization_method,
            'pareto_rank': synthesis.pareto_rank,
            'risk_metrics': {
                'volatility': f"{synthesis.risk_analysis.volatility:.2%}",
                'var_95': f"{synthesis.risk_analysis.var_95:.2%}",
                'max_drawdown': f"{synthesis.risk_analysis.max_drawdown:.2%}",
                'beta': f"{synthesis.risk_analysis.beta:.2f}",
                'concentration_risk': f"{synthesis.risk_analysis.concentration_risk:.2f}"
            },
            'cost_metrics': {
                'total_expense_ratio': f"{synthesis.cost_analysis.total_expense_ratio:.3%}",
                'transaction_costs': f"{synthesis.cost_analysis.transaction_costs:.3%}",
                'tax_efficiency': f"{synthesis.cost_analysis.tax_efficiency_score:.1%}",
                'optimization_savings': f"{synthesis.cost_analysis.fee_optimization_savings:.3%}"
            },
            'improvement_metrics': {k: f"{v:.4f}" for k, v in synthesis.improvement_metrics.items()},
            'stress_test_results': {k: f"{v:.2%}" for k, v in synthesis.risk_analysis.stress_test_results.items()}
        }


# Convenience function for easy integration
async def synthesize_optimal_portfolio(agent_proposals: List[AgentStrategy],
                                     client_goals: Dict[str, Any],
                                     market_data: List[MarketData],
                                     portfolio_value: float = 100000) -> PortfolioSynthesis:
    """
    Convenience function to synthesize optimal portfolio from agent proposals.
    """
    surgeon = PortfolioSurgeon()
    return await surgeon.synthesize_portfolio(
        agent_proposals, client_goals, market_data, portfolio_value
    )


if __name__ == "__main__":
    # Example usage
    async def main():
        from strategy_optimization_arena import run_strategy_optimization
        
        # Sample client input
        client_input = {
            "goals": {
                "strategy": "balanced growth with ESG focus",
                "timeline": "15 years",
                "target_amount": 1500000,
                "risk_tolerance": "moderate to high"
            },
            "constraints": {
                "capital": 200000,
                "contributions": 3000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 75
            }
        }
        
        # Get agent proposals
        arena_result = await run_strategy_optimization(client_input, num_agents=20)
        
        # Convert to AgentStrategy objects (simplified for demo)
        from strategy_optimization_arena import AgentStrategy, AgentRole, StrategyType
        agent_proposals = []
        for strategy_data in arena_result['top_strategies'][:10]:
            strategy = AgentStrategy(
                agent_id=strategy_data['agent_id'],
                agent_name=strategy_data['agent_name'],
                agent_role=AgentRole(strategy_data['agent_role']),
                strategy_type=StrategyType(strategy_data['strategy_type']),
                asset_allocation=strategy_data['asset_allocation'],
                expected_return=strategy_data['expected_return'],
                risk_score=strategy_data['risk_score'],
                timeline_fit=strategy_data['timeline_fit'],
                capital_efficiency=strategy_data['capital_efficiency']
            )
            agent_proposals.append(strategy)
        
        # Synthesize optimal portfolio
        synthesis_result = await synthesize_optimal_portfolio(
            agent_proposals, arena_result['client_goals'], [], 200000
        )
        
        # Display results
        surgeon = PortfolioSurgeon()
        summary = surgeon.get_synthesis_summary(synthesis_result)
        print(json.dumps(summary, indent=2))
    
    # Run example
    asyncio.run(main())