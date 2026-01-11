# Authentication Flow Test

## Test Cases

### 1. Login Flow
- [ ] Navigate to `/login`
- [ ] Verify login form is displayed
- [ ] Verify sign up form is accessible via tabs
- [ ] Submit valid credentials
- [ ] Verify redirect to dashboard (`/`)
- [ ] Verify user session is established

### 2. Logout Flow
- [ ] Navigate to dashboard
- [ ] Find and click logout button (likely in navbar)
- [ ] Verify redirect to `/login`
- [ ] Verify user session is cleared

### 3. Protected Route Access
- [ ] Navigate to `/` while not logged in
- [ ] Verify redirect to `/login`
- [ ] Log in with valid credentials
- [ ] Navigate to `/` again
- [ ] Verify dashboard is displayed

### 4. Sign Up Flow
- [ ] Navigate to `/login`
- [ ] Click on "Sign Up" tab
- [ ] Enter valid registration details
- [ ] Submit form
- [ ] Verify account creation and possible redirect to login

### 5. Error Handling
- [ ] Attempt login with invalid credentials
- [ ] Verify appropriate error message is displayed
- [ ] Attempt login with malformed email
- [ ] Verify form validation
- [ ] Test password requirements (min length, etc.)

## Expected Behaviors
- Authentication state persists across page refreshes
- Proper error messages are displayed for failed operations
- User is redirected appropriately based on authentication state
- JWT tokens are handled securely
- User isolation is maintained (users can only access their own data)