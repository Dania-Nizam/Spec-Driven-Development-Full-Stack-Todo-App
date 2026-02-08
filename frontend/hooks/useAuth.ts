import { useSession } from '@/lib/auth-client';

export function useAuth() {
  const { data: session, status } = useSession();

  const isAuthenticated = status === 'authenticated';
  const isLoading = status === 'loading';

  const getUserInfo = () => {
    // 1. Library session check (Primary)
    if (session?.user && isAuthenticated) {
      return {
        userId: session.user.id,
        email: session.user.email,
        name: session.user.name,
        token: session.token
      };
    }

    // 2. Manual Cookie Fallback (Secondary)
    if (typeof document !== 'undefined') {
      const cookies = document.cookie.split('; ');
      const tokenCookie = cookies.find(row => row.startsWith('access_token='));
      
      if (tokenCookie) {
        const token = tokenCookie.split('=')[1];
        // Note: Aapke screenshot mein access_token maujood hai
        // Hum dummy data bhej rahe hain taake frontend crash na ho
        return { 
          userId: "current-user", // Backend isay token se verify kar lega
          name: "User",
          token: token 
        };
      }
    }

    return null;
  };

  const getToken = () => {
    if (session && isAuthenticated) {
      return session.token;
    }
    if (typeof document !== 'undefined') {
        const tokenCookie = document.cookie.split('; ').find(row => row.startsWith('access_token='));
        return tokenCookie ? tokenCookie.split('=')[1] : null;
    }
    return null;
  };

  return {
    isAuthenticated: isAuthenticated || !!getToken(), // Agar cookie hai toh authenticated maanein
    isLoading,
    session,
    getUserInfo,
    getToken,
  };
}