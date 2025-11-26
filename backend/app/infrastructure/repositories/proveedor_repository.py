from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.proveedor import Proveedor
from app.domain.repositories.proveedor_repository import ProveedorRepository
from app.infrastructure.db.models.proveedor_model import ProveedorModel
from app.infrastructure.db.mappers.proveedor_mapper import ProveedorMapper


class SQLAlchemyProveedorRepository(ProveedorRepository):
    """
    Implementación del repositorio de proveedores usando SQLAlchemy
    """

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, proveedor_id: int) -> Optional[Proveedor]:
        model = self.session.query(ProveedorModel).filter(
            ProveedorModel.id == proveedor_id
        ).first()
        return ProveedorMapper.to_entity(model) if model else None

    def get_by_user_id(self, user_id: int) -> Optional[Proveedor]:
        model = self.session.query(ProveedorModel).filter(
            ProveedorModel.user_id == user_id
        ).first()
        return ProveedorMapper.to_entity(model) if model else None

    def list(self, is_available: Optional[bool] = None) -> List[Proveedor]:
        query = self.session.query(ProveedorModel)
        
        if is_available is not None:
            query = query.filter(ProveedorModel.is_available == is_available)
        
        models = query.all()
        return [ProveedorMapper.to_entity(m) for m in models]

    def list_by_especialidad(self, especialidad: str) -> List[Proveedor]:
        models = self.session.query(ProveedorModel).filter(
            ProveedorModel.especialidad == especialidad,
            ProveedorModel.is_available == True
        ).all()
        return [ProveedorMapper.to_entity(m) for m in models]

    def save(self, proveedor: Proveedor) -> Proveedor:
        """
        Guarda o actualiza un proveedor
        """
        if proveedor.id is not None:
            # Actualizar proveedor existente
            model = self.session.query(ProveedorModel).filter(
                ProveedorModel.id == proveedor.id
            ).first()
            if not model:
                raise ValueError(f"Proveedor with id {proveedor.id} not found")
            
            ProveedorMapper.update_model_from_entity(model, proveedor)
        else:
            # Crear nuevo proveedor
            model = ProveedorMapper.to_model(proveedor)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return ProveedorMapper.to_entity(model)

    def delete(self, proveedor_id: int) -> None:
        model = self.session.query(ProveedorModel).filter(
            ProveedorModel.id == proveedor_id
        ).first()
        if model:
            self.session.delete(model)
            self.session.commit()
