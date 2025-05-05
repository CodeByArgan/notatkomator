import { useMutation, useQuery } from '@tanstack/react-query';
import { createContext, ReactNode, useContext, useState } from 'react';
import { axiosGet } from './utils';
import { BaseResponse } from './api';
import { useNavigate } from 'react-router';

export type Auth = {
  email: string;
  role: 'user' | 'admin';
};

interface AuthContextProps {
  auth: Auth;
  logout: () => void;
  checkLogin: () => void;
}

const AuthContext = createContext<AuthContextProps>({
  auth: {
    email: '',
    role: 'user',
  },
  logout: () => {},
  checkLogin: () => {},
});

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth can be used only in AuthProvider scope');
  }

  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();
  const [auth, setAuth] = useState<Auth>({
    email: '',
    role: 'user',
  });

  const { isPending, refetch } = useQuery({
    queryKey: ['auth'],
    queryFn: async () => {
      const response = await axiosGet<Auth>({ url: '/auth/me' });
      setAuth(response);
      return response;
    },
    retry: false,
    refetchOnWindowFocus: false,
  });

  const logout = useMutation({
    mutationFn: async () =>
      await axiosGet<BaseResponse>({ url: '/auth/logout' }),
    onSuccess: () => {
      setAuth({
        email: '',
        role: 'user',
      });

      navigate('/');
    },
  });

  if (isPending) {
    return null;
  }

  return (
    <AuthContext.Provider
      value={{
        auth,
        logout: () => logout.mutate(),
        checkLogin: () => refetch(),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
