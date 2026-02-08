# Update Task Skill

This skill updates an existing todo task via the backend API.

## Description
Updates an existing todo task in the user's task list using the backend API with JWT authentication.

## Parameters
- `task_id` (string, optional): The ID of the task to update
- `title` (string, optional): New title of the task
- `description` (string, optional): New detailed description of the task
- `priority` (string, optional): New priority level (low, medium, high)
- `tags` (array, optional): New array of tag strings
- `due_date` (string, optional): New due date in YYYY-MM-DD format
- `recurrence` (string, optional): New recurrence pattern (daily, weekly, monthly, yearly)
- `status` (string, optional): New status (pending, in_progress, completed)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message

## Example Usage
```python
result = update_task_skill({
    "task_id": "123",
    "due_date": "2026-02-10",
    "priority": "high"
})
```