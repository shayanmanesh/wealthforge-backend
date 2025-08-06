# Orchestrator Agent with AutoGen

A sophisticated multi-agent orchestration system that distributes investment advisory tasks to specialized agents and manages competition with dynamic weighting based on strategy types.

## 🎯 Overview

The Orchestrator Agent system creates a competitive environment where specialized investment strategy agents compete to provide the best recommendations for clients. The system uses dynamic weighting to select the most appropriate agents based on the client's investment strategy and requirements.

## 🏗️ Architecture

### Core Components

1. **OrchestratorAgent**: Main orchestrator that manages task distribution and agent competition
2. **StrategyAgent**: Specialized agents for different investment strategies 
3. **CompetitionManager**: Manages scoring and performance tracking
4. **Dynamic Weighting System**: Selects optimal agents based on strategy matching

### Agent Specializations

- **Conservative_Advisor**: Capital preservation, low-risk investments
- **Aggressive_Advisor**: High-growth, high-risk investments  
- **Moderate_Advisor**: Balanced growth and stability
- **Growth_Advisor**: Capital appreciation focused
- **Income_Advisor**: Dividend and income generation
- **Balanced_Advisor**: Diversified asset allocation

## 🚀 Key Features

### Multi-Agent Competition
- **Strategy Matching**: Agents are scored based on how well they match the target strategy
- **Performance History**: Historical success rates influence agent selection
- **Confidence Scoring**: Agents provide confidence levels for their recommendations
- **Dynamic Selection**: Top 3 agents compete for each task

### Dynamic Weighting System
```python
total_score = (strategy_match * 0.4 + 
               performance_score * 0.3 + 
               confidence * 0.3)
```

### Competition Management
- **Real-time Scoring**: Agents are scored for each task
- **Performance Tracking**: Success rates are tracked and updated
- **Learning System**: Agent performance improves over time
- **Consensus Building**: Multiple expert opinions are aggregated

## 🔧 Usage

### Basic Usage

```python
from orchestrator_agent import orchestrate_investment_task

# Client input with goals and constraints
user_input = {
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

# Execute orchestration
result = await orchestrate_investment_task(user_input)
```

### Advanced Usage

```python
from orchestrator_agent import OrchestratorAgent
from goal_constraint_parser import parse_goal_constraints

# Create orchestrator with custom configuration
orchestrator = OrchestratorAgent(enable_logging=True)

# Parse user input
parsed_goals = parse_goal_constraints(user_input)

# Execute with custom task description
result = await orchestrator.orchestrate_task(
    parsed_goals, 
    "Provide comprehensive retirement planning recommendation"
)
```

## 📊 Strategy Matching Examples

The orchestrator intelligently matches agents to strategies:

| Input Strategy | Top Agent | Match Score |
|---------------|-----------|-------------|
| "aggressive growth" | Growth_Advisor | 0.94 |
| "conservative income" | Conservative_Advisor | 1.0 |
| "balanced portfolio" | Balanced_Advisor | 0.95 |
| "capital preservation" | Conservative_Advisor | 0.85 |

## 🏆 Competition Process

1. **Task Received**: Orchestrator receives parsed goals and constraints
2. **Agent Scoring**: All agents are scored for strategy match
3. **Selection**: Top 3 agents are selected for competition
4. **Execution**: Each agent provides recommendations
5. **Winner Selection**: Best recommendation based on confidence and fit
6. **Consensus**: Aggregate insights from all competing agents

## 📈 Performance Tracking

```python
# Get performance summary
summary = orchestrator.get_performance_summary()

print(f"Total tasks: {summary['total_tasks']}")
for agent, score in summary['agent_scores'].items():
    print(f"{agent}: {score['performance_score']:.3f}")
```

## 🎪 Demo Scenarios

### Young Professional (Aggressive Growth)
- **Profile**: 28-year-old software engineer
- **Strategy**: Aggressive growth for retirement
- **Timeline**: 35 years
- **Result**: Growth_Advisor wins with 94% confidence

### Pre-Retiree (Conservative Income)
- **Profile**: 58-year-old nearing retirement
- **Strategy**: Income and capital preservation
- **Timeline**: 7 years to retirement
- **Result**: Conservative_Advisor wins with 95% confidence

