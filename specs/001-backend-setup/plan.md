# Implementation Plan: Backend API Implementation

**Branch**: `001-backend-spec-manager` | **Date**: 2026-01-07 | **Spec**: /specs/001-backend-spec-manager/spec.md
**Input**: Feature specification from `/specs/001-backend-spec-manager/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure, production-ready FastAPI backend with Neon PostgreSQL storage and strict multi-user isolation via JWT authentication. The backend will provide REST API endpoints for all 5 Basic Level Todo features (Add, Delete, Update, View, Mark Complete) with proper user isolation to ensure no user can access another user's tasks.

## Technical Context

**Language/Version**: Python 3.11+ (required by spec)
**Primary Dependencies**: FastAPI, SQLModel, python-jose, passlib, Neon PostgreSQL driver
**Storage**: Neon Serverless PostgreSQL database (DATABASE_URL)
**Testing**: pytest for backend API testing
**Target Platform**: Linux server environment (cloud deployment)
**Project Type**: Web application backend (REST API)
**Performance Goals**: Efficient per-user queries with proper indexing, support for multiple concurrent users
**Constraints**: Must enforce strict multi-user isolation, JWT verification required for all endpoints, canonical path rules enforced
**Scale/Scope**: Multi-user todo application with data persistence and authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development Compliance
- ✅ Feature specification exists at `/specs/001-backend-spec-manager/spec.md`
- ✅ All code will be generated from approved specs (no manual coding)
- ✅ Backend API requirements clearly defined with exact endpoints
- ✅ Research, data model, and API contracts documented in specs/

### Technology Stack Compliance
- ✅ Using FastAPI for backend (as mandated by constitution)
- ✅ Using SQLModel for ORM (as mandated by constitution)
- ✅ Using Neon Serverless PostgreSQL (as mandated by constitution)
- ✅ Using Better Auth + JWT with shared BETTER_AUTH_SECRET

### Security & User Isolation Compliance
- ✅ All endpoints will be under `/api/{user_id}/tasks/*` (as required)
- ✅ JWT authentication required for all endpoints (as required)
- ✅ User isolation: user_id path parameter must match JWT user_id (as required)
- ✅ Proper error responses: 401 unauthorized, 403 user_id_mismatch, 404 not_found

### API Contract Compliance
- ✅ All 6 required endpoints will be implemented with exact paths:
  - GET `/api/{user_id}/tasks` - List all tasks
  - POST `/api/{user_id}/tasks` - Create a new task
  - GET `/api/{user_id}/tasks/{id}` - Get task details
  - PUT `/api/{user_id}/tasks/{id}` - Update a task
  - DELETE `/api/{user_id}/tasks/{id}` - Delete a task
  - PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion
- ✅ Canonical path rules: no trailing slashes, exact completion path

### Project Structure Compliance
- ✅ Follows monorepo structure with `/backend/` directory
- ✅ Maintains clear separation of concerns (models, schemas, api, database, core)
- ✅ Proper testing structure with dedicated tests/ directory

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI application entry point
├── models/              # SQLModel database models
│   ├── __init__.py
│   ├── user.py          # User model
│   └── task.py          # Task model
├── schemas/             # Pydantic schemas for API
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── api/                 # API routes and endpoints
│   ├── __init__.py
│   ├── deps.py          # Dependencies (JWT verification)
│   └── tasks.py         # Task endpoints
├── database/            # Database setup and session management
│   ├── __init__.py
│   └── session.py
├── core/                # Core configuration
│   ├── __init__.py
│   └── config.py
└── tests/               # Backend API tests
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py     # Authentication tests
    └── test_tasks.py    # Task API tests
```

**Structure Decision**: This is a web application with separate frontend and backend components. The backend will be implemented in the `/backend/` directory using FastAPI with a clear separation of concerns: models for database interaction, schemas for API data validation, API routes for endpoints, and proper dependency management for JWT authentication.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
