# Auth Check Skill

This skill verifies JWT authentication and returns the user ID.

## Description
Verifies the validity of a JWT token and extracts the user ID for subsequent API calls.

## Parameters
- `token` (string, required): The JWT token to verify

## Returns
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `user_id` (string, optional): The extracted user ID if authentication succeeds

## Example Usage
```python
result = auth_check_skill({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
})
```