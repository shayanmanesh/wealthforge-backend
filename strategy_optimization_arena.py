"""
Strategy Optimization Arena using CrewAI

This module implements a comprehensive strategy optimization arena with 50 specialized agents
using CrewAI framework. Agents compete using AlphaScore = (ExpectedReturn * TimelineFit) / (RiskScore * CapitalEfficiency).
"""

import json
import asyncio
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
from crewai import Agent, Task, Crew, Process
from goal_constraint_parser import parse_goal_constraints


class AgentRole(Enum):
    """Specialized agent roles in the optimization arena."""
    MARKET_ANALYST = "market_analyst"
    RISK_OPTIMIZER = "risk_optimizer"
    PORTFOLIO_MANAGER = "portfolio_manager"
    QUANT_RESEARCHER = "quant_researcher"
    ESG_SPECIALIST = "esg_specialist"
    SECTOR_SPECIALIST = "sector_specialist"
    MACRO_ECONOMIST = "macro_economist"
    TECHNICAL_ANALYST = "technical_analyst"
    FUNDAMENTAL_ANALYST = "fundamental_analyst"
    DERIVATIVES_SPECIALIST = "derivatives_specialist"


class StrategyType(Enum):
    """Investment strategy types for arena competition."""
    MOMENTUM = "momentum"
    VALUE = "value"
    GROWTH = "growth"
    INCOME = "income"
    CONTRARIAN = "contrarian"
    QUANTITATIVE = "quantitative"
    ESG_FOCUSED = "esg_focused"
    SECTOR_ROTATION = "sector_rotation"
    MACRO_HEDGE = "macro_hedge"
    ARBITRAGE = "arbitrage"


@dataclass
class MarketData:
    """Dummy market data for simulations."""
    timestamp: datetime
    spy_price: float
    vix: float
    ten_year_yield: float
    dollar_index: float
    oil_price: float
    gold_price: float
    sector_performance: Dict[str, float]
    volatility_surface: Dict[str, float]
    
    @classmethod
    def generate_dummy_data(cls, days_back: int = 252) -> List['MarketData']:
        """Generate dummy market data for simulations."""
        data = []
        base_date = datetime.now() - timedelta(days=days_back)
        
        # Initialize base values
        spy_price = 450.0
        vix = 20.0
        ten_year_yield = 4.5
        dollar_index = 103.0
        oil_price = 80.0
        gold_price = 2000.0
        
        sectors = ['Technology', 'Healthcare', 'Financial', 'Energy', 'Consumer', 'Industrial', 'Utilities', 'Real Estate']
        
        for i in range(days_back):
            # Add random walk with mean reversion
            spy_price *= (1 + np.random.normal(0.0005, 0.015))
            vix *= (1 + np.random.normal(-0.001, 0.05))
            vix = max(10, min(50, vix))  # Constrain VIX
            
            ten_year_yield += np.random.normal(0, 0.02)
            ten_year_yield = max(2, min(8, ten_year_yield))
            
            dollar_index += np.random.normal(0, 0.3)
            oil_price *= (1 + np.random.normal(0, 0.02))
            gold_price *= (1 + np.random.normal(0, 0.012))
            
            # Generate sector performance
            sector_perf = {}
            for sector in sectors:
                sector_perf[sector] = np.random.normal(0.0008, 0.018)
            
            # Generate volatility surface
            vol_surface = {
                '1m': vix * np.random.uniform(0.8, 1.2),
                '3m': vix * np.random.uniform(0.9, 1.1),
                '6m': vix * np.random.uniform(0.95, 1.05),
                '1y': vix * np.random.uniform(1.0, 1.1)
            }
            
            data.append(cls(
                timestamp=base_date + timedelta(days=i),
                spy_price=spy_price,
                vix=vix,
                ten_year_yield=ten_year_yield,
                dollar_index=dollar_index,
                oil_price=oil_price,
                gold_price=gold_price,
                sector_performance=sector_perf,
                volatility_surface=vol_surface
            ))
        
        return data


@dataclass
class PortfolioMetrics:
    """Portfolio performance metrics for agent evaluation."""
    expected_return: float
    risk_score: float
    sharpe_ratio: float
    max_drawdown: float
    timeline_fit: float
    capital_efficiency: float
    volatility: float
    beta: float
    alpha: float
    information_ratio: float


