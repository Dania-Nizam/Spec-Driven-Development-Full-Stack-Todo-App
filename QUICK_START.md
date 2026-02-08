# Quick Start Guide - Hackathon II Implementation

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon recommended)
- OpenAI API key

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `backend/.env` file:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@host/database

# Authentication (generate a secure random string)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters

# OpenAI API
OPENAI_API_KEY=sk-proj-...your-key-here...

# Optional
ENVIRONMENT=development
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start Backend Server

```bash
cd backend
python main.py
```

The backend will:
- ✅ Create all database tables automatically (User, Task, Conversation, Message)
- ✅ Start on http://localhost:8000
- ✅ Load all routers (Auth, Tasks, Chat, Conversations)

**Expected Output:**
```
✅ Auth router loaded
✅ Tasks router loaded
✅ Chat router loaded
✅ Conversations router loaded
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will start on http://localhost:3000

## Testing the Implementation

### Test 1: User Registration & Login

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' \
  -c cookies.txt

# The access_token cookie will be saved in cookies.txt
```

### Test 2: Natural Language Chat (OpenAI Agent)

```bash
# Test adding a task via natural language
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "Add a task to buy groceries tomorrow"
  }'

# Expected response:
# {
#   "response": "I've added a task 'Buy groceries' with due date tomorrow.",
#   "session_id": "thread_abc123",
#   "conversation_context": {
#     "conversation_id": 1,
#     "thread_id": "thread_abc123"
#   },
#   "success": true
# }
```

### Test 3: View Tasks

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "Show me my tasks",
    "conversation_context": {
      "conversation_id": 1,
      "thread_id": "thread_abc123"
    }
  }'
```

### Test 4: Conversation History

```bash
# List all conversations
curl http://localhost:8000/api/conversations/ \
  -b cookies.txt

# Get messages from a conversation
curl http://localhost:8000/api/conversations/1/messages \
  -b cookies.txt
```

### Test 5: Complex Natural Language Queries

Try these messages to verify OpenAI Agent intelligence:

```bash
# Flexible phrasing
"I need to remember to call mom"
"Can you help me add a task for buying milk?"
"What do I need to do today?"
"Show me my high priority tasks"
"Mark the first task as done"
"Delete task number 2"
"Change task 3 to high priority"
```

## Verification Checklist

### Backend Verification

- [ ] Backend starts without errors
- [ ] All 4 routers load successfully
- [ ] Database tables are created (User, Task, Conversation, Message)
- [ ] Can register and login users
- [ ] JWT authentication works
- [ ] Chat endpoint responds to messages
- [ ] OpenAI Agent calls MCP tools correctly
- [ ] Messages are saved to database
- [ ] Conversation history can be retrieved

### Frontend Verification

- [ ] Frontend starts without errors
- [ ] Can navigate to login page
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Chat interface loads
- [ ] Can send messages
- [ ] Receives AI responses
- [ ] Conversation persists across page refresh
- [ ] Can view task list
- [ ] Tasks created via chat appear in task list

### Integration Verification

- [ ] Natural language understanding works (not just exact phrases)
- [ ] Tasks are created/updated/deleted via chat
- [ ] Conversation context is maintained
- [ ] Multiple conversations can be created
- [ ] User can only access their own data
- [ ] System works after server restart (stateless)

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### Issue: "Database connection failed"

**Solution:**
- Verify DATABASE_URL is correct
- Check if database exists
- Ensure database is accessible from your machine
- For Neon, check if IP is whitelisted

### Issue: "OpenAI API error"

**Solution:**
- Verify OPENAI_API_KEY is correct
- Check OpenAI account has credits
- Ensure API key has proper permissions

### Issue: "401 Unauthorized" on chat

**Solution:**
- Ensure you're sending the access_token cookie
- Check if JWT token is expired (default 30 minutes)
- Re-login to get fresh token

### Issue: "Conversation not found"

**Solution:**
- Ensure conversation_id is being sent in subsequent requests
- Check if conversation belongs to the authenticated user
- Verify conversation exists in database

### Issue: Tables not created

**Solution:**
```bash
# Restart backend to trigger table creation
cd backend
python main.py
```

## Database Inspection

To verify tables were created:

```sql
-- Connect to your database and run:
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- Should show:
-- user
-- task
-- conversation
-- message
```

## API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Next Steps After Testing

1. **Deploy Backend**
   - Deploy to Vercel/Railway/Render
   - Set environment variables in production
   - Update CORS settings for production domain

2. **Deploy Frontend**
   - Deploy to Vercel
   - Update API_URL to production backend
   - Configure Better Auth for production

3. **Monitor & Optimize**
   - Set up error logging (Sentry)
   - Monitor OpenAI API usage
   - Set up database backups
   - Configure rate limiting

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the HACKATHON_II_COMPLETE.md file
3. Check individual step completion files (STEP_1_COMPLETION.md, etc.)
4. Verify all environment variables are set correctly

---

**Ready to Test!** 🚀

Start with the backend setup, then test the chat endpoint with natural language queries.
