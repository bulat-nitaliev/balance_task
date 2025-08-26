import pytest
from fastapi import status
from src.schemas import UserResponse


class TestUsersAPI:
    def test_create_user_success(self, client):
        """Тест успешного создания пользователя через API"""
        response = client.post(
            "/users",
            json={"name": "Test User", "email": "test@example.com", "balance": 100.0},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
        assert data["balance"] == 100.0
        assert "id" in data

    def test_create_user_duplicate_email(self, client):
        """Тест создания пользователя с дублирующимся email через API"""
        client.post(
            "/users",
            json={"name": "User1", "email": "test@example.com", "balance": 100.0},
        )

        response = client.post(
            "/users",
            json={"name": "User2", "email": "test@example.com", "balance": 200.0},
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    def test_create_user_negative_balance(self, client):
        """Тест создания пользователя с отрицательным балансом"""
        response = client.post(
            "/users",
            json={"name": "Test User", "email": "test@example.com", "balance": -50.0},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_users_empty(self, client):
        """Тест получения пустого списка пользователей"""
        response = client.get("/users")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_users_with_data(self, client, sample_users):
        """Тест получения списка пользователей с данными"""
        response = client.get("/users")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert {user["email"] for user in data} == {
            "alice@example.com",
            "bob@example.com",
            "charlie@example.com",
        }

    def test_create_user_invalid_email(self, client):
        """Тест создания пользователя с невалидным email"""
        response = client.post(
            "/users",
            json={"name": "Test User", "email": "invalid-email", "balance": 100.0},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTransferAPI:
    def test_transfer_success(self, client, sample_users):
        """Тест успешного перевода через API"""
        alice, bob, _ = sample_users

        response = client.post(
            "/transfer",
            json={
                "from_user_id": str(alice.id),
                "to_user_id": str(bob.id),
                "amount": 100.0,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Transfer successful"
        assert data["from_user_balance"] == 900.0
        assert data["to_user_balance"] == 600.0

    def test_transfer_insufficient_funds(self, client, sample_users):
        """Тест перевода при недостатке средств через API"""
        alice, bob, _ = sample_users

        response = client.post(
            "/transfer",
            json={
                "from_user_id": str(bob.id),
                "to_user_id": str(alice.id),
                "amount": 600.0,  # У Bob только 500
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Insufficient funds" in response.json()["detail"]

    def test_transfer_self(self, client, sample_users):
        """Тест перевода самому себе через API"""
        alice, _, _ = sample_users

        response = client.post(
            "/transfer",
            json={
                "from_user_id": str(alice.id),
                "to_user_id": str(alice.id),
                "amount": 100.0,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "yourself" in response.json()["detail"].lower()

    def test_transfer_user_not_found(self, client, sample_users):
        """Тест перевода с несуществующим пользователем через API"""
        import uuid

        alice, _, _ = sample_users
        fake_id = str(uuid.uuid4())

        response = client.post(
            "/transfer",
            json={
                "from_user_id": fake_id,
                "to_user_id": str(alice.id),
                "amount": 100.0,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_transfer_invalid_uuid(self, client):
        """Тест перевода с невалидным UUID"""
        response = client.post(
            "/transfer",
            json={
                "from_user_id": "invalid-uuid",
                "to_user_id": "also-invalid",
                "amount": 100.0,
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_transfer_zero_amount(self, client, sample_users):
        """Тест перевода нулевой суммы через API"""
        alice, bob, _ = sample_users

        response = client.post(
            "/transfer",
            json={
                "from_user_id": str(alice.id),
                "to_user_id": str(bob.id),
                "amount": 0.0,
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_transfer_negative_amount(self, client, sample_users):
        """Тест перевода отрицательной суммы через API"""
        alice, bob, _ = sample_users

        response = client.post(
            "/transfer",
            json={
                "from_user_id": str(alice.id),
                "to_user_id": str(bob.id),
                "amount": -50.0,
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestHealthCheck:
    def test_health_check(self, client):
        """Тест health check endpoint"""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"
        assert response.json()["users_count"] == 0

    def test_health_check_with_users(self, client, sample_users):
        """Тест health check с пользователями"""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["users_count"] == 3
