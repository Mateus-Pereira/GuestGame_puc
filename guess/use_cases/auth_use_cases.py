import uuid
from typing import Dict, Any
from flask_jwt_extended import create_access_token

from ..domain.entities import User
from ..domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from ..domain.repositories import UserRepository
from ..domain.services import PasswordService


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
    
    def execute(self, username: str, email: str, password: str) -> Dict[str, Any]:
        if self.user_repository.get_by_username(username):
            raise UserAlreadyExistsException("Username já existe")
        
        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsException("Email já está em uso")
        
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=self.password_service.hash_password(password)
        )
        
        self.user_repository.create(user)
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'Usuário criado com sucesso',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
    
    def execute(self, username: str, password: str) -> Dict[str, Any]:
        user = self.user_repository.get_by_username(username)
        
        if not user or not self.password_service.verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Credenciais inválidas")
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }


class GetUserProfileUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: str) -> Dict[str, Any]:
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            raise InvalidCredentialsException("Usuário não encontrado")
        
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
