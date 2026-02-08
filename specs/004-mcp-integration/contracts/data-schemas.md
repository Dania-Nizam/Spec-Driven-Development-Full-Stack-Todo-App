# Data Schemas: MCP Integration for Todo Chatbot

**Feature**: MCP Integration (001-mcp-integration)
**Date**: 2026-02-03
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

## Overview

This document defines the data schemas used in the Model Context Protocol (MCP) integration with the Todo Chatbot. These schemas govern the structure of requests, responses, and data models used by the MCP server and its tools.

## MCP Tool Definition Schema

### Tool Definition Object
```json
{
  "type": "object",
  "properties": {
    "tool_id": {
      "type": "string",
      "description": "Unique identifier for the tool",
      "pattern": "^[a-z0-9_-]+$"
    },
    "name": {
      "type": "string",
      "description": "Display name of the tool",
      "minLength": 1,
      "maxLength": 100
    },
    "description": {
      "type": "string",
      "description": "Human-readable description of the tool",
      "maxLength": 1000
    },
    "input_schema": {
      "type": "object",
      "description": "JSON Schema for input parameters",
      "$ref": "#/definitions/jsonSchema"
    },
    "output_schema": {
      "type": "object",
      "description": "JSON Schema for output",
      "$ref": "#/definitions/jsonSchema"
    },
    "authentication_required": {
      "type": "boolean",
      "description": "Whether authentication is required",
      "default": true
    },
    "is_active": {
      "type": "boolean",
      "description": "Whether the tool is enabled",
      "default": true
    },
    "version": {
      "type": "string",
      "description": "Version of the tool definition",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    }
  },
  "required": ["tool_id", "name", "description", "input_schema", "output_schema", "version"],
  "definitions": {
    "jsonSchema": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["object", "array", "string", "number", "integer", "boolean", "null"]
        },
        "properties": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/definitions/jsonSchema"
          }
        },
        "required": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

## MCP Session Schema

### Session Object
```json
{
  "type": "object",
  "properties": {
    "session_id": {
      "type": "string",
      "description": "Unique identifier for the session",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "user_id": {
      "type": "integer",
      "description": "Reference to the authenticated user",
      "minimum": 1
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when session was created"
    },
    "last_activity_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of last activity"
    },
    "expires_at": {
      "type": "string",
      "format": "date-time",
      "description": "Session expiration time"
    },
    "context_data": {
      "type": "object",
      "description": "Serialized conversation context",
      "additionalProperties": true
    },
    "is_active": {
      "type": "boolean",
      "description": "Whether the session is currently active",
      "default": true
    }
  },
  "required": ["session_id", "user_id", "created_at", "expires_at", "is_active"]
}
```

## MCP Tool Call Schema

### Tool Call Object
```json
{
  "type": "object",
  "properties": {
    "call_id": {
      "type": "string",
      "description": "Unique identifier for the tool call",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "session_id": {
      "type": "string",
      "description": "Reference to the parent session",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "tool_name": {
      "type": "string",
      "description": "Name of the tool being called",
      "pattern": "^[a-z0-9_]+$",
      "maxLength": 100
    },
    "input_parameters": {
      "type": "object",
      "description": "Parameters passed to the tool",
      "additionalProperties": true
    },
    "result": {
      "type": "object",
      "description": "Result returned by the tool",
      "additionalProperties": true
    },
    "error": {
      "type": "string",
      "description": "Error message if the call failed",
      "maxLength": 1000
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the call was made"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "success", "error"],
      "description": "Status of the call"
    }
  },
  "required": ["call_id", "session_id", "tool_name", "timestamp", "status"]
}
```

## MCP Conversation Context Schema

### Conversation Context Object
```json
{
  "type": "object",
  "properties": {
    "session_id": {
      "type": "string",
      "description": "Reference to the session",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "context_id": {
      "type": "string",
      "description": "Unique identifier for this context",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "previous_tasks_referenced": {
      "type": "array",
      "description": "Task IDs referenced in conversation",
      "items": {
        "type": "integer",
        "minimum": 1
      },
      "uniqueItems": true
    },
    "current_topic": {
      "type": "string",
      "description": "Current topic of conversation",
      "maxLength": 200
    },
    "pending_clarifications": {
      "type": "array",
      "description": "Clarifications needed from user",
      "items": {
        "type": "string",
        "maxLength": 500
      }
    },
    "conversation_history": {
      "type": "array",
      "description": "History of conversation turns",
      "items": {
        "type": "object",
        "properties": {
          "turn_id": {
            "type": "string",
            "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
          },
          "role": {
            "type": "string",
            "enum": ["user", "assistant"]
          },
          "content": {
            "type": "string",
            "maxLength": 5000
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          }
        },
        "required": ["turn_id", "role", "content", "timestamp"]
      }
    },
    "last_task_action": {
      "type": "string",
      "description": "Last action taken on a task",
      "enum": ["add", "update", "delete", "view", "mark_complete", "search", "set_recurring"],
      "maxLength": 20
    },
    "last_task_id": {
      "type": "integer",
      "description": "ID of the last referenced task",
      "minimum": 1
    }
  },
  "required": ["session_id", "context_id"]
}
```

## Request/Response Schemas

### Generic Request Schema
```json
{
  "type": "object",
  "properties": {
    "session_id": {
      "type": "string",
      "description": "Session identifier for stateful operations",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "request_id": {
      "type": "string",
      "description": "Unique identifier for this request",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the request was made"
    },
    "data": {
      "type": "object",
      "description": "Request-specific data",
      "additionalProperties": true
    }
  },
  "required": ["request_id", "timestamp", "data"]
}
```

### Generic Response Schema
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation succeeded"
    },
    "result": {
      "type": "object",
      "description": "Result data if successful",
      "additionalProperties": true
    },
    "error": {
      "type": "object",
      "description": "Error information if unsuccessful",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code"
        },
        "message": {
          "type": "string",
          "description": "Human-readable error message"
        },
        "details": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": true
          }
        }
      },
      "required": ["code", "message"]
    },
    "session_id": {
      "type": "string",
      "description": "Session identifier for stateful operations",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "request_id": {
      "type": "string",
      "description": "Identifier for the original request",
      "pattern": "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the response was generated"
    }
  },
  "required": ["success", "session_id", "request_id", "timestamp"]
}
```

## Tool-Specific Schemas

### Add Task Tool Schema
Input:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "The title of the task",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional description of the task",
      "maxLength": 1000
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Priority of the task",
      "default": "medium"
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "description": "Due date for the task in YYYY-MM-DD format"
    },
    "tags": {
      "type": "array",
      "description": "Tags to assign to the task",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      }
    }
  },
  "required": ["title"]
}
```

Output:
```json
{
  "type": "object",
  "properties": {
    "task": {
      "$ref": "#/definitions/taskObject"
    },
    "message": {
      "type": "string",
      "description": "Confirmation message"
    }
  },
  "required": ["task", "message"]
}
```

### View Tasks Tool Schema
Input:
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "description": "Filter by task status",
      "default": "all"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "all"],
      "description": "Filter by task priority"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "description": "Maximum number of tasks to return"
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of tasks to skip (for pagination)"
    },
    "sort_by": {
      "type": "string",
      "enum": ["created_at", "updated_at", "due_date", "priority"],
      "description": "Field to sort by",
      "default": "created_at"
    },
    "sort_order": {
      "type": "string",
      "enum": ["asc", "desc"],
      "description": "Sort order",
      "default": "desc"
    }
  }
}
```

Output:
```json
{
  "type": "object",
  "properties": {
    "tasks": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/taskObject"
      }
    },
    "total_count": {
      "type": "integer",
      "description": "Total number of tasks matching the criteria"
    },
    "filtered_count": {
      "type": "integer",
      "description": "Number of tasks returned in this response"
    },
    "message": {
      "type": "string",
      "description": "Informational message"
    }
  },
  "required": ["tasks", "total_count", "filtered_count"]
}
```

### Update Task Tool Schema
Input:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "New title for the task"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "New description for the task"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "New priority for the task"
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "description": "New due date for the task in YYYY-MM-DD format"
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status for the task"
    }
  },
  "required": ["task_id"]
}
```

Output:
```json
{
  "type": "object",
  "properties": {
    "task": {
      "$ref": "#/definitions/taskObject"
    },
    "message": {
      "type": "string",
      "description": "Confirmation message"
    }
  },
  "required": ["task", "message"]
}
```

## Definitions

### Task Object Definition
```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Unique identifier for the task",
      "minimum": 1
    },
    "user_id": {
      "type": "integer",
      "description": "ID of the user who owns the task",
      "minimum": 1
    },
    "title": {
      "type": "string",
      "description": "Title of the task",
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional description of the task",
      "maxLength": 1000
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
    "tags": {
      "type": "array",
      "description": "Tags assigned to the task",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      }
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