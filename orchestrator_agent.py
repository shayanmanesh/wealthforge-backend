"""
Orchestrator Agent with AutoGen

This module implements an orchestrator that distributes tasks to specialized agents
and manages competition with dynamic weighting based on strategy types.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from autogen_agentchat.agents import AssistantAgent, BaseChatAgent
from goal_constraint_parser import parse_goal_constraints


class StrategyType(Enum):
    """Investment strategy types for agent specialization."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    GROWTH = "growth"
    INCOME = "income"
    BALANCED = "balanced"


@dataclass
class AgentScore:
    """Scoring system for agent performance."""
    agent_name: str
    strategy_match: float  # How well the agent matches the strategy (0-1)
    performance_score: float  # Historical performance score (0-1)
    confidence: float  # Agent's confidence in recommendation (0-1)
    total_score: float = field(init=False)
    
    def __post_init__(self):
        """Calculate total score with dynamic weighting."""
        self.total_score = (
            self.strategy_match * 0.4 +
            self.performance_score * 0.3 +
            self.confidence * 0.3
        )


@dataclass
class TaskResult:
    """Result from an agent task execution."""
    agent_name: str
    strategy_type: StrategyType
    recommendation: Dict[str, Any]
    reasoning: str
    confidence: float
    execution_time: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class StrategyAgent:
    """Specialized agent for specific investment strategies."""
    
    def __init__(self, 
                 name: str, 
                 strategy_type: StrategyType,
                 expertise_areas: List[str],
                 performance_history: float = 0.8,
                 **kwargs):
        """
        Initialize a strategy-specific agent.
        
        Args:
            name: Agent name
            strategy_type: Primary strategy specialization
            expertise_areas: Areas of expertise
            performance_history: Historical performance score (0-1)
        """
        self.name = name
        self.strategy_type = strategy_type
        self.expertise_areas = expertise_areas
        self.performance_history = performance_history
        
        # Store additional configuration
        self.config = kwargs
        
        # Create description based on strategy
        self.description = self._create_description()
    
    def _create_description(self) -> str:
        """Create agent description."""
        return f"Specialized {self.strategy_type.value} investment advisor with expertise in {', '.join(self.expertise_areas)}"
    
    def _create_system_message(self) -> str:
        """Create system message based on agent's strategy specialization."""
        base_message = f"""
You are a specialized investment advisor with expertise in {self.strategy_type.value} investment strategies.

Your specialization areas: {', '.join(self.expertise_areas)}

Key responsibilities:
1. Analyze investment goals and constraints
2. Provide {self.strategy_type.value}-focused recommendations
3. Explain your reasoning clearly
4. Rate your confidence in recommendations (0-1 scale)
5. Consider risk management appropriate for {self.strategy_type.value} strategies

Always respond in JSON format with these fields:
- recommendation: Your investment recommendation
- reasoning: Detailed explanation of your reasoning
- confidence: Your confidence level (0-1)
- risk_assessment: Risk analysis for this strategy
- expected_return: Expected return estimate
- time_horizon: Recommended time horizon
"""
        
        # Add strategy-specific guidance
        if self.strategy_type == StrategyType.CONSERVATIVE:
            base_message += """
Focus on:
- Capital preservation
- Low-risk investments (bonds, CDs, high-grade securities)
- Stable, predictable returns
- High liquidity options
- Risk tolerance: Very low to low
"""
        elif self.strategy_type == StrategyType.AGGRESSIVE:
            base_message += """
Focus on:
- High growth potential
- Higher-risk investments (growth stocks, emerging markets)
- Maximum capital appreciation
- Longer investment horizons
- Risk tolerance: High to very high
"""
        elif self.strategy_type == StrategyType.MODERATE:
            base_message += """
Focus on:
- Balanced approach between growth and stability
- Mix of stocks and bonds
- Moderate risk tolerance
- Steady growth with some income
- Risk tolerance: Medium
"""
        elif self.strategy_type == StrategyType.GROWTH:
            base_message += """
Focus on:
- Capital appreciation
- Growth stocks and growth funds
- Reinvestment of dividends
- Medium to long-term horizons
- Risk tolerance: Medium to high
"""
        elif self.strategy_type == StrategyType.INCOME:
            base_message += """
Focus on:
- Regular income generation
- Dividend-paying stocks, bonds, REITs
- Stable cash flow
- Lower volatility
- Risk tolerance: Low to medium
"""
        elif self.strategy_type == StrategyType.BALANCED:
            base_message += """
Focus on:
- Equal emphasis on growth and income
- Diversified portfolio
- Risk management through allocation
- Steady performance
- Risk tolerance: Medium
"""
        
        return base_message


