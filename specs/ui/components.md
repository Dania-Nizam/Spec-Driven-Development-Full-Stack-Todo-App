# Reusable UI Components Specification

## TaskCard Component

### Purpose
Display individual tasks in a card format with key information and action controls.

### Visual Design
- **Container**: Card component with subtle shadow and rounded corners
- **Padding**: Consistent internal padding (p-4)
- **Spacing**: Appropriate spacing between elements
- **Hover Effect**: Slight elevation increase on hover for interactivity

### Layout Structure
- **Top Row**: Checkbox on left, title text in middle, action icons on right
- **Bottom Row**: Description preview or status badge
- **Separator**: Optional visual separation between elements

### Elements
- **Checkbox**: Left-aligned for completion status with proper focus states
- **Title**: Bold, primary text color, truncation for long titles
- **Description Preview**: Secondary text color, limited to 2 lines maximum
- **Action Icons**: Edit (pencil icon) and Delete (trash icon) on right side
- **Status Badge**: Visual indicator for task status (completed, pending, etc.)

### Interactions
- **Hover**: Action icons appear/disappear smoothly
- **Click**: Checkbox toggles completion status
- **Edit Click**: Opens TaskForm with pre-filled data
- **Delete Click**: Triggers confirmation dialog
- **Complete Toggle**: Instant visual feedback with strikethrough on title

### States
- **Completed**: Strikethrough on title, muted colors
- **Pending**: Normal appearance with full contrast
- **Hover**: Subtle background change or elevation
- **Loading**: Skeleton loading state during updates

### Responsive Behavior
- **Mobile**: Full-width cards with touch-friendly targets
- **Desktop**: Grid layout with consistent spacing
- **Adaptive**: Adjust layout based on available space

## TaskForm Component (in Dialog/Modal)

### Purpose
Unified form component for creating and editing tasks with validation and submission handling.

### Container
- **Dialog Wrapper**: Modal overlay with backdrop
- **Form Container**: Card-style form with proper spacing
- **Responsive**: Full-width on mobile, constrained width on desktop

### Form Fields
- **Title Input**: Required text field with character counter
  - Label: "Task Title"
  - Placeholder: "Enter task title..."
  - Validation: Required field with minimum length
  - Max Length: 100 characters
- **Description Textarea**: Optional multi-line text field
  - Label: "Description" (optional)
  - Placeholder: "Add details about your task..."
  - Rows: 4 by default
  - Max Length: 500 characters

### Form Controls
- **Submit Button**: Primary button with loading state
  - Text: "Save Task" for new, "Update Task" for edit
  - Loading: Spinner icon during submission
  - Disabled: When form is invalid
- **Cancel Button**: Secondary button to close form
  - Text: "Cancel"
  - Action: Close dialog without saving
- **Close Icon**: X button in top-right corner

### Validation
- **Real-time**: Field validation as user types
- **Error Messages**: Clear, specific error messages below each field
- **Required Fields**: Visual indication of required fields
- **Character Limits**: Display remaining characters

### States
- **Create Mode**: Empty form for new task creation
- **Edit Mode**: Pre-populated form with existing task data
- **Loading**: Skeleton state while loading edit data
- **Submitting**: Loading state during save operation
- **Error**: Form-wide error messages for API failures

### Behavior
- **Auto-focus**: Focus on title field when opened
- **Keyboard**: Submit on Enter key (except in textarea)
- **Validation**: Prevent submission with invalid data
- **Success**: Close dialog and show success toast on save

## Navbar Component

### Purpose
Consistent navigation element across all pages with app identity and user controls.

### Layout Structure
- **Container**: Fixed top navigation with full-width
- **Flex Layout**: Horizontal flexbox with space-between
- **Height**: Consistent height (h-16) across all pages

### Left Section (Brand)
- **Logo/Icon**: App logo or brand icon
- **App Name**: Text "Todo App" or appropriate brand name
- **Link**: Clickable area that returns to dashboard

### Right Section (User Controls)
- **User Greeting**: Display user name or email (truncated if long)
- **Avatar**: Circular avatar with user initials or image
- **Dropdown Menu**: Accessible menu with user options
  - Profile View
  - Settings
  - Logout option
  - Divider between user actions and logout

