import { Navigate, Route, Routes } from 'react-router';

import { HomePage, LoginPage, PageNotFound } from './pages';
import { MainLayout, Topbar } from './shared';
import { useAuth } from './AuthContext';

export const AuthRouting = () => {
  const { auth } = useAuth();

  if (auth.email === '') {
    return <Navigate to="/" replace />;
  }

  return (
    <div
      className="grid h-screen"
      style={{
        gridTemplateAreas: "'topbar' 'content'",
        gridTemplateRows: '57px 1fr',
        rowGap: '8px',
      }}
    >
      <div style={{ gridArea: 'topbar' }}>
        <Topbar />
      </div>
      <div style={{ gridArea: 'content' }}>
        <MainLayout />
      </div>
    </div>
  );
};

export const MainRouter = () => (
  <Routes>
    <Route index element={<LoginPage />} />

    <Route path="/*" element={<AuthRouting />}>
      <Route path="home" element={<HomePage />} />

      <Route path="*" element={<PageNotFound />} />
    </Route>
  </Routes>
);
