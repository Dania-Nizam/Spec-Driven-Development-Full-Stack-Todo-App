# Quickstart Guide: MCP Integration for Todo Chatbot

**Feature**: MCP Integration (001-mcp-integration)
**Date**: 2026-02-03
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

## Overview

This guide provides step-by-step instructions to set up and run the Model Context Protocol (MCP) integration for the Todo Chatbot. The MCP server exposes standardized tools for todo operations with JWT authentication and stateful conversation support.

## Prerequisites

- Python 3.11+
- pip package manager
- Existing Phase II Todo application with database
- Valid BETTER_AUTH_SECRET configured
- Network connectivity for external services (if applicable)

## Installation

### 1. Install MCP Dependencies

First, install the Official MCP SDK and related dependencies:

```bash
# Navigate to the backend directory
cd /path/to/todo-app/backend

# Activate your virtual environment
source venv/bin/activate  # Linux/Mac
# or
source venv\Scripts\activate  # Windows

# Install MCP SDK and dependencies
pip install mcp-python
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

### 2. Verify Existing Dependencies

Ensure the following dependencies are available (should already be installed for Phase II/III):

```bash
pip install fastapi
pip install uvicorn
pip install sqlmodel
pip install psycopg2-binary
```

## Configuration

### 1. Environment Variables

Add the following environment variables to your `.env` file:

```env
# MCP Server Configuration
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
MCP_SERVER_DEBUG=false

# Authentication (must match Phase II/III settings)
BETTER_AUTH_SECRET=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname

# Optional: MCP-specific settings
MCP_SESSION_TIMEOUT=1800  # 30 minutes in seconds
MCP_MAX_CONCURRENT_SESSIONS=50
```

### 2. Database Setup

The MCP integration uses the existing Phase II database schema. No additional migrations are required as MCP stores session data in memory/cache by default.

## Running the MCP Server

### 1. Start the MCP Server

```bash
# Navigate to backend directory
cd /path/to/todo-app/backend

# Activate virtual environment
source venv/bin/activate

# Start the MCP server
python -m mcp.server
```

Alternatively, you can use uvicorn:

```bash
uvicorn mcp.server:app --host 0.0.0.0 --port 8001
```

### 2. Verify Server is Running

Check that the server is running by visiting:
```
http://localhost:8001/health
```

You should see a response like:
```json
{
  "status": "healthy",
  "service": "mcp-server",
  "version": "1.0.0"
}
```

## Using MCP Tools

### 1. Authentication

All MCP tool calls require JWT authentication. Obtain a valid JWT token from the main application's authentication endpoint:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### 2. Calling MCP Tools

Once authenticated, you can call MCP tools with your JWT token:

```bash
curl -X POST http://localhost:8001/mcp/tools/add_task \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample task",
    "description": "This is a sample task created via MCP",
    "priority": "medium"
  }'
```

### 3. Available MCP Tools

The following tools are available through the MCP server:

#### add_task
- **Endpoint**: `POST /mcp/tools/add_task`
- **Parameters**: `title` (string, required), `description` (string, optional), `priority` (string, optional), `due_date` (string, optional)
- **Returns**: Created task object with ID

#### view_tasks
- **Endpoint**: `POST /mcp/tools/view_tasks`
- **Parameters**: `status` (string, optional), `priority` (string, optional), `limit` (integer, optional), `offset` (integer, optional)
- **Returns**: Array of task objects

#### update_task
- **Endpoint**: `POST /mcp/tools/update_task`
- **Parameters**: `task_id` (integer, required), `title` (string, optional), `description` (string, optional), `priority` (string, optional)
- **Returns**: Updated task object

#### delete_task
- **Endpoint**: `POST /mcp/tools/delete_task`
- **Parameters**: `task_id` (integer, required)
- **Returns**: Confirmation of deletion

#### mark_complete
- **Endpoint**: `POST /mcp/tools/mark_complete`
- **Parameters**: `task_id` (integer, required), `completed` (boolean, optional, default: true)
- **Returns**: Updated task object

#### search_filter_tasks
- **Endpoint**: `POST /mcp/tools/search_filter_tasks`
- **Parameters**: `query` (string, optional), `status` (string, optional), `priority` (string, optional), `tags` (array, optional)
- **Returns**: Array of matching task objects

## Integration with ChatbotOrchestratorAgent

### 1. Configure MCP Integration

To use MCP tools from the ChatbotOrchestratorAgent, ensure the following configuration:

```python
# In your orchestrator configuration
MCP_SERVER_URL = "http://localhost:8001"
MCP_ENABLED = True
```

### 2. Example Integration

The ChatbotOrchestratorAgent can call MCP tools like this:

```python
# Example of MCP tool call from orchestrator
async def call_mcp_tool(tool_name: str, parameters: dict, jwt_token: str):
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    response = await http_client.post(
        f"http://localhost:8001/mcp/tools/{tool_name}",
        json=parameters,
        headers=headers
    )

    return response.json()
```

## Development Setup

### 1. Running in Development Mode

For development, you can run the server with auto-reload:

```bash
uvicorn mcp.server:app --reload --host 0.0.0.0 --port 8001
```

### 2. Running Tests

Execute the MCP-specific tests:

```bash
# Run MCP unit tests
python -m pytest tests/mcp/test_server.py

# Run MCP integration tests
python -m pytest tests/mcp/test_integration.py

# Run all MCP tests
python -m pytest tests/mcp/
```

### 3. Environment Configuration for Development

Create a development-specific `.env` file:

```env
# Development-specific settings
MCP_SERVER_DEBUG=true
MCP_LOG_LEVEL=DEBUG
MCP_SESSION_TIMEOUT=3600  # 1 hour for development

# Same authentication as production
BETTER_AUTH_SECRET=your-dev-secret-key
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure your JWT token is valid and not expired
   - Verify that BETTER_AUTH_SECRET matches between services
   - Check that the user_id in the token matches the requested operation

2. **Connection Issues**
   - Verify that the MCP server is running on the expected port
   - Check firewall settings if running across different machines
   - Ensure the database connection is available

3. **Tool Not Found Errors**
   - Verify that the tool name matches exactly what's registered
   - Check that the MCP server has loaded all tool definitions
   - Review server logs for registration errors

### Debugging Commands

```bash
# Check server status
curl http://localhost:8001/health

# List available tools
curl http://localhost:8001/mcp/tools/list

# Check server logs
tail -f logs/mcp-server.log
```

## Stopping the Server

To stop the MCP server, press `Ctrl+C` in the terminal where it's running.