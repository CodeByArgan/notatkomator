import { Outlet } from 'react-router';

export const MainLayout = () => {
  return (
    <div className="flex flex-col bg-stone-900 h-screen w-screen overflow-hidden gap-4">
      <Outlet />
    </div>
  );
};
