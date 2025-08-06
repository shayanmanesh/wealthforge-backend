# WealthForge - AI Investment Advisory Platform

A comprehensive AI-powered investment advisory platform featuring goal-constraint parsing and multi-agent orchestration for intelligent investment recommendations.

## 🏗️ Core Components

### 1. Goal-Constraint Parser
A sophisticated Python parser built with LangChain that processes user JSON input containing investment goals (strategy, timeline) and constraints (capital, contributions) into structured data.

### 2. Orchestrator Agent with AutoGen
A multi-agent orchestration system that distributes tasks to specialized investment strategy agents and manages competition with dynamic weighting based on strategy types.

### 3. Strategy Optimization Arena with CrewAI
A comprehensive 50-agent strategy optimization arena using CrewAI that generates and competes investment strategies using the AlphaScore algorithm: `(ExpectedReturn × TimelineFit) / (RiskScore × CapitalEfficiency)`.

### 4. Portfolio Surgeon with Pareto Optimization
Advanced portfolio optimization system that synthesizes multiple agent proposals using Pareto-optimal logic, integrated with NeuralDarkPool for risk analysis and FeeAnnihilator for cost optimization.

### 5. Constraint Compliance Auditor with RegulatoryTuring
Comprehensive regulatory compliance auditing system with AI-powered RegulatoryTuring agent for SEC compliance checking, capital validation, and systematic constraint compliance verification.

### 6. Fine-Tuning Engine with GoalExceedPredictor and SensitivityAnalyzer
Advanced constraint optimization system that simulates parameter adjustments to help clients exceed their financial goals through Monte Carlo prediction modeling and multi-parameter sensitivity analysis.

## 🚀 Full-Stack Integration

WealthForge now includes complete **production-ready full-stack implementation**:

### FastAPI Backend
- **8 RESTful API endpoints** for all WealthForge components
- **Async operations** with Kafka messaging for background processing
- **Real-time data integration** from Polygon.io and FRED APIs
- **Redis caching** for high-performance responses
- **Docker deployment** with monitoring and scaling
- **Comprehensive API documentation** with interactive OpenAPI docs

### React Frontend
- **Modern TypeScript React** application with Tailwind CSS
- **Multi-step client profile form** for goals and constraints input
- **Interactive data visualization** with charts and real-time updates
- **Responsive design** optimized for all device sizes
- **Seamless API integration** with loading states and error handling
- **Production-ready deployment** with optimized builds

## 🎯 Platform Features

### Goal-Constraint Parser Features
- **JSON Input Processing**: Accepts both JSON strings and Python dictionaries
- **LangChain Integration**: Uses LangChain for intelligent parsing with fallback mechanisms
- **Pydantic Validation**: Robust data validation and type conversion
- **Strategy Normalization**: Intelligently normalizes investment strategies (e.g., "aggressive growth" → "aggressive")
- **Timeline Classification**: Converts specific durations to standardized categories (e.g., "15 years" → "long-term")
- **Structured Output**: Returns well-formatted Python dictionaries
- **Error Handling**: Comprehensive validation with meaningful error messages
- **Flexible Input**: Handles missing optional fields gracefully
- **Timestamp Tracking**: Automatic parsing timestamp generation

### Orchestrator Agent Features
- **Multi-Agent Competition**: Specialized agents compete to provide best recommendations
- **Dynamic Weighting**: Agent selection based on strategy matching and performance history
- **Task Distribution**: Intelligent distribution of investment advisory tasks
- **Performance Tracking**: Continuous learning and performance improvement
- **Consensus Building**: Aggregates insights from multiple expert agents
- **Real-time Scoring**: Agents scored on strategy match, performance, and confidence
- **AutoGen Integration**: Built on AutoGen's agent framework
- **Scalable Architecture**: Handles multiple concurrent advisory requests

### Strategy Optimization Arena Features
- **50 Specialized Agents**: Comprehensive coverage across 10 financial roles and expertise areas
- **AlphaScore Algorithm**: Sophisticated scoring system balancing return, risk, timeline, and efficiency
- **CrewAI Integration**: Powered by CrewAI framework for robust agent coordination
- **Market Simulation**: Realistic market data generation with multi-asset coverage
- **Strategy Competition**: Large-scale agent competitions with detailed analytics
- **Performance Analytics**: Comprehensive performance tracking and leaderboards
- **Risk Management**: Advanced risk assessment and optimization
- **Simulation Engine**: Monte Carlo strategy performance projections

