import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGame } from '../hooks/useGame';
import { useAuthContext } from '../contexts/AuthContext';
import { GuessResponse } from '../types';

const Breaker: React.FC = () => {
  const [gameId, setGameId] = useState('');
  const [guess, setGuess] = useState('');
  const [gameStarted, setGameStarted] = useState(false);
  const [gameResult, setGameResult] = useState<GuessResponse | null>(null);
  const [attempts, setAttempts] = useState<GuessResponse[]>([]);
  const [error, setError] = useState('');
  
  const { makeGuess, loading } = useGame();
  const { isAuthenticated } = useAuthContext();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleStartGame = (e: React.FormEvent) => {
    e.preventDefault();
    if (!gameId.trim()) {
      setError('Por favor, digite o ID do jogo');
      return;
    }
    setGameStarted(true);
    setError('');
  };

  const handleGuess = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!guess.trim()) {
      setError('Por favor, digite sua tentativa');
      return;
    }

    try {
      const response = await makeGuess(gameId, guess.trim());
      
      const newAttempt = { ...response, guess_text: guess.trim() };
      setAttempts(prev => [...prev, newAttempt]);
      setGameResult(response);
      setGuess('');
      
      if (response.is_correct || response.game_over) {
        setGameStarted(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer tentativa');
    }
  };

  const resetGame = () => {
    setGameId('');
    setGuess('');
    setGameStarted(false);
    setGameResult(null);
    setAttempts([]);
    setError('');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="breaker-container">
      <div className="breaker-card">
        <h2>🔍 Jogar Guess Game</h2>
        
        {!gameStarted ? (
          <form onSubmit={handleStartGame}>
            <div className="form-group">
              <label htmlFor="gameId">ID do Jogo:</label>
              <input
                type="text"
                id="gameId"
                value={gameId}
                onChange={(e) => setGameId(e.target.value)}
                placeholder="Cole o ID do jogo aqui"
                required
              />
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            <button type="submit">Iniciar Jogo</button>
          </form>
        ) : (
          <div className="game-area">
            <div className="game-info">
              <p><strong>ID do Jogo:</strong> {gameId}</p>
              {gameResult && (
                <p>
                  <strong>Tentativas:</strong> {gameResult.attempts_made} / {gameResult.max_attempts}
                </p>
              )}
            </div>
            
            {!gameResult?.is_correct && !gameResult?.game_over && (
              <form onSubmit={handleGuess}>
                <div className="form-group">
                  <label htmlFor="guess">Sua tentativa:</label>
                  <input
                    type="text"
                    id="guess"
                    value={guess}
                    onChange={(e) => setGuess(e.target.value)}
                    placeholder="Digite sua tentativa"
                    required
                    disabled={loading}
                  />
                </div>
                
                <button type="submit" disabled={loading}>
                  {loading ? 'Enviando...' : 'Tentar'}
                </button>
              </form>
            )}
            
            {error && <div className="error-message">{error}</div>}
            
            <div className="attempts-history">
              <h3>Histórico de Tentativas</h3>
              {attempts.length === 0 ? (
                <p>Nenhuma tentativa ainda.</p>
              ) : (
                <div className="attempts-list">
                  {attempts.map((attempt, index) => (
                    <div key={index} className={`attempt ${attempt.is_correct ? 'correct' : 'incorrect'}`}>
                      <div className="attempt-text">
                        <strong>Tentativa {index + 1}:</strong> {attempts[index]?.guess_text || guess}
                      </div>
                      <div className="attempt-result">
                        {attempt.is_correct ? (
                          <span className="success">✅ Correto!</span>
                        ) : (
                          <div className="feedback">
                            <span>Posições corretas: {attempt.correct_positions || 0}</span>
                            <span>Letras corretas (posição errada): {attempt.correct_letters || 0}</span>
                          </div>
                        )}
                      </div>
                      <div className="attempt-message">{attempt.result}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            {(gameResult?.is_correct || gameResult?.game_over) && (
              <div className="game-end">
                {gameResult.is_correct ? (
                  <div className="success-message">
                    <h3>🎉 Parabéns! Você acertou!</h3>
                  </div>
                ) : (
                  <div className="game-over-message">
                    <h3>😔 Game Over!</h3>
                    <p>A resposta era: <strong>{gameResult.secret_phrase}</strong></p>
                  </div>
                )}
                <button onClick={resetGame} className="new-game-btn">
                  Jogar Novamente
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Breaker;
