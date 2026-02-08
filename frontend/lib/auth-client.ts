import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    // Your backend URL
   baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
});

// These hooks will be used in components
export const { useSession, signIn, signOut, signUp } = authClient;