### Family Planning (Balanced Approach)
- **Profile**: Family with children
- **Strategy**: Education and retirement savings
- **Timeline**: 15 years for college, 30 for retirement
- **Result**: Balanced_Advisor wins with 88% confidence

## 🔄 Integration with Goal-Constraint Parser

The orchestrator seamlessly integrates with the Goal-Constraint Parser:

```python
# Raw user input is automatically parsed
raw_input = {
    "goals": {"strategy": "I want aggressive growth", "timeline": "20 years"},
    "constraints": {"capital": 50000}
}

# Orchestrator handles parsing and execution
result = await orchestrate_investment_task(raw_input)
```

## 📋 Output Structure

```json
{
  "task_description": "Provide investment recommendation",
  "target_strategy": "aggressive",
  "execution_time": 0.05,
  "competing_agents": ["Growth_Advisor", "Aggressive_Advisor", "Moderate_Advisor"],
  "agent_results": [
    {
      "agent_name": "Growth_Advisor",
      "strategy_type": "growth",
      "recommendation": {
        "allocation": {"growth_stocks": 70, "emerging_markets": 20, "bonds": 10},
        "specific_investments": ["Tech ETFs", "Growth funds"],
        "rationale": "Maximize growth potential"
      },
      "reasoning": "Growth strategy targets long-term appreciation",
      "confidence": 0.92,
      "execution_time": 0.01
    }
  ],
  "winner": {
    "agent": "Growth_Advisor",
    "strategy": "growth",
    "confidence": 0.92,
    "reason": "Highest confidence for this strategy type"
  },
  "consensus_recommendation": {
    "strategy_consensus": "Based on 3 expert opinions",
    "average_confidence": 0.87,
    "recommendation_summary": "Implement diversified growth portfolio"
  }
}
```

## 🧪 Testing

Run comprehensive tests:

```bash
# Test all functionality
python test_orchestrator.py

# Run practical demos
python orchestrator_demo.py
```

## ⚖️ Dynamic Weighting Details

### Strategy Match Scoring
- **Direct Match**: 1.0 (e.g., "aggressive" → Aggressive_Advisor)
- **Partial Match**: 0.7 (e.g., "growth stocks" → Growth_Advisor)
- **Related Terms**: 0.5 (e.g., "long-term" → Growth_Advisor)
- **Default**: 0.3 (any agent can provide basic advice)

### Performance Updates
- **Exponential Moving Average**: New performance = 0.7 × old + 0.3 × new
- **Real-time Learning**: Performance improves based on success rates
- **Adaptive Selection**: Better-performing agents get selected more often

## 🔧 Configuration

### Custom LLM Configuration
```python
orchestrator = OrchestratorAgent(
    llm_config={
        "timeout": 120,
        "temperature": 0.1,
        "config_list": [{"model": "gpt-4", "api_key": "your-key"}]
    }
)
```

### Agent Customization
```python
custom_agent = StrategyAgent(
    name="ESG_Advisor",
    strategy_type=StrategyType.BALANCED,
    expertise_areas=["ESG_investing", "sustainable_funds"],
    performance_history=0.9
)
```

## 🤝 Integration Points

1. **Goal-Constraint Parser**: Automatic parsing of user inputs
2. **AutoGen Framework**: Built on AutoGen's agent architecture
3. **LangChain**: Compatible with LangChain LLM integrations
4. **Pydantic**: Robust data validation and type checking

## 📊 Performance Metrics

- **Task Distribution**: Intelligent agent selection
- **Competition Efficiency**: Sub-second agent competition
- **Accuracy**: High-confidence recommendations
- **Learning**: Adaptive performance improvement
- **Scalability**: Handles multiple concurrent tasks

## 🎯 Use Cases

1. **Robo-Advisory Platforms**: Automated investment recommendations
2. **Financial Planning Tools**: Multi-perspective financial advice
3. **Investment Research**: Comparative strategy analysis
4. **Client Advisory**: Human advisor augmentation
5. **Risk Assessment**: Multi-agent risk evaluation

## 🚀 Future Enhancements

- **Real AutoGen Integration**: Full AutoGen chat capabilities
- **Market Data Integration**: Real-time market data incorporation
- **Backtesting**: Historical performance simulation
- **Custom Agent Training**: Domain-specific agent development
- **API Integration**: REST API for web applications

The Orchestrator Agent system provides a sophisticated, scalable solution for multi-agent investment advisory with intelligent task distribution and competitive recommendation generation.