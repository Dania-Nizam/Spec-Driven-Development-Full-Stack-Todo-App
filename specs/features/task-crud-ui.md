# Frontend Feature – Task CRUD UI Flow

## Overview

This specification defines the complete user interface flow for managing tasks through Create, Read, Update, and Delete operations in the Todo application. All operations will be integrated with the backend API using JWT authentication.

## Task CRUD Operations

### 1. Add Task Operation

#### Flow
- **Trigger**: User clicks Floating Action Button (FAB) in bottom-right corner of dashboard
- **Modal Opening**: TaskForm modal opens with empty fields
- **Form Interaction**: User fills in task title (required) and description (optional)
- **Validation**: Real-time validation of input fields
- **Submission**: User clicks "Save Task" button
- **API Call**: POST request to `/api/{user_id}/tasks` with JWT token
- **UI Update**: New task appears in task list with success toast
- **Error Handling**: Display error message if submission fails

#### UI Elements
- **Floating Action Button**: Plus icon with "Add Task" tooltip
- **TaskForm Modal**: Pre-filled with empty values
- **Success Toast**: "Task created successfully" message
- **Error Toast**: Specific error message from API

#### API Integration
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Headers**: `Authorization: Bearer {JWT_TOKEN}`
- **Request Body**: `{ title: string, description?: string }`
- **Response**: Created task object with ID
- **Error Handling**: Catch and display specific API error messages

#### Loading States
- **Button Loading**: Spinner on save button during submission
- **Form Disable**: Disable form fields during submission
- **Toast Feedback**: Immediate visual feedback on completion

### 2. View Task List Operation

#### Flow
- **Initial Load**: Dashboard loads and fetches tasks from API
- **Display**: Tasks rendered as TaskCard components in responsive grid
- **Empty State**: Friendly message when no tasks exist
- **Loading State**: Skeleton cards during initial data fetch
- **Refresh**: Pull-to-refresh or refresh button for updated data

#### UI Elements
- **Task Cards**: Individual TaskCard components showing title, description, and status
- **Grid Layout**: Responsive grid adapting to screen size
- **Loading Skeletons**: Placeholder cards during data fetch
- **Empty State**: Illustration and message when no tasks exist

#### API Integration
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Headers**: `Authorization: Bearer {JWT_TOKEN}`
- **Response**: Array of task objects
- **Pagination**: Support for loading more tasks if needed

#### Performance
- **Initial Load**: Display cached data if available, then refresh with API
- **Caching**: Client-side caching for improved perceived performance
- **Error Recovery**: Retry mechanism for failed requests

### 3. Update Task Operation

#### Flow
- **Trigger**: User clicks edit icon (pencil) on a TaskCard
- **Modal Opening**: TaskForm modal opens with pre-filled task data
- **Form Interaction**: User modifies title and/or description
- **Validation**: Real-time validation of input fields
- **Submission**: User clicks "Update Task" button
- **API Call**: PUT request to `/api/{user_id}/tasks/{task_id}` with JWT token
- **UI Update**: Updated task reflects changes in task list with success toast
- **Error Handling**: Display error message if update fails

#### UI Elements
- **Edit Icon**: Pencil icon appearing on TaskCard hover
- **TaskForm Modal**: Pre-filled with existing task values
- **Success Toast**: "Task updated successfully" message
- **Error Toast**: Specific error message from API