@dataclass
class AgentStrategy:
    """Investment strategy proposed by an agent."""
    agent_id: str
    agent_name: str
    agent_role: AgentRole
    strategy_type: StrategyType
    asset_allocation: Dict[str, float]
    expected_return: float
    risk_score: float
    timeline_fit: float
    capital_efficiency: float
    alpha_score: float = field(init=False)
    confidence: float = 0.8
    reasoning: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate AlphaScore after initialization."""
        self.alpha_score = self.calculate_alpha_score()
    
    def calculate_alpha_score(self) -> float:
        """Calculate AlphaScore = (ExpectedReturn * TimelineFit) / (RiskScore * CapitalEfficiency)."""
        if self.risk_score == 0 or self.capital_efficiency == 0:
            return 0.0
        
        return (self.expected_return * self.timeline_fit) / (self.risk_score * self.capital_efficiency)


class FinancialAgent:
    """Base class for financial agents in the optimization arena."""
    
    def __init__(self, agent_id: str, name: str, role: AgentRole, specialization: str):
        """Initialize a financial agent."""
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.specialization = specialization
        self.performance_history: List[float] = []
        self.success_rate = 0.5  # Initial success rate
        
        # Create CrewAI agent
        self.crew_agent = self._create_crew_agent()
    
    def _create_crew_agent(self) -> Agent:
        """Create the underlying CrewAI agent."""
        role_descriptions = {
            AgentRole.MARKET_ANALYST: f"Expert market analyst specializing in {self.specialization}",
            AgentRole.RISK_OPTIMIZER: f"Risk optimization specialist focusing on {self.specialization}",
            AgentRole.PORTFOLIO_MANAGER: f"Portfolio manager with expertise in {self.specialization}",
            AgentRole.QUANT_RESEARCHER: f"Quantitative researcher specializing in {self.specialization}",
            AgentRole.ESG_SPECIALIST: f"ESG investment specialist focusing on {self.specialization}",
            AgentRole.SECTOR_SPECIALIST: f"Sector specialist with deep knowledge of {self.specialization}",
            AgentRole.MACRO_ECONOMIST: f"Macroeconomic analyst specializing in {self.specialization}",
            AgentRole.TECHNICAL_ANALYST: f"Technical analysis expert focusing on {self.specialization}",
            AgentRole.FUNDAMENTAL_ANALYST: f"Fundamental analysis specialist in {self.specialization}",
            AgentRole.DERIVATIVES_SPECIALIST: f"Derivatives and hedging specialist in {self.specialization}"
        }
        
        backstory = f"""
