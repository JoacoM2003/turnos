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
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    @classmethod
    def create(
        cls,
        email: Email,
        password_hash: PasswordHash,
        username: str,
        role: Role = Role.USER,
    ):
        now = datetime.now(timezone.utc)

        return cls(
            id=None,
            email=email,
            password_hash=password_hash,
            username=username,
            role=role,
            created_at=now,
            updated_at=now,
            is_active=True,
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

    def update_profile(self, username: Optional[str] = None):
        if username:
            if len(username) < 3:
                raise ValueError("Username too short")
            self.username = username

        self.updated_at = datetime.now(timezone.utc)
