export interface User {
  id: string;
  username: string;
  email: string;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  user: User;
}

export interface Game {
  id: string;
  max_attempts: number;
  created_at: string;
  completed_at?: string;
  is_completed: boolean;
  attempts_count: number;
}

export interface Attempt {
  id: string;
  guess_text: string;
  correct_letters: number;
  correct_positions: number;
  is_correct: boolean;
  created_at: string;
}

export interface GameDetails {
  game: Game;
  attempts: Attempt[];
}

export interface GuessResponse {
  result: string;
  is_correct: boolean;
  attempts_made: number;
  max_attempts: number;
  remaining_attempts: number;
  correct_letters?: number;
  correct_positions?: number;
  game_over?: boolean;
  secret_phrase?: string;
  guess_text?: string; // Added for storing the guess text in attempts
}

export interface CreateGameRequest {
  password: string;
  max_attempts: number;
}

export interface CreateGameResponse {
  game_id: string;
  max_attempts: number;
  message: string;
}

export interface ApiError {
  error: string;
}
