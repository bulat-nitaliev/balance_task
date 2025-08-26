import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models import storage, User
from src.services import UserService


@pytest.fixture(autouse=True)
def clean_storage():
    """Очищаем хранилище перед каждым тестом"""
    storage.users.clear()
    storage.emails.clear()
    yield


@pytest.fixture
def client():
    """Тестовый клиент FastAPI"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_users():
    """Фикстура с тестовыми пользователями"""
    users_data = [
        {"name": "Alice", "email": "alice@example.com", "balance": 1000.0},
        {"name": "Bob", "email": "bob@example.com", "balance": 500.0},
        {"name": "Charlie", "email": "charlie@example.com", "balance": 200.0},
    ]

    users = []
    for user_data in users_data:
        user = UserService.create_user(
            user_data["name"], user_data["email"], user_data["balance"]
        )
        users.append(user)

    return users
