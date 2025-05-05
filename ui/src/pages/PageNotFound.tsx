import { Link } from 'react-router';

export const PageNotFound = () => {
  return (
    <div className="flex flex-col h-screen justify-center items-center">
      <h1 className="text-4xl">Strona nie znaleziona</h1>
      <h3 className="text-xl">
        Wróć do strony domowej <Link to="/home">Strona domowa</Link>
      </h3>
    </div>
  );
};
