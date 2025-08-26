from .models import storage, User
from .exceptions import *
from uuid import UUID


class UserService:
    @staticmethod
    def create_user(name: str, email: str, balance: float):
        if email in storage.emails:
            raise UserAlreadyExistsException(f"User with email {email} already exists")

        user = User(name, email, balance)
        storage.users[user.id] = user
        storage.emails.add(email)
        return user

    @staticmethod
    def get_all_users():
        return list(storage.users.values())

    @staticmethod
    def get_user_by_id(user_id: UUID):
        if user_id not in storage.users:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return storage.users[user_id]


class TransferService:
    @staticmethod
    def validate_amount(amount: float):
        """Валидация суммы перевода"""
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

    @staticmethod
    def make_transfer(from_user_id: UUID, to_user_id: UUID, amount: float):
        if from_user_id == to_user_id:
            raise SelfTransferException("Cannot transfer to yourself")

        # Валидация суммы
        TransferService.validate_amount(amount)

        from_user = UserService.get_user_by_id(from_user_id)
        to_user = UserService.get_user_by_id(to_user_id)

        if from_user.balance < amount:
            raise InsufficientFundsException(
                f"Insufficient funds. Current balance: {from_user.balance}, required: {amount}"
            )

        # Выполняем перевод атомарно
        from_user.balance -= amount
        to_user.balance += amount

        return from_user, to_user
