#!/bin/bash

set -e

echo "🚀 Starting OpenMemory installation..."

# Set environment variables
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
MISTRAL_API_KEY="${MISTRAL_API_KEY:-}"
USER="${USER:-$(whoami)}"
NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8765}"

# Check if at least one API key is provided
if [ -z "$OPENAI_API_KEY" ] && [ -z "$MISTRAL_API_KEY" ]; then
  echo "❌ No API key provided. Please set either OPENAI_API_KEY or MISTRAL_API_KEY."
  echo "For OpenAI: curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | OPENAI_API_KEY=your_api_key bash"
  echo "For Mistral: curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | MISTRAL_API_KEY=your_api_key bash"
  echo "You can also set them as global environment variables:"
  echo "  export OPENAI_API_KEY=your_api_key"
  echo "  export MISTRAL_API_KEY=your_api_key"
  exit 1
fi

# Determine which provider to use
if [ -n "$MISTRAL_API_KEY" ]; then
  echo "🔧 Using Mistral as the LLM and embedder provider"
  PROVIDER="mistral"
  API_KEY_VAR="MISTRAL_API_KEY"
  API_KEY_VALUE="$MISTRAL_API_KEY"
elif [ -n "$OPENAI_API_KEY" ]; then
  echo "🔧 Using OpenAI as the LLM and embedder provider"
  PROVIDER="openai"
  API_KEY_VAR="OPENAI_API_KEY"
  API_KEY_VALUE="$OPENAI_API_KEY"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "❌ Docker not found. Please install Docker first."
  exit 1
fi

# Check if docker compose is available
if ! docker compose version &> /dev/null; then
  echo "❌ Docker Compose not found. Please install Docker Compose V2."
  exit 1
fi

# Check if the container "mem0_ui" already exists and remove it if necessary
if [ $(docker ps -aq -f name=mem0_ui) ]; then
  echo "⚠️ Found existing container 'mem0_ui'. Removing it..."
  docker rm -f mem0_ui
fi

# Find an available port starting from 3000
echo "🔍 Looking for available port for frontend..."
for port in {3000..3010}; do
  if ! lsof -i:$port >/dev/null 2>&1; then
    FRONTEND_PORT=$port
    break
  fi
done

if [ -z "$FRONTEND_PORT" ]; then
  echo "❌ Could not find an available port between 3000 and 3010"
  exit 1
fi

# Export required variables for Compose and frontend
export OPENAI_API_KEY
export MISTRAL_API_KEY
export USER
export NEXT_PUBLIC_API_URL
export NEXT_PUBLIC_USER_ID="$USER"
export FRONTEND_PORT
export PROVIDER
export API_KEY_VAR
export API_KEY_VALUE

# Create docker-compose.yml file
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml <<EOF
services:
  mem0_store:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - mem0_storage:/mem0/storage
  openmemory-mcp:
    build: 
      context: .
      dockerfile: api/Dockerfile
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - USER=${USER}
      - QDRANT_HOST=mem0_store
      - QDRANT_PORT=6333
      - PROVIDER=${PROVIDER}
      - AUTO_CONFIGURE=true
    depends_on:
      - mem0_store
    ports:
      - "8765:8765"

volumes:
  mem0_storage:
EOF

# Build and start services
echo "🚀 Building and starting backend services with Mistral support..."
docker compose up -d --build

# Build and start the frontend
echo "🚀 Building and starting frontend on port $FRONTEND_PORT..."
docker build -t openmemory-ui:local -f ui/Dockerfile ui/
docker run -d \
  --name mem0_ui \
  -p ${FRONTEND_PORT}:3000 \
  -e NEXT_PUBLIC_API_URL="$NEXT_PUBLIC_API_URL" \
  -e NEXT_PUBLIC_USER_ID="$USER" \
  openmemory-ui:local

echo "✅ Backend:  http://localhost:8765"
echo "✅ Frontend: http://localhost:$FRONTEND_PORT"
echo "🔧 Provider: $PROVIDER"
echo "🔑 API Key:  $API_KEY_VAR (configured)"
echo "🏗️  Built locally with Mistral support"

if [ "$PROVIDER" = "mistral" ]; then
    echo "📝 Note: Using Mistral AI with models:"
    echo "   - LLM: mistral-small-latest"
    echo "   - Embedder: mistral-embed"
elif [ "$PROVIDER" = "openai" ]; then
    echo "📝 Note: Using OpenAI with models:"
    echo "   - LLM: gpt-4o-mini"
    echo "   - Embedder: text-embedding-3-small"
fi

# Open the frontend URL in the default web browser
echo "🌐 Opening frontend in the default browser..."
URL="http://localhost:$FRONTEND_PORT"

if command -v xdg-open > /dev/null; then
  xdg-open "$URL"        # Linux
elif command -v open > /dev/null; then
  open "$URL"            # macOS
elif command -v start > /dev/null; then
  start "$URL"           # Windows (if run via Git Bash or similar)
else
  echo "⚠️ Could not detect a method to open the browser. Please open $URL manually."
fi
