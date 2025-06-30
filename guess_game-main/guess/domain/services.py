import bcrypt
from .entities import GuessResult
from .exceptions import InvalidGuessException


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


class GuessService:
    def __init__(self, secret_word: str):
        self.secret_word = secret_word.lower()
    
    def evaluate_guess(self, guess: str) -> GuessResult:
        guess = guess.lower()
        
        if len(guess) < len(self.secret_word):
            raise InvalidGuessException("Sua tentativa é muito curta", 0, 0)
        
        if len(guess) > len(self.secret_word):
            raise InvalidGuessException("Sua tentativa é muito longa", 0, 0)
        
        correct_positions, correct_letters = self._compare_strings(guess)
        
        if correct_positions == len(self.secret_word):
            return GuessResult(
                is_correct=True,
                correct_letters=correct_letters,
                correct_positions=correct_positions,
                message="Parabéns! Você acertou!"
            )
        
        message = self._build_feedback_message(correct_positions, correct_letters)
        raise InvalidGuessException(message, correct_letters, correct_positions)
    
    def _compare_strings(self, guess: str) -> tuple[int, int]:
        correct_positions = 0
        correct_letters = 0
        target_counted = [False] * len(self.secret_word)
        
        for i in range(len(self.secret_word)):
            if guess[i] == self.secret_word[i]:
                correct_positions += 1
                target_counted[i] = True
        
        for i in range(len(guess)):
            if guess[i] != self.secret_word[i]:
                for j in range(len(self.secret_word)):
                    if guess[i] == self.secret_word[j] and not target_counted[j]:
                        correct_letters += 1
                        target_counted[j] = True
                        break
        
        return correct_positions, correct_letters
    
    def _build_feedback_message(self, correct_positions: int, correct_letters: int) -> str:
        total_letters = len(self.secret_word)
        
        position_word = "posição" if correct_positions == 1 else "posições"
        letter_word = "letra" if correct_letters == 1 else "letras"
        total_word = "letra" if total_letters == 1 else "letras"
        
        return (f"Incorreto, mas você acertou {correct_positions} {letter_word} "
                f"na {position_word} correta, {correct_letters} em posição errada, "
                f"de {total_letters} {total_word} no total")
