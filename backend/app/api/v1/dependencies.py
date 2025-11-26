from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_session

# Repositorios
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.cliente_repository import ClienteRepository
from app.domain.repositories.proveedor_repository import ProveedorRepository
from app.domain.repositories.servicio_repository import ServicioRepository
from app.domain.repositories.recurso_repository import RecursoRepository
from app.domain.repositories.reserva_repository import ReservaRepository

from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
from app.infrastructure.repositories.servicio_repository import SQLAlchemyServicioRepository
from app.infrastructure.repositories.recurso_repository import SQLAlchemyRecursoRepository
from app.infrastructure.repositories.reserva_repository import SQLAlchemyReservaRepository

# Servicios
from app.domain.services.password_hasher import PasswordHasher
from app.infrastructure.services.bcrypt_password_hasher import BcryptPasswordHasher

# Use Cases
from app.domain.use_cases.users.create_user import CreateUserUseCase
from app.domain.use_cases.users.authenticate_user import AuthenticateUserUseCase


# ===== REPOSITORIOS =====

def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_cliente_repository(session: Session = Depends(get_session)) -> ClienteRepository:
    return SQLAlchemyClienteRepository(session)


def get_proveedor_repository(session: Session = Depends(get_session)) -> ProveedorRepository:
    return SQLAlchemyProveedorRepository(session)


def get_servicio_repository(session: Session = Depends(get_session)) -> ServicioRepository:
    return SQLAlchemyServicioRepository(session)


def get_recurso_repository(session: Session = Depends(get_session)) -> RecursoRepository:
    return SQLAlchemyRecursoRepository(session)


def get_reserva_repository(session: Session = Depends(get_session)) -> ReservaRepository:
    return SQLAlchemyReservaRepository(session)


# ===== SERVICIOS =====

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


# ===== USE CASES =====

def get_create_user_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo, password_hasher)


def get_authenticate_user_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repo, password_hasher)