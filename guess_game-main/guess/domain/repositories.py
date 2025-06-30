from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import User, Game, Attempt


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> None:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass


class GameRepository(ABC):
    @abstractmethod
    def create(self, game: Game) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, game_id: str) -> Optional[Game]:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str, limit: int = 50) -> List[Game]:
        pass
    
    @abstractmethod
    def update(self, game: Game) -> None:
        pass


class AttemptRepository(ABC):
    @abstractmethod
    def create(self, attempt: Attempt) -> None:
        pass
    
    @abstractmethod
    def get_by_game_id(self, game_id: str) -> List[Attempt]:
        pass
    
    @abstractmethod
    def count_by_game_id(self, game_id: str) -> int:
        pass
