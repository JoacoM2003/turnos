from dataclasses import dataclass

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.password_hash import PasswordHash
from app.domain.value_objects.role import Role


@dataclass
class CreateUserDTO:
    email: str
    password: str
    username: str
    role: str = "user"


class CreateUserUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher  # interfaz, no bcrypt directamente

    def execute(self, data: CreateUserDTO) -> User:
        # 1) Validar email y convertir a value object
        email_vo = Email(data.email)

        # 2) Verificar si ya existe
        existing = self.user_repository.get_by_email(email_vo)
        if existing:
            raise ValueError("Email already registered")

        # 3) Hash del password
        hashed_password = self.password_hasher.hash(data.password)

        # 4) Crear entidad
        user = User(
            id=None,
            email=email_vo,
            password_hash=PasswordHash(hashed_password),
            username=data.username,
            role=Role(data.role)
        )

        # 5) Guardar en repositorio
        saved_user = self.user_repository.save(user)

        return saved_user
