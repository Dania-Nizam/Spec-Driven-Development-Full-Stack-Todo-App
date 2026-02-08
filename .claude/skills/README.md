# Agent Skills for AI-Powered Todo Chatbot

This directory contains reusable agent skills for the AI-powered todo chatbot. Each skill is designed to perform a specific task related to managing todo items through the backend API.

## Available Skills

### 1. add_task_skill
Adds a new todo task to the user's task list.
- Parameters: title (required), description, priority, tags, due_date, recurrence
- Returns: success status, message, and task_id

### 2. delete_task_skill
Deletes a todo task from the user's task list.
- Parameters: task_id or title
- Returns: success status and message

### 3. update_task_skill
Updates an existing todo task in the user's task list.
- Parameters: task_id (required), title, description, priority, tags, due_date, recurrence, status
- Returns: success status and message

### 4. view_tasks_skill
Retrieves and lists the user's todo tasks.
- Parameters: filter_status, filter_priority, sort_by, order
- Returns: success status, message, and tasks array

### 5. mark_complete_skill
Marks a todo task as complete or incomplete.
- Parameters: task_id (required), complete (required)
- Returns: success status and message

### 6. search_filter_tasks_skill
Searches and filters the user's todo tasks.
- Parameters: query, filter_status, filter_priority, filter_due_date_from, filter_due_date_to, tags, sort_by, order
- Returns: success status, message, and tasks array

### 7. set_recurring_skill
Sets or updates the recurring pattern of a todo task.
- Parameters: task_id (required), recurrence_pattern (required), recurrence_end_date, recurrence_interval
- Returns: success status and message

### 8. auth_check_skill
Verifies JWT authentication and returns the user ID.
- Parameters: token (required)
- Returns: success status, message, and user_id

### 9. get_task_context_skill
Retrieves recent task context for follow-up conversations.
- Parameters: user_id (required), limit, include_completed
- Returns: success status, message, and context array

## Integration with OpenAI Assistant API

Each skill comes with a `get_openai_tool_definition()` function that returns the appropriate JSON schema for registering the function as a tool with the OpenAI Assistant API.

## Usage Example

```python
from .skills import (
    add_task_skill,
    view_tasks_skill,
    get_all_tool_definitions
)

# Get all tool definitions to register with OpenAI Assistant
tools = get_all_tool_definitions()

# Or use a specific skill directly
result = add_task_skill({
    "title": "Buy groceries",
    "description": "Buy milk, bread, and eggs",
    "priority": "medium",
    "due_date": "2026-02-05"
})
```

## Authentication

All skills that interact with the backend API require JWT authentication. The skills expect the `BETTER_AUTH_TOKEN` environment variable to be set with a valid JWT token.

## Error Handling

All skills follow a consistent error handling pattern:
- Always return a dictionary with a `success` boolean field
- Include a `message` field with a descriptive status message
- Include additional fields as needed for successful operations

## Environment Variables

Skills require the following environment variables:
- `BETTER_AUTH_TOKEN`: JWT token for API authentication
- `BACKEND_BASE_URL`: Base URL of the backend API (default: http://localhost:8000)
- `OPENAI_API_KEY`: API key for OpenAI services