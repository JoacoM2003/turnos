from app.domain.entities.cliente import Cliente
from app.infrastructure.db.models.cliente_model import ClienteModel


class ClienteMapper:
    """
    Mapper entre entidad Cliente y modelo ClienteModel
    """

    @staticmethod
    def to_entity(model: ClienteModel) -> Cliente:
        """Convierte un modelo de DB a entidad de dominio"""
        return Cliente(
            id=model.id,
            user_id=model.user_id,
            nombre=model.nombre,
            apellido=model.apellido,
            telefono=model.telefono,
            dni=model.dni,
            fecha_nacimiento=model.fecha_nacimiento,
            direccion=model.direccion,
            notas=model.notas,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Cliente) -> ClienteModel:
        """Convierte una entidad de dominio a modelo de DB"""
        model = ClienteModel(
            id=entity.id,
            user_id=entity.user_id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            telefono=entity.telefono,
            dni=entity.dni,
            fecha_nacimiento=entity.fecha_nacimiento,
            direccion=entity.direccion,
            notas=entity.notas,
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def update_model_from_entity(model: ClienteModel, entity: Cliente) -> None:
        """Actualiza un modelo existente con datos de la entidad"""
        model.nombre = entity.nombre
        model.apellido = entity.apellido
        model.telefono = entity.telefono
        model.dni = entity.dni
        model.fecha_nacimiento = entity.fecha_nacimiento
        model.direccion = entity.direccion
        model.notas = entity.notas
        model.updated_at = entity.updated_at