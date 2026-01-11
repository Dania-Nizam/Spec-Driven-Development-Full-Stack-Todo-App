---
id: 0002
title: Add Claude skills files
stage: general
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: Create skills folder and add skill definitions
labels: ["claude-code","project-setup","skills"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/
 - .claude/skills/spec-reader/SKILL.md
 - .claude/skills/spec-writer/SKILL.md
 - .claude/skills/spec-validator/SKILL.md
 - .claude/skills/design-system-generator/SKILL.md
 - .claude/skills/responsive-layout-designer/SKILL.md
 - .claude/skills/sqlmodel-schema-generator/SKILL.md
 - .claude/skills/jwt-middleware-generator/SKILL.md
 - .claude/skills/fastapi-endpoint-generator/SKILL.md
 - .claude/skills/nextjs-page-generator/SKILL.md
 - .claude/skills/responsive-tester/SKILL.md
 - history/prompts/general/0002-add-claude-skills-files.general.prompt.md
tests:
 - none
---

## Prompt

add skills in skills folder spec-reader
   Purpose: Read and parse all Spec-Kit Plus files in /specs folder to understand project requirements
   Used by: orchestrator, spec-manager, constitution-keeper, all specialists
spec-writer
   Purpose: Create detailed specs with UI/UX requirements, API contracts, database schema
   Used by: spec-manager, orchestrator
spec-validator
   Purpose: Validate spec completeness, consistency with constitution, and quality
   Used by: constitution-keeper, orchestrator
design-system-generator
   Purpose: Generate consistent color schemes, typography, spacing, and reusable components (Tailwind/Shadcn)
   Used by: spec-manager, full-stack-frontend
responsive-layout-designer
   Purpose: Design mobile-first responsive layouts for Todo list, forms, auth pages
   Used by: spec-manager, full-stack-frontend
sqlmodel-schema-generator
   Purpose: Generate SQLModel models for User and Task with proper relationships and user_id isolation
   Used by: database-specialist, backend-specialist
jwt-middleware-generator
   Purpose: Generate JWT verification middleware/dependency for FastAPI using shared BETTER_AUTH_SECRET
   Used by: full-stack-backend, auth-specialist
fastapi-endpoint-generator
   Purpose: Create production-ready FastAPI CRUD endpoints with user isolation and error handling
   Used by: full-stack-backend
nextjs-page-generator
   Purpose: Generate beautiful Next.js pages and components (App Router) with JWT-protected data fetching
   Used by: full-stack-frontend
responsive-tester
    Purpose: Test responsive design across all breakpoints and suggest improvements
    Used by: orchestrator, constitution-keeper, frontend-specialist

## Response snapshot

- Created `.claude/skills/`.
- Added SKILL.md definitions for:
  - spec-reader, spec-writer, spec-validator
  - design-system-generator, responsive-layout-designer, responsive-tester
  - sqlmodel-schema-generator, jwt-middleware-generator, fastapi-endpoint-generator, nextjs-page-generator

## Outcome

- ✅ Impact: Project now has reusable Claude Code skills available under `.claude/skills/`.
- 🧪 Tests: Not applicable.
- 📁 Files: Added skill folders and SKILL.md definitions.
- 🔁 Next prompts: Use skills from orchestrator/specialists; keep descriptions aligned with repo workflow.
- 🧠 Reflection: Kept each skill minimal and role-focused to reduce accidental drift.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add allowed-tools restrictions per skill when needed.
