# Task 01 – Implement Root Layout and Global Components

## Purpose
Set up global structure used across all pages

## Requirements
- /app/layout.tsx with html, body, providers
- Include Navbar component (app name + logout when auth)
- Include Toaster (sonner)
- Font setup (Inter or system)
- Tailwind base styles
- Metadata and title
- Create centralized API client with JWT interceptor

## Implementation Details
- Create root layout file that wraps all pages in the application
- Set up Next.js App Router layout with proper HTML structure
- Integrate Shadcn/ui components and Lucide icons
- Implement responsive design ready for all screen sizes
- Include global providers (Better Auth, Theme Provider, etc.)
- Set up proper metadata for SEO
- Ensure font loading is optimized
- Add global styles and base Tailwind configurations
- Create centralized API client that automatically attaches Authorization: Bearer {token} header from Better Auth session
- User isolation enforced: user_id sourced ONLY from authenticated session. Path construction: `/api/${session.user.id}/tasks/...`
- Error responses strictly follow constitution format: { "error": string } — no 'detail' field

## Dependencies
- Next.js 16+ with App Router
- Shadcn/ui components
- Lucide React icons
- Better Auth client
- Tailwind CSS
- Sonner for toasts
- Centralized API client with JWT interceptor

## Success Criteria
- Root layout renders properly across all pages
- Navbar displays correctly with app name and logout when authenticated
- Toaster component appears and functions properly
- Fonts load correctly
- Responsive design works on all screen sizes
- Global providers are properly initialized
- Centralized API client properly attaches JWT tokens to all requests
- User isolation enforced: all API paths use authenticated user_id only
- Error handling responds to standard JSON error formats