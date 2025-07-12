# Using Mistral with OpenMemory

This guide explains how to configure OpenMemory to use Mistral as your LLM and/or embedder provider.

## Prerequisites

1. **Mistral API Key**: You need a Mistral API key from [platform.mistral.ai](https://platform.mistral.ai/)
2. **OpenMemory**: A running OpenMemory instance

## Setup Options

### Option 1: Environment Variable (Recommended)

Set your Mistral API key as an environment variable:

```bash
export MISTRAL_API_KEY=your-mistral-api-key-here
```

### Option 2: Direct Configuration

You can also configure the API key directly in the UI or configuration files.

## Configuration

### Using the Web UI

1. Open your OpenMemory dashboard (default: http://localhost:3000)
2. Go to Settings/Configuration
3. **For LLM Configuration:**
   - Select "Mistral" as the LLM Provider
   - Set Model to "mistral-small-latest" (or other Mistral models)
   - API Key: Use "env:MISTRAL_API_KEY" (if using environment variable) or enter your key directly

4. **For Embedder Configuration:**
   - Select "Mistral" as the Embedder Provider  
   - Set Model to "mistral-embed"
   - API Key: Use "env:MISTRAL_API_KEY" (if using environment variable) or enter your key directly

5. Save the configuration

### Using Configuration Files

You can also configure Mistral by editing the configuration directly. Here's an example configuration:

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

## Available Models

### LLM Models
- `mistral-small-latest` - Latest small model (recommended for most use cases)
- `mistral-medium-latest` - Medium-sized model for more complex tasks
- `mistral-large-latest` - Largest model for most demanding tasks
- `open-mistral-7b` - Open source 7B parameter model
- `open-mixtral-8x7b` - Open source mixture of experts model

### Embedding Models
- `mistral-embed` - Mistral's embedding model (1024 dimensions)

## Example Docker Setup

If you're running OpenMemory with Docker, you can pass the Mistral API key as an environment variable:

```bash
docker run -d \
  --name openmemory \
  -p 8765:8765 \
  -e MISTRAL_API_KEY=your-mistral-api-key-here \
  mem0/openmemory-mcp:latest
```

## Testing the Configuration

After setting up Mistral, you can test it by:

1. Adding a memory through the UI or API
2. Searching for memories to verify the embeddings work
3. Checking the logs to ensure there are no API key errors

## Troubleshooting

### Common Issues

1. **"Mistral API key is required" Error**
   - Ensure your `MISTRAL_API_KEY` environment variable is set
   - Or ensure you've entered the API key directly in the configuration

2. **"Unsupported model" Error**
   - Verify you're using a valid Mistral model name
   - Check the available models list above

3. **Rate Limiting**
   - Mistral has rate limits based on your plan
   - Consider upgrading your Mistral plan if you hit limits frequently

4. **Connection Issues**
   - Ensure your server has internet access to reach api.mistral.ai
   - Check firewall settings if running in a restricted environment

## Benefits of Using Mistral

- **High Quality**: Mistral models provide excellent performance for various tasks
- **Efficiency**: Good balance of performance and speed
- **Cost-Effective**: Competitive pricing compared to other providers
- **European Provider**: Data processed in Europe (good for GDPR compliance)
- **Open Models**: Some models are open source and can be self-hosted

## Mixed Provider Setup

You can also use Mistral for only LLM or only embeddings while using another provider for the other component:

```json
{
  "mem0": {
    "llm": {
      "provider": "mistral",
      "config": {
        "model": "mistral-small-latest",
        "api_key": "env:MISTRAL_API_KEY"
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

This allows you to leverage the best of both providers based on your specific needs. 