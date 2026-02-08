# API Contract: Frontend-Backend Interface for Todo Application

## Overview
This document defines the API contract between the frontend and backend for the multi-user todo application. All endpoints follow the pattern `/api/{user_id}/tasks/*` and require JWT authentication.

## Authentication
All API requests must include a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Error Handling
All error responses follow the format:
```json
{
  "error": "error_message"
}
```

### Standard Error Codes
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User ID in path doesn't match authenticated user ID
- 404 Not Found: Requested resource doesn't exist for authenticated user
- 422 Unprocessable Entity: Invalid request data

## API Endpoints

### List Tasks
```
GET /api/{user_id}/tasks
```

**Description**: Retrieve all tasks for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id (string): The ID of the user whose tasks to retrieve

**Success Response**:
- Code: 200
- Content:
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "user_id": "uuid-string"
  }
]
```

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 500: Internal server error

### Create Task
```
POST /api/{user_id}/tasks
```

**Description**: Create a new task for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`
- Content-Type: application/json

**Path Parameters**:
- user_id (string): The ID of the user creating the task

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

**Success Response**:
- Code: 201
- Content:
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "uuid-string"
}
```

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 422: Invalid request data
- 500: Internal server error

### Get Task
```
GET /api/{user_id}/tasks/{id}
```

**Description**: Retrieve a specific task for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id (string): The ID of the user
- id (string): The ID of the task to retrieve

**Success Response**:
- Code: 200
- Content:
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "uuid-string"
}
```

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 404: Task not found
- 500: Internal server error

### Update Task
```
PUT /api/{user_id}/tasks/{id}
```

**Description**: Update a specific task for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`
- Content-Type: application/json

**Path Parameters**:
- user_id (string): The ID of the user
- id (string): The ID of the task to update

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Success Response**:
- Code: 200
- Content:
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "uuid-string"
}
```

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 404: Task not found
- 422: Invalid request data
- 500: Internal server error

### Delete Task
```
DELETE /api/{user_id}/tasks/{id}
```

**Description**: Delete a specific task for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id (string): The ID of the user
- id (string): The ID of the task to delete

**Success Response**:
- Code: 200
- Content: `{}`

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 404: Task not found
- 500: Internal server error

### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
```

**Description**: Toggle the completion status of a specific task for the specified user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id (string): The ID of the user
- id (string): The ID of the task to toggle

**Success Response**:
- Code: 200
- Content:
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "uuid-string"
}
```

**Error Responses**:
- 401: Unauthorized
- 403: User ID mismatch
- 404: Task not found
- 500: Internal server error

## Client Implementation Requirements

### Headers
- All requests must include `Authorization: Bearer <token>`
- POST and PUT requests must include `Content-Type: application/json`

### URL Construction
- Base URL should be configurable (e.g., via environment variable)
- Construct URLs as `${BASE_URL}/api/${user_id}/tasks${path}`

### Error Handling
- Catch and handle 401, 403, 404 errors appropriately
- Display user-friendly error messages based on response content
- Implement retry logic for 5xx errors if needed

### JWT Token Management
- Store JWT token securely (preferably in httpOnly cookie or secure storage)
- Include token in Authorization header for all API requests
- Handle token expiration and refresh if implemented