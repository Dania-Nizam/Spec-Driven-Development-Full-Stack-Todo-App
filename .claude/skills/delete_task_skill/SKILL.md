# Delete Task Skill

This skill deletes a todo task via the backend API.

## Description
Deletes a todo task from the user's task list using the backend API with JWT authentication.

## Parameters
- `task_id` (string, optional): The ID of the task to delete
- `title` (string, optional): The title of the task to delete (if ID not provided)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message

## Example Usage
```python
result = delete_task_skill({
    "task_id": "123"
})
```