#### API Integration
- **Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`
- **Headers**: `Authorization: Bearer {JWT_TOKEN}`
- **Request Body**: `{ title: string, description?: string }`
- **Response**: Updated task object
- **Error Handling**: Catch and display specific API error messages

#### Optimistic Updates
- **Immediate Feedback**: Update UI immediately, revert on error
- **Visual Indication**: Subtle visual cue during update process
- **Recovery**: Revert changes and display error if API call fails

### 4. Delete Task Operation

#### Flow
- **Trigger**: User clicks delete icon (trash) on a TaskCard
- **Confirmation**: Confirmation dialog appears with warning
- **Confirmation Action**: User confirms deletion
- **API Call**: DELETE request to `/api/{user_id}/tasks/{task_id}` with JWT token
- **UI Update**: Task removes from list with success toast
- **Cancellation**: User can cancel deletion at any time

#### UI Elements
- **Delete Icon**: Trash icon appearing on TaskCard hover
- **Confirmation Dialog**: Modal with warning message and confirm/cancel buttons
- **Success Toast**: "Task deleted successfully" message
- **Error Toast**: Specific error message from API

#### API Integration
- **Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`
- **Headers**: `Authorization: Bearer {JWT_TOKEN}`
- **Response**: Success confirmation
- **Error Handling**: Catch and display specific API error messages

#### Safety Measures
- **Confirmation**: Required confirmation for destructive action
- **Undo Option**: Potentially implement undo functionality
- **Visual Warning**: Clear indication of destructive nature

### 5. Mark Complete Operation

#### Flow
- **Trigger**: User clicks checkbox on a TaskCard
- **Immediate Feedback**: Visual change to indicate completion status
- **API Call**: PATCH request to `/api/{user_id}/tasks/{task_id}/complete` with JWT token
- **UI Update**: Task appearance updates to reflect completion status
- **Error Recovery**: Revert UI change if API call fails

#### UI Elements
- **Checkbox**: Interactive checkbox element on each TaskCard
- **Visual Feedback**: Strikethrough on title, faded appearance for completed tasks
- **Error Toast**: Specific error message from API if update fails

