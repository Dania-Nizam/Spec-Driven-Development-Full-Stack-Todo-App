# View Tasks Skill

This skill retrieves and lists todo tasks from the backend API.

## Description
Retrieves and lists the user's todo tasks using the backend API with JWT authentication.

## Parameters
- `filter_status` (string, optional): Filter tasks by status (pending, in_progress, completed)
- `filter_priority` (string, optional): Filter tasks by priority (low, medium, high)
- `sort_by` (string, optional): Sort tasks by (title, due_date, priority, created_at)
- `order` (string, optional): Sort order (asc, desc)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `tasks` (array): Array of task objects

## Example Usage
```python
result = view_tasks_skill({
    "filter_status": "pending",
    "sort_by": "due_date"
})
```