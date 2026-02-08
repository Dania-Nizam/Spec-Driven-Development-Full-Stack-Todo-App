# Implementation Plan: MCP Integration for Todo Chatbot

**Branch**: `001-mcp-integration` | **Date**: 2026-02-03 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Model Context Protocol (MCP) integration using Official MCP SDK for the Todo Chatbot to enable standardized tool exposure and stateful conversations. The implementation will create an MCP server that exposes all existing Todo Agent Skills as standardized tools with proper authentication, stateful conversation context, and advanced features like recurring tasks and due date reminders. The MCP server will integrate with the ChatbotOrchestratorAgent to provide standardized interfaces compatible with OpenAI Agents SDK and Claude Code workflows.

## Technical Context

**Language/Version**: Python 3.11+ (required by spec)
**Primary Dependencies**: Official MCP SDK, FastAPI, python-jose, passlib, existing todo skills from backend/agents/skills/, OpenAI Agents SDK
**Storage**: Neon Serverless PostgreSQL database (DATABASE_URL) with existing Phase II schema
**Testing**: pytest with MCP client testing, integration tests for tool calls, conversation state validation
**Target Platform**: Linux server, containerized deployment
**Project Type**: Web application (backend component extending Phase II architecture)
**Performance Goals**: <500ms response time for 90% of MCP tool calls, support 50 concurrent MCP sessions
**Constraints**: Must maintain strict user isolation, reuse existing Phase II auth patterns, follow established API contract patterns, ensure backward compatibility with existing todo operations
**Scale/Scope**: Individual user sessions with multi-user support via authenticated MCP tool calls

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Development**: ✅ All implementation will be based on the approved specification in spec.md
2. **Authentication Compliance**: ✅ Will implement JWT token validation and user isolation following Phase II patterns
3. **API Contract Compliance**: ✅ Will integrate with existing Phase II endpoints respecting the canonical path rules
4. **Security Requirements**: ✅ MCP tools will require JWT authentication before execution, enforcing user isolation
5. **Manual Coding Prohibition**: ✅ All code will be generated from specifications using Claude Code
6. **Monorepo Structure**: ✅ Will maintain clear separation of concerns in existing backend structure
7. **Phase III Requirements**: ✅ MCP integration aligns with Phase III goals for standardized tool exposure and stateful conversations

*Post-Design Constitution Check: All gates passed*

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── mcp/
│   ├── server.py                    # Main MCP server implementation using Official MCP SDK
│   ├── tools/                       # Directory containing standardized tool implementations
│   │   ├── add_task.py              # MCP tool for adding tasks
│   │   ├── update_task.py           # MCP tool for updating tasks
│   │   ├── delete_task.py           # MCP tool for deleting tasks
│   │   ├── view_tasks.py            # MCP tool for viewing tasks
│   │   ├── mark_complete.py         # MCP tool for marking tasks complete
│   │   ├── search_filter_tasks.py   # MCP tool for searching/filtering tasks
│   │   ├── set_recurring.py         # MCP tool for recurring tasks
│   │   └── get_task_context.py      # MCP tool for task context
│   ├── auth.py                      # JWT authentication wrapper for MCP tool calls
│   ├── context.py                   # Conversation context management module
│   ├── schemas.py                   # Tool schemas and validation definitions
│   ├── integration.py               # Integration layer connecting MCP tools to existing todo skills
│   ├── config.py                    # Configuration management for MCP server
│   └── __init__.py                  # Package initialization
└── tests/
    └── mcp/                         # MCP-specific tests
        ├── test_server.py           # Server functionality tests
        ├── test_tools.py            # Individual tool tests
        └── test_integration.py      # Integration tests
```

**Structure Decision**: Backend component extending existing architecture with dedicated mcp/ module for Model Context Protocol implementation. This maintains separation of concerns while integrating with existing todo skills and authentication patterns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [Not Applicable] | [All constitution checks passed] |
