---
id: 1
title: generate-frontend-specifications
stage: spec
date_iso: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-spec-manager
branch: 002-frontend-spec-manager
user: claude
command: sp.specify
labels: ["spec", "frontend", "ui", "design-system", "task-crud"]
links:
  spec: "/mnt/d/todo-app/specs/002-frontend-spec-manager/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - /mnt/d/todo-app/specs/002-frontend-spec-manager/spec.md
  - /mnt/d/todo-app/specs/ui/design-system.md
  - /mnt/d/todo-app/specs/ui/pages.md
  - /mnt/d/todo-app/specs/ui/components.md
  - /mnt/d/todo-app/specs/features/task-crud-ui.md
  - /mnt/d/todo-app/specs/002-frontend-spec-manager/checklists/requirements.md
tests_yaml:
  - spec-validation
  - checklist-verification
prompt_text: |
  You are the spec-manager subagent.

  Task: Generate complete frontend specifications for Phase II Full-Stack Todo Web Application.

  Focus exclusively on frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Shadcn/ui components, Better Auth integration, fully responsive mobile-first design.

  Create these four critical Markdown spec files with high detail so that full-stack-frontend agent can generate stunning, professional UI in one shot.

  Use these skills:
  - spec-writer: For structured, clear Markdown
  - design-system-generator: For consistent colors, typography, spacing
  - responsive-layout-designer: For mobile/tablet/desktop layouts

  After generating each spec, IMMEDIATELY write it as an actual file on disk in /specs folder.

  1. File: /specs/ui/design-system.md
     Title: UI Design System – Colors, Typography, Components
     Content:
     - Primary Color: Indigo (#6366f1)
     - Accent: Blue (#3b82f6)
     - Neutral: Slate/Gray tones
     - Success: Green, Error: Red, Warning: Amber
     - Typography: Inter font or system stack, proper hierarchy (h1-h4, body, small)
     - Spacing: Tailwind consistent scale
     - Components: Use Shadcn/ui — Button, Card, Input, Checkbox, Dialog, Toaster, Badge, Avatar
     - Icons: Lucide-react
     - Dark Mode: Support via Tailwind dark:
     - Rounded corners, subtle shadows, hover effects

  2. File: /specs/ui/pages.md
     Title: Frontend Pages & Layout Specification
     Content:
     - App Structure: Next.js App Router (/app folder)
     - Root Layout: Navbar + main content + toaster
     - Pages:
       - /login → Centered card with tabs or separate signin/signup
         - Email/password fields
         - Submit button
         - Error/success messages
         - Responsive: Full screen on mobile
       - / (dashboard) → Protected main page
         - Top or side navbar with app name, user avatar, logout
         - Task list area (cards or table)
         - Floating Action Button (FAB) bottom-right for "Add Task"
         - Empty state if no tasks
         - Loading skeleton
     - Protected Routes: Redirect to /login if not authenticated

  3. File: /specs/ui/components.md
     Title: Reusable UI Components Specification
     Content:
     - TaskCard:
       - Checkbox for complete
       - Title + description preview
       - Edit/Delete icons (hover)
       - Badge for status
     - TaskForm (in Dialog/Modal):
       - Title input (required)
       - Description textarea (optional)
       - Submit/Cancel buttons
     - Navbar:
       - Logo/App name
       - User greeting or avatar dropdown with logout
     - Toaster for success/error messages
     - LoadingSpinner component

  4. File: /specs/features/task-crud-ui.md
     Title: Frontend Feature – Task CRUD UI Flow
     Content:
     - Implement all 5 Basic Level features via UI:
       1. Add Task → Click FAB → Open modal → Fill form → Submit → API POST → Refresh list + toast
       2. View Task List → Dashboard shows cards with tasks fetched via GET
       3. Update Task → Click edit icon → Open modal with prefilled data → PUT → Update UI
       4. Delete Task → Click delete → Confirm dialog → DELETE → Remove from UI
       5. Mark Complete → Click checkbox → PATCH /complete → Toggle instantly
     - API Integration:
       - All calls to backend with JWT in Authorization: Bearer header
       - Use fetch or axios with interceptors
       - Handle loading, error, success states
     - Responsive Behavior:
       - Mobile: Vertical stack, FAB fixed bottom, full-width cards
       - Desktop: Grid layout for tasks, sidebar possible
     - UX Polish:
       - Smooth transitions
       - Optimistic updates where possible
       - Keyboard navigation support

  Workflow:
  1. Generate each spec with visual descriptions and exact requirements.
  2. Use design-system-generator and responsive-layout-designer for beautiful, consistent, mobile-first design.
  3. After each spec, write the full content to the correct file path on disk.
  4. Confirm file creation.

  Final Response:
  "Frontend specifications successfully generated and saved:
  - /specs/ui/design-system.md
  - /specs/ui/pages.md
  - /specs/ui/components.md
  - /specs/features/task-crud-ui.md

  Frontend specs are now complete and ready for:
  1. constitution-keeper review
  2. Implementation by full-stack-frontend agent using nextjs-page-generator, responsive-layout-designer, and design-system-generator skills

  Next step: Build a stunning, professional, responsive Todo app UI that impresses judges."
response_text: |
  Successfully generated complete frontend specifications for the Todo Web Application. Created four critical specification files:

  1. /specs/ui/design-system.md - Comprehensive UI design system with colors, typography, and components
  2. /specs/ui/pages.md - Detailed frontend pages and layout specifications
  3. /specs/ui/components.md - Reusable UI components specification
  4. /specs/features/task-crud-ui.md - Task CRUD UI flow with API integration details

  All specifications include detailed requirements for Next.js 16+ (App Router), TypeScript, Tailwind CSS, Shadcn/ui components, Better Auth integration, and responsive mobile-first design. The specifications are ready for implementation by the full-stack-frontend agent.
outcome: Successfully generated comprehensive frontend specifications for the Todo application, including design system, pages, components, and CRUD flow specifications.
evaluation: All required specification files have been created with detailed requirements and are ready for the next phase of development.
---