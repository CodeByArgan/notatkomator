import { Outlet } from 'react-router';

export const MainLayout = () => {
  return (
    <div className="flex flex-col bg-stone-900 h-full w-screen overflow-hidden gap-4 px-2">
      <Outlet />
    </div>
  );
};
