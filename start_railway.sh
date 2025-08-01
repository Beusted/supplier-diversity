#!/bin/bash

echo "🚂 Railway Startup Script"
echo "📍 PORT environment variable: $PORT"

# Set default port if PORT is not set
if [ -z "$PORT" ]; then
    PORT=8080
    echo "⚠️  PORT not set, using default: $PORT"
fi

echo "🚀 Starting Streamlit on port $PORT"
echo "📄 Using: frontend/main_dashboard.py (modern UI)"

# Start the modern dashboard UI
exec streamlit run frontend/main_dashboard.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false
