# Backend Development Plan – Phase II

## Objective

Build a secure, production-ready FastAPI backend with persistent Neon PostgreSQL storage and strict multi-user isolation via JWT — implementing all 5 Basic Level Todo features as REST API.

## Prerequisites (Already Done or In Progress)

- constitution.md approved and active
- Backend specs ready:
  - `/specs/database/schema.md`
  - `/specs/authentication.md`
  - `/specs/api/rest-endpoints.md`

## Phase II Backend Milestones (In Exact Order)

### 1. Project Setup & Structure

**Responsibility**: orchestrator / full-stack-backend

1. Create `/backend` folder with proper Python project structure:
   - `main.py`
   - `routers/tasks.py`
   - `models/__init__.py`
   - `schemas/__init__.py`
   - `dependencies/auth.py`
   - `database.py` (DB session setup)

2. Add dependency manifest (choose one):
   - `pyproject.toml` **or** `requirements.txt`

3. Add the required Python dependencies:
   - `fastapi`
   - `uvicorn`
   - `sqlmodel`
   - `psycopg2-binary`
   - `python-jose[cryptography]`
   - `passlib[bcrypt]`
   - `python-dotenv`

4. Confirm environment variables are supported:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`

**Dependencies**:
- None

**Deliverables**:
- Backend project skeleton ready for DB/auth/routes wiring

---

### 2. Database Models & Connection

**Responsibility**: database-specialist

1. Implement SQLModel models exactly per `/specs/database/schema.md`:
   - `User` + `Task`
   - FK ownership via `Task.user_id -> User.id` with cascade delete
   - Indexing strategy (user_id and (user_id, completed))

2. Implement database connection using `DATABASE_URL`:
   - Engine/session creation
   - Session lifecycle management

3. Verify database connectivity to Neon:
   - Startup connection check using env var

**Dependencies**:
- Phase 1 structure exists (places to put `database.py` and models)

**Deliverables**:
- DB models + DB session setup + verified connectivity

---

### 3. JWT Authentication & Security Middleware

**Responsibility**: auth-specialist

1. Implement JWT verification dependency per `/specs/authentication.md`:
   - Extract from `Authorization: Bearer <token>`
   - Verify signature using `BETTER_AUTH_SECRET`
   - Enforce algorithm `HS256`
   - Enforce `exp`

2. Extract user identity:
   - `user_id` (integer)
   - `email`

3. Enforce strict user isolation rules:
   - `{user_id}` path parameter must match token `user_id` (403 on mismatch)
   - All task queries must filter by authenticated `user_id`

4. Integrate the dependency with all protected routes (tasks router)

**Dependencies**:
- Phase 1 structure exists (`dependencies/auth.py`)

**Deliverables**:
- A reusable auth dependency that can be attached to every route

---

### 4. Task CRUD API Endpoints

**Responsibility**: full-stack-backend

1. Create tasks router per `/specs/api/rest-endpoints.md`.

2. Implement all endpoints (exact paths):
   - `GET /api/{user_id}/tasks`
   - `POST /api/{user_id}/tasks`
   - `GET /api/{user_id}/tasks/{id}`
   - `PUT /api/{user_id}/tasks/{id}`
   - `DELETE /api/{user_id}/tasks/{id}`
   - `PATCH /api/{user_id}/tasks/{id}/complete`

3. Use Pydantic/SQLModel schemas for request/response:
   - `TaskCreate`, `TaskUpdate`, `TaskOut`

4. Apply strict query filtering:
   - Every read/write must be filtered by authenticated `user_id`

5. Implement error semantics:
   - 401 `{ "error": "unauthorized" }`
   - 403 `{ "error": "user_id_mismatch" }`
   - 404 `{ "error": "not_found" }`

6. Enforce canonical path rules:
   - No trailing slashes; trailing slash returns 404

**Dependencies**:
- Phase 2 DB setup complete
- Phase 3 auth dependency complete

**Deliverables**:
- Tasks router fully functional and secured

---

### 5. Testing & Validation

**Responsibility**: orchestrator + constitution-keeper

1. Manual test all endpoints with:
   - Valid JWT
   - Missing JWT
   - Invalid JWT
   - Expired JWT

2. Verify user isolation:
   - User A cannot list/get/update/delete User B tasks

3. Verify OpenAPI/Swagger UI:
   - `/docs` renders and shows endpoints

4. Run constitution-keeper final review for spec compliance

**Dependencies**:
- Phases 1–4 complete

**Deliverables**:
- Verified behavior and security; compliance gate passed

---

### 6. Documentation & Readiness

1. Update `README.md` with backend run instructions:
   - `uvicorn main:app --reload`

2. Confirm backend is ready for frontend integration:
   - Endpoints stable
   - Auth expectations documented

**Dependencies**:
- Phase 5 complete

**Deliverables**:
- Backend is runnable and consumable by frontend

## Agent Responsibilities Summary

- **database-specialist**: Step 2
- **auth-specialist**: Step 3
- **full-stack-backend**: Steps 1, 4
- **constitution-keeper**: Review after each major step
- **orchestrator**: Coordinate and delegate

## Success Criteria

- All endpoints work with correct user filtering
- Zero cross-user data access
- Runs locally with Neon DB
- Fully spec-driven (no manual code)
- Ready for frontend to consume

## Timeline (Current: January 07, 2026)

Target complete backend by January 10, 2026 to allow time for frontend and final submission (Jan 18).
