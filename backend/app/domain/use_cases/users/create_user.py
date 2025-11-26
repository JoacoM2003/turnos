from dataclasses import dataclass

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.password_hasher import PasswordHasher
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
    """
    Caso de uso: Crear un nuevo usuario.
    Orquesta la lógica de aplicación sin dependencias de infraestructura.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, data: CreateUserDTO) -> User:
        # 1) Validar y crear value object de email
        email_vo = Email(data.email)

        # 2) Verificar que no exista el email
        existing = self.user_repository.get_by_email(email_vo)
        if existing:
            raise ValueError("Email already registered")

        # 3) Hashear contraseña
        hashed_password = self.password_hasher.hash(data.password)

        # 4) Crear entidad usando factory method
        user = User.create(
            email=email_vo,
            password_hash=PasswordHash(hashed_password),
            username=data.username,
            role=Role(data.role)
        )

        # 5) Persistir
        saved_user = self.user_repository.save(user)

        return saved_user