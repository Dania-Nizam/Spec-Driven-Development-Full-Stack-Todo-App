# Data Model: Frontend Specifications for Todo Web Application

## Core Entities

### Task
**Purpose**: Represents a todo item managed by the frontend application

```typescript
interface Task {
  id: string;                    // Unique identifier for the task
  title: string;                 // Title of the task (required)
  description?: string;          // Optional description of the task
  completed: boolean;            // Completion status (true/false)
  created_at: string;            // ISO 8601 timestamp when task was created
  updated_at: string;            // ISO 8601 timestamp when task was last updated
  user_id: string;               // ID of the user who owns this task
}
```

**Validation Rules**:
- `id`: Required, UUID format
- `title`: Required, 1-200 characters
- `description`: Optional, 0-1000 characters
- `completed`: Required, boolean
- `created_at`: Required, ISO 8601 format
- `updated_at`: Required, ISO 8601 format
- `user_id`: Required, UUID format

### User Session
**Purpose**: Represents the authenticated user session state

```typescript
interface UserSession {
  user_id: string;               // Unique identifier for the authenticated user
  email: string;                 // User's email address
  token: string;                 // JWT token for API authentication
  expires_at: string;            // ISO 8601 timestamp when token expires
}
```

**Validation Rules**:
- `user_id`: Required, UUID format
- `email`: Required, valid email format
- `token`: Required, JWT format
- `expires_at`: Required, ISO 8601 format

### API Response Format
**Purpose**: Standardized format for API responses

```typescript
interface ApiResponse<T> {
  data?: T;                      // Response data (optional for error responses)
  error?: string;                // Error message (present on error responses)
}
```

### Task Form Data
**Purpose**: Structure for task creation/update form submissions

```typescript
interface TaskFormData {
  title: string;                 // Title of the task (required)
  description?: string;          // Optional description of the task
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, 0-1000 characters

## State Management

### Task State
**Purpose**: Application state for managing tasks

```typescript
type TaskState = {
  tasks: Task[];                 // List of user's tasks
  loading: boolean;              // Loading state indicator
  error: string | null;          // Error message if any
  selectedTask: Task | null;     // Currently selected task for editing
}
```

### UI State
**Purpose**: State for UI components

```typescript
type UIState = {
  darkMode: boolean;             // Dark/light mode preference
  mobileMenuOpen: boolean;       // Mobile navigation menu state
  toastOpen: boolean;            // Toast notification visibility
  toastMessage: string;          // Toast notification message
}
```

## API Integration Models

### API Configuration
**Purpose**: Configuration for API calls

```typescript
interface ApiConfig {
  baseUrl: string;               // Base URL for API calls
  headers: Record<string, string>; // Default headers for API requests
}
```

### API Error Response
**Purpose**: Standardized format for error responses from the API

```typescript
interface ApiErrorResponse {
  error: string;                 // Error message from the API
}
```

## Frontend-Specific Data Structures

### Component Props
**Purpose**: Props for reusable components

```typescript
interface TaskCardProps {
  task: Task;                    // Task data to display
  onToggleComplete: (id: string) => void; // Callback for toggling completion
  onEdit: (task: Task) => void;  // Callback for editing the task
  onDelete: (id: string) => void; // Callback for deleting the task
}
```

### Loading States
**Purpose**: Loading state representations

```typescript
type LoadingState = 'idle' | 'loading' | 'success' | 'error';

interface LoadingStateWithMessage {
  state: LoadingState;
  message?: string;
}
```