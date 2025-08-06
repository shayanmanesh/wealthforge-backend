# WealthForge Backend - Deployment Troubleshooting Guide

## Issues Fixed ✅

### 1. **CRITICAL**: Missing Dependencies (Latest Fix)
- **Problem**: `ModuleNotFoundError: No module named 'kafka'` causing deployment failure
- **Fix**: Added `kafka-python`, `pandas`, `scipy`, and `httpx` to `requirements.txt`
- **Details**: App was importing these modules but they weren't in dependencies

### 2. Port Configuration
- **Problem**: App was hardcoded to port 8000, but Render needs to use `$PORT` environment variable
- **Fix**: Modified `app.py` to read port from environment variable

### 3. CORS Configuration
- **Problem**: Production CORS was only allowing one domain
- **Fix**: Added support for Vercel deployment domains

### 4. Health Check Robustness
- **Problem**: Simple health check might not catch all issues
- **Fix**: Enhanced health check with proper error handling and Redis connectivity testing

### 5. Environment Configuration Logging
- **Problem**: No visibility into configuration issues during startup
- **Fix**: Added configuration logging for debugging

### 6. Import Error Handling
- **Problem**: Kafka imports were failing at module level
- **Fix**: Improved import handling with dynamic initialization

## Deployment Files Created/Modified

1. **`render.yaml`** - Updated with better configuration
2. **`Procfile`** - Alternative deployment configuration
3. **`start.sh`** - Startup script for better control
4. **`app.py`** - Enhanced with production-ready features

## Next Steps

### 1. Environment Variables to Set in Render

**Required for basic functionality:**
- `ENVIRONMENT=production`
- `SECRET_KEY` (auto-generated in render.yaml)

**Optional but recommended:**
- `OPENAI_API_KEY` - For AI functionality
- `POLYGON_API_KEY` - For real-time market data
- `FRED_API_KEY` - For economic data

**Infrastructure (if available):**
- `REDIS_URL` - For caching
- `KAFKA_BOOTSTRAP_SERVERS` - For message queuing

### 2. Alternative Start Commands

If the startup script doesn't work, try these in render.yaml:

```yaml
# Option 1: Direct gunicorn (current)
startCommand: ./start.sh

# Option 2: Direct gunicorn command
startCommand: gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1 --timeout 120

# Option 3: Python direct
startCommand: python app.py
```

### 3. Debugging Steps

1. **Check Render logs** for startup errors
2. **Test health endpoint**: `https://your-app.onrender.com/health`
3. **Check environment variables** in Render dashboard
4. **Monitor startup logs** for configuration messages

### 4. Common Issues & Solutions

**Issue: "Module not found" errors**
- Solution: Check `requirements.txt` is complete
- Check: Verify Python version compatibility

**Issue: "Port already in use"**
- Solution: Ensure only one worker in production
- Check: `--workers 1` flag is set

**Issue: "Health check failed"**
- Solution: Check `/health` endpoint manually
- Check: Verify all external services are optional

**Issue: "CORS errors from frontend"**
- Solution: Update CORS origins in `app.py`
- Check: Add your frontend domain to allowed origins

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=development
export PORT=8000

# Run the application
python app.py
```

## Monitoring

- Health endpoint: `/health`
- API docs: `/docs`
- Alternative docs: `/redoc`

The application is designed to be resilient and start even if Redis/Kafka are not available.