# Confluence MCP Server

A Model Context Protocol (MCP) server for integrating Confluence with AI applications like Claude.

## Overview

This MCP server provides tools to interact with Confluence spaces and pages, enabling AI applications to:
- List and search Confluence spaces
- Browse pages and page content
- Search across Confluence
- Get Confluence instance information

## Features

The server exposes the following tools:

- **list_spaces**: List all Confluence spaces
- **get_space_details**: Get detailed information about a specific space
- **list_pages**: List pages in a specific space
- **get_page_content**: Get the content of a page by title
- **search_pages**: Search for pages using CQL (Confluence Query Language)
- **get_confluence_info**: Get information about the Confluence instance

## Installation

### Prerequisites

- Python 3.10 or higher
- uv (recommended) or pip for package management

### Setup

1. Clone or create the project directory
2. Install dependencies using uv:

\\\bash
uv sync
\\\

Or with pip:

\\\bash
pip install -r requirements.txt
\\\

## Configuration

1. Copy the example configuration:

\\\bash
cp .env.example .env
\\\

2. Edit .env and add your Confluence credentials:

### For Confluence Cloud:

\\\env
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_TOKEN=your-api-token
\\\

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

### For Confluence Server/Data Center:

\\\env
CONFLUENCE_URL=https://confluence.company.com
CONFLUENCE_USERNAME=your-username
CONFLUENCE_PASSWORD=your-password
\\\

## Running the Server

### With uv:

\\\bash
uv run confluence_server.py
\\\

### With Python directly:

\\\bash
python confluence_server.py
\\\

### With MCP Inspector (for testing):

\\\bash
# Terminal 1: Start the server
uv run confluence_server.py

# Terminal 2: Run the inspector
npx -y @modelcontextprotocol/inspector
\\\

Then connect to http://localhost:8000/mcp in the inspector.

## Integration with Claude Desktop

### macOS/Linux:

1. Edit your Claude Desktop config:

\\\bash
code ~/Library/Application Support/Claude/claude_desktop_config.json
\\\

2. Add the server configuration:

\\\json
{
  "mcpServers": {
    "confluence": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/python-mcp-server",
        "run",
        "confluence_server.py"
      ]
    }
  }
}
\\\

3. Restart Claude Desktop

### Windows:

1. Edit your Claude Desktop config:

\\\
code %APPDATA%\Claude\claude_desktop_config.json
\\\

2. Add the server configuration with forward slashes:

\\\json
{
  "mcpServers": {
    "confluence": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Dev/Confluence MCP Hackathon/python-mcp-server",
        "run",
        "confluence_server.py"
      ]
    }
  }
}
\\\

3. Restart Claude Desktop

## Example Usage

Once integrated with Claude Desktop, you can ask:

- "What spaces do we have in Confluence?"
- "Show me the pages in the Engineering space"
- "Search for documentation about API"
- "Get the content of the Getting Started page in our main space"
- "What Confluence version are we running?"

## Architecture

The server uses:
- **mcp[cli]**: The official Python MCP SDK with FastMCP
- **atlassian-python-api**: Python library for Confluence API interaction
- **FastMCP**: Simplified MCP server framework with automatic tool discovery

## Tool Details

### list_spaces(limit: int = 25)
Lists Confluence spaces with pagination support.

### get_space_details(space_key: str)
Returns detailed information about a space including name, key, type, and description.

### list_pages(space_key: str, limit: int = 10)
Lists pages in a specific space with pagination.

### get_page_content(space_key: str, page_title: str)
Retrieves the content of a specific page by its title.

### search_pages(query: str, limit: int = 10)
Searches for pages using CQL (Confluence Query Language). Example queries:
- \	ext ~ "keyword"\
- \space = KEY AND type = page\
- \created <= -1d\

### get_confluence_info()
Returns information about the Confluence instance including version and URL.

## Error Handling

The server handles common errors gracefully:
- Missing credentials
- Connection failures
- Invalid space keys or page titles
- API rate limiting

All errors are returned as readable messages to the AI client.

## Troubleshooting

### Connection Issues

1. Verify CONFLUENCE_URL is correct
2. Check credentials are valid
3. Ensure your Confluence instance is accessible from your machine
4. For Cloud, verify your API token hasn't expired

### Tool Not Showing Up in Claude

1. Restart Claude Desktop
2. Check the logs in Claude Server > Server Logs
3. Verify the .env file contains valid credentials

## Security

 **Important**: Never commit your .env file to version control. The .env.example file shows the required variables without sensitive data.

For production deployments:
- Use environment variables or secure credential management
- Consider using OAuth2 authentication
- Restrict API token permissions to minimum required

## Development

To extend the server with additional Confluence functionality:

1. Edit confluence_server.py
2. Add new tools using the @mcp.tool() decorator
3. Test with the MCP Inspector
4. Restart Claude Desktop to reload changes

## References

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Confluence Python API](https://atlassian-python-api.readthedocs.io/)
- [Confluence REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/)
- [CQL (Confluence Query Language)](https://developer.atlassian.com/cloud/confluence/basic-cql/)

## License

MIT
