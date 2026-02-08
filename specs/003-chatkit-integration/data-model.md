# Data Model: AI Chatbot Backend Orchestration

## Entities

### ChatRequest
Represents the input from the frontend chat interface to the backend orchestration system.

**Fields:**
- message: string (the user's natural language input)
- sessionId: Optional[string] (identifier for maintaining conversation context)
- timestamp: datetime (when the request was received)

**Validation Rules:**
- message must be 1-2000 characters
- sessionId must be valid UUID format if provided
- timestamp must be in the present or past

### ChatResponse
Represents the response from the backend orchestration system to the frontend.

**Fields:**
- response: string (the chatbot's response to the user's message)
- sessionId: string (session identifier for maintaining conversation context)
- taskId: Optional[string] (ID of any task created/modified by the message)
- intent: Optional[string] (detected intent from the user's message, e.g., 'add_task', 'view_tasks', 'update_task')
- success: bool (indicates whether the operation was successful)

**Validation Rules:**
- response must be 1-5000 characters
- sessionId must be valid UUID format
- taskId must be valid integer string if provided
- intent must be one of predefined values if provided

### ChatSession
Represents a user's chat interaction, containing message history and metadata (may be extended later).

**Fields:**
- id: string (unique identifier for the session)
- userId: string (authenticated user ID from JWT)
- createdAt: datetime (timestamp when session started)
- updatedAt: datetime (timestamp of last activity)
- isActive: bool (whether session is currently active)
- metadata: Dict[str, Any] (additional session data)

**Validation Rules:**
- id must be unique
- userId must be present and valid
- createdAt must be in the past
- updatedAt must be >= createdAt
- isActive must be boolean

### ChatMessage
Represents individual messages in the conversation, including content, sender type, timestamp, and status (may be extended later).

**Fields:**
- id: string (unique identifier for the message)
- sessionId: string (reference to parent ChatSession)
- content: string (message text content)
- sender: Union['user', 'bot'] (identifies message origin)
- timestamp: datetime (when message was sent/received)
- status: Union['sent', 'delivered', 'error', 'processing'] (delivery status)

**Validation Rules:**
- id must be unique
- sessionId must reference valid ChatSession
- content must be non-empty
- sender must be either 'user' or 'bot'
- timestamp must be present
- status must be one of the defined values

## State Transitions

### ChatMessage Status Transitions
1. Initial: `processing` (when message is being processed by orchestrator)
2. Success: `processing` → `delivered` (when response is ready)
3. Failure: `processing` → `error` (with error message)

### ChatSession Activity Transitions
1. Creation: `isActive: false` → `isActive: true` (when user starts chat)
2. Inactivity: `isActive: true` → `isActive: false` (after timeout or session end)

## Relationships

### ChatSession → ChatMessage
- One-to-many relationship
- ChatSession can have multiple ChatMessages
- Messages are associated with session but not deleted when session ends (for history)

## Data Validation

### Input Validation
- Message content: 1-2000 characters
- Session timeout: 30 minutes of inactivity
- Maximum concurrent sessions: 1 per user
- Content filtering: No HTML/JS injection allowed

### Security Constraints
- User isolation: Users can only access their own sessions and messages
- JWT validation: All operations require valid JWT token
- Rate limiting: Maximum 10 messages per minute per user
- Content sanitization: All user input sanitized before processing

## API Request/Response Models

### ChatAPIRequest
**Fields:**
- message: string (the user's message to send to the chatbot)
- sessionId: Optional[string] (optional session identifier for maintaining conversation context)

**Validation Rules:**
- message is required and must be between 1-2000 characters
- sessionId is optional, valid UUID format if provided

### ChatAPIResponse
**Fields:**
- response: string (the chatbot's response to the user's message)
- sessionId: string (session identifier for maintaining conversation context)
- taskId: Optional[string] (optional ID of any task created/modified by the message)
- intent: Optional[string] (detected intent from the user's message)

**Validation Rules:**
- response is required and must be between 1-5000 characters
- sessionId is required and must be valid UUID format
- taskId is optional, valid integer string if provided
- intent is optional, must be one of predefined values if provided