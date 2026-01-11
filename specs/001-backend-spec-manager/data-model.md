# Data Model Specification: Backend API

## Overview
This document defines the database schema for the multi-user todo application with strict user isolation.

## Entity Models

### User Model
**Entity Name**: User

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
  - Type: int
  - Constraints: Primary Key, Auto-increment
  - Description: Unique identifier for each user
- `email`: String (Unique, Indexed)
  - Type: str
  - Constraints: Unique, Indexed, Required
  - Description: User's email address used for identification
- `created_at`: DateTime
  - Type: datetime
  - Constraints: Required, Auto-populated
  - Description: Timestamp when the user account was created

**Relationships**:
- One-to-Many with Task model (CASCADE delete)
  - Relationship: `user.tasks` → List of Task objects
  - Foreign Key: `task.user_id` references `user.id`
  - Delete Rule: CASCADE (deleting a user deletes all their tasks)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Email cannot be null or empty

### Task Model
**Entity Name**: Task

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
  - Type: int
  - Constraints: Primary Key, Auto-increment
  - Description: Unique identifier for each task
- `title`: String
  - Type: str
  - Constraints: Required
  - Description: Title or name of the task
- `description`: String (Optional)
  - Type: str
  - Constraints: Optional, Nullable
  - Description: Detailed description of the task
- `completed`: Boolean
  - Type: bool
  - Constraints: Required, Default: False
  - Description: Whether the task has been completed
- `user_id`: Integer (Foreign Key)
  - Type: int
  - Constraints: Required, Foreign Key to User.id
  - Description: Reference to the user who owns this task
- `created_at`: DateTime
  - Type: datetime
  - Constraints: Required, Auto-populated
  - Description: Timestamp when the task was created
- `updated_at`: DateTime
  - Type: datetime
  - Constraints: Required, Auto-populated and updated
  - Description: Timestamp when the task was last updated

**Relationships**:
- Many-to-One with User model
  - Relationship: `task.user` → User object
  - Foreign Key: `task.user_id` references `user.id`
  - Delete Rule: CASCADE (if user is deleted, all tasks are deleted)

**Validation Rules**:
- Title cannot be null or empty
- Completed field defaults to False if not specified
- user_id must reference an existing user
- All tasks must belong to a valid user (foreign key constraint)

**State Transitions**:
- New task: `completed = False`
- Completed task: `completed = True`
- Uncompleted task: `completed = False`

## Indexing Strategy

### Required Indexes
1. **User.email** (Unique Index)
   - Purpose: Enable fast user lookup by email for authentication
   - Type: Unique Index
   - Fields: email

2. **Task.user_id** (Standard Index)
   - Purpose: Enable efficient per-user queries for user isolation
   - Type: Standard Index
   - Fields: user_id

3. **Task.user_id + Task.completed** (Composite Index)
   - Purpose: Enable efficient queries for filtered views (e.g., completed/uncompleted tasks per user)
   - Type: Composite Index
   - Fields: user_id, completed

## Database Constraints

### Referential Integrity
- Foreign Key Constraint: `task.user_id` references `user.id`
- Delete Rule: CASCADE (removes all tasks when user is deleted)
- Action Rule: RESTRICT (prevents deletion of user if referenced by other entities)

### Uniqueness Constraints
- User.email: Must be unique across all users

### Check Constraints
- Task.title: Cannot be empty or null
- Task.user_id: Must reference an existing user

## Data Access Patterns

### Required Queries
1. **List all tasks for a specific user**
   - Query: SELECT * FROM task WHERE user_id = :user_id
   - Index Used: Task.user_id
   - Expected Performance: O(log n) due to indexing

2. **Get a specific task for a specific user**
   - Query: SELECT * FROM task WHERE user_id = :user_id AND id = :task_id
   - Index Used: Task.user_id
   - Expected Performance: O(log n) due to indexing

3. **Create a new task for a user**
   - Query: INSERT INTO task (title, description, completed, user_id, created_at, updated_at) VALUES (:title, :description, :completed, :user_id, NOW(), NOW())
   - Validation: Ensure user_id exists
   - Expected Performance: O(log n) for insertion

4. **Update a specific task for a specific user**
   - Query: UPDATE task SET title=:title, description=:description, completed=:completed, updated_at=NOW() WHERE user_id = :user_id AND id = :task_id
   - Index Used: Task.user_id
   - Expected Performance: O(log n) for update

5. **Delete a specific task for a specific user**
   - Query: DELETE FROM task WHERE user_id = :user_id AND id = :task_id
   - Index Used: Task.user_id
   - Expected Performance: O(log n) for deletion

## Security Considerations

### Data Isolation
- All queries must be filtered by user_id to ensure user isolation
- No cross-user data access is allowed
- Database-level constraints support application-level security

### Audit Trail
- created_at and updated_at fields provide temporal information
- These fields are automatically managed by the application layer

## Migration Strategy

### Initial Schema Creation
1. Create User table
2. Create Task table
3. Establish foreign key relationship
4. Create required indexes
5. Set up constraints

### Future Extension Points
- Additional user profile fields (separate table to maintain normalization)
- Task categories/tags (many-to-many relationship)
- Task sharing functionality (would require careful security consideration)