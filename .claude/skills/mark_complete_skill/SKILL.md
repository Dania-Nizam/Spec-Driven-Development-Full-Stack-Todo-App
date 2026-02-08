# Mark Complete Skill

This skill marks a todo task as complete or incomplete via the backend API.

## Description
Marks a todo task as complete or incomplete using the backend API with JWT authentication.

## Parameters
- `task_id` (string, required): The ID of the task to update
- `complete` (boolean, required): Whether to mark the task as complete (true) or incomplete (false)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message

## Example Usage
```python
result = mark_complete_skill({
    "task_id": "123",
    "complete": True
})
```