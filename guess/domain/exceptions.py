class DomainException(Exception):
    pass


class UserAlreadyExistsException(DomainException):
    pass


class InvalidCredentialsException(DomainException):
    pass


class GameNotFoundException(DomainException):
    pass


class UnauthorizedAccessException(DomainException):
    pass


class GameCompletedException(DomainException):
    pass


class MaxAttemptsExceededException(DomainException):
    pass


class InvalidGuessException(DomainException):
    def __init__(self, message: str, correct_letters: int = 0, correct_positions: int = 0):
        super().__init__(message)
        self.correct_letters = correct_letters
        self.correct_positions = correct_positions
