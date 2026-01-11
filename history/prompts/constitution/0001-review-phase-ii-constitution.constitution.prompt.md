---
id: 0001
title: Review Phase II constitution
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: constitution compliance review
labels: [constitution,compliance,hackathon2]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/d/todo-app/history/prompts/constitution/0001-review-phase-ii-constitution.constitution.prompt.md
tests:
 - none
---

## Prompt

Review /mnt/d/todo-app/specs/constitution.md for full compliance with Hackathon II Phase II rules and the project constitution requirements.

Checklist:
- Must clearly state NO MANUAL CODING and spec-driven development.
- Must mention required stack: Next.js 16+ App Router, Tailwind + shadcn/ui; FastAPI + SQLModel; Neon Postgres.
- Must specify Better Auth + JWT with shared BETTER_AUTH_SECRET.
- Must specify strict per-user isolation and 401 without token.
- Must list the REST endpoints EXACTLY as required by the hackathon document (methods and paths).
- Must include monorepo + spec-kit structure requirements.
- Must be comprehensive and enforceable (penalties).

Return APPROVED or REJECTED with a bullet list of required changes (exact wording suggestions), and note any mismatches/ambiguities (e.g., trailing slashes, /complete patch path, /tasks vs /tasks/).

## Response snapshot

VERDICT: REJECTED

Reviewed /mnt/d/todo-app/specs/constitution.md plus related repo evidence. Found: SDD and stack are stated, but endpoint exactness cannot be proven, mismatch status codes are unspecified, and the repo’s constitutional source-of-truth is ambiguous because /mnt/d/todo-app/.specify/memory/constitution.md is still an unfilled template. Also .spec-kit/config.yaml is referenced but missing.

## Outcome

- ✅ Impact: Identified concrete constitution and repo compliance blockers.
- 🧪 Tests: none
- 📁 Files: Added a constitution-stage PHR.
- 🔁 Next prompts: Update constitution wording; add missing Spec-Kit config; decide single constitution source-of-truth.
- 🧠 Reflection: Strict gates require evidence for endpoint exactness and enforceable error semantics.

## Evaluation notes (flywheel)

- Failure modes observed: Missing authoritative hackathon endpoint contract evidence; placeholder constitution template causes ambiguity.
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Make constitution specify exact mismatch status code semantics and align repo structure to its own mandates.