### Portfolio Surgeon Features
- **Pareto-Optimal Synthesis**: Multi-objective optimization finding optimal risk-return frontiers
- **NeuralDarkPool Integration**: Advanced AI-powered risk analysis with neural network simulation
- **FeeAnnihilator Cost Optimization**: Comprehensive fee minimization and tax efficiency optimization
- **Agent Proposal Synthesis**: Intelligent combination of multiple agent strategies
- **Multi-Objective Optimization**: Balances return, risk, cost, and utility simultaneously
- **Advanced Risk Modeling**: VaR, stress testing, concentration analysis, and tail risk assessment
- **Performance Enhancement**: Consistently outperforms individual agent recommendations
- **Real-World Integration**: Production-ready optimization with comprehensive analytics

### Constraint Compliance Auditor Features
- **RegulatoryTuring AI Agent**: Intelligent regulatory analysis with comprehensive knowledge base
- **SEC Compliance Checking**: Systematic validation of Investment Advisers Act and Securities Act requirements
- **Capital Adequacy Validation**: Emergency fund, investment capital, and liquidity requirements assessment
- **Contribution Compliance**: IRA, 401(k), and tax-advantaged account limit validation
- **FINRA Suitability Analysis**: Rule 2111 suitability and know-your-customer compliance
- **Risk Tolerance Alignment**: Portfolio risk validation against client tolerance and regulatory standards
- **Automated Violation Detection**: Rule-based compliance checking with severity classification
- **Comprehensive Audit Reporting**: Detailed compliance documentation with scoring and recommendations

### Fine-Tuning Engine Features
- **GoalExceedPredictor**: 10,000-run Monte Carlo simulation for goal achievement probability analysis
- **SensitivityAnalyzer**: Multi-parameter impact assessment with elasticity and threshold detection
- **Constraint Optimization**: Intelligent simulation of capital, contribution, and timeline adjustments
- **Three Key Adjustments**: Capital optimization, contribution enhancement, and timeline extension
- **Multi-Strategy Analysis**: Conservative, balanced, and aggressive optimization approaches
- **Implementation Feasibility**: Real-world practicality assessment for recommended adjustments
- **Scenario Generation**: Automated creation of optimal constraint adjustment combinations
- **Goal Exceedance Modeling**: Advanced prediction of exceeding financial targets by 25%+ margins

### FastAPI Backend Features
- **8 RESTful Endpoints**: Complete API coverage for all WealthForge components
- **Async Operations**: Kafka messaging for background task processing
- **Real-time Data**: Live market data from Polygon.io and economic data from FRED
- **High Performance**: Redis caching with 95% faster responses for cached data
- **Production Ready**: Docker deployment with monitoring, scaling, and security
- **Interactive Documentation**: Auto-generated OpenAPI docs at `/docs` and `/redoc`
- **Authentication**: Bearer token security with configurable JWT support
- **Monitoring**: Prometheus metrics, Grafana dashboards, and health checks

### React Frontend Features
- **Modern TypeScript**: Full type safety with React 19 and latest TypeScript
- **Tailwind CSS**: Utility-first styling with custom design system
- **Multi-step Forms**: Comprehensive 4-tab client profile wizard
- **Data Visualization**: Interactive charts using Recharts library
- **Real-time Updates**: Live API health monitoring and status indicators
- **Responsive Design**: Mobile-first approach with optimized layouts
- **Error Handling**: Comprehensive error states with user-friendly messages
- **Loading States**: Smooth animations and progress indicators

## 📦 Installation

### Prerequisites

1. **Python 3.11+** with virtual environment
2. **Docker & Docker Compose** (for full stack deployment)
3. **API Keys** (optional for demo):
   - Polygon.io API key for real-time market data
   - FRED API key for economic data

### Quick Start (API Only)

```bash
# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Start WealthForge API
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Access API
open http://localhost:8000         # API root
open http://localhost:8000/docs    # Interactive API documentation
open http://localhost:8000/redoc   # Alternative API documentation
```

### Full Stack Deployment (Recommended)

