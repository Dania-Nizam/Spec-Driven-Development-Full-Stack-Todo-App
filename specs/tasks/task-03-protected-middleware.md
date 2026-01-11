# Task 03 – Implement Protected Routes Middleware

## Purpose
Redirect unauthenticated users to login

## Requirements
- File: /middleware.ts
- Use Better Auth middleware or custom check
- Protect / (dashboard) route
- Allow public access to /login
- On protected route without session → redirect to /login
- Validate JWT tokens against shared BETTER_AUTH_SECRET
- Handle 401 responses: redirect to login + "Session expired" toast
- Handle 403 responses: "Access denied" toast (rare during route resolution)
- Handle 404 responses: "Page not found" (if route doesn't exist)

## Implementation Details
- Create Next.js middleware to protect routes
- Integrate with Better Auth for session checking
- Define protected routes (dashboard) and public routes (login)
- Implement redirect logic for unauthenticated users
- Ensure middleware works correctly with App Router
- Add proper error handling for 401, 403, and 404 responses
- Validate JWT tokens against shared BETTER_AUTH_SECRET
- Optimize performance of middleware checks
- Test middleware with various route combinations
- Implement error handling per constitution: 401 → redirect to /login + "Session expired" toast
- For 403 responses during route resolution: show "Access denied" toast
- For 404 responses: show "Page not found" toast
- User isolation enforced: user_id sourced ONLY from authenticated session. Path construction: `/api/${session.user.id}/tasks/...`
- Error responses strictly follow constitution format: { "error": string } — no 'detail' field

## Dependencies
- Better Auth middleware/client
- Next.js middleware API
- Session management from Better Auth
- Shared BETTER_AUTH_SECRET for JWT validation

## Success Criteria
- Middleware correctly protects dashboard route
- Unauthenticated users redirected to login
- Authenticated users can access dashboard
- Login page remains accessible to all users
- Middleware performs efficiently
- No unintended route restrictions
- 401 responses properly handled with redirect and toast
- 403 and 404 responses handled appropriately
- JWT tokens validated against shared secret