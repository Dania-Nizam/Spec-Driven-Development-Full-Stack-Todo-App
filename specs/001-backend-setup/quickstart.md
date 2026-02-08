# Quickstart Guide: Backend API Development

## Prerequisites

### System Requirements
- Python 3.11+
- pip package manager
- Git version control
- Access to Neon PostgreSQL instance

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend/
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Installation

### Backend Dependencies
Install the required Python packages:

```bash
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] psycopg2-binary uvicorn pytest httpx python-multipart
```

### Environment Variables
Create a `.env` file in the backend directory with the following variables:

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models/              # SQLModel database models
│   ├── __init__.py
│   ├── user.py          # User model
│   └── task.py          # Task model
├── schemas/             # Pydantic schemas for API
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── api/                 # API routes and endpoints
│   ├── __init__.py
│   ├── deps.py          # Dependencies (JWT verification)
│   └── tasks.py         # Task endpoints
├── database/            # Database setup and session management
│   ├── __init__.py
│   └── session.py
├── core/                # Core configuration
│   ├── __init__.py
│   └── config.py
└── tests/               # Backend API tests
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py     # Authentication tests
    └── test_tasks.py    # Task API tests
```

## Running the Application

### Start the Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Base API: http://localhost:8000

### Environment Configuration
Set the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/todo_db` |
| `BETTER_AUTH_SECRET` | Secret key for JWT signing | `my-super-secret-jwt-key` |
| `ENVIRONMENT` | Environment type | `development` |

## API Endpoints

All endpoints require JWT authentication and follow the canonical path structure:

### Task Management Endpoints

#### List all tasks for a user
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Authentication**: Required JWT token
- **Path Parameter**: `{user_id}` - authenticated user ID
- **Response**: `200 OK` with array of Task objects

#### Create a new task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Authentication**: Required JWT token
- **Path Parameter**: `{user_id}` - authenticated user ID
- **Request Body**: Task creation schema
- **Response**: `201 Created` with created Task object

#### Get a specific task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Authentication**: Required JWT token
- **Path Parameters**: `{user_id}`, `{id}` - task ID
- **Response**: `200 OK` with Task object or `404 Not Found`

#### Update a task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Authentication**: Required JWT token
- **Path Parameters**: `{user_id}`, `{id}` - task ID
- **Request Body**: Task update schema
- **Response**: `200 OK` with updated Task object or `404 Not Found`

#### Delete a task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Authentication**: Required JWT token
- **Path Parameters**: `{user_id}`, `{id}` - task ID
- **Response**: `200 OK` on success or `404 Not Found`

#### Toggle task completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Authentication**: Required JWT token
- **Path Parameters**: `{user_id}`, `{id}` - task ID
- **Response**: `200 OK` with updated Task object or `404 Not Found`

## Authentication

### JWT Token Format
The backend expects JWT tokens in the Authorization header:

```
Authorization: Bearer <jwt_token_here>
```

### JWT Claims Expected
- `sub` (subject): User ID as integer
- `email`: User's email address
- `exp` (expiration): Token expiration timestamp

### Error Responses
- **Unauthorized**: `401 {"error": "unauthorized"}`
- **User ID Mismatch**: `403 {"error": "user_id_mismatch"}`
- **Not Found**: `404 {"error": "not_found"}`

## Running Tests

### Execute All Tests
```bash
pytest
```

### Execute Tests with Coverage
```bash
pytest --cov=.
```

### Execute Specific Test File
```bash
pytest tests/test_tasks.py
```

## Database Management

### Initialize Database
The application automatically creates tables on startup if they don't exist.

### Migration Strategy
For production deployments, use Alembic for database migrations:

```bash
# Install alembic
pip install alembic

# Initialize alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Development Workflow

### 1. Setting Up Local Development
1. Create virtual environment
2. Install dependencies
3. Configure environment variables
4. Run database migrations
5. Start development server

### 2. Adding New Features
1. Update data models in `models/`
2. Create/update schemas in `schemas/`
3. Implement API endpoints in `api/`
4. Add tests in `tests/`
5. Verify functionality with interactive docs

### 3. Testing Checklist
- [ ] All endpoints require authentication
- [ ] User isolation is enforced (user_id matching)
- [ ] Proper error responses are returned
- [ ] Database operations work correctly
- [ ] JWT verification functions properly

## Troubleshooting

### Common Issues

**Issue**: Database connection fails
- **Solution**: Verify DATABASE_URL is correctly formatted and accessible

**Issue**: JWT authentication fails
- **Solution**: Check that BETTER_AUTH_SECRET matches between frontend and backend

**Issue**: User isolation not working
- **Solution**: Verify that all endpoints check {user_id} against JWT user_id

**Issue**: Endpoints return 404
- **Solution**: Check for trailing slashes in paths (not allowed per canonical rules)

## Production Deployment

### Environment Variables for Production
```bash
DATABASE_URL=postgresql://production-db-url
BETTER_AUTH_SECRET=production-jwt-secret
ENVIRONMENT=production
LOG_LEVEL=info
```

### Recommended Production Commands
```bash
# Using uvicorn in production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using gunicorn with uvicorn worker
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Health Checks
- **Health Endpoint**: `GET /health` - Returns service status
- **Database Check**: Verifies database connectivity
- **Response**: `200 OK` with status information