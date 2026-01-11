# Backend Database Schema – SQLModel Models for User and Task

**Status**: Draft (backend-only)

## Purpose

Provide persistent multi-user storage for the Phase II Todo application using **Neon Serverless PostgreSQL**, with **strict per-user ownership** of tasks.

Key outcomes:
- Every `Task` belongs to exactly one `User`.
- It must be structurally difficult/impossible to create “orphan tasks”.
- Queries must efficiently filter tasks by `user_id` for strict multi-tenant isolation.

## Connection

- Database engine: PostgreSQL (Neon Serverless)
- Environment variable:
  - `DATABASE_URL`: SQLAlchemy/SQLModel compatible Postgres connection string.

## Models (SQLModel)

> Naming: models are described as `User` and `Task`.
> IDs are **integers** (primary keys).

### User

**Table**: `user`

Fields:
- `id`: `Integer`, **Primary Key**, auto-increment
  - This `id` must match the `user_id` claim in Better Auth JWTs.
- `email`: `str`, **unique**, **indexed**, required
- `created_at`: `datetime`, required

Notes:
- Passwords are managed by Better Auth; backend does **not** store or validate passwords.
- The `User` table exists as a local identity/profile record required for FK ownership of tasks.
- How user rows are created:
  - On first authenticated request for a given JWT `user_id`, backend may create the `User` row if missing (upsert behavior). (Implementation detail; acceptable as long as it preserves unique email + id mapping.)
  - Alternatively, user rows can be provisioned during sign-up flow (outside this backend-only scope).

Constraints:
- `email` must be unique.

Recommended indexes:
- Unique index on `email`.

### Task

**Table**: `task`

Fields:
- `id`: `Integer`, **Primary Key**, auto-increment
- `title`: `str`, **required**
- `description`: `str`, optional/nullable
- `completed`: `bool`, default `False`
- `user_id`: `Integer`, **required**, **Foreign Key** to `User.id` with `ondelete="CASCADE"`
  - This must equal the authenticated JWT `user_id` for all task operations.
- `created_at`: `datetime`, required
- `updated_at`: `datetime`, optional/nullable

Constraints:
- `user_id` is **NOT NULL**.
- `user_id` references an existing `User.id`.
- When a `User` is deleted, all tasks owned by that user are deleted (cascade).

Recommended indexes:
- Index on `user_id`
- Composite index on `(user_id, completed)` (supports fast filtering of user tasks by completion)

## Relationships

- One-to-many:
  - `User` **has many** `Task`
- Many-to-one:
  - `Task` **belongs to** one `User`

Behavioral expectations:
- Relationship definitions should support convenient ORM navigation (`user.tasks`, `task.user`) without breaking isolation.
- Ownership enforcement must still be done at query level in the API layer (see @specs/authentication.md and @specs/api/rest-endpoints.md).

## Ownership / Tenant Isolation Guarantees

- Every persisted `Task` row must include a valid `user_id`.
- The backend must never query tasks without scoping to the authenticated `user_id`.

## Best Practices

- Always query tasks using `WHERE task.user_id = :authenticated_user_id`.
- Prefer indexes that match query patterns:
  - List tasks by user
  - Filter tasks by completed status for a user
- Use `created_at` as immutable creation timestamp.
- Update `updated_at` on task changes (title/description/completed).

## Acceptance Criteria

- [ ] User table exists with `id`, unique indexed `email`, `created_at` (password not stored server-side).
- [ ] Task table exists with `id`, `title`, optional `description`, `completed` default false, `user_id` NOT NULL FK to user with cascade delete, `created_at`, optional `updated_at`.
- [ ] Indexes exist for efficient per-user queries (at minimum `user_id`; ideally `(user_id, completed)` as well).
- [ ] No task can exist without a valid owner (`user_id`).
