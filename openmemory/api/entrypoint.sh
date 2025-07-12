#!/bin/bash

set -e

echo "🚀 Starting OpenMemory MCP Server..."

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 3

# Run auto-configuration if enabled
if [ "$AUTO_CONFIGURE" = "true" ]; then
    echo "🔧 Running auto-configuration..."
    python auto_configure.py
fi

# Start the main application
echo "🚀 Starting the OpenMemory API server..."
exec uvicorn main:app --host 0.0.0.0 --port 8765 