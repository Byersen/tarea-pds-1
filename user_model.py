from dataclasses import dataclass
from typing import Optional, Dict, List
import uuid

@dataclass
class User:
    id: str
    name: str
    email: str
    age: int
    active: bool = True

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        if self.age < 0 or self.age > 150:
            raise ValueError("Age must be between 0 and 150")


class UserRepository:
    """Repositorio simple para operaciones CRUD de usuarios"""

    def __init__(self):
        self._users: Dict[str, User] = {}

    def create(self, name: str, email: str, age: int, active: bool = True) -> User:
        user_id = str(uuid.uuid4())
        user = User(id=user_id, name=name, email=email, age=age, active=active)
        self._users[user_id] = user
        return user

    def read(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def update(self, user_id: str, name: Optional[str] = None, 
               email: Optional[str] = None, age: Optional[int] = None, 
               active: Optional[bool] = None) -> Optional[User]:
        if user_id not in self._users:
            return None

        user = self._users[user_id]
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if age is not None:
            user.age = age
        if active is not None:
            user.active = active

        # Validar después de actualizar
        User(user.id, user.name, user.email, user.age, user.active)
        return user

    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_all(self) -> List[User]:
        return list(self._users.values())

    def clear(self):
        self._users.clear()
