---
id: 001
title: Update Constitution Phase III
stage: constitution
date_iso: 2026-02-02
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: Claude Code
command: "Update the existing Phase II Constitution.md to include Phase III updates"
labels:
  - constitution
  - phase-iii
  - ai-chatbot
  - todo-app
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt History Record

## PROMPT_TEXT

You are Claude Code, helping with Spec-Driven Development for Hackathon II Phase III: AI-Powered Todo Chatbot.

Task: Update the existing Phase II Constitution.md to include Phase III updates. Keep the entire original content intact (do NOT remove or change previous sections), and ADD a new major section at the end called "## Phase III Updates: AI-Powered Conversational Chatbot" (before the Enforcement section if needed, but preferably as a new numbered/headed section after Phase II Requirements).

Key additions to include in the new Phase III section:

- Phase III Goal: Build an integrated conversational AI chatbot on top of Phase II full-stack app, allowing natural language management of Todo lists (e.g., "Add a high-priority task to buy groceries tomorrow", "Reschedule my morning meetings to 2 PM", "Show my pending tasks").
- Must implement all Basic, Intermediate, and Advanced Todo features via natural language.
- Technology additions: OpenAI ChatKit for frontend conversational UI, OpenAI Agents SDK for agent orchestration and tool calling, Official MCP SDK for Model Context Protocol (expose Todo operations as MCP tools/server for standardized integration and stateful conversations).
- Reusable Intelligence (Bonus +200): Define and use reusable Agent Skills (e.g., add_task_skill, update_task_skill, etc. in backend/agents/skills/todo_skills.py) registered in ChatbotOrchestratorAgent. Reuse Phase II subagents (auth-specialist, database-specialist, etc.) where possible.
- Architecture: Central ChatbotOrchestratorAgent coordinates flow: NLP parsing → Auth check → Skill/tool calls → Response generation. Use MCP SDK for conversation state persistence and tool exposure.
- Security extension: All chatbot operations MUST respect Phase II JWT authentication (extract user_id from token/session, enforce isolation). No anonymous Todo access in chat.
- Error & UX: Friendly, natural responses; handle ambiguities, follow-ups, confirmations; support potential multi-language (Urdu) and voice if bonus pursued.
- Development: Strictly Spec-Driven – new specs in /specs/features/chatbot.md, /specs/agent-skills.md, etc. All code generated via Claude Code from refined specs.
- Monorepo extensions: New folders/files for agents/skills, MCP server (e.g., mcp/server.py with tools), ChatKit integration in frontend.
- Binding rules: Chatbot MUST call backend REST API via skills (no direct DB access in chat logic). MCP tools MUST wrap existing API endpoints securely.

Output ONLY the FULL updated Constitution Markdown (original + new Phase III section). Do NOT add extra commentary outside the Markdown. Ensure formatting remains clean, tables intact, and language professional.

Here is the current Constitution content to update:

[Current Constitution content provided]

## RESPONSE_TEXT

Updated the project constitution by adding a new Phase III section that covers the AI-powered conversational chatbot requirements. The new section (numbered as 11) includes subsections for:

1. Phase III Goal - Natural language management of Todo lists
2. Technology Stack Extensions - OpenAI ChatKit, Agents SDK, MCP SDK
3. Reusable Intelligence - Agent Skills and subagent reuse
4. Security & Authentication Extension - JWT integration and user isolation
5. User Experience & Error Handling - Natural responses and error recovery
6. Development & Specification Requirements - Spec-driven approach for new features

The original Phase II content was preserved unchanged, and the new Phase III content was appended as a continuation of the existing document structure.