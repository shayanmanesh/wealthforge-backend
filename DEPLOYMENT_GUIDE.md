# WealthForge FastAPI Deployment Guide

Complete deployment guide for the WealthForge AI-Powered Investment Platform with FastAPI, Kafka, and async operations.

## 🚀 Quick Start

### 1. Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd wealthforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp config.env.example .env
# Edit .env with your API keys
```

### 2. Start WealthForge API (Standalone)

```bash
# Start FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Access API
open http://localhost:8000
open http://localhost:8000/docs  # Interactive API docs
```

### 3. Full Production Setup with Docker

```bash
# Start complete stack
docker-compose up -d

# View logs
docker-compose logs -f

# Stop stack
docker-compose down
```

## 🐳 Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ disk space

### Services Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WealthForge Stack                        │
├─────────────────────────────────────────────────────────────┤
│  wealthforge-api:8000     │  Main FastAPI application       │
│  wealthforge-consumer     │  Kafka message consumer         │
│  redis:6379              │  Cache & session storage        │
│  kafka:9092              │  Message broker                 │
│  zookeeper:2181          │  Kafka coordination            │
│  kafka-ui:8080           │  Kafka monitoring              │
│  redis-commander:8081    │  Redis monitoring              │
│  prometheus:9090         │  Metrics collection            │
│  grafana:3000            │  Visualization dashboards      │
└─────────────────────────────────────────────────────────────┘
```

### Docker Services

#### Core Services
- **wealthforge-api**: Main FastAPI application with all 6 WealthForge components
- **wealthforge-consumer**: Kafka consumer for async message processing
- **redis**: High-performance caching and session storage
- **kafka**: Message broker for async operations
- **zookeeper**: Kafka cluster coordination

#### Monitoring Services  
- **kafka-ui**: Web interface for Kafka monitoring
- **redis-commander**: Redis data browser and management
- **prometheus**: Metrics collection and storage
- **grafana**: Visualization dashboards and alerting

### Environment Configuration

Create `.env` file from `config.env.example`:

```bash
# Environment
ENVIRONMENT=development

# API Keys
POLYGON_API_KEY=your_polygon_api_key_here
FRED_API_KEY=your_fred_api_key_here

# Infrastructure
REDIS_URL=redis://redis:6379
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Security
SECRET_KEY=your-super-secret-key-here

# Performance
MAX_AGENTS=100
DEFAULT_AGENTS=50
```

### Production Deployment

```bash
# Production stack
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale API instances
docker-compose up --scale wealthforge-api=3 -d

# Health checks
curl http://localhost:8000/health

# View metrics
open http://localhost:9090  # Prometheus
open http://localhost:3000  # Grafana (admin/wealthforge123)
```

## ⚙️ Configuration

### FastAPI Application Settings

```python
# app.py configuration
class Config:
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "YOUR_POLYGON_API_KEY_HERE")
    FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-in-production")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
```

### Kafka Topics

Automatically created topics for async operations:
- `goal_parsing_events`
- `strategy_optimization_events`
- `portfolio_synthesis_events`
- `compliance_audit_events`
- `fine_tuning_events`
- `market_data_requests`
- `economic_data_requests`
- `complete_analysis_events`

### Redis Cache Configuration

Cache TTL settings:
- Market data: 5 minutes
- Economic data: 1 hour
- Analysis results: 30 minutes
- User sessions: 24 hours

## 🔌 API Integration

### Authentication

```bash
# Set authorization header
export API_TOKEN="your-api-token"

# Example request
curl -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8000/api/v1/parse-goals \
     -d '{
       "goals": {
         "strategy": "aggressive growth",
         "timeline": "15 years",
         "target_amount": 1000000
       },
       "constraints": {
         "capital": 200000,
         "contributions": 3000
       }
     }'
```

### Complete Analysis Workflow

```bash
# 1. Parse client goals
PARSE_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/parse-goals \
  -d @client_profile.json)

# 2. Run strategy optimization
STRATEGY_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/strategy-optimization \
  -d @strategy_request.json)

# 3. Portfolio synthesis
PORTFOLIO_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/portfolio-synthesis \
  -d @portfolio_request.json)

# 4. Compliance audit
AUDIT_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/compliance-audit \
  -d @audit_request.json)

# 5. Fine-tuning optimization
TUNING_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/fine-tuning \
  -d @tuning_request.json)

# Or run complete analysis in one call
COMPLETE_RESPONSE=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8000/api/v1/complete-analysis \
  -d @client_profile.json)
```

## 📊 Monitoring & Observability

### Health Monitoring

```bash
# API health check
curl http://localhost:8000/health

# Response
{
  "success": true,
  "message": "Health check completed",
  "data": {
    "api": "healthy",
    "redis": "connected",
    "kafka": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Performance Metrics

Access monitoring dashboards:
- **API Metrics**: http://localhost:8000/metrics (if enabled)
- **Kafka UI**: http://localhost:8080
- **Redis Commander**: http://localhost:8081
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Logging

```bash
# View API logs
docker-compose logs -f wealthforge-api

# View consumer logs  
docker-compose logs -f wealthforge-consumer

