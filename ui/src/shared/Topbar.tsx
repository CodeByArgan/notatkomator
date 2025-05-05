import { useAuth } from '../AuthContext';

export const Topbar = () => {
  const { logout } = useAuth();
  return (
    <div className="flex justify-between items-center h-full px-2 bg-purple-500">
      <h1 className="text-lg">Notatkomator</h1>
      <button
        onClick={logout}
        className="cursor-pointer border-white border-1 p-2 rounded-sm hover:bg-white/10"
      >
        Logout
      </button>
    </div>
  );
};
