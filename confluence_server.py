#!/usr/bin/env python3
"""
MCP Server for Confluence
This server exposes tools to interact with Confluence spaces and pages.
"""

import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv
from atlassian import Confluence
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize logging (to stderr to avoid interfering with stdio-based MCP)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Confluence", instructions="Connect to Confluence to manage spaces and pages")

# Confluence client (lazy initialized)
confluence_client: Optional[Confluence] = None


def get_confluence_client() -> Confluence:
    """Get or create Confluence client"""
    global confluence_client
    
    if confluence_client is None:
        # Get credentials from environment
        url = os.getenv('CONFLUENCE_URL')
        username = os.getenv('CONFLUENCE_USERNAME')
        password = os.getenv('CONFLUENCE_PASSWORD')
        token = os.getenv('CONFLUENCE_TOKEN')
        
        if not url:
            raise ValueError("CONFLUENCE_URL environment variable is required")
        
        # Initialize client
        if token:
            # Cloud-based Confluence with API token
            confluence_client = Confluence(
                url=url,
                username=username,
                password=token,
                cloud=True
            )
        elif username and password:
            # Server or Data Center Confluence
            confluence_client = Confluence(
                url=url,
                username=username,
                password=password
            )
        else:
            raise ValueError("Either CONFLUENCE_TOKEN or both CONFLUENCE_USERNAME and CONFLUENCE_PASSWORD are required")
        
        logger.info(f"Connected to Confluence at {url}")
    
    return confluence_client


@mcp.tool(description="List all spaces in Confluence")
def list_spaces(limit: int = 25) -> str:
    """List all spaces in the Confluence instance"""
    try:
        client = get_confluence_client()
        spaces_data = client.get_all_spaces(start=0, limit=limit)
        
        # get_all_spaces returns a dict with 'results' key
        spaces = spaces_data.get('results', []) if isinstance(spaces_data, dict) else spaces_data
        
        if not spaces:
            return "No spaces found"
        
        result = "Available Confluence Spaces:\\n\\n"
        for space in spaces:
            space_key = space.get('key', 'N/A')
            space_name = space.get('name', 'N/A')
            space_type = space.get('type', 'N/A')
            result += f"- **{space_name}** (Key: {space_key}, Type: {space_type})\\n"
        
        return result
    except Exception as e:
        return f"Error listing spaces: {str(e)}"


@mcp.tool(description="Get details about a specific Confluence space")
def get_space_details(space_key: str) -> str:
    """Get detailed information about a space"""
    try:
        client = get_confluence_client()
        space = client.get_space(space_key)
        
        result = f"**Space: {space.get('name')}**\\n\\n"
        result += f"Key: {space.get('key')}\\n"
        result += f"Type: {space.get('type')}\\n"
        
        if 'description' in space and space['description']:
            result += f"Description: {space['description'].get('plain', {}).get('value', 'N/A')}\\n"
        
        return result
    except Exception as e:
        return f"Error getting space details: {str(e)}"


@mcp.tool(description="List pages in a space")
def list_pages(space_key: str, limit: int = 10) -> str:
    """List pages in a specific space"""
    try:
        client = get_confluence_client()
        pages_data = client.get_all_pages_from_space(space_key, start=0, limit=limit)
        
        # Handle both dict and list return types
        if isinstance(pages_data, dict):
            pages = pages_data.get('results', []) if 'results' in pages_data else pages_data.get('page', [])
        else:
            pages = pages_data
        
        if not pages:
            return f"No pages found in space {space_key}"
        
        result = f"Pages in space **{space_key}**:\\n\\n"
        for page in pages:
            page_title = page.get('title', 'N/A')
            page_id = page.get('id', 'N/A')
            result += f"- {page_title} (ID: {page_id})\\n"
        
        return result
    except Exception as e:
        return f"Error listing pages: {str(e)}"


@mcp.tool(description="Get page content by title")
def get_page_content(space_key: str, page_title: str) -> str:
    """Get the content of a page by title"""
    try:
        client = get_confluence_client()
        page = client.get_page_by_title(space_key, page_title)
        
        if not page:
            return f"Page '{page_title}' not found in space {space_key}"
        
        title = page.get('title', 'N/A')
        page_id = page.get('id', 'N/A')
        body = page.get('body', {}).get('storage', {}).get('value', 'No content')
        
        result = f"**{title}** (ID: {page_id})\\n\\n"
        # Safely handle body content
        if isinstance(body, str):
            result += f"Content:\n{body[:500]}...\n"
        else:
            result += "Content: [Unable to parse]"
        
        return result
    except Exception as e:
        return f"Error getting page content: {str(e)}"


@mcp.tool(description="Search for pages in Confluence")
def search_pages(query: str, limit: int = 10) -> str:
    """Search for pages in Confluence"""
    try:
        client = get_confluence_client()
        results = client.cql(query, limit=limit)
        
        if not results:
            return f"No results found for query: {query}"
        
        # Handle different return formats
        result_list = results.get('results', []) if isinstance(results, dict) else results
        
        if not result_list:
            return f"No results found for query: {query}"
        
        result = f"Search results for: **{query}**\n\n"
        for item in result_list[:limit]:
            item_type = item.get('type', 'unknown')
            title = item.get('title', 'N/A')
            space = item.get('space', {}).get('key', 'N/A')
            result += f"- [{item_type}] {title} (Space: {space})\\n"
        
        return result
    except Exception as e:
        return f"Error searching pages: {str(e)}"


@mcp.tool(description="Get Confluence instance info")
def get_confluence_info() -> str:
    """Get information about the Confluence instance"""
    try:
        client = get_confluence_client()
        # Try different method names that might exist
        info = None
        if hasattr(client, 'get_server_info'):
            info = client.get_server_info()
        elif hasattr(client, 'get_confluence_info'):
            info = client.get_confluence_info()
        else:
            # Fallback: use get_all_spaces to at least show we're connected
            spaces = client.get_all_spaces(limit=1)
            return "**Confluence Instance Connected**\n\nServer responding to requests."
        
        result = "**Confluence Instance Information**\n\n"
        result += f"Version: {info.get('version', info.get('versionNumbers', 'N/A'))}\n"
        result += f"Build Number: {info.get('buildNumber', 'N/A')}\\n"
        result += f"URL: {info.get('baseUrl', 'N/A')}\\n"
        
        return result
    except Exception as e:
        return f"Error getting Confluence info: {str(e)}"


def main():
    """Run the MCP server"""
    try:
        logger.info("Starting Confluence MCP Server...")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
