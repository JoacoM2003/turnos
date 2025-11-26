from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_mapper import UserMapper


class SQLAlchemyUserRepository(UserRepository):
    """
    Implementación del repositorio de usuarios usando SQLAlchemy.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return UserMapper.to_entity(model) if model else None

    def get_by_email(self, email: Email) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.email == email.value).first()
        return UserMapper.to_entity(model) if model else None

    def list(self) -> List[User]:
        models = self.session.query(UserModel).all()
        return [UserMapper.to_entity(m) for m in models]

    def save(self, user: User) -> User:
        """
        Guarda o actualiza un usuario.
        Si tiene ID, actualiza; si no, inserta.
        """
        if user.id is not None:
            # Actualizar usuario existente
            model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
            if not model:
                raise ValueError(f"User with id {user.id} not found")
            
            UserMapper.update_model_from_entity(model, user)
        else:
            # Crear nuevo usuario
            model = UserMapper.to_model(user)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return UserMapper.to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()