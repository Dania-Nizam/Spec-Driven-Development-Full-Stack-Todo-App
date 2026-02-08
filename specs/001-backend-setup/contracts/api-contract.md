# API Contract: Backend Task Management API

## Overview
This document defines the complete API contract for the multi-user todo application backend, including all endpoints, request/response schemas, authentication requirements, and error handling.

## Base URL
```
https://api.example.com  # Production
http://localhost:8000    # Development
```

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token_here>
```

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Error Responses
All error responses follow the same format:
```json
{
  "error": "error_type"
}
```

### Standard Error Types
- `unauthorized`: 401 - Missing or invalid JWT token
- `user_id_mismatch`: 403 - Path user_id doesn't match JWT user_id
- `not_found`: 404 - Requested resource not found for authenticated user
- `validation_error`: 422 - Request body validation failed

## Data Models

### User Model
```json
{
  "id": 123,
  "email": "user@example.com",
  "created_at": "2023-01-01T10:00:00Z"
}
```

### Task Model
```json
{
  "id": 456,
  "title": "Complete project",
  "description": "Finish the backend implementation",
  "completed": false,
  "user_id": 123,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

### Create Task Request
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

### Update Task Request
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

## Endpoints

### 1. List User Tasks
**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieve all tasks for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user

**Query Parameters**: None

**Request Headers**:
- `Authorization: Bearer <token>`

**Success Response**:
- `200 OK`
```json
[
  {
    "id": 1,
    "title": "Task 1",
    "description": "Description of task 1",
    "completed": false,
    "user_id": 123,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  },
  {
    "id": 2,
    "title": "Task 2",
    "description": "Description of task 2",
    "completed": true,
    "user_id": 123,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T11:00:00Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `404 Not Found`: `{"error": "not_found"}` (if user doesn't exist)

### 2. Create Task
**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new task for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

**Request Headers**:
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Success Response**:
- `201 Created`
```json
{
  "id": 3,
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "user_id": 123,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `422 Validation Error`: `{"error": "validation_error"}`

### 3. Get Task
**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieve a specific task for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user
- `id` (integer): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Success Response**:
- `200 OK`
```json
{
  "id": 5,
  "title": "Specific task",
  "description": "Description of specific task",
  "completed": false,
  "user_id": 123,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `404 Not Found`: `{"error": "not_found"}`

### 4. Update Task
**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update a specific task for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user
- `id` (integer): Task ID

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Request Headers**:
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Success Response**:
- `200 OK`
```json
{
  "id": 7,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "user_id": 123,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `404 Not Found`: `{"error": "not_found"}`
- `422 Validation Error`: `{"error": "validation_error"}`

### 5. Delete Task
**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Delete a specific task for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user
- `id` (integer): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Success Response**:
- `200 OK`
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `404 Not Found`: `{"error": "not_found"}`

### 6. Toggle Task Completion
**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle the completion status of a specific task for the specified user

**Authentication**: Required JWT token

**Path Parameters**:
- `user_id` (integer): User ID matching the authenticated user
- `id` (integer): Task ID

**Request Headers**:
- `Authorization: Bearer <token>`

**Success Response**:
- `200 OK`
```json
{
  "id": 9,
  "title": "Toggle task",
  "description": "Description of toggle task",
  "completed": true,
  "user_id": 123,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: `{"error": "unauthorized"}`
- `403 Forbidden`: `{"error": "user_id_mismatch"}`
- `404 Not Found`: `{"error": "not_found"}`

## Canonical Path Rules

### No Trailing Slashes
- ❌ `GET /api/123/tasks/` - Returns 404
- ✅ `GET /api/123/tasks` - Valid endpoint

### Exact Completion Path
- ❌ `PATCH /api/123/tasks/456/toggle` - Returns 404
- ❌ `PATCH /api/123/tasks/456/completion` - Returns 404
- ✅ `PATCH /api/123/tasks/456/complete` - Valid endpoint

## Security Requirements

### User Isolation
- All endpoints must verify that the path parameter `{user_id}` matches the authenticated user ID from the JWT token
- No user may access, modify, or delete another user's tasks
- Database queries must always be filtered by the authenticated user ID

### JWT Validation
- All endpoints require a valid JWT token
- JWT must be signed with the shared BETTER_AUTH_SECRET
- JWT algorithm must be HS256
- JWT must contain valid `sub` (user_id) and `exp` (expiration) claims

## Performance Requirements

### Response Times
- P95 response time: <200ms for all endpoints
- P99 response time: <500ms for all endpoints

### Concurrency
- Support for 100+ concurrent users
- Proper database connection pooling
- Efficient indexing for user-based queries

## Validation Rules

### Task Creation
- Title is required and cannot be empty
- Description is optional
- Completed defaults to false if not provided

### Task Updates
- At least one field must be provided for update
- Title cannot be empty
- Completed field must be boolean

### Path Validation
- user_id and task id must be valid integers
- user_id must correspond to an existing user
- task id must correspond to an existing task for the specified user