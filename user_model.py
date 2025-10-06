from dataclasses import dataclass

@dataclass
class User:
    """Modelo básico de Usuario"""
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