### Elements
- **Avatar**: 32x32px circular image with initials fallback
- **Dropdown Trigger**: Clickable area around avatar/name
- **Menu Position**: Right-aligned dropdown below trigger
- **Logout Button**: Destructive style for logout action

### Responsive Behavior
- **Desktop**: Full display of all elements
- **Mobile**: May collapse elements or use hamburger menu
- **Accessibility**: Proper ARIA labels and keyboard navigation

### States
- **Default**: Normal appearance with subtle hover effects
- **Dropdown Open**: Menu visible with proper positioning
- **Loading**: Skeleton state during initial load
- **User Not Loaded**: Placeholder display until user data available

## Toaster Component

### Purpose
Global notification system for displaying success, error, warning, and info messages.

### Implementation
- **Library**: Use shadcn/ui Toast component or similar
- **Position**: Top-right corner with proper z-index
- **Animation**: Smooth entrance and exit animations

### Toast Types
- **Success**: Green accent with checkmark icon
- **Error**: Red accent with error icon
- **Warning**: Amber accent with warning icon
- **Info**: Blue accent with info icon

### Content Structure
- **Icon**: Appropriate icon for toast type
- **Title**: Brief message title
- **Description**: Optional detailed message
- **Close Button**: Dismiss button for manual closure
- **Auto-dismiss**: Automatically dismiss after 5 seconds

### Behavior
- **Stacking**: New toasts stack vertically
- **Focus**: Pause auto-dismiss when user interacts with toast
- **Persistence**: Manual close option for important messages

### Error Toast Patterns
- **401 Unauthorized**: "Session expired. Redirecting to login..." with auto-redirect after 2 seconds
- **403 Forbidden**: "Access denied. You don't have permission for this action." with redirect option
- **404 Not Found**: "Task not found. Please refresh the page." with refresh option
- **400 Validation Error**: "Invalid input: [specific error from API]" with details
- **Network Error**: "Connection failed. Please check your internet connection and try again."
- **Generic Error**: "Something went wrong. Please try again later."

## LoadingSpinner Component

### Purpose
Consistent loading indicator for various loading states throughout the application.

### Visual Design
- **Style**: Circular spinner with rotating animation
- **Size**: Multiple sizes (small, medium, large) for different contexts
- **Color**: Primary color (indigo) for consistency

### Usage Contexts
- **Button Loading**: Inside buttons during submission
- **Page Loading**: Full-page or section loading state
- **Data Fetch**: Indicator during API calls
- **Inline Loading**: Small spinner within content areas

### Sizes
- **Small**: 16px diameter (for inline use)
- **Medium**: 24px diameter (for buttons)
- **Large**: 40px diameter (for page sections)

### Variants
- **Primary**: Indigo color for main actions
- **Secondary**: Gray color for subtle loading states
- **White**: For use on colored backgrounds

## Additional Components

### EmptyState Component
- **Visual**: Friendly illustration or icon
- **Message**: Clear, encouraging text
- **Action**: Primary button for next step
- **Secondary**: Optional secondary action or link

### ConfirmationDialog Component
- **Purpose**: Confirm destructive actions like deletion
- **Structure**: Modal with title, description, and action buttons
- **Actions**: Cancel (secondary) and Confirm (destructive)
- **Accessibility**: Proper focus management and keyboard handling

### DataTable Component (if needed)
- **Responsive**: Stacked layout on mobile, table on desktop
- **Sorting**: Clickable headers for sorting
- **Pagination**: Controls for navigating large datasets
- **Loading**: Skeleton rows during data fetch

## Component Properties

### Consistency Standards
- **Class Names**: Use consistent Tailwind classes across components
- **Spacing**: Follow established spacing system (space-1 to space-16)
- **Colors**: Use design system color palette consistently
- **Typography**: Apply typography hierarchy consistently
- **Transitions**: Use consistent timing (150ms, 200ms, 300ms) for animations
- **Focus States**: Consistent focus rings for accessibility
- **Z-Index**: Consistent stacking context management

### Accessibility
- **ARIA Labels**: Proper labels for screen readers
- **Keyboard Navigation**: Full keyboard operability
- **Focus Management**: Proper focus handling in modals and menus
- **Contrast Ratios**: Maintain WCAG 2.1 AA standards
- **Semantic HTML**: Use appropriate HTML elements