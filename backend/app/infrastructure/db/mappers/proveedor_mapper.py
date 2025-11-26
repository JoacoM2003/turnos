from app.domain.entities.proveedor import Proveedor
from app.infrastructure.db.models.proveedor_model import ProveedorModel


class ProveedorMapper:
    """
    Mapper entre entidad Proveedor y modelo ProveedorModel
    """

    @staticmethod
    def to_entity(model: ProveedorModel) -> Proveedor:
        """Convierte un modelo de DB a entidad de dominio"""
        return Proveedor(
            id=model.id,
            user_id=model.user_id,
            nombre=model.nombre,
            apellido=model.apellido,
            especialidad=model.especialidad,
            matricula=model.matricula,
            telefono=model.telefono,
            biografia=model.biografia,
            foto_url=model.foto_url,
            is_available=model.is_available,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Proveedor) -> ProveedorModel:
        """Convierte una entidad de dominio a modelo de DB"""
        model = ProveedorModel(
            id=entity.id,
            user_id=entity.user_id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            especialidad=entity.especialidad,
            matricula=entity.matricula,
            telefono=entity.telefono,
            biografia=entity.biografia,
            foto_url=entity.foto_url,
            is_available=entity.is_available,
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def update_model_from_entity(model: ProveedorModel, entity: Proveedor) -> None:
        """Actualiza un modelo existente con datos de la entidad"""
        model.nombre = entity.nombre
        model.apellido = entity.apellido
        model.especialidad = entity.especialidad
        model.matricula = entity.matricula
        model.telefono = entity.telefono
        model.biografia = entity.biografia
        model.foto_url = entity.foto_url
        model.is_available = entity.is_available
        model.updated_at = entity.updated_at