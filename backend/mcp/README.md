# Model Context Protocol (MCP) Integration

This directory contains the implementation for the Model Context Protocol (MCP) integration with the Todo Chatbot. The MCP server exposes standardized tools for todo operations with JWT authentication and stateful conversation support.

## Overview

The MCP integration enables standardized tool exposure for the Todo Chatbot, allowing for:
- Standardized tool calling interfaces
- Stateful conversation contexts
- JWT-authenticated tool access
- Integration with OpenAI Agents SDK and Claude Code workflows
- Advanced features like recurring tasks and due date reminders

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Chatbot       │────│   MCP Server     │────│   Todo Skills    │
│   Orchestrator  │    │                  │    │                  │
└─────────────────┘    │ • Tool Registry  │    │ • add_task       │
                       │ • Auth Wrapper   │    │ • view_tasks     │
                       │ • Session Mgmt   │    │ • update_task    │
                       │ • Context Mgmt   │    │ • delete_task    │
                       └──────────────────┘    │ • mark_complete  │
                                               │ • search_filter  │
                                               │ • set_recurring  │
                                               │ • get_context    │
                                               └──────────────────┘
```

## Components

### MCP Server (`server.py`)
Main entry point for the MCP server, implementing the core protocol and handling client connections.

### Tools (`tools/`)
Individual tool implementations that map to existing todo skills:
- `add_task.py` - Add new tasks
- `view_tasks.py` - View tasks with filtering
- `update_task.py` - Update existing tasks
- `delete_task.py` - Delete tasks
- `mark_complete.py` - Mark tasks as complete/incomplete
- `search_filter_tasks.py` - Search and filter tasks
- `set_recurring.py` - Configure recurring tasks
- `get_task_context.py` - Retrieve task context

### Authentication (`auth.py`)
JWT authentication wrapper that validates tokens before executing any MCP tool calls, ensuring user isolation.

### Context Management (`context.py`)
Handles conversation state across multiple tool calls, maintaining context for stateful conversations.

### Configuration (`config.py`)
Server configuration and settings management.

### Integration (`integration.py`)
Layer connecting MCP tools to existing todo skills, ensuring seamless integration with the existing system.

## API Endpoints

- `GET /health` - Server health check
- `GET /mcp/tools/list` - List available tools
- `POST /mcp/tools/{tool_name}` - Execute specific tool
- `GET /mcp/session/{session_id}` - Get session information

## Security

All MCP tool calls require JWT authentication using the same patterns as the Phase II Todo application. The system enforces strict user isolation, ensuring that users can only access their own data.

## Usage

To start the MCP server:

```bash
cd backend
python -m mcp.server
```

Or with uvicorn:

```bash
uvicorn mcp.server:app --host 0.0.0.0 --port 8001
```

## Integration with ChatbotOrchestratorAgent

The ChatbotOrchestratorAgent can call MCP tools through the integration layer, allowing for standardized tool access while maintaining compatibility with existing functionality.