class CompetitionManager:
    """Manages competition between agents and scoring."""
    
    def __init__(self):
        """Initialize the competition manager."""
        self.agent_scores: Dict[str, AgentScore] = {}
        self.task_history: List[TaskResult] = []
    
    def calculate_strategy_match(self, agent: StrategyAgent, target_strategy: str) -> float:
        """
        Calculate how well an agent matches the target strategy.
        
        Args:
            agent: The strategy agent
            target_strategy: Target strategy from user input
            
        Returns:
            Match score between 0 and 1
        """
        target_lower = target_strategy.lower()
        agent_strategy = agent.strategy_type.value.lower()
        
        # Direct match
        if agent_strategy in target_lower or target_lower in agent_strategy:
            return 1.0
        
        # Partial matches based on strategy relationships
        strategy_relationships = {
            "conservative": ["income", "stable", "low-risk", "capital preservation"],
            "aggressive": ["growth", "high-risk", "maximum return", "capital appreciation"],
            "moderate": ["balanced", "medium-risk", "steady growth"],
            "growth": ["aggressive", "capital appreciation", "long-term"],
            "income": ["conservative", "dividend", "stable income"],
            "balanced": ["moderate", "diversified", "mixed allocation"]
        }
        
        if agent_strategy in strategy_relationships:
            for related_term in strategy_relationships[agent_strategy]:
                if related_term in target_lower:
                    return 0.7
        
        # Default partial match for any strategy agent
        return 0.3
    
    def score_agents(self, agents: List[StrategyAgent], target_strategy: str) -> List[AgentScore]:
        """
        Score all agents for a given target strategy.
        
        Args:
            agents: List of strategy agents
            target_strategy: Target investment strategy
            
        Returns:
            List of agent scores sorted by total score
        """
        scores = []
        
        for agent in agents:
            strategy_match = self.calculate_strategy_match(agent, target_strategy)
            
            # Use agent's historical performance
            performance_score = agent.performance_history
            
            # Initial confidence based on strategy match
            confidence = strategy_match * 0.8 + 0.2
            
            score = AgentScore(
                agent_name=agent.name,
                strategy_match=strategy_match,
                performance_score=performance_score,
                confidence=confidence
            )
            
            scores.append(score)
            self.agent_scores[agent.name] = score
        
        # Sort by total score descending
        return sorted(scores, key=lambda x: x.total_score, reverse=True)
    
    def update_performance(self, agent_name: str, success_rate: float):
        """Update agent performance based on task results."""
        if agent_name in self.agent_scores:
            # Exponential moving average for performance updates
            current_perf = self.agent_scores[agent_name].performance_score
            self.agent_scores[agent_name].performance_score = (
                0.7 * current_perf + 0.3 * success_rate
            )


