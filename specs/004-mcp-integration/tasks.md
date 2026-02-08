---
description: "Task list for MCP Integration for Todo Chatbot"
---

# Tasks: MCP Integration for Todo Chatbot

**Input**: Design documents from `/specs/001-mcp-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app backend**: `backend/src/`, `backend/tests/`

<!--

  ============================================================================

  IMPORTANT: The tasks below are ACTUAL tasks based on:

  - User stories from spec.md (with their priorities P1, P2, P3...)

  - Feature requirements from plan.md

  - Entities from data-model.md

  - Endpoints from contracts/

  ============================================================================

-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create MCP directory structure in backend/mcp/
- [ ] T002 [P] Install Official MCP SDK and related dependencies in backend/requirements.txt
- [ ] T003 [P] Configure project dependencies (mcp-python, fastapi, python-jose, passlib) in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Set up MCP server structure with proper configuration in backend/mcp/server.py
- [ ] T005 [P] Implement JWT authentication wrapper for MCP tools in backend/mcp/auth.py
- [ ] T006 [P] Create request/response models for MCP operations in backend/mcp/models.py
- [ ] T007 Create configuration module for MCP server in backend/mcp/config.py
- [ ] T008 Set up environment variables and configuration loading for MCP
- [ ] T009 Create base service layer for MCP operations in backend/mcp/services.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - MCP-Enabled Todo Operations (Priority: P1) 🎯 MVP

**Goal**: As a user of the todo chatbot, I want to interact with my tasks using natural language that gets translated into standardized MCP tool calls, so that I can manage my tasks efficiently with consistent, reliable operations.

**Independent Test**: Can be fully tested by sending natural language commands to the chatbot and verifying that appropriate MCP tools are called with correct parameters, delivering consistent task management operations.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create MCP Tool Definition models in backend/mcp/models.py
- [ ] T011 [P] [US1] Create MCP Session management in backend/mcp/session.py
- [ ] T012 [US1] Implement add_task MCP tool in backend/mcp/tools/add_task.py
- [ ] T013 [US1] Implement view_tasks MCP tool in backend/mcp/tools/view_tasks.py
- [ ] T014 [US1] Implement update_task MCP tool in backend/mcp/tools/update_task.py
- [ ] T015 [P] [US1] Create tool schemas in backend/mcp/schemas.py
- [ ] T016 [P] [US1] Create MCP tool registry in backend/mcp/registry.py
- [ ] T017 [US1] Create MCP endpoint POST /mcp/tools/{tool_name} in backend/mcp/routers/tools.py
- [ ] T018 [US1] Create router module init in backend/mcp/routers/__init__.py
- [ ] T019 [US1] Register basic tools as MCP tools
- [ ] T020 [US1] Implement basic flow: auth → validate → tool execution → response

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure MCP Tool Access (Priority: P1)

**Goal**: As a security-conscious user, I want my MCP tool calls to be protected by JWT authentication, so that unauthorized access to my todo data is prevented.

**Independent Test**: Can be tested by attempting MCP tool calls with invalid/missing JWT tokens and verifying that access is denied, while valid tokens allow access.

### Implementation for User Story 2

- [ ] T021 [P] [US2] Enhance JWT validation with user_id matching in mcp/auth.py
- [ ] T022 [US2] Implement user isolation checks in MCP authentication
- [ ] T023 [US2] Add 401/403 error handling for authentication failures
- [ ] T024 [US2] Create user isolation middleware for MCP endpoints
- [ ] T025 [US2] Add validation to ensure JWT user_id matches tool operation scope
- [ ] T026 [US2] Implement proper error responses per constitution requirements

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Stateful Conversations with Context (Priority: P2)

**Goal**: As a user engaging in multi-turn conversations with the chatbot, I want the system to maintain context across messages, so that I can have natural conversations that reference previous interactions and tasks.

**Independent Test**: Can be tested by having multi-turn conversations where the chatbot references previous tasks or context, maintaining coherence throughout the interaction.

### Implementation for User Story 3

- [ ] T027 [P] [US3] Implement delete_task MCP tool in backend/mcp/tools/delete_task.py
- [ ] T028 [P] [US3] Implement mark_complete MCP tool in backend/mcp/tools/mark_complete.py
- [ ] T029 [P] [US3] Implement search_filter_tasks MCP tool in backend/mcp/tools/search_filter_tasks.py
- [ ] T030 [P] [US3] Implement set_recurring MCP tool in backend/mcp/tools/set_recurring.py
- [ ] T031 [P] [US3] Implement get_task_context MCP tool in backend/mcp/tools/get_task_context.py
- [ ] T032 [P] [US3] Implement conversation context management in backend/mcp/context.py
- [ ] T033 [US3] Register all tools as MCP tools
- [ ] T034 [US3] Enhance MCP tools to recognize context-aware parameters
- [ ] T035 [US3] Add support for contextual task references (e.g., "that task", "previous item")
- [ ] T036 [US3] Implement context-aware responses using conversation context

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Advanced Task Features via Natural Language (Priority: P2)

**Goal**: As a power user, I want to define advanced task features like recurring tasks and due dates through natural language, so that I can create sophisticated task management without complex interfaces.

**Independent Test**: Can be tested by providing natural language input about recurring tasks and due dates and verifying that advanced task features are properly created and managed.

### Implementation for User Story 4

- [ ] T037 [P] [US4] Implement recurring task patterns in backend/mcp/tools/set_recurring.py
- [ ] T038 [US4] Add due date and reminder functionality to MCP tools
- [ ] T039 [P] [US4] Implement advanced task features (tags, categories, etc.) in MCP tools
- [ ] T040 [US4] Add time-based reminder triggers to MCP tools
- [ ] T041 [P] [US4] Enhance conversation context with advanced feature tracking
- [ ] T042 [US4] Implement natural language processing for advanced features in MCP
- [ ] T043 [US4] Add error handling for advanced feature requests requiring clarification
- [ ] T044 [US4] Create integration tests for advanced feature scenarios

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Integrated Chatbot Orchestration (Priority: P3)

**Goal**: As a developer integrating systems, I want the ChatbotOrchestratorAgent to seamlessly call MCP tools, so that I can leverage standardized interfaces for consistent behavior across different AI platforms.

**Independent Test**: Can be tested by triggering the ChatbotOrchestratorAgent and verifying it properly calls MCP tools instead of direct implementations.

### Implementation for User Story 5

- [ ] T045 [P] [US5] Create MCP integration module in backend/mcp/integration.py
- [ ] T046 [US5] Update ChatbotOrchestratorAgent to support MCP tool calls
- [ ] T047 [US5] Implement MCP tool discovery and registration in orchestrator
- [ ] T048 [US5] Create fallback mechanisms for when MCP tools unavailable
- [ ] T049 [P] [US5] Add MCP compatibility layer for OpenAI Agents SDK
- [ ] T050 [US5] Test integration between ChatbotOrchestratorAgent and MCP tools

**Checkpoint**: At this point, all user stories should work independently

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T051 [P] Add comprehensive error handling for all MCP tool executions
- [ ] T052 Add input sanitization and validation for all MCP tool parameters
- [ ] T053 [P] Implement MCP session timeout and cleanup in backend/mcp/session.py
- [ ] T054 Add rate limiting to MCP endpoints
- [ ] T055 [P] Add logging and monitoring for MCP operations
- [ ] T056 Implement proper MCP session management with UUID generation
- [ ] T057 Add performance optimizations and caching where needed for MCP
- [ ] T058 Run validation tests to ensure all MCP functionality works per spec
- [ ] T059 Create MCP-specific documentation in backend/mcp/README.md
- [ ] T060 Add unit tests for all MCP components

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 completion - builds upon basic tool access
- **User Story 3 (P3)**: Depends on User Story 1 completion - enhances existing functionality
- **User Story 4 (P4)**: Depends on User Story 3 completion - builds on context management
- **User Story 5 (P5)**: Depends on User Story 1 completion - integrates with orchestrator

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All components within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

### Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create MCP Tool Definition models in backend/mcp/models.py"
Task: "Create tool schemas in backend/mcp/schemas.py"
Task: "Create MCP tool registry in backend/mcp/registry.py"
Task: "Create MCP endpoint POST /mcp/tools/{tool_name} in backend/mcp/routers/tools.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3 (after US1)
   - Developer D: User Story 4 (after US3)
   - Developer E: User Story 5 (after US1)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence