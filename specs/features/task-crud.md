# Feature: Task CRUD Operations (Backend)

## Purpose
Implement the 5 Basic Level features (Add, Delete, Update, View, Mark Complete) as secure FastAPI REST API endpoints with persistent storage and strict multi-user isolation.

## Scope
- Backend only (FastAPI + SQLModel)
- All operations on Task model
- Every task belongs to exactly one authenticated user
- No cross-user access allowed

## Dependencies
- Approved specs: /specs/database/schema.md, /specs/authentication.md, /specs/api/rest-endpoints.md
- JWT authentication active
- User model exists

## Functional Requirements

### 1. Create Task (Add Task)
- Endpoint: POST /api/{user_id}/tasks
- Authenticated user_id from JWT must match path {user_id}
- Request Body:
  {
    "title": str (required, min_length=1),
    "description": str | null (optional)
  }
- Behavior:
  - Create new Task with provided data
  - Set user_id = authenticated user
  - Set completed = False
  - Set created_at = now
- Success: 201 Created, return full Task object
- Errors: 400 (validation), 401 (auth)

### 2. List Tasks (View Task List)
- Endpoint: GET /api/{user_id}/tasks
- Auth required, user_id match
- Query Params (optional):
  - completed: bool (filter by completion)
  - search: str (search in title/description)
- Behavior:
  - Return all tasks belonging to authenticated user
  - Order by created_at DESC
- Success: 200 OK, return list of Task objects

### 3. Get Single Task (View Details)
- Endpoint: GET /api/{user_id}/tasks/{task_id}
- Auth required, user_id match
- Behavior:
  - Return task if task.user_id == authenticated user_id
  - Else 404 Not Found
- Success: 200 OK, full Task object

### 4. Update Task
- Endpoint: PUT /api/{user_id}/tasks/{task_id}
- Auth required, ownership check
- Request Body:
  {
    "title": str (optional),
    "description": str | null (optional)
  }
- Behavior:
  - Update only provided fields
  - Update updated_at = now
  - Ownership required
- Success: 200 OK, updated Task
- Errors: 404 (not found or not owner), 400

### 5. Delete Task
- Endpoint: DELETE /api/{user_id}/tasks/{task_id}
- Auth required, ownership check
- Behavior:
  - Soft or hard delete (hard preferred with CASCADE)
  - Only if task belongs to user
- Success: 200 OK, { "success": true }
- Errors: 404

### 6. Mark as Complete (Toggle)
- Endpoint: PATCH /api/{user_id}/tasks/{task_id}/complete
- Auth required, ownership check
- Behavior:
  - Toggle task.completed field
  - Update updated_at
- Success: 200 OK, updated Task

## Non-Functional Requirements
- All queries filtered by user_id from JWT
- Proper HTTP status codes
- Pydantic models for request/response
- Error responses with clear messages
- Async support recommended
- Logging for create/update/delete

## Response Schema Example (TaskOut)
{
  "id": int,
  "title": str,
  "description": str | null,
  "completed": bool,
  "user_id": int,
  "created_at": datetime,
  "updated_at": datetime | null
}

## Security Rules (Mandatory)
- Every endpoint must call JWT dependency
- Path user_id MUST equal JWT user_id
- Database queries MUST include WHERE user_id = current_user.id
- 401 if no/invalid token
- 404 if task not found OR not owned by user