from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.domain.value_objects.email import Email
from app.domain.value_objects.password_hash import PasswordHash
from app.domain.value_objects.role import Role


@dataclass
class User:
    id: Optional[int]
    email: Email
    password_hash: PasswordHash
    username: str
    role: Role
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        email: Email,
        password_hash: PasswordHash,
        username: str,
        role: Role = Role.CLIENTE,
    ):
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            email=email,
            password_hash=password_hash,
            username=username,
            role=role,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def change_password(self, new_password_hash: PasswordHash):
        self.password_hash = new_password_hash
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)