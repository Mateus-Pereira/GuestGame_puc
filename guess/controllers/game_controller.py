from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..domain.exceptions import (
    GameNotFoundException, UnauthorizedAccessException, 
    GameCompletedException, MaxAttemptsExceededException
)
from ..use_cases.game_use_cases import (
    CreateGameUseCase, MakeGuessUseCase, 
    GetUserGamesUseCase, GetGameDetailsUseCase
)
from ..infrastructure.postgres_repositories import (
    PostgresGameRepository, PostgresAttemptRepository
)


game_bp = Blueprint('game_bp', __name__)


def _get_game_dependencies():
    game_repository = PostgresGameRepository()
    attempt_repository = PostgresAttemptRepository()
    
    return {
        'create_game_use_case': CreateGameUseCase(game_repository),
        'make_guess_use_case': MakeGuessUseCase(game_repository, attempt_repository),
        'get_user_games_use_case': GetUserGamesUseCase(game_repository, attempt_repository),
        'get_game_details_use_case': GetGameDetailsUseCase(game_repository, attempt_repository)
    }


@game_bp.route('/create', methods=['POST'])
@jwt_required()
def create_game():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        password = data.get('password')
        max_attempts = data.get('max_attempts', 10)
        
        if not password:
            return jsonify({'error': 'Password é obrigatório'}), 400
        
        deps = _get_game_dependencies()
        result = deps['create_game_use_case'].execute(user_id, password, max_attempts)
        
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Erro ao criar jogo: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@game_bp.route('/guess/<game_id>', methods=['POST'])
@jwt_required()
def guess(game_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        guess_text = data.get('guess')
        
        if not guess_text:
            return jsonify({'error': 'Guess é obrigatório'}), 400
        
        deps = _get_game_dependencies()
        result = deps['make_guess_use_case'].execute(user_id, game_id, guess_text)
        
        return jsonify(result), 200
        
    except GameNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except UnauthorizedAccessException as e:
        return jsonify({'error': str(e)}), 403
    except (GameCompletedException, MaxAttemptsExceededException) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Erro na tentativa: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@game_bp.route('/games', methods=['GET'])
@jwt_required()
def get_user_games():
    try:
        user_id = get_jwt_identity()
        
        deps = _get_game_dependencies()
        result = deps['get_user_games_use_case'].execute(user_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao listar jogos: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@game_bp.route('/game/<game_id>', methods=['GET'])
@jwt_required()
def get_game_details(game_id):
    try:
        user_id = get_jwt_identity()
        
        deps = _get_game_dependencies()
        result = deps['get_game_details_use_case'].execute(user_id, game_id)
        
        return jsonify(result), 200
        
    except GameNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except UnauthorizedAccessException as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        current_app.logger.error(f"Erro ao obter detalhes do jogo: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@game_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