You are {self.name}, a highly experienced {role_descriptions[self.role]}.
You have years of experience in financial markets and specialize in {self.specialization}.
Your goal is to provide optimal investment strategies that maximize risk-adjusted returns.
You compete with other agents to provide the best investment recommendations.
"""
        
        return Agent(
            role=role_descriptions[self.role],
            goal=f"Provide optimal investment strategies in {self.specialization}",
            backstory=backstory,
            verbose=False,
            allow_delegation=False
        )
    
    def generate_strategy(self, market_data: List[MarketData], 
                         client_goals: Dict[str, Any], 
                         timeline: int = 252) -> AgentStrategy:
        """Generate an investment strategy based on market data and client goals."""
        # Simulate strategy generation based on agent role and specialization
        strategy_type = self._select_strategy_type()
        allocation = self._generate_allocation(market_data, client_goals)
        
        # Calculate metrics based on agent's expertise
        expected_return = self._calculate_expected_return(allocation, market_data)
        risk_score = self._calculate_risk_score(allocation, market_data)
        timeline_fit = self._calculate_timeline_fit(client_goals, timeline)
        capital_efficiency = self._calculate_capital_efficiency(allocation, client_goals)
        
        return AgentStrategy(
            agent_id=self.agent_id,
            agent_name=self.name,
            agent_role=self.role,
            strategy_type=strategy_type,
            asset_allocation=allocation,
            expected_return=expected_return,
            risk_score=risk_score,
            timeline_fit=timeline_fit,
            capital_efficiency=capital_efficiency,
            confidence=min(0.95, self.success_rate + random.uniform(0.1, 0.3)),
            reasoning=f"{self.role.value} analysis suggests {strategy_type.value} strategy"
        )
    
    def _select_strategy_type(self) -> StrategyType:
        """Select strategy type based on agent role and specialization."""
        role_strategy_preferences = {
            AgentRole.MARKET_ANALYST: [StrategyType.MOMENTUM, StrategyType.SECTOR_ROTATION],
            AgentRole.RISK_OPTIMIZER: [StrategyType.VALUE, StrategyType.CONTRARIAN],
            AgentRole.PORTFOLIO_MANAGER: [StrategyType.GROWTH, StrategyType.INCOME],
            AgentRole.QUANT_RESEARCHER: [StrategyType.QUANTITATIVE, StrategyType.ARBITRAGE],
            AgentRole.ESG_SPECIALIST: [StrategyType.ESG_FOCUSED, StrategyType.GROWTH],
            AgentRole.SECTOR_SPECIALIST: [StrategyType.SECTOR_ROTATION, StrategyType.VALUE],
            AgentRole.MACRO_ECONOMIST: [StrategyType.MACRO_HEDGE, StrategyType.CONTRARIAN],
            AgentRole.TECHNICAL_ANALYST: [StrategyType.MOMENTUM, StrategyType.QUANTITATIVE],
            AgentRole.FUNDAMENTAL_ANALYST: [StrategyType.VALUE, StrategyType.GROWTH],
            AgentRole.DERIVATIVES_SPECIALIST: [StrategyType.ARBITRAGE, StrategyType.MACRO_HEDGE]
        }
        
        preferences = role_strategy_preferences.get(self.role, list(StrategyType))
        return random.choice(preferences)
    
    def _generate_allocation(self, market_data: List[MarketData], 
                           client_goals: Dict[str, Any]) -> Dict[str, float]:
        """Generate asset allocation based on agent's expertise."""
        # Base allocation categories
        categories = ['Stocks', 'Bonds', 'Real Estate', 'Commodities', 'Cash', 'Alternatives']
        
        # Generate allocation based on role
        if self.role == AgentRole.RISK_OPTIMIZER:
            # More conservative allocation
            allocation = {
                'Stocks': random.uniform(0.3, 0.6),
                'Bonds': random.uniform(0.2, 0.4),
                'Real Estate': random.uniform(0.05, 0.15),
                'Commodities': random.uniform(0.02, 0.08),
                'Cash': random.uniform(0.05, 0.15),
                'Alternatives': random.uniform(0.02, 0.1)
            }
        elif self.role == AgentRole.QUANT_RESEARCHER:
            # More quantitative allocation
            allocation = {
                'Stocks': random.uniform(0.4, 0.8),
                'Bonds': random.uniform(0.1, 0.3),
                'Real Estate': random.uniform(0.03, 0.1),
                'Commodities': random.uniform(0.05, 0.15),
                'Cash': random.uniform(0.02, 0.1),
                'Alternatives': random.uniform(0.05, 0.2)
            }
        else:
            # Balanced allocation with role-specific adjustments
            allocation = {
                'Stocks': random.uniform(0.4, 0.7),
                'Bonds': random.uniform(0.15, 0.35),
                'Real Estate': random.uniform(0.05, 0.12),
                'Commodities': random.uniform(0.03, 0.1),
                'Cash': random.uniform(0.03, 0.12),
                'Alternatives': random.uniform(0.03, 0.15)
            }
        
        # Normalize to sum to 1.0
        total = sum(allocation.values())
        allocation = {k: v/total for k, v in allocation.items()}
        
        return allocation
    
    def _calculate_expected_return(self, allocation: Dict[str, float], 
                                 market_data: List[MarketData]) -> float:
        """Calculate expected return based on allocation and market conditions."""
        # Historical returns by asset class (annualized)
        expected_returns = {
            'Stocks': 0.10,
            'Bonds': 0.04,
            'Real Estate': 0.08,
            'Commodities': 0.06,
            'Cash': 0.02,
            'Alternatives': 0.12
        }
        
        # Adjust based on recent market conditions
        recent_spy_return = (market_data[-1].spy_price - market_data[-21].spy_price) / market_data[-21].spy_price
        market_adjustment = recent_spy_return * 0.5  # Partial correlation
        
        portfolio_return = sum(allocation[asset] * (expected_returns[asset] + market_adjustment) 
                             for asset in allocation)
        
        # Add agent expertise bonus
        expertise_bonus = (self.success_rate - 0.5) * 0.02
        
        return portfolio_return + expertise_bonus
    
    def _calculate_risk_score(self, allocation: Dict[str, float], 
                            market_data: List[MarketData]) -> float:
        """Calculate risk score based on allocation and market volatility."""
        # Historical volatilities by asset class
        volatilities = {
            'Stocks': 0.16,
            'Bonds': 0.04,
            'Real Estate': 0.12,
            'Commodities': 0.20,
            'Cash': 0.01,
            'Alternatives': 0.18
        }
        
        # Calculate portfolio volatility (simplified)
        portfolio_vol = sum(allocation[asset] * volatilities[asset] for asset in allocation)
        
        # Adjust based on current VIX
        current_vix = market_data[-1].vix
        vix_adjustment = (current_vix - 20) / 20  # Normalize around 20
        
        risk_score = portfolio_vol * (1 + vix_adjustment * 0.3)
        
        return max(0.01, risk_score)  # Ensure positive risk score
    
    def _calculate_timeline_fit(self, client_goals: Dict[str, Any], timeline: int) -> float:
        """Calculate how well the strategy fits the client's timeline."""
        # Extract timeline information
        goal_timeline = client_goals.get('goals', {}).get('timeline', 'medium-term')
        
        # Convert to numerical timeline
        if 'short' in goal_timeline.lower() or any(str(i) in goal_timeline for i in range(1, 4)):
            target_timeline = 1  # 1 year
        elif 'long' in goal_timeline.lower() or any(str(i) in goal_timeline for i in range(10, 40)):
            target_timeline = 15  # 15 years
        else:
            target_timeline = 5  # 5 years (medium-term)
        
        # Calculate fit based on strategy appropriateness for timeline
        strategy_timeline_match = {
            StrategyType.MOMENTUM: 0.8 if target_timeline <= 2 else 0.6,
            StrategyType.VALUE: 0.9 if target_timeline >= 5 else 0.5,
            StrategyType.GROWTH: 0.95 if target_timeline >= 10 else 0.7,
            StrategyType.INCOME: 0.8,  # Good for all timelines
            StrategyType.CONTRARIAN: 0.9 if target_timeline >= 3 else 0.4,
            StrategyType.QUANTITATIVE: 0.7,  # Neutral
            StrategyType.ESG_FOCUSED: 0.9 if target_timeline >= 5 else 0.6,
            StrategyType.SECTOR_ROTATION: 0.7 if target_timeline <= 5 else 0.5,
            StrategyType.MACRO_HEDGE: 0.8,  # Good for all timelines
            StrategyType.ARBITRAGE: 0.6 if target_timeline <= 2 else 0.4
        }
        
        base_fit = strategy_timeline_match.get(self._select_strategy_type(), 0.7)
        
        # Add noise based on agent expertise
        expertise_adjustment = (self.success_rate - 0.5) * 0.2
        
        return min(1.0, base_fit + expertise_adjustment + random.uniform(-0.1, 0.1))
    
    def _calculate_capital_efficiency(self, allocation: Dict[str, float], 
                                    client_goals: Dict[str, Any]) -> float:
        """Calculate capital efficiency based on allocation and client constraints."""
        # Extract capital information
        constraints = client_goals.get('constraints', {})
        capital = constraints.get('capital', 100000)
        contributions = constraints.get('contributions', 0)
        
        # Calculate efficiency based on allocation complexity and costs
        complexity_score = len([v for v in allocation.values() if v > 0.05])  # Number of significant allocations
        efficiency_penalty = (complexity_score - 3) * 0.05  # Penalty for over-diversification
        
        # Adjust based on capital size (larger capital = better efficiency)
        capital_factor = min(1.0, capital / 100000)  # Normalize to 100k base
        
        # Base efficiency
        base_efficiency = 0.8 - efficiency_penalty + (capital_factor * 0.2)
        
        # Agent expertise adjustment
        expertise_bonus = (self.success_rate - 0.5) * 0.3
        
        return max(0.1, min(1.0, base_efficiency + expertise_bonus))
    
    def update_performance(self, actual_return: float, benchmark_return: float):
        """Update agent performance based on actual results."""
        # Calculate relative performance
        relative_performance = actual_return - benchmark_return
        
        # Update success rate (exponential moving average)
        success = 1.0 if relative_performance > 0 else 0.0
        self.success_rate = 0.8 * self.success_rate + 0.2 * success
        
        # Store performance history
        self.performance_history.append(actual_return)
        if len(self.performance_history) > 100:
            self.performance_history.pop(0)  # Keep last 100 results


