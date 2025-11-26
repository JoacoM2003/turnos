from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.password_hash import PasswordHash
from app.domain.value_objects.role import Role
from app.infrastructure.db.models.user_model import UserModel


class UserMapper:
    """
    Mapper entre entidad User y modelo UserModel.
    Responsable de las conversiones bidireccionales.
    """

    @staticmethod
    def to_entity(model: UserModel) -> User:
        """Convierte un modelo de DB a entidad de dominio"""
        return User(
            id=model.id,
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash),
            username=model.username,
            role=Role(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        """Convierte una entidad de dominio a modelo de DB"""
        model = UserModel(
            id=entity.id,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            username=entity.username,
            role=entity.role.value,
            is_active=entity.is_active,
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def update_model_from_entity(model: UserModel, entity: User) -> None:
        """Actualiza un modelo existente con datos de la entidad"""
        model.email = entity.email.value
        model.password_hash = entity.password_hash.value
        model.username = entity.username
        model.role = entity.role.value
        model.is_active = entity.is_active
        model.updated_at = entity.updated_at
