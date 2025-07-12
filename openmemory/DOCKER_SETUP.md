# OpenMemory Docker Setup

This guide explains how to set up OpenMemory using Docker with automatic provider detection.

## Quick Start

OpenMemory now supports automatic configuration based on the API key you provide. You can use either OpenAI or Mistral as your provider.

### Option 1: Using OpenAI (Default)

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | OPENAI_API_KEY=your_openai_api_key bash
```

### Option 2: Using Mistral

```bash
curl -sL https://raw.githubusercontent.com/mem0ai/mem0/main/openmemory/run.sh | MISTRAL_API_KEY=your_mistral_api_key bash
```

## How It Works

The system automatically detects which provider to use based on the API key you provide and **builds the Docker images locally** to include the latest Mistral support:

1. **If `MISTRAL_API_KEY` is provided**: 
   - Uses Mistral as both LLM and embedder provider
   - LLM Model: `mistral-small-latest`
   - Embedder Model: `mistral-embed`

2. **If `OPENAI_API_KEY` is provided**: 
   - Uses OpenAI as both LLM and embedder provider
   - LLM Model: `gpt-4o-mini`
   - Embedder Model: `text-embedding-3-small`

**Note**: The setup script builds the Docker images locally from source code to ensure you have the latest Mistral integration. This means the first run will take longer as it builds the images, but subsequent runs will be faster.

## Environment Variables

The setup script supports the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MISTRAL_API_KEY`: Your Mistral API key
- `USER`: Your username (defaults to current user)
- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to `http://localhost:8765`)

## Configuration Files

The system automatically creates configuration files based on your provider:

### Mistral Configuration
```json
{
  "mem0": {
    "llm": {
      "provider": "mistral",
      "config": {
        "model": "mistral-small-latest",
        "temperature": 0.1,
        "max_tokens": 2000,
        "api_key": "env:MISTRAL_API_KEY"
      }
    },
    "embedder": {
      "provider": "mistral",
      "config": {
        "model": "mistral-embed",
        "api_key": "env:MISTRAL_API_KEY"
      }
    }
  }
}
```

### OpenAI Configuration
```json
{
  "mem0": {
    "llm": {
      "provider": "openai",
      "config": {
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "max_tokens": 2000,
        "api_key": "env:OPENAI_API_KEY"
      }
    },
    "embedder": {
      "provider": "openai",
      "config": {
        "model": "text-embedding-3-small",
        "api_key": "env:OPENAI_API_KEY"
      }
    }
  }
}
```

## Manual Setup

If you prefer to set up manually:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mem0ai/mem0.git
   cd mem0/openmemory
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   # OR
   export MISTRAL_API_KEY=your_mistral_api_key
   ```

3. **Run the setup script**:
   ```bash
   ./run.sh
   ```

## Troubleshooting

### Common Issues

1. **No API key provided**:
   ```
   ❌ No API key provided. Please set either OPENAI_API_KEY or MISTRAL_API_KEY.
   ```
   **Solution**: Provide either `OPENAI_API_KEY` or `MISTRAL_API_KEY`.

2. **Docker not found**:
   ```
   ❌ Docker not found. Please install Docker first.
   ```
   **Solution**: Install Docker from [docker.com](https://www.docker.com/get-started).

3. **Port already in use**:
   The script automatically finds available ports between 3000-3010 for the frontend.

### Checking Configuration

Once the system is running, you can check the configuration by:

1. Opening the frontend (usually `http://localhost:3000`)
2. Going to Settings/Configuration
3. Viewing the current provider settings

## API Keys

### Getting API Keys

- **OpenAI**: Get your API key from [platform.openai.com](https://platform.openai.com/api-keys)
- **Mistral**: Get your API key from [platform.mistral.ai](https://platform.mistral.ai/)

### Security

- API keys are stored as environment variables
- They are not logged or displayed in plain text
- The system uses environment variable references (`env:API_KEY_NAME`) in configuration files

## Services

The Docker setup includes:

1. **Qdrant Vector Database** (`mem0_store`): Stores memory embeddings
2. **OpenMemory API** (`openmemory-mcp`): Backend API server
3. **OpenMemory UI** (`mem0_ui`): Frontend web interface

## Default Ports

- **Backend API**: 8765
- **Frontend UI**: 3000-3010 (automatically detected)
- **Qdrant**: 6333 (internal)

## Logs

To view logs:

```bash
# View all services
docker compose logs -f

# View specific service
docker compose logs -f openmemory-mcp
docker logs -f mem0_ui
```

## Building Process

The setup script now builds images locally to include Mistral support:

### Backend Build Process:
1. **Builds mem0 package** with Mistral LLM and embedder implementations
2. **Installs dependencies** including system packages for compilation
3. **Includes auto-configuration** script for provider detection
4. **Sets up environment** for both OpenAI and Mistral API keys

### Frontend Build Process:
1. **Builds UI locally** with Mistral provider options
2. **Includes updated form components** for Mistral configuration
3. **Maintains compatibility** with existing OpenAI setups

### Build Time:
- **First run**: ~5-10 minutes (building images)
- **Subsequent runs**: ~30 seconds (using cached images)

## Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove frontend
docker stop mem0_ui
docker rm mem0_ui
```

## Updating

To update to the latest version:

```bash
# Pull latest images
docker compose pull
docker pull mem0/openmemory-ui:latest

# Restart services
docker compose down
docker compose up -d
docker stop mem0_ui
docker rm mem0_ui

# Restart frontend
docker run -d --name mem0_ui -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8765" \
  -e NEXT_PUBLIC_USER_ID="$USER" \
  mem0/openmemory-ui:latest
``` 