# View all logs
docker-compose logs -f
```

### Key Metrics to Monitor

#### API Performance
- Request latency (p50, p95, p99)
- Throughput (requests/second)
- Error rates by endpoint
- Cache hit/miss ratios

#### Component Performance
- Goal parsing time
- Strategy optimization time (50 agents)
- Portfolio synthesis time
- Compliance audit time
- Fine-tuning optimization time

#### Infrastructure Metrics
- Redis memory usage
- Kafka message throughput
- Docker container resource usage
- External API rate limits

## 🔐 Security

### Production Security Checklist

```bash
# 1. Change default passwords
SECRET_KEY=generate-strong-secret-key
GRAFANA_ADMIN_PASSWORD=change-default-password

# 2. Configure CORS for production
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# 3. Enable HTTPS
# Use reverse proxy (nginx/traefik) with SSL certificates

# 4. Secure Redis
# Enable authentication and encryption in transit

# 5. Secure Kafka
# Configure SASL/SSL authentication

# 6. API rate limiting
# Implement rate limiting per user/IP

# 7. Input validation
# Already implemented with Pydantic models
```

### Network Security

```yaml
# docker-compose.prod.yml additions
services:
  wealthforge-api:
    networks:
      - internal
      - external
    
  redis:
    networks:
      - internal
    # Remove port exposure for production
    
  kafka:
    networks:
      - internal
    # Remove port exposure for production

networks:
  internal:
    driver: bridge
    internal: true
  external:
    driver: bridge
```

## 🚀 Scaling & Performance

### Horizontal Scaling

```bash
# Scale API instances
docker-compose up --scale wealthforge-api=5 -d

# Load balancer configuration (nginx example)
upstream wealthforge_api {
    server wealthforge-api-1:8000;
    server wealthforge-api-2:8000;
    server wealthforge-api-3:8000;
}
```

### Performance Optimization

#### Redis Optimization
```bash
# Increase Redis memory
redis:
  image: redis:7-alpine
  command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
```

#### Kafka Optimization
```bash
# Increase Kafka partitions for better parallelism
KAFKA_NUM_PARTITIONS=6
KAFKA_DEFAULT_REPLICATION_FACTOR=3
```

#### FastAPI Optimization
```python
# app.py - production settings
if config.ENVIRONMENT == "production":
    app = FastAPI(
        title="WealthForge API",
        docs_url=None,  # Disable docs in production
        redoc_url=None,
        openapi_url=None
    )
```

### Load Testing

```bash
# Install load testing tools
pip install locust

# Run load tests
locust -f load_tests.py --host=http://localhost:8000
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Redis Connection Failed
```bash
# Check Redis status
docker-compose ps redis

# View Redis logs
docker-compose logs redis

# Fix: Restart Redis
docker-compose restart redis
```

#### 2. Kafka Connection Issues
```bash
# Check Kafka status
docker-compose ps kafka zookeeper

# View Kafka logs
docker-compose logs kafka

# Fix: Restart Kafka stack
docker-compose restart zookeeper kafka
```

#### 3. API Performance Issues
```bash
# Check API logs
docker-compose logs wealthforge-api | grep ERROR

# Monitor resource usage
docker stats

# Check cache performance
redis-cli info stats
```

#### 4. Memory Issues
```bash
# Increase Docker memory limits
# Edit docker-compose.yml:
services:
  wealthforge-api:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
```

## 🔧 Development

### Local Development Workflow

```bash
# 1. Start supporting services only
docker-compose up redis kafka zookeeper -d

# 2. Run API locally for development
source venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 3. Run consumer locally
python kafka_consumer.py

# 4. Run tests
python -m pytest tests/
```

### Adding New Features

1. **New API Endpoint**:
   - Add Pydantic models
   - Implement endpoint function
   - Add Kafka event publishing
   - Update documentation

2. **New Kafka Consumer**:
   - Add topic handler in `kafka_consumer.py`
   - Update topic list in docker-compose.yml
   - Add metrics collection

3. **New External API**:
   - Create client class
   - Add configuration
   - Implement caching
   - Add error handling

## 📋 Production Checklist

### Pre-deployment
- [ ] Set production environment variables
- [ ] Configure external API keys
- [ ] Set up SSL certificates
- [ ] Configure monitoring
- [ ] Set up log aggregation
- [ ] Configure backups
- [ ] Security review

### Post-deployment
- [ ] Verify health checks
- [ ] Monitor performance metrics
- [ ] Check log outputs
- [ ] Validate external API connections
- [ ] Test critical user flows
- [ ] Set up alerting
- [ ] Document runbooks

## 🌟 Success Metrics

### API Performance Targets
- **Response time**: < 2s for complete analysis
- **Availability**: > 99.9% uptime
- **Throughput**: 100+ concurrent users
- **Cache hit rate**: > 80%

### Business Metrics
- **Goal achievement improvement**: 5-50x better outcomes
- **Analysis accuracy**: > 95% client satisfaction
- **Compliance score**: > 90% average
- **Time to insights**: < 30 seconds

---

## 🎉 WealthForge: Production-Ready Investment Platform

The WealthForge FastAPI deployment provides:
- **Enterprise-grade architecture** with async operations
- **Scalable infrastructure** with Docker containers
- **Real-time data integration** from Polygon.io and FRED
- **Comprehensive monitoring** with metrics and dashboards
- **Production security** with authentication and validation
- **High performance** with caching and optimization

Ready for institutional deployment with comprehensive documentation, monitoring, and support infrastructure.