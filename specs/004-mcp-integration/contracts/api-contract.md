# API Contract: MCP Integration for Todo Chatbot

**Feature**: MCP Integration (001-mcp-integration)
**Date**: 2026-02-03
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

## Overview

This document defines the API contract for the Model Context Protocol (MCP) integration with the Todo Chatbot. The MCP server exposes standardized tools for todo operations with JWT authentication and stateful conversation support.

## MCP Server Endpoints

### Health Check

**Endpoint**: `GET /health`

**Description**: Check the health status of the MCP server.

**Request**:
- Headers: None required
- Body: None
- Query Parameters: None

**Response**:
- Status: `200 OK`
- Content-Type: `application/json`
- Body:
```json
{
  "status": "healthy",
  "service": "mcp-server",
  "version": "1.0.0"
}
```

### List Available Tools

**Endpoint**: `GET /mcp/tools/list`

**Description**: Retrieve a list of all available MCP tools.

**Request**:
- Headers:
  - `Authorization: Bearer <valid_jwt_token>` (required)
- Body: None
- Query Parameters: None

**Response**:
- Status: `200 OK`
- Content-Type: `application/json`
- Body:
```json
{
  "tools": [
    {
      "name": "add_task",
      "description": "Add a new task to the user's todo list",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "description": "The title of the task"
          },
          "description": {
            "type": "string",
            "description": "Optional description of the task"
          },
          "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "Priority of the task"
          },
          "due_date": {
            "type": "string",
            "format": "date",
            "description": "Due date for the task in YYYY-MM-DD format"
          }
        },
        "required": ["title"]
      }
    },
    {
      "name": "view_tasks",
      "description": "View the user's tasks with optional filtering",
      "parameters": {
        "type": "object",
        "properties": {
          "status": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "description": "Filter by task status (default: all)"
          },
          "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "Filter by task priority"
          },
          "limit": {
            "type": "integer",
            "description": "Maximum number of tasks to return"
          },
          "offset": {
            "type": "integer",
            "description": "Number of tasks to skip (for pagination)"
          }
        }
      }
    }
  ]
}
```

### Execute MCP Tool

**Endpoint**: `POST /mcp/tools/{tool_name}`

**Description**: Execute a specific MCP tool with provided parameters.

**Path Parameters**:
- `tool_name`: The name of the tool to execute (e.g., add_task, view_tasks)

**Request**:
- Headers:
  - `Authorization: Bearer <valid_jwt_token>` (required)
  - `Content-Type: application/json`
- Body: JSON object with tool parameters as defined in the tool schema
- Query Parameters: None

**Valid Tool Names**:
- `add_task`
- `view_tasks`
- `update_task`
- `delete_task`
- `mark_complete`
- `search_filter_tasks`
- `set_recurring`
- `get_task_context`

**Example Request** (add_task):
```json
{
  "title": "Buy groceries",
  "description": "Buy milk, bread, and eggs",
  "priority": "high",
  "due_date": "2026-02-05"
}
```

**Response**:
- Status: `200 OK` on success
- Status: `401 Unauthorized` for invalid/missing JWT
- Status: `403 Forbidden` for user isolation violations
- Status: `400 Bad Request` for invalid parameters
- Status: `500 Internal Server Error` for server errors
- Content-Type: `application/json`

**Successful Response Body**:
```json
{
  "success": true,
  "result": {
    // Tool-specific result
  },
  "session_id": "uuid-of-session",
  "timestamp": "2026-02-03T10:00:00Z"
}
```

**Error Response Body**:
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-readable error message",
  "session_id": "uuid-of-session",
  "timestamp": "2026-02-03T10:00:00Z"
}
```

### Session Management

**Endpoint**: `GET /mcp/session/{session_id}`

**Description**: Get information about a specific MCP session.

**Path Parameters**:
- `session_id`: The ID of the session to retrieve

**Request**:
- Headers:
  - `Authorization: Bearer <valid_jwt_token>` (required)
- Body: None
- Query Parameters: None

**Response**:
- Status: `200 OK` on success
- Status: `401 Unauthorized` for invalid/missing JWT
- Status: `403 Forbidden` for user isolation violations
- Status: `404 Not Found` for non-existent session
- Content-Type: `application/json`

**Response Body**:
```json
{
  "session_id": "uuid-of-session",
  "user_id": 123,
  "created_at": "2026-02-03T09:00:00Z",
  "last_activity_at": "2026-02-03T10:00:00Z",
  "expires_at": "2026-02-03T10:30:00Z",
  "is_active": true,
  "context_summary": {
    "previous_tasks_referenced": [1, 2, 3],
    "current_topic": "task management",
    "pending_clarifications": []
  }
}
```

## Authentication & Authorization

### JWT Token Requirements

All MCP endpoints (except `/health`) require a valid JWT token in the Authorization header:
- Header: `Authorization: Bearer <jwt_token>`
- Token must be valid and not expired
- User ID in token must match the requested operation scope

### Error Responses

#### 401 Unauthorized
```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Invalid or missing JWT token",
  "timestamp": "2026-02-03T10:00:00Z"
}
```

#### 403 Forbidden
```json
{
  "success": false,
  "error": "forbidden",
  "message": "Access denied: User ID mismatch or insufficient permissions",
  "timestamp": "2026-02-03T10:00:00Z"
}
```

#### 400 Bad Request
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Invalid parameters provided",
  "details": [
    {
      "field": "title",
      "issue": "required"
    }
  ],
  "timestamp": "2026-02-03T10:00:00Z"
}
```

## Data Schemas

### Task Object Schema
```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Unique identifier for the task"
    },
    "user_id": {
      "type": "integer",
      "description": "ID of the user who owns the task"
    },
    "title": {
      "type": "string",
      "description": "Title of the task"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the task"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Priority of the task"
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "description": "Due date for the task in YYYY-MM-DD format"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when the task was created"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when the task was last updated"
    }
  },
  "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
}
```

### Recurring Task Pattern Schema
```json
{
  "type": "object",
  "properties": {
    "frequency": {
      "type": "string",
      "enum": ["daily", "weekly", "monthly", "yearly"],
      "description": "How often the task recurs"
    },
    "interval": {
      "type": "integer",
      "description": "Interval multiplier (e.g., every 2 weeks)",
      "minimum": 1
    },
    "ends_on": {
      "type": "string",
      "format": "date",
      "description": "Date when recurrence should end"
    },
    "occurrences": {
      "type": "integer",
      "description": "Number of occurrences before ending",
      "minimum": 1
    }
  },
  "required": ["frequency"]
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| unauthorized | 401 | Missing or invalid JWT token |
| forbidden | 403 | User ID mismatch or insufficient permissions |
| validation_error | 400 | Invalid parameters provided |
| not_found | 404 | Requested resource not found |
| rate_limited | 429 | Too many requests |
| server_error | 500 | Internal server error |
| tool_not_found | 404 | Requested tool does not exist |
| session_expired | 401 | Session has expired |
| context_error | 400 | Conversation context issue |

## Rate Limits

The MCP server implements rate limiting:
- Per-user: 100 requests per minute per user
- Per-IP: 1000 requests per minute per IP address
- Per-session: 50 tool calls per minute per session

Rate limited requests return status `429 Too Many Requests` with:
```json
{
  "success": false,
  "error": "rate_limited",
  "message": "Too many requests, please try again later",
  "retry_after": 60,
  "timestamp": "2026-02-03T10:00:00Z"
}
```

## Versioning

The API uses semantic versioning. Current version: v1.0.0
Future versions will be served under `/mcp/v2/`, `/mcp/v3/`, etc., with the base path serving the current version.