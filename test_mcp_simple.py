#!/usr/bin/env python3

import json
import sys
import os

# Add the bridge to Python path
sys.path.insert(0, 'openmemory/openmemory-mcp-bridge/src')

from openmemory_mcp_bridge.main import OpenMemoryMCPBridge
import asyncio

async def test_bridge():
    """Test the MCP bridge directly"""
    
    # Initialize bridge
    bridge = OpenMemoryMCPBridge(
        base_url="http://localhost:8765",
        client="test_client",
        user_id="moot"
    )
    
    try:
        print("🚀 Testing OpenMemory MCP Bridge with Mistral")
        print("=" * 50)
        
        # Test adding memories
        print("\n💾 Testing: Add Memories")
        add_result = await bridge._add_memories({
            "memories": [
                "I love Italian food, especially pasta and pizza",
                "My favorite programming language is Python", 
                "I work as a software engineer at a tech startup"
            ]
        })
        print(f"✅ Add Result: {json.dumps(add_result, indent=2)}")
        
        # Wait for processing
        await asyncio.sleep(3)
        
        # Test getting memories  
        print("\n🔍 Testing: Get Memories")
        get_result = await bridge._get_memories({
            "page": 1,
            "size": 10
        })
        print(f"✅ Get Result: {json.dumps(get_result, indent=2)}")
        
        # Test getting configuration
        print("\n🔧 Testing: Get Configuration")
        config_result = await bridge._get_configuration({})
        print(f"✅ Config Result: {json.dumps(config_result, indent=2)}")
        
        print("\n🎉 All MCP Bridge tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bridge.close()

if __name__ == "__main__":
    asyncio.run(test_bridge()) 