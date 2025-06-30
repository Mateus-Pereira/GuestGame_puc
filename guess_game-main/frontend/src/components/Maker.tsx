import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGame } from '../hooks/useGame';
import { useAuthContext } from '../contexts/AuthContext';

const Maker: React.FC = () => {
  const [password, setPassword] = useState('');
  const [maxAttempts, setMaxAttempts] = useState(10);
  const [gameId, setGameId] = useState<string | null>(null);
  const [error, setError] = useState('');
  
  const { createGame, loading } = useGame();
  const { isAuthenticated } = useAuthContext();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!password.trim()) {
      setError('Por favor, digite uma palavra ou frase');
      return;
    }

    try {
      const response = await createGame({
        password: password.trim(),
        max_attempts: maxAttempts
      });
      
      setGameId(response.game_id);
      setPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao criar jogo');
    }
  };

  const copyGameId = () => {
    if (gameId) {
      navigator.clipboard.writeText(gameId);
      alert('ID do jogo copiado para a área de transferência!');
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="maker-container">
      <div className="maker-card">
        <h2>🎯 Criar Novo Jogo</h2>
        
        {!gameId ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="password">Palavra ou Frase Secreta:</label>
              <input
                type="text"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Digite a palavra ou frase para adivinhar"
                required
                disabled={loading}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="maxAttempts">Número máximo de tentativas:</label>
              <input
                type="number"
                id="maxAttempts"
                value={maxAttempts}
                onChange={(e) => setMaxAttempts(parseInt(e.target.value))}
                min="1"
                max="50"
                required
                disabled={loading}
              />
              <small>Entre 1 e 50 tentativas</small>
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            <button type="submit" disabled={loading}>
              {loading ? 'Criando...' : 'Criar Jogo'}
            </button>
          </form>
        ) : (
          <div className="game-created">
            <h3>✅ Jogo criado com sucesso!</h3>
            <div className="game-id-container">
              <label>ID do Jogo:</label>
              <div className="game-id-display">
                <code>{gameId}</code>
                <button onClick={copyGameId} className="copy-btn">
                  📋 Copiar
                </button>
              </div>
            </div>
            <p>Compartilhe este ID com outras pessoas para que possam jogar!</p>
            <button 
              onClick={() => {
                setGameId(null);
                setMaxAttempts(10);
              }}
              className="new-game-btn"
            >
              Criar Outro Jogo
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Maker;