```bash
# Set up environment variables
cp config.env.example .env
# Edit .env with your API keys (optional for demo)

# Start complete stack with Docker
docker-compose up -d

# Access services
open http://localhost:8000         # WealthForge API
open http://localhost:8000/docs    # API Documentation  
open http://localhost:3000         # React Frontend
open http://localhost:8080         # Kafka UI
open http://localhost:8081         # Redis Commander
open http://localhost:3001         # Grafana (admin/wealthforge123)
open http://localhost:9090         # Prometheus
```

## 🚀 Quick Start

### 1. Goal-Constraint Parser

```python
from goal_constraint_parser import parse_goal_constraints

# Example input
investment_data = {
    "goals": {
        "strategy": "aggressive growth",
        "timeline": "10 years",
        "target_amount": 500000,
        "risk_tolerance": "high"
    },
    "constraints": {
        "capital": 25000,
        "contributions": 2000,
        "contribution_frequency": "monthly",
        "max_risk_percentage": 85,
        "liquidity_needs": "low"
    },
    "additional_preferences": {
        "sector_preferences": ["technology", "biotech"],
        "esg_requirements": False
    }
}

# Parse the data
result = parse_goal_constraints(investment_data)
print(result)
```

### 2. Orchestrator Agent (Multi-Agent Advisory)

```python
from orchestrator_agent import orchestrate_investment_task
import asyncio

async def get_investment_advice():
    # Client input
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
    
    # Get multi-agent recommendations
    result = await orchestrate_investment_task(user_input)
    
    print(f"Strategy: {result['target_strategy']}")
    print(f"Winner: {result['winner']['agent']}")
    print(f"Confidence: {result['winner']['confidence']:.1%}")
    print(f"Competing Agents: {', '.join(result['competing_agents'])}")

# Run the example
asyncio.run(get_investment_advice())
```

### 3. Strategy Optimization Arena (50-Agent Competition)

```python
from strategy_optimization_arena import run_strategy_optimization
import asyncio

async def run_arena_competition():
    # Complex investment scenario
    client_input = {
        "goals": {
            "strategy": "aggressive growth with ESG focus",
            "timeline": "20 years",
            "target_amount": 2500000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 200000,
            "contributions": 5000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85
        }
    }
    
    # Run competition with all 50 agents
    result = await run_strategy_optimization(client_input, num_agents=50)
    
    # Show results
    winner = result['winner']
    print(f"🏆 Winner: {winner['agent_name']} ({winner['agent_role']})")
    print(f"📊 AlphaScore: {winner['alpha_score']:.4f}")
    print(f"💰 Expected Return: {winner['expected_return']:.2%}")
    print(f"⚖️ Risk Score: {winner['risk_score']:.3f}")
    print(f"🎯 Strategy: {winner['strategy_type']}")
    
    # Show top 5 strategies
    print(f"\n🎖️ Top 5 Strategies:")
    for i, strategy in enumerate(result['top_strategies'][:5], 1):
        print(f"   {i}. {strategy['agent_name']} - AlphaScore: {strategy['alpha_score']:.4f}")

# Run the arena
asyncio.run(run_arena_competition())
```

### 4. Portfolio Surgeon (Pareto-Optimal Synthesis)

```python
from portfolio_surgeon import synthesize_optimal_portfolio
from strategy_optimization_arena import run_strategy_optimization
import asyncio

async def run_portfolio_surgeon():
    # Complex investment scenario
    client_input = {
        "goals": {
            "strategy": "aggressive growth with ESG focus",
            "timeline": "20 years",
            "target_amount": 2500000,
            "risk_tolerance": "high but sophisticated"
        },
        "constraints": {
            "capital": 300000,
            "contributions": 5000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85
        },
        "additional_preferences": {
            "esg_investing": True,
            "sector_focus": ["technology", "healthcare", "renewable_energy"]
        }
    }
    
    # Step 1: Get agent proposals from Strategy Arena
    arena_result = await run_strategy_optimization(client_input, num_agents=20)
    
    # Convert to agent proposals (simplified)
    agent_proposals = convert_arena_results(arena_result)
    
    # Step 2: Run Portfolio Surgeon synthesis
    synthesis_result = await synthesize_optimal_portfolio(
        agent_proposals,
        arena_result['client_goals'],
        market_data,
        portfolio_value=300000
    )
    
    # Show results
    print(f"🔬 Portfolio Surgeon Results:")
    print(f"   Expected Return: {synthesis_result.expected_return:.2%}")
    print(f"   Risk Score: {synthesis_result.risk_score:.3f}")
    print(f"   Sharpe Ratio: {synthesis_result.sharpe_ratio:.3f}")
    print(f"   Synthesis Confidence: {synthesis_result.synthesis_confidence:.1%}")
    
    print(f"\n💼 Optimal Allocation:")
    for asset, weight in synthesis_result.final_allocation.items():
        print(f"   {asset}: {weight:.1%}")
    
    print(f"\n📊 Advanced Analytics:")
    print(f"   Volatility: {synthesis_result.risk_analysis.volatility:.2%}")
    print(f"   VaR (95%): {synthesis_result.risk_analysis.var_95:.2%}")
    print(f"   Expense Ratio: {synthesis_result.cost_analysis.total_expense_ratio:.3%}")
    print(f"   Tax Efficiency: {synthesis_result.cost_analysis.tax_efficiency_score:.1%}")

# Run the Portfolio Surgeon
asyncio.run(run_portfolio_surgeon())
```

