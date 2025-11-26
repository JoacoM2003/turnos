from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.servicio import Servicio
from app.domain.repositories.servicio_repository import ServicioRepository
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.infrastructure.db.mappers.servicio_mapper import ServicioMapper


class SQLAlchemyServicioRepository(ServicioRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, servicio: Servicio) -> Servicio:
        if servicio.id is not None:
            model = self.session.query(ServicioModel).filter(
                ServicioModel.id == servicio.id
            ).first()
            if not model:
                raise ValueError(f"Servicio with id {servicio.id} not found")
            
            model.nombre = servicio.nombre
            model.descripcion = servicio.descripcion
            model.categoria = servicio.categoria
            model.is_active = servicio.is_active
            model.updated_at = servicio.updated_at
        else:
            model = ServicioMapper.to_model(servicio)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return ServicioMapper.to_entity(model)

    def get_by_id(self, servicio_id: int) -> Optional[Servicio]:
        model = self.session.query(ServicioModel).filter(
            ServicioModel.id == servicio_id
        ).first()
        return ServicioMapper.to_entity(model) if model else None

    def list_by_proveedor(self, proveedor_id: int) -> List[Servicio]:
        models = self.session.query(ServicioModel).filter(
            ServicioModel.proveedor_id == proveedor_id
        ).all()
        return [ServicioMapper.to_entity(m) for m in models]

    def search(self, nombre: Optional[str] = None, categoria: Optional[str] = None) -> List[Servicio]:
        query = self.session.query(ServicioModel).filter(
            ServicioModel.is_active == True
        )
        
        if nombre:
            query = query.filter(ServicioModel.nombre.ilike(f'%{nombre}%'))
        
        if categoria:
            query = query.filter(ServicioModel.categoria == categoria)
        
        models = query.all()
        return [ServicioMapper.to_entity(m) for m in models]

    def delete(self, servicio_id: int) -> None:
        model = self.session.query(ServicioModel).filter(
            ServicioModel.id == servicio_id
        ).first()
        if model:
            self.session.delete(model)
            self.session.commit()