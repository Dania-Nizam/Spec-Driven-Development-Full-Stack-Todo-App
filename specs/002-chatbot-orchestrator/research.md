# Research Summary: Chatbot Orchestrator for AI-Powered Todo Chatbot

## Overview

This research document outlines the technical decisions, architecture patterns, and implementation approach for the ChatbotOrchestratorAgent using OpenAI Agents SDK. The solution integrates with reusable Agent Skills and enforces Phase II security standards while supporting all Todo features via natural language processing.

## Technology Stack Confirmation

### FastAPI (Python 3.13+)
**Decision**: Use FastAPI as the primary web framework for the chat endpoint
**Rationale**: FastAPI provides excellent performance, built-in async support, automatic API documentation, and seamless integration with existing Phase II architecture. Its dependency injection system works well with JWT authentication patterns established in Phase II.

**Alternatives considered**:
- Flask: Less performant, fewer built-in features
- Django: Overkill for API-only service, heavier framework
- Express.js: Would require changing to Node.js ecosystem

### OpenAI Agents SDK
**Decision**: Use OpenAI Agents SDK for agent orchestration and tool calling
**Rationale**: Provides robust natural language processing capabilities, built-in function calling, and state management for conversations. Integrates well with existing todo operations through tool registration.

**Alternatives considered**:
- LangChain: More complex, vendor lock-in to OpenAI
- Custom NLP: Time-intensive, reinventing existing solutions
- Hugging Face transformers: More complex setup, requires model hosting

### SQLModel/Neon PostgreSQL Integration
**Decision**: Leverage existing Phase II SQLModel and Neon PostgreSQL infrastructure
**Rationale**: Maintains consistency with existing architecture, reduces complexity, and ensures data integrity across the application. All todo operations remain consistent with Phase II patterns.

**Alternatives considered**:
- MongoDB: Would require significant changes to data layer
- In-memory storage: Not suitable for production, no persistence
- Separate database: Increases complexity and data synchronization issues

## Architecture Patterns

### Agent Orchestration Pattern
**Decision**: Implement ChatbotOrchestratorAgent as central coordinator
**Rationale**: Provides clean separation of concerns with distinct responsibilities:
1. Authentication verification through auth_check_skill
2. Natural language intent parsing
3. Tool/skill selection and execution
4. Context management via get_task_context_skill
5. Response generation

**Alternatives considered**:
- Direct API calls: No natural language processing
- Monolithic approach: Harder to maintain and extend
- Multiple specialized agents: More complex coordination needed

### Skills-Based Integration
**Decision**: Register all todo operations as reusable skills/tools
**Rationale**: Enables flexible natural language processing where the agent can dynamically call appropriate skills based on user intent. Skills maintain proper authentication and user isolation patterns.

**Skills to implement**:
- `add_task_skill`: Handle "Add task..." requests
- `delete_task_skill`: Handle "Delete task..." requests
- `update_task_skill`: Handle "Update task..." requests
- `view_tasks_skill`: Handle "Show tasks..." requests
- `mark_complete_skill`: Handle "Complete task..." requests
- `search_filter_tasks_skill`: Handle "Find tasks..." requests
- `set_recurring_skill`: Handle recurring task requests
- `auth_check_skill`: Handle authentication verification
- `get_task_context_skill`: Provide context for follow-up requests

### Security Architecture
**Decision**: Implement layered security approach with JWT validation at multiple levels
**Rationale**: Ensures user isolation is maintained throughout the system:
1. JWT validation at the API endpoint level
2. User ID verification in the path matches authenticated user
3. Skill-level validation to prevent unauthorized access
4. Proper error handling for authentication failures

**Alternatives considered**:
- Session-based auth: More complex for API-only service
- OAuth 2.0: Overkill for existing Better Auth integration
- API keys: Less secure, harder to manage

## Natural Language Processing Approach

### Intent Classification
**Decision**: Use OpenAI Agents SDK for intent classification and tool selection
**Rationale**: Leverages advanced AI models for accurate intent recognition without requiring custom training. The agent automatically selects appropriate skills based on user input.

**Processing flow**:
1. User sends natural language message to chat endpoint
2. JWT authentication validates user identity
3. OpenAI agent parses intent and selects appropriate skill
4. Selected skill executes with validated user context
5. Response is generated and returned to user

### Context Management
**Decision**: Implement conversation context using get_task_context_skill
**Rationale**: Enables natural follow-up conversations where users can reference previous tasks or operations without repeating full context.

## Implementation Considerations

### Streaming Responses
**Decision**: Support server-sent events (SSE) for streaming responses
**Rationale**: Provides better user experience for longer responses, showing progress as the AI generates the response.

### Error Handling
**Decision**: Implement comprehensive error handling at multiple levels
- API level: Proper HTTP status codes (401, 403, 404)
- Authentication level: Clear error messages for auth failures
- Skill level: Graceful handling of failed operations
- AI level: Fallback responses for unrecognized intents

### Testing Strategy
**Decision**: Implement both unit and integration tests
- Unit tests for individual skills and components
- Integration tests for the full chat endpoint workflow
- Mock OpenAI responses for predictable testing
- Test user isolation to ensure security