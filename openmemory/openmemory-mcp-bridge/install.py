#!/usr/bin/env python3
"""
OpenMemory MCP Bridge Install Script

This script installs the OpenMemory MCP Bridge package and configures it for use with MCP clients.
"""

import sys
import subprocess
import json
import os
import platform
from pathlib import Path
from urllib.parse import urlparse

def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_uvx():
    """Check if uvx is available"""
    print("Checking for uvx...")
    
    # Check if uvx is available
    success, stdout, stderr = run_command("uvx --version")
    
    if success:
        print("✓ uvx is available!")
        return True
    else:
        print("✗ uvx is not available. Please install uvx first:")
        print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

def configure_claude_desktop(base_url, client, user_id):
    """Configure Claude Desktop to use the OpenMemory MCP Bridge"""
    
    # Determine the config file path based on the platform
    if platform.system() == "Darwin":  # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif platform.system() == "Windows":
        config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        config_path = Path.home() / ".config" / "claude" / "claude_desktop_config.json"
    
    # Create the config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing config or create new one
    config = {"mcpServers": {}}
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse existing config file {config_path}")
    
    # Add the OpenMemory MCP Bridge configuration
    config["mcpServers"]["openmemory"] = {
        "command": "uvx",
        "args": [
            "openmemory-mcp-bridge",
            "--sse",
            f"{base_url}/mcp/{client}/sse/{user_id}"
        ]
    }
    
    # Write the config file
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Claude Desktop configured! Config file: {config_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to configure Claude Desktop: {e}")
        return False

def main():
    """Main install function"""
    print("OpenMemory MCP Bridge Installer")
    print("=" * 40)
    
    # Get configuration from command line or use defaults
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765"
    client = sys.argv[2] if len(sys.argv) > 2 else "claude"
    user_id = sys.argv[3] if len(sys.argv) > 3 else "default"
    
    print(f"Base URL: {base_url}")
    print(f"Client: {client}")
    print(f"User ID: {user_id}")
    print()
    
    # Check uvx availability
    if not check_uvx():
        sys.exit(1)
    
    # Configure Claude Desktop
    if not configure_claude_desktop(base_url, client, user_id):
        sys.exit(1)
    
    print()
    print("🎉 Configuration complete!")
    print()
    print("Next steps:")
    print("1. Restart Claude Desktop")
    print("2. You should now see OpenMemory tools available in Claude Desktop")
    print("3. Test by asking Claude to remember something about you")
    print()
    print("For other MCP clients, use this configuration:")
    print(f'  Command: uvx')
    print(f'  Args: openmemory-mcp-bridge --sse {base_url}/mcp/{client}/sse/{user_id}')

if __name__ == "__main__":
    main() 