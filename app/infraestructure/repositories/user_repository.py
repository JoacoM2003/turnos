from typing import Optional, List, Callable
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_mapper import UserMapper


class SQLAlchemyUserRepository(UserRepository):
    """
    Repositorio SQLAlchemy limpio:
    - No contiene lógica de dominio.
    - Usa session_factory para evitar acoplamiento.
    - Mapper se encarga de las conversiones.
    """

    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    # QUERIES
    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.session_factory() as db:
            model = db.query(UserModel).filter(UserModel.id == user_id).first()
            return UserMapper.to_entity(model) if model else None

    def get_by_email(self, email: Email) -> Optional[User]:
        with self.session_factory() as db:
            model = db.query(UserModel).filter(UserModel.email == email.value).first()
            return UserMapper.to_entity(model) if model else None

    def list(self) -> List[User]:
        with self.session_factory() as db:
            models = db.query(UserModel).all()
            return [UserMapper.to_entity(m) for m in models]

    # COMMANDS
    def save(self, user: User) -> User:
        """
        Inserta o actualiza, delegando la mutación al mapper.
        Respeta la idea de “repositorio como colección”.
        """
        with self.session_factory() as db:
            if user.id is not None:
                model = db.query(UserModel).filter(UserModel.id == user.id).first()
                if not model:
                    raise ValueError("User not found.")

                # Delegamos lógica al mapper
                UserMapper.update_model(model, user)

            else:
                model = UserMapper.to_model(user)
                db.add(model)

            db.commit()
            db.refresh(model)
            return UserMapper.to_entity(model)

    def delete(self, user_id: int) -> None:
        with self.session_factory() as db:
            model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not model:
                return
            db.delete(model)
            db.commit()
