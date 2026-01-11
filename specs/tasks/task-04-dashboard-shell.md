# Task 04 – Implement Dashboard Shell and Task List Skeleton

## Purpose
Main protected page structure

## Requirements
- Route: /app/page.tsx
- Navbar with user greeting/logout
- Main content area
- FAB button (mobile fixed) for Add Task
- Loading skeleton grid (3-6 cards)
- Empty state component
- Responsive grid: 1 col mobile, 2-3 col desktop
- Extract user_id from session for API calls
- Fetch tasks using GET /api/{user_id}/tasks
- Handle 401 → redirect to /login + "Session expired" toast
- Handle 403 → "Access denied - invalid user" toast + refresh
- Handle 404 → "Task not found" message
- Handle Network error → "Connection failed" toast
- Parse JSON error responses: { "error": "error_type" }
- Examples:
  - 401 → { "error": "unauthorized" } → show "Session expired" → redirect to login
  - 403 → { "error": "user_id_mismatch" } → show "Access denied"
  - 404 → { "error": "not_found" } → show "Task not found"

## Implementation Details
- Create dashboard page with proper layout
- Implement Navbar with user greeting and logout functionality
- Add Floating Action Button (FAB) for adding tasks
- Create loading skeleton components for task cards
- Implement empty state when no tasks exist
- Design responsive grid layout for task display
- Extract user_id from authenticated session and use for API path construction
- Fetch tasks using GET /api/{user_id}/tasks with Authorization: Bearer {token} header
- Implement error handling per constitution:
  - 401 → redirect to /login + "Session expired" toast
  - 403 → "Access denied - invalid user" toast + refresh
  - 404 → "Task not found" message
  - Network error → "Connection failed" toast
- On API error response, parse the "error" field from JSON response and display in toast
- Examples:
  - 401 → { "error": "unauthorized" } → show "Session expired" → redirect to login
  - 403 → { "error": "user_id_mismatch" } → show "Access denied"
  - 404 → { "error": "not_found" } → show "Task not found"
- Prepare structure for future task integration
- Ensure responsive design works across devices
- Add proper accessibility attributes
- User isolation enforced: user_id sourced ONLY from authenticated session. Path construction: `/api/${session.user.id}/tasks/...`
- Error responses strictly follow constitution format: { "error": string } — no 'detail' field

## Dependencies
- Better Auth session management
- Shadcn/ui components (Skeleton, Button, Card)
- Lucide React icons
- Tailwind CSS for responsive design
- Navbar component from Task 01
- Centralized API client with JWT interceptor

## Success Criteria
- Dashboard page renders properly when authenticated
- Navbar displays user greeting and logout
- FAB button appears and is fixed on mobile
- Loading skeletons display during data fetch
- Empty state shows when no tasks exist
- Responsive grid works on mobile and desktop
- User_id successfully extracted from session and used for API calls
- API calls made with proper Authorization header
- Error handling works correctly (401, 403, 404, network)
- JSON error responses parsed correctly
- Layout adapts to different screen sizes