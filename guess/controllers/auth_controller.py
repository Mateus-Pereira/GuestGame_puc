from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from ..use_cases.auth_use_cases import RegisterUserUseCase, LoginUserUseCase, GetUserProfileUseCase
from ..infrastructure.postgres_repositories import PostgresUserRepository


auth_bp = Blueprint('auth', __name__)


def _get_auth_dependencies():
    user_repository = PostgresUserRepository()
    return {
        'register_use_case': RegisterUserUseCase(user_repository),
        'login_use_case': LoginUserUseCase(user_repository),
        'profile_use_case': GetUserProfileUseCase(user_repository)
    }


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Username, email e password são obrigatórios'}), 400
        
        deps = _get_auth_dependencies()
        result = deps['register_use_case'].execute(username, email, password)
        
        return jsonify(result), 201
        
    except UserAlreadyExistsException as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        current_app.logger.error(f"Erro no registro: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        deps = _get_auth_dependencies()
        result = deps['login_use_case'].execute(username, password)
        
        return jsonify(result), 200
        
    except InvalidCredentialsException as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        current_app.logger.error(f"Erro no login: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        
        deps = _get_auth_dependencies()
        result = deps['profile_use_case'].execute(user_id)
        
        return jsonify(result), 200
        
    except InvalidCredentialsException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Erro ao obter perfil: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
