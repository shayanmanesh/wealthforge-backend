#!/bin/bash

# WealthForge Backend Startup Script

echo "🚀 Starting WealthForge Backend..."

# Set environment variables if not already set
export ENVIRONMENT=${ENVIRONMENT:-production}
export PORT=${PORT:-8000}

# Log environment info
echo "Environment: $ENVIRONMENT"
echo "Port: $PORT"

# Test imports first
echo "🧪 Testing app imports..."
python3 -c "import app; print('✅ App imports successful')" || {
    echo "❌ App import failed. Check dependencies."
    exit 1
}

# Start the application
if [ "$ENVIRONMENT" = "development" ]; then
    echo "🔧 Starting in development mode..."
    python3 app.py
else
    echo "🚀 Starting in production mode..."
    gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1 --timeout 120
fi