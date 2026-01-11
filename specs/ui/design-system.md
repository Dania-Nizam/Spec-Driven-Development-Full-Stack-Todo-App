# UI Design System – Colors, Typography, Components

## Color Palette

### Primary Colors
- **Primary**: Indigo (#6366f1) - Used for main buttons, primary actions, and important UI elements
- **Primary Dark**: Indigo (#4f46e5) - Hover states and active states for primary elements
- **Accent**: Blue (#3b82f6) - Used for secondary actions and highlights

### Neutral Colors
- **Background**: White (#ffffff) / Dark: Gray-900 (#111827)
- **Surface**: Gray-50 (#f9fafb) / Dark: Gray-800 (#1f2937)
- **Text Primary**: Gray-900 (#111827) / Dark: Gray-50 (#f9fafb)
- **Text Secondary**: Gray-600 (#4b5563) / Dark: Gray-300 (#d1d5db)
- **Border**: Gray-200 (#e5e7eb) / Dark: Gray-700 (#374151)

### Status Colors
- **Success**: Green-500 (#10b981) - For success messages and positive actions
- **Error**: Red-500 (#ef4444) - For error messages and destructive actions
- **Warning**: Amber-500 (#f59e0b) - For warnings and cautionary states
- **Info**: Blue-500 (#3b82f6) - For informational messages

## Typography

### Font Stack
- **Primary**: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"
- **Fallback**: System font stack for optimal performance and consistency

### Hierarchy
- **H1**: 36px (2.25rem), font-weight: 700, line-height: 1.2
- **H2**: 30px (1.875rem), font-weight: 600, line-height: 1.3
- **H3**: 24px (1.5rem), font-weight: 600, line-height: 1.4
- **H4**: 20px (1.25rem), font-weight: 600, line-height: 1.5
- **Body**: 16px (1rem), font-weight: 400, line-height: 1.6
- **Small**: 14px (0.875rem), font-weight: 400, line-height: 1.4

## Spacing System

### Tailwind Spacing Scale
- **Space-1**: 0.25rem (4px)
- **Space-2**: 0.5rem (8px)
- **Space-3**: 0.75rem (12px)
- **Space-4**: 1rem (16px)
- **Space-5**: 1.25rem (20px)
- **Space-6**: 1.5rem (24px)
- **Space-8**: 2rem (32px)
- **Space-10**: 2.5rem (40px)
- **Space-12**: 3rem (48px)
- **Space-16**: 4rem (64px)

## Components

### Button Component
- **Variants**: Primary, Secondary, Destructive, Ghost, Link
- **Sizes**: Small (h-8 rounded-md px-3), Default (h-10 px-4 py-2), Large (h-12 rounded-md px-8)
- **States**: Default, Hover, Active, Disabled, Loading
- **Focus**: Ring-2 ring-offset-2 ring-indigo-500 for accessibility

### Card Component
- **Background**: White/Gray-50 with subtle shadow (shadow-sm)
- **Border**: 1px solid Gray-200
- **Rounded**: Rounded-lg
- **Padding**: p-6 for main content
- **Header**: p-6 pb-2 for card headers

### Input Component
- **Height**: h-10 for default inputs
- **Border**: 1px solid Gray-300, focus:ring-2 focus:ring-indigo-500
- **Rounded**: Rounded-md
- **Padding**: px-3 py-2
- **States**: Default, Focus, Error, Disabled

### Checkbox Component
- **Size**: 16px x 16px (h-4 w-4)
- **Border**: 2px solid Gray-300
- **Checked**: bg-indigo-500 border-indigo-500
- **Focus**: ring-2 ring-indigo-500 ring-offset-2

### Dialog/Modal Component
- **Backdrop**: Black with 50% opacity (bg-black/50)
- **Container**: White background, rounded-lg, shadow-xl
- **Padding**: p-6
- **Max Width**: Responsive (mobile: 90%, desktop: 25rem)

### Badge Component
- **Variants**: Default, Primary, Secondary, Destructive, Outline
- **Sizes**: Default (h-6 px-2), Secondary (h-5 px-1.5)
- **Rounded**: Rounded-full or rounded-md based on context

### Avatar Component
- **Size**: 8 (w-8 h-8), 10 (w-10 h-10), 16 (w-16 h-16)
- **Rounded**: Rounded-full
- **Fallback**: Initials or default icon

## Icons

### Icon Library
- **Primary**: Lucide-react icons for all interface elements
- **Size**: 16px, 20px, 24px for different contexts
- **Color**: Text secondary color by default, primary color for active states

## Dark Mode

### Implementation
- **Selector**: Tailwind's `dark:` prefix for all dark mode variants
- **Automatic**: System preference detection with manual override option
- **Smooth**: CSS transitions for theme switching (0.2s duration)

### Elevation & Shadows
- **Default**: shadow-sm for cards and elevated elements
- **Hover**: shadow-md for interactive elements on hover
- **Focus**: ring-2 for focus states with appropriate color

### Rounded Corners
- **Small Elements**: rounded-sm (border radius: 2px)
- **Medium Elements**: rounded-md (border radius: 6px)
- **Large Elements**: rounded-lg (border radius: 8px)
- **Circular**: rounded-full for avatars and circular elements

## Hover Effects
- **Buttons**: Slight opacity change (0.9) or color shift
- **Cards**: Subtle elevation increase (shadow-md)
- **Interactive Elements**: Cursor pointer and appropriate visual feedback