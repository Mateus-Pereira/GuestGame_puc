from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None


@dataclass
class Game:
    id: str
    user_id: str
    secret_phrase: str
    max_attempts: int
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    is_completed: bool = False


@dataclass
class Attempt:
    id: str
    game_id: str
    guess_text: str
    correct_letters: int
    correct_positions: int
    is_correct: bool
    created_at: Optional[datetime] = None


@dataclass
class GuessResult:
    is_correct: bool
    correct_letters: int
    correct_positions: int
    message: str
