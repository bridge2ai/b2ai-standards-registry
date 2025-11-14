# AI Access to the Standards Explorer

The Bridge2AI Standards Explorer can be accessed by AI agents and Large Language Models (LLMs) through the **Standards Explorer MCP**. This enables AI assistants like Claude, ChatGPT, and others to search, query, and retrieve standards information in real-time.

## What is MCP?

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI applications connect to external data sources and tools. Think of it as a universal adapter that lets AI assistants access databases, APIs, and services in a consistent way.

## Standards Explorer MCP Server

The [Standards Explorer MCP Server](https://github.com/bridge2ai/standards-explorer-mcp) provides AI agents with tools to:

- 🔍 **Search standards** by name, description, or any text field
- 📊 **Execute SQL queries** directly against the Standards Explorer tables (standards, topics, substrates, organizations)
- 🎯 **Filter by topic, organization, or data substrate**
- 📖 **Retrieve detailed information** about specific standards
- 🔄 **Browse paginated results** for large result sets

No API key is required.

## Quick Start

### Installation

Depending on the software you use to work with AI agents, you may not need to install the MCP on its own.

Feel free to skip to the next section if you are not certain.

The MCP server requires Python 3.9+ and can be installed using `uv` or `pip`:

```bash
# Using uv (recommended)
uv pip install standards-explorer-mcp

# Or using pip
pip install standards-explorer-mcp
```

## Using the MCP with Agentic Frameworks

### Using with Claude Desktop

Claude Desktop has native MCP support. To add the Standards Explorer:

1. **Locate your Claude Desktop config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the Standards Explorer MCP server:**

```json
{
  "mcpServers": {
    "standards-explorer": {
      "command": "uvx",
      "args": ["standards-explorer-mcp"]
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Verify it's working:** Look for the 🔌 icon in Claude Desktop, or ask Claude:
   > "Can you search the Bridge2AI Standards Explorer for FHIR standards?"

### Using with VSCode (GitHub Copilot Chat)

VSCode with GitHub Copilot supports MCP servers through the Copilot Chat interface.

1. **Install the MCP extension for VSCode:**
   - Open VSCode Extensions (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "Model Context Protocol"
   - Install the MCP extension

2. **Configure the MCP server:**
   - Open VSCode Settings (Ctrl+, / Cmd+,)
   - Search for "MCP Servers"
   - Add the Standards Explorer configuration:

```json
{
  "mcp.servers": {
    "standards-explorer": {
      "command": "uvx",
      "args": ["standards-explorer-mcp"]
    }
  }
}
```

3. **Restart VSCode**

4. **Use in Copilot Chat:** Open Copilot Chat (Ctrl+Alt+I / Cmd+Option+I) and ask:
   > "@standards-explorer Find standards related to FHIR"

**Note:** MCP support in VSCode/GitHub Copilot may require specific versions or preview features. Check the [GitHub Copilot documentation](https://docs.github.com/en/copilot) for the latest information.

### Using with Goose

[Goose](https://github.com/square/goose) is an AI developer agent that runs in your terminal. It has native MCP support.

1. **Install Goose:**
```bash
# Install via pip
pip install goose-ai

# Or via homebrew (macOS)
brew install goose-ai
```

2. **Configure the MCP server:**

Create or edit `~/.config/goose/config.yaml`:

```yaml
mcp_servers:
  standards-explorer:
    command: uvx
    args:
      - standards-explorer-mcp
```

3. **Run Goose:**
```bash
goose session start
```

4. **Use the Standards Explorer:** In the Goose session, ask:
   > "Use the standards-explorer to find genomics standards"
   
   > "Query the Bridge2AI Standards Explorer for HL7 standards"

Goose will automatically use the MCP server to access the Standards Explorer data.

### Using with Other AI Applications

The MCP server uses the standard Model Context Protocol, so it works with any MCP-compatible AI application:

```python
from fastmcp import Client

async with Client("standards-explorer-mcp") as client:
    # Search for standards
    result = await client.call_tool(
        "search_standards",
        {"search_text": "FHIR", "max_results": 5}
    )
    print(result.data)
```

## Available Tools

The MCP server provides several tools that AI agents can use:

### 1. `search_standards`

Search for standards by text across multiple fields.

**Parameters:**
- `search_text` (required): Text to search for
- `columns_to_search` (optional): Specific columns to search (default: name, description)
- `max_results` (optional): Maximum results to return (default: 10)
- `offset` (optional): Skip this many results for pagination (default: 0)
- `include_topic_search` (optional): Also search by topic name (default: true)
- `include_substrate_search` (optional): Also search by substrate name (default: true)
- `include_organization_search` (optional): Also search by organization name (default: true)

**Example queries you can ask:**
- "Find standards related to FHIR"
- "Search for genomics standards"
- "Show me standards from HL7"
- "What standards work with JSON?"

### 2. `query_table`

Execute custom SQL queries against the Standards Explorer tables.

**Parameters:**
- `sql_query` (required): SQL query to execute
- `max_wait_seconds` (optional): Maximum wait time (default: 30)

**Example SQL queries:**
```sql
-- Find open standards
SELECT id, name, is_open FROM syn63096833 WHERE is_open = 'true' LIMIT 10

-- Search by description
SELECT id, name, description FROM syn63096833 
WHERE description LIKE '%metadata%' LIMIT 5

-- Filter by category
SELECT name, category FROM syn63096833 
WHERE category = 'B2AI_STANDARD:BiomedicalStandard' LIMIT 20
```

### 3. `search_by_topic`

Find standards related to a specific data topic.

**Parameters:**
- `topic_name` (required): Name of the topic (e.g., "EHR", "Genomics", "Image")
- `max_results` (optional): Maximum results (default: 20)

**Example queries:**
- "Find standards for EHR data"
- "What standards concern genomics?"
- "Show me imaging standards"

### 4. `search_by_substrate`

Find standards that work with specific data formats or structures.

**Parameters:**
- `substrate_name` (required): Name of the substrate (e.g., "JSON", "CSV", "BIDS")
- `max_results` (optional): Maximum results (default: 20)

**Example queries:**
- "Find standards that use JSON"
- "What standards work with CSV files?"
- "Show me BIDS-compatible standards"

### 5. `search_by_organization`

Find standards associated with specific organizations.

**Parameters:**
- `organization_name` (required): Name of the organization (e.g., "HL7", "W3C", "CDISC")
- `max_results` (optional): Maximum results (default: 20)
- `search_responsible_only` (optional): Only search responsible organizations (default: false)

**Example queries:**
- "What standards does HL7 maintain?"
- "Find W3C standards"
- "Show me CDISC standards"

### 6. `list_topics` / `list_substrates` / `list_organizations`

Get complete lists of available topics, substrates, or organizations.

**Example queries:**
- "What topics are available in the Standards Explorer?"
- "List all data substrates"
- "Show me all organizations"

### 7. `get_standards_table_info`

Get metadata about the Standards Explorer tables and project.

## Example Conversations

Here are examples of how you might interact with an AI assistant using the MCP server:

### Example 1: Finding Healthcare Standards

**You:** "Can you find healthcare interoperability standards?"

**AI:** *Uses `search_standards` with "healthcare interoperability"*

"I found several healthcare interoperability standards:

1. **FHIR** (Fast Healthcare Interoperability Resources) - A standard for exchanging healthcare information electronically
2. **HL7 v2** - Messaging standard for healthcare data exchange
3. **HL7 CDA** - Clinical Document Architecture for medical documents
..."

### Example 2: Finding Standards by Organization

**You:** "What standards does the W3C maintain?"

**AI:** *Uses `search_by_organization` with "W3C"*

"The W3C (World Wide Web Consortium) is responsible for several standards in the Explorer:

1. **RDF** - Resource Description Framework
2. **JSON-LD** - JSON for Linking Data
3. **PROV-O** - Provenance Ontology
..."

### Example 3: Topic-Based Search

**You:** "Show me standards for genomic data"

**AI:** *Uses `search_by_topic` with "Genomics"*

"Here are standards that concern genomic data:

1. **VCF** - Variant Call Format
2. **FASTQ** - Format for storing biological sequences
3. **BAM/SAM** - Binary/Sequence Alignment Map formats
..."

### Example 4: Custom SQL Query

**You:** "Find all open-source standards that work with imaging data"

**AI:** *Uses `query_table` with a SQL query joining multiple criteria*

"I found 15 open-source imaging standards:

1. **NIfTI** - Neuroimaging Informatics Technology Initiative format
2. **DICOM** - Digital Imaging and Communications in Medicine
3. **BIDS** - Brain Imaging Data Structure
..."

## Advanced Usage

### Running the Server Standalone

For development or debugging, you can run the MCP server directly:

```bash
# Start the server
uv run standards-explorer-mcp

# Or with Python
python -m standards_explorer_mcp
```

The server communicates via stdio using the MCP protocol.

### Authentication (Optional)

The server accesses public Synapse tables and **does not require authentication**. However, if you need authenticated access for private tables (e.g., if you want to access Standards Explorer data alongside other data on Synapse):

```bash
# Set your Synapse Personal Access Token
export SYNAPSE_AUTH_TOKEN="your_token_here"

# Then run the server
uv run standards-explorer-mcp
```

To get a Synapse Personal Access Token:
1. Log in to [Synapse](https://www.synapse.org/)
2. Go to Account Settings → Personal Access Tokens
3. Create a new token with view/download scopes

### Testing the Server

The repository includes tests you can run:

```bash
# Clone the repository
git clone https://github.com/bridge2ai/standards-explorer-mcp.git
cd standards-explorer-mcp

# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/standards_explorer_mcp --cov-report=html
```

## Technical Details

### Architecture

The MCP server uses the Synapse Table Query API with an async job pattern:

1. **Start Query**: POST to `/entity/{id}/table/query/async/start` → returns async token
2. **Poll for Results**: GET `/entity/{id}/table/query/async/get/{token}` 
   - Returns 202 while processing
   - Returns 200 with results when complete
3. **Automatic Retry**: Server polls every 1 second with configurable timeout

### Tables Accessed

- `syn63096833` - DataStandardOrTool (main standards table)
- `syn63096835` - DataTopics (topics/domains)
- `syn63096834` - DataSubstrate (data formats)
- `syn63096836` - Organization (organizations)
- `syn63096806` - Project container

### Implementation

Built with:
- **FastMCP** (v2.12.5+) - MCP server framework
- **httpx** (v0.27.0+) - Async HTTP client
- **Python 3.9+** - Runtime environment

The server separates business logic from MCP decorators for easy testing and maintenance.

## Troubleshooting

### Server Not Starting

**Problem:** MCP server fails to start in Claude Desktop

**Solutions:**
- Check that `uvx` is installed: `uv --version`
- Verify the config file syntax is valid JSON
- Check Claude Desktop logs for error messages
- Try running `uvx standards-explorer-mcp` manually to test

### No Tools Appearing

**Problem:** AI assistant doesn't show Standards Explorer tools

**Solutions:**
- Restart Claude Desktop after editing config
- Look for the 🔌 icon to confirm MCP connection
- Check that the server process is running
- Verify network access to `repo-prod.prod.sagebase.org`

### Queries Timing Out

**Problem:** Queries take too long or timeout

**Solutions:**
- Increase `max_wait_seconds` parameter
- Use LIMIT clauses to reduce result size
- Check internet connection to Synapse API
- Try simpler queries first to verify connectivity

### Search Returns No Results

**Problem:** Searches don't find expected standards

**Solutions:**
- Try broader search terms
- Use `list_topics` or `list_substrates` to see available options
- Check spelling of organization/topic names
- Use `query_table` with SQL LIKE for flexible matching

## Resources

- **MCP Server Repository**: [github.com/bridge2ai/standards-explorer-mcp](https://github.com/bridge2ai/standards-explorer-mcp)
- **Model Context Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **FastMCP Documentation**: [gofastmcp.com](https://gofastmcp.com/)
- **Claude Desktop MCP Guide**: [Anthropic MCP Documentation](https://docs.anthropic.com/claude/docs)
- **Synapse REST API**: [rest-docs.synapse.org](https://rest-docs.synapse.org/rest/index.html)
- **Standards Explorer on Synapse**: [synapse.org/Synapse:syn63096806](https://www.synapse.org/Synapse:syn63096806/tables/)

## Support

For questions or issues:
- **MCP Server Issues**: [GitHub Issues](https://github.com/bridge2ai/standards-explorer-mcp/issues)
- **Standards Explorer Content**: [b2ai-standards-registry Issues](https://github.com/bridge2ai/b2ai-standards-registry/issues)
- **FastMCP Support**: [FastMCP Discord](https://discord.gg/uu8dJCgttd)
- **Synapse API Support**: [help.synapse.org](https://help.synapse.org/)

## Next Steps

After setting up the MCP server:

1. **Try basic searches**: Ask your AI assistant to search for familiar standards
2. **Explore topics**: Use `list_topics` to see what domains are covered
3. **Experiment with SQL**: Try custom queries for specific use cases
4. **Combine with other tools**: Use Standards Explorer data alongside other MCP servers
5. **Provide feedback**: Report issues or suggest features on GitHub

For programmatic access without AI agents, see [Programmatic Access](programmatic-access.md).
