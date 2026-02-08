"""
Data models for the MCP (Model Context Protocol) server.

This module defines the data structures used by the MCP server.
"""
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class MCPServerHealthResponse(BaseModel):
    """
    Response model for the health check endpoint.
    """
    status: str
    service: str
    version: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "mcp-server",
                "version": "1.0.0",
                "timestamp": "2026-02-03T10:00:00Z"
            }
        }


class MCPToolDefinition(BaseModel):
    """
    Model for an MCP tool definition.
    """
    name: str
    description: str
    parameters: Dict[str, Any]

    @validator('name')
    def validate_name(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Tool name must be a non-empty string')
        if len(v) > 100:
            raise ValueError('Tool name must be less than 100 characters')
        # Allow only alphanumeric, underscore, and hyphen
        import re
        if not re.match(r'^[a-z0-9_-]+$', v):
            raise ValueError('Tool name can only contain lowercase letters, numbers, underscores, and hyphens')
        return v.lower()

    @validator('description')
    def validate_description(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Description must be a non-empty string')
        if len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v

    class Config:
        json_schema_extra = {
            "example": {
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
                        }
                    },
                    "required": ["title"]
                }
            }
        }


class MCPToolCallRequest(BaseModel):
    """
    Request model for calling an MCP tool.
    """
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: datetime
    data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "request_id": "550e8400-e29b-41d4-a716-446655440001",
                "timestamp": "2026-02-03T10:00:00Z",
                "data": {
                    "title": "Buy groceries",
                    "priority": "high"
                }
            }
        }


class MCPToolCallResponse(BaseModel):
    """
    Response model for an MCP tool call.
    """
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    session_id: str
    request_id: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "result": {
                    "task": {
                        "id": 123,
                        "title": "Buy groceries",
                        "priority": "high"
                    },
                    "message": "Task created successfully"
                },
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "request_id": "550e8400-e29b-41d4-a716-446655440001",
                "timestamp": "2026-02-03T10:00:00Z"
            }
        }


class MCPErrorDetail(BaseModel):
    """
    Model for detailed error information.
    """
    code: str
    message: str
    details: Optional[List[Dict[str, Any]]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": "validation_error",
                "message": "Invalid parameters provided",
                "details": [
                    {
                        "field": "title",
                        "issue": "required"
                    }
                ]
            }
        }


class MCPSessionInfo(BaseModel):
    """
    Model for MCP session information.
    """
    session_id: str
    user_id: int
    created_at: datetime
    last_activity_at: datetime
    expires_at: datetime
    is_active: bool
    context_summary: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "created_at": "2026-02-03T09:00:00Z",
                "last_activity_at": "2026-02-03T10:00:00Z",
                "expires_at": "2026-02-03T10:30:00Z",
                "is_active": True,
                "context_summary": {
                    "previous_tasks_referenced": [1, 2, 3],
                    "current_topic": "task management",
                    "pending_clarifications": []
                }
            }
        }


class MCPTaskStatus(Enum):
    """
    Enum for task status values.
    """
    PENDING = "pending"
    COMPLETED = "completed"
    ALL = "all"


class MCPTaskPriority(Enum):
    """
    Enum for task priority values.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MCPTask(BaseModel):
    """
    Model for a task in the MCP system.
    """
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    priority: MCPTaskPriority = MCPTaskPriority.MEDIUM
    due_date: Optional[str] = None  # Format: YYYY-MM-DD
    completed: bool = False
    tags: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "user_id": 123,
                "title": "Buy groceries",
                "description": "Milk, bread, eggs",
                "priority": "high",
                "due_date": "2026-02-05",
                "completed": False,
                "tags": ["shopping", "urgent"],
                "created_at": "2026-02-03T09:00:00Z",
                "updated_at": "2026-02-03T09:00:00Z"
            }
        }


class MCPToolExecutionResult(BaseModel):
    """
    Model for the result of a tool execution.
    """
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    tool_name: str
    execution_time: float  # in seconds

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "result": {"task_id": 123, "status": "created"},
                "tool_name": "add_task",
                "execution_time": 0.123
            }
        }


class MCPListToolsResponse(BaseModel):
    """
    Response model for listing available tools.
    """
    tools: List[MCPToolDefinition]

    class Config:
        json_schema_extra = {
            "example": {
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
                                }
                            },
                            "required": ["title"]
                        }
                    }
                ]
            }
        }


class MCPToolStats(BaseModel):
    """
    Model for tool execution statistics.
    """
    calls: int
    successes: int
    failures: int
    total_duration: float
    avg_duration: float
    last_called: Optional[datetime]

    class Config:
        json_schema_extra = {
            "example": {
                "calls": 10,
                "successes": 8,
                "failures": 2,
                "total_duration": 0.5,
                "avg_duration": 0.0625,
                "last_called": "2026-02-03T10:00:00Z"
            }
        }


class MCPTaskFilter(BaseModel):
    """
    Model for task filtering parameters.
    """
    status: Optional[MCPTaskStatus] = MCPTaskStatus.ALL
    priority: Optional[MCPTaskPriority] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"

    class Config:
        json_schema_extra = {
            "example": {
                "status": "pending",
                "priority": "high",
                "limit": 10,
                "offset": 0,
                "sort_by": "created_at",
                "sort_order": "desc"
            }
        }


class MCPConversationTurn(BaseModel):
    """
    Model for a conversation turn in the context.
    """
    turn_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: str  # ISO format

    @validator('role')
    def validate_role(cls, v):
        if v not in ["user", "assistant"]:
            raise ValueError('Role must be either "user" or "assistant"')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "turn_id": "550e8400-e29b-41d4-a716-446655440002",
                "role": "user",
                "content": "Add a task to buy groceries",
                "timestamp": "2026-02-03T10:00:00Z"
            }
        }


class MCPContextData(BaseModel):
    """
    Model for conversation context data.
    """
    context_id: str
    session_id: str
    user_id: Optional[int]
    created_at: datetime
    last_updated_at: datetime
    expires_at: datetime
    previous_tasks_referenced: List[int]
    current_topic: str
    pending_clarifications: List[str]
    conversation_history: List[MCPConversationTurn]
    last_task_action: str
    last_task_id: Optional[int]
    custom_data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "context_id": "550e8400-e29b-41d4-a716-446655440003",
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "created_at": "2026-02-03T09:00:00Z",
                "last_updated_at": "2026-02-03T10:00:00Z",
                "expires_at": "2026-02-03T11:00:00Z",
                "previous_tasks_referenced": [1, 2, 3],
                "current_topic": "task management",
                "pending_clarifications": [],
                "conversation_history": [
                    {
                        "turn_id": "550e8400-e29b-41d4-a716-446655440002",
                        "role": "user",
                        "content": "Add a task to buy groceries",
                        "timestamp": "2026-02-03T10:00:00Z"
                    }
                ],
                "last_task_action": "add",
                "last_task_id": 123,
                "custom_data": {}
            }
        }