class OrchestratorAgent:
    """
    Main orchestrator that distributes tasks and manages agent competition.
    """
    
    def __init__(self, 
                 llm_config: Optional[Dict] = None,
                 enable_logging: bool = True):
        """
        Initialize the orchestrator.
        
        Args:
            llm_config: Configuration for LLM (OpenAI, etc.)
            enable_logging: Enable detailed logging
        """
        self.llm_config = llm_config or self._get_default_llm_config()
        self.enable_logging = enable_logging
        
        # Initialize specialized agents
        self.agents = self._create_specialized_agents()
        
        # Initialize competition manager
        self.competition_manager = CompetitionManager()
        
        # Task execution history
        self.execution_history: List[Dict[str, Any]] = []
    
    def _get_default_llm_config(self) -> Dict:
        """Get default LLM configuration."""
        return {
            "timeout": 120,
            "temperature": 0.1,
            "config_list": [
                {
                    "model": "gpt-3.5-turbo",
                    "api_key": None  # Will use environment variable
                }
            ]
        }
    
    def _create_specialized_agents(self) -> List[StrategyAgent]:
        """Create specialized investment strategy agents."""
        agents = [
            StrategyAgent(
                name="Conservative_Advisor",
                strategy_type=StrategyType.CONSERVATIVE,
                expertise_areas=["bonds", "CDs", "money_markets", "capital_preservation"],
                performance_history=0.85,
                llm_config=self.llm_config
            ),
            StrategyAgent(
                name="Aggressive_Advisor",
                strategy_type=StrategyType.AGGRESSIVE,
                expertise_areas=["growth_stocks", "emerging_markets", "high_risk_high_reward"],
                performance_history=0.78,
                llm_config=self.llm_config
            ),
            StrategyAgent(
                name="Moderate_Advisor",
                strategy_type=StrategyType.MODERATE,
                expertise_areas=["balanced_funds", "mixed_allocation", "moderate_growth"],
                performance_history=0.82,
                llm_config=self.llm_config
            ),
            StrategyAgent(
                name="Growth_Advisor",
                strategy_type=StrategyType.GROWTH,
                expertise_areas=["growth_stocks", "technology", "capital_appreciation"],
                performance_history=0.80,
                llm_config=self.llm_config
            ),
            StrategyAgent(
                name="Income_Advisor",
                strategy_type=StrategyType.INCOME,
                expertise_areas=["dividend_stocks", "REITs", "income_generation"],
                performance_history=0.83,
                llm_config=self.llm_config
            ),
            StrategyAgent(
                name="Balanced_Advisor",
                strategy_type=StrategyType.BALANCED,
                expertise_areas=["asset_allocation", "diversification", "risk_management"],
                performance_history=0.81,
                llm_config=self.llm_config
            )
        ]
        
        return agents
    
    def select_competing_agents(self, 
                              target_strategy: str, 
                              num_agents: int = 3) -> List[StrategyAgent]:
        """
        Select top agents for competition based on strategy matching.
        
        Args:
            target_strategy: Target investment strategy
            num_agents: Number of agents to select for competition
            
        Returns:
            List of selected agents
        """
        # Score all agents
        scores = self.competition_manager.score_agents(self.agents, target_strategy)
        
        # Select top performers
        selected_scores = scores[:num_agents]
        selected_agents = []
        
        for score in selected_scores:
            for agent in self.agents:
                if agent.name == score.agent_name:
                    selected_agents.append(agent)
                    break
        
        if self.enable_logging:
            print(f"Selected agents for strategy '{target_strategy}':")
            for score in selected_scores:
                print(f"  {score.agent_name}: {score.total_score:.3f}")
        
        return selected_agents
    
    async def orchestrate_task(self, 
                             parsed_goals: Dict[str, Any],
                             task_description: str = "Provide investment recommendation") -> Dict[str, Any]:
        """
        Orchestrate task distribution and agent competition.
        
        Args:
            parsed_goals: Parsed goals and constraints from goal-constraint parser
            task_description: Description of the task to perform
            
        Returns:
            Orchestration results with recommendations from competing agents
        """
        start_time = datetime.now()
        
        # Extract strategy from parsed goals
        strategy = parsed_goals.get('goals', {}).get('strategy', 'moderate')
        
        # Select competing agents
        competing_agents = self.select_competing_agents(strategy, num_agents=3)
        
        # Create task message
        task_message = self._create_task_message(parsed_goals, task_description)
        
        # Execute tasks with competing agents
        agent_results = []
        
        for agent in competing_agents:
            try:
                result = await self._execute_agent_task(agent, task_message)
                agent_results.append(result)
            except Exception as e:
                if self.enable_logging:
                    print(f"Error with agent {agent.name}: {e}")
                # Create fallback result
                fallback_result = TaskResult(
                    agent_name=agent.name,
                    strategy_type=agent.strategy_type,
                    recommendation={"error": str(e)},
                    reasoning="Agent execution failed",
                    confidence=0.0,
                    execution_time=0.0
                )
                agent_results.append(fallback_result)
        
        # Determine winner and compile results
        execution_time = (datetime.now() - start_time).total_seconds()
        
        results = {
            "task_description": task_description,
            "target_strategy": strategy,
            "execution_time": execution_time,
            "competing_agents": [agent.name for agent in competing_agents],
            "agent_results": [self._task_result_to_dict(result) for result in agent_results],
            "winner": self._determine_winner(agent_results),
            "consensus_recommendation": self._build_consensus(agent_results),
            "timestamp": start_time.isoformat()
        }
        
        # Store in history
        self.execution_history.append(results)
        
        return results
    
    def _create_task_message(self, parsed_goals: Dict[str, Any], task_description: str) -> str:
        """Create detailed task message for agents."""
        return f"""
{task_description}

Client Goals and Constraints:
{json.dumps(parsed_goals, indent=2)}

Please analyze this information and provide your specialized recommendation based on your expertise in {'{agent_strategy}'} strategies.

Respond in the following JSON format:
{{
    "recommendation": {{"allocation": {{}}, "specific_investments": [], "rationale": ""}},
    "reasoning": "Detailed explanation of your analysis and recommendation",
    "confidence": 0.85,
    "risk_assessment": {{"level": "medium", "factors": []}},
    "expected_return": {{"annual": 0.08, "range": "6-10%"}},
    "time_horizon": "5-7 years"
}}
"""
    
    async def _execute_agent_task(self, agent: StrategyAgent, task_message: str) -> TaskResult:
        """Execute task with a specific agent."""
        start_time = datetime.now()
        
        # Format task message with agent's strategy
        formatted_message = task_message.replace('{agent_strategy}', agent.strategy_type.value)
        
        try:
            # Simulate agent response (in real implementation, this would use AutoGen's chat)
            response = self._simulate_agent_response(agent, formatted_message)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return TaskResult(
                agent_name=agent.name,
                strategy_type=agent.strategy_type,
                recommendation=response.get("recommendation", {}),
                reasoning=response.get("reasoning", ""),
                confidence=response.get("confidence", 0.5),
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            raise Exception(f"Agent {agent.name} failed: {e}")
    
    def _simulate_agent_response(self, agent: StrategyAgent, message: str) -> Dict[str, Any]:
        """
        Simulate agent response based on strategy type.
        In a real implementation, this would use AutoGen's conversation system.
        """
        strategy = agent.strategy_type
        
        if strategy == StrategyType.CONSERVATIVE:
            return {
                "recommendation": {
                    "allocation": {"bonds": 60, "stocks": 30, "cash": 10},
                    "specific_investments": ["Treasury bonds", "High-grade corporate bonds", "Blue-chip dividend stocks"],
                    "rationale": "Focus on capital preservation with stable, low-risk investments"
                },
                "reasoning": "Conservative approach prioritizes safety and steady returns over growth",
                "confidence": 0.9,
                "risk_assessment": {"level": "low", "factors": ["market volatility", "inflation risk"]},
                "expected_return": {"annual": 0.05, "range": "4-6%"},
                "time_horizon": "Any timeframe"
            }
        elif strategy == StrategyType.AGGRESSIVE:
            return {
                "recommendation": {
                    "allocation": {"growth_stocks": 70, "emerging_markets": 20, "bonds": 10},
                    "specific_investments": ["Tech growth stocks", "Emerging market ETFs", "Small-cap funds"],
                    "rationale": "Maximize growth potential through high-risk, high-reward investments"
                },
                "reasoning": "Aggressive strategy targets maximum capital appreciation for long-term investors",
                "confidence": 0.75,
                "risk_assessment": {"level": "high", "factors": ["market volatility", "sector concentration"]},
                "expected_return": {"annual": 0.12, "range": "8-15%"},
                "time_horizon": "10+ years"
            }
        else:  # Moderate/Balanced
            return {
                "recommendation": {
                    "allocation": {"stocks": 60, "bonds": 35, "alternatives": 5},
                    "specific_investments": ["Index funds", "Balanced mutual funds", "REITs"],
                    "rationale": "Balanced approach between growth and stability"
                },
                "reasoning": "Moderate strategy balances risk and return for steady long-term growth",
                "confidence": 0.85,
                "risk_assessment": {"level": "medium", "factors": ["market cycles", "interest rate changes"]},
                "expected_return": {"annual": 0.08, "range": "6-10%"},
                "time_horizon": "5-10 years"
            }
    
    def _determine_winner(self, results: List[TaskResult]) -> Dict[str, Any]:
        """Determine the winning recommendation based on scoring."""
        if not results:
            return {"agent": "None", "reason": "No valid results"}
        
        # Score results based on confidence and strategy match
        best_result = max(results, key=lambda x: x.confidence)
        
        return {
            "agent": best_result.agent_name,
            "strategy": best_result.strategy_type.value,
            "confidence": best_result.confidence,
            "reason": f"Highest confidence ({best_result.confidence:.3f}) for this strategy type"
        }
    
    def _build_consensus(self, results: List[TaskResult]) -> Dict[str, Any]:
        """Build consensus recommendation from all agent results."""
        if not results:
            return {"message": "No consensus available"}
        
        # Extract common themes
        all_recommendations = [r.recommendation for r in results if r.recommendation]
        
        # Simple consensus (in real implementation, this would be more sophisticated)
        consensus = {
            "strategy_consensus": f"Based on {len(results)} expert opinions",
            "common_themes": [
                "Diversification is important",
                "Consider time horizon",
                "Match risk tolerance"
            ],
            "average_confidence": sum(r.confidence for r in results) / len(results),
            "recommendation_summary": "Implement a diversified portfolio aligned with risk tolerance"
        }
        
        return consensus
    
    def _task_result_to_dict(self, result: TaskResult) -> Dict[str, Any]:
        """Convert TaskResult to dictionary."""
        return {
            "agent_name": result.agent_name,
            "strategy_type": result.strategy_type.value,
            "recommendation": result.recommendation,
            "reasoning": result.reasoning,
            "confidence": result.confidence,
            "execution_time": result.execution_time,
            "timestamp": result.timestamp
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary of all agents."""
        summary = {
            "total_tasks": len(self.execution_history),
            "agent_scores": {name: score.__dict__ for name, score in self.competition_manager.agent_scores.items()},
            "recent_tasks": self.execution_history[-5:] if self.execution_history else []
        }
        
        return summary


# Convenience function for easy integration
async def orchestrate_investment_task(user_input: Dict[str, Any], 
                                    task_description: str = "Provide investment recommendation") -> Dict[str, Any]:
    """
    Convenience function to orchestrate investment tasks.
    
    Args:
        user_input: Raw user input with goals and constraints
        task_description: Description of the task
        
    Returns:
        Orchestration results
    """
    # Parse user input using our goal-constraint parser
    parsed_goals = parse_goal_constraints(user_input)
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Execute orchestration
    results = await orchestrator.orchestrate_task(parsed_goals, task_description)
    
    return results


if __name__ == "__main__":
    # Example usage
    async def main():
        sample_input = {
            "goals": {
                "strategy": "aggressive growth",
                "timeline": "15 years",
                "target_amount": 1000000,
                "risk_tolerance": "high"
            },
            "constraints": {
                "capital": 75000,
                "contributions": 3000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 85,
                "liquidity_needs": "low"
            }
        }
        
        result = await orchestrate_investment_task(sample_input)
        print(json.dumps(result, indent=2))
    
    # Run the example
    import asyncio
    asyncio.run(main())