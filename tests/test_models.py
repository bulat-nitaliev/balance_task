import pytest
from uuid import UUID
from src.models import User, InMemoryStorage


class TestUserModel:
    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User("Test User", "test@example.com", 100.0)

        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.balance == 100.0
        assert isinstance(user.id, UUID)


class TestInMemoryStorage:
    def test_storage_initialization(self):
        """Тест инициализации хранилища"""
        storage = InMemoryStorage()

        assert storage.users == {}
        assert storage.emails == set()

    def test_storage_singleton(self):
        """Тест что storage является синглтоном"""
        from src.models import storage as storage1
        from src.models import storage as storage2

        assert storage1 is storage2
