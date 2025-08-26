import pytest
from uuid import UUID, uuid4
from src.services import UserService, TransferService
from src.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InsufficientFundsException,
    SelfTransferException,
)


class TestUserService:
    def test_create_user_success(self):
        """Тест успешного создания пользователя"""
        user = UserService.create_user("Test", "test@example.com", 100.0)

        assert user.name == "Test"
        assert user.email == "test@example.com"
        assert user.balance == 100.0
        assert isinstance(user.id, UUID)

    def test_create_user_duplicate_email(self):
        """Тест создания пользователя с дублирующимся email"""
        UserService.create_user("Test1", "test@example.com", 100.0)

        with pytest.raises(UserAlreadyExistsException):
            UserService.create_user("Test2", "test@example.com", 200.0)

    def test_get_all_users(self):
        """Тест получения всех пользователей"""
        UserService.create_user("User1", "user1@example.com", 100.0)
        UserService.create_user("User2", "user2@example.com", 200.0)

        users = UserService.get_all_users()
        assert len(users) == 2
        assert {user.email for user in users} == {
            "user1@example.com",
            "user2@example.com",
        }

    def test_get_user_by_id_success(self):
        """Тест успешного получения пользователя по ID"""
        user = UserService.create_user("Test", "test@example.com", 100.0)
        found_user = UserService.get_user_by_id(user.id)

        assert found_user.id == user.id
        assert found_user.name == user.name

    def test_get_user_by_id_not_found(self):
        """Тест получения несуществующего пользователя"""
        fake_id = uuid4()

        with pytest.raises(UserNotFoundException):
            UserService.get_user_by_id(fake_id)


class TestTransferService:
    def test_transfer_success(self, sample_users):
        """Тест успешного перевода"""
        alice, bob, _ = sample_users

        from_user, to_user = TransferService.make_transfer(alice.id, bob.id, 100.0)

        assert from_user.balance == 900.0  # 1000 - 100
        assert to_user.balance == 600.0  # 500 + 100

    def test_transfer_insufficient_funds(self, sample_users):
        """Тест перевода при недостатке средств"""
        alice, bob, _ = sample_users

        with pytest.raises(InsufficientFundsException):
            TransferService.make_transfer(bob.id, alice.id, 600.0)  # У Bob только 500

    def test_transfer_self(self, sample_users):
        """Тест перевода самому себе"""
        alice, _, _ = sample_users

        with pytest.raises(SelfTransferException):
            TransferService.make_transfer(alice.id, alice.id, 100.0)

    def test_transfer_user_not_found(self, sample_users):
        """Тест перевода с несуществующим пользователем"""
        alice, _, _ = sample_users
        fake_id = uuid4()

        with pytest.raises(UserNotFoundException):
            TransferService.make_transfer(alice.id, fake_id, 100.0)

        with pytest.raises(UserNotFoundException):
            TransferService.make_transfer(fake_id, alice.id, 100.0)

    def test_transfer_zero_amount(self, sample_users):
        """Тест перевода нулевой суммы"""
        alice, bob, _ = sample_users

        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            TransferService.make_transfer(alice.id, bob.id, 0.0)

    def test_transfer_negative_amount(self, sample_users):
        """Тест перевода отрицательной суммы"""
        alice, bob, _ = sample_users

        with pytest.raises(ValueError, match="Amount must be greater than 0"):
            TransferService.make_transfer(alice.id, bob.id, -50.0)
