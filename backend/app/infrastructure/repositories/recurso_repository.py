from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.recurso import Recurso
from app.domain.repositories.recurso_repository import RecursoRepository
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.mappers.recurso_mapper import RecursoMapper


class SQLAlchemyRecursoRepository(RecursoRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, recurso: Recurso) -> Recurso:
        if recurso.id is not None:
            model = self.session.query(RecursoModel).filter(
                RecursoModel.id == recurso.id
            ).first()
            if not model:
                raise ValueError(f"Recurso with id {recurso.id} not found")
            
            model.nombre = recurso.nombre
            model.descripcion = recurso.descripcion
            model.capacidad = recurso.capacidad
            model.imagen_url = recurso.imagen_url
            model.caracteristicas = recurso.caracteristicas
            model.is_active = recurso.is_active
            model.orden = recurso.orden
            model.updated_at = recurso.updated_at
        else:
            model = RecursoMapper.to_model(recurso)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return RecursoMapper.to_entity(model)

    def get_by_id(self, recurso_id: int) -> Optional[Recurso]:
        model = self.session.query(RecursoModel).filter(
            RecursoModel.id == recurso_id
        ).first()
        return RecursoMapper.to_entity(model) if model else None

    def list_by_servicio(self, servicio_id: int) -> List[Recurso]:
        models = self.session.query(RecursoModel).filter(
            RecursoModel.servicio_id == servicio_id,
            RecursoModel.is_active == True
        ).order_by(RecursoModel.orden).all()
        
        return [RecursoMapper.to_entity(m) for m in models]

    def delete(self, recurso_id: int) -> None:
        model = self.session.query(RecursoModel).filter(
            RecursoModel.id == recurso_id
        ).first()
        if model:
            self.session.delete(model)
            self.session.commit()