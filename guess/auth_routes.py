from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import uuid
from .repository import get_repository

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Username, email e password são obrigatórios'}), 400
        
        # Verificar se usuário já existe
        repo = get_repository()
        existing_user = repo.get_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username já existe'}), 409
        
        existing_email = repo.get_user_by_email(email)
        if existing_email:
            return jsonify({'error': 'Email já está em uso'}), 409
        
        # Hash da senha
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Criar usuário
        user_id = str(uuid.uuid4())
        repo.create_user(user_id, username, email, password_hash)
        
        # Criar token JWT
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Erro no registro: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login do usuário"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        # Buscar usuário
        repo = get_repository()
        user = repo.get_user_by_username(username)
        
        if not user:
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Verificar senha
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Criar token JWT
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no login: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obter perfil do usuário autenticado"""
    try:
        user_id = get_jwt_identity()
        repo = get_repository()
        user = repo.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter perfil: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
