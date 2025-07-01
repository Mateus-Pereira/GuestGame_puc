import uuid
import base64
from typing import Dict, Any, List
from datetime import datetime

from ..domain.entities import Game, Attempt
from ..domain.exceptions import (
    GameNotFoundException, UnauthorizedAccessException, 
    GameCompletedException, MaxAttemptsExceededException, InvalidGuessException
)
from ..domain.repositories import GameRepository, AttemptRepository
from ..domain.services import GuessService


class CreateGameUseCase:
    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository
    
    def execute(self, user_id: str, password: str, max_attempts: int) -> Dict[str, Any]:
        if max_attempts < 1 or max_attempts > 50:
            raise ValueError("Número de tentativas deve estar entre 1 e 50")
        
        encoded_password = base64.b64encode(password.encode('utf-8')).decode()
        
        game = Game(
            id=str(uuid.uuid4()),
            user_id=user_id,
            secret_phrase=encoded_password,
            max_attempts=max_attempts
        )
        
        self.game_repository.create(game)
        
        return {
            'game_id': game.id,
            'max_attempts': max_attempts,
            'message': 'Jogo criado com sucesso'
        }


class MakeGuessUseCase:
    def __init__(self, game_repository: GameRepository, attempt_repository: AttemptRepository):
        self.game_repository = game_repository
        self.attempt_repository = attempt_repository
    
    def execute(self, user_id: str, game_id: str, guess: str) -> Dict[str, Any]:
        game = self.game_repository.get_by_id(game_id)
        
        if not game:
            raise GameNotFoundException("Jogo não encontrado")
        
        if game.user_id != user_id:
            raise UnauthorizedAccessException("Acesso negado")
        
        if game.is_completed:
            raise GameCompletedException("Jogo já foi completado")
        
        attempts_count = self.attempt_repository.count_by_game_id(game_id)
        
        if attempts_count >= game.max_attempts:
            raise MaxAttemptsExceededException("Limite de tentativas excedido")
        
        decoded_password = base64.b64decode(game.secret_phrase).decode()
        guess_service = GuessService(decoded_password)
        
        try:
            result = guess_service.evaluate_guess(guess)
            is_correct = True
            feedback = result.message
            
            game.is_completed = True
            game.completed_at = datetime.utcnow()
            self.game_repository.update(game)
            
            correct_letters = result.correct_letters
            correct_positions = result.correct_positions
            
        except InvalidGuessException as e:
            is_correct = False
            feedback = str(e)
            correct_letters = e.correct_letters
            correct_positions = e.correct_positions
        
        attempt = Attempt(
            id=str(uuid.uuid4()),
            game_id=game_id,
            guess_text=guess,
            correct_letters=correct_letters,
            correct_positions=correct_positions,
            is_correct=is_correct
        )
        
        self.attempt_repository.create(attempt)
        
        attempts_made = attempts_count + 1
        remaining_attempts = game.max_attempts - attempts_made
        
        response = {
            'result': feedback,
            'is_correct': is_correct,
            'attempts_made': attempts_made,
            'max_attempts': game.max_attempts,
            'remaining_attempts': remaining_attempts
        }
        
        if not is_correct:
            response.update({
                'correct_letters': correct_letters,
                'correct_positions': correct_positions
            })
        
        if not is_correct and remaining_attempts == 0:
            response.update({
                'game_over': True,
                'secret_phrase': decoded_password
            })
        
        return response


class GetUserGamesUseCase:
    def __init__(self, game_repository: GameRepository, attempt_repository: AttemptRepository):
        self.game_repository = game_repository
        self.attempt_repository = attempt_repository
    
    def execute(self, user_id: str) -> Dict[str, Any]:
        games = self.game_repository.get_by_user_id(user_id)
        
        games_data = []
        for game in games:
            attempts_count = self.attempt_repository.count_by_game_id(game.id)
            games_data.append({
                'id': game.id,
                'max_attempts': game.max_attempts,
                'created_at': game.created_at.isoformat() if game.created_at else None,
                'completed_at': game.completed_at.isoformat() if game.completed_at else None,
                'is_completed': game.is_completed,
                'attempts_count': attempts_count
            })
        
        return {'games': games_data}


class GetGameDetailsUseCase:
    def __init__(self, game_repository: GameRepository, attempt_repository: AttemptRepository):
        self.game_repository = game_repository
        self.attempt_repository = attempt_repository
    
    def execute(self, user_id: str, game_id: str) -> Dict[str, Any]:
        game = self.game_repository.get_by_id(game_id)
        
        if not game:
            raise GameNotFoundException("Jogo não encontrado")
        
        if game.user_id != user_id:
            raise UnauthorizedAccessException("Acesso negado")
        
        attempts = self.attempt_repository.get_by_game_id(game_id)
        
        attempts_data = []
        for attempt in attempts:
            attempts_data.append({
                'id': attempt.id,
                'guess_text': attempt.guess_text,
                'correct_letters': attempt.correct_letters,
                'correct_positions': attempt.correct_positions,
                'is_correct': attempt.is_correct,
                'created_at': attempt.created_at.isoformat() if attempt.created_at else None
            })
        
        game_data = {
            'id': game.id,
            'user_id': game.user_id,
            'max_attempts': game.max_attempts,
            'created_at': game.created_at.isoformat() if game.created_at else None,
            'completed_at': game.completed_at.isoformat() if game.completed_at else None,
            'is_completed': game.is_completed
        }
        
        return {
            'game': game_data,
            'attempts': attempts_data
        }
