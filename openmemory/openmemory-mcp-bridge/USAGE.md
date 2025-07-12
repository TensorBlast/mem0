# OpenMemory MCP Bridge Usage Guide

## Overview

The OpenMemory MCP Bridge (`openmemory-mcp-bridge`) is a direct replacement for `supergateway` that provides better reliability and OpenMemory-specific optimizations.

## Key Differences from Supergateway

| Feature | Supergateway | OpenMemory MCP Bridge |
|---------|--------------|----------------------|
| **Connection** | Uses intermediary proxy | Direct connection to OpenMemory |
| **Configuration** | Single SSE URL | Flexible: SSE URL or explicit parameters |
| **Error Handling** | Basic error messages | Detailed error messages and logging |
| **Installation** | Requires npm installation | Uses uvx (no installation needed) |
| **Maintenance** | Third-party dependency | Maintained by OpenMemory team |

## Migration from Supergateway

### Before (Supergateway):
```json
{
  "mcpServers": {
    "openmemory": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--sse",
        "http://localhost:8765/mcp/claude/sse/moot"
      ]
    }
  }
}
```

### After (OpenMemory MCP Bridge):
```json
{
  "mcpServers": {
    "openmemory": {
      "command": "uvx",
      "args": [
        "openmemory-mcp-bridge",
        "--sse",
        "http://localhost:8765/mcp/claude/sse/moot"
      ]
    }
  }
}
```

## Dynamic Client and User ID Support

The bridge supports dynamic client and user ID parameters as shown in the OpenMemory dashboard:

### URL-based (like supergateway):
```bash
uvx openmemory-mcp-bridge --sse http://localhost:8765/mcp/{client}/sse/{user_id}
```

### Explicit parameters (more flexible):
```bash
uvx openmemory-mcp-bridge --base-url http://localhost:8765 --client {client} --user-id {user_id}
```

### Mixed approach (URL with overrides):
```bash
uvx openmemory-mcp-bridge --sse http://localhost:8765/mcp/claude/sse/default --client cursor --user-id custom_user
```

## Examples

### Claude Desktop
```json
{
  "mcpServers": {
    "openmemory": {
      "command": "uvx",
      "args": [
        "openmemory-mcp-bridge",
        "--sse",
        "http://localhost:8765/mcp/claude/sse/moot"
      ]
    }
  }
}
```

### Cursor IDE
```json
{
  "mcpServers": {
    "openmemory": {
      "command": "uvx",
      "args": [
        "openmemory-mcp-bridge",
        "--sse",
        "http://localhost:8765/mcp/cursor/sse/moot"
      ]
    }
  }
}
```

### Multiple Users
```json
{
  "mcpServers": {
    "openmemory-alice": {
      "command": "uvx",
      "args": [
        "openmemory-mcp-bridge",
        "--base-url",
        "http://localhost:8765",
        "--client",
        "claude",
        "--user-id",
        "alice"
      ]
    },
    "openmemory-bob": {
      "command": "uvx",
      "args": [
        "openmemory-mcp-bridge",
        "--base-url",
        "http://localhost:8765",
        "--client",
        "claude",
        "--user-id",
        "bob"
      ]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **"Server disconnected" errors**: 
   - Ensure OpenMemory server is running on the correct port
   - Check that the URL format is correct: `/mcp/{client}/sse/{user_id}`

2. **uvx not found**:
   - Install uvx: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or use pip: `pip install uv`

3. **Connection refused**:
   - Verify OpenMemory server is running: `curl http://localhost:8765/health`
   - Check firewall settings

### Debugging

Enable verbose logging to see detailed connection information:

```bash
uvx openmemory-mcp-bridge --sse http://localhost:8765/mcp/claude/sse/moot --verbose
```

## Publishing to PyPI

To publish this package to PyPI:

1. Build the package:
   ```bash
   python -m build
   ```

2. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

3. Test installation:
   ```bash
   uvx openmemory-mcp-bridge --help
   ```

## Development

For local development:

```bash
# Install in development mode
pip install -e .

# Test the CLI
openmemory-mcp-bridge --help

# Run tests
pytest
``` 