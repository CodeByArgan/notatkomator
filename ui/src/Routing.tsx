import { Route, Routes } from 'react-router';

import { HomePage } from './pages';
import { MainLayout } from './shared';

export const MainRouter = () => (
  <Routes>
    <Route element={<MainLayout />}>
      <Route index element={<HomePage />} />
    </Route>
  </Routes>
);
