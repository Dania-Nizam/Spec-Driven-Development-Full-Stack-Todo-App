# Get Task Context Skill

This skill retrieves recent task context for follow-up conversations.

## Description
Retrieves recent task context to provide continuity in conversations with the AI assistant.

## Parameters
- `user_id` (string, required): The ID of the user whose task context to retrieve
- `limit` (integer, optional): Maximum number of recent tasks to return (default: 5)
- `include_completed` (boolean, optional): Whether to include completed tasks (default: false)

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `context` (array): Array of recent task objects with context

## Example Usage
```python
result = get_task_context_skill({
    "user_id": "1",
    "limit": 3,
    "include_completed": true
})
```