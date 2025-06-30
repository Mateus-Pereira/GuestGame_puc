import React, { useState, useEffect } from 'react';
import { useAuthContext } from '../contexts/AuthContext';
import { authService } from '../services/authService';
import { Link } from 'react-router-dom';

interface Game {
  id: string;
  max_attempts: number;
  created_at: string;
  completed_at?: string;
  is_completed: boolean;
  attempts_count: number;
}

const GamesList: React.FC = () => {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, isAuthenticated } = useAuthContext();

  useEffect(() => {
    if (isAuthenticated) {
      fetchGames();
    }
  }, [isAuthenticated]);

  const fetchGames = async () => {
    try {
      const token = authService.getToken();
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost/api';
      const response = await fetch(`${backendUrl}/games`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setGames(data.games);
      } else {
        setError('Erro ao carregar jogos');
      }
    } catch (error) {
      console.error('Error fetching games:', error);
      setError('Erro de conexão');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  const copyGameId = (gameId: string) => {
    navigator.clipboard.writeText(gameId);
    alert('ID do jogo copiado para a área de transferência!');
  };

  if (!isAuthenticated) {
    return (
      <div className="games-container">
        <div className="auth-container">
          <h2>📋 Meus Jogos</h2>
          <p>Você precisa estar logado para ver seus jogos.</p>
          <div className="auth-actions">
            <Link to="/login" className="button primary">Fazer Login</Link>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="games-container">
        <h2>📋 Meus Jogos</h2>
        <div className="info-message">
          <div className="loading-spinner"></div>
          Carregando seus jogos...
        </div>
      </div>
    );
  }

  return (
    <div className="games-container">
      <h2>📋 Meus Jogos</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      {games.length === 0 ? (
        <div className="no-games">
          <h3>🎮 Nenhum jogo encontrado</h3>
          <p>Você ainda não criou nenhum jogo. Que tal começar agora?</p>
          <Link to="/maker" className="button primary">Criar Primeiro Jogo</Link>
        </div>
      ) : (
        <div className="games-list">
          {games.map((game) => (
            <div key={game.id} className="game-card">
              <div className="game-header">
                <h3>🎯 Jogo #{game.id.substring(0, 8)}...</h3>
                <span className={`status ${game.is_completed ? 'completed' : 'active'}`}>
                  {game.is_completed ? '✅ Concluído' : '🎮 Ativo'}
                </span>
              </div>
              
              <div className="game-details">
                <p><strong>📅 Criado em:</strong> {formatDate(game.created_at)}</p>
                {game.completed_at && (
                  <p><strong>🏁 Concluído em:</strong> {formatDate(game.completed_at)}</p>
                )}
                <p><strong>🎯 Tentativas máximas:</strong> {game.max_attempts}</p>
                <p><strong>📊 Tentativas feitas:</strong> {game.attempts_count}</p>
              </div>
              
              <div className="game-actions">
                <button 
                  onClick={() => copyGameId(game.id)}
                  className="copy-button"
                >
                  📋 Copiar ID
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GamesList;
