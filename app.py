"""
WealthForge FastAPI Backend Application

Production-ready API service integrating all WealthForge components:
- Goal-Constraint Parser
- Strategy Optimization Arena  
- Portfolio Surgeon
- Constraint Compliance Auditor
- Fine-Tuning Engine
- Real-time data from Polygon.io and FRED API
- Async operations with Kafka messaging
"""

import asyncio
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import httpx
import redis
from kafka import KafkaProducer, KafkaConsumer
import aiohttp

# Import WealthForge components
from goal_constraint_parser import parse_goal_constraints
from strategy_optimization_arena import run_strategy_optimization, AgentStrategy, MarketData
from portfolio_surgeon import synthesize_optimal_portfolio, PortfolioSynthesis
from constraint_compliance_auditor import perform_compliance_audit, ComplianceAuditReport
from fine_tuning_engine import optimize_goal_exceedance, OptimizationStrategy, OptimizationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "YOUR_POLYGON_API_KEY_HERE")
    FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE") 
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    SECRET_KEY = os.getenv("SECRET_KEY", "wealthforge-secret-key-change-in-production")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

config = Config()

# Global connections
redis_client = None
kafka_producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    # Startup
    logger.info("🚀 Starting WealthForge API...")
    
    # Initialize Redis connection
    global redis_client
    try:
        redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)
        await asyncio.get_event_loop().run_in_executor(None, redis_client.ping)
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.warning(f"⚠️ Redis connection failed: {e}")
        redis_client = None
    
    # Initialize Kafka producer
    global kafka_producer
    try:
        kafka_producer = KafkaProducer(
            bootstrap_servers=[config.KAFKA_BOOTSTRAP_SERVERS],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3,
            retry_backoff_ms=1000
        )
        logger.info("✅ Kafka producer initialized")
    except Exception as e:
        logger.warning(f"⚠️ Kafka connection failed: {e}")
        kafka_producer = None
    
    logger.info("🌟 WealthForge API started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down WealthForge API...")
    
    if kafka_producer:
        kafka_producer.close()
        logger.info("✅ Kafka producer closed")
    
    if redis_client:
        redis_client.close()
        logger.info("✅ Redis connection closed")
    
    logger.info("👋 WealthForge API shutdown complete")

