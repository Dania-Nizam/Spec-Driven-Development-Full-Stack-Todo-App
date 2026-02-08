# Data Model: Chatbot Orchestrator for AI-Powered Todo Chatbot

## Overview

This document defines the data entities for the ChatbotOrchestratorAgent system. The entities are designed to support natural language processing, conversation context, and integration with existing Phase II todo operations while maintaining user isolation and security requirements.

## Key Entities

### ChatMessage
**Description**: Represents a message in the conversation with content, user_id, timestamp, and processing status

**Fields**:
- `content` (str, required): The natural language message from the user or bot (1-2000 characters)
- `user_id` (int, required): The authenticated user ID (matches JWT claim)
- `timestamp` (datetime, required): When the message was sent/received
- `sender_type` (str, required): Who sent the message ('user', 'bot')
- `session_id` (str, optional): Session identifier for conversation context
- `processing_status` (str, required): Status of message processing ('received', 'processing', 'processed', 'error')

**Validation Rules**:
- `content` must be 1-2000 characters
- `user_id` must match authenticated user from JWT
- `sender_type` must be one of ['user', 'bot']
- `processing_status` must be one of ['received', 'processing', 'processed', 'error']
- `session_id` follows UUID format if provided

### ConversationContext
**Description**: Maintains the context of a conversation including recent tasks referenced for follow-up operations

**Fields**:
- `session_id` (str, required): Unique identifier for the conversation session (UUID)
- `user_id` (int, required): The authenticated user ID
- `recent_tasks` (list[int], optional): List of recent task IDs referenced in conversation
- `last_intent` (str, optional): Last processed intent from user message
- `context_data` (dict, optional): Additional context for follow-up operations
- `created_at` (datetime, required): When the context was created
- `updated_at` (datetime, required): When the context was last updated

**Validation Rules**:
- `session_id` must follow UUID format
- `user_id` must match authenticated user from JWT
- `recent_tasks` contains valid task IDs for the user
- `last_intent` must be a valid intent type
- `created_at` defaults to current time
- `updated_at` updates on each modification

### AgentTool
**Description**: Represents a registered skill/tool that the orchestrator agent can call to perform specific actions

**Fields**:
- `tool_id` (str, required): Unique identifier for the tool (snake_case format)
- `tool_name` (str, required): Display name of the tool
- `description` (str, required): Description of what the tool does
- `parameters` (dict, required): JSON schema defining the parameters the tool accepts
- `handler_function` (str, required): Name of the function that handles the tool call
- `is_active` (bool, required): Whether the tool is currently available for use

**Validation Rules**:
- `tool_id` must be unique and follow snake_case format
- `parameters` must be a valid JSON schema
- `handler_function` must correspond to an existing function
- `is_active` defaults to True

### ChatRequest
**Description**: Represents the input from the frontend chat interface to the backend orchestrator

**Fields**:
- `message` (str, required): The user's natural language input (1-2000 characters)
- `session_id` (str, optional): Session identifier for maintaining conversation context
- `user_id` (int, required): Authenticated user ID from JWT
- `timestamp` (datetime, required): When the request was received

**Validation Rules**:
- `message` must be 1-2000 characters
- `session_id` must be valid UUID format if provided
- `user_id` must match authenticated user from JWT
- `timestamp` defaults to current time

### ChatResponse
**Description**: Represents the response from the backend orchestrator to the frontend

**Fields**:
- `response` (str, required): The chatbot's response to the user's message (1-5000 characters)
- `session_id` (str, required): Session identifier for maintaining conversation context
- `task_id` (int, optional): ID of any task created/modified by the message
- `intent` (str, optional): Detected intent from the user's message (e.g., 'add_task', 'view_tasks', 'update_task')
- `success` (bool, required): Indicates whether the operation was successful
- `timestamp` (datetime, required): When the response was generated

**Validation Rules**:
- `response` must be 1-5000 characters
- `session_id` must be valid UUID format
- `task_id` must be valid if provided
- `intent` must be one of predefined values if provided
- `success` defaults to True
- `timestamp` defaults to current time

## State Transitions

### ChatMessage Processing States
1. `received`: Message received, JWT validated
2. `processing`: NLP parsing and intent classification
3. `executing`: Skills being executed
4. `generating`: Response being composed
5. `processed`: Response delivered to user
6. `error`: Processing failed at any stage

### ConversationContext Lifecycle
- Created when a new conversation session starts
- Updated with each new message and referenced tasks
- Maintained for duration of conversation session
- Archived when session ends or times out

## API Request/Response Models

### POST /api/{user_id}/chat Request Model
```json
{
  "message": "Natural language command to process",
  "session_id": "Optional session identifier for context (UUID format)"
}
```

**Validation**:
- `message` required, 1-2000 characters
- `session_id` optional, UUID format if provided
- `{user_id}` path parameter must match authenticated user ID from JWT

### POST /api/{user_id}/chat Response Model
```json
{
  "response": "Natural language response from the chatbot",
  "session_id": "Session identifier (UUID format)",
  "task_id": "Optional ID of task created/modified",
  "intent": "Detected intent from user message",
  "success": "Boolean indicating operation success",
  "timestamp": "ISO 8601 formatted timestamp"
}
```

**Validation**:
- `response` required, 1-5000 characters
- `session_id` required, UUID format
- `success` required, boolean
- `timestamp` in ISO 8601 format

## Relationship Diagram

```
User (Phase II) --(1 to many)--> ConversationContext --(1 to many)--> ChatMessage
ChatRequest --(1 to 1)--> ChatResponse
ConversationContext --(1 to many)--> AgentTool (referenced)
```

## Security Considerations

1. **User Isolation**: All entities must validate user_id against JWT claims
2. **Data Integrity**: Chat messages cannot be modified after creation
3. **Access Control**: Users can only access their own conversations and messages
4. **Audit Trail**: All operations are timestamped for security monitoring

## Performance Considerations

1. **Indexing**: ChatMessage table should be indexed by user_id and timestamp
2. **Partitioning**: Consider time-based partitioning for ChatMessage table
3. **Caching**: ConversationContext may benefit from caching
4. **Pagination**: ChatMessage retrieval should support pagination for long conversations