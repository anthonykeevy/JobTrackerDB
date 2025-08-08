import { useEffect, useState } from 'react';

interface UserSession {
  userId: number;
  profileId: number;
  email: string;
  loginTime: string;
}

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [userSession, setUserSession] = useState<UserSession | null>(null);

  useEffect(() => {
    const validateSession = () => {
      try {
        const sessionData = localStorage.getItem('userSession');
        
        if (!sessionData) {
          console.log('❌ No session found - redirecting to login');
          setIsAuthenticated(false);
          setUserSession(null);
          setIsLoading(false);
          return;
        }

        const session: UserSession = JSON.parse(sessionData);
        
        // Check if session is valid (not expired, has required fields)
        if (!session.userId || !session.email) {
          console.log('❌ Invalid session data - redirecting to login');
          localStorage.removeItem('userSession');
          setIsAuthenticated(false);
          setUserSession(null);
          setIsLoading(false);
          return;
        }

        // Check if session is not too old (optional - 24 hours)
        const loginTime = new Date(session.loginTime);
        const now = new Date();
        const hoursSinceLogin = (now.getTime() - loginTime.getTime()) / (1000 * 60 * 60);
        
        if (hoursSinceLogin > 24) {
          console.log('❌ Session expired - redirecting to login');
          localStorage.removeItem('userSession');
          setIsAuthenticated(false);
          setUserSession(null);
          setIsLoading(false);
          return;
        }

        console.log('✅ Valid session found for user:', session.userId);
        setIsAuthenticated(true);
        setUserSession(session);
        setIsLoading(false);
        
      } catch (error) {
        console.error('❌ Error validating session:', error);
        localStorage.removeItem('userSession');
        setIsAuthenticated(false);
        setUserSession(null);
        setIsLoading(false);
      }
    };

    validateSession();
  }, []);

  const logout = () => {
    localStorage.removeItem('userSession');
    setIsAuthenticated(false);
    setUserSession(null);
    window.location.href = '/login';
  };

  return {
    isAuthenticated,
    isLoading,
    userSession,
    logout
  };
}; 