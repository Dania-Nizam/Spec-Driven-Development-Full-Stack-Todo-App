# API Contract: Chat Integration

## Overview

This document defines the API contract between the frontend ChatKit integration and the backend chat endpoint for the AI-powered Todo chatbot.

## Base URL

All endpoints are relative to the application's base URL.

## Authentication

All chat endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

The JWT token must be obtained from Better Auth session and contain the authenticated user ID.

## Endpoints

### POST /api/{user_id}/chat

Send a message to the AI chatbot for processing.

#### Parameters

Path Parameter:
- `user_id` (string, required): The authenticated user's ID, must match the user ID in the JWT token

#### Request Body

```json
{
  "message": "The user's message to send to the chatbot",
  "sessionId": "Optional session identifier for maintaining conversation context"
}
```

**Request Body Validation:**
- `message`: Required, 1-2000 characters
- `sessionId`: Optional, valid UUID format if provided

#### Headers
```
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

#### Response

**Success Response (200 OK):**
```json
{
  "response": "The chatbot's response to the user's message",
  "sessionId": "Session identifier for maintaining conversation context",
  "taskId": "Optional ID of any task created/modified by the message",
  "intent": "Detected intent from the user's message (e.g., 'add_task', 'view_tasks', 'update_task')",
  "success": true
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "error": "unauthorized"
}
```

**403 Forbidden:**
```json
{
  "error": "user_id_mismatch"
}
```

**400 Bad Request:**
```json
{
  "error": "invalid_request",
  "details": "Message is required and must be between 1-2000 characters"
}
```

**500 Internal Server Error:**
```json
{
  "error": "server_error",
  "details": "An unexpected error occurred processing your request"
}
```

## Message Processing

The chat endpoint processes natural language input to perform Todo operations:
- Add tasks: "Add a task to buy groceries"
- View tasks: "Show my pending tasks"
- Update tasks: "Change the due date of task 1 to tomorrow"
- Complete tasks: "Mark task 1 as complete"
- Delete tasks: "Delete task 1"
- Search/filter tasks: "Show me urgent tasks"

## Session Management

The backend maintains conversation context through the sessionId parameter, allowing for contextual responses based on previous interactions.

## Rate Limiting

To prevent abuse, the API implements rate limiting:
- Maximum 10 requests per minute per user
- Excessive requests return 429 Too Many Requests response

## Response Streaming

The endpoint supports server-sent events (SSE) for streaming responses. To enable streaming, include the header:
```
Accept: text/event-stream
```

When streaming is enabled, the response will be sent as a series of events:
```
data: {"chunk": "First part of response"}

data: {"chunk": "Second part of response"}

data: {"done": true, "finalResponse": "Complete response here"}
```

## Security Requirements

- All requests must include a valid JWT token
- The user_id in the path must match the authenticated user ID from the JWT token
- Users cannot access or modify other users' data
- All inputs must be validated and sanitized
- Proper error handling without leaking sensitive information