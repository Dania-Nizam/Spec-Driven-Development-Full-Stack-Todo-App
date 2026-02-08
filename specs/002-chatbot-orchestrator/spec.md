# Feature Specification: Chatbot Orchestrator for AI-Powered Todo Chatbot

**Feature Branch**: `001-chatbot-orchestrator`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase III: Implement the core backend logic for the AI-Powered Todo Chatbot using OpenAI Agents SDK, integrating with reusable Agent Skills and Phase II REST API.

Detailed Requirements:
- Create ChatbotOrchestratorAgent using OpenAI Agents SDK as the central coordinator.
- Register all reusable Agent Skills from backend/agents/skills/todo_skills.py as tools: add_task_skill, delete_task_skill, update_task_skill, view_tasks_skill, mark_complete_skill, search_filter_tasks_skill, set_recurring_skill, auth_check_skill, get_task_context_skill.
- Handle full conversational flow:
  1. Authenticate request using auth_check_skill (JWT from header/session, extract user_id).
  2. Parse natural language intent and entities (using model reasoning or handoff to NLP sub-agent if separate).
  3. Execute appropriate skill/tool based on intent (e.g., add_task_skill for "add task buy groceries high priority").
  4. Use get_task_context_skill for follow-up context (e.g., "update that task").
  5. Generate natural, friendly response.
- Create FastAPI endpoint: POST /api/{user_id}/chat to receive messages and invoke orchestrator.
- Enforce Phase II security: Strict user isolation, 401/403/404 errors as per constitution.
- Support all Todo features via natural language: Basic (add/delete/update/view/mark), Intermediate (priorities/tags/search/sort), Advanced (recurring auto-reschedule, due dates with reminders).
- Reuse Phase II sub-agents (auth-specialist, database-specialist) via handoffs if needed.
- No direct database access — all operations via skills that call Phase II REST API.

Generate a complete Markdown spec with sections: Overview, Agent Architecture, Tool Registration, Flow Diagram (text), Security Rules, Feature Coverage, Deliverables (files in /backend/agents)."

## Overview

Implement the core backend logic for the AI-Powered Todo Chatbot using OpenAI Agents SDK as the central coordinator. The ChatbotOrchestratorAgent will integrate with reusable Agent Skills and enforce Phase II security standards while supporting all Todo features via natural language processing.

## Agent Architecture

The ChatbotOrchestratorAgent serves as the central coordinator that manages the full conversational flow by coordinating between authentication, natural language processing, skill execution, and response generation. The agent will leverage OpenAI's Agents SDK for orchestration and maintain strict separation of concerns with specialized skills.

## Tool Registration

The orchestrator agent will register the following reusable Agent Skills as tools:
- add_task_skill: For adding new todo tasks
- delete_task_skill: For removing todo tasks
- update_task_skill: For updating task details
- view_tasks_skill: For listing and viewing tasks
- mark_complete_skill: For marking tasks as complete/incomplete
- search_filter_tasks_skill: For searching and filtering tasks
- set_recurring_skill: For setting recurring patterns on tasks
- auth_check_skill: For verifying JWT authentication and extracting user_id
- get_task_context_skill: For retrieving recent task context for follow-up conversations

## Flow Diagram (text)

1. **Request Authentication**: The system receives a chat message and authenticates the request using auth_check_skill to validate the JWT and extract the user_id.
2. **Natural Language Processing**: The orchestrator parses the natural language input to identify intent and extract entities using model reasoning capabilities.
3. **Skill Selection**: Based on the parsed intent, the orchestrator selects the appropriate skill/tool to execute (e.g., add_task_skill for "add task buy groceries high priority").
4. **Context Retrieval**: If needed, the orchestrator uses get_task_context_skill to retrieve recent task context for follow-up conversations (e.g., when user says "update that task").
5. **Skill Execution**: The selected skill is executed with the parsed parameters and user context.
6. **Response Generation**: The orchestrator generates a natural, friendly response based on the skill execution results.
7. **Response Delivery**: The response is returned to the frontend for display to the user.

## Security Rules

- **JWT Authentication**: All chat requests must include a valid JWT token which is verified using auth_check_skill.
- **User Isolation**: Strict user isolation is enforced - each user can only access their own tasks as determined by the authenticated user_id.
- **Authorization Checks**: The system must return 401 Unauthorized for missing/invalid tokens, 403 Forbidden for user_id mismatches, and 404 Not Found for non-existent resources.
- **Secure Tool Access**: All operations must go through registered skills that call the Phase II REST API - no direct database access is allowed.
- **Data Validation**: All inputs from natural language processing must be validated before being passed to skills.

## Feature Coverage

The chatbot must support all Todo features via natural language:

**Basic Features:**
- Add tasks (e.g., "Add a task to buy groceries")
- Delete tasks (e.g., "Delete the meeting task")
- Update tasks (e.g., "Change the grocery task to tomorrow")
- View task lists (e.g., "Show my tasks", "Show pending tasks")
- Mark tasks as complete/incomplete (e.g., "Mark task 1 as complete")

**Intermediate Features:**
- Priorities (e.g., "Add a high priority task")
- Tags (e.g., "Tag this task as work")
- Search and filter (e.g., "Find tasks with 'grocery'", "Show urgent tasks")
- Sorting (e.g., "Show tasks by due date")

**Advanced Features:**
- Recurring tasks (e.g., "Make this task repeat weekly")
- Auto-rescheduling (e.g., "Move this task to next Tuesday")
- Due dates and reminders (e.g., "Set a reminder for tomorrow at 9 AM")

