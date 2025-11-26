from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.cliente import Cliente
from app.domain.repositories.cliente_repository import ClienteRepository
from app.infrastructure.db.models.cliente_model import ClienteModel
from app.infrastructure.db.mappers.cliente_mapper import ClienteMapper


class SQLAlchemyClienteRepository(ClienteRepository):
    """
    Implementación del repositorio de clientes usando SQLAlchemy
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        model = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente_id
        ).first()
        return ClienteMapper.to_entity(model) if model else None

    def get_by_user_id(self, user_id: int) -> Optional[Cliente]:
        model = self.session.query(ClienteModel).filter(
            ClienteModel.user_id == user_id
        ).first()
        return ClienteMapper.to_entity(model) if model else None

    def list(self) -> List[Cliente]:
        models = self.session.query(ClienteModel).all()
        return [ClienteMapper.to_entity(m) for m in models]

    def save(self, cliente: Cliente) -> Cliente:
        """
        Guarda o actualiza un cliente
        """
        if cliente.id is not None:
            # Actualizar cliente existente
            model = self.session.query(ClienteModel).filter(
                ClienteModel.id == cliente.id
            ).first()
            if not model:
                raise ValueError(f"Cliente with id {cliente.id} not found")
            
            ClienteMapper.update_model_from_entity(model, cliente)
        else:
            # Crear nuevo cliente
            model = ClienteMapper.to_model(cliente)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return ClienteMapper.to_entity(model)

    def delete(self, cliente_id: int) -> None:
        model = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente_id
        ).first()
        if model:
            self.session.delete(model)
            self.session.commit()
