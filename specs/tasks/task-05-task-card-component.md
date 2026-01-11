# Task 05 – Implement Reusable TaskCard Component

## Purpose
Display single task beautifully

## Requirements
- Component: /components/TaskCard.tsx
- Props: task object (id, title, description, completed)
- UI: Card with checkbox left, title bold, description small, edit/delete icons right
- Completed: line-through + opacity
- Hover effects
- Responsive full width on mobile
- Use Shadcn/ui Card, Checkbox, Badge
- PATCH /api/{user_id}/tasks/{id}/complete → empty body, toggle complete
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
- Create reusable TaskCard component
- Implement props interface for task object
- Design UI with checkbox on left, content in middle, icons on right
- Add visual indication for completed tasks (strikethrough, opacity)
- Implement hover effects for interactivity
- Ensure responsive design for mobile and desktop
- Use Shadcn/ui components for consistency
- Add proper accessibility attributes
- Include edit and delete icon buttons
- Implement proper state management for completion status
- Implement PATCH /api/{user_id}/tasks/{id}/complete with empty body to toggle completion
- Use authenticated user_id from session for API path construction
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
- User isolation enforced: user_id sourced ONLY from authenticated session. Path construction: `/api/${session.user.id}/tasks/...`
- Error responses strictly follow constitution format: { "error": string } — no 'detail' field

## Dependencies
- Shadcn/ui components (Card, Checkbox, Badge)
- Lucide React icons
- Tailwind CSS for styling
- TypeScript for type safety
- Centralized API client with JWT interceptor
- Better Auth session management

## Success Criteria
- TaskCard component renders properly with all required props
- Checkbox appears on left side of card
- Title is bold and description is smaller
- Edit/delete icons appear on right side
- Completed tasks show strikethrough and reduced opacity
- Hover effects work properly
- Component is fully responsive
- Uses Shadcn/ui components correctly
- Accessible to screen readers and keyboard navigation
- PATCH completion endpoint works properly
- Error handling works correctly (401, 403, 404, network)
- JSON error responses parsed correctly
- API calls use authenticated user_id only