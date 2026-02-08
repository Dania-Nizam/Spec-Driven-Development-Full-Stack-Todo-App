# Quickstart Guide: Frontend Todo Application

## Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (assumes running on localhost:8000 or configured endpoint)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the root directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_URL=http://localhost:3000
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

Application will be available at `http://localhost:3000`

## Key Features Setup

### Authentication
- Better Auth is configured for user registration and login
- Sessions are stored securely with JWT tokens
- Redirect to `/login` if not authenticated

### API Integration
- All API calls automatically include the JWT token in the Authorization header
- Error handling follows the `{ "error": string }` format as specified
- User isolation enforced by using authenticated user_id in all requests

### Responsive Design
- Mobile-first approach using Tailwind CSS
- Responsive breakpoints:
  - Mobile: 320px - 767px
  - Tablet: 768px - 1199px
  - Desktop: 1200px+

### Dark Mode
- Toggle available in the UI
- Persists user preference in localStorage
- Respects system preference by default

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests (if configured)

## API Endpoints Used

The frontend communicates with the backend using these exact endpoints:

- `GET /api/{user_id}/tasks` - Fetch all user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Component Structure

- `/app` - Next.js App Router pages
- `/components` - Reusable UI components
- `/lib` - Utility functions and API client
- `/hooks` - Custom React hooks
- `/public` - Static assets

## Common Issues and Solutions

### Authentication Issues
- Ensure `BETTER_AUTH_SECRET` matches the backend
- Check that the backend is running and accessible

### API Connection Issues
- Verify `NEXT_PUBLIC_API_BASE_URL` points to the correct backend
- Confirm JWT tokens are being sent with requests

### Styling Issues
- Check that Tailwind CSS is properly configured
- Verify shadcn/ui components are correctly imported