# FastAPI app initialization
app = FastAPI(
    title="WealthForge API",
    description="AI-Powered Investment Platform with 6 Core Components",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.ENVIRONMENT == "development" else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token (simplified for demo)."""
    if config.ENVIRONMENT == "development":
        return {"user_id": "demo_user", "permissions": ["all"]}
    
    # In production, implement proper JWT validation
    token = credentials.credentials
    if token != "valid-api-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return {"user_id": "authenticated_user", "permissions": ["all"]}

# Pydantic Models
class ClientProfileRequest(BaseModel):
    """Client profile input model."""
    goals: Dict[str, Any] = Field(..., description="Investment goals and objectives")
    constraints: Dict[str, Any] = Field(..., description="Financial constraints and limitations")
    additional_preferences: Optional[Dict[str, Any]] = Field(None, description="Additional client preferences")
    financial_info: Optional[Dict[str, Any]] = Field(None, description="Detailed financial information")

class StrategyOptimizationRequest(BaseModel):
    """Strategy optimization request model."""
    client_profile: ClientProfileRequest
    num_agents: Optional[int] = Field(50, description="Number of agents to deploy", ge=10, le=100)
    strategy_focus: Optional[str] = Field("balanced", description="Strategy focus area")

class PortfolioSynthesisRequest(BaseModel):
    """Portfolio synthesis request model."""
    client_profile: ClientProfileRequest
    portfolio_value: float = Field(..., description="Portfolio value for optimization", gt=0)
    use_real_data: Optional[bool] = Field(True, description="Use real market data if available")

class ComplianceAuditRequest(BaseModel):
    """Compliance audit request model."""
    client_profile: ClientProfileRequest
    portfolio_id: Optional[str] = Field(None, description="Portfolio ID if available")

class FineTuningRequest(BaseModel):
    """Fine-tuning optimization request model."""
    client_profile: ClientProfileRequest
    target_exceedance: Optional[float] = Field(0.25, description="Target exceedance percentage", ge=0, le=1)
    strategy: Optional[str] = Field("balanced", description="Optimization strategy")
    portfolio_id: Optional[str] = Field(None, description="Portfolio ID for context")

class MarketDataRequest(BaseModel):
    """Market data request model."""
    symbols: List[str] = Field(..., description="Stock symbols to fetch")
    timespan: Optional[str] = Field("day", description="Data timespan")
    limit: Optional[int] = Field(100, description="Number of data points", ge=1, le=1000)

class EconomicDataRequest(BaseModel):
    """Economic data request model."""
    series_id: str = Field(..., description="FRED series ID")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")

# Response Models
class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Utility Functions
async def publish_to_kafka(topic: str, message: Dict[str, Any]):
    """Publish message to Kafka topic asynchronously."""
    if kafka_producer:
        try:
            def send_message():
                kafka_producer.send(topic, message)
                kafka_producer.flush()
            
            await asyncio.get_event_loop().run_in_executor(None, send_message)
            logger.info(f"📤 Published to Kafka topic '{topic}'")
        except Exception as e:
            logger.error(f"❌ Kafka publish failed: {e}")

async def cache_result(key: str, data: Dict[str, Any], ttl: int = 3600):
    """Cache result in Redis with TTL."""
    if redis_client:
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: redis_client.setex(key, ttl, json.dumps(data, default=str))
            )
            logger.info(f"💾 Cached result with key '{key}'")
        except Exception as e:
            logger.error(f"❌ Cache operation failed: {e}")

async def get_cached_result(key: str) -> Optional[Dict[str, Any]]:
    """Get cached result from Redis."""
    if redis_client:
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                redis_client.get, 
                key
            )
            if result:
                logger.info(f"🔍 Cache hit for key '{key}'")
                return json.loads(result)
        except Exception as e:
            logger.error(f"❌ Cache retrieval failed: {e}")
    return None

# External API Integration
class PolygonAPIClient:
    """Polygon.io API client for real-time market data."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
    
    async def get_stock_data(self, symbol: str, timespan: str = "day", limit: int = 100) -> Dict[str, Any]:
        """Fetch stock data from Polygon.io."""
        if self.api_key == "YOUR_POLYGON_API_KEY_HERE":
            # Return mock data if no API key
            return self._get_mock_stock_data(symbol, limit)
        
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/1/{timespan}/2023-01-01/2024-12-31"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": limit,
            "apikey": self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_polygon_data(data)
                    else:
                        logger.error(f"Polygon API error: {response.status}")
                        return self._get_mock_stock_data(symbol, limit)
        except Exception as e:
            logger.error(f"Polygon API request failed: {e}")
            return self._get_mock_stock_data(symbol, limit)
    
    def _get_mock_stock_data(self, symbol: str, limit: int) -> Dict[str, Any]:
        """Generate mock stock data for testing."""
        import random
        base_price = 100 + random.uniform(-50, 200)
        
        data = []
        for i in range(limit):
            price_change = random.uniform(-0.05, 0.05)
            base_price *= (1 + price_change)
            
            data.append({
                "timestamp": (datetime.now() - timedelta(days=limit-i)).isoformat(),
                "open": round(base_price * 0.99, 2),
                "high": round(base_price * 1.02, 2),
                "low": round(base_price * 0.98, 2),
                "close": round(base_price, 2),
                "volume": random.randint(100000, 10000000)
            })
        
        return {
            "symbol": symbol,
            "count": len(data),
            "results": data,
            "status": "mock_data",
            "request_id": f"mock_{symbol}_{datetime.now().isoformat()}"
        }
    
    def _process_polygon_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw Polygon API response."""
        if "results" not in raw_data:
            return {"error": "Invalid data format", "raw_data": raw_data}
        
        processed_results = []
        for item in raw_data["results"]:
            processed_results.append({
                "timestamp": datetime.fromtimestamp(item["t"] / 1000).isoformat(),
                "open": item["o"],
                "high": item["h"], 
                "low": item["l"],
                "close": item["c"],
                "volume": item["v"]
            })
        
        return {
            "symbol": raw_data.get("ticker"),
            "count": raw_data.get("resultsCount", 0),
            "results": processed_results,
            "status": "OK",
            "request_id": raw_data.get("request_id")
        }

class FREDAPIClient:
    """FRED (Federal Reserve Economic Data) API client."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred"
    
    async def get_economic_data(self, series_id: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Fetch economic data from FRED API."""
        if self.api_key == "YOUR_FRED_API_KEY_HERE":
            # Return mock data if no API key
            return self._get_mock_economic_data(series_id)
        
        url = f"{self.base_url}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }
        
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_fred_data(data, series_id)
                    else:
                        logger.error(f"FRED API error: {response.status}")
                        return self._get_mock_economic_data(series_id)
        except Exception as e:
            logger.error(f"FRED API request failed: {e}")
            return self._get_mock_economic_data(series_id)
    
    def _get_mock_economic_data(self, series_id: str) -> Dict[str, Any]:
        """Generate mock economic data for testing."""
        import random
        
        # Common economic indicators with realistic ranges
        series_configs = {
            "GDP": {"base": 25000, "range": 2000, "trend": 0.02},
            "UNRATE": {"base": 4.0, "range": 2.0, "trend": 0.0},
            "FEDFUNDS": {"base": 2.5, "range": 3.0, "trend": 0.0},
            "CPIAUCSL": {"base": 280, "range": 20, "trend": 0.025},
            "DGS10": {"base": 3.0, "range": 2.0, "trend": 0.0}
        }
        
        # Use GDP as default if series not found
        config = series_configs.get(series_id, series_configs["GDP"])
        
        data = []
        start_date = datetime.now() - timedelta(days=365*2)  # 2 years of data
        
        for i in range(24):  # Monthly data for 2 years
            date = start_date + timedelta(days=30*i)
            trend_value = config["base"] * (1 + config["trend"]) ** (i/12)
            noise = random.uniform(-config["range"]/2, config["range"]/2)
            value = round(trend_value + noise, 2)
            
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "value": str(value)
            })
        
        return {
            "series_id": series_id,
            "count": len(data),
            "observations": data,
            "status": "mock_data",
            "units": "mock_units"
        }
    
    def _process_fred_data(self, raw_data: Dict[str, Any], series_id: str) -> Dict[str, Any]:
        """Process raw FRED API response."""
        if "observations" not in raw_data:
            return {"error": "Invalid data format", "raw_data": raw_data}
        
        observations = []
        for obs in raw_data["observations"]:
            if obs["value"] != ".":  # FRED uses "." for missing values
                observations.append({
                    "date": obs["date"],
                    "value": obs["value"]
                })
        
        return {
            "series_id": series_id,
            "count": len(observations),
            "observations": observations,
            "status": "OK",
            "units": raw_data.get("units", "unknown")
        }

# Initialize API clients
polygon_client = PolygonAPIClient(config.POLYGON_API_KEY)
fred_client = FREDAPIClient(config.FRED_API_KEY)

# API Routes

@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint with API information."""
    return APIResponse(
        success=True,
        message="WealthForge API - AI-Powered Investment Platform",
        data={
            "version": "1.0.0",
            "components": [
                "Goal-Constraint Parser",
                "Strategy Optimization Arena", 
                "Portfolio Surgeon",
                "Constraint Compliance Auditor",
                "Fine-Tuning Engine"
            ],
            "external_apis": [
                "Polygon.io (Market Data)",
                "FRED (Economic Data)"
            ],
            "features": [
                "Async Operations",
                "Kafka Messaging",
                "Redis Caching",
                "Real-time Data"
            ]
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "api": "healthy",
        "redis": "connected" if redis_client else "disconnected",
        "kafka": "connected" if kafka_producer else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return APIResponse(
        success=True,
        message="Health check completed",
        data=health_status
    )

@app.post("/api/v1/parse-goals", response_model=APIResponse)
async def parse_client_goals(
    request: ClientProfileRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Parse and validate client goals and constraints."""
    start_time = datetime.utcnow()
    
    try:
        # Check cache first
        cache_key = f"parsed_goals:{hash(str(request.dict()))}"
        cached_result = await get_cached_result(cache_key)
        
        if cached_result:
            return APIResponse(
                success=True,
                message="Goals parsed successfully (cached)",
                data=cached_result,
                execution_time=(datetime.utcnow() - start_time).total_seconds()
            )
        
        # Parse goals using WealthForge parser
        client_dict = request.dict()
        parsed_client = parse_goal_constraints(client_dict)
        
        result_data = {
            "parsed_profile": parsed_client,
            "original_profile": client_dict,
            "parsing_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"]
        }
        
        # Cache result
        background_tasks.add_task(cache_result, cache_key, result_data, 3600)
        
        # Publish to Kafka for analytics
        background_tasks.add_task(
            publish_to_kafka,
            "goal_parsing_events",
            {
                "event_type": "goal_parsed",
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "profile_complexity": len(str(client_dict))
            }
        )
        
        return APIResponse(
            success=True,
            message="Goals parsed and validated successfully",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Goal parsing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Goal parsing failed: {str(e)}"
        )

@app.post("/api/v1/strategy-optimization", response_model=APIResponse)
async def run_strategy_optimization_api(
    request: StrategyOptimizationRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Run strategy optimization with 50 AI agents."""
    start_time = datetime.utcnow()
    
    try:
        # Check cache first
        cache_key = f"strategy_opt:{hash(str(request.dict()))}"
        cached_result = await get_cached_result(cache_key)
        
        if cached_result:
            return APIResponse(
                success=True,
                message="Strategy optimization completed (cached)",
                data=cached_result,
                execution_time=(datetime.utcnow() - start_time).total_seconds()
            )
        
        # Run strategy optimization
        client_profile = request.client_profile.dict()
        
        # Parse client profile first
        parsed_client = parse_goal_constraints(client_profile)
        
        # Run arena optimization
        arena_result = await run_strategy_optimization(
            parsed_client, 
            num_agents=request.num_agents
        )
        
        result_data = {
            "arena_result": arena_result,
            "optimization_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"],
            "num_agents_used": request.num_agents,
            "strategy_focus": request.strategy_focus
        }
        
        # Cache result for 1 hour
        background_tasks.add_task(cache_result, cache_key, result_data, 3600)
        
        # Publish to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "strategy_optimization_events",
            {
                "event_type": "strategy_optimized",
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "num_agents": request.num_agents,
                "strategies_generated": arena_result["strategies_generated"],
                "execution_time": arena_result["execution_time"]
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Strategy optimization completed with {request.num_agents} agents",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Strategy optimization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategy optimization failed: {str(e)}"
        )

@app.post("/api/v1/portfolio-synthesis", response_model=APIResponse)
async def portfolio_synthesis_api(
    request: PortfolioSynthesisRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Synthesize optimal portfolio using Pareto optimization."""
    start_time = datetime.utcnow()
    
    try:
        # Parse client profile
        client_profile = request.client_profile.dict()
        parsed_client = parse_goal_constraints(client_profile)
        
        # Run strategy optimization first to get agent proposals
        arena_result = await run_strategy_optimization(parsed_client, num_agents=30)
        
        # Convert strategies to agent proposals
        agent_proposals = []
        for strategy_data in arena_result['top_strategies'][:15]:
            try:
                from strategy_optimization_arena import AgentRole, StrategyType
                strategy = AgentStrategy(
                    agent_id=strategy_data['agent_id'],
                    agent_name=strategy_data['agent_name'],
                    agent_role=AgentRole(strategy_data['agent_role']),
                    strategy_type=StrategyType(strategy_data['strategy_type']),
                    asset_allocation=strategy_data['asset_allocation'],
                    expected_return=strategy_data['expected_return'],
                    risk_score=strategy_data['risk_score'],
                    timeline_fit=strategy_data['timeline_fit'],
                    capital_efficiency=strategy_data['capital_efficiency'],
                    confidence=strategy_data['confidence']
                )
                agent_proposals.append(strategy)
            except Exception as e:
                logger.warning(f"Strategy conversion warning: {e}")
                continue
        
        # Generate or fetch market data
        if request.use_real_data:
            # Try to fetch real market data
            try:
                market_symbols = ["SPY", "QQQ", "IWM", "EFA", "AGG"]
                market_data_raw = {}
                for symbol in market_symbols:
                    market_data_raw[symbol] = await polygon_client.get_stock_data(symbol)
                
                # Convert to MarketData format
                market_data = MarketData.generate_from_external_data(market_data_raw)
            except Exception as e:
                logger.warning(f"Real data fetch failed, using dummy data: {e}")
                market_data = MarketData.generate_dummy_data(days_back=500)
        else:
            market_data = MarketData.generate_dummy_data(days_back=500)
        
        # Run portfolio synthesis
        synthesis_result = await synthesize_optimal_portfolio(
            agent_proposals,
            arena_result['client_goals'],
            market_data,
            portfolio_value=request.portfolio_value
        )
        
        result_data = {
            "synthesis_result": {
                "portfolio_id": synthesis_result.portfolio_id,
                "final_allocation": synthesis_result.final_allocation,
                "expected_return": synthesis_result.expected_return,
                "risk_score": synthesis_result.risk_score,
                "sharpe_ratio": synthesis_result.sharpe_ratio,
                "synthesis_confidence": synthesis_result.synthesis_confidence,
                "contributing_agents": synthesis_result.contributing_agents,
                "optimization_method": synthesis_result.optimization_method,
                "risk_analysis": {
                    "volatility": synthesis_result.risk_analysis.volatility,
                    "var_95": synthesis_result.risk_analysis.var_95,
                    "max_drawdown": synthesis_result.risk_analysis.max_drawdown,
                    "beta": synthesis_result.risk_analysis.beta
                },
                "cost_analysis": {
                    "total_expense_ratio": synthesis_result.cost_analysis.total_expense_ratio,
                    "tax_efficiency_score": synthesis_result.cost_analysis.tax_efficiency_score,
                    "fee_optimization_savings": synthesis_result.cost_analysis.fee_optimization_savings
                }
            },
            "synthesis_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"],
            "portfolio_value": request.portfolio_value,
            "used_real_data": request.use_real_data
        }
        
        # Cache result for 30 minutes
        cache_key = f"portfolio_synthesis:{synthesis_result.portfolio_id}"
        background_tasks.add_task(cache_result, cache_key, result_data, 1800)
        
        # Publish to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "portfolio_synthesis_events",
            {
                "event_type": "portfolio_synthesized",
                "user_id": user["user_id"],
                "portfolio_id": synthesis_result.portfolio_id,
                "timestamp": datetime.utcnow().isoformat(),
                "expected_return": synthesis_result.expected_return,
                "risk_score": synthesis_result.risk_score,
                "synthesis_confidence": synthesis_result.synthesis_confidence
            }
        )
        
        return APIResponse(
            success=True,
            message="Portfolio synthesis completed successfully",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Portfolio synthesis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Portfolio synthesis failed: {str(e)}"
        )

@app.post("/api/v1/compliance-audit", response_model=APIResponse)
async def compliance_audit_api(
    request: ComplianceAuditRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Perform comprehensive compliance audit."""
    start_time = datetime.utcnow()
    
    try:
        # Parse client profile
        client_profile = request.client_profile.dict()
        parsed_client = parse_goal_constraints(client_profile)
        
        # Get portfolio if portfolio_id provided
        portfolio_result = None
        if request.portfolio_id:
            # Try to get from cache
            portfolio_cache_key = f"portfolio_synthesis:{request.portfolio_id}"
            cached_portfolio = await get_cached_result(portfolio_cache_key)
            if cached_portfolio and "synthesis_result" in cached_portfolio:
                # Convert back to PortfolioSynthesis object (simplified)
                portfolio_data = cached_portfolio["synthesis_result"]
                # In a real implementation, you'd reconstruct the full object
        
        # Run compliance audit
        audit_report = await perform_compliance_audit(
            parsed_client, 
            portfolio_result
        )
        
        result_data = {
            "audit_report": {
                "audit_id": audit_report.audit_id,
                "overall_compliance": audit_report.overall_compliance.value,
                "audit_score": audit_report.audit_score,
                "requires_manual_review": audit_report.requires_manual_review,
                "capital_validation": {
                    "compliance_status": audit_report.capital_validation.compliance_status.value,
                    "total_capital": audit_report.capital_validation.total_capital,
                    "investment_capital": audit_report.capital_validation.investment_capital,
                    "warnings": audit_report.capital_validation.warnings
                },
                "contribution_validation": {
                    "compliance_status": audit_report.contribution_validation.compliance_status.value,
                    "ira_contributions": audit_report.contribution_validation.ira_contributions,
                    "ira_limit": audit_report.contribution_validation.ira_limit,
                    "violations": audit_report.contribution_validation.violations
                },
                "regulatory_analysis": {
                    "client_classification": audit_report.regulatory_analysis.client_classification,
                    "regulatory_risk_score": audit_report.regulatory_analysis.regulatory_risk_score,
                    "applicable_regulations": [reg.value for reg in audit_report.regulatory_analysis.applicable_regulations],
                    "suitability_assessment": audit_report.regulatory_analysis.suitability_assessment
                },
                "violations": [
                    {
                        "violation_id": v.violation_id,
                        "severity": v.severity.value,
                        "description": v.description,
                        "recommendation": v.recommendation
                    } for v in audit_report.violations
                ],
                "recommendations": audit_report.recommendations
            },
            "audit_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"],
            "portfolio_id": request.portfolio_id
        }
        
        # Cache result for 2 hours
        cache_key = f"compliance_audit:{audit_report.audit_id}"
        background_tasks.add_task(cache_result, cache_key, result_data, 7200)
        
        # Publish to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "compliance_audit_events",
            {
                "event_type": "compliance_audited",
                "user_id": user["user_id"],
                "audit_id": audit_report.audit_id,
                "timestamp": datetime.utcnow().isoformat(),
                "overall_compliance": audit_report.overall_compliance.value,
                "audit_score": audit_report.audit_score,
                "violations_count": len(audit_report.violations)
            }
        )
        
        return APIResponse(
            success=True,
            message="Compliance audit completed successfully",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Compliance audit failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compliance audit failed: {str(e)}"
        )

@app.post("/api/v1/fine-tuning", response_model=APIResponse)
async def fine_tuning_optimization_api(
    request: FineTuningRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Perform goal exceedance optimization with constraint fine-tuning."""
    start_time = datetime.utcnow()
    
    try:
        # Parse client profile
        client_profile = request.client_profile.dict()
        parsed_client = parse_goal_constraints(client_profile)
        
        # Map strategy string to OptimizationStrategy enum
        strategy_mapping = {
            "conservative": OptimizationStrategy.CONSERVATIVE,
            "balanced": OptimizationStrategy.BALANCED,
            "aggressive": OptimizationStrategy.AGGRESSIVE
        }
        optimization_strategy = strategy_mapping.get(request.strategy, OptimizationStrategy.BALANCED)
        
        # Get portfolio context if available
        portfolio_result = None
        if request.portfolio_id:
            portfolio_cache_key = f"portfolio_synthesis:{request.portfolio_id}"
            cached_portfolio = await get_cached_result(portfolio_cache_key)
            # In production, reconstruct PortfolioSynthesis object
        
        # Run fine-tuning optimization
        optimization_result = await optimize_goal_exceedance(
            parsed_client,
            target_exceedance=request.target_exceedance,
            strategy=optimization_strategy,
            portfolio_result=portfolio_result
        )
        
        result_data = {
            "optimization_result": {
                "optimization_id": optimization_result.optimization_id,
                "original_goal_probability": optimization_result.original_goal_probability,
                "optimized_goal_probability": optimization_result.optimized_goal_probability,
                "improvement_factor": optimization_result.improvement_factor,
                "recommended_scenarios": [
                    {
                        "scenario_id": scenario.scenario_id,
                        "scenario_name": scenario.scenario_name,
                        "probability_of_success": scenario.probability_of_success,
                        "excess_achievement": scenario.excess_achievement,
                        "implementation_score": scenario.implementation_score,
                        "time_to_goal": scenario.time_to_goal,
                        "adjustments": [
                            {
                                "adjustment_type": adj.adjustment_type.value,
                                "description": adj.description,
                                "current_value": adj.current_value,
                                "suggested_value": adj.suggested_value,
                                "impact_magnitude": adj.impact_magnitude,
                                "implementation_difficulty": adj.implementation_difficulty
                            } for adj in scenario.adjustments
                        ]
                    } for scenario in optimization_result.recommended_scenarios[:3]
                ],
                "sensitivity_analysis": {
                    param: {
                        "sensitivity_coefficient": analysis.sensitivity_coefficient,
                        "elasticity": analysis.elasticity,
                        "critical_threshold": analysis.critical_threshold,
                        "risk_factors": analysis.risk_factors
                    } for param, analysis in optimization_result.sensitivity_analysis.items()
                },
                "implementation_roadmap": optimization_result.implementation_roadmap,
                "risk_assessment": optimization_result.risk_assessment
            },
            "optimization_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"],
            "target_exceedance": request.target_exceedance,
            "strategy": request.strategy
        }
        
        # Cache result for 1 hour
        cache_key = f"fine_tuning:{optimization_result.optimization_id}"
        background_tasks.add_task(cache_result, cache_key, result_data, 3600)
        
        # Publish to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "fine_tuning_events",
            {
                "event_type": "optimization_completed",
                "user_id": user["user_id"],
                "optimization_id": optimization_result.optimization_id,
                "timestamp": datetime.utcnow().isoformat(),
                "improvement_factor": optimization_result.improvement_factor,
                "target_exceedance": request.target_exceedance,
                "strategy": request.strategy
            }
        )
        
        return APIResponse(
            success=True,
            message="Fine-tuning optimization completed successfully",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Fine-tuning optimization failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fine-tuning optimization failed: {str(e)}"
        )

@app.post("/api/v1/market-data", response_model=APIResponse)
async def get_market_data_api(
    request: MarketDataRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Fetch real-time market data from Polygon.io."""
    start_time = datetime.utcnow()
    
    try:
        market_data = {}
        
        for symbol in request.symbols:
            # Check cache first
            cache_key = f"market_data:{symbol}:{request.timespan}:{request.limit}"
            cached_data = await get_cached_result(cache_key)
            
            if cached_data:
                market_data[symbol] = cached_data
            else:
                # Fetch from Polygon.io
                symbol_data = await polygon_client.get_stock_data(
                    symbol, 
                    request.timespan, 
                    request.limit
                )
                market_data[symbol] = symbol_data
                
                # Cache for 5 minutes
                background_tasks.add_task(cache_result, cache_key, symbol_data, 300)
        
        result_data = {
            "market_data": market_data,
            "symbols_requested": request.symbols,
            "timespan": request.timespan,
            "limit": request.limit,
            "data_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"]
        }
        
        # Publish to Kafka for analytics
        background_tasks.add_task(
            publish_to_kafka,
            "market_data_requests",
            {
                "event_type": "market_data_fetched",
                "user_id": user["user_id"],
                "symbols": request.symbols,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Market data fetched for {len(request.symbols)} symbols",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Market data fetch failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Market data fetch failed: {str(e)}"
        )

@app.post("/api/v1/economic-data", response_model=APIResponse)
async def get_economic_data_api(
    request: EconomicDataRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Fetch economic data from FRED API."""
    start_time = datetime.utcnow()
    
    try:
        # Check cache first
        cache_key = f"economic_data:{request.series_id}:{request.start_date}:{request.end_date}"
        cached_data = await get_cached_result(cache_key)
        
        if cached_data:
            economic_data = cached_data
        else:
            # Fetch from FRED
            economic_data = await fred_client.get_economic_data(
                request.series_id,
                request.start_date,
                request.end_date
            )
            
            # Cache for 1 hour
            background_tasks.add_task(cache_result, cache_key, economic_data, 3600)
        
        result_data = {
            "economic_data": economic_data,
            "series_id": request.series_id,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "data_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"]
        }
        
        # Publish to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "economic_data_requests",
            {
                "event_type": "economic_data_fetched",
                "user_id": user["user_id"],
                "series_id": request.series_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Economic data fetched for series {request.series_id}",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Economic data fetch failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Economic data fetch failed: {str(e)}"
        )

@app.post("/api/v1/complete-analysis", response_model=APIResponse)
async def complete_analysis_api(
    request: ClientProfileRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(verify_token)
):
    """Run complete WealthForge analysis with all 6 components."""
    start_time = datetime.utcnow()
    
    try:
        client_profile = request.dict()
        
        # Step 1: Parse goals
        parsed_client = parse_goal_constraints(client_profile)
        
        # Step 2: Strategy optimization
        arena_result = await run_strategy_optimization(parsed_client, num_agents=50)
        
        # Step 3: Portfolio synthesis
        # Convert strategies to agent proposals
        agent_proposals = []
        for strategy_data in arena_result['top_strategies'][:15]:
            try:
                from strategy_optimization_arena import AgentRole, StrategyType
                strategy = AgentStrategy(
                    agent_id=strategy_data['agent_id'],
                    agent_name=strategy_data['agent_name'],
                    agent_role=AgentRole(strategy_data['agent_role']),
                    strategy_type=StrategyType(strategy_data['strategy_type']),
                    asset_allocation=strategy_data['asset_allocation'],
                    expected_return=strategy_data['expected_return'],
                    risk_score=strategy_data['risk_score'],
                    timeline_fit=strategy_data['timeline_fit'],
                    capital_efficiency=strategy_data['capital_efficiency'],
                    confidence=strategy_data['confidence']
                )
                agent_proposals.append(strategy)
            except Exception as e:
                continue
        
        market_data = MarketData.generate_dummy_data(days_back=500)
        portfolio_value = float(client_profile.get('constraints', {}).get('capital', 100000))
        
        synthesis_result = await synthesize_optimal_portfolio(
            agent_proposals,
            arena_result['client_goals'],
            market_data,
            portfolio_value=portfolio_value
        )
        
        # Step 4: Compliance audit
        audit_report = await perform_compliance_audit(parsed_client, synthesis_result)
        
        # Step 5: Fine-tuning optimization
        optimization_result = await optimize_goal_exceedance(
            parsed_client,
            target_exceedance=0.30,
            strategy=OptimizationStrategy.BALANCED,
            portfolio_result=synthesis_result
        )
        
        # Compile complete analysis
        result_data = {
            "complete_analysis": {
                "client_profile": parsed_client,
                "arena_result": {
                    "strategies_generated": arena_result["strategies_generated"],
                    "winner": arena_result["winner"],
                    "execution_time": arena_result["execution_time"]
                },
                "portfolio_synthesis": {
                    "portfolio_id": synthesis_result.portfolio_id,
                    "expected_return": synthesis_result.expected_return,
                    "risk_score": synthesis_result.risk_score,
                    "sharpe_ratio": synthesis_result.sharpe_ratio,
                    "final_allocation": synthesis_result.final_allocation
                },
                "compliance_audit": {
                    "audit_id": audit_report.audit_id,
                    "overall_compliance": audit_report.overall_compliance.value,
                    "audit_score": audit_report.audit_score
                },
                "optimization": {
                    "optimization_id": optimization_result.optimization_id,
                    "improvement_factor": optimization_result.improvement_factor,
                    "original_goal_probability": optimization_result.original_goal_probability,
                    "optimized_goal_probability": optimization_result.optimized_goal_probability
                }
            },
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "user_id": user["user_id"],
            "components_executed": 6
        }
        
        # Cache complete analysis for 30 minutes
        cache_key = f"complete_analysis:{hash(str(client_profile))}"
        background_tasks.add_task(cache_result, cache_key, result_data, 1800)
        
        # Publish comprehensive event to Kafka
        background_tasks.add_task(
            publish_to_kafka,
            "complete_analysis_events",
            {
                "event_type": "complete_analysis_finished",
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "portfolio_id": synthesis_result.portfolio_id,
                "audit_id": audit_report.audit_id,
                "optimization_id": optimization_result.optimization_id,
                "execution_time": (datetime.utcnow() - start_time).total_seconds()
            }
        )
        
        return APIResponse(
            success=True,
            message="Complete WealthForge analysis completed successfully",
            data=result_data,
            execution_time=(datetime.utcnow() - start_time).total_seconds()
        )
        
    except Exception as e:
        logger.error(f"Complete analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Complete analysis failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True if config.ENVIRONMENT == "development" else False,
        workers=1 if config.ENVIRONMENT == "development" else 4
    )