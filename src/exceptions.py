class AppException(Exception):
    """Базовое исключение приложения"""

    pass


class UserAlreadyExistsException(AppException):
    """Пользователь с таким email уже существует"""

    pass


class UserNotFoundException(AppException):
    """Пользователь не найден"""

    pass


class InsufficientFundsException(AppException):
    """Недостаточно средств"""

    pass


class SelfTransferException(AppException):
    """Нельзя переводить самому себе"""

    pass
