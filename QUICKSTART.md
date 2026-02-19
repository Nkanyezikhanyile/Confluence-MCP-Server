# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

With uv (recommended):
\\\ash
uv sync
\\\

With pip:
\\\ash
pip install -r requirements.txt
\\\

### 2. Configure Credentials

Copy and edit the environment file:
\\\ash
cp .env.example .env
\\\

Edit .env with your Confluence details:

**For Confluence Cloud:**
\\\env
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_TOKEN=your-api-token-from-settings
\\\

Get your API token: https://id.atlassian.com/manage-profile/security/api-tokens

**For Confluence Server/Data Center:**
\\\env
CONFLUENCE_URL=https://confluence.company.com
CONFLUENCE_USERNAME=your-username
CONFLUENCE_PASSWORD=your-password
\\\

### 3. Test the Server

Start the server:
\\\ash
uv run confluence_server.py
\\\

In another terminal, run the test script:
\\\ash
uv run test_server.py
\\\

You should see available tools and test results.

## Integrate with Claude Desktop

### Find Your Path

Get the absolute path to the python-mcp-server directory:
\\\ash
pwd  # On Mac/Linux
cd   # On Windows (will show current path)
\\\

### Update Claude Config

**Mac/Linux:**
\\\ash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
\\\

**Windows:**
- Press \Win + R\
- Type: \%APPDATA%\Claude\claude_desktop_config.json\
- Edit with your text editor

### Add This Configuration

\\\json
{
  "mcpServers": {
    "confluence": {
      "command": "uv",
      "args": [
        "--directory",
        "/YOUR/ABSOLUTE/PATH/TO/python-mcp-server",
        "run",
        "confluence_server.py"
      ]
    }
  }
}
\\\

**Important on Windows:** Use forward slashes (\/\) in the path, not backslashes (\\\\).

### Restart Claude Desktop

Close and reopen Claude Desktop. The Confluence server is now available!

## Try It Out

Ask Claude:
- "What Confluence spaces do we have?"
- "Show me pages in the [SPACE_KEY] space"
- "Search for documentation about [topic]"
- "Get the Confluence server version"

## Tools Available

1. **list_spaces** - See all Confluence spaces
2. **get_space_details** - Get space information
3. **list_pages** - List pages in a space
4. **get_page_content** - Read page content
5. **search_pages** - Search using Confluence Query Language (CQL)
6. **get_confluence_info** - Check instance version and URL

## Troubleshooting

**"Connection refused" or "Invalid credentials"**
- Verify CONFLUENCE_URL is correct
- Check username/token in .env
- Test URL in browser
- For Cloud: Verify API token is valid

**"Server didn't show up in Claude"**
- Restart Claude Desktop
- Check path in claude_desktop_config.json uses forward slashes
- Verify python-mcp-server directory exists at that path

**Python errors when running**
- Verify Python 3.10+ is installed: \python --version\
- Re-run: \uv sync\ or \pip install -r requirements.txt\
- Check .env file exists and has required variables

## Next Steps

- Read [README.md](./README.md) for full documentation
- Check [confluence_server.py](./confluence_server.py) to understand the code
- Extend with more tools using \@mcp.tool()\ decorator
- Check [MCP Docs](https://modelcontextprotocol.io/) for advanced features