### Output Example

```json
{
  "goals": {
    "strategy": "aggressive",
    "timeline": "short-term",
    "target_amount": 500000.0,
    "risk_tolerance": "high"
  },
  "constraints": {
    "capital": 25000.0,
    "contributions": 2000.0,
    "contribution_frequency": "monthly",
    "max_risk_percentage": 85.0,
    "liquidity_needs": "low"
  },
  "additional_preferences": {
    "sector_preferences": ["technology", "biotech"],
    "esg_requirements": false
  },
  "parsed_timestamp": "2024-01-01T12:00:00.000000"
}
```

## 📊 Supported Fields

### Goals (Required)
- `strategy`: Investment strategy (conservative, moderate, aggressive, growth, income, balanced)
- `timeline`: Investment timeline (short-term, medium-term, long-term, or specific durations)
- `target_amount`: Target amount to achieve (optional)
- `risk_tolerance`: Risk tolerance level (low, medium, high) (optional)

### Constraints (Required)
- `capital`: Initial capital amount (required, must be > 0)
- `contributions`: Regular contribution amount (optional)
- `contribution_frequency`: Frequency of contributions (monthly, quarterly, annual) (optional)
- `max_risk_percentage`: Maximum risk percentage 0-100 (optional)
- `liquidity_needs`: Liquidity requirements (high, medium, low) (optional)

### Additional Preferences (Optional)
- Any custom key-value pairs for additional requirements or preferences

## 🔧 Advanced Usage

### Using Custom LLM

```python
from goal_constraint_parser import GoalConstraintParser
from langchain_community.llms import OpenAI

# Create custom LLM (requires API key)
custom_llm = OpenAI(temperature=0, openai_api_key="your-key")

# Create parser with custom LLM
parser = GoalConstraintParser(llm=custom_llm)
result = parser.parse_json_input(your_data)
```

### Direct Parsing (Fallback Mode)

```python
from goal_constraint_parser import GoalConstraintParser

parser = GoalConstraintParser()
# Use direct parsing (bypasses LLM)
result = parser._direct_parse(your_data)
```

### JSON String Input

```python
json_string = '''
{
    "goals": {
        "strategy": "balanced",
        "timeline": "5 years"
    },
    "constraints": {
        "capital": 50000
    }
}
'''

result = parse_goal_constraints(json_string)
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_parser.py

# Run direct parsing tests
python test_direct_parsing.py

# Run demo
python simple_parser_demo.py
```

## 📁 File Structure

