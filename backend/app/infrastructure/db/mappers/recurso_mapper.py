from app.domain.entities.recurso import Recurso
from app.infrastructure.db.models.recurso_model import RecursoModel


class RecursoMapper:
    
    @staticmethod
    def to_entity(model: RecursoModel) -> Recurso:
        return Recurso(
            id=model.id,
            servicio_id=model.servicio_id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            capacidad=model.capacidad,
            imagen_url=model.imagen_url,
            caracteristicas=model.caracteristicas,
            is_active=model.is_active,
            orden=model.orden,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: Recurso) -> RecursoModel:
        model = RecursoModel(
            id=entity.id,
            servicio_id=entity.servicio_id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            capacidad=entity.capacidad,
            imagen_url=entity.imagen_url,
            caracteristicas=entity.caracteristicas,
            is_active=entity.is_active,
            orden=entity.orden
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model