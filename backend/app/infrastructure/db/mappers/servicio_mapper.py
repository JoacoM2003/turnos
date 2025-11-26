from app.domain.entities.servicio import Servicio
from app.infrastructure.db.models.servicio_model import ServicioModel


class ServicioMapper:
    
    @staticmethod
    def to_entity(model: ServicioModel) -> Servicio:
        return Servicio(
            id=model.id,
            proveedor_id=model.proveedor_id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            categoria=model.categoria,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: Servicio) -> ServicioModel:
        model = ServicioModel(
            id=entity.id,
            proveedor_id=entity.proveedor_id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            categoria=entity.categoria,
            is_active=entity.is_active
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model