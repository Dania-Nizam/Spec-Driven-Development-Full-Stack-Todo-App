# Set Recurring Skill

This skill sets or updates the recurring pattern of a todo task via the backend API.

## Description
Sets or updates the recurring pattern of a todo task using the backend API with JWT authentication.

## Parameters
- `task_id` (string, required): The ID of the task to update
- `recurrence_pattern` (string, required): The recurrence pattern (daily, weekly, monthly, yearly)
- `recurrence_end_date` (string, optional): End date for the recurrence in YYYY-MM-DD format
- `recurrence_interval` (integer, optional): Interval for the recurrence (e.g., every 2 weeks)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message

## Example Usage
```python
result = set_recurring_skill({
    "task_id": "123",
    "recurrence_pattern": "weekly",
    "recurrence_interval": 2
})
```