#### API Integration
- **Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`
- **Headers**: `Authorization: Bearer {JWT_TOKEN}`
- **Request Body**: `{ completed: boolean }`
- **Response**: Updated task object
- **Error Handling**: Revert UI state and display error if API call fails

#### Optimistic Updates
- **Instant Feedback**: Update UI immediately upon user action
- **Visual Cue**: Clear visual indication of state change
- **Recovery**: Revert to previous state if API call fails

## API Integration Details

### Better Auth Integration
- **Setup**: Configure Better Auth client in Next.js App Router with shared BETTER_AUTH_SECRET
- **Login Flow**: Use Better Auth client to authenticate user and acquire JWT token on successful login
- **Token Storage**: Store JWT in httpOnly cookies (preferred for security) or encrypted localStorage
- **Session Management**: Use Better Auth hooks (useSession, useSignOut) for session state management
- **User ID Extraction**: Extract authenticated user_id from Better Auth session for API path construction

### Authentication
- **JWT Token**: Obtain from Better Auth session, stored securely in httpOnly cookies or encrypted storage
- **Header Format**: `Authorization: Bearer {token}` applied to all API requests
- **Token Refresh**: Automatic refresh via Better Auth client when token expires
- **Error Handling**: Intercept 401 responses → auto logout → redirect to login with notification

### Centralized API Client
- **Implementation**: Create centralized API client module with request/response interceptors
- **Security Headers**: Automatically attach `Authorization: Bearer {token}` to all requests
- **Base URL**: Consistent base URL configuration for API endpoints
- **User ID Injection**: Use authenticated user_id from Better Auth session for all API paths

### Request Handling
- **HTTP Client**: Use fetch with centralized configuration or axios instance
- **Interceptors**: Implement request/response interceptors for:
  - Attaching Authorization header automatically
  - Handling 401/403/404 responses appropriately
  - Managing loading states globally
  - Parsing error responses consistently
- **Timeouts**: Set reasonable timeouts for API requests (10-30 seconds)
- **Retry Logic**: Implement retry mechanism for failed requests (except authentication errors)

### Error Handling
- **401 Unauthorized**: "Session expired. Redirecting to login..." toast → auto redirect to `/login` after 2 seconds
- **403 Forbidden**: "Access denied. You don't have permission for this action." toast → refresh task list or redirect to dashboard
- **404 Not Found**: "Task not found. Please refresh the page." toast with refresh option
- **400 Validation Error**: "Invalid input: [specific error from API]" with field highlighting
- **Network Errors**: "Connection failed. Please check your internet connection and try again." toast
- **Generic Errors**: "Something went wrong. Please try again later." toast
- **API Errors**: Parse and display specific error messages from API
- **Validation Errors**: Highlight fields with validation errors using proper feedback

### Session Management
- **Token Expiration**: Intercept 401 responses → auto logout → redirect to login
- **Secure Logout**: Clear all tokens/cookies → redirect to `/login` → show "Logged out successfully" toast
- **Protected Routes**: Client-side check using Better Auth session to redirect unauthenticated users
- **Path Validation**: Ensure all API calls use authenticated user_id from session (not URL parameters)

### Loading States
- **Global Loading**: Indicator for overall page loading
- **Component Loading**: Individual loading states for components
- **Optimistic Updates**: Immediate UI feedback where appropriate (with error recovery)
- **Skeleton Screens**: Placeholders during initial data loads
- **API Call States**: Visual feedback during all API operations

### Patch Complete Endpoint Update
- **Correct Method**: Use empty PATCH request to `/api/{user_id}/tasks/{task_id}/complete`
- **Request Body**: No request body required (empty payload)
- **Response Handling**: Toggle completion status in UI immediately, revert on error
- **Error Recovery**: If PATCH fails, revert UI to previous state and show error toast

## Responsive Behavior

### Mobile
- **Vertical Stack**: Tasks displayed in vertical stack
- **Fixed FAB**: Floating Action Button fixed at bottom-right
- **Full-width Cards**: Task cards spanning full screen width
- **Touch Targets**: Adequate sizing for touch interactions
- **Swipe Actions**: Potential for swipe gestures on task cards

### Desktop
- **Grid Layout**: Responsive grid for task cards
- **Sidebar Potential**: Space for additional navigation or filters
- **Hover States**: Visual feedback on interactive elements
- **Keyboard Navigation**: Full keyboard accessibility

### Breakpoints
- **Mobile**: Up to 768px width
- **Tablet**: 768px to 1024px width
- **Desktop**: Above 1024px width
- **Adjustments**: Layout adjustments at each breakpoint

## UX Polish

### Transitions
- **Smooth Animations**: CSS transitions for state changes
- **Page Transitions**: Smooth transitions between pages
- **Loading Animations**: Subtle animations during loading states
- **Feedback Animations**: Micro-interactions for user actions

### Optimistic Updates
- **Instant Feedback**: UI updates immediately on user action
- **Error Recovery**: Revert changes if API calls fail
- **Visual Cues**: Clear indication of pending operations
- **Performance**: Improved perceived performance

### Keyboard Navigation
- **Tab Order**: Logical tab order through interface elements
- **Keyboard Shortcuts**: Potential for common task operations
- **Focus Management**: Proper focus handling in modals and forms
- **Accessibility**: Full keyboard operability for all features

### Performance Optimization
- **Code Splitting**: Lazy loading for non-critical components
- **Image Optimization**: Proper image loading and optimization
- **Data Fetching**: Efficient data loading strategies
- **Memory Management**: Proper cleanup of event listeners and subscriptions

## Security Considerations

### Input Sanitization
- **Client Validation**: Input validation and sanitization on client
- **User Content**: Proper handling of user-generated content
- **Cross-site Scripting**: Prevention of XSS through proper escaping

### Data Protection
- **JWT Handling**: Secure storage and transmission of tokens
- **API Endpoints**: Proper authentication for all API calls
- **Privacy**: Respect user privacy in data handling

## Testing Considerations

### User Flows
- **Happy Path**: Test primary success scenarios
- **Error Paths**: Test error handling and recovery
- **Edge Cases**: Test boundary conditions and unusual inputs
- **Performance**: Test under various network conditions

### Accessibility
- **Screen Readers**: Test with screen reader software
- **Keyboard Navigation**: Test full keyboard operability
- **Color Contrast**: Verify sufficient color contrast ratios
- **Focus Management**: Test focus behavior in all components