# Frontend Authentication Integration Specification

## Better Auth Setup

### Configuration
- **Library**: Better Auth client for Next.js 16+ App Router
- **Environment**: Use shared `BETTER_AUTH_SECRET` from backend configuration
- **Provider**: Configure as authentication provider in root layout or app context
- **Session Management**: Implement client-side session state using Better Auth hooks

### Client Initialization
- **Location**: Initialize Better Auth client in `app/providers.tsx` or similar provider component
- **Configuration**: Set up with backend API endpoint and shared secret
- **Middleware**: Configure Next.js middleware for server-side session validation

## Authentication Flows

### Login Flow
- **Trigger**: User submits credentials on `/login` page
- **Process**: Use Better Auth client to authenticate user credentials
- **Success**:
  - Acquire JWT token from Better Auth
  - Store in secure httpOnly cookies (preferred) or encrypted localStorage
  - Redirect to dashboard (`/`)
  - Show "Welcome back!" success toast
- **Failure**: Display specific error message from Better Auth (invalid credentials, etc.)

### Signup Flow
- **Trigger**: User submits registration on `/login` page (signup tab)
- **Process**: Use Better Auth client to register new user
- **Success**:
  - Create account and authenticate user
  - Acquire JWT token from Better Auth
  - Store in secure httpOnly cookies or encrypted localStorage
  - Redirect to dashboard (`/`)
  - Show "Account created successfully!" success toast
- **Failure**: Display specific error message from Better Auth (email exists, validation errors, etc.)

### Logout Flow
- **Trigger**: User clicks logout in navbar dropdown
- **Process**: Use Better Auth signOut hook/function
- **Actions**:
  - Clear all authentication tokens/cookies
  - Invalidate Better Auth session
  - Redirect to `/login`
  - Show "Logged out successfully" toast

## Session Management

### Token Storage
- **Preferred Method**: httpOnly cookies for maximum security (accessible only by server)
- **Fallback**: Encrypted localStorage with additional security measures if cookies unavailable
- **Encryption**: Use Next.js encryption methods if storing in localStorage
- **Expiry**: Respect JWT expiration time for automatic cleanup

### Session Validation
- **Client-Side**: Use Better Auth `useSession` hook for real-time session status
- **Server-Side**: Implement Next.js middleware for server-side rendering validation
- **API Integration**: Extract user_id from JWT/session for all API calls
- **Expiration Handling**: Monitor session expiry and auto-logout when expired

## API Security Integration

### Authorization Header Management
- **Centralized Client**: Create unified API client module that handles all requests
- **Automatic Attachment**: Interceptors automatically add `Authorization: Bearer {token}` to all requests
- **Token Refresh**: Automatic token refresh when needed using Better Auth client
- **Error Handling**: Intercept 401 responses and trigger auto-logout

### User ID Consistency
- **Source**: Always extract user_id from authenticated session/JWT (not URL parameters)
- **Path Construction**: Use extracted user_id for all API endpoint paths
- **Validation**: Verify that displayed data belongs to authenticated user
- **Mismatch Handling**: Detect and handle user_id mismatches gracefully

## Protected Route Implementation

### Client-Side Protection
- **Wrapper Component**: Create higher-order component or hook for protected routes
- **Session Check**: Check Better Auth session before rendering protected content
- **Redirect Logic**: Redirect to `/login` if session is invalid or expired
- **Loading State**: Show loading indicator while checking session status

### Server-Side Protection
- **Next.js Middleware**: Implement middleware to check authentication server-side
- **SSR Support**: Ensure protected content is not rendered if unauthenticated
- **SEO Benefits**: Proper HTTP status codes for search engine optimization

## Error Handling for Security

### Authentication Errors (401)
- **Detection**: Intercept 401 responses from API calls
- **Action**: Clear all tokens → redirect to `/login` → show "Session expired" toast
- **Automatic**: Trigger without user interaction after detection

### Authorization Errors (403)
- **Detection**: Intercept 403 responses from API calls
- **Action**: Show "Access denied" toast → refresh current view or redirect to dashboard
- **User ID Mismatch**: Specifically handle cases where path user_id doesn't match session user_id

### Token Expiration
- **Pre-emptive**: Monitor JWT expiry time and refresh before expiration
- **Reactive**: Handle 401 responses as token expiration signals
- **User Experience**: Seamless refresh without disrupting user workflow

## Security Best Practices

### Secure Token Handling
- **Transport**: Always use HTTPS for token transmission
- **Storage**: Prefer httpOnly cookies over localStorage when possible
- **Access**: Limit token access to necessary components only
- **Cleanup**: Clear tokens on logout, tab close, or session end

### Session Hijacking Prevention
- **Short-lived Tokens**: Use short-lived JWTs with refresh tokens
- **Origin Checks**: Validate request origins where possible
- **Rate Limiting**: Implement rate limiting for authentication endpoints
- **Monitoring**: Log authentication-related events for security monitoring

## Integration Points

### Next.js App Router Integration
- **Providers**: Wrap application with Better Auth provider in root layout
- **Hooks**: Use Better Auth hooks (`useSession`, `useSignOut`, etc.) throughout app
- **Server Components**: Use Better Auth server functions for server-side validation
- **Client Components**: Use Better Auth client functions for client-side operations

### Component Integration
- **Navbar**: Show user info and logout when authenticated
- **Protected Pages**: Implement protection logic using Better Auth session
- **API Calls**: Automatically include authorization headers via centralized client
- **Error Boundaries**: Handle authentication errors gracefully in UI