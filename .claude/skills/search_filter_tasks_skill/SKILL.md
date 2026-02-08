# Search and Filter Tasks Skill

This skill searches and filters todo tasks via the backend API.

## Description
Searches and filters the user's todo tasks using the backend API with JWT authentication.

## Parameters
- `query` (string, optional): Search term to match in task titles or descriptions
- `filter_status` (string, optional): Filter tasks by status (pending, in_progress, completed)
- `filter_priority` (string, optional): Filter tasks by priority (low, medium, high)
- `filter_due_date_from` (string, optional): Filter tasks with due date on or after YYYY-MM-DD
- `filter_due_date_to` (string, optional): Filter tasks with due date on or before YYYY-MM-DD
- `tags` (array, optional): Filter tasks by tags
- `sort_by` (string, optional): Sort tasks by (title, due_date, priority, created_at)
- `order` (string, optional): Sort order (asc, desc)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `tasks` (array): Array of matching task objects

## Example Usage
```python
result = search_filter_tasks_skill({
    "query": "groceries",
    "filter_priority": "high"
})
```