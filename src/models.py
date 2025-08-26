from typing import Dict
from uuid import UUID, uuid4


class User:
    def __init__(self, name: str, email: str, balance: float):
        self.id = uuid4()
        self.name = name
        self.email = email
        self.balance = balance


class InMemoryStorage:
    def __init__(self):
        self.users: Dict[UUID, User] = {}
        self.emails: set = set()


storage = InMemoryStorage()
