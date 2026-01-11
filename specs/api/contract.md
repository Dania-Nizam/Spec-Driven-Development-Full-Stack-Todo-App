# API Contract (Authoritative)

This document is the authoritative API contract referenced by `.specify/memory/constitution.md`.

## Canonical path rules

- No trailing slashes on endpoints.
- All endpoints are under `/api/{user_id}/tasks...`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Error semantics (binding)

- Missing/invalid/expired JWT: **401** `{ "error": "unauthorized" }`
- `{user_id}` path != authenticated JWT user id: **403** `{ "error": "user_id_mismatch" }`
- Task not found for authenticated user: **404** `{ "error": "not_found" }`
