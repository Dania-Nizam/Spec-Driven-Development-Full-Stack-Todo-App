# Frontend Pages & Layout Specification

## App Structure

### Next.js App Router
- **Folder Structure**: `/app` directory following Next.js 16+ App Router conventions
- **Route Handlers**: Leverage React Server Components for initial data fetching where appropriate
- **Client Components**: Use 'use client' directive for interactive elements
- **Layout System**: Nested layouts with root layout containing global UI elements

## Root Layout

### Global Elements
- **Navbar**: Consistent header across all pages with app branding and user controls
- **Main Content Area**: Outlet for page-specific content with appropriate padding
- **Toaster**: Global notification container positioned top-right for all toast messages
- **Loading States**: Global loading indicators for data fetching

### Root Template
- **HTML Structure**: Proper HTML5 structure with lang attribute and meta tags
- **CSS Loading**: Tailwind CSS with dark mode configuration
- **Font Loading**: Preload Inter font or system font stack for performance

## Page Specifications

### /login Page (Authentication Page)

#### Purpose
Centralized authentication page for user login and signup with Better Auth integration.

#### Layout Structure
- **Container**: Centered card with maximum width constraint (max-w-md)
- **Background**: Light gray background with centered content
- **Responsive**: Full-screen height on mobile, centered card on desktop

#### Components Used
- **Card**: Main container for authentication form
- **Tabs** (optional): Separate tabs for login/signup or unified form
- **Input Fields**: Email and password inputs with proper validation
- **Button**: Submit button with loading state
- **Links**: Password reset and navigation links

#### Visual Design
- **Spacing**: Generous padding (p-8) inside card
- **Typography**: Clear heading with supporting text
- **Form Layout**: Vertical stack of form elements
- **Error Display**: Inline error messages with red color scheme

#### Responsive Behavior
- **Mobile**: Full-width card with vertical spacing
- **Desktop**: Fixed-width card centered on screen
- **Breakpoint**: Switch from full-screen to constrained width at md breakpoint

#### Features
- **Email Validation**: Real-time email format validation
- **Password Requirements**: Visibility of password strength or requirements
- **Error Handling**: Clear display of authentication errors
- **Loading States**: Button loading indicator during submission
- **Social Login**: Potential for social authentication providers

### / (Dashboard) Page (Protected Main Page)

#### Purpose
Authenticated user's main task management interface with comprehensive task overview.

#### Layout Structure
- **Top Navigation**: Fixed header with app name, user profile, and logout
- **Main Content**: Scrollable area with task list and floating action button
- **Responsive**: Adaptable layout for mobile and desktop

#### Components Used
- **Navbar**: Top navigation bar with user controls
- **Task Cards**: Individual task display components
- **Floating Action Button**: FAB for adding new tasks
- **Empty State**: Message when no tasks exist
- **Skeleton Loaders**: Loading placeholders during data fetch

#### Visual Design
- **Background**: Clean white/surface background
- **Task Spacing**: Consistent vertical spacing between task cards
- **Header**: Clear visual separation from content area
- **Footer**: Minimal footer with necessary links

#### Responsive Behavior
- **Mobile**: Single column layout, FAB fixed bottom-right
- **Tablet**: May expand to 2-column grid
- **Desktop**: Grid layout (2-3 columns) with sidebar potential
- **Breakpoints**:
  - Mobile: <768px
  - Tablet: 768px - 1024px
  - Desktop: >1024px

#### Features
- **Task Filtering**: Ability to filter tasks by status/completion
- **Search Capability**: Search across task titles/descriptions
- **Pagination**: Load more or pagination for large task lists
- **Quick Actions**: Swipe actions or quick buttons on mobile
- **Keyboard Shortcuts**: Support for common actions via keyboard

#### Empty State
- **Visual**: Friendly illustration or icon
- **Message**: Clear, encouraging message
- **CTA**: Prominent button to create first task

#### Loading States
- **Initial Load**: Skeleton screens for task cards
- **Refresh**: Subtle loading indicator
- **Error State**: Clear error message with retry option

## Protected Routes

### Authentication Guard
- **Redirect**: Unauthenticated users redirected to `/login`
- **Token Check**: Verify JWT validity via Better Auth session before allowing access
- **Session Management**: Handle token expiration gracefully with automatic logout

### Implementation
- **Better Auth Integration**: Use Better Auth client-side session management for initial auth state
- **Server-Side**: Leverage Better Auth's Next.js middleware for initial auth check on server for SEO/better UX
- **Client-Side**: Additional client-side protection layer using Better Auth hooks
- **User ID Extraction**: Extract authenticated user_id from JWT/session to populate API paths

### Session Protection
- **Middleware**: Implement protected route wrapper that checks Better Auth session
- **Path Validation**: Ensure all API calls use the authenticated user_id (extracted from session/JWT) rather than URL parameters
- **Automatic Redirect**: Redirect to login if session is invalid or expired

### Error Handling
- **Invalid Token**: Clear messaging and redirect to login with "Session expired" notification
- **Network Issues**: Graceful degradation with retry options
- **Expired Session**: Automatic redirect to login with notification and token cleanup
- **403 Forbidden**: "Access denied" notification with redirect to dashboard if user_id mismatch detected

## Navigation

### Consistency
- **Back Buttons**: Consistent placement and behavior
- **Breadcrumbs**: When appropriate for deeper navigation
- **Active States**: Clear indication of current page/location

### Transitions
- **Page Transitions**: Smooth transitions between pages
- **Loading Feedback**: Visual feedback during navigation
- **History Management**: Proper browser back/forward support

## Accessibility

### Standards
- **WCAG 2.1 AA**: Meet accessibility guidelines
- **Keyboard Navigation**: Full keyboard operability
- **Screen Reader**: Proper semantic markup and ARIA labels
- **Focus Management**: Logical focus order and visible focus states