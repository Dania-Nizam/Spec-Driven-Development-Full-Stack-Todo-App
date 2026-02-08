# Research Findings: MCP Integration for Todo Chatbot

**Feature**: MCP Integration (001-mcp-integration)
**Date**: 2026-02-03
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

## Executive Summary

This research document addresses the technical unknowns identified during planning for the Model Context Protocol (MCP) integration with the Todo Chatbot. The research covers MCP SDK integration patterns, authentication approaches, tool schema design, and integration strategies with existing todo skills.

## Decision Log

### Decision: MCP SDK Implementation Approach
**Rationale**: The Official MCP SDK will be used to create a standalone MCP server that integrates with existing todo skills. This approach allows for standardized tool exposure while maintaining compatibility with OpenAI Agents SDK and Claude Code workflows.

**Alternatives considered**:
- Direct API integration without MCP: Would not provide standardized tool exposure
- Custom protocol implementation: Would lack industry standardization
- Client-side MCP implementation: Would not provide server-side stateful conversations

### Decision: Authentication Wrapper Design
**Rationale**: A JWT authentication wrapper will be implemented to validate tokens before executing any MCP tool calls. This ensures user isolation and security while maintaining compatibility with existing Phase II authentication patterns.

**Alternatives considered**:
- No authentication: Would violate security requirements
- Separate authentication system: Would create inconsistency with existing patterns
- Per-tool authentication: Would be redundant and inefficient

### Decision: Stateful Conversation Context Management
**Rationale**: Conversation context will be maintained using session-based state management that persists across multiple MCP tool calls. This enables stateful conversations with task references and context awareness.

**Alternatives considered**:
- Stateless operations: Would not support contextual responses
- Client-side context only: Would not provide server-side persistence
- Database-backed sessions: Would add unnecessary complexity for conversation state

## MCP SDK Integration Research

### MCP Server Architecture
The Official MCP SDK provides a framework for creating standardized tool servers. Key components include:
- Resource providers for exposing data and functionality
- Tool definitions with schemas and descriptions
- Standardized protocols for client-server communication
- Built-in support for conversation context and state management

### Tool Schema Design
MCP tools follow a standardized schema format that includes:
- Tool name and description
- Parameter definitions with types and validation
- Return value specifications
- Error handling patterns

For the Todo Chatbot, each existing skill will be exposed as an MCP tool with appropriate schemas:
- add_task_tool: Accepts title, description, priority, due_date parameters
- view_tasks_tool: Accepts filters, pagination parameters
- update_task_tool: Accepts task_id and partial update parameters
- delete_task_tool: Accepts task_id parameter
- mark_complete_tool: Accepts task_id and completion status
- search_filter_tasks_tool: Accepts query and filter parameters
- set_recurring_tool: Accepts task_id and recurrence pattern
- get_task_context_tool: Accepts session parameters

### Integration Patterns
The MCP server will integrate with existing todo skills through:
- An integration layer that maps MCP tool calls to existing skill functions
- Authentication validation before forwarding requests to skills
- Response formatting to match MCP protocol expectations
- Error handling that translates skill errors to MCP-compatible responses

## Authentication Research

### JWT Token Validation
The MCP server will implement JWT token validation using the same patterns as Phase II:
- Extract token from Authorization header
- Validate token signature using shared BETTER_AUTH_SECRET
- Extract user_id from token payload
- Verify user_id matches the requested operation scope

### Security Wrapper Implementation
A security wrapper will be implemented as middleware that:
- Intercepts all MCP tool calls
- Validates JWT tokens before execution
- Ensures user isolation by comparing token user_id with operation context
- Returns appropriate error responses for authentication failures

## Stateful Conversation Handling

### Session Management
The MCP server will maintain conversation state using:
- Session identifiers to correlate related tool calls
- Context storage for maintaining conversation history
- Task reference tracking for contextual responses
- Cross-message data correlation for enhanced user experience

### Context Persistence
Conversation context will be stored temporarily in memory with:
- Session timeouts to prevent resource exhaustion
- Context cleanup after conversation completion
- Thread-safe access patterns for concurrent sessions
- Serialization support for context backup/restore

## Advanced Features Implementation

### Natural Language Processing Integration
The MCP server will work alongside existing NLP components to:
- Parse natural language into structured MCP tool calls
- Handle ambiguous requests that require clarification
- Support advanced features like recurring tasks and due date reminders
- Maintain conversational flow across multiple tool calls

### Recurring Task Patterns
Recurring task functionality will be exposed through:
- Standardized recurrence pattern definitions
- Calendar integration for date/time calculations
- Reminder scheduling and notification triggers
- Pattern validation and conflict resolution

## Integration with ChatbotOrchestratorAgent

### Handoff Patterns
The ChatbotOrchestratorAgent will be able to call MCP tools through:
- Standardized tool calling interfaces
- Consistent authentication patterns
- Unified error handling
- Shared conversation context management

### Compatibility Considerations
To maintain compatibility with OpenAI Agents SDK:
- MCP tool schemas will align with OpenAI function calling format
- Response formats will be compatible with agent processing
- Error responses will follow expected patterns
- Tool availability will be discoverable through standard mechanisms

## Performance and Scalability Research

### Performance Goals
The MCP server implementation will target:
- Sub-500ms response times for 90% of tool calls
- Support for 50+ concurrent conversation sessions
- Efficient context management with minimal memory overhead
- Low-latency authentication validation

### Scalability Patterns
The design supports scalability through:
- Stateless tool execution (except for conversation context)
- Modular tool architecture for independent scaling
- Connection pooling for database operations
- Caching strategies for frequently accessed data

## Error Handling and Recovery

### Error Classification
MCP tool errors will be classified as:
- Authentication errors: Invalid/missing JWT tokens
- Authorization errors: Insufficient permissions for requested operation
- Validation errors: Invalid input parameters
- System errors: Internal server errors during execution
- Business logic errors: Operation constraints violated

### Recovery Strategies
The system will implement recovery through:
- Graceful degradation when MCP server unavailable
- Fallback to direct skill calls if MCP unavailable
- Context preservation during temporary failures
- User-friendly error messages for conversational handling

## Technology Stack Alignment

### Python Ecosystem
The MCP integration will use:
- Official MCP SDK for Python (mcp-python)
- FastAPI for web framework compatibility
- python-jose for JWT validation
- Existing skill modules from backend/agents/skills/
- Standard library for serialization and validation

### Compatibility Requirements
The implementation maintains compatibility with:
- Existing Phase II authentication patterns
- Current database schema and models
- OpenAI Agents SDK integration
- Claude Code workflow requirements
- DevOps and deployment patterns