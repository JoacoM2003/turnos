from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.user import User
from app.domain.value_objects.email import Email


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
