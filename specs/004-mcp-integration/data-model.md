# Data Model: MCP Integration for Todo Chatbot

**Feature**: MCP Integration (001-mcp-integration)
**Date**: 2026-02-03
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

## Overview

This document defines the data models and entities required for the Model Context Protocol (MCP) integration with the Todo Chatbot. The models extend the existing Phase II todo system to support MCP-specific concepts while maintaining compatibility with existing functionality.

## Core Entities

### MCP Session
Represents a stateful conversation session with the MCP server.

**Fields**:
- `session_id`: string (UUID) - Unique identifier for the session
- `user_id`: integer - Reference to the authenticated user
- `created_at`: datetime - Timestamp when session was created
- `last_activity_at`: datetime - Timestamp of last activity
- `expires_at`: datetime - Session expiration time
- `context_data`: dict - Serialized conversation context
- `is_active`: boolean - Whether the session is currently active

**Relationships**:
- Belongs to User (many-to-one)
- Contains multiple MCP Tool Calls (one-to-many)

**Validation Rules**:
- session_id must be a valid UUID
- user_id must reference an existing user
- expires_at must be after created_at
- is_active defaults to True

### MCP Tool Call
Represents an individual tool call within an MCP session.

**Fields**:
- `call_id`: string (UUID) - Unique identifier for the tool call
- `session_id`: string - Reference to the parent session
- `tool_name`: string - Name of the tool being called
- `input_parameters`: dict - Parameters passed to the tool
- `result`: dict - Result returned by the tool
- `error`: string - Error message if the call failed
- `timestamp`: datetime - When the call was made
- `status`: string (enum: pending, success, error) - Status of the call

**Relationships**:
- Belongs to MCP Session (many-to-one)

**Validation Rules**:
- call_id must be a valid UUID
- session_id must reference an active session
- tool_name must be a valid registered tool
- status must be one of the allowed values

### MCP Tool Definition
Defines the schema and behavior of an MCP tool.

**Fields**:
- `tool_id`: string - Unique identifier for the tool
- `name`: string - Display name of the tool
- `description`: string - Human-readable description
- `input_schema`: dict - JSON Schema for input parameters
- `output_schema`: dict - JSON Schema for output
- `authentication_required`: boolean - Whether authentication is required
- `is_active`: boolean - Whether the tool is enabled
- `version`: string - Version of the tool definition

**Validation Rules**:
- tool_id must be unique
- input_schema must be a valid JSON Schema
- output_schema must be a valid JSON Schema
- authentication_required defaults to True

### MCP Conversation Context
Maintains state across multiple tool calls in a conversation.

**Fields**:
- `session_id`: string - Reference to the session
- `context_id`: string (UUID) - Unique identifier for this context
- `previous_tasks_referenced`: list of integers - Task IDs referenced in conversation
- `current_topic`: string - Current topic of conversation
- `pending_clarifications`: list of strings - Clarifications needed from user
- `conversation_history`: list of dicts - History of conversation turns
- `last_task_action`: string - Last action taken on a task
- `last_task_id`: integer - ID of the last referenced task

**Relationships**:
- Belongs to MCP Session (one-to-one)

**Validation Rules**:
- session_id must reference an existing session
- context_id must be a valid UUID
- previous_tasks_referenced must reference existing tasks

## State Transitions

### MCP Session Lifecycle
- **Created**: Session initiated with user authentication
- **Active**: Session is accepting tool calls
- **Paused**: Session temporarily inactive (timeout)
- **Expired**: Session has exceeded TTL
- **Terminated**: Session explicitly closed by user

### MCP Tool Call Status
- **Pending**: Tool call initiated but not yet processed
- **Success**: Tool call completed successfully
- **Error**: Tool call failed with an error

## Relationships

```
User (1) <---> (Many) MCP Session <---> (Many) MCP Tool Call
MCP Session <---> (One) MCP Conversation Context
MCP Tool Definition (Many) <---> (Many) MCP Tool Call
```

## Indexes

- MCP Session: Index on (user_id, session_id, is_active)
- MCP Tool Call: Index on (session_id, timestamp, status)
- MCP Tool Definition: Index on (tool_id, is_active, version)

## Constraints

### User Isolation
- All MCP operations must be scoped to the authenticated user
- Sessions can only access tasks belonging to the user
- Tool calls must validate user permissions before execution

### Security Constraints
- All tools require JWT authentication validation
- Session expiration prevents unauthorized access
- Input validation prevents injection attacks

### Data Integrity
- Referential integrity maintained between related entities
- Foreign key constraints enforced by database
- Unique constraints on identifiers

## State Management

### Session State Management
- Automatic expiration of idle sessions
- Context cleanup when session terminates
- Concurrent session handling with thread safety

### Conversation Context Persistence
- Temporary storage during active sessions
- Serialization format for context transfer
- Cleanup of expired context data

## Validation Rules

### MCP Tool Definition Validation
- Schema validation for input/output schemas
- Authentication requirement enforcement
- Tool name uniqueness within namespace

### Session Validation
- Active session check before tool execution
- User authentication validation
- Session timeout enforcement

### Tool Call Validation
- Parameter validation against schema
- Permission validation for user data access
- Error response validation for user safety