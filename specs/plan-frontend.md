# Frontend Development Plan – Phase II

## Objective
Build a beautiful, modern, fully responsive Next.js 16+ web application that implements all 5 Basic Level Todo features with secure Better Auth integration, JWT-protected API calls, and perfect user experience.

## Current Status (January 07, 2026)
- Backend live at http://127.0.0.1:8000 with Swagger UI
- All backend endpoints working
- Frontend specs approved (or in final refinement):
  - /specs/ui/design-system.md
  - /specs/ui/pages.md
  - /specs/ui/components.md
  - /specs/features/task-crud-ui.md (with security fixes)

## Prerequisites
- Node.js 18+ and pnpm/yarn/npm installed
- Backend running locally
- .env.local with NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

## Frontend Milestones (In Exact Order)

### 1. Project Setup & Structure
Responsibility: full-stack-frontend
- Create /frontend folder in monorepo
- npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
- Install additional packages:
  - @better-auth/react
  - @better-auth/next-js
  - lucide-react
  - sonner (for toasts)
  - clsx tailwind-merge
  - date-fns (optional)
- Setup Shadcn/ui: npx shadcn-ui@latest init
- Add key components: button, card, input, dialog, checkbox, toast, badge, avatar, skeleton
- Create centralized API client with JWT interceptor

### 2. Authentication & Protected Routes
Responsibility: full-stack-frontend + auth-specialist review
- Implement Better Auth client setup
- Create /app/login/page.tsx with beautiful signin/signup form
- Secure token storage (httpOnly cookies preferred)
- Create middleware.ts for protected routes (redirect to login if no session)
- Implement logout functionality
- Global auth context or use Better Auth hooks
- The frontend will extract the authenticated user_id exclusively from the Better Auth session/JWT. This user_id will be stored in a global context and used to construct all API paths dynamically.
- The authenticated user_id is obtained EXCLUSIVELY from the Better Auth session or decoded JWT.
- user_id will NEVER be derived from URL parameters, query strings, manual input, or any external source.

### 3. Root Layout & Core Pages
Responsibility: full-stack-frontend
- /app/layout.tsx: Root layout with Navbar, Toaster, main content
- Navbar: App name left, user avatar + logout dropdown right
- /app/page.tsx (dashboard): Protected main page
  - Task list grid (responsive: 1 col mobile, 2-3 col desktop)
  - FAB button (mobile fixed bottom)
  - Empty state + loading skeletons

### 4. Task CRUD UI Components & Flow
Responsibility: full-stack-frontend
- TaskCard component: Checkbox, title, description, edit/delete icons
- TaskFormDialog: Triggered by FAB or edit
- Implement all 5 Basic Level features:
  1. Add Task → FAB → Dialog → POST → Refresh + toast
  2. View List → GET on load → Render cards
  3. Update Task → Edit → Prefill dialog → PUT
  4. Delete Task → Confirm → DELETE → Remove card
  5. Mark Complete → Checkbox → PATCH /complete (empty body)
- Optimistic updates where possible
- Full error handling (401 → login, 403 → access denied, 404 → not found)
- All API calls will use the authenticated user_id from session to build paths (e.g., `/api/${session.user.id}/tasks`). No URL manipulation or external user_id sources allowed.
- All API paths are constructed using ONLY the user_id from the authenticated session.
- Any attempt to use user_id from URL manipulation or other sources is strictly prohibited and will be prevented by design.

### 5. Polish & Responsiveness
Responsibility: full-stack-frontend
- Mobile-first responsive design (Tailwind breakpoints)
- Dark mode support
- Subtle animations and hover effects
- Keyboard navigation
- Accessibility (ARIA labels, focus management)
- Loading states everywhere

### 6. Testing & Validation
Responsibility: orchestrator + constitution-keeper
- Manual end-to-end test with multiple users
- Verify user isolation (no cross-user tasks visible)
- Test token expiration → auto redirect to login
- Final constitution-keeper review for spec compliance

### 7. Deployment Preparation
- Build and test: npm run build && npm run start
- Prepare for Vercel deployment
- Update README with frontend instructions

## Security Rules
- User Isolation Enforcement: Every API request path parameter {user_id} is derived solely from the authenticated JWT/session
- On any 403 Forbidden response (user_id mismatch), display 'Access Denied' toast and refresh data
- Strict User ID Source Restriction: user_id for ALL API calls MUST come solely from the authenticated JWT/session. Use of URL parameters, query strings, local state, or any other source for user_id is FORBIDDEN to prevent bypass of user isolation.

## Agent Responsibilities
- full-stack-frontend: All implementation (Steps 1-5)
- constitution-keeper: Review after major milestones
- orchestrator: Coordinate and delegate

## Success Criteria
- Beautiful, professional UI that feels like a real product
- Perfect integration with live backend
- Strict user isolation and security
- Fully responsive on mobile and desktop
- All 5 Basic Level features working smoothly
- Spec-driven (no manual assumptions)
- Strict user isolation verified: All API paths use JWT-derived user_id only
- Verified: No API call uses user_id from any source other than authenticated session

