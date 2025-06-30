import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

const Home: React.FC = () => {
  const { isAuthenticated, user } = useAuthContext();

  return (
    <div className="home">
      <h1>🎮 Bem-vindo ao Guess Game!</h1>
      
      {isAuthenticated ? (
        <div>
          <h2>Olá, {user?.username}! 👋</h2>
          <p>O que você gostaria de fazer hoje?</p>
          
          <div className="action-cards">
            <div className="card">
              <h3>🎯 Criar Jogo</h3>
              <p>Crie um novo jogo de adivinhação com sua palavra ou frase secreta.</p>
              <Link to="/maker" className="button">Criar Jogo</Link>
            </div>
            
            <div className="card">
              <h3>🔍 Jogar</h3>
              <p>Tente adivinhar a palavra ou frase de um jogo existente.</p>
              <Link to="/breaker" className="button">Jogar</Link>
            </div>
            
            <div className="card">
              <h3>📋 Meus Jogos</h3>
              <p>Veja todos os jogos que você criou e seu status.</p>
              <Link to="/games" className="button">Ver Jogos</Link>
            </div>
          </div>
        </div>
      ) : (
        <div>
          <p>Um jogo de adivinhação onde você pode criar desafios ou tentar resolver os de outros jogadores!</p>
          
          <div className="features">
            <h2>✨ Funcionalidades:</h2>
            <ul>
              <li>🎯 Crie jogos com palavras ou frases secretas</li>
              <li>🔢 Configure o número de tentativas (1-50)</li>
              <li>📊 Receba feedback detalhado sobre suas tentativas</li>
              <li>📈 Acompanhe o histórico dos seus jogos</li>
              <li>🔒 Sistema seguro com autenticação</li>
            </ul>
          </div>
          
          <div className="auth-actions">
            <h2>Comece agora:</h2>
            <Link to="/register" className="button primary">Criar Conta</Link>
            <Link to="/login" className="button secondary">Fazer Login</Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
