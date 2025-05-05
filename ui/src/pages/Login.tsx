import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { AuthProvider, Descope } from '@descope/react-sdk';
import { useMutation } from '@tanstack/react-query';

import { useAuth } from '../AuthContext';
import { axiosPost } from '../utils';
import { BaseResponse } from '../api';

export const LoginPage = () => {
  const navigate = useNavigate();
  const { auth, checkLogin } = useAuth();

  const verifyOtp = useMutation({
    mutationFn: async ({
      sessionJwt,
      email,
    }: {
      sessionJwt: string;
      email: string;
    }) => {
      await axiosPost<BaseResponse>({
        url: '/auth/verify-otp',
        data: { sessionJwt, email },
      });
    },
    onSuccess: async () => {
      await checkLogin();
      navigate('/home');
    },
  });

  useEffect(() => {
    if (auth.email !== '') {
      navigate('/home');
    }
  }, [auth.email]);

  return (
    <div className="h-screen flex justify-center items-center bg-stone-900">
      <AuthProvider projectId={import.meta.env.VITE_DESCOPE_PROJECT_ID}>
        <Descope
          flowId="sign-up-or-in-email-input"
          theme="dark"
          onSuccess={async (e) => {
            console.log(e);

            const response = await verifyOtp.mutate({
              email: e.detail?.user?.email || '',
              sessionJwt: e.detail.sessionJwt,
            });

            console.log(response);
          }}
          onError={(err) => {
            console.log('Error!', err);
          }}
        />
      </AuthProvider>
    </div>
  );
};