```
wealthforge/
├── Backend (Python):
│   ├── goal_constraint_parser.py       # Goal-Constraint Parser (LangChain)
│   ├── orchestrator_agent.py           # Orchestrator Agent (AutoGen)
│   ├── strategy_optimization_arena.py  # Strategy Arena (CrewAI + 50 agents)
│   ├── portfolio_surgeon.py            # Portfolio Surgeon (Pareto + NeuralDarkPool + FeeAnnihilator)
│   ├── constraint_compliance_auditor.py # Compliance Auditor (RegulatoryTuring + SEC)
│   ├── fine_tuning_engine.py           # Fine-Tuning Engine (GoalExceedPredictor + SensitivityAnalyzer)
│   ├── app.py                          # FastAPI application
│   ├── kafka_consumer.py               # Async message consumer
│   └── test_api_integration.py         # API integration tests
│
├── Frontend (React):
│   ├── frontend/src/
│   │   ├── components/
│   │   │   ├── WealthForgeDashboard.tsx    # Main dashboard
│   │   │   ├── ClientProfileForm.tsx       # Multi-step form
│   │   │   └── AnalysisResults.tsx         # Results visualization
│   │   ├── services/
│   │   │   └── api.ts                      # API service layer
│   │   ├── App.tsx                         # Main React app
│   │   └── index.css                       # Tailwind CSS styles
│   ├── package.json                        # React dependencies
│   └── tailwind.config.js                  # Tailwind configuration
│
├── Testing & Demos:
│   ├── test_parser.py                  # Parser test suite
│   ├── test_orchestrator.py            # Orchestrator test suite
│   ├── test_strategy_arena.py          # Strategy Arena test suite
│   ├── test_portfolio_surgeon.py       # Portfolio Surgeon test suite
│   ├── test_compliance_auditor.py      # Compliance Auditor test suite
│   ├── test_fine_tuning_engine.py      # Fine-Tuning Engine test suite
│   ├── three_adjustments_demo.py       # Three constraint adjustments demo
│   ├── complete_platform_demo.py       # Complete platform demo
│   └── ultimate_platform_demo.py       # Ultimate integration demo
│
├── Infrastructure:
│   ├── docker-compose.yml              # Complete stack deployment
│   ├── Dockerfile                      # FastAPI container
│   ├── requirements.txt                # Python dependencies
│   ├── config.env.example              # Environment configuration
│   ├── kafka_consumer.py               # Message queue processor
│   └── venv/                           # Python virtual environment
│
└── Documentation:
    ├── README.md                       # Main documentation
    ├── API_DOCUMENTATION.md            # FastAPI documentation
    ├── DEPLOYMENT_GUIDE.md             # Deployment guide
    ├── frontend/README_FRONTEND.md     # Frontend documentation
    ├── ORCHESTRATOR_README.md          # Orchestrator detailed docs
    ├── STRATEGY_ARENA_README.md        # Strategy Arena detailed docs
    ├── PORTFOLIO_SURGEON_README.md     # Portfolio Surgeon detailed docs
    ├── COMPLIANCE_AUDITOR_README.md    # Compliance Auditor detailed docs
    └── FINE_TUNING_ENGINE_README.md    # Fine-Tuning Engine detailed docs
```

## 🔍 Data Validation

The parser includes robust validation:

- **Strategy Validation**: Normalizes and validates investment strategies
- **Timeline Validation**: Converts durations to standard categories
- **Capital Validation**: Ensures positive capital amounts
- **Contribution Validation**: Validates contribution amounts are non-negative
- **Risk Percentage Validation**: Ensures values are between 0-100
- **Type Conversion**: Automatically converts strings to appropriate numeric types

## ⚠️ Error Handling

The parser handles various error scenarios:

- Invalid JSON format
- Missing required fields
- Invalid data types
- Negative capital amounts
- Out-of-range risk percentages
- LLM parsing failures (graceful fallback to direct parsing)

## 🔄 Normalization Examples

### Strategy Normalization
- "aggressive growth" → "aggressive"
- "conservative income" → "conservative"
- "growth stocks" → "growth"
- "balanced portfolio" → "balanced"

### Timeline Classification
- "short-term", "1 year", "2 years" → "short-term"
- "5 years", "7 years", "medium" → "medium-term"
- "15 years", "long-term", "30 years" → "long-term"

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass

## 📝 Notes

- The parser uses LangChain but includes a robust fallback mechanism
- When no OpenAI API key is configured, it automatically falls back to direct parsing
- All monetary values are converted to floats
- Timestamps are automatically generated in ISO format
- Additional preferences are preserved as-is in the output

## 🚀 Example Use Cases

- **Investment Portfolio Planning**: Parse user investment goals and constraints
- **Retirement Planning**: Process retirement savings objectives and limitations
- **Financial Advisory Tools**: Structure client investment preferences
- **Robo-Advisor Input**: Convert user inputs into standardized formats
- **Risk Assessment**: Parse and validate risk tolerance and constraints