# Backend Authentication – Better Auth JWT Integration & User Isolation

**Status**: Draft (backend-only)

## Purpose

Provide **stateless JWT-based authentication** for the FastAPI backend such that:
- Requests are authenticated via a JWT issued by Better Auth (frontend).
- The backend enforces **zero cross-user access** via strict user isolation.
- Every API request must be authorized both by:
  1) a valid JWT, and
  2) `{user_id}` in the URL matching the authenticated user.

## Shared Secret

- Environment variable: `BETTER_AUTH_SECRET`
  - This **must** be the same secret used by the frontend Better Auth configuration.
  - This secret is used to verify JWT signature.

## JWT Expectations

### Transport

- Client sends token in header:
  - `Authorization: Bearer <token>`

### Required payload claims

JWT payload must include:
- `user_id` (**integer**)
  - Canonical type is integer to match DB (`User.id`).
- `email` (string)
- `exp` (expiration timestamp)

Optional claims (if present, backend does **not** require them):
- `iss`, `aud`, `sub`

> Note: The backend treats `user_id` as the primary subject for authorization. Email is informational.

### Accepted algorithms / header expectations

- Backend must accept only HS256 tokens verified with `BETTER_AUTH_SECRET`.
- If JWT `alg` is missing or not `HS256`, treat token as invalid.

### Issuer / audience validation

- Backend does **not** validate `iss` or `aud` (Better Auth issuer/audience values are not pinned in this repo).
- Signature + expiration are the required checks.

## Verification Flow (Backend)

For every request to `/api/{user_id}/tasks...`:

1. **Extract token**
   - Read `Authorization` header.
   - Expect `Bearer <token>` format.

2. **Verify token**
   - Verify JWT signature using `BETTER_AUTH_SECRET` and restrict to algorithm `HS256`.
   - Verify token is not expired (`exp`).

3. **Extract identity**
   - Extract `user_id` and `email` from payload.

4. **Enforce path/user match**
   - Compare `{user_id}` path parameter with JWT payload `user_id`.
   - They must match **exactly** as integers (no string-based alternative mapping).
   - If payload `user_id` is missing or not an integer, treat as invalid token (401).
   - If path/user mismatch: 403.

5. **Dependency injection**
   - Provide a dependency (e.g., `get_current_user`) that returns a `current_user` object containing at minimum:
     - `user_id`
     - `email`

6. **Query scoping rule**
   - All database reads/writes for tasks must be scoped to `current_user.user_id`.

## Error Handling

### Unauthorized (authentication failure)
Return **401 Unauthorized** when any of these occur:
- Missing `Authorization` header
- Malformed `Authorization` header (not `Bearer <token>`)
- JWT signature invalid
- JWT expired
- Required claims missing (`user_id`, `exp`)

Response body:
```json
{ "error": "unauthorized" }
```

### Forbidden (user mismatch)
Return **403 Forbidden** when:
- JWT is valid, but `{user_id}` in the path does not match JWT `user_id`

Response body:
```json
{ "error": "user_id_mismatch" }
```

> This 403 rule is binding and must be consistently applied across all endpoints.

## Security Rules (Non-Negotiable)

- **No cross-user data access**: a user must never be able to read/modify/delete tasks not owned by them.
- **Query isolation**: every task query must include `WHERE task.user_id = current_user.user_id`.
- **Do not trust path `user_id`**: treat it as an authorization constraint to validate, not as the source of truth.
- **No token in URL**: token must be in Authorization header only.

## Acceptance Criteria

- [ ] Backend verifies JWT using shared `BETTER_AUTH_SECRET`.
- [ ] Backend extracts `user_id` from JWT payload and uses it as authenticated identity.
- [ ] Backend rejects missing/invalid/expired token with 401 `{ "error": "unauthorized" }`.
- [ ] Backend rejects `{user_id}` mismatch with 403 `{ "error": "user_id_mismatch" }`.
- [ ] All task queries are filtered by `current_user.user_id`.
