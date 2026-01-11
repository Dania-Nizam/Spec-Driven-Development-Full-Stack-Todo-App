---
id: 0007
title: Backend specs compliance review
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: danianizam
command: review-backend-specs
labels: ["review","constitution-keeper","backend","spec","api","auth","db"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/d/todo-app/history/prompts/general/0007-backend-specs-compliance-review.general.prompt.md
tests:
 - none
---

## Prompt

<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of /mnt/d/todo-app/CLAUDE.md (project instructions, checked into the codebase):

# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto-create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you MUST create a PHR (Prompt History Record).

[...snip: full CLAUDE.md included in conversation context...]
</system-reminder>
Please perform a strict constitution-keeper compliance review (APPROVED/REJECTED/REQUEST SPEC REFINEMENT) for the backend specs we just created:
- /mnt/d/todo-app/specs/database/schema.md
- /mnt/d/todo-app/specs/authentication.md
- /mnt/d/todo-app/specs/api/rest-endpoints.md
Also cross-check against:
- /mnt/d/todo-app/.specify/memory/constitution.md (authoritative)
- /mnt/d/todo-app/specs/api/contract.md (authoritative API contract)

Focus on Hackathon II Phase II rules: no manual coding, JWT auth requirements, strict per-user isolation, exact endpoint paths (no trailing slashes), error semantics (401/403/404 JSON bodies), and spec-driven requirements. Output: verdict + concrete issues and exact file:line references where applicable.

## Response snapshot

Verdict: REQUEST SPEC REFINEMENT. Identified spec structure gaps (missing plan/tasks), contract drift (param name mismatch), and auth/db ambiguities (user_id type, unnecessary password fields) with required fixes and file:line citations.

## Outcome

- Impact: blocked until specs become self-consistent, testable, and fully spec-driven.
- Tests: none
- Files: created PHR only
- Next prompts: refine specs per required fixes and resubmit for review
- Reflection: strict contract alignment and unambiguous auth/user_id type are essential for zero-manual-coding compliance.

## Evaluation notes (flywheel)

- Failure modes observed: spec drift vs authoritative contract; underspecified identity model; missing spec-kit plan/tasks artifacts.
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): align rest-endpoints paths/params to contract exactly; decide user_id canonical type; clarify user table necessity.
