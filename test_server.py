#!/usr/bin/env python3
"""
Simple script to test the Confluence MCP server locally.
This demonstrates how to create an MCP client and test the server tools.
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()


async def test_confluence_server():
    """Test the Confluence MCP server"""
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["confluence_server.py"]
    )
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize connection
                await session.initialize()
                
                print("Connected to Confluence MCP Server!")
                print("Available tools:")
                
                # List available tools
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                print("\\n" + "="*60)
                
                # Test get_confluence_info
                print("\\nTesting get_confluence_info()...")
                result = await session.call_tool("get_confluence_info", {})
                print(f"Result: {result.content[0].text if result.content else 'No content'}")
                
                print("\\n" + "="*60)
                
                # Test list_spaces
                print("\\nTesting list_spaces()...")
                result = await session.call_tool("list_spaces", {"limit": 5})
                print(f"Result: {result.content[0].text if result.content else 'No content'}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_confluence_server())
