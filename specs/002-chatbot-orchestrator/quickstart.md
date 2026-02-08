# Quickstart Guide: Chatbot Orchestrator for AI-Powered Todo Chatbot

## Prerequisites

- Python 3.13+ installed
- FastAPI and related dependencies installed
- Existing Phase II backend with JWT authentication configured
- Neon PostgreSQL database with existing schema
- OpenAI API key for agent orchestration

## Installation

1. Install required dependencies:
```bash
pip install fastapi uvicorn openai python-jose[cryptography] passlib[bcrypt] sqlmodel httpx
```

2. Install additional dependencies for skills framework:
```bash
pip install pydantic-settings
```

3. Install OpenAI Agents SDK:
```bash
pip install openai-agents-sdk
```

## Configuration

1. Set up environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
BETTER_AUTH_SECRET=your_jwt_secret_key
```

2. Register the chat router in your main FastAPI application (`backend/main.py`):
```python
from src.api.routes.chat import router as chat_router

app.include_router(chat_router, prefix="/api/{user_id}", tags=["chat"])
```

## API Endpoint

The chat endpoint is available at:
```
POST /api/{user_id}/chat
```

## Running the Service

1. Start the backend service:
```bash
uvicorn backend.main:app --reload --port 8000
```

2. The chat endpoint will be available at `http://localhost:8000/api/{user_id}/chat`

## Testing the Integration

1. Verify JWT authentication works by making a request without a token (should return 401):
```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

2. Test with a valid JWT token:
```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_valid_jwt_token" \
  -d '{"message": "Add a task to buy groceries"}'
```

3. Verify user isolation by attempting to access another user's chat endpoint with mismatched user_id (should return 403).

## Skill Registration

All todo operation skills must be registered with the ChatbotOrchestratorAgent:

- `add_task_skill`: Handles "Add task..." requests
- `delete_task_skill`: Handles "Delete task..." requests
- `update_task_skill`: Handles "Update task..." requests
- `view_tasks_skill`: Handles "Show tasks..." requests
- `mark_complete_skill`: Handles "Complete task..." requests
- `search_filter_tasks_skill`: Handles "Find tasks..." requests
- `set_recurring_skill`: Handles recurring task requests
- `auth_check_skill`: Handles authentication verification
- `get_task_context_skill`: Provides context for follow-up requests

## Troubleshooting

- **Authentication Issues**: Ensure JWT token is properly formatted and valid
- **User Isolation Issues**: Verify that the user_id in the path matches the authenticated user ID in the JWT
- **Skill Execution Issues**: Check that all required skills are properly registered with the orchestrator
- **Database Connection Issues**: Verify DATABASE_URL is properly configured
- **OpenAI API Issues**: Confirm OPENAI_API_KEY is valid and has proper permissions
- **Agent Orchestration Issues**: Ensure OpenAI Agents SDK is properly configured and initialized