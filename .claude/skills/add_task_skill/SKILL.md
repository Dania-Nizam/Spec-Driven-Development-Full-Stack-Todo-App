# Add Task Skill

This skill adds a new todo task via the backend API.

## Description
Adds a new todo task to the user's task list using the backend API with JWT authentication.

## Parameters
- `title` (string, required): The title of the task
- `description` (string, optional): Detailed description of the task
- `priority` (string, optional): Priority level (low, medium, high)
- `tags` (array, optional): Array of tag strings
- `due_date` (string, optional): Due date in YYYY-MM-DD format
- `recurrence` (string, optional): Recurrence pattern (daily, weekly, monthly, yearly)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `task_id` (string, optional): ID of the created task if successful

## Example Usage
```python
result = add_task_skill({
    "title": "Buy groceries",
    "description": "Buy milk, bread, and eggs",
    "priority": "medium",
    "due_date": "2026-02-05"
})
```