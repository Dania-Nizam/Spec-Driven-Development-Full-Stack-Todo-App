# Implementation Tasks: Backend API Implementation

## Feature Overview
Secure, production-ready FastAPI backend with Neon PostgreSQL storage and strict multi-user isolation via JWT — implementing all 5 Basic Level Todo features as REST API.

**Feature**: Backend API Implementation
**Branch**: 001-backend-spec-manager
**Spec**: /specs/001-backend-spec-manager/spec.md

## Implementation Strategy
Build the backend in incremental phases, starting with foundational components (setup, models, authentication) followed by individual user stories for each CRUD operation. Each phase delivers a testable increment.

**MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (Create Task) = Minimal working API with user isolation

## Phase 1: Setup (Project Initialization)

### Goal
Initialize the project structure with all necessary configurations and dependencies.

### Independent Test Criteria
- Project structure matches plan.md
- Dependencies can be installed
- Development server starts without errors
- Database connection can be established

### Implementation Tasks

- [X] T001 Create backend directory structure with all subdirectories
- [X] T002 [P] Create requirements.txt with all required dependencies
- [X] T003 [P] Initialize main.py with basic FastAPI app
- [X] T004 [P] Set up virtual environment and install dependencies
- [X] T005 [P] Create .env file template with required environment variables

## Phase 2: Foundational (Blocking Prerequisites)

### Goal
Implement core infrastructure components that all user stories depend on.

### Independent Test Criteria
- Database models can be created and queried
- JWT authentication works correctly
- User isolation is enforced at the database level
- Core configuration is loaded properly

### Implementation Tasks

- [X] T010 [P] Implement User SQLModel in backend/models/user.py
- [X] T011 [P] Implement Task SQLModel in backend/models/task.py
- [X] T012 [P] Create Pydantic schemas for User in backend/schemas/user.py
- [X] T013 [P] Create Pydantic schemas for Task in backend/schemas/task.py
- [X] T014 [P] Set up database session management in backend/database/session.py
- [X] T015 [P] Create JWT dependency for authentication in backend/api/deps.py
- [X] T016 [P] Implement JWT verification utility functions in backend/core/security.py
- [X] T017 [P] Create core configuration in backend/core/config.py
- [X] T018 Create database engine and session setup in backend/database/__init__.py
- [X] T019 Create models package init in backend/models/__init__.py
- [X] T020 Create schemas package init in backend/schemas/__init__.py
- [X] T021 Create database package init in backend/database/__init__.py
- [X] T022 Create core package init in backend/core/__init__.py
- [X] T023 Create API package init in backend/api/__init__.py

## Phase 3: [US1] Create Task (Add Task Feature)

### Goal
Implement task creation functionality with user isolation and validation.

### Independent Test Criteria
- User can create a new task with title and optional description
- Task is associated with the authenticated user
- Validation prevents creation of tasks without title
- User isolation prevents creation for another user

### Implementation Tasks

- [X] T025 [US1] Create POST endpoint for creating tasks in backend/api/tasks.py
- [X] T026 [US1] Implement task creation logic with user association
- [X] T027 [US1] Add request validation for task creation
- [X] T028 [US1] Ensure user_id from JWT matches path parameter
- [X] T029 [US1] Set default values for new tasks (completed=False)
- [X] T030 [US1] Return proper response with created task and 201 status

## Phase 4: [US2] List Tasks (View Task List Feature)

### Goal
Implement task listing functionality with user isolation and filtering.

### Independent Test Criteria
- User can list all their tasks
- User cannot see tasks from other users
- Tasks are ordered by creation date
- Filtering by completion status works (optional)

### Implementation Tasks

- [X] T035 [US2] Create GET endpoint for listing tasks in backend/api/tasks.py
- [X] T036 [US2] Implement task listing logic with user filtering
- [X] T037 [US2] Add ordering by creation date (descending)
- [X] T038 [US2] Ensure user_id from JWT matches path parameter
- [X] T039 [US2] Return proper response with task list

## Phase 5: [US3] Get Single Task (View Details Feature)

### Goal
Implement retrieving a single task with user isolation.

### Independent Test Criteria
- User can retrieve a specific task they own
- User cannot retrieve tasks from other users
- Proper 404 response when task not found
- Proper 403 response when user_id mismatch

### Implementation Tasks

