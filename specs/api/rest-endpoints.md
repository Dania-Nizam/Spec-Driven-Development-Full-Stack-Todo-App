# Backend REST API Endpoints – Task CRUD Operations

**Status**: Draft (backend-only)

## Base Path

All endpoints are under:
- `/api/{user_id}/tasks`

## Authentication + Authorization (Binding)

- All endpoints require a valid JWT:
  - `Authorization: Bearer <token>`
- The authenticated user id derived from JWT **must** match `{user_id}` path parameter.
  - If mismatch: **403** `{ "error": "user_id_mismatch" }`
- If token missing/invalid/expired: **401** `{ "error": "unauthorized" }`

See: `@specs/authentication.md`

## Canonical Path Rules

- **No trailing slashes** are permitted.
- Requests with a trailing slash must return **404**.
- Completion endpoint path must be exactly:
  - `PATCH /api/{user_id}/tasks/{id}/complete`

## Data Scoping / Filtering Rule

All task reads and writes must be constrained by:
- `task.user_id == authenticated_user_id`

> Do not allow callers to set or override `user_id` in request bodies.

## Schemas (Pydantic / SQLModel)

### TaskCreate
Fields:
- `title`: string (required, non-empty)
- `description`: string (optional)

### TaskUpdate
Fields (full update via PUT):
- `title`: string (required, non-empty)
- `description`: string (optional)

> `completed` is not settable through PUT in this contract; completion is controlled by the `/complete` endpoint.

### TaskOut
Fields:
- `id`: integer
- `title`: string
- `description`: string | null
- `completed`: boolean
- `user_id`: integer
- `created_at`: datetime
- `updated_at`: datetime | null

## Endpoints Table (Exact)

| Method | Path                                  | Purpose            | Request Body                          | Response        | Status Codes |
|--------|---------------------------------------|--------------------|---------------------------------------|-----------------|--------------|
| GET    | /api/{user_id}/tasks                  | List user's tasks  | None                                  | List[TaskOut]   | 200          |
| POST   | /api/{user_id}/tasks                  | Create task        | TaskCreate (title, description?)      | TaskOut         | 201          |
| GET    | /api/{user_id}/tasks/{id}             | Get single task    | None                                  | TaskOut         | 200 / 404    |
| PUT    | /api/{user_id}/tasks/{id}             | Full update task   | TaskUpdate                            | TaskOut         | 200 / 404    |
| DELETE | /api/{user_id}/tasks/{id}             | Delete task        | None                                  | {success: true} | 200 / 404    |
| PATCH  | /api/{user_id}/tasks/{id}/complete    | Toggle complete    | None                                  | TaskOut         | 200 / 404    |

## Endpoint Details

### GET `/api/{user_id}/tasks`

Behavior:
- Returns all tasks owned by authenticated user.
- Must not include tasks for any other user.

Response (200):
- JSON array of `TaskOut`.

### POST `/api/{user_id}/tasks`

Behavior:
- Creates a task for the authenticated user.
- `user_id` is derived from JWT; ignore/forbid any `user_id` in input.

Request body:
- `TaskCreate`

Response (201):
- `TaskOut` of created task.

### GET `/api/{user_id}/tasks/{id}`

Behavior:
- Fetch a single task by `id`, **scoped to authenticated user**.

Response:
- 200: `TaskOut`
- 404: `{ "error": "not_found" }` (when id not found for this user)

### PUT `/api/{user_id}/tasks/{id}`

Behavior:
- Full update of a task (title + description), **scoped to authenticated user**.

Request body:
- `TaskUpdate`

Response:
- 200: `TaskOut`
- 404: `{ "error": "not_found" }`

### DELETE `/api/{user_id}/tasks/{id}`

Behavior:
- Deletes a task **scoped to authenticated user**.

Response:
- 200: `{ "success": true }`
- 404: `{ "error": "not_found" }`

### PATCH `/api/{user_id}/tasks/{id}/complete`

Behavior:
- Toggles completion state of the task **scoped to authenticated user**.
- No request body.

Response:
- 200: `TaskOut`
- 404: `{ "error": "not_found" }`

## Error Handling (Global)

- 401 `{ "error": "unauthorized" }` for missing/invalid/expired JWT.
- 403 `{ "error": "user_id_mismatch" }` when path user mismatch.
- 404 `{ "error": "not_found" }` when a task is not found for authenticated user.

## Acceptance Criteria

- [ ] Endpoints exist exactly as listed in the table (paths/methods), with no trailing slashes.
- [ ] JWT required for all endpoints; 401 on missing/invalid.
- [ ] `{user_id}` path mismatch returns 403 `user_id_mismatch`.
- [ ] All task reads/writes are scoped to authenticated user.
- [ ] Correct response bodies for 404 and delete success.
