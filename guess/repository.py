import os
import psycopg2
import psycopg2.extras
from flask import current_app
from datetime import datetime

class PostgresRepository:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('FLASK_DB_HOST', 'localhost'),
            'port': os.getenv('FLASK_DB_PORT', '5432'),
            'database': os.getenv('FLASK_DB_NAME', 'guess_game'),
            'user': os.getenv('FLASK_DB_USER', 'postgres'),
            'password': os.getenv('FLASK_DB_PASSWORD', 'secretpass')
        }
    
    def get_connection(self):
        """Obter conexão com o banco de dados"""
        return psycopg2.connect(**self.connection_params)
    
    def create_user(self, user_id, username, email, password_hash):
        """Criar novo usuário"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (id, username, email, password_hash)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, username, email, password_hash))
                conn.commit()
    
    def get_user_by_username(self, username):
        """Buscar usuário por username"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, password_hash, created_at
                    FROM users WHERE username = %s
                """, (username,))
                return cur.fetchone()
    
    def get_user_by_email(self, email):
        """Buscar usuário por email"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, password_hash, created_at
                    FROM users WHERE email = %s
                """, (email,))
                return cur.fetchone()
    
    def get_user_by_id(self, user_id):
        """Buscar usuário por ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, username, email, created_at
                    FROM users WHERE id = %s
                """, (user_id,))
                return cur.fetchone()
    
    def create_game(self, game_id, user_id, secret_phrase, max_attempts):
        """Criar novo jogo"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO games (id, user_id, secret_phrase, max_attempts)
                    VALUES (%s, %s, %s, %s)
                """, (game_id, user_id, secret_phrase, max_attempts))
                conn.commit()
    
    def get_game(self, game_id):
        """Buscar jogo por ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, user_id, secret_phrase, max_attempts, 
                           created_at, completed_at, is_completed
                    FROM games WHERE id = %s
                """, (game_id,))
                return cur.fetchone()
    
    def get_user_games(self, user_id, limit=50):
        """Listar jogos do usuário"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT g.id, g.max_attempts, g.created_at, g.completed_at, 
                           g.is_completed, COUNT(a.id) as attempts_count
                    FROM games g
                    LEFT JOIN attempts a ON g.id = a.game_id
                    WHERE g.user_id = %s
                    GROUP BY g.id, g.max_attempts, g.created_at, g.completed_at, g.is_completed
                    ORDER BY g.created_at DESC
                    LIMIT %s
                """, (user_id, limit))
                return cur.fetchall()
    
    def save_attempt(self, attempt_id, game_id, guess_text, correct_letters, correct_positions, is_correct):
        """Salvar tentativa"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO attempts (id, game_id, guess_text, correct_letters, 
                                        correct_positions, is_correct)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (attempt_id, game_id, guess_text, correct_letters, correct_positions, is_correct))
                conn.commit()
    
    def get_attempts_count(self, game_id):
        """Contar tentativas de um jogo"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM attempts WHERE game_id = %s
                """, (game_id,))
                return cur.fetchone()[0]
    
    def get_game_attempts(self, game_id):
        """Buscar tentativas de um jogo"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, guess_text, correct_letters, correct_positions, 
                           is_correct, created_at
                    FROM attempts 
                    WHERE game_id = %s 
                    ORDER BY created_at ASC
                """, (game_id,))
                return cur.fetchall()
    
    def complete_game(self, game_id):
        """Marcar jogo como completado"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE games 
                    SET is_completed = TRUE, completed_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (game_id,))
                conn.commit()


def get_repository():
    """Factory function para obter repositório"""
    db_type = os.getenv('FLASK_DB_TYPE', 'postgres')
    
    if db_type == 'postgres':
        return PostgresRepository()
    else:
        raise ValueError(f"Tipo de banco não suportado: {db_type}")
