---
id: 0006
title: Generate backend specs
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: danianizam
command: /sp.specify
labels: ["spec","backend","api","database","auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/d/todo-app/specs/database/schema.md
 - /mnt/d/todo-app/specs/authentication.md
 - /mnt/d/todo-app/specs/api/rest-endpoints.md
tests:
 - none
---

## Prompt

You are the spec-manager subagent.

Task: Generate ONLY the backend-related specifications for Phase II (Full-Stack Web Application) of Hackathon II.

Focus exclusively on backend: FastAPI REST API, SQLModel database schema, and JWT authentication integration with strict user isolation.

Create these three Markdown specs with full detail so that database-specialist, auth-specialist, and full-stack-backend agents can implement perfectly.

Use spec-writer skill for clear, structured, implementable content.

After generating each spec's content, IMMEDIATELY write it as an actual file on disk in the /specs folder (create the file if needed).

1. File: /specs/database/schema.md
   Title: Backend Database Schema – SQLModel Models for User and Task
   Sections:
   - Purpose: Persistent multi-user storage in Neon Serverless PostgreSQL with strict ownership
   - Connection: DATABASE_URL env var
   - Models Detail:
     - User:
       - id: Integer (PrimaryKey)
       - email: str (unique, indexed)
       - hashed_password: str
       - created_at: datetime
     - Task:
       - id: Integer (PrimaryKey)
       - title: str (required)
       - description: str (optional)
       - completed: bool (default: False)
       - user_id: Integer (ForeignKey to User.id, required, ondelete="CASCADE")
       - created_at: datetime
       - updated_at: datetime (optional)
   - Relationships: User has many Tasks; Task belongs to one User
   - Constraints: Every Task must have valid user_id — no orphan tasks
   - Best Practices: Indexes on user_id and completed

2. File: /specs/authentication.md
   Title: Backend Authentication – Better Auth JWT Integration & User Isolation
   Sections:
   - Purpose: Stateless, secure auth with zero cross-user access
   - Shared Secret: BETTER_AUTH_SECRET env var (same as frontend)
   - JWT Payload: user_id, email, exp
   - Verification Flow:
     - Extract token from Authorization: Bearer <token>
     - Verify signature and expiration
     - Extract user_id from payload
     - Compare with {user_id} in path — must match exactly
     - Inject current_user into dependency
   - Error Handling: 401 Unauthorized for invalid/missing/expired/mismatch token
   - Security Rules: All queries MUST filter by authenticated user_id

3. File: /specs/api/rest-endpoints.md
   Title: Backend REST API Endpoints – Task CRUD Operations
   Sections:
   - Base Path: /api/{user_id}/tasks
   - All endpoints require valid JWT and user_id match
   - Use Pydantic schemas for request/response
   - Endpoints Table (Exact from document):
     | Method | Path                            | Purpose                  | Request Body                  | Response             | Status Codes |
     |--------|---------------------------------|--------------------------|-------------------------------|----------------------|--------------|
     | GET    | /api/{user_id}/tasks            | List user's tasks        | None                          | List[TaskOut]        | 200          |
     | POST   | /api/{user_id}/tasks            | Create task              | TaskCreate (title, description?) | TaskOut           | 201          |
     | GET    | /api/{user_id}/tasks/{task_id}  | Get single task          | None                          | TaskOut              | 200/404      |
     | PUT    | /api/{user_id}/tasks/{task_id}  | Full update task         | TaskUpdate                    | TaskOut              | 200/404      |
     | DELETE | /api/{user_id}/tasks/{task_id}  | Delete task              | None                          | {success: true}      | 200/404      |
     | PATCH  | /api/{user_id}/tasks/{task_id}/complete | Toggle complete   | None                          | TaskOut              | 200/404      |
   - Filtering: Always WHERE user_id = authenticated_user_id
   - Error Handling: Proper HTTP exceptions

Workflow:
1. Generate detailed content for each spec.
2. After each spec, write the full content to the exact file path on disk.
3. Confirm file creation.

Final Response:
"Backend-only specifications generated and saved to disk:
- /specs/database/schema.md
- /specs/authentication.md
- /specs/api/rest-endpoints.md

Backend specs ready for review by constitution-keeper and implementation by backend agents."

## Response snapshot

- Created backend-only specs and wrote them to disk:
  - `/specs/database/schema.md` (User/Task SQLModel schema, relationships, constraints, indexes)
  - `/specs/authentication.md` (Better Auth JWT verification flow + strict path/user match)
  - `/specs/api/rest-endpoints.md` (exact CRUD + complete endpoints table + error semantics)

## Outcome

- ✅ Impact: Backend specification surface is now documented for DB, auth, and REST API with strict user isolation.
- 🧪 Tests: none
- 📁 Files: 3 new spec files created under `/specs/...`.
- 🔁 Next prompts: Run constitution-keeper review, then generate backend implementation from these specs.
- 🧠 Reflection: Specs were kept aligned with the existing `specs/api/contract.md` and constitution endpoint/error rules.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add a spec lint/validation step (grep + structured checks) before code generation.
