# API Contract: Chatbot Orchestrator for AI-Powered Todo Chatbot

## Overview

This document defines the API contract for the ChatbotOrchestratorAgent system. The API provides a natural language interface to all Todo operations while maintaining strict user isolation through JWT authentication.

## Endpoint: POST /api/{user_id}/chat

### Description
Processes natural language commands from users and orchestrates appropriate todo operations using OpenAI Agents SDK and reusable skills. The endpoint handles authentication, intent parsing, skill execution, and response generation.

### Authentication
- **Required**: JWT token in Authorization header
- **Header**: `Authorization: Bearer <valid-jwt-token>`
- **Validation**: Token must be valid and not expired
- **User Isolation**: `{user_id}` path parameter must match authenticated user ID from JWT

### Request

#### Path Parameters
- `{user_id}` (integer, required): The authenticated user's ID
  - Must match the user ID extracted from the JWT token
  - Range: positive integers only

#### Headers
- `Authorization` (string, required): JWT token with format "Bearer <token>"
- `Content-Type` (string, required): Must be "application/json"

#### Body
```json
{
  "message": "Natural language command to process",
  "session_id": "Optional session identifier for context (UUID format)"
}
```

**Body Field Requirements:**
- `message` (string, required): The natural language command from the user
  - Min length: 1 character
  - Max length: 2000 characters
  - Cannot be empty or whitespace only
- `session_id` (string, optional): Session identifier for maintaining conversation context
  - Format: UUID v4 format if provided
  - Used for conversation history and context awareness

### Response

#### Success Response (200 OK)
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

**Success Response Fields:**
- `response` (string): The chatbot's natural language response
  - Min length: 1 character
  - Max length: 5000 characters
- `session_id` (string): The session identifier (newly created or existing)
  - Format: UUID v4
- `task_id` (integer, optional): ID of task that was created or modified
  - Present only when a specific task operation occurred
- `intent` (string, optional): The classified intent from the user's message
  - Values: "add_task", "delete_task", "update_task", "view_tasks", "mark_complete", "search_tasks", "set_recurring", "other"
- `success` (boolean): Indicates whether the operation was successful
- `timestamp` (string): ISO 8601 formatted timestamp of response generation

#### Error Responses

**401 Unauthorized**
```json
{
  "error": "unauthorized",
  "message": "Invalid or missing JWT token"
}
```

**403 Forbidden**
```json
{
  "error": "user_id_mismatch",
  "message": "The user_id in the path does not match the authenticated user"
}
```

**404 Not Found**
```json
{
  "error": "not_found",
  "message": "User not found or session invalid"
}
```

**422 Unprocessable Entity**
```json
{
  "error": "validation_error",
  "details": [
    {
      "field": "message",
      "message": "Message must be between 1 and 2000 characters"
    }
  ]
}
```

### Example Requests

#### Example 1: Add a new task
```
POST /api/123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task to buy groceries tomorrow",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Example 2: View pending tasks
```
POST /api/123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Show me my pending tasks",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Example 3: Mark task as complete
```
POST /api/123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Mark task 5 as complete",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Example Responses

#### Success Response
```json
{
  "response": "I've added the task 'buy groceries tomorrow' to your list. The task ID is 456.",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": 456,
  "intent": "add_task",
  "success": true,
  "timestamp": "2026-02-02T23:00:00Z"
}
```

#### Error Response (Unauthorized)
```json
{
  "error": "unauthorized",
  "message": "Invalid or missing JWT token"
}
```

### Implementation Requirements

1. **Authentication**: Must validate JWT token and extract user_id
2. **User Isolation**: Must verify that {user_id} path parameter matches authenticated user
3. **Intent Parsing**: Must classify user intent using OpenAI Agents SDK
4. **Skill Execution**: Must execute appropriate skills based on classified intent
5. **Response Generation**: Must generate natural language response
6. **Session Management**: Must maintain conversation context when session_id provided
7. **Error Handling**: Must return appropriate HTTP status codes and error messages

### Performance Requirements

- **Response Time**: <2 seconds for 90% of requests
- **Throughput**: Support 100 concurrent chat sessions
- **Rate Limiting**: Maximum 10 messages per minute per user
- **Resource Usage**: <100MB memory per concurrent session

### Security Requirements

- **Input Sanitization**: All user input must be sanitized before processing
- **No SQL Injection**: All database operations must use parameterized queries
- **No XSS**: All output must be properly escaped
- **JWT Validation**: Tokens must be validated against shared BETTER_AUTH_SECRET
- **User Isolation**: Users cannot access other users' data or sessions