class StrategyOptimizationArena:
    """Main arena for strategy optimization with 50 competing agents."""
    
    def __init__(self):
        """Initialize the strategy optimization arena."""
        self.agents: List[FinancialAgent] = []
        self.market_data: List[MarketData] = []
        self.competition_history: List[Dict[str, Any]] = []
        self.current_rankings: List[Tuple[str, float]] = []
        
        # Initialize agents and market data
        self._initialize_agents()
        self._initialize_market_data()
    
    def _initialize_agents(self):
        """Create 50 specialized agents with different roles and specializations."""
        agent_specs = [
            # Market Analysts (5)
            (AgentRole.MARKET_ANALYST, "TechMarketGuru", "Technology Sector Analysis"),
            (AgentRole.MARKET_ANALYST, "HealthcareOracle", "Healthcare Market Trends"),
            (AgentRole.MARKET_ANALYST, "FinancialSeer", "Financial Sector Dynamics"),
            (AgentRole.MARKET_ANALYST, "EnergyTracker", "Energy Market Analysis"),
            (AgentRole.MARKET_ANALYST, "ConsumerInsight", "Consumer Discretionary Analysis"),
            
            # Risk Optimizers (5)
            (AgentRole.RISK_OPTIMIZER, "RiskMaster", "Portfolio Risk Management"),
            (AgentRole.RISK_OPTIMIZER, "VolatilityHunter", "Volatility Optimization"),
            (AgentRole.RISK_OPTIMIZER, "DrawdownMinimizer", "Maximum Drawdown Control"),
            (AgentRole.RISK_OPTIMIZER, "CorrelationBreaker", "Correlation Analysis"),
            (AgentRole.RISK_OPTIMIZER, "TailRiskGuard", "Tail Risk Protection"),
            
            # Portfolio Managers (5)
            (AgentRole.PORTFOLIO_MANAGER, "BalancedPro", "Balanced Portfolio Management"),
            (AgentRole.PORTFOLIO_MANAGER, "GrowthChampion", "Growth Portfolio Specialist"),
            (AgentRole.PORTFOLIO_MANAGER, "IncomeExpert", "Income-Focused Portfolios"),
            (AgentRole.PORTFOLIO_MANAGER, "GlobalManager", "International Diversification"),
            (AgentRole.PORTFOLIO_MANAGER, "SmallCapSpecialist", "Small Cap Portfolio Management"),
            
            # Quantitative Researchers (5)
            (AgentRole.QUANT_RESEARCHER, "AlphaHunter", "Statistical Arbitrage"),
            (AgentRole.QUANT_RESEARCHER, "MomentumQuant", "Momentum Factor Analysis"),
            (AgentRole.QUANT_RESEARCHER, "MeanReversionBot", "Mean Reversion Strategies"),
            (AgentRole.QUANT_RESEARCHER, "FactorModeler", "Multi-Factor Model Development"),
            (AgentRole.QUANT_RESEARCHER, "MLTrader", "Machine Learning Trading"),
            
            # ESG Specialists (5)
            (AgentRole.ESG_SPECIALIST, "SustainabilityPro", "ESG Integration"),
            (AgentRole.ESG_SPECIALIST, "ClimateInvestor", "Climate Change Investment"),
            (AgentRole.ESG_SPECIALIST, "GovernanceExpert", "Corporate Governance"),
            (AgentRole.ESG_SPECIALIST, "ImpactInvestor", "Impact Investment Strategies"),
            (AgentRole.ESG_SPECIALIST, "GreenBondSpecialist", "Green Finance"),
            
            # Sector Specialists (5)
            (AgentRole.SECTOR_SPECIALIST, "BiotechBull", "Biotechnology Investments"),
            (AgentRole.SECTOR_SPECIALIST, "TechTitan", "Technology Innovation"),
            (AgentRole.SECTOR_SPECIALIST, "REITExpert", "Real Estate Investment"),
            (AgentRole.SECTOR_SPECIALIST, "CommodityKing", "Commodity Trading"),
            (AgentRole.SECTOR_SPECIALIST, "UtilityStable", "Utility Sector Analysis"),
            
            # Macro Economists (5)
            (AgentRole.MACRO_ECONOMIST, "FedWatcher", "Federal Reserve Policy"),
            (AgentRole.MACRO_ECONOMIST, "CurrencyAnalyst", "Foreign Exchange"),
            (AgentRole.MACRO_ECONOMIST, "InflationTracker", "Inflation Analysis"),
            (AgentRole.MACRO_ECONOMIST, "CycleTimer", "Economic Cycle Analysis"),
            (AgentRole.MACRO_ECONOMIST, "GeopoliticalRisk", "Geopolitical Risk Assessment"),
            
            # Technical Analysts (5)
            (AgentRole.TECHNICAL_ANALYST, "ChartMaster", "Technical Pattern Analysis"),
            (AgentRole.TECHNICAL_ANALYST, "TrendFollower", "Trend Following Systems"),
            (AgentRole.TECHNICAL_ANALYST, "SupportResistance", "Support/Resistance Analysis"),
            (AgentRole.TECHNICAL_ANALYST, "VolumeAnalyst", "Volume Profile Analysis"),
            (AgentRole.TECHNICAL_ANALYST, "MomentumTracker", "Momentum Indicators"),
            
            # Fundamental Analysts (5)
            (AgentRole.FUNDAMENTAL_ANALYST, "ValueSeeker", "Value Investment Analysis"),
            (AgentRole.FUNDAMENTAL_ANALYST, "EarningsGuru", "Earnings Analysis"),
            (AgentRole.FUNDAMENTAL_ANALYST, "DCFMaster", "Discounted Cash Flow"),
            (AgentRole.FUNDAMENTAL_ANALYST, "RatioAnalyst", "Financial Ratio Analysis"),
            (AgentRole.FUNDAMENTAL_ANALYST, "QualityFocused", "Quality Investment"),
            
            # Derivatives Specialists (5)
            (AgentRole.DERIVATIVES_SPECIALIST, "OptionsWizard", "Options Strategies"),
            (AgentRole.DERIVATIVES_SPECIALIST, "HedgeMaster", "Portfolio Hedging"),
            (AgentRole.DERIVATIVES_SPECIALIST, "VolatilityTrader", "Volatility Trading"),
            (AgentRole.DERIVATIVES_SPECIALIST, "StructuredProducts", "Structured Product Design"),
            (AgentRole.DERIVATIVES_SPECIALIST, "ArbitrageHunter", "Arbitrage Strategies")
        ]
        
        # Create agents
        for i, (role, name, specialization) in enumerate(agent_specs):
            agent_id = f"agent_{i+1:02d}"
            agent = FinancialAgent(agent_id, name, role, specialization)
            self.agents.append(agent)
        
        print(f"✅ Initialized {len(self.agents)} specialized agents")
    
    def _initialize_market_data(self):
        """Initialize market data for simulations."""
        self.market_data = MarketData.generate_dummy_data(days_back=504)  # 2 years of data
        print(f"✅ Generated {len(self.market_data)} days of market data")
    
    async def run_competition(self, client_goals: Dict[str, Any], 
                            num_agents: int = 50) -> Dict[str, Any]:
        """Run a strategy optimization competition."""
        print(f"\n🏁 Starting Strategy Optimization Competition")
        print(f"   Competing Agents: {min(num_agents, len(self.agents))}")
        print(f"   Client Goals: {client_goals.get('goals', {}).get('strategy', 'N/A')}")
        
        start_time = datetime.now()
        
        # Select agents for competition
        competing_agents = self.agents[:min(num_agents, len(self.agents))]
        
        # Generate strategies from all agents
        strategies: List[AgentStrategy] = []
        
        for agent in competing_agents:
            try:
                strategy = agent.generate_strategy(self.market_data, client_goals)
                strategies.append(strategy)
            except Exception as e:
                print(f"⚠️ Agent {agent.name} failed to generate strategy: {e}")
        
        # Sort strategies by AlphaScore
        strategies.sort(key=lambda s: s.alpha_score, reverse=True)
        
        # Update rankings
        self.current_rankings = [(s.agent_name, s.alpha_score) for s in strategies]
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Compile results
        results = {
            "competition_id": f"comp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": start_time.isoformat(),
            "execution_time": execution_time,
            "total_agents": len(competing_agents),
            "strategies_generated": len(strategies),
            "client_goals": client_goals,
            "top_strategies": [self._strategy_to_dict(s) for s in strategies[:10]],
            "winner": self._strategy_to_dict(strategies[0]) if strategies else None,
            "alpha_score_distribution": {
                "max": max(s.alpha_score for s in strategies) if strategies else 0,
                "min": min(s.alpha_score for s in strategies) if strategies else 0,
                "mean": np.mean([s.alpha_score for s in strategies]) if strategies else 0,
                "std": np.std([s.alpha_score for s in strategies]) if strategies else 0
            },
            "strategy_type_distribution": self._get_strategy_type_distribution(strategies),
            "role_performance": self._get_role_performance(strategies)
        }
        
        # Store in competition history
        self.competition_history.append(results)
        
        return results
    
    def _strategy_to_dict(self, strategy: AgentStrategy) -> Dict[str, Any]:
        """Convert AgentStrategy to dictionary."""
        return {
            "agent_id": strategy.agent_id,
            "agent_name": strategy.agent_name,
            "agent_role": strategy.agent_role.value,
            "strategy_type": strategy.strategy_type.value,
            "alpha_score": strategy.alpha_score,
            "expected_return": strategy.expected_return,
            "risk_score": strategy.risk_score,
            "timeline_fit": strategy.timeline_fit,
            "capital_efficiency": strategy.capital_efficiency,
            "confidence": strategy.confidence,
            "asset_allocation": strategy.asset_allocation,
            "reasoning": strategy.reasoning
        }
    
    def _get_strategy_type_distribution(self, strategies: List[AgentStrategy]) -> Dict[str, int]:
        """Get distribution of strategy types."""
        distribution = {}
        for strategy in strategies:
            strategy_type = strategy.strategy_type.value
            distribution[strategy_type] = distribution.get(strategy_type, 0) + 1
        return distribution
    
    def _get_role_performance(self, strategies: List[AgentStrategy]) -> Dict[str, Dict[str, float]]:
        """Get performance statistics by agent role."""
        role_performance = {}
        
        for role in AgentRole:
            role_strategies = [s for s in strategies if s.agent_role == role]
            if role_strategies:
                role_performance[role.value] = {
                    "count": len(role_strategies),
                    "avg_alpha_score": np.mean([s.alpha_score for s in role_strategies]),
                    "max_alpha_score": max(s.alpha_score for s in role_strategies),
                    "avg_confidence": np.mean([s.confidence for s in role_strategies])
                }
        
        return role_performance
    
    def simulate_strategy_performance(self, strategy: AgentStrategy, 
                                    simulation_days: int = 252) -> Dict[str, float]:
        """Simulate strategy performance over time."""
        # Use Monte Carlo simulation for strategy performance
        np.random.seed(42)  # For reproducible results
        
        # Generate daily returns based on strategy
        daily_returns = []
        for _ in range(simulation_days):
            # Base return from expected annual return
            daily_base_return = strategy.expected_return / 252
            
            # Add volatility based on risk score
            daily_volatility = strategy.risk_score / np.sqrt(252)
            
            # Generate random return
            daily_return = np.random.normal(daily_base_return, daily_volatility)
            daily_returns.append(daily_return)
        
        # Calculate performance metrics
        total_return = np.prod([1 + r for r in daily_returns]) - 1
        volatility = np.std(daily_returns) * np.sqrt(252)
        sharpe_ratio = (strategy.expected_return - 0.02) / volatility if volatility > 0 else 0
        
        # Calculate maximum drawdown
        cumulative_returns = np.cumprod([1 + r for r in daily_returns])
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdowns)
        
        return {
            "total_return": total_return,
            "annualized_return": ((1 + total_return) ** (252/simulation_days)) - 1,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": len([r for r in daily_returns if r > 0]) / len(daily_returns),
            "best_day": max(daily_returns),
            "worst_day": min(daily_returns)
        }
    
    def get_leaderboard(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """Get current leaderboard of top performing agents."""
        if not self.current_rankings:
            return []
        
        leaderboard = []
        for i, (agent_name, alpha_score) in enumerate(self.current_rankings[:top_n]):
            # Find agent details
            agent = next((a for a in self.agents if a.name == agent_name), None)
            if agent:
                leaderboard.append({
                    "rank": i + 1,
                    "agent_name": agent_name,
                    "agent_role": agent.role.value,
                    "specialization": agent.specialization,
                    "alpha_score": alpha_score,
                    "success_rate": agent.success_rate,
                    "competitions_won": len([h for h in self.competition_history 
                                           if h.get('winner', {}).get('agent_name') == agent_name])
                })
        
        return leaderboard
    
    def get_arena_statistics(self) -> Dict[str, Any]:
        """Get comprehensive arena statistics."""
        if not self.competition_history:
            return {"message": "No competitions completed yet"}
        
        all_strategies = []
        for competition in self.competition_history:
            all_strategies.extend(competition.get('top_strategies', []))
        
        if not all_strategies:
            return {"message": "No strategy data available"}
        
        alpha_scores = [s['alpha_score'] for s in all_strategies]
        
        return {
            "total_competitions": len(self.competition_history),
            "total_strategies_evaluated": len(all_strategies),
            "active_agents": len(self.agents),
            "alpha_score_statistics": {
                "max": max(alpha_scores),
                "min": min(alpha_scores),
                "mean": np.mean(alpha_scores),
                "std": np.std(alpha_scores),
                "median": np.median(alpha_scores)
            },
            "most_successful_role": self._get_most_successful_role(),
            "most_used_strategy_type": self._get_most_used_strategy_type(),
            "average_competition_time": np.mean([c['execution_time'] for c in self.competition_history]),
            "market_data_days": len(self.market_data)
        }
    
    def _get_most_successful_role(self) -> str:
        """Get the most successful agent role."""
        role_wins = {}
        for competition in self.competition_history:
            winner = competition.get('winner')
            if winner:
                role = winner.get('agent_role')
                role_wins[role] = role_wins.get(role, 0) + 1
        
        if not role_wins:
            return "No data"
        
        return max(role_wins, key=role_wins.get)
    
    def _get_most_used_strategy_type(self) -> str:
        """Get the most frequently used strategy type."""
        strategy_counts = {}
        for competition in self.competition_history:
            for strategy in competition.get('top_strategies', []):
                strategy_type = strategy.get('strategy_type')
                strategy_counts[strategy_type] = strategy_counts.get(strategy_type, 0) + 1
        
        if not strategy_counts:
            return "No data"
        
        return max(strategy_counts, key=strategy_counts.get)


# Convenience function for easy usage
async def run_strategy_optimization(client_input: Dict[str, Any], 
                                  num_agents: int = 50) -> Dict[str, Any]:
    """
    Convenience function to run strategy optimization.
    
    Args:
        client_input: Client goals and constraints
        num_agents: Number of agents to compete (max 50)
        
    Returns:
        Competition results
    """
    # Parse client input
    parsed_goals = parse_goal_constraints(client_input)
    
    # Create arena
    arena = StrategyOptimizationArena()
    
    # Run competition
    results = await arena.run_competition(parsed_goals, num_agents)
    
    return results


if __name__ == "__main__":
    # Example usage
    async def main():
        sample_input = {
            "goals": {
                "strategy": "aggressive growth with technology focus",
                "timeline": "15 years",
                "target_amount": 2000000,
                "risk_tolerance": "high"
            },
            "constraints": {
                "capital": 150000,
                "contributions": 5000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 85,
                "liquidity_needs": "low"
            }
        }
        
        result = await run_strategy_optimization(sample_input, num_agents=20)
        print(json.dumps(result, indent=2))
    
    # Run the example
    asyncio.run(main())