## Deliverables

### Files to be created in /backend/agents:

- **chatbot_orchestrator_agent/orchestrator.py**: Core ChatbotOrchestratorAgent implementation using OpenAI Agents SDK
- **chatbot_orchestrator_agent/__init__.py**: Module initialization and exports
- **routes/chat.py**: FastAPI endpoint at POST /api/{user_id}/chat to receive messages and invoke orchestrator
- **routes/__init__.py**: Route module initialization
- **dependencies/auth.py**: JWT authentication dependency for chat endpoints
- **services/chat_service.py**: Service layer for chat operations
- **config/agents_config.py**: Configuration for agent tools and settings

### Integration with existing skills:

- **skills/todo_skills.py**: Integration with existing Agent Skills for task operations
- **utils/context_manager.py**: Context management for conversation history and follow-up handling

## User Stories

### User Story 1 - Chat Request Processing (Priority: P1)

As an authenticated user, I want to send natural language messages to the chatbot and receive appropriate responses that perform Todo operations. The system should authenticate my request, interpret my intent, execute the appropriate action, and provide a natural response.

**Why this priority**: This is the core functionality that enables the entire chatbot experience. Without proper request processing, no other features are possible.

**Independent Test**: The system can receive a chat message, authenticate the user, process the natural language intent, execute the appropriate skill, and return a response.

**Acceptance Scenarios**:
1. **Given** I am an authenticated user, **When** I send a message like "Add a task to buy groceries", **Then** the system processes my intent, calls add_task_skill, and confirms the task was added.
2. **Given** I send a malformed message, **When** the system processes it, **Then** it responds with a helpful clarification message.

---

### User Story 2 - Authentication and User Isolation (Priority: P1)

As a security-conscious user, I want to ensure that my chat interactions only affect my own tasks and that unauthorized users cannot access my data. The system must enforce strict authentication and user isolation.

**Why this priority**: Security and privacy are fundamental requirements. Without proper authentication and isolation, the system is vulnerable to data breaches.

**Independent Test**: The system validates JWT tokens for each request and ensures operations only affect the authenticated user's data.

**Acceptance Scenarios**:
1. **Given** I send a chat request with a valid JWT, **When** I request to view my tasks, **Then** I only see my own tasks.
2. **Given** I send a chat request without a valid JWT, **When** I try to perform any operation, **Then** I receive a 401 Unauthorized error.

---

### User Story 3 - Comprehensive Todo Feature Support (Priority: P2)

As a user, I want to access all Todo features through natural language commands including basic CRUD operations, priorities, tags, search/filter, recurring tasks, and due date management. The chatbot should understand and execute these varied intents.

**Why this priority**: This delivers the full value of the chatbot by enabling all Todo functionality through natural language, providing a rich user experience.

**Independent Test**: The system can interpret and execute commands for all supported Todo features through natural language.

**Acceptance Scenarios**:
1. **Given** I send a natural language command like "Set a recurring weekly task to water plants", **When** the system processes it, **Then** it creates a recurring task with the specified parameters.
2. **Given** I send a follow-up command like "Update that task to Friday", **When** the system processes it, **Then** it modifies the previous task based on context.

---

## Edge Cases

- What happens when the JWT token expires mid-conversation?
- How does the system handle ambiguous natural language that could map to multiple intents?
- What occurs when a user refers to a task by context (e.g., "that task") but no clear reference exists?
- How does the system respond when a requested skill fails or returns an error?
- What happens when the OpenAI Agents SDK is temporarily unavailable?

## Requirements

### Functional Requirements

- **FR-001**: System MUST authenticate all chat requests using JWT tokens via auth_check_skill
- **FR-002**: System MUST register all Agent Skills (add_task_skill, delete_task_skill, etc.) as tools for the orchestrator agent
- **FR-003**: System MUST parse natural language input to identify intent and extract entities
- **FR-004**: System MUST execute appropriate skills based on parsed intent
- **FR-005**: System MUST retrieve task context for follow-up conversations using get_task_context_skill
- **FR-006**: System MUST generate natural, friendly responses to user inputs
- **FR-007**: System MUST create a FastAPI endpoint at POST /api/{user_id}/chat
- **FR-008**: System MUST enforce strict user isolation between different user accounts
- **FR-009**: System MUST return proper HTTP error codes (401, 403, 404) as per Phase II constitution
- **FR-010**: System MUST support all Basic, Intermediate, and Advanced Todo features via natural language
- **FR-011**: System MUST route all operations through registered skills that call Phase II REST API
- **FR-012**: System MUST handle conversation context for follow-up interactions

### Key Entities

- **ChatMessage**: Represents a message in the conversation with content, user_id, timestamp, and processing status
- **ConversationContext**: Maintains the context of a conversation including recent tasks referenced for follow-up operations
- **AgentTool**: Represents a registered skill/tool that the orchestrator agent can call to perform specific actions

## Success Criteria

### Measurable Outcomes

- **SC-001**: 95% of natural language commands are correctly interpreted and mapped to appropriate skills
- **SC-002**: All authenticated requests are processed with proper user isolation in 100% of cases
- **SC-003**: The chat endpoint responds within 3 seconds for 90% of requests under normal load
- **SC-004**: Users can perform all Todo operations through natural language with 90% success rate
- **SC-005**: The system correctly handles follow-up conversations using context in 85% of cases
- **SC-006**: Zero direct database access occurs - all operations go through registered skills calling REST API
