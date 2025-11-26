from dataclasses import dataclass
from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.password_hasher import PasswordHasher
from app.domain.value_objects.email import Email


@dataclass
class AuthenticateUserDTO:
    email: str
    password: str


class AuthenticateUserUseCase:
    """
    Caso de uso: Autenticar un usuario
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, data: AuthenticateUserDTO) -> Optional[User]:
        # 1) Buscar usuario por email
        email_vo = Email(data.email)
        user = self.user_repository.get_by_email(email_vo)
        
        if not user:
            return None
        
        # 2) Verificar que esté activo
        if not user.is_active:
            raise ValueError("Usuario inactivo")
        
        # 3) Verificar contraseña
        if not self.password_hasher.verify(data.password, user.password_hash.value):
            return None
        
        return user