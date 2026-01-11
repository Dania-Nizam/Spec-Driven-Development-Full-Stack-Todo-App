# Task 02 – Implement Login / Signup Page

## Purpose
Public authentication page

## Requirements
- Route: /app/login/page.tsx
- Design: Centered card, full height, beautiful background
- Fields: Email, Password
- Tabs or separate buttons for Sign In / Sign Up
- Better Auth client integration for auth
- Loading state on submit
- Success → redirect to / (store session)
- Error → toast message
- Responsive: Perfect on mobile and desktop
- Use Shadcn/ui Card, Input, Button, Tabs
- Handle authentication API errors:
  - Invalid credentials → toast "Invalid email or password"
  - Server error → toast "Login failed — try again"
  - Network error → toast "Connection failed"

## Implementation Details
- Create login page with centered card layout
- Implement both sign in and sign up functionality
- Use Shadcn/ui components for consistent design
- Integrate Better Auth client for authentication
- Add proper loading states during authentication
- Handle success and error cases appropriately
- Implement responsive design for all screen sizes
- Add proper validation for email and password fields
- Include proper error messaging
- Ensure smooth transitions and user experience
- On successful authentication, store session and redirect to dashboard
- Error handling for authentication API errors:
  - Invalid credentials → toast "Invalid email or password"
  - Server error → toast "Login failed — try again"
  - Network error → toast "Connection failed"
- User isolation enforced: user_id sourced ONLY from authenticated session. Path construction: `/api/${session.user.id}/tasks/...`
- Error handling complies with constitution by responding to standard JSON error formats: { "error": string } — no 'detail' field
- Clarify: Better Auth client handles auth flow, but if backend returns error (e.g., during token validation), expect { "error": "unauthorized" }
- Error responses strictly follow constitution format: { "error": string } — no 'detail' field

## Dependencies
- Better Auth client
- Shadcn/ui components (Card, Input, Button, Tabs)
- Lucide React icons
- Tailwind CSS
- Sonner for toast notifications
- Next.js App Router for navigation

## Success Criteria
- Login page displays properly with centered card
- Both sign in and sign up functionality work
- Better Auth integration functions correctly
- Loading states display during authentication
- Successful authentication redirects to dashboard and stores session
- Error messages display appropriately
- Responsive design works on mobile and desktop
- Form validation works properly
- Session management properly handles user authentication
- Authentication API errors handled with appropriate toasts