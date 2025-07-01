import { useState } from 'react';
import { gameService } from '../services/gameService';
import { CreateGameRequest, GuessResponse } from '../types';

export const useGame = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createGame = async (request: CreateGameRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await gameService.createGame(request);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const makeGuess = async (gameId: string, guess: string): Promise<GuessResponse> => {
    setLoading(true);
    setError(null);
    try {
      const response = await gameService.makeGuess(gameId, guess);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getUserGames = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await gameService.getUserGames();
      return response.games;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getGameDetails = async (gameId: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await gameService.getGameDetails(gameId);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    createGame,
    makeGuess,
    getUserGames,
    getGameDetails,
  };
};