- [X] T040 [US3] Create GET endpoint for getting a single task in backend/api/tasks.py
- [X] T041 [US3] Implement task retrieval logic with user validation
- [X] T042 [US3] Ensure user_id from JWT matches path parameter
- [X] T043 [US3] Return proper response with task details
- [X] T044 [US3] Handle 404 when task not found for user

## Phase 6: [US4] Update Task (Modify Task Feature)

### Goal
Implement task updating functionality with user isolation.

### Independent Test Criteria
- User can update their own tasks
- User cannot update tasks from other users
- Only provided fields are updated
- Updated timestamp is properly set

### Implementation Tasks

- [X] T045 [US4] Create PUT endpoint for updating tasks in backend/api/tasks.py
- [X] T046 [US4] Implement task update logic with user validation
- [X] T047 [US4] Ensure user_id from JWT matches path parameter
- [X] T048 [US4] Update only provided fields and set updated_at
- [X] T049 [US4] Return proper response with updated task

## Phase 7: [US5] Delete Task (Remove Task Feature)

### Goal
Implement task deletion functionality with user isolation.

### Independent Test Criteria
- User can delete their own tasks
- User cannot delete tasks from other users
- Proper response is returned on successful deletion
- Associated data is properly cleaned up

### Implementation Tasks

- [X] T050 [US5] Create DELETE endpoint for deleting tasks in backend/api/tasks.py
- [X] T051 [US5] Implement task deletion logic with user validation
- [X] T052 [US5] Ensure user_id from JWT matches path parameter
- [X] T053 [US5] Return proper response on successful deletion
- [X] T054 [US5] Ensure cascade deletion works properly

## Phase 8: [US6] Mark as Complete (Toggle Completion Feature)

### Goal
Implement task completion toggling functionality with user isolation.

### Independent Test Criteria
- User can toggle completion status of their tasks
- User cannot modify completion status of other users' tasks
- Updated timestamp is properly set
- Proper response with updated task is returned

### Implementation Tasks

- [X] T055 [US6] Create PATCH endpoint for toggling task completion in backend/api/tasks.py
- [X] T056 [US6] Implement completion toggle logic with user validation
- [X] T057 [US6] Ensure user_id from JWT matches path parameter
- [X] T058 [US6] Toggle completion status and update updated_at
- [X] T059 [US6] Return proper response with updated task

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Add error handling, validation, documentation, and testing to complete the implementation.

### Independent Test Criteria
- All endpoints return proper error responses
- API documentation is available via Swagger UI
- All security requirements are met
- Canonical path rules are enforced

### Implementation Tasks

- [X] T060 Add proper error responses (401, 403, 404) to all endpoints
- [X] T061 [P] Add input validation with Pydantic schemas to all endpoints
- [X] T062 [P] Implement canonical path validation (no trailing slashes)
- [ ] T063 [P] Add rate limiting to all endpoints
- [ ] T064 [P] Add logging to all endpoints
- [ ] T065 [P] Add comprehensive API documentation with OpenAPI
- [X] T066 [P] Add database migrations support
- [X] T067 [P] Add comprehensive unit tests for all endpoints
- [X] T068 [P] Add integration tests for user isolation
- [X] T069 [P] Add health check endpoint
- [X] T070 [P] Add comprehensive README with API usage instructions

## Dependencies

### User Story Completion Order
- [US1] Create Task (Prerequisite for: [US3], [US4], [US5], [US6])
- [US2] List Tasks (Independent)
- [US3] Get Single Task (Depends on: [US1])
- [US4] Update Task (Depends on: [US1])
- [US5] Delete Task (Depends on: [US1])
- [US6] Mark as Complete (Depends on: [US1])

### Critical Path
Setup → Foundational → [US1] Create Task → [US6] Mark as Complete → Polish

## Parallel Execution Examples

### Per User Story
Each user story can be developed in parallel by different developers as they all work on the same backend/api/tasks.py file but implement different endpoints.

### Per Component Type
- Models: T010-T011 (User and Task models can be done in parallel)
- Schemas: T012-T013 (User and Task schemas can be done in parallel)
- Tests: T067-T068 (Unit and integration tests can be done in parallel)

## Quality Gates
- [ ] All tests pass
- [ ] Code follows PEP 8 standards
- [ ] Security requirements met (user isolation verified)
- [ ] API contract matches specification
- [ ] Performance requirements met