# Backend API Implementation – Phase II

**Status**: Draft | **Priority**: High | **Type**: Backend Implementation

## Summary

Build a secure, production-ready FastAPI backend with persistent Neon PostgreSQL storage and strict multi-user isolation via JWT — implementing all 5 Basic Level Todo features as REST API.

## Background

This is Phase II of the Hackathon II project. The backend will provide persistent storage for multi-user todo tasks, with JWT-based authentication and strict per-user data isolation to ensure no user can ever access another user's tasks.

## Requirements

### Functional Requirements

**FR-1: Database Models**
- Implement User and Task SQLModel models with proper relationships
- User model: id (PK, integer), email (unique, indexed), created_at
- Task model: id (PK, integer), title (required), description (optional), completed (default False), user_id (FK to User with CASCADE), created_at, updated_at

**FR-2: Authentication**
- Implement JWT verification using shared BETTER_AUTH_SECRET
- Accept only HS256 algorithm
- Validate JWT signature and expiration (exp claim)
- Extract user_id (integer) and email from JWT payload
- Return 401 {error: "unauthorized"} for missing/invalid/expired tokens

**FR-3: User Isolation**
- All endpoints must match {user_id} path parameter with JWT user_id
- Return 403 {error: "user_id_mismatch"} on mismatch
- All task queries must be filtered by authenticated user_id
- No cross-user data access allowed

**FR-4: REST API Endpoints**
Implement the following endpoints under `/api/{user_id}/tasks`:
- GET `/api/{user_id}/tasks` - List user's tasks (200: List[TaskOut])
- POST `/api/{user_id}/tasks` - Create task (201: TaskOut)
- GET `/api/{user_id}/tasks/{id}` - Get single task (200/404)
- PUT `/api/{user_id}/tasks/{id}` - Full update (200/404)
- DELETE `/api/{user_id}/tasks/{id}` - Delete task (200/404)
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion (200/404)

**FR-5: Canonical Path Rules**
- No trailing slashes allowed (return 404 if present)
- Completion endpoint must be exactly `PATCH /api/{user_id}/tasks/{id}/complete`

### Non-Functional Requirements

**NFR-1: Security**
- All endpoints require JWT authentication
- Zero cross-user data leakage
- Proper error responses with consistent JSON format

**NFR-2: Performance**
- Database indexes on user_id and (user_id, completed)
- Support efficient per-user queries

**NFR-3: Reliability**
- Cascade delete: deleting a User deletes all their tasks
- Proper error handling and validation

## Dependencies

- Neon Serverless PostgreSQL database (DATABASE_URL)
- Shared BETTER_AUTH_SECRET for JWT verification
- Backend specs completed (@specs/database/schema.md, @specs/authentication.md, @specs/api/rest-endpoints.md)

## Constraints

- Must follow Constitution (spec-driven development, no manual coding)
- Must use exact API paths and error responses as specified
- Must use FastAPI, SQLModel, python-jose, passlib
- Python 3.11+ required

## Acceptance Criteria

- [ ] Backend project structure exists with main.py, routers, models, schemas, dependencies
- [ ] User and Task SQLModel models match schema spec exactly
- [ ] JWT verification dependency extracts user_id and email correctly
- [ ] All 6 REST endpoints exist at exact paths specified
- [ ] All endpoints enforce JWT authentication (401 on invalid)
- [ ] All endpoints enforce user_id matching (403 on mismatch)
- [ ] All task queries are scoped to authenticated user_id
- [ ] Database connectivity verified to Neon
- [ ] OpenAPI/Swagger UI accessible at /docs
- [ ] Constitution compliance verified

## Related Specs

- Database Schema: @specs/database/schema.md
- Authentication: @specs/authentication.md
- REST Endpoints: @specs/api/rest-endpoints.md
- Backend Plan: @specs/plan-backend.md
- Constitution: @/.specify/memory/constitution.md
