import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuthContext();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="nav-brand">
          <Link to="/">🎮 Guess Game</Link>
        </div>
        
        <div className="nav-center">
          <ul className="nav-links">
            {isAuthenticated ? (
              <>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/maker">Criar Jogo</Link></li>
                <li><Link to="/breaker">Jogar</Link></li>
                <li><Link to="/games">Meus Jogos</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/login">Login</Link></li>
                <li><Link to="/register">Registro</Link></li>
              </>
            )}
          </ul>
        </div>

        <div className="nav-right">
          {isAuthenticated && (
            <>
              <span className="user-info">Olá, {user?.username}!</span>
              <button onClick={handleLogout} className="logout-button">
                Sair
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
