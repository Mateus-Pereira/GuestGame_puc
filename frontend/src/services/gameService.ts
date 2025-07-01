import { apiClient } from './api';
import { 
  CreateGameRequest, 
  CreateGameResponse, 
  Game, 
  GameDetails, 
  GuessResponse 
} from '../types';

export class GameService {
  async createGame(request: CreateGameRequest): Promise<CreateGameResponse> {
    return apiClient.post<CreateGameResponse>('/create', request);
  }

  async makeGuess(gameId: string, guess: string): Promise<GuessResponse> {
    return apiClient.post<GuessResponse>(`/guess/${gameId}`, { guess });
  }

  async getUserGames(): Promise<{ games: Game[] }> {
    return apiClient.get<{ games: Game[] }>('/games');
  }

  async getGameDetails(gameId: string): Promise<GameDetails> {
    return apiClient.get<GameDetails>(`/game/${gameId}`);
  }

  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return apiClient.get<{ status: string; timestamp: string }>('/health');
  }
}

export const gameService = new GameService();
