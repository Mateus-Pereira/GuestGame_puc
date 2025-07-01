import os
import psycopg2
import psycopg2.extras
from typing import List, Optional
from datetime import datetime

from ..domain.entities import User, Game, Attempt
from ..domain.repositories import UserRepository, GameRepository, AttemptRepository


class PostgresConnection:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('FLASK_DB_HOST', 'localhost'),
            'port': os.getenv('FLASK_DB_PORT', '5432'),
            'database': os.getenv('FLASK_DB_NAME', 'guess_game'),
            'user': os.getenv('FLASK_DB_USER', 'postgres'),
            'password': os.getenv('FLASK_DB_PASSWORD', 'secretpass')
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.connection_params)


class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.db = PostgresConnection()
    
    def create(self, user: User) -> None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (id, username, email, password_hash)
                    VALUES (%s, %s, %s, %s)
                """, (user.id, user.username, user.email, user.password_hash))
                conn.commit()
    
    def get_by_username(self, username: str) -> Optional[User]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, password_hash, created_at
                    FROM users WHERE username = %s
                """, (username,))
                row = cur.fetchone()
                return self._row_to_user(row) if row else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, password_hash, created_at
                    FROM users WHERE email = %s
                """, (email,))
                row = cur.fetchone()
                return self._row_to_user(row) if row else None
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, password_hash, created_at
                    FROM users WHERE id = %s
                """, (user_id,))
                row = cur.fetchone()
                return self._row_to_user(row) if row else None
    
    def _row_to_user(self, row) -> User:
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=row['created_at']
        )


class PostgresGameRepository(GameRepository):
    def __init__(self):
        self.db = PostgresConnection()
    
    def create(self, game: Game) -> None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO games (id, user_id, secret_phrase, max_attempts)
                    VALUES (%s, %s, %s, %s)
                """, (game.id, game.user_id, game.secret_phrase, game.max_attempts))
                conn.commit()
    
    def get_by_id(self, game_id: str) -> Optional[Game]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, user_id, secret_phrase, max_attempts, 
                           created_at, completed_at, is_completed
                    FROM games WHERE id = %s
                """, (game_id,))
                row = cur.fetchone()
                return self._row_to_game(row) if row else None
    
    def get_by_user_id(self, user_id: str, limit: int = 50) -> List[Game]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, user_id, secret_phrase, max_attempts, 
                           created_at, completed_at, is_completed
                    FROM games 
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (user_id, limit))
                rows = cur.fetchall()
                return [self._row_to_game(row) for row in rows]
    
    def update(self, game: Game) -> None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE games 
                    SET is_completed = %s, completed_at = %s
                    WHERE id = %s
                """, (game.is_completed, game.completed_at, game.id))
                conn.commit()
    
    def _row_to_game(self, row) -> Game:
        return Game(
            id=row['id'],
            user_id=row['user_id'],
            secret_phrase=row['secret_phrase'],
            max_attempts=row['max_attempts'],
            created_at=row['created_at'],
            completed_at=row['completed_at'],
            is_completed=row['is_completed']
        )


class PostgresAttemptRepository(AttemptRepository):
    def __init__(self):
        self.db = PostgresConnection()
    
    def create(self, attempt: Attempt) -> None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO attempts (id, game_id, guess_text, correct_letters, 
                                        correct_positions, is_correct)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (attempt.id, attempt.game_id, attempt.guess_text, 
                      attempt.correct_letters, attempt.correct_positions, attempt.is_correct))
                conn.commit()
    
    def get_by_game_id(self, game_id: str) -> List[Attempt]:
        with self.db.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, game_id, guess_text, correct_letters, correct_positions, 
                           is_correct, created_at
                    FROM attempts 
                    WHERE game_id = %s 
                    ORDER BY created_at ASC
                """, (game_id,))
                rows = cur.fetchall()
                return [self._row_to_attempt(row) for row in rows]
    
    def count_by_game_id(self, game_id: str) -> int:
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM attempts WHERE game_id = %s
                """, (game_id,))
                return cur.fetchone()[0]
    
    def _row_to_attempt(self, row) -> Attempt:
        return Attempt(
            id=row['id'],
            game_id=row['game_id'],
            guess_text=row['guess_text'],
            correct_letters=row['correct_letters'],
            correct_positions=row['correct_positions'],
            is_correct=row['is_correct'],
            created_at=row